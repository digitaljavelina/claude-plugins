---
name: config-evolve
description: "Suggests additive changes to your Claude Code config based on how you actually work. Runs the same way on demand (/config-evolve) or monthly (a scheduled claude -p run): it analyzes your recent usage (prompt history, session transcripts, and the usage report if present) plus your current config, then proposes a ranked set of improvements: a new skill to solve a recurring task, a CLAUDE.md rule, a hook, a permission allowlist entry, a saved slash command, an MCP server, or a settings tweak. Writes a dated review doc, never auto-applies, offers a guided apply for the items you approve (backing up each file first), and remembers past decisions so it never re-suggests what you rejected. Use when the user says config-evolve, evolve my config, monthly config checkup, suggest improvements to my Claude setup, what should I add to my Claude config, or what skill or hook should I build next. It complements setup-audit, which removes bloat and conflicts; config-evolve is the ADD side. If the built-in /insights report is available it folds it in, but it never requires it."
---

# config-evolve

A self-contained advisor for your Claude Code setup. It looks at how you actually worked and proposes a small, high-signal set of *additive* changes: things to build or add so next month runs smoother. It behaves the same whether you run it on demand or a scheduler runs it monthly.

This is the ADD counterpart to `setup-audit`. setup-audit finds bloat, conflicts, and duplicate capabilities and offers to cut them. config-evolve looks for *missing* capabilities and drafts them. If the user asks to clean up or slim down, hand off to setup-audit.

## How it runs

- **On demand**: `/config-evolve`.
- **Monthly**: a scheduler runs `claude -p "/config-evolve"` (see `references/scheduling.md`). Same analysis, same proposals.
- **Apply**: `/config-evolve apply`, or the user replying with item numbers after a run.

## Two verbs, and why they never mix

- **ANALYZE**: gather evidence, propose, score, write the dated doc, update state. Changes no config. Safe to run unattended.
- **APPLY**: apply the specific items the user picked, with backups and verification.

A single run never analyzes and applies in the same turn. Applying is always a separate, explicit human action. That is what makes the unattended monthly run safe: with no one to pick items, nothing is applied.

## Paths and config (resolve once)

- **Output dir**: `$CONFIG_EVOLVE_OUTPUT_DIR`, else `~/.claude/config-evolve/reports/`. Create if missing.
- **State file**: `~/.claude/config-evolve/state.json`.
- **Optional config**: `~/.claude/config-evolve/config.json` may set `outputDir`, `thresholds`, `maxProposals`, and `email` (`{ "to": "...", "sendCommand": "..." }`). Read if present.
- **Scheduled marker**: env `CONFIG_EVOLVE_SCHEDULED=1` means an unattended run. In that case, after writing the doc, run the email `sendCommand` if configured, then stop. Do not print an interactive apply summary.

Never write secrets to any of these files.

---

# ANALYZE flow

## 1. Load state

Read `~/.claude/config-evolve/state.json` if it exists (schema below). It records every prior proposal and its disposition, so this run avoids repeating handled ideas. On a first run there is no state; analyze from the start of available history and, interactively, offer to set up the monthly schedule at the end (`references/scheduling.md`).

```json
{
  "lastRun": "YYYY-MM-DD",
  "proposals": [
    { "id": "kebab-id", "title": "...", "type": "skill|claude-md|hook|permission|command|mcp|settings",
      "firstSeen": "YYYY-MM-DD", "timesSeen": 2,
      "disposition": "proposed|applied|rejected|deferred|watching", "resolvedAt": "YYYY-MM-DD|null" }
  ],
  "appliedChangelog": [ { "date": "YYYY-MM-DD", "id": "...", "summary": "..." } ]
}
```

`periodStart` for this run = state's `lastRun`, or earliest available data on a first run.

## 2. Gather evidence (read-only)

Look at how the user worked since `periodStart`. Read only; never modify these.

