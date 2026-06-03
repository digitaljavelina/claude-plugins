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

### changelog-monitor

Monitor the Claude Code changelog for new versions.

**Usage:**

- `/changelog-monitor` — Check once for new versions
- `/loop /changelog-monitor` — Monitor continuously

### migrate-ai-config

Interactively migrate Claude Code and/or Codex config (skills, hooks, plugins, commands, agents, MCP servers, prompts, settings) between macOS, Windows, and Linux. Asks source/target OS and tools, then emits a tailored migration playbook.

### setup-audit

Audit a Claude Code installation on two tracks:

- **Instruction files** (`CLAUDE.md`, skills, settings, hooks) for bloat, conflicts, and redundancy.
- **Skill & plugin inventory** for duplicate and overlapping capabilities.

Reports findings (scored rule table, cut list, conflict report, overlap clusters, removal-candidate list), then offers to remove flagged items after confirmation, backing up everything first.

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
