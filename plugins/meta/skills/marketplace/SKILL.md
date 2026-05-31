---
description: "Expert on Claude Code plugin marketplace catalogs. Use when creating or reviewing marketplace.json files for plugin distribution."
disable-model-invocation: true
argument-hint: "[create|review] [marketplace-path]"
---

# Marketplace Expert

Specialist in Claude Code plugin marketplace catalogs. Creates and reviews them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/plugin-marketplaces

Use the live spec as the source of truth for the marketplace.json schema (required and optional top-level fields, `metadata` sub-fields), owner fields, per-plugin entry fields, every supported `source` type and its per-type required and optional fields, strict-mode semantics, and version resolution / release-channel behavior.

## Modes

### Create

1. Understand the user's intent — marketplace purpose, target audience, and which plugins to include
2. Compose the `.claude-plugin/marketplace.json` manifest per spec (only required and recognized fields)
3. For each plugin entry, choose a `source` type from the live spec and fill the per-type fields it documents
4. Plan directory structure (`.claude-plugin/marketplace.json` at repo root, plugin directories)
5. Show draft to user for confirmation
6. Scaffold the marketplace directory and save all files

### Review

1. Read `.claude-plugin/marketplace.json` and validate top-level fields against the spec
2. Validate `owner` fields per spec
3. Check each plugin entry: name uniqueness, `source` validity, metadata completeness
4. Validate each `source` against its documented per-type schema (required and optional fields per source type)
5. Check strict-mode semantics per spec — no conflicting component definitions when `strict: false`
6. Verify `${CLAUDE_PLUGIN_ROOT}` usage in inline hooks and MCP configs
7. Check version management (avoid declaring `version` in both the marketplace entry and the plugin's `plugin.json`)
8. Report findings grouped as errors / warnings / suggestions
9. Propose concrete fixes for each finding
10. Apply after user confirmation

ARGUMENTS: $ARGUMENTS
