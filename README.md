# Digital Javelina Claude Plugins

A collection of Claude Code plugins and skills, published as a single marketplace.

## Installation

Add this marketplace to Claude Code:

```sh
/plugin marketplace add digitaljavelina/claude-plugins
```

Then install any plugin:

```sh
/plugin install changelog-monitor@digitaljavelina-plugins
/plugin install migrate-ai-config@digitaljavelina-plugins
/plugin install setup-audit@digitaljavelina-plugins
/plugin install claude-usage@digitaljavelina-plugins
/plugin install yt-tutorial@digitaljavelina-plugins
```

## Available Plugins

| Plugin              | Version | Description                                                                                                                                                                                                                                                                                                                      |
| ------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `changelog-monitor` | 1.1.3   | Monitor the Claude Code changelog for new versions. Run `/changelog-monitor` to check once, or `/loop /changelog-monitor` to monitor continuously.                                                                                                                                                                               |
| `migrate-ai-config` | 1.0.3   | Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) between macOS, Windows, and Linux. Asks source/target OS and tools, then emits a tailored migration playbook.                                                                                   |
| `setup-audit`       | 1.0.0   | Audit a Claude Code installation on two tracks: instruction files (`CLAUDE.md`, skills, settings, hooks) for bloat, conflicts, and redundancy, and the skill/plugin inventory for duplicate and overlapping capabilities. Reports findings, then offers to remove flagged items after confirmation, backing up everything first. |
| `claude-usage`      | 1.0.0   | Report Claude Code usage from local session transcripts: total active hours, session count, date range, and per-month / per-project breakdowns. Estimates hands-on-keyboard time by capping idle gaps; points to `ccusage` for token and cost data.                                                                              |
| `yt-tutorial`       | 1.0.0   | Turn a YouTube video into a complete, beginner-friendly, publication-ready tutorial. Fetches the transcript with `yt-dlp` / `youtube-transcript-api`, optionally researches real-world examples, and rewrites the content in a conversational explainer voice with every code block decoded line by line.                         |

### Prerequisites

Most plugins run with no extra setup. The exception is `yt-tutorial`, which shells out to external tools to fetch a video's transcript and metadata. Before using it, install:

- [`uv`](https://docs.astral.sh/uv/) — runs the bundled transcript script and auto-installs its Python dependencies (`youtube-transcript-api`) on first use, so you don't install those yourself.
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — pulls the video title, channel, and description.

On macOS both are available via Homebrew: `brew install uv yt-dlp`.

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
