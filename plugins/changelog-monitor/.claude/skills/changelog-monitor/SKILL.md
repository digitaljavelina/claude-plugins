---
name: changelog-monitor
description: Check the Claude Code changelog for new versions. Use with /loop to monitor continuously, or run once to see the latest changes.
user_invocable: true
---

# Claude Code Changelog Monitor

This skill fetches the Claude Code changelog from GitHub and reports on new versions.

## How It Works

1. Fetch the changelog from https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
2. Compare against the last seen version stored in `~/.claude-changelog-last-version`
3. Report any new versions with their changes (always print the latest changelog entry regardless)
4. Update the stored version

## Execution Steps

### Step 1: Fetch the Changelog

Use WebFetch to get the raw changelog:

```
URL: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
Prompt: Extract all version numbers and their changes. Format as a list with version number followed by bullet points of changes.
```

### Step 2: Read Last Seen Version

Read the file `~/.claude-changelog-last-version` to get the previously seen version.
If the file doesn't exist, this is the first run.

### Step 3: Compare and Report

Parse the changelog to find versions. Version headers look like:
- `## 1.0.50` or `## [1.0.50]` or `### 1.0.50`

If there are new versions since the last seen:
1. Display each new version with its changes

If no new versions:
- Report "Claude Code is up to date at version X.Y.Z"

In both cases, always display the latest changelog entry (the most recent version and its changes).

### Step 4: Save Current Version

Write the latest version number to `~/.claude-changelog-last-version`

## Output Format

When new versions are found:

```
🚀 Claude Code Update!

## Version X.Y.Z (NEW)
- Change 1
- Change 2
- Change 3

## Version X.Y.W (NEW)
- Change 1
- Change 2

---
Updated from version A.B.C → X.Y.Z
```

When up to date:

```
✓ Claude Code is up to date (version X.Y.Z)

## Latest: Version X.Y.Z
- Change 1
- Change 2
```

## Loop Mode

When invoked with `/loop`, this skill will:
1. Check the changelog
2. Report findings
3. Wait for the next loop iteration
4. Repeat

