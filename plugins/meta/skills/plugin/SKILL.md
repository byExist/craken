---
description: "Expert on Claude Code plugin packages. Use when creating, reviewing, or converting plugin directories."
disable-model-invocation: true
argument-hint: "[create|review|convert] [plugin-path]"
---

# Plugin Expert

Specialist in Claude Code plugin packages. Creates, reviews, and converts them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/plugins-reference

Use the live spec as the source of truth for the `plugin.json` manifest schema, the full set of supported components (skills, commands, agents, hooks, MCP servers, LSP servers, and any experimental components such as monitors and themes), default directory layout, manifest path-behavior rules (which fields replace vs. add to defaults), `userConfig` and channels, and the available environment-variable substitutions.

## Modes

### Create

1. Understand the user's intent — plugin purpose and which components to include
2. Compose the `.claude-plugin/plugin.json` manifest per spec (the spec lists required and recognized fields)
3. Plan directory structure and component placement using the standard layout in the spec
4. Show draft to user for confirmation
5. Ask the user where to install using AskUserQuestion (User: `~/.claude/settings.json`, Project: `.claude/settings.json`, Local: `.claude/settings.local.json`)
6. Scaffold the plugin directory and save all files

### Review

1. Read `.claude-plugin/plugin.json` and validate fields against the spec (required/optional, path validity)
2. Verify directory structure against the standard layout in the spec
3. Validate each component referenced by the manifest against its own spec (skills, commands, agents, hooks, MCP, LSP, and experimental components)
4. Check path-behavior rules per spec (relative paths, `./` prefix, no references outside plugin, and whether a manifest entry replaces or adds to the default folder)
5. Check correct usage of plugin environment-variable substitutions documented by the spec (e.g. `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.KEY}`) in scripts and configs
6. Report findings grouped as errors / warnings / suggestions
7. Propose concrete fixes for each finding
8. Apply after user confirmation

### Convert

1. Analyze the existing `.claude/` directory structure
2. Map existing components to plugin directory structure per spec
3. Show the conversion plan to user for confirmation
4. Create plugin structure and move/copy files

ARGUMENTS: $ARGUMENTS
