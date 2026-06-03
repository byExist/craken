---
description: "Author a new response-voice persona with the user through a brief Q&A, then save it for reuse with /voice:use."
disable-model-invocation: true
allowed-tools: Write
---

Create a new voice persona with the user, then save it.

!`mkdir -p "${CLAUDE_PLUGIN_DATA}/personas"`

Personas that already exist — don't clobber one unless the user means to:
!`ls -1 "${CLAUDE_PLUGIN_DATA}/personas" 2>/dev/null | sed 's/\.md$//'`

Follow this persona file format exactly:

!`cat "${CLAUDE_SKILL_DIR}/template.md"`

Steps:

1. If the user already described the voice they want (how to think, what to lead with, tone, what to avoid), use that. Otherwise ask one or two focused questions to pin it down.
2. Pick a short lowercase slug for the name, or use the one the user gave. If that slug already appears in the list above, tell the user and confirm before overwriting.
3. Write the persona to `${CLAUDE_PLUGIN_DATA}/personas/<slug>.md` following the format above.
4. Tell the user it is saved and can be activated with `/voice:use <slug>`.

Do not adopt the voice yourself — `new` only authors and saves. Activation is `/voice:use`.
