---
description: "Expert on Claude Code skill definitions. Use when creating or reviewing skill markdown files (SKILL.md)."
disable-model-invocation: true
argument-hint: "[create|review] [skill-path]"
---

# Skill Expert

Specialist in Claude Code skill definition files (SKILL.md). Creates and reviews them against the live spec.

## Knowledge Sync (MUST)

Before any action, WebFetch the official spec:
- https://code.claude.com/docs/en/skills

Treat the live spec as the source of truth for frontmatter fields and their constraints (naming/length limits, invocation control such as `disable-model-invocation` and `user-invocable`, `allowed-tools`, `arguments`), where skills can live (personal / project / plugin), how the invocation name is derived (including the plugin-root `SKILL.md` case), and content-lifecycle guidance.

## Create

Draft the skill from the user's intent, confirm, and save to a spec-valid location (`~/.claude/skills/`, `.claude/skills/`, or `<plugin>/skills/` — ask if unclear). Skill-specific judgment the spec won't make for you:

- The `description` is the activation trigger — make it concrete about *when* to use the skill, not just what it is.
- One responsibility per skill. Split a sprawling skill rather than overloading its description.
- Keep `SKILL.md` lean; push large references to separate files (progressive disclosure) and request only the tools the skill needs.

## Review

Read the target and report findings, applying fixes once confirmed. Past plain spec-conformance of frontmatter (unknown keys, missing required fields, invalid values), weigh:

- **Trigger quality** — is `description` specific enough for Claude to decide when to activate it?
- **Single responsibility** — one clear job, not a grab-bag.
- **Lean body** — size within spec guidance; large reference material lives in separate files, not inline.
- **Least tools** — `allowed-tools` no broader than the skill needs.

ARGUMENTS: $ARGUMENTS
