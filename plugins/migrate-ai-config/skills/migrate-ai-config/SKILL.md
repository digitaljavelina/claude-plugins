---
name: migrate-ai-config
description: Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) and optionally chat history (.jsonl transcripts, so past conversations are preserved and resumable) between macOS, Windows, and Linux. Use when the user wants to move their AI-tool setup to a new machine or OS, or says "migrate my claude code", "move my codex setup", "migrate to my new laptop", "set up claude code on my other computer", "preserve my chat history".
---

# migrate-ai-config

Generate a **single-use, tailored migration playbook** for moving Claude Code and/or Codex between machines. Instead of making the user pick the right static guide, interview them and emit only the steps their exact OS pair needs.

## Step 1 — Run the interview

Call `AskUserQuestion` with these five questions (single call, five questions):

1. **Source OS** (single): macOS / Windows / Linux
2. **Target OS** (single): macOS / Windows / Linux
3. **Tools** (multiSelect): Claude Code / Codex
4. **Chat history** (single): Skip / All history / Recent only (last 90 days)
5. **Deliverable** (single): Save the tailored playbook to a Markdown file / Show steps inline only

If the user already stated any of these in their message, skip that question.

Chat history is the `.jsonl` transcript trees (large and full of machine-specific absolute paths), kept separate from portable config. Include the **Restore chat history** block in Step 4 only when the user picks **All history** or **Recent only**; the recent filter adds a `-mtime -90` window when exporting.

**Windows-history caveat — surface this inline (not only in the playbook).** If the user opts into history **and** either OS is Windows, tell them directly, before generating the playbook, that Claude encodes its per-project transcript folders using drive letters and backslashes, so cross-OS `--resume` is **not guaranteed** to reopen old sessions in the right project. Their transcripts will still copy over fully and stay readable/greppable for reference; only in-project resume is the unreliable part. Offer to proceed as a readable archive (and mention the optional best-effort rewrite in the Windows block).

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
**Prepare target → Export from source → Transfer → Restore Claude Code → Restore Codex → Restore chat history → Gotchas → Verification checklist.**

Drop any block the shape doesn't need (omit **Restore chat history** entirely when the user picked **Skip** in Step 1). Substitute the username/paths captured in Step 3. If the deliverable is a file, write `<Source>-to-<Target>-AI-Migration.md` to the directory chosen in Step 3 (default: current working directory); otherwise print inline.

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

### Portable in-place sed helper (use in every rewrite snippet below)

macOS (BSD) `sed -i` needs a backup-suffix argument (`-i ''`); GNU `sed -i` on Linux must **not** have one. The snippets below show macOS form; on a **Unix target**, define `sedi` once and substitute it for every `sed -i ''` so the same playbook runs on either OS:

```bash
# Run on the TARGET machine. Detects BSD vs GNU sed.
sedi() { if sed --version >/dev/null 2>&1; then sed -i "$@"; else sed -i '' "$@"; fi; }
# then e.g.:  sedi "s#/Users/olduser#$HOME#g" ~/.claude/settings.json
```

### EASY-shape fix (Unix→Unix, only if home/username changed)

```bash
sedi "s#/Users/olduser#$HOME#g" ~/.claude/settings.json        # sedi = portable in-place sed (above)
find ~/.claude/hooks -type f -exec sed -i '' "s#/Users/olduser#$HOME#g" {} +   # macOS; Linux: drop the ''
sedi "s#/Users/olduser#$HOME#g" ~/.codex/config.toml
```
On Linux the home prefix is `/home/<you>`, not `/Users/<you>` — `$HOME` resolves it on the target either way.

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

### Chat history — what to export (only if not "Skip")

```
Claude Code:  .claude/projects/**/*.jsonl   (the transcripts; dir name = cwd with / and . → -)
              .claude/todos/                 (per-session todo state)
              .claude/history.jsonl          (prompt history)
Codex:        .codex/sessions/**/*.jsonl     (date-foldered rollout files)
              .codex/history.jsonl  .codex/session_index.jsonl
```

History is bulky and path-saturated, so keep it out of the main config archive. **Recent only** = add `-mtime -90` to each `find` during export:

```bash
# Source: bundle only recent transcripts (drop -mtime for "All history")
find ~/.claude/projects ~/.claude/todos -type f -mtime -90 -print0 | tar --null -czf claude-history.tgz -T -
find ~/.codex/sessions -name '*.jsonl' -mtime -90 -print0 | tar --null -czf codex-history.tgz -T -
# (history.jsonl / session_index.jsonl: copy whole, they are small)
```

### Restore chat history — resume where possible

**Unix→Unix, same username:** extract verbatim into `~/.claude` / `~/.codex`. `claude --resume` works immediately; no rewrite.

**Unix→Unix, different home/username:** rename the encoded project dirs to the new home, then rewrite embedded paths inside every transcript. Resume then works for any project you recreate at the matching path.

```bash
# 1. Rename encoded project dirs.  Encoding = path with both '/' and '.' replaced by '-'.
NEWENC=$(printf '%s' "$HOME" | sed 's#[/.]#-#g')     # e.g. -Users-newuser  (or -home-newuser on Linux)
OLDENC="-Users-olduser"                               # source machine's home, encoded
cd ~/.claude/projects
for d in "$OLDENC"*; do [ -e "$d" ] && mv "$d" "$NEWENC${d#"$OLDENC"}"; done
# 2. Rewrite absolute paths inside transcripts + todos (sedi helper; while-loop keeps it in-shell).
find ~/.claude/projects ~/.claude/todos -name '*.jsonl' -print0 \
  | while IFS= read -r -d '' f; do sedi "s#/Users/olduser#$HOME#g" "$f"; done
# 3. Codex: no encoded dirs, just rewrite the embedded cwd.
find ~/.codex/sessions -name '*.jsonl' -print0 \
  | while IFS= read -r -d '' f; do sedi "s#/Users/olduser#$HOME#g" "$f"; done
sedi "s#/Users/olduser#$HOME#g" ~/.codex/history.jsonl ~/.codex/session_index.jsonl 2>/dev/null
```

**Windows involved (CRLF or INTERP shape):** Claude's dir encoding uses drive letters and backslashes, so reliable cross-OS resume is not guaranteed. Extract verbatim so transcripts stay **readable and greppable** for reference, and tell the user resume may not surface them in-project. (Optional best-effort: also `dos2unix` the `.jsonl` and `sed` `C:\Users\<you>` → `$HOME` as in the CRLF block, but verify before relying on `--resume`.)

### Verification (all shapes)

`claude --version` + `/help` + a custom skill + hooks fire + `claude mcp list`; `codex --version` + prompts as `/<name>` + MCP connects + `notify` fires. Chat history (if migrated): `claude --resume` lists old sessions and one reopens in the right project; `codex resume` finds a past session. Final sweep: grep config **and transcripts** for any leftover source-OS path.
