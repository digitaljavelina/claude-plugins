# Running it monthly

config-evolve rides on the built-in `/insights` command, which runs headless. So the monthly job is just `/insights` run unattended. The bundled hook does the config-evolve work automatically, and because ANALYZE never applies, the unattended run is safe by design.

Set `CONFIG_EVOLVE_SCHEDULED=1` in the job's environment so the run knows to email the doc (if configured) and skip the interactive apply summary.

On a first interactive run with no schedule detected, offer to set one of these up.

---

## Option A: Scheduled cloud routine (recommended)

Runs in the cloud with the plugin installed. No local machine required.

Use Claude Code scheduling (the `/schedule` skill or your routines UI) to create a routine:

- **Schedule (cron):** `0 8 1 * *`  (08:00 on the 1st of every month)
- **Prompt:** `/insights`
- **Allowed tools:** `Bash,Read,Write,Glob,Grep,WebFetch,WebSearch`
- **Env (if the platform allows):** `CONFIG_EVOLVE_SCHEDULED=1`

If the platform cannot set an env var, the run still works and still writes the doc. It just will not auto-email. With no one present to pick items, nothing is applied either way.

---

## Option B: Local launchd (macOS) or cron (Linux)

Runs on your own machine, offline. This is the generalized form of a personal `com.<you>.claude-insights.plist`, with no hardcoded home path or address.

**launchd (macOS):** create `~/Library/LaunchAgents/dev.digitaljavelina.config-evolve.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>dev.digitaljavelina.config-evolve</string>
  <key>ProgramArguments</key>
  <array>
    <string>claude</string>
    <string>-p</string><string>/insights</string>
    <string>--allowedTools</string><string>Bash,Read,Write,Glob,Grep,WebFetch,WebSearch</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Day</key><integer>1</integer><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>EnvironmentVariables</key>
  <dict>
    <key>CONFIG_EVOLVE_SCHEDULED</key><string>1</string>
    <key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
  </dict>
  <key>StandardOutPath</key><string>/tmp/config-evolve.out.log</string>
  <key>StandardErrorPath</key><string>/tmp/config-evolve.err.log</string>
</dict>
</plist>
```

Load it: `launchctl load ~/Library/LaunchAgents/dev.digitaljavelina.config-evolve.plist`
(`claude` must be on the `PATH` you set above; run `which claude` to confirm the location.)

**cron (Linux):**

```sh
# crontab -e, then add:
0 8 1 * * CONFIG_EVOLVE_SCHEDULED=1 claude -p "/insights" --allowedTools "Bash,Read,Write,Glob,Grep,WebFetch,WebSearch" >> "$HOME/.claude/config-evolve/cron.log" 2>&1
```

---

## Option C: SessionStart nudge (portable, no infra)

Zero infrastructure, cross-platform, but it reminds rather than runs. A `SessionStart` hook checks `lastRun` in state and, if more than ~30 days have passed, prints a one-line nudge when you open Claude Code. You then run `/insights` yourself.

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
        "command": "test -f \"$HOME/.claude/config-evolve/state.json\" && python3 -c \"import json,datetime,os; s=json.load(open(os.path.expanduser('~/.claude/config-evolve/state.json'))); lr=datetime.date.fromisoformat(s.get('lastRun','2000-01-01')); print('config-evolve: monthly checkup due (last run '+str(lr)+'). Run /insights.') if (datetime.date.today()-lr).days>=30 else None\" || true" } ] }
    ]
  }
}
```

---

## Optional: email the monthly doc

To email the doc on scheduled runs, add to `~/.claude/config-evolve/config.json`:

```json
{ "email": { "to": "you@example.com", "sendCommand": "~/.claude/config-evolve/send-report.sh" } }
```

`sendCommand` is any script that mails the most recent `config-evolve-*.md` from the output dir. Off by default and never required.
