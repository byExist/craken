---
description: "Review one or more Claude Code harness artifacts by enumerating their review units and dispatching each to the matching meta expert skill (skill, agent, hook, mcp, marketplace, plugin, rule)."
disable-model-invocation: true
argument-hint: "[path-or-keyword ...]"
---

# Review Dispatcher

Work out which units a target breaks down into, then hand each to its matching meta expert in review mode. This skill routes; it does not evaluate.

## Workflow

1. **Resolve targets.** Parse `$ARGUMENTS` — one or more file/directory paths, bare domain keywords, or natural-language phrasing that names files. If empty or ambiguous, ask what to review. Given only a domain keyword with no path, ask for the path.
2. **Enumerate review units.** For each target, list what to review:
   - A directory with `.claude-plugin/plugin.json` → one `plugin` unit. Review the package against the plugin spec; do **not** descend into its skills/agents/hooks.
   - Any single file or manifest the table matches → one unit of that domain.
   - A plain directory (no `plugin.json`) → every leaf the table matches beneath it, but stop at any nested `plugin.json` (that subtree is one `plugin` unit, not its leaves).
3. **Dispatch each unit.** For every enumerated unit, invoke `Skill(skill="meta:<domain>", args="review <path>")`, one at a time.

## Identification Table

| Artifact | Domain |
| --- | --- |
| Directory with `.claude-plugin/plugin.json` | `plugin` |
| `**/SKILL.md` | `skill` |
| `**/.claude/agents/**/*.md`, `**/agents/*.md` | `agent` |
| `settings.json` / `settings.local.json` with a `hooks` key, or a hook script referenced from one | `hook` |
| `**/.mcp.json`, `**/mcp.json` | `mcp` |
| `**/.claude-plugin/marketplace.json`, `**/marketplace.json` | `marketplace` |
| `**/.claude/rules/**/*.md`, `**/rules/*.md` | `rule` |

ARGUMENTS: $ARGUMENTS
