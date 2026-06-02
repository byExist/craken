---
description: "Expert on Claude Code plugin marketplace catalogs. Use when creating or reviewing marketplace.json files for plugin distribution."
user-invocable: false
argument-hint: "[create|review] [marketplace-path]"
---

# Marketplace Expert

Specialist in Claude Code plugin marketplace catalogs. Creates and reviews them against the live spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/plugin-marketplaces

Treat the live spec as the source of truth for the marketplace.json schema (required and optional top-level fields, `metadata` sub-fields), owner fields, per-plugin entry fields, every supported `source` type and its per-type fields, strict-mode semantics, and version resolution / release-channel behavior.

## Create

Compose the `.claude-plugin/marketplace.json` at the repo root and confirm before scaffolding. For each plugin entry, pick a `source` type from the spec and fill the fields that type documents — the per-type schema is the part that's easy to get wrong.

## Review

Read the catalog and report findings, applying fixes once confirmed. Past top-level field conformance, weigh:

- **Owner & entries** — `owner` fields valid; each plugin entry has a unique name, valid `source`, and complete metadata.
- **Source schema** — every `source` validates against its own per-type required/optional fields.
- **Strict mode** — no conflicting component definitions when `strict: false`.
- **Substitutions** — `${CLAUDE_PLUGIN_ROOT}` correct in any inline hooks or MCP configs.
- **Version** — don't declare `version` in both the marketplace entry and the plugin's `plugin.json`.

ARGUMENTS: $ARGUMENTS
