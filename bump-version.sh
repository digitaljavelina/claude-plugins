#!/usr/bin/env bash
set -euo pipefail

PLUGIN_NAME="${1:-}"
LEVEL="${2:-patch}"

if [[ -z "$PLUGIN_NAME" ]]; then
  echo "Usage: $0 <plugin-name> [patch|minor|major]"
  exit 1
fi

PLUGIN_JSON="plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
MARKETPLACE_JSON=".claude-plugin/marketplace.json"

if [[ ! -f "$PLUGIN_JSON" ]]; then
  echo "Error: $PLUGIN_JSON not found"
  exit 1
fi

CURRENT=$(python3 -c "import json; print(json.load(open('$PLUGIN_JSON'))['version'])")

NEW=$(python3 - <<EOF
parts = list(map(int, "$CURRENT".split('.')))
{"major": (0,), "minor": (1,), "patch": (2,)}
level = "$LEVEL"
if level == 'major':
    parts[0] += 1; parts[1] = 0; parts[2] = 0
elif level == 'minor':
    parts[1] += 1; parts[2] = 0
elif level == 'patch':
    parts[2] += 1
else:
    raise SystemExit(f"Unknown level: {level}. Use patch, minor, or major.")
print('.'.join(map(str, parts)))
EOF
)

echo "$PLUGIN_NAME: $CURRENT → $NEW"

python3 - <<EOF
import json
with open('$PLUGIN_JSON') as f:
    d = json.load(f)
d['version'] = '$NEW'
with open('$PLUGIN_JSON', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
EOF

python3 - <<EOF
import json
with open('$MARKETPLACE_JSON') as f:
    d = json.load(f)
for plugin in d['plugins']:
    if plugin['name'] == '$PLUGIN_NAME':
        plugin['version'] = '$NEW'
        break
else:
    raise SystemExit(f"Plugin '$PLUGIN_NAME' not found in $MARKETPLACE_JSON")
with open('$MARKETPLACE_JSON', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
EOF

echo "Updated: $PLUGIN_JSON"
echo "Updated: $MARKETPLACE_JSON"
