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
```

## Available Plugins

| Plugin              | Version | Description                                                                                                                                                                                                                                                                                                                      |
| ------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `changelog-monitor` | 1.1.3   | Monitor the Claude Code changelog for new versions. Run `/changelog-monitor` to check once, or `/loop /changelog-monitor` to monitor continuously.                                                                                                                                                                               |
| `migrate-ai-config` | 1.0.3   | Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) between macOS, Windows, and Linux. Asks source/target OS and tools, then emits a tailored migration playbook.                                                                                   |
| `setup-audit`       | 1.0.0   | Audit a Claude Code installation on two tracks: instruction files (`CLAUDE.md`, skills, settings, hooks) for bloat, conflicts, and redundancy, and the skill/plugin inventory for duplicate and overlapping capabilities. Reports findings, then offers to remove flagged items after confirmation, backing up everything first. |

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
