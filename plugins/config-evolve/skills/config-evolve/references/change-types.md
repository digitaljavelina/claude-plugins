# Change-type catalog

Two groups. The first four are what `/insights` already drafts. config-evolve captures them verbatim into the review doc, tags them `source: insights`, and diffs them against state so they are not re-proposed once handled. The last four are what `/insights` does not emphasize. config-evolve originates these itself, tagged `source: config-evolve`, from the evidence in the `/insights` report (its tool-usage, friction, and session stats, plus the "Features to Try" and "On the Horizon" sections). Do not run a separate deep transcript crawl for them; keep it light.

Always draft the real artifact, never a description of it. A proposal the user cannot apply as-is does not belong in the doc.

---

## Captured from /insights (source: insights)

### CLAUDE.md rule
A preference, correction, or project fact `/insights` saw Claude get wrong. The report gives the exact line and the mistake it prevents. Capture both. Keep additions terse; `setup-audit` exists to fight CLAUDE.md bloat, so every line must earn its place.

### Skill
A repeated multi-step workflow. `/insights` writes the `SKILL.md`. Capture it whole; it applies to `~/.claude/skills/<name>/SKILL.md`.

### Hook
A deterministic "always / whenever X do Y" that Claude keeps forgetting, or a guardrail the user wants enforced. `/insights` writes the hook script and the `settings.json` block. Capture both. Automatic behaviors need a hook because the harness runs hooks deterministically while the model may not honor a written instruction.

### Headless script
A structured multi-step process run repeatedly. `/insights` writes a `claude -p` script with `--allowedTools`. Capture it as a file the user can save and run.

---

## Added by config-evolve (source: config-evolve)

### Permission allowlist entry
**Signal**: the same safe command approved over and over (visible in the report's tool-usage and friction stats). **Draft**: the exact `permissions.allow` entry for `settings.json` (or project `.claude/settings.json`). Only allowlist genuinely safe, read-only, or clearly-authorized commands. Never allowlist destructive or credential-touching commands.

### Saved slash command
**Signal**: one long prompt reused often with little variation. Distinct from a skill: a command is a fixed prompt, a skill is a procedure with judgment. **Draft**: the command markdown targeting `~/.claude/commands/<name>.md`.

### MCP server
**Signal**: repeated manual work against an external service (an API, a SaaS tool, a database) that a Model Context Protocol server would let Claude drive directly. **Draft**: the MCP config block for settings or `.mcp.json`, with **placeholder credentials only** and a one-line note on where to get the real token. Never write a real secret.

### Settings tweak
**Signal**: friction from a default that no longer fits the work mix, readable from the report's session-type and tool breakdown. Wrong default model tier, no statusline, an output-style mismatch, a hand-set env var. **Draft**: the precise `settings.json` key and value as a diff, with a one-line rationale tied to the observed usage.

---

## Out of scope (hand off, do not draft)

- Removing bloated or conflicting CLAUDE.md rules, or duplicate/overlapping skills and plugins. That is `setup-audit`. Note it in one line and move on.
- Anything requiring a real secret. Scaffold with placeholders and stop.
