---
name: config-evolve
description: "Runs Claude Code's built-in /insights command for you and turns its report into applied config improvements. On demand (/config-evolve) or monthly (a scheduled claude -p run) it generates a fresh /insights analysis under the hood, captures the fixes it drafts (CLAUDE.md rules, skills, hooks, headless scripts), extends them with the change types /insights skips (permission allowlist entries, saved slash commands, MCP servers, settings tweaks), diffs everything against prior months so applied or rejected items never reappear, writes a dated review doc, and then applies the ones you approve with backups. Never auto-applies. Use when the user says config-evolve, evolve my config, monthly config checkup, run insights and suggest changes, apply my insights suggestions, suggest improvements to my Claude setup, or what should I add to my Claude config. It complements setup-audit, which removes bloat; config-evolve is the ADD side, grounded in /insights."
---

# config-evolve

config-evolve runs Claude Code's built-in `/insights` command for you, then turns its analysis into config changes you can review and apply. `/insights` has the deep session analysis; config-evolve adds the operational layer around it: it runs it on a cadence, remembers decisions across months, covers more change types, and applies the fixes safely instead of leaving you to copy-paste.

It is the ADD counterpart to `setup-audit`. setup-audit finds bloat, conflicts, and duplicate capabilities and offers to cut them. config-evolve finds *missing* capabilities and drafts them. If the user asks to clean up or slim down, hand off to setup-audit.

## How it runs

- **On demand**: `/config-evolve`.
- **Monthly**: a scheduler runs `claude -p "/config-evolve"` (see `references/scheduling.md`). Same behavior.
- **Apply**: `/config-evolve apply`, or the user replying with item numbers after a run.

Either way, config-evolve invokes `/insights` itself. You never run `/insights` first.

## Two verbs, and why they never mix

- **ANALYZE**: run `/insights`, build proposals, score, write the dated doc, update state. Changes no config. Safe to run unattended.
- **APPLY**: apply the specific items the user picked, with backups and verification.

A single run never analyzes and applies in the same turn. Applying is always a separate, explicit human action. That is what makes the unattended monthly run safe: with no one to pick items, nothing is applied.

## Paths and config (resolve once)

- **Output dir**: `$CONFIG_EVOLVE_OUTPUT_DIR`, else `~/.claude/config-evolve/reports/`. Create if missing.
- **State file**: `~/.claude/config-evolve/state.json`.
- **Optional config**: `~/.claude/config-evolve/config.json` may set `outputDir`, `thresholds`, `maxProposals`, `insightsTools`, and `email` (`{ "to": "...", "sendCommand": "..." }`). Read if present.
- **Scheduled marker**: env `CONFIG_EVOLVE_SCHEDULED=1` means an unattended run. In that case, after writing the doc, run the email `sendCommand` if configured, then stop. Do not print an interactive apply summary.
- **Nested-run marker**: config-evolve sets env `CONFIG_EVOLVE_RUNNING=1` on the `/insights` it launches. If you have your own `/insights` hooks (for example a summary or email hook), check this var and exit early so they do not double-fire on config-evolve's internal analysis run.

Never write secrets to any of these files.

---

# ANALYZE flow

## 1. Load state

Read `~/.claude/config-evolve/state.json` if it exists (schema below). It records every prior proposal and its disposition, so this run avoids repeating handled ideas. On a first run there is no state; analyze from the start of available history and, interactively, offer to set up the monthly schedule at the end (`references/scheduling.md`).

```json
{
  "lastRun": "YYYY-MM-DD",
  "proposals": [
    { "id": "kebab-id", "title": "...", "type": "skill|claude-md|hook|headless|permission|command|mcp|settings",
      "source": "insights|config-evolve", "firstSeen": "YYYY-MM-DD", "timesSeen": 2,
      "disposition": "proposed|applied|rejected|deferred|watching", "resolvedAt": "YYYY-MM-DD|null" }
  ],
  "appliedChangelog": [ { "date": "YYYY-MM-DD", "id": "...", "summary": "..." } ]
}
```

## 2. Run /insights and capture the report

config-evolve grounds its suggestions in a fresh `/insights` report, which it generates itself by running the built-in command headless. Do this with Bash:

```bash
OUT="${CONFIG_EVOLVE_OUTPUT_DIR:-$HOME/.claude/config-evolve/reports}"
mkdir -p "$OUT"
RAW="$OUT/insights-raw-$(date +%F).md"
# Reuse today's report if it already exists; do not pay for /insights twice in one day.
if [ ! -s "$RAW" ]; then
  # CONFIG_EVOLVE_RUNNING lets a user's own /insights hooks detect and skip this nested run
  # (so a personal summary/email hook does not double-fire on config-evolve's internal analysis).
  CONFIG_EVOLVE_RUNNING=1 timeout 900 claude -p "/insights" \
    --allowedTools "Bash,Read,Glob,Grep,WebFetch,WebSearch" \
    > "$RAW" 2> "$OUT/insights.err.log" || true
fi
```

