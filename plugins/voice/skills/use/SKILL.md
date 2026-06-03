---
description: "Activate a saved voice persona by name and keep it for the rest of the session."
argument-hint: "<name>"
disable-model-invocation: true
allowed-tools: Read, Write
---

Activate the voice persona "$ARGUMENTS".

!`mkdir -p "${CLAUDE_PLUGIN_DATA}/state"`

1. Read `${CLAUDE_PLUGIN_DATA}/personas/$ARGUMENTS.md`. If it does not exist, stop and tell the user to run `/voice:list` to see what is available.
2. Record the selection so it restores when this session is resumed: write the single line `$ARGUMENTS` to `${CLAUDE_PLUGIN_DATA}/state/${CLAUDE_SESSION_ID}`.
3. Adopt that persona's voice now and maintain it for the rest of the session.
