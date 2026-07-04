---
name: config-evolve
description: "The monthly memory-and-apply layer around Claude Code's built-in /insights command. /insights already analyzes your session history and drafts fixes (CLAUDE.md rules, skills, hooks, headless scripts). config-evolve captures those fixes into a dated, ranked review doc, diffs them against prior months so applied or rejected items never reappear, extends coverage to the change types /insights skips (permission allowlist entries, saved slash commands, MCP servers, settings tweaks), and then applies the ones you approve with backups and verification. It runs automatically right after /insights (via a bundled hook), on a monthly schedule, or on demand with /config-evolve. Use when the user says config-evolve, evolve my config, monthly config checkup, apply my insights suggestions, act on /insights, or what should I add to my Claude setup. It is the ADD layer; hand cleanup and dedup to setup-audit."
---

# config-evolve

Claude Code's built-in `/insights` command reads your session history and writes a report that already includes ready-to-paste fixes: `CLAUDE.md` rules, new skills, hooks, and headless scripts. It is excellent, but it is stateless (it re-suggests the same things every month), it stops at those four fix types, and applying its fixes is manual copy-paste.

config-evolve is the layer that closes those gaps. It does not re-analyze your usage. It rides on the `/insights` output and adds four things: **memory** (a state file so month N+1 is a diff), **reach** (four more change types), a **durable dated review doc**, and a **safe guided apply** with backups.

This is the ADD counterpart to `setup-audit`. setup-audit trims bloat, conflicts, and duplicate capabilities. config-evolve proposes and applies new ones. Send removal work there.

## How it is triggered

- **After `/insights`** (primary): the bundled `UserPromptSubmit` hook fires on `/insights` and injects a directive to run the ANALYZE flow below on the report `/insights` just produced. This is what the monthly scheduled `claude -p "/insights"` job uses (see `references/scheduling.md`).
- **On demand**: `/config-evolve` runs ANALYZE against the most recent `/insights` output. If none is available this turn, ask the user to run `/insights` first (interactive) or point to the newest saved report.
- **Apply**: `/config-evolve apply` (or the user replying with item numbers) runs the APPLY flow.

## Two verbs, and why they never mix

- **ANALYZE**: capture fixes, extend, diff, score, write the dated doc, update state, print an apply summary. It changes no config. It is safe to run unattended.
- **APPLY**: apply the specific items the user picked, with backups and verification.

A single run never analyzes and applies in the same turn. Applying is always a separate, explicit human action. That is what makes the unattended monthly run safe: with no one to pick items, nothing is applied.

## Paths and config (resolve once)

- **Output dir**: `$CONFIG_EVOLVE_OUTPUT_DIR`, else `~/.claude/config-evolve/reports/`. Create if missing.
- **State file**: `~/.claude/config-evolve/state.json`.
- **Optional config**: `~/.claude/config-evolve/config.json` may set `outputDir`, `thresholds`, `maxProposals`, and `email` (`{ "to": "...", "sendCommand": "..." }`). Read if present.
- **Scheduled marker**: env `CONFIG_EVOLVE_SCHEDULED=1` means an unattended run. In that case, after writing the doc, run the email `sendCommand` if configured, and stop. Do not print an interactive apply summary.

Never write secrets to any of these files.

---

# ANALYZE flow

## 1. Get the insights material

Work from the `/insights` report and fixes available this turn (the hook path always has a fresh one). Read the four fix categories `/insights` produces: `CLAUDE.md` rules, skill files, hooks, headless scripts. Keep each fix verbatim; you will need the exact artifact.

If there is no `/insights` output this turn and you were invoked standalone, stop and ask the user to run `/insights` first. Do not fabricate an analysis. config-evolve rides on `/insights`; it does not replace it.

## 2. Load state and diff

Read `~/.claude/config-evolve/state.json` (schema below). For each `/insights` fix, compute a stable `id` (kebab of its target + intent). Then:

- If `id` disposition is `applied` or `rejected`, drop it (do not re-surface). For `rejected`, that is the whole point of the memory.
- If seen before as `deferred` or `watching`, increment `timesSeen` and keep it.
- If new, add it with `timesSeen: 1`, `firstSeen: today`.

```json
{
  "lastRun": "YYYY-MM-DD",
  "proposals": [
    { "id": "kebab-id", "title": "...", "type": "claude-md|skill|hook|headless|permission|command|mcp|settings",
      "source": "insights|config-evolve", "firstSeen": "YYYY-MM-DD", "timesSeen": 2,
      "disposition": "proposed|applied|rejected|deferred|watching", "resolvedAt": "YYYY-MM-DD|null" }
  ],
  "appliedChangelog": [ { "date": "YYYY-MM-DD", "id": "...", "summary": "..." } ]
}
```

## 3. Extend coverage

`/insights` covers `CLAUDE.md`, skills, hooks, and headless scripts. Add the change types it does not emphasize, when the evidence supports them. The signal-to-artifact catalog is in `references/change-types.md` (load it). The four to add here:

- **Permission allowlist entry**: the same safe command approved over and over. Draft the `permissions.allow` line.
- **Saved slash command**: one long prompt reused often with little variation.
- **MCP server**: repeated manual work against an external service. Scaffold with placeholder credentials only.
- **Settings tweak**: friction from a default that no longer fits (model tier, output style, statusline, a hand-set env var).

Evidence for these can come from the `/insights` report's own statistics (tool usage, friction types, session types) and its "Features to Try" / "On the Horizon" sections. Do not launch a separate deep transcript crawl; keep this light and mark each `source: config-evolve`.

Mark `id`, `type`, `source`, and disposition for every extended item too, and diff against state exactly as in step 2.

## 4. Score and filter

Score each surviving proposal: **Impact** 1-5 (monthly time/friction saved), **Confidence** 1-5 (strength of evidence), **Effort** low/med/high. `Priority = Impact x Confidence`, tie-break to lower Effort.

Defaults (override in `config.json`): surface only Confidence >= 3; cap the doc at the top **7**; anything real but under the bar goes on a **Watching** list carried in state, not the doc. This threshold is the dial between coach and nag. Tune it in `config.json` if the user wants it stricter or looser.

## 5. Write the dated review doc

Write `<outputDir>/config-evolve-<YYYY-MM-DD>.md` using `references/review-template.md`. Every proposal carries its evidence, the ready-to-apply artifact (verbatim), its score, and a `[source: insights|config-evolve]` tag. Include a Watching list and a Changelog of what was applied since last run (from state). Writing the doc changes no config.

## 6. Deliver and record

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
- One dated backup per touched file, before editing. `settings.json` re-validated after.
- No secrets in the doc, state, or config. MCP proposals ship placeholder credentials only.
- Cap the doc at the top proposals; the rest go on Watching. Do not flood.
- config-evolve rides on `/insights`; it never invents an analysis when none exists.
- Adding capabilities only. Removal, dedup, and conflicts go to setup-audit (note in one line, do not act).
