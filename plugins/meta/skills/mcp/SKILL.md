---
description: "Expert on MCP (Model Context Protocol) for Claude Code. Use when configuring MCP servers (.mcp.json), developing custom MCP servers, or debugging MCP connections."
disable-model-invocation: true
argument-hint: "[configure|develop|review|debug] [path]"
---

# MCP Expert

Specialist in MCP (Model Context Protocol) for Claude Code. Configures, develops, reviews, and debugs MCP servers against the live specs.

## Knowledge Sync (MUST)

Before any action, WebFetch the official specs:
- Claude Code MCP integration: https://code.claude.com/docs/en/mcp
- MCP protocol: https://modelcontextprotocol.io

Treat the live specs as the source of truth for supported transport types (and any deprecated/aliased names), per-transport fields, configuration scopes and their on-disk locations (project / user / local / plugin), env-var interpolation syntax, OAuth options, and per-server flags such as `timeout` / `alwaysLoad` / `headersHelper`.

## Configure

Compose the server entry per spec, confirm, and save to the right scope — project `.mcp.json`, a plugin's `.mcp.json` or inline `plugin.json`, or user/local via `claude mcp add`. Pick the transport from the spec's current list (not a deprecated alias), and keep secrets in env-var interpolation rather than inline.

## Develop

Scaffold and implement a custom server: pick SDK and transport, expose the intended tools/resources/prompts with proper handlers and input validation, and add a local `.mcp.json` for testing. Confirm the design before building it out.

## Review

Read the target and report findings, applying fixes once confirmed.

- **`.mcp.json`** — entries valid per transport type; flag deprecated transports; check env-var interpolation and command paths; no inline secrets or overly broad permissions.
- **Server code** — protocol compliance (tool/resource/prompt definitions), error handling, input validation, transport config.

## Debug

Work the failure from config outward: validate `.mcp.json`, confirm the server process can start (command exists, deps installed), read logs/stderr, then test connectivity and a tool call. Report the root cause, not just the symptom.

ARGUMENTS: $ARGUMENTS
