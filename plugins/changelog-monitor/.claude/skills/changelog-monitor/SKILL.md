---
name: changelog-monitor
description: Check the Claude Code changelog for new versions. Use with /loop to monitor continuously, or run once to see the latest changes.
---

# Claude Code Changelog Monitor

This skill fetches the Claude Code changelog from GitHub and reports on new versions.

## How It Works

1. Fetch the changelog from https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
2. Compare against the last seen version stored in `~/.claude-changelog-last-version`
3. Report any new versions with their changes
4. Update the stored version
5. If running with `/loop`, send a system notification when new versions are detected (macOS, Linux, and Windows supported)

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
2. Send a system notification using the appropriate command for the detected OS:
   ```bash
   OS=$(uname -s 2>/dev/null || echo "Windows")
   case "$OS" in
     Darwin)
       osascript -e 'display notification "New version X.Y.Z released" with title "Claude Code Update"'
       ;;
     Linux)
       notify-send "Claude Code Update" "New version X.Y.Z released" 2>/dev/null || true
       ;;
     MINGW*|CYGWIN*|MSYS*)
       powershell.exe -Command "
         Add-Type -AssemblyName System.Windows.Forms;
         \$n = New-Object System.Windows.Forms.NotifyIcon;
         \$n.Icon = [System.Drawing.SystemIcons]::Information;
         \$n.BalloonTipTitle = 'Claude Code Update';
         \$n.BalloonTipText = 'New version X.Y.Z released';
         \$n.Visible = \$true;
         \$n.ShowBalloonTip(5000);
         Start-Sleep 5;
         \$n.Dispose()
       " 2>/dev/null || true
       ;;
   esac
   ```

If no new versions:
- Report "Claude Code is up to date at version X.Y.Z"

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
```

## Loop Mode

When invoked with `/loop`, this skill will:
1. Check the changelog
2. Report findings
3. Wait for the next loop iteration
4. Repeat

The system notification ensures you're alerted even if the terminal isn't in focus.

- **macOS**: Uses `osascript` (built-in, no dependencies)
- **Linux**: Uses `notify-send` (requires `libnotify-bin`; fails silently if unavailable)
- **Windows**: Uses PowerShell tray balloon tip via `System.Windows.Forms` (built-in, no dependencies)
