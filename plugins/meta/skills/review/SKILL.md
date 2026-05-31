---
description: "Review a Claude Code harness artifact by dispatching to the appropriate meta expert skill (skill, agent, hook, mcp, marketplace, plugin, rule)."
disable-model-invocation: true
argument-hint: "[path-or-keyword]"
---

# Review Dispatcher

Identify the domain of the target artifact and invoke the matching meta expert skill in review mode. This skill itself does not evaluate — it routes.

## Workflow

1. **Resolve target.** Parse `$ARGUMENTS`. Accept a file/directory path, a bare domain keyword (`skill`, `agent`, `hook`, `mcp`, `marketplace`, `plugin`, `rule`), or natural-language phrasing that names a file. If empty or ambiguous, ask the user what to review.
2. **Classify domain.** Apply the routing table below — first match wins. If multiple patterns match or none match, list the candidates and ask via AskUserQuestion (single-select).
3. **Dispatch.** Invoke the matching expert skill via the Skill tool with `review <path>` as the argument. For multiple targets, dispatch sequentially.

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

When only a domain keyword is given, ask for the path before dispatching.

## Dispatch Map

- `skill` → `Skill(skill="meta:skill", args="review <path>")`
- `agent` → `Skill(skill="meta:agent", args="review <path>")`
- `hook` → `Skill(skill="meta:hook", args="review <path>")`
- `mcp` → `Skill(skill="meta:mcp", args="review <path>")`
- `marketplace` → `Skill(skill="meta:marketplace", args="review <path>")`
- `plugin` → `Skill(skill="meta:plugin", args="review <path>")`
- `rule` → `Skill(skill="meta:rule", args="review <path>")`

ARGUMENTS: $ARGUMENTS
