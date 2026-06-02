---
description: "Expert on Claude Code hook definitions. Use when creating or reviewing hooks in settings files."
user-invocable: false
argument-hint: "[create|review] [settings-path]"
---

# Hook Expert

Specialist in Claude Code hook definitions. Creates and reviews them against the live spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/hooks

Treat the live spec as the source of truth for supported event names, the matcher target type per event, supported handler types and their required fields, exit-code semantics, and the JSON output schema.

## Create

Pin down which event to hook and what behavior to add or guard, draft the definition (event, matcher group(s), handler(s)) from the spec's vocabulary, confirm, and save to the right place — scope decides where: `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`, a plugin's `hooks/hooks.json` or inline `plugin.json`, or a skill/agent's `hooks` frontmatter. Hook-specific judgment:

- Use only event names, matcher syntax, and handler types the live spec documents — never invent them.
- A matcher must fit the event's documented target type; not every event matches on tool name.

## Review

Read the target settings file or skill/agent frontmatter and report findings, applying fixes once confirmed. Weigh:

- **Event validity** — check names against the live spec; never hardcode the event list here.
- **Matcher** — exact name, `|`-list, or regex, and that it fits the event's documented matcher target.
- **Handler** — type and required fields per spec (the spec enumerates every supported type).
- **Security** — sensitive-file access, input validation, exit-code handling.

ARGUMENTS: $ARGUMENTS
