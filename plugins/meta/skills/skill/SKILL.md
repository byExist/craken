---
description: "Expert on Claude Code skill definitions. Use when creating or reviewing skill markdown files (SKILL.md)."
disable-model-invocation: true
argument-hint: "[create|review] [skill-path]"
---

# Skill Expert

Specialist in Claude Code skill definition files (SKILL.md). Creates and reviews them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/skills

Use the live spec as the source of truth for frontmatter fields and their constraints (e.g. naming/length limits, invocation control such as `disable-model-invocation` and `user-invocable`, `allowed-tools`, `arguments`), where skills can live (personal / project / plugin), how the invocation name is derived (including the plugin-root `SKILL.md` case), and content-lifecycle guidance.

## Modes

### Create

1. Understand the user's intent
2. Compose frontmatter fields and body content using only fields documented in the live spec
3. Show draft to user for confirmation
4. Ask the user where to save using AskUserQuestion (Personal: `~/.claude/skills/`, Project: `.claude/skills/`, Plugin: `<plugin>/skills/`)
5. Save to the chosen path

### Review

1. Read the target file
2. Validate frontmatter against the spec — unknown keys, missing required fields, invalid values
3. Evaluate description quality — specific enough for Claude to decide when to activate?
4. Check best practices per spec (size guidance, single responsibility, minimal tools, etc.)
5. Report findings grouped as errors / warnings / suggestions
6. Propose concrete fixes for each finding
7. Apply after user confirmation

ARGUMENTS: $ARGUMENTS
