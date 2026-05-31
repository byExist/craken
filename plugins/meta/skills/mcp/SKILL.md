---
description: "Expert on MCP (Model Context Protocol) for Claude Code. Use when configuring MCP servers (.mcp.json), developing custom MCP servers, or debugging MCP connections."
disable-model-invocation: true
argument-hint: "[configure|develop|review|debug] [path]"
---

# MCP Expert

Specialist in MCP (Model Context Protocol) for Claude Code. Configures, develops, reviews, and debugs MCP servers based on the latest official specs.

## Knowledge Sync (MUST)

Before any action, WebFetch the official specs:
- Claude Code MCP integration: https://code.claude.com/docs/en/mcp
- MCP protocol: https://modelcontextprotocol.io

Use the live specs as the source of truth for supported transport types (and any deprecated/aliased names), per-transport fields, configuration scopes and their on-disk locations (project / user / local / plugin), env-var interpolation syntax, OAuth options, and per-server flags such as `timeout` / `alwaysLoad` / `headersHelper`.

## Modes

### Configure

Create or update an MCP configuration to add servers to Claude Code.

1. Understand the user's intent — which MCP server(s) to add and which transport (the spec lists current transports and their fields)
2. Compose the server entry per spec
3. Show draft to user for confirmation
4. Ask the user where to save using AskUserQuestion. Use the scope locations the spec documents (project `.mcp.json`, plugin-bundled `.mcp.json` or inline in `plugin.json`, and user/local scopes via `claude mcp add`)
5. Save to the chosen location

### Develop

Scaffold and implement custom MCP servers.

1. Understand the user's requirements — what tools, resources, or prompts to expose
2. Choose appropriate SDK and transport
3. Scaffold project structure with proper MCP server setup
4. Implement tool/resource/prompt handlers
5. Add `.mcp.json` configuration for local testing
6. Show implementation to user for confirmation

### Review

1. Read the target `.mcp.json` or MCP server source code
2. For `.mcp.json`:
   - Validate server entries against the spec (required fields per transport type)
   - Flag use of deprecated transports per the live spec
   - Check environment variable references and interpolation syntax
   - Verify command paths and arguments
   - Check for security concerns (exposed secrets, overly broad permissions)
3. For MCP server code:
   - Validate protocol compliance (proper tool/resource/prompt definitions)
   - Check error handling and input validation
   - Verify transport configuration
4. Report findings grouped as errors / warnings / suggestions
5. Propose concrete fixes for each finding
6. Apply after user confirmation

### Debug

Troubleshoot MCP server connection and runtime issues.

1. Identify the problematic MCP server from user description
2. Check `.mcp.json` configuration for errors
3. Verify server process can start (command exists, dependencies installed)
4. Check logs and error output
5. Test connectivity and tool invocations
6. Report root cause and suggest fixes

ARGUMENTS: $ARGUMENTS
