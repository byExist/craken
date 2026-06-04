---
description: "Delete a saved voice persona by name."
argument-hint: "<name>"
disable-model-invocation: true
allowed-tools: Read, Bash(rm *)
---

Delete the voice persona "$ARGUMENTS".

1. Confirm `${CLAUDE_PLUGIN_DATA}/personas/$ARGUMENTS.md` exists. If not, tell the user and stop.
2. Delete that file.
3. If `${CLAUDE_PLUGIN_DATA}/state/${CLAUDE_SESSION_ID}` contains "$ARGUMENTS", delete that state file too and revert to your default response style.
4. Confirm what was removed.
