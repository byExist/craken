#!/usr/bin/env bash
# SessionStart: restore THIS session's selected voice persona.
# Personas authored by /voice:new live in $CLAUDE_PLUGIN_DATA/personas/<name>.md.
# The per-session selection lives in $CLAUDE_PLUGIN_DATA/state/<session_id>.
# session_id comes from the hook's stdin JSON (hook commands don't get
# ${CLAUDE_SESSION_ID} substitution). The persona printed to stdout is injected
# as context at session start.
set -euo pipefail

dir="${CLAUDE_PLUGIN_DATA:-}"
[ -n "$dir" ] || exit 0

state_dir="$dir/state"

# GC: drop stale per-session selections (>7 days). Personas are never touched.
[ -d "$state_dir" ] && find "$state_dir" -type f -mtime +7 -delete 2>/dev/null || true

input="$(cat)"
if command -v jq >/dev/null 2>&1; then
  sid="$(printf '%s' "$input" | jq -r '.session_id // empty')"
else
  sid="$(printf '%s' "$input" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
fi
[ -n "$sid" ] || exit 0

state="$state_dir/$sid"
[ -f "$state" ] || exit 0

voice="$(cat "$state" 2>/dev/null || true)"
[ -n "$voice" ] || exit 0
# Persona names are slugs; reject anything else to guard against path traversal.
case "$voice" in *[!a-zA-Z0-9_-]*) exit 0 ;; esac

persona="$dir/personas/${voice}.md"
[ -f "$persona" ] && cat "$persona"
exit 0
