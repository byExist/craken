---
description: "Clear the active voice and revert to the default response style."
disable-model-invocation: true
---

!`rm -f "${CLAUDE_PLUGIN_DATA}/state/${CLAUDE_SESSION_ID}"`

Voice cleared. Revert to your default response style for the rest of the session, and don't restore any persona when this session is resumed.
