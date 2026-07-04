# Digital Javelina Claude Plugins

A collection of Claude Code plugins and skills, published as a single marketplace.

## Installation

Add this marketplace to Claude Code:

```sh
/plugin marketplace add digitaljavelina/claude-plugins
```

Then install any plugin:

```sh
/plugin install config-evolve@digitaljavelina-plugins
/plugin install changelog-monitor@digitaljavelina-plugins
/plugin install migrate-ai-config@digitaljavelina-plugins
/plugin install setup-audit@digitaljavelina-plugins
/plugin install claude-usage@digitaljavelina-plugins
/plugin install yt-tutorial@digitaljavelina-plugins
/plugin install transcript-to-notebooklm@digitaljavelina-plugins
```

## Available Plugins

| Plugin              | Version | Description                                                                                                                                                                                                                                                                                                                      |
| ------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `config-evolve`     | 1.1.0   | Suggests additive changes to your Claude Code config from how you actually work. Runs the same on demand (`/config-evolve`) or monthly (a scheduled `claude -p` run): it analyzes your recent usage (prompt history, session transcripts, the usage report if present) and current config, then proposes a ranked set of ready-to-apply improvements: a new skill, a `CLAUDE.md` rule, a hook, a permission allowlist entry, a saved slash command, an MCP server, or a settings tweak. Writes a dated review doc, never auto-applies, offers a guided apply for the items you approve (backing up each file first), and remembers past decisions so it never re-suggests what you rejected. Self-contained; complements `setup-audit` by focusing on what to add, not what to cut. |
| `changelog-monitor` | 1.1.3   | Monitor the Claude Code changelog for new versions. Run `/changelog-monitor` to check once, or `/loop /changelog-monitor` to monitor continuously.                                                                                                                                                                               |
| `migrate-ai-config` | 1.1.0   | Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) and optionally chat history (`.jsonl` transcripts, so past conversations are preserved and resumable) between macOS, Windows, and Linux. Asks source/target OS, tools, and history scope, then emits a tailored migration playbook. |
| `setup-audit`       | 1.0.0   | Audit a Claude Code installation on two tracks: instruction files (`CLAUDE.md`, skills, settings, hooks) for bloat, conflicts, and redundancy, and the skill/plugin inventory for duplicate and overlapping capabilities. Reports findings, then offers to remove flagged items after confirmation, backing up everything first. |
| `claude-usage`      | 1.0.0   | Report Claude Code usage from local session transcripts: total active hours, session count, date range, and per-month / per-project breakdowns. Estimates hands-on-keyboard time by capping idle gaps; points to `ccusage` for token and cost data.                                                                              |
| `yt-tutorial`       | 1.0.0   | Turn a YouTube video into a complete, beginner-friendly, publication-ready tutorial. Fetches the transcript with `yt-dlp` / `youtube-transcript-api`, optionally researches real-world examples, and rewrites the content in a conversational explainer voice with every code block decoded line by line.                         |
| `transcript-to-notebooklm` | 1.0.0 | Clean `.srt` / `.vtt` subtitles or any timestamped transcript into plain `.txt` (strips timecodes, cue indices, and tags, de-dups rolling captions, reflows into paragraphs), then create a NotebookLM notebook and upload the cleaned files as sources. Handles a whole mixed folder in one pass and passes already-clean transcripts through untouched. |

### Prerequisites

Most plugins run with no extra setup. Two have external dependencies: `yt-tutorial` and `transcript-to-notebooklm`.

#### yt-tutorial

`yt-tutorial` shells out to external tools to fetch a video's transcript and metadata. Before using it, install:

- [`uv`](https://docs.astral.sh/uv/) — runs the bundled transcript script and auto-installs its Python dependencies (`youtube-transcript-api`) on first use, so you don't install those yourself.
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — pulls the video title, channel, and description.

Install both for your platform:

- **macOS** (Homebrew): `brew install uv yt-dlp`
- **Linux**:
  - `uv` — `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - `yt-dlp` — via your package manager (`sudo apt install yt-dlp`, `sudo dnf install yt-dlp`, `sudo pacman -S yt-dlp`) or `pipx install yt-dlp` for the newest release.
- **Windows** (PowerShell):
  - `uv` — `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
  - `yt-dlp` — `winget install yt-dlp.yt-dlp` (or `scoop install yt-dlp`).

#### transcript-to-notebooklm

Cleaning transcripts into `.txt` needs only Python 3 (standard library, nothing to install). The NotebookLM step needs the [`nlm`](https://pypi.org/project/notebooklm-mcp-cli/) CLI to create the notebook and upload sources:

- Install: `uv tool install notebooklm-mcp-cli` (or `pipx install notebooklm-mcp-cli`), which provides the `nlm` command.
- Authenticate once with `nlm login` (opens a browser to capture your Google/NotebookLM session). Sessions are short-lived; re-run `nlm login` if it reports expired cookies.

If you only want clean `.txt` files and not a notebook, you can use the plugin without `nlm` and skip the upload step.

## Repo layout

```
.claude-plugin/marketplace.json   # marketplace manifest, lists all plugins
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill>/SKILL.md
bump-version.sh                   # bump a plugin version in plugin.json + marketplace.json
```

Bump a plugin version:

```sh
./bump-version.sh <plugin-name> [patch|minor|major]
```
