# Review-doc template

Write the review doc with this structure. Fill every drafted artifact in full so each item is apply-ready. Keep prose tight and free of filler.

```markdown
# Config Evolve: <YYYY-MM-DD>

**Period covered:** <periodStart> to <today>
**Sessions analyzed:** <n>  ·  **Top projects:** <a, b, c>
**Proposals this run:** <k>  ·  **Applied since last run:** <m>

> Nothing here has been changed. Reply with the numbers you want to apply, or run
> `/config-evolve` interactively to apply with backups.

---

## Proposals (ranked)

### 1. <Title>
- **Type:** claude-md | skill | hook | headless | permission | command | mcp | settings
- **Source:** insights | config-evolve
- **Evidence:** <what triggered this, with counts and a concrete example>
- **Benefit:** <what it saves each month>
- **Score:** Impact <1-5> · Confidence <1-5> · Effort <low/med/high> · Priority <n>
- **Apply to:** <exact target path>

<the ready-to-apply artifact: full SKILL.md, exact diff, hook script + settings block,
allowlist line, command body, MCP config with placeholder creds, or settings diff>

### 2. <Title>
...

---

## Watching (below threshold this month)

Signals that are real but have not yet crossed the bar (recurred < 3 times or lower confidence). They carry over in state and may be proposed next month.

- <signal> (seen <n>x): <why it is not yet a proposal>

---

## Changelog (applied since last run)

- <YYYY-MM-DD> / <id> / <one-line summary>

---

## Cleanup note

<If duplicate/overlapping/bloated config was noticed, one line only:>
Run `setup-audit` to review and trim <the overlap you spotted>.
```
