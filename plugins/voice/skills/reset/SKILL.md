---
description: "Clear the active voice and revert to the default response style."
disable-model-invocation: true
---

!`rm -f "${CLAUDE_PLUGIN_DATA}/state/${CLAUDE_SESSION_ID}"`

Voice cleared. Revert to your default response style for the rest of the session. If a default is configured in plugin settings, it will be restored when this session resumes; otherwise no persona returns.
