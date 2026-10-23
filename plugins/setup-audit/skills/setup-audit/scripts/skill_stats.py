#!/usr/bin/env python3
"""Inventory every installed skill and count real usage from Claude Code session logs.

Read-only. Prints a summary table and writes full JSON. Never prints message text:
only skill names, counts, dates, paths, and word counts leave this script.

Usage:
    python3 -I skill_stats.py [--days 90] [--json OUT.json] [--project DIR ...]
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

HOME = os.path.expanduser("~")
CODE_EXT = {".py", ".js", ".ts", ".mjs", ".cjs", ".sh", ".bash", ".zsh", ".rb", ".go", ".swift"}
CMD_RE = re.compile(r"<command-name>/?([^<\s]+)</command-name>")


def read_frontmatter(text):
    """Return (name, description, body) from a SKILL.md. Tolerates folded/multiline YAML values."""
    name, desc, body = None, "", text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm, body = text[3:end], text[end + 4:]
            lines = fm.splitlines()
            i = 0
            while i < len(lines):
                m = re.match(r"^(name|description):\s*(.*)$", lines[i])
                if m:
                    key, val = m.group(1), m.group(2).strip()
                    if val in ("", ">", "|", ">-", "|-"):
                        parts = []
                        while i + 1 < len(lines) and (lines[i + 1].startswith((" ", "\t")) or not lines[i + 1].strip()):
                            i += 1
                            parts.append(lines[i].strip())
                        val = " ".join(p for p in parts if p)
                    val = val.strip().strip('"').strip("'")
                    if key == "name":
                        name = val
                    else:
                        desc = val
                i += 1
    return name, desc, body


def scan_skill_dir(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return None
    name, desc, _ = read_frontmatter(text)
    files, has_code, newest = 0, False, os.path.getmtime(path)
    for root, dirs, fnames in os.walk(skill_dir, followlinks=False):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", ".venv")]
        for f in fnames:
            files += 1
            fp = os.path.join(root, f)
            if os.path.splitext(f)[1].lower() in CODE_EXT:
                has_code = True
            try:
                newest = max(newest, os.path.getmtime(fp))
            except OSError:
                pass
    return {
        "name": name or os.path.basename(skill_dir.rstrip("/")),
        "skill_md_words": len(text.split()),
        "description_words": len(desc.split()),
        "has_code": has_code,
        "files": files,
        "last_changed": dt.datetime.fromtimestamp(newest).date().isoformat(),
    }


def skill_dirs_under(root):
    """Yield child dirs of root that hold a SKILL.md (one level, following symlinks)."""
    if not os.path.isdir(root):
        return
    for entry in sorted(os.listdir(root)):
        d = os.path.join(root, entry)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            yield d


def build_inventory(projects):
    roots = [
        ("claude-code", "standalone", os.path.join(HOME, ".claude/skills")),
        ("codex/agents", "standalone", os.path.join(HOME, ".agents/skills")),
        ("codex", "standalone", os.path.join(HOME, ".codex/skills")),
    ]
    for p in projects:
        roots.append(("claude-code", "project:" + os.path.basename(os.path.abspath(p)), os.path.join(p, ".claude/skills")))

    plugin_roots = []
    ip = os.path.join(HOME, ".claude/plugins/installed_plugins.json")
    try:
        plugins = json.load(open(ip)).get("plugins", {})
    except (OSError, ValueError):
        plugins = {}
    for key, installs in plugins.items():
        plugin = key.split("@")[0]
        for inst in installs if isinstance(installs, list) else [installs]:
            path = inst.get("installPath")
            if path:
                plugin_roots.append((plugin, os.path.join(path, "skills")))

    by_real = {}

    def add(skill_dir, tool, source, plugin=None):
        real = os.path.realpath(skill_dir)
        info = by_real.get(real)
        if info is None:
            info = scan_skill_dir(real)
            if info is None:
                return
            info.update({"paths": [], "tools": [], "sources": [], "plugin": plugin})
            by_real[real] = info
        if skill_dir not in info["paths"]:
            info["paths"].append(skill_dir)
        if real not in info["paths"]:
            info["paths"].append(real)
        for lst, val in ((info["tools"], tool), (info["sources"], source)):
            if val not in lst:
                lst.append(val)
        if plugin and not info["plugin"]:
            info["plugin"] = plugin

    for tool, source, root in roots:
        for d in skill_dirs_under(root):
            add(d, tool, source)
    for plugin, root in plugin_roots:
        for d in skill_dirs_under(root):
            add(d, "claude-code", "plugin:" + plugin, plugin)

    checked = [r for _, _, r in roots] + [r for _, r in plugin_roots]
    return list(by_real.values()), {r: os.path.isdir(r) for r in checked}


def parse_ts(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def count_usage(days):
    now = dt.datetime.now(dt.timezone.utc)
    cutoff = now - dt.timedelta(days=days)
    base = os.path.join(HOME, ".claude/projects")
    loads, slashes = Counter(), Counter()
    sidechain = Counter()
    last = {}
    weekly = defaultdict(Counter)
    daily = defaultdict(Counter)
    seen = set()
    files = bad = 0
    first_ts = last_ts = None

    for root, _, fnames in os.walk(base):
        for f in fnames:
            if not f.endswith(".jsonl"):
                continue
            fp = os.path.join(root, f)
            try:
                if dt.datetime.fromtimestamp(os.path.getmtime(fp), dt.timezone.utc) < cutoff:
                    continue
                fh = open(fp, encoding="utf-8", errors="ignore")
            except OSError:
                continue
            files += 1
            with fh:
                for line in fh:
                    is_skill = '"name":"Skill"' in line
                    is_cmd = "<command-name>" in line
                    if not (is_skill or is_cmd):
                        continue
                    try:
                        d = json.loads(line)
                    except ValueError:
                        bad += 1
                        continue
                    if d.get("type") not in ("user", "assistant"):
                        continue
                    ts = parse_ts(d.get("timestamp"))
                    if ts is None or ts < cutoff:
                        continue
                    first_ts = min(first_ts, ts) if first_ts else ts
                    last_ts = max(last_ts, ts) if last_ts else ts
                    content = (d.get("message") or {}).get("content")
                    hits = []
                    if d["type"] == "assistant" and isinstance(content, list):
                        for b in content:
                            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                                key = ("load", b.get("id"))
                                if key in seen:
                                    continue
                                seen.add(key)
                                skill = (b.get("input") or {}).get("skill")
                                if skill:
                                    hits.append(("load", skill.lstrip("/")))
                    elif d["type"] == "user" and is_cmd:
                        text = content if isinstance(content, str) else json.dumps(content)
                        key = ("slash", d.get("uuid"))
                        if key not in seen:
                            seen.add(key)
                            hits += [("slash", m) for m in CMD_RE.findall(text)[:1]]
                    for kind, skill in hits:
                        (loads if kind == "load" else slashes)[skill] += 1
                        if d.get("isSidechain"):
                            sidechain[skill] += 1
                        week = (ts - cutoff).days // 7
                        weekly[skill][week] += 1
                        daily[skill][ts.date().isoformat()] += 1
                        if skill not in last or ts > last[skill]:
                            last[skill] = ts

    coverage = {
        "logs_root": base,
        "window_days": days,
        "window_start": cutoff.date().isoformat(),
        "window_end": now.date().isoformat(),
        "files_scanned": files,
        "unparseable_lines": bad,
        "first_event": first_ts.date().isoformat() if first_ts else None,
        "last_event": last_ts.date().isoformat() if last_ts else None,
        "codex_history": "not parsed (format unverified); Codex-only skills show unknown usage",
    }
    return loads, slashes, sidechain, last, weekly, daily, coverage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--json", help="write full results here")
    ap.add_argument("--project", action="append", default=[], help="project dir whose .claude/skills to include")
    args = ap.parse_args()

    copies, roots = build_inventory(args.project)
    loads, slashes, sidechain, last, weekly, daily, coverage = count_usage(args.days)
    weeks = (args.days + 6) // 7

    # One row per skill name. Copies of the same name (a standalone folder plus plugin
    # bundles) are listed under it, and each logged event is counted once per name.
    groups = {}
    for c in copies:
        groups.setdefault(c["name"], []).append(c)

    def base(k):
        return k.split(":", 1)[-1]

    events = defaultdict(lambda: {"loads": 0, "slashes": 0, "sidechain": 0, "last": None,
                                  "weekly": Counter(), "daily": Counter(), "qualified": Counter()})
    orphans = {}
    merged = set()  # weekly/daily/sidechain are keyed by logged name across both kinds
    for counter, kind in ((loads, "loads"), (slashes, "slashes")):
        for k, n in counter.items():
            name = base(k)
            if name not in groups:
                if kind == "loads":
                    orphans[k] = n
                continue  # unmatched slash commands are built-ins like /clear
            e = events[name]
            e[kind] += n
            if ":" in k:
                e["qualified"][k.split(":", 1)[0]] += n
            if k in merged:
                continue
            merged.add(k)
            e["sidechain"] += sidechain[k]
            e["weekly"].update(weekly[k])
            e["daily"].update(daily[k])
            if k in last and (e["last"] is None or last[k] > e["last"]):
                e["last"] = last[k]

    rows = []
    for name, cs in groups.items():
        e = events[name]
        total = e["loads"] + e["slashes"]
        for c in cs:
            c["qualified_uses"] = e["qualified"].get(c["plugin"], 0) if c["plugin"] else None
        rows.append({
            "name": name,
            "copies": len(cs),
            "copies_differ": len({c["skill_md_words"] for c in cs}) > 1,
            "sources": sorted({s for c in cs for s in c["sources"]}),
            "tools": sorted({t for c in cs for t in c["tools"]}),
            "has_code": any(c["has_code"] for c in cs),
            "description_words": max(c["description_words"] for c in cs),
            "description_words_all_copies": sum(c["description_words"] for c in cs),
            "skill_md_words": max(c["skill_md_words"] for c in cs),
            "last_changed": max(c["last_changed"] for c in cs),
            "model_loads": e["loads"],
            "slash_runs": e["slashes"],
            "subagent_uses": e["sidechain"],
            "total_uses": total,
            "uses_per_week": round(total / max(weeks, 1), 2),
            "last_used": e["last"].date().isoformat() if e["last"] else None,
            "weekly": [e["weekly"][w] for w in range(weeks)],
            "daily": dict(sorted(e["daily"].items())),
            "copy_details": cs,
        })
    rows.sort(key=lambda r: (-r["total_uses"], r["name"]))

    totals = {
        "unique_skills": len(rows),
        "skill_copies_on_disk": len(copies),
        "names_with_multiple_copies": sum(1 for r in rows if r["copies"] > 1),
        "used_in_window": sum(1 for r in rows if r["total_uses"]),
        "no_observed_use": sum(1 for r in rows if not r["total_uses"]),
        "description_words_all_copies": sum(r["description_words_all_copies"] for r in rows),
        "model_loads": sum(r["model_loads"] for r in rows),
        "slash_runs": sum(r["slash_runs"] for r in rows),
        "loads_of_skills_not_on_disk": sum(orphans.values()),
        "loads_logged": sum(loads.values()),
    }
    assert totals["model_loads"] + totals["loads_of_skills_not_on_disk"] == totals["loads_logged"], "load counts do not reconcile"
    out = {"generated": dt.date.today().isoformat(), "coverage": coverage, "roots_checked": roots,
           "totals": totals, "loads_of_skills_not_on_disk": orphans, "skills": rows}

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2, default=str)

    print(f'# skill_stats  window {coverage["window_start"]} .. {coverage["window_end"]}  '
          f'logs {coverage["files_scanned"]} files  events {coverage["first_event"]} .. {coverage["last_event"]}')
    print("# roots: " + ", ".join(f'{r} ({"ok" if ok else "missing"})' for r, ok in roots.items() if "/plugins/cache/" not in r))
    print("# totals: " + json.dumps(totals))
    if orphans:
        print("# loads of skills not on disk (built into Claude Code, or since removed/renamed): " + json.dumps(orphans))
    print(f'{"skill":36} {"copies":>6} {"uses":>5} {"model":>5} {"slash":>5} {"/wk":>5} {"last_used":>10} {"descW":>5} {"mdW":>5} code  sources')
    for r in rows:
        cp = f'{r["copies"]}{"*" if r["copies_differ"] else ""}'
        print(f'{r["name"][:36]:36} {cp:>6} {r["total_uses"]:5} {r["model_loads"]:5} {r["slash_runs"]:5} '
              f'{r["uses_per_week"]:5} {r["last_used"] or "-":>10} {r["description_words"]:5} '
              f'{r["skill_md_words"]:5} {"y" if r["has_code"] else "-":4}  {",".join(r["sources"])[:60]}')
    print("# copies marked * have different SKILL.md sizes: same name, different content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
