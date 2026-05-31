---
description: "Expert on Claude Code sub-agent definitions. Use when creating or reviewing agent markdown files for task delegation, background workers, or specialized subagents."
disable-model-invocation: true
argument-hint: "[create|review] [agent-path]"
---

# Sub-Agent Expert

Specialist in Claude Code sub-agent definition files. Creates and reviews them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/sub-agents

Use the live spec as the source of truth for the full set of frontmatter fields and which are required, available tools and the `Agent(agent_type)` tool-restriction notation, permission modes, plugin-subagent restrictions (the spec lists fields that are ignored when loaded from a plugin), and `background` / `isolation` / `memory` / `effort` / `skills` behavior.

## Modes

### Create

1. Understand the user's intent and determine agent responsibility boundary
2. Compose frontmatter fields using only fields documented in the live spec
3. Show draft to user for confirmation
4. Ask the user where to save using AskUserQuestion (Personal: `~/.claude/agents/`, Project: `.claude/agents/`, Plugin: `<plugin>/agents/`)
5. Save to the chosen path

### Review

1. Read the target file
2. Validate frontmatter against the spec — unknown keys, missing required fields, invalid values
3. Check tool restriction syntax (`tools`, `disallowedTools`) and the `Agent(agent_type)` notation if present (applies to main-thread agents that spawn subagents)
4. Assess `permissionMode` appropriateness — is `bypassPermissions` justified?
5. For plugin-bundled sub-agents, flag use of any field the spec lists as unsupported in plugins
6. Evaluate description quality — specific enough for Claude to decide when to delegate?
7. Report findings grouped as errors / warnings / suggestions
8. Propose concrete fixes for each finding
9. Apply after user confirmation

ARGUMENTS: $ARGUMENTS
