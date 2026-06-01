---
description: "Review a Claude Code harness artifact by dispatching to the appropriate meta expert skill (skill, agent, hook, mcp, marketplace, plugin, rule)."
disable-model-invocation: true
argument-hint: "[path-or-keyword]"
---

# Review Dispatcher

Identify the domain of the target artifact and invoke the matching meta expert skill in review mode. This skill routes; it does not evaluate.

## Workflow

1. **Resolve target.** Parse `$ARGUMENTS` — a file/directory path, a bare domain keyword, or natural-language phrasing that names a file. If empty or ambiguous, ask what to review.
2. **Classify domain.** Apply the routing table below; first match wins. If several match or none do, list the candidates and ask via AskUserQuestion (single-select). Given only a domain keyword, ask for the path first.
3. **Dispatch.** Invoke the matched expert via `Skill(skill="meta:<domain>", args="review <path>")`. For multiple targets, dispatch sequentially.

## Routing Table

| Target | Domain |
| --- | --- |
| `**/SKILL.md` or a directory containing one | `skill` |
| `**/.claude/agents/**/*.md`, `**/agents/*.md` | `agent` |
| `settings.json` / `settings.local.json` containing a `hooks` key, or a hook script referenced from one | `hook` |
| `**/.mcp.json`, `**/mcp.json` | `mcp` |
| `**/.claude-plugin/marketplace.json`, `**/marketplace.json` | `marketplace` |
| Directory containing `.claude-plugin/plugin.json` | `plugin` |
| `**/.claude/rules/**/*.md`, `**/rules/*.md` | `rule` |

ARGUMENTS: $ARGUMENTS
