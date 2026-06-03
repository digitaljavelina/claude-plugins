#!/usr/bin/env python3
"""Compute Claude Code usage stats from local session transcripts.

Claude Code records no duration of its own, so "hours used" is reconstructed
from the per-message timestamps in ~/.claude/projects/**/*.jsonl. Within each
session we sum the gaps between consecutive messages, but cap any single gap at
--idle minutes so a session left open overnight does not count as hours of work.
That capped sum is the "active hours" estimate: roughly hands-on-keyboard time.

Only transcripts still on disk are visible. Claude Code prunes old sessions
(cleanupPeriodDays, default 30), so totals reach back only as far as retention.
"""

import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from datetime import datetime


def parse_ts(s):
    """Parse an ISO-8601 timestamp (handles a trailing Z) into epoch seconds."""
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except (ValueError, AttributeError):
        return None


def decode_project_dir(name):
    """Turn an encoded project-dir name back into something path-like.

    Claude Code names each project folder after the cwd with separators
    flattened to dashes, e.g. '-Users-me-code-foo'. We can't perfectly invert
    that (real dashes are ambiguous), but restoring slashes is good enough for a
    readable per-project label.
    """
    return name.replace("-", "/")


def collect(projects_dir, idle_cap):
    files = glob.glob(os.path.join(projects_dir, "**", "*.jsonl"), recursive=True)

    total_active = 0.0
    sessions_with_time = 0
    by_month = defaultdict(float)
    by_day = defaultdict(float)
    by_project = defaultdict(float)
    project_sessions = defaultdict(int)
    all_ts = []

    for fp in files:
        ts = []
        try:
            with open(fp, "r", errors="ignore") as fh:
                for line in fh:
                    # Cheap pre-filter: skip lines that can't carry a timestamp
                    # before paying for json.loads on a large transcript.
                    if '"timestamp"' not in line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    v = parse_ts(obj.get("timestamp"))
                    if v is not None:
                        ts.append(v)
        except OSError:
            continue

        if len(ts) < 2:
            continue

        ts.sort()
        sessions_with_time += 1
        all_ts.append(ts[0])
        all_ts.append(ts[-1])

        # Project label is the directory holding the transcript, relative to
        # projects_dir (the encoded cwd).
        rel = os.path.relpath(fp, projects_dir)
        project = rel.split(os.sep)[0]
        project_sessions[project] += 1

        for a, b in zip(ts, ts[1:]):
            active = min(b - a, idle_cap)
            total_active += active
            by_month[datetime.fromtimestamp(a).strftime("%Y-%m")] += active
            by_day[datetime.fromtimestamp(a).strftime("%Y-%m-%d")] += active
            by_project[project] += active

    return {
        "files": len(files),
        "sessions_with_time": sessions_with_time,
        "total_active": total_active,
        "by_month": by_month,
        "by_day": by_day,
        "by_project": by_project,
        "project_sessions": project_sessions,
        "all_ts": all_ts,
    }


def fmt_hours(seconds):
    h = seconds / 3600
    if h < 1:
        return f"{seconds/60:.0f} min"
    return f"{h:.1f} h"


def render_text(stats, idle_cap, top_projects, show_days):
    out = []
    cap_min = int(idle_cap // 60)
    out.append("Claude Code usage")
    out.append("=" * 48)

    if stats["all_ts"]:
        lo = datetime.fromtimestamp(min(stats["all_ts"])).strftime("%Y-%m-%d")
        hi = datetime.fromtimestamp(max(stats["all_ts"])).strftime("%Y-%m-%d")
        span_days = (max(stats["all_ts"]) - min(stats["all_ts"])) / 86400
        out.append(f"date range:        {lo} -> {hi}  ({span_days:.0f} days)")
    out.append(f"transcripts:       {stats['files']}")
    out.append(f"sessions counted:  {stats['sessions_with_time']}")
    out.append("")
    out.append(f"TOTAL ACTIVE TIME: {fmt_hours(stats['total_active'])}"
               f"   (idle gaps capped at {cap_min} min)")
    out.append("")

    out.append("By month:")
    for m in sorted(stats["by_month"]):
        out.append(f"  {m}   {fmt_hours(stats['by_month'][m]):>9}")
    out.append("")

    projects = sorted(stats["by_project"].items(), key=lambda kv: kv[1], reverse=True)
    out.append(f"Top {min(top_projects, len(projects))} projects:")
    for proj, secs in projects[:top_projects]:
        label = decode_project_dir(proj)
        if len(label) > 50:
            label = "..." + label[-47:]
        sess = stats["project_sessions"][proj]
        out.append(f"  {fmt_hours(secs):>9}  ({sess:>3} sess)  {label}")

    if show_days:
        out.append("")
        out.append("By day:")
        for d in sorted(stats["by_day"]):
            out.append(f"  {d}   {fmt_hours(stats['by_day'][d]):>9}")

    out.append("")
    out.append("Note: derived from local transcripts only; sessions older than")
    out.append("your retention window (cleanupPeriodDays) are already pruned.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--idle", type=float, default=5.0,
                    help="idle-gap cap in minutes (default 5). Gaps longer than "
                         "this count as only this many minutes of active time.")
    ap.add_argument("--projects-dir",
                    default=os.path.expanduser("~/.claude/projects"),
                    help="path to Claude Code projects dir")
    ap.add_argument("--top-projects", type=int, default=10,
                    help="how many projects to list (default 10)")
    ap.add_argument("--days", action="store_true",
                    help="also print a per-day breakdown")
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON instead of a report")
    args = ap.parse_args()

    if not os.path.isdir(args.projects_dir):
        print(f"No transcripts found at {args.projects_dir}", file=sys.stderr)
        sys.exit(1)

    idle_cap = args.idle * 60
    stats = collect(args.projects_dir, idle_cap)

    if args.json:
        payload = {
            "idle_cap_minutes": args.idle,
            "transcripts": stats["files"],
            "sessions_counted": stats["sessions_with_time"],
            "total_active_hours": round(stats["total_active"] / 3600, 2),
            "by_month_hours": {m: round(s / 3600, 2)
                               for m, s in sorted(stats["by_month"].items())},
            "by_project_hours": {decode_project_dir(p): round(s / 3600, 2)
                                 for p, s in sorted(stats["by_project"].items(),
                                                    key=lambda kv: kv[1], reverse=True)},
        }
        if stats["all_ts"]:
            payload["date_range"] = {
                "from": datetime.fromtimestamp(min(stats["all_ts"])).strftime("%Y-%m-%d"),
                "to": datetime.fromtimestamp(max(stats["all_ts"])).strftime("%Y-%m-%d"),
            }
        if args.days:
            payload["by_day_hours"] = {d: round(s / 3600, 2)
                                       for d, s in sorted(stats["by_day"].items())}
        print(json.dumps(payload, indent=2))
    else:
        print(render_text(stats, idle_cap, args.top_projects, args.days))


if __name__ == "__main__":
    main()