**Usage signals**
- `~/.claude/history.jsonl`: global prompt history. Cluster prompts into recurring task types; note repeated phrasings and corrections.
- `~/.claude/projects/*/*.jsonl`: session transcripts. Sample the most recent sessions in the window. Look for: multi-step workflows the user re-drives and re-explains; the same safe Bash or MCP command approved over and over; corrections the user repeats ("no, use uv not pip"); context restated across sessions.
- `~/.claude/usage-data/report*.html`: the usage report, if the user generates one. Pull top projects, active hours, and tool mix to weight where improvements matter.
- **Optional bonus**: if a recent built-in `/insights` report or summary is saved on disk (for example under the output dir or the user's notes), fold its findings and any fixes it drafted into this run as extra signal. Never require it; config-evolve stands alone.

**Current config surface** (so proposals are non-duplicative and land cleanly)
- `~/.claude/CLAUDE.md`, project `./CLAUDE.md`, `./.claude/CLAUDE.md`.
- Skill inventory: names + descriptions under `~/.claude/skills/` (follow symlinks) and installed plugins (`~/.claude/plugins/installed_plugins.json`).
- `~/.claude/settings.json` and project settings: existing `hooks`, `permissions.allow`, `env`, `model`, `outputStyle`, `statusLine`.
- MCP servers from settings or `.mcp.json`.

Before proposing anything, confirm the capability does not already exist. If a matching skill, hook, rule, or allowlist entry is already present, do not propose it.

## 3. Turn signals into proposals

Map each recurring signal to the right kind of config change. The full catalog, with the signal to look for and how to draft each artifact, is in `references/change-types.md` (load it). In short:

| Signal | Proposed change |
| --- | --- |
| A multi-step workflow re-driven and re-explained | A new **skill** (draft the SKILL.md) |
| A preference / correction / context repeated | A **CLAUDE.md** rule (draft the exact line) |
| A deterministic "always / whenever do X" the model keeps forgetting | A **hook** (draft the script + settings snippet) |
| The same safe command approved again and again | A **permission** allowlist entry |
| One long prompt reused often | A saved **slash command** |
| Repeated manual work against an external service | An **MCP server** (scaffold with placeholder creds) |
| Friction from a wrong default (model, output style, no statusline) | A **settings** tweak |

For each candidate, draft the actual artifact (the file contents or the exact diff), not a description of it. A proposal the user cannot apply as-is does not belong in the doc. Removal, dedup, and conflict cleanup are out of scope; if you see them, note "run setup-audit" in one line and move on.

## 4. Score, filter, and diff against state

Score each candidate: **Impact** 1-5 (monthly time/friction saved), **Confidence** 1-5 (strength of evidence), **Effort** low/med/high. `Priority = Impact x Confidence`, tie-break to lower Effort.

Then diff against state:
- Drop anything whose `id` is already `applied` or `rejected` (never re-surface a rejected idea; that is the point of the memory).
- A prior `deferred` or `watching` item that recurs gets `timesSeen` incremented and stays in play.
- New candidates start at `timesSeen: 1`, `firstSeen: today`.

Defaults (override in `config.json`): surface only candidates that recurred **>= 3 times** with **Confidence >= 3**; cap the doc at the top **7**. Anything real but under the bar goes on a **Watching** list carried in state, not the doc. This threshold is the dial between coach and nag; tune it in `config.json` if the user wants it stricter or looser.

## 5. Write the dated review doc

Write `<outputDir>/config-evolve-<YYYY-MM-DD>.md` using `references/review-template.md`: a header (period, sessions analyzed), the ranked proposals each with evidence + the ready-to-apply artifact + score, a Watching list, and a Changelog of what was applied since last run (from state). Writing the doc changes no config.

## 6. Deliver and record

Update `state.json`: set `lastRun` to today and merge this run's proposals (new ids added, recurring ids updated).

Then:
- **Scheduled run** (`CONFIG_EVOLVE_SCHEDULED=1`): run the email `sendCommand` if configured, then stop. Do not offer apply.
- **Interactive run**: print a compact numbered summary (title, type, one-line evidence, priority) and tell the user to reply with the item numbers to apply, or run `/config-evolve apply`.

---

# APPLY flow

Triggered only by an explicit user action (item numbers, or `/config-evolve apply`). Read the latest review doc in `<outputDir>`.

For each item the user picked, in order:

1. **Back up first**: copy the target file to `<file>.bak-config-evolve-<YYYY-MM-DD>` before editing. New files (a skill, command, hook script) have nothing to back up.
2. **Apply** the artifact verbatim from the doc. New skills go to `~/.claude/skills/<name>/SKILL.md`; commands to `~/.claude/commands/<name>.md`; `CLAUDE.md` and `settings.json` edits apply the exact diff.
3. **Verify**: `settings.json` must still parse as JSON; for `CLAUDE.md` or a new file, re-read the changed region and confirm the content landed.
4. Show the resulting diff or path.

Record each applied item in `appliedChangelog` and set disposition `applied`. Items the user skipped become `deferred`. If the user says never suggest something again, set `rejected` so the memory suppresses it next month.

Never apply an item the user did not pick. Never edit a file you have not read this run.

---

# Guardrails

- ANALYZE never mutates config; the doc is always safe to generate, interactive or headless.
- One dated backup per touched file, before editing. `settings.json` re-validated after.
- No secrets in the doc, state, or config. MCP proposals ship placeholder credentials only.
- Cap the doc at the top proposals; the rest go on Watching. Do not flood.
- Adding capabilities only. Removal, dedup, and conflicts go to setup-audit (note in one line, do not act).
