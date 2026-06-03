---
name: claude-usage
description: >-
  Report how much the user has used Claude Code: total active hours, sessions,
  date range, and per-month / per-project breakdowns, computed from local
  session transcripts in ~/.claude/projects. Use this skill whenever the user
  asks how long, how many hours, or how much they have used Claude Code, asks
  for their usage stats / history / totals, says things like "how many hours
  have I spent in Claude Code", "what's my total usage", "how much have I used
  this", "track my usage", or wants a time breakdown by month or by project.
  Note this measures TIME (hours of activity); for token counts and dollar cost
  the skill points to ccusage instead.
---

# Claude Code usage tracker

Report the user's Claude Code usage, with **total active hours** as the headline
number, plus a breakdown by month and by project.

## Why this needs a script

Claude Code stores no duration anywhere. The `/usage` command shows only the
current rate-limit windows, not lifetime totals, and nothing records wall-clock
time. The one durable signal is the per-message `timestamp` in each session
transcript under `~/.claude/projects/**/*.jsonl`. "Hours used" has to be
reconstructed from those, which is what the bundled script does. Don't try to
answer from memory or from `/usage`. Run the script.

## How active hours are estimated

Within each session the script sums the gaps between consecutive message
timestamps, but caps any single gap at the idle threshold (default 5 minutes).
That way a session left open while the user was away counts as a few minutes,
not several idle hours. The capped sum is the **active hours** estimate, roughly
hands-on-keyboard time. The threshold is an assumption, not a fact, so if the
user wants a looser or tighter definition, change `--idle` and rerun rather than
arguing about the "right" number.

## Running it

The script ships with this plugin. `${CLAUDE_PLUGIN_ROOT}` resolves to the
plugin's install directory:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/claude-usage/scripts/usage_stats.py"
```

Useful flags:

- `--idle <minutes>` — idle-gap cap (default 5). Raising it counts more
  away-from-keyboard time as active, so the total grows.
- `--top-projects <n>` — how many projects to list (default 10).
- `--days` — add a per-day breakdown.
- `--json` — machine-readable output, for when the user wants the data piped
  somewhere or charted rather than read.
- `--projects-dir <path>` — point at a non-default transcripts location.

Run it, then summarize the result for the user in prose: lead with the total
active hours and the date range, then the monthly trend, then notable projects
if relevant. Don't just dump the raw table unless they want the detail.

## The retention caveat (state it once)

The script only sees transcripts still on disk. Claude Code prunes old sessions
based on `cleanupPeriodDays` (default 30), so the totals reach back only as far
as the user's retention window, not to their very first session. When the user
asks about "all time" or "since the beginning", mention this once so the number
isn't mistaken for a complete lifetime total. The script prints the actual date
range it found, which is the honest floor.

## Tokens and cost are a different question

This skill measures **time**. If the user asks about tokens, spend, or dollar
cost, that data also lives in the same transcripts but is better handled by the
existing community tool:

```bash
npx ccusage@latest          # daily token + cost report
npx ccusage@latest monthly  # rolled up by month
```

Mention `ccusage` for cost questions rather than reimplementing it here.
