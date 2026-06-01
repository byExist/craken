---
description: "Expert on Claude Code sub-agent definitions. Use when creating or reviewing agent markdown files for task delegation, background workers, or specialized subagents."
disable-model-invocation: true
argument-hint: "[create|review] [agent-path]"
---

# Sub-Agent Expert

Specialist in Claude Code sub-agent definition files. Creates and reviews them against the live spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/sub-agents

Treat the live spec as the source of truth for the full set of frontmatter fields and which are required, available tools and the `Agent(agent_type)` tool-restriction notation, permission modes, plugin-subagent restrictions (fields the spec says are ignored when loaded from a plugin), and `background` / `isolation` / `memory` / `effort` / `skills` behavior.

## Create

Draft the agent from the user's intent, confirm, and save to a spec-valid location (`~/.claude/agents/`, `.claude/agents/`, or `<plugin>/agents/` — ask if unclear). Agent-specific judgment the spec won't make for you:

- Define a sharp responsibility boundary — an agent is a delegation unit; vague scope makes it fire on the wrong work.
- The `description` is the delegation trigger — make it concrete about *when* to delegate here.
- Grant the narrowest tools that do the job, and justify any non-default `permissionMode`.

## Review

Read the target and report findings, applying fixes once confirmed. Past plain spec-conformance of frontmatter, weigh:

- **Tool restrictions** — `tools` / `disallowedTools` syntax, and the `Agent(agent_type)` notation if present (applies to main-thread agents that spawn subagents).
- **Permission** — is a non-default `permissionMode` (especially `bypassPermissions`) justified?
- **Plugin limits** — for plugin-bundled agents, flag any field the spec lists as unsupported there.
- **Trigger quality** — is `description` specific enough for Claude to decide when to delegate?

ARGUMENTS: $ARGUMENTS
