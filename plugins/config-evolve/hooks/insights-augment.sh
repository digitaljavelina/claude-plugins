#!/usr/bin/env bash
# config-evolve: augment the built-in /insights command.
# Fires on every UserPromptSubmit; does nothing unless the prompt invokes /insights.
# On a match, injects a directive telling Claude to run the config-evolve ANALYZE
# flow on the report /insights is about to produce. Never triggers an apply.

prompt=$(jq -r '.prompt // ""' 2>/dev/null || true)

# Only act on an /insights invocation. Exit fast and silently otherwise.
if ! echo "$prompt" | grep -qE '^[[:space:]]*/insights\b'; then
  exit 0
fi

if [[ -n "${CONFIG_EVOLVE_SCHEDULED:-}" ]]; then
  MODE_LINE="This is an unattended, scheduled run (CONFIG_EVOLVE_SCHEDULED is set). After writing the review doc and updating state, run the email sendCommand from ~/.claude/config-evolve/config.json if one is configured, then stop. Do NOT print an interactive apply summary and do NOT apply anything."
else
  MODE_LINE="This is an interactive run. After writing the review doc, print a compact numbered summary of the proposals and tell the user to reply with the item numbers to apply, or run /config-evolve apply. Do NOT apply anything in this turn."
fi

cat <<INSTRUCTIONS

---
config-evolve is installed. After you generate the /insights report and its fixes,
run the config-evolve skill's ANALYZE flow on that output. In short:

1. Capture every /insights fix (CLAUDE.md rules, skills, hooks, headless scripts) verbatim,
   each with a stable id.
2. Load ~/.claude/config-evolve/state.json and diff: drop anything already applied or rejected,
   increment timesSeen on repeats, add new items.
3. Extend coverage with the change types /insights does not emphasize when the evidence supports
   them: permission allowlist entries, saved slash commands, MCP servers (placeholder creds only),
   and settings tweaks. Tag these source: config-evolve.
4. Score (Impact x Confidence, tie-break to lower Effort), keep Confidence >= 3, cap the top 7,
   put the rest on a Watching list in state.
5. Write a dated review doc to the config-evolve output dir (default ~/.claude/config-evolve/reports/)
   using the skill's review template, then update state.json.

$MODE_LINE

Applying is always a separate, explicit step. Never analyze and apply in the same turn.
Follow the config-evolve skill for the full procedure and the review-doc template.
---
INSTRUCTIONS

exit 0
