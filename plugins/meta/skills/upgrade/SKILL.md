---
description: "Upgrade meta expert skills (skill, agent, hook, mcp, marketplace, plugin, rule) so their guidance reflects the current Claude Code spec. Detects drift between SKILL.md content and the latest official docs."
disable-model-invocation: true
argument-hint: "[domain?]"
---

# Meta Upgrade

The expert SKILL.md files carry static guidance — best-practice checklists, procedures, examples — that can drift as the Claude Code spec evolves. This skill audits each expert against the latest official docs and proposes fixes.

## Targets

Domains: `skill`, `agent`, `hook`, `mcp`, `marketplace`, `plugin`, `rule`.

If `$ARGUMENTS` names one or more domains, process only those. Otherwise process all seven.

## Workflow (per expert)

1. **Read.** Open `plugins/meta/skills/<domain>/SKILL.md` and note its Knowledge Sync block — the search queries and URLs there identify the authoritative spec.
2. **Sync.** Run that Knowledge Sync procedure (WebSearch → WebFetch) to pull the freshest official docs.
3. **Diagnose drift.** Compare frontmatter and body against the docs. Flag:
   - Frontmatter keys removed, renamed, or required keys missing
   - Procedures referencing removed/renamed features
   - Best-practice items the current spec contradicts
   - Examples using outdated syntax
   - Knowledge Sync queries or URLs that no longer hit live docs
4. **Propose patch.** Group findings as **must-fix** (spec contradiction) and **nice-to-have** (clarity, freshness). Show concrete Edit diffs.
5. **Apply.** After user confirmation, apply with Edit. If the user defers, skip and continue.

## After All Targets

- Re-check sibling dispatchers (e.g., `meta:review` routing table) for stale references to the expert set.
- If any SKILL.md changed, recommend a `meta` plugin version bump in `.claude-plugin/marketplace.json` — do not apply it automatically; let the user decide patch vs minor.

ARGUMENTS: $ARGUMENTS
