---
description: "Expert on Claude Code rule definitions. Use when creating or reviewing modular rules in .claude/rules/ directories."
disable-model-invocation: true
argument-hint: "[create|review] [rules-dir-or-file-path]"
---

# Rule Expert

Specialist in Claude Code modular rule files (`.claude/rules/*.md`). Creates and reviews them based on the latest official spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/memory (the `.claude/rules/` section covers modular rules, the `paths` frontmatter, glob support, scopes, symlinks, plugin-provided rules, and known limitations)

Use the live spec as the source of truth for recognized frontmatter, supported glob syntax, loading semantics (always-loaded vs. path-scoped, and when path-scoped rules do / do not inject), symlink behavior, plugin-provided rules, and user-level vs. project-level precedence.

## Modes

### Create

1. Understand the user's intent — what guideline or convention to codify
2. Decide scope: unconditional (always loaded) or path-scoped per spec
3. If path-scoped, compose `paths` frontmatter using the glob syntax the spec documents
4. Write focused, specific, actionable rule content (avoid vague statements like "write clean code")
5. Show draft to user for confirmation
6. Ask the user where to save using AskUserQuestion (Project: `.claude/rules/`, User: `~/.claude/rules/`, Plugin: `<plugin>/rules/`)
7. Save to the chosen path

### Review

1. Discover all `.md` files recursively under the target rules directory
2. Validate frontmatter against the spec — flag unrecognized fields
3. Validate `paths` glob patterns — check syntax against the spec and whether they match actual project files (use Glob to verify)
4. Detect overlapping rules — multiple files with identical or heavily-overlapping `paths` patterns
5. Evaluate content quality:
   - Specific and actionable? ("Use 2-space indentation" > "Format code properly")
   - Single topic per file?
   - Reasonable length? (rule files should be concise; large guidelines belong in skills)
6. Assess placement appropriateness:
   - Short, always-applicable conventions → rule or CLAUDE.md (either is fine)
   - Path-scoped conventions → rule with `paths` (good fit)
   - Large reference sets with on-demand lookup → skill (not rule)
7. Count unconditional rules and warn if excessive (context budget impact)
8. Note any limitations from the live spec relevant to the rules being reviewed (e.g., when path-scoped rules do / do not inject)
9. Report findings grouped as errors / warnings / suggestions
10. Propose concrete fixes for each finding
11. Apply after user confirmation

ARGUMENTS: $ARGUMENTS
