#!/usr/bin/env bash
# PreToolUse guard for Edit|Write. Reads hook JSON on stdin.
set -euo pipefail
payload=$(cat)
file=$(echo "$payload" | jq -r '.tool_input.file_path // empty')
[ -z "$file" ] && exit 0

if [ "$(basename "$file")" = "PREDICTION.md" ] && [ -f "$file" ] && grep -q '^PINNED:' "$file"; then
  echo "BLOCKED by prereg_guard: PREDICTION.md is hash-pinned (pre-registered). Post-pin edits destroy the audit trail. Parameter changes = tuning events: log in TUNING_LOG.md; affected comparisons become FIT (prereg-pipeline skill)." >&2
  exit 2
fi

if echo "$file" | grep -qE '(^|/)data/raw/'; then
  echo "BLOCKED by prereg_guard: data/raw/ is immutable. Fetch corrected data via scripts/fetch_data.py with a new data/MANIFEST.md entry." >&2
  exit 2
fi
exit 0
