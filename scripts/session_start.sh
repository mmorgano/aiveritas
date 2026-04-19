#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSIONS_DIR="$REPO_ROOT/SESSIONS"
TODAY="$(date +%F)"
TODAY_FILE="$SESSIONS_DIR/SESSION_${TODAY}.md"
LAST_FILE="$SESSIONS_DIR/LAST_SESSIONS.md"

mkdir -p "$SESSIONS_DIR"

if [[ ! -f "$TODAY_FILE" ]]; then
  cat > "$TODAY_FILE" <<EOF
# Session ${TODAY}

## Goal

- Define the current working goal.

## Current Context

- Branch:
- Related files:
- Constraints:

## Completed

- 

## Decisions

- 

## Next Steps

- [ ] Review LAST_SESSIONS.md
- [ ] Confirm the immediate next code or documentation change

## Resume Prompt

Use this session file and LAST_SESSIONS.md to resume work.
Summarize the latest progress, identify the first unfinished next step, and continue with the smallest useful change.
EOF
fi

if [[ ! -f "$LAST_FILE" ]]; then
  cp "$TODAY_FILE" "$LAST_FILE"
fi

NEXT_STEP="$(
  awk '
    /^## Next Steps/ { in_section=1; next }
    /^## / && in_section { exit }
    in_section && /^\- \[ \]/ { sub(/^- \[ \] /, ""); print; exit }
  ' "$LAST_FILE"
)"

if [[ -z "$NEXT_STEP" ]]; then
  NEXT_STEP="Review the latest session notes and choose the smallest unfinished task."
fi

printf '%s\n' \
  "Session file: $TODAY_FILE" \
  "Last session copy: $LAST_FILE" \
  "" \
  "Suggested next step:" \
  "- $NEXT_STEP" \
  "" \
  "Recent session context:" \
  ""

sed -n '1,120p' "$LAST_FILE"
