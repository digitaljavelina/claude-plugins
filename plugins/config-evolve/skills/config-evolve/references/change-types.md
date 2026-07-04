# Change-type catalog

For each recurring signal, this is what to propose, how to draft the artifact, and an example. Always draft the real artifact, so the user can apply it as-is. A proposal the user cannot apply as-is does not belong in the doc.

---

## 1. New skill

**Signal**: a multi-step workflow the user re-drives across sessions and re-explains each time. Three or more repeats of the same shape (same goal, same rough steps) is the trigger.

**Draft**: a complete `SKILL.md` with YAML frontmatter (`name`, trigger-rich `description`) and a body of numbered steps that capture how the user actually does the task. Target `~/.claude/skills/<name>/SKILL.md`.

**Example evidence**: "In 4 sessions you walked Claude through the same release flow: bump version, update changelog, tag, push. Drafting a `cut-release` skill removes the re-explaining."

---

## 2. CLAUDE.md rule

**Signal**: a preference, correction, or piece of context the user restates. "Use uv not pip," "editor is VS Code," "always dark mode." If you had to be told twice, it belongs in CLAUDE.md.

**Draft**: the exact line or short block to add, and which file (user `~/.claude/CLAUDE.md` for global preferences, project `./CLAUDE.md` for project facts). Show it as a diff against the current file so it slots into the right section.

**Example evidence**: "You corrected pip to uv in 3 sessions. Add one line to the user CLAUDE.md and it stops recurring."

**Note**: keep additions terse. Its sibling `setup-audit` exists to fight CLAUDE.md bloat, so every proposed rule must earn its line. Prefer one sentence over a paragraph.

---

## 3. Hook

**Signal**: a deterministic "always / every time / whenever X, do Y" that the model keeps forgetting, or a guarantee the user wants enforced rather than remembered. Automatic behaviors need a hook, because the harness runs hooks deterministically while the model may or may not honor a written instruction.

**Draft**: the hook script (bash or the user's preferred runtime) plus the `settings.json` `hooks` block that wires it to the right event (`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`). Keep the script small and idempotent.

**Example evidence**: "You asked Claude to run the test suite before every commit in 5 sessions; twice it forgot. A PreToolUse hook on `git commit` makes it non-optional."

---

## 4. Permission allowlist entry

**Signal**: the same safe command approved over and over in the permission prompt. Read-only Bash (`git status`, `ls`, `rg`) or a specific MCP tool the user always allows.

**Draft**: the exact `permissions.allow` entry for `settings.json` (or project `.claude/settings.json` if it is project-specific). Only propose allowlisting genuinely safe, read-only, or clearly-authorized commands. Never allowlist destructive or credential-touching commands.

**Example evidence**: "You approved `gh pr view` 11 times this month. Allowlisting it cuts the prompts."

---

## 5. Saved slash command

**Signal**: one long prompt the user pastes or retypes often, with little variation. Distinct from a skill: a command is a fixed prompt, a skill is a procedure with judgment.

**Draft**: the command markdown file (the prompt body) targeting `~/.claude/commands/<name>.md`, or a plugin `commands/` dir if the user develops plugins.

**Example evidence**: "You pasted the same 'summarize this thread into decisions and action items' prompt 6 times. Save it as `/decisions`."

---

## 6. MCP server

**Signal**: repeated manual work against an external service (an API, a SaaS tool, a database) that a Model Context Protocol server would let Claude drive directly.

**Draft**: the MCP server config block for settings or `.mcp.json`, with **placeholder credentials only** and a one-line note on where to get the real token. Never write a real secret.

**Example evidence**: "You hand-relayed Linear issue data in 4 sessions. A Linear MCP server lets Claude query it directly." Ship the config with `"token": "<YOUR_LINEAR_TOKEN>"`.

---

## 7. Settings tweak

**Signal**: friction from a default that no longer fits the work mix. Wrong default model for the task load, no statusline showing useful context, an output style mismatch, a missing env var the user sets by hand each time.

**Draft**: the precise `settings.json` key and value to change, shown as a diff, with a one-line rationale tied to the observed usage.

**Example evidence**: "80% of your sessions this month were quick edits, but your default model is the heaviest tier. Consider a lighter default and escalate on demand."

---

## Out of scope (hand off, do not draft)

- Removing bloated or conflicting CLAUDE.md rules, or duplicate/overlapping skills and plugins. That is `setup-audit`. Note it in one line and move on.
- Anything requiring a real secret. Scaffold with placeholders and stop.
