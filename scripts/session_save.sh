#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSIONS_DIR="$REPO_ROOT/SESSIONS"
TODAY="$(date +%F)"
TODAY_FILE="$SESSIONS_DIR/SESSION_${TODAY}.md"
LAST_FILE="$SESSIONS_DIR/LAST_SESSIONS.md"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
SESSION_NOTES="${SESSION_NOTES:-}"

mkdir -p "$SESSIONS_DIR"

if [[ ! -f "$TODAY_FILE" ]]; then
  printf '%s\n' \
    "Missing today session file: $TODAY_FILE" \
    "Run: make session-start" >&2
  exit 1
fi

if [[ -n "$SESSION_NOTES" ]]; then
  {
    printf '\n## Save Snapshot %s\n\n' "$TIMESTAMP"
    OLD_IFS="$IFS"
    IFS='|'
    read -r -a raw_items <<< "${SESSION_NOTES//||/|}"
    IFS="$OLD_IFS"

    for item in "${raw_items[@]}"; do
      [[ -z "$item" ]] && continue
      printf -- '- %s\n' "$item"
    done
  } >> "$TODAY_FILE"
fi

cp "$TODAY_FILE" "$LAST_FILE"

printf '%s\n' \
  "Saved session snapshot." \
  "Today file: $TODAY_FILE" \
  "Synced copy: $LAST_FILE"
