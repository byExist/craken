---
description: "Upgrade meta expert skills (skill, agent, hook, mcp, marketplace, plugin, rule) so their guidance reflects the current Claude Code spec. Detects drift between SKILL.md content and the latest official docs."
disable-model-invocation: true
argument-hint: "[domain?]"
---

# Meta Upgrade

The expert SKILL.md files carry static guidance — checklists, procedures, examples — that drifts as the Claude Code spec evolves. This skill audits each expert against the latest official docs and proposes fixes.

Targets: `skill`, `agent`, `hook`, `mcp`, `marketplace`, `plugin`, `rule`. If `$ARGUMENTS` names domains, process only those; otherwise all seven.

## Per Expert

**Sync, then diagnose.** Open the expert's `SKILL.md`, run its Knowledge Sync block (the queries/URLs there are the authoritative spec) to pull the freshest docs, then compare frontmatter and body against them. Flag drift:

- Frontmatter keys removed, renamed, or required keys now missing
- Procedures referencing removed/renamed features
- Best-practice items the current spec contradicts
- Examples using outdated syntax
- Knowledge Sync queries or URLs that no longer hit live docs

**Propose, then apply.** Group findings as **must-fix** (spec contradiction) vs. **nice-to-have** (clarity, freshness), show concrete Edit diffs, and apply on confirmation — skip and continue if the user defers.

## After All Targets

- Re-check sibling dispatchers (e.g., `meta:review` routing table) for stale references to the expert set.
- If any SKILL.md changed, recommend a `meta` version bump in `.claude-plugin/marketplace.json` — don't apply automatically; let the user decide patch vs. minor.

ARGUMENTS: $ARGUMENTS
