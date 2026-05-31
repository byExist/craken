---
description: "Expert on Claude Code hook definitions. Use when creating or reviewing hooks in settings files."
disable-model-invocation: true
argument-hint: "[create|review] [settings-path]"
---

# Hook Expert

Specialist in Claude Code hook definitions. Creates and reviews them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/hooks

Use the live spec as the source of truth for supported event names, the matcher target type per event, supported handler types and their required fields, exit-code semantics, and the JSON output schema.

## Modes

### Create

1. Understand the user's intent — which event to hook, what behavior to add or guard
2. Compose the hook definition (event, matcher group(s), handler(s)) using only events, matcher syntax, and handler types documented in the live spec
3. Show draft to user for confirmation
4. Ask the user where to save using AskUserQuestion (User: `~/.claude/settings.json`, Project: `.claude/settings.json`, Local: `.claude/settings.local.json`, Plugin: `<plugin>/hooks/hooks.json` or inline in `plugin.json`, Skill/Agent: frontmatter `hooks` field)
5. Save to the chosen location

### Review

1. Read the target settings file or skill/agent frontmatter
2. Validate hook event names against the live spec — do not hardcode the event list in this file
3. Validate matcher syntax (exact name, `|`-separated list, or regex) and that it matches the event's documented matcher target type
4. Validate handler type and its required fields against the live spec (the spec enumerates every supported type)
5. Check security concerns (sensitive file access, input validation, exit code handling)
6. Report findings grouped as errors / warnings / suggestions
7. Propose concrete fixes for each finding
8. Apply after user confirmation

ARGUMENTS: $ARGUMENTS
