---
name: migrate-ai-config
description: Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) between macOS, Windows, and Linux. Use when the user wants to move their AI-tool setup to a new machine or OS, or says "migrate my claude code", "move my codex setup", "migrate to my new laptop", "set up claude code on my other computer".
---

# migrate-ai-config

Generate a **single-use, tailored migration playbook** for moving Claude Code and/or Codex between machines. Instead of making the user pick the right static guide, interview them and emit only the steps their exact OS pair needs.

## Step 1 — Run the interview

Call `AskUserQuestion` with these four questions (single call, four questions):

1. **Source OS** (single): macOS / Windows / Linux
2. **Target OS** (single): macOS / Windows / Linux
3. **Tools** (multiSelect): Claude Code / Codex
4. **Deliverable** (single): Save the tailored playbook to a Markdown file / Show steps inline only

If the user already stated any of these in their message, skip that question.

## Step 2 — Classify the migration "shape"

The 9 OS combinations collapse to three shapes. Treat **macOS and Linux as identical** (both Unix: LF endings, Unix exec bit, `~/.claude` + `~/.codex`, bash hooks run natively). The only Unix difference is the home prefix: `/Users/<you>` (macOS) vs `/home/<you>` (Linux).

| Source → Target | Shape | Fixes to include |
|---|---|---|
| Unix → Unix (Mac↔Linux, same→same) | **EASY** | Home-prefix rewrite *only if it changed*; re-auth; reinstall plugins |
| Windows → Unix | **CRLF** | `dos2unix` + `chmod +x` + `C:\Users\<you>` → home; re-auth; reinstall |
| Unix → Windows | **INTERP** | Wrap `.sh` hooks in `bash`, path rewrite to `C:/Users/<you>`, `python3`→`python`, `cmd /c` MCP wrappers; re-auth; reinstall |

Same-OS with the **same username** = no path rewrite at all; the playbook is just copy + re-auth + reinstall plugins.

## Step 3 — Follow-up questions (AskUserQuestion)

Ask only what the classified shape needs. Each is an `AskUserQuestion`; the user can always pick **Other** to type a free-text value — that is how usernames and custom paths are captured.

- **Source username** — whenever the shape rewrites paths (any Windows endpoint, or Unix→Unix where the home prefix changes). Ask: "What's your username on the SOURCE machine? (the `<X>` in `C:\Users\<X>`, `/Users/<X>`, or `/home/<X>`)". Offer options like `Same as this machine's username` and `Use a placeholder I'll edit later`; the user selects **Other** to type the real one. Substitute it into the source home prefix — the target side resolves via `$HOME`.
- **Output directory** — only when the deliverable is a Markdown file. Ask: "Where should I save the playbook?". Offer `Current directory` and `A different folder`; the user selects **Other** to type a path. Default to the current working directory.
- **INTERP shape only** — ask (AskUserQuestion) whether to use **Git Bash** (keep `.sh` hooks, wrap in `bash`) or **rewrite hooks to PowerShell**. Default Git Bash.

## Step 4 — Emit the playbook

Assemble from the building blocks below, in this order, including a section per selected tool:
**Prepare target → Export from source → Transfer → Restore Claude Code → Restore Codex → Gotchas → Verification checklist.**

Drop any block the shape doesn't need. Substitute the username/paths captured in Step 3. If the deliverable is a file, write `<Source>-to-<Target>-AI-Migration.md` to the directory chosen in Step 3 (default: current working directory); otherwise print inline.

---

## Building blocks

### Portable config (what to export — both tools)

```
Claude Code:  .claude/{settings.json, settings.local.json, CLAUDE.md, statusline.sh}
              .claude/{hooks,skills,commands,agents}/
              .claude/plugins/{installed_plugins.json, known_marketplaces.json}
              + mcpServers block copied out of .claude.json (NOT the whole file)
Codex:        .codex/{config.toml, AGENTS.md}  +  .codex/prompts/
```

### Never copy — re-authenticate / reinstall

```
.claude/.credentials.json  → run `claude` and sign in   (macOS = Keychain)
.codex/auth.json           → run `codex login`
.claude/plugins/cache,data → reinstall via CLI (see "Reinstall plugins + MCP" below)
.claude.json projects/     → regenerates per machine
```

### Prepare-target snippets

- **Unix target:** `brew install node python3 uv` (+ `dos2unix` if source is Windows). Linux: distro packages or Homebrew-on-Linux.
- **Windows target:** `winget install OpenJS.NodeJS Python.Python.3.12 Git.Git astral-sh.uv` — Git provides the `bash` your hooks need.
- Then install + first-run each tool so the config dir and fresh auth exist:
  `curl -fsSL https://claude.ai/install.sh | bash` (Unix) or `irm https://claude.ai/install.ps1 | iex` (Windows); `npm install -g @openai/codex` then `codex login`.

### EASY-shape fix (Unix→Unix, only if home/username changed)

```bash
sed -i '' "s#/Users/olduser#$HOME#g" ~/.claude/settings.json   # macOS sed
# Linux sed: sed -i  "s#/Users/olduser#$HOME#g" ...   (note: /home/<you>)
find ~/.claude/hooks -type f -exec sed -i '' "s#/Users/olduser#$HOME#g" {} +
sed -i '' "s#/Users/olduser#$HOME#g" ~/.codex/config.toml
```

### CRLF-shape fixes (Windows→Unix)

```bash
find ~/.claude/hooks ~/.claude/skills -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' \) -exec dos2unix {} +
dos2unix ~/.claude/statusline.sh
chmod +x ~/.claude/statusline.sh
find ~/.claude/hooks -type f -name '*.sh' -exec chmod +x {} +
sed -i '' "s#C:\\\\Users\\\\<you>#$HOME#g; s#\\\\#/#g" ~/.claude/settings.json
```

### INTERP-shape fixes (Unix→Windows)

```jsonc
// settings.json — wrap .sh hooks with Git Bash, forward slashes, no escaping
"command": "bash \"C:/Users/<you>/.claude/hooks/session-start.sh\""
```
- Paths `/Users/<you>` → `C:/Users/<you>`; `python3` → `python`.
- `config.toml` MCP servers: wrap `command="cmd", args=["/c","npx",...]` if a bare `npx` won't launch. `notify` → `["python", "C:\\Users\\<you>\\.codex\\notify.py"]`.

### Reinstall plugins + MCP (all shapes)

```bash
# Plugins — registry copied, but binaries are platform-specific, so reinstall via CLI:
claude plugin marketplace add <source>        # for each entry in known_marketplaces.json
claude plugin install <name>@<marketplace>    # for each entry in installed_plugins.json

# MCP servers — from the saved mcpServers block (drop any Windows `cmd /c` wrapper):
claude mcp add <name> -- <command> <args...>
```

### Verification (all shapes)

`claude --version` + `/help` + a custom skill + hooks fire + `claude mcp list`; `codex --version` + prompts as `/<name>` + MCP connects + `notify` fires. Final sweep: grep config for any leftover source-OS path.