Then read `$RAW`. It holds `/insights`' full report: its drafted fixes (CLAUDE.md rules, skills, hooks, headless scripts, each with the mistake it prevents) and its statistics (tool usage, friction types, session types, projects). Keep the drafted fixes verbatim; you will surface them as proposals tagged `source: insights`.

**Robustness**:
- The reuse guard keeps repeat runs cheap. Respect an existing non-empty `$RAW` from today.
- If the run fails or `$RAW` is empty (too little history, or `/insights` unavailable), fall back to config-evolve's own direct analysis: read `~/.claude/history.jsonl`, sample recent `~/.claude/projects/*/*.jsonl` transcripts, and `~/.claude/usage-data/report*.html` if present. Note in the doc that the fallback source was used.
- A user may override the tool list via `config.json` `insightsTools`.

## 3. Read the current config surface

So proposals are non-duplicative and land cleanly, read (read-only):
- `~/.claude/CLAUDE.md`, project `./CLAUDE.md`, `./.claude/CLAUDE.md`.
- Skill inventory under `~/.claude/skills/` (follow symlinks) and installed plugins (`~/.claude/plugins/installed_plugins.json`).
- `~/.claude/settings.json` and project settings: existing `hooks`, `permissions.allow`, `env`, `model`, `outputStyle`, `statusLine`.
- MCP servers from settings or `.mcp.json`.

If a proposed capability already exists, drop it.

## 4. Build proposals

Two sources, one ranked list. The catalog with how to draft each artifact is in `references/change-types.md` (load it).

**From the /insights report** (`source: insights`): surface each fix it drafted, verbatim. These are CLAUDE.md rules, skills, hooks, and headless scripts, each already tied to a specific mistake or pattern `/insights` found.

**Extended by config-evolve** (`source: config-evolve`): add the change types `/insights` does not emphasize, drawn from the report's own statistics (tool usage, friction, session types) plus what you saw in the config surface:
- **Permission allowlist entry**: the same safe command approved over and over.
- **Saved slash command**: one long prompt reused often.
- **MCP server**: repeated manual work against an external service (placeholder credentials only).
- **Settings tweak**: friction from a default that no longer fits (model tier, output style, statusline).

Draft the real artifact for every proposal, not a description. A proposal the user cannot apply as-is does not belong in the doc. Removal, dedup, and conflicts are out of scope; note "run setup-audit" in one line and move on.

## 5. Score, filter, and diff against state

Score each proposal: **Impact** 1-5 (monthly time/friction saved), **Confidence** 1-5, **Effort** low/med/high. `Priority = Impact x Confidence`, tie-break to lower Effort.

Diff against state:
- Drop anything whose `id` is already `applied` or `rejected` (never re-surface a rejected idea; that is the point of the memory).
- A prior `deferred`/`watching` item that recurs gets `timesSeen` incremented and stays in play.
- New proposals start at `timesSeen: 1`, `firstSeen: today`.

Defaults (override in `config.json`): surface only Confidence >= 3; cap the doc at the top **7**; anything real but under the bar goes on a **Watching** list carried in state, not the doc. This is the dial between coach and nag.

## 6. Write the dated review doc

Write `<outputDir>/config-evolve-<YYYY-MM-DD>.md` using `references/review-template.md`. Each proposal carries its evidence, the ready-to-apply artifact (verbatim), its score, and a `[source: insights|config-evolve]` tag. Include a Watching list and a Changelog of what was applied since last run (from state). Writing the doc changes no config. Keep the raw `insights-raw-<date>.md` alongside it for reference.

## 7. Deliver and record

Update `state.json`: set `lastRun` to today and merge this run's proposals.

Then:
- **Scheduled run** (`CONFIG_EVOLVE_SCHEDULED=1`): run the email `sendCommand` if configured, then stop. Do not offer apply.
- **Interactive run**: print a compact numbered summary (title, type, source, one-line evidence, priority) and tell the user to reply with the item numbers to apply, or run `/config-evolve apply`.

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
- Running `/insights` is the expensive step. Reuse today's captured report; do not re-run it within the same day.
- One dated backup per touched file, before editing. `settings.json` re-validated after.
- No secrets in the doc, state, or config. MCP proposals ship placeholder credentials only.
- Cap the doc at the top proposals; the rest go on Watching. Do not flood.
- Adding capabilities only. Removal, dedup, and conflicts go to setup-audit (note in one line, do not act).
