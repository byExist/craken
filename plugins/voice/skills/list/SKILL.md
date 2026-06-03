---
description: "List saved voice personas and show which one is active in this session."
disable-model-invocation: true
---

Saved personas:
!`ls -1 "${CLAUDE_PLUGIN_DATA}/personas" 2>/dev/null | sed 's/\.md$//'`

Active in this session:
!`cat "${CLAUDE_PLUGIN_DATA}/state/${CLAUDE_SESSION_ID}" 2>/dev/null || echo "(none)"`

Present this to the user concisely. If no personas are saved, suggest creating one with `/voice:new`.
