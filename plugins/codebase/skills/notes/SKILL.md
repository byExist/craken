---
description: "Recall and record per-repo notes under plugin data — what it takes to work a repo beyond a fresh worktree, kept across worktrees. Referenced by the work skill, which passes <owner>/<repo>."
user-invocable: false
allowed-tools: Read, Write, Edit, Bash(cat *), Bash(echo *), Bash(mkdir *)
---

# Repo Notes

## Store

```
${CLAUDE_PLUGIN_DATA}/notes/<owner>/<repo>/
├── NOTE.md       # index
└── <page>.md     # one note each
```

Per-repo notes kept across worktrees.

## NOTE.md

```
- [<title>](<page>.md) — <summary>
...
```

## <page>.md

What to know or do to work this repo, and why.

## Recording

After the worktree is set up, record any further configuration step that was needed, or anything the user explicitly asks you to record. Show the proposed note for the user's review before writing. Create the store if it doesn't exist.

## Recall

Each page records what was true when written, so confirm the named file, command, or version still holds before relying on it.

Below is this repo's NOTE.md. Read any page that fits the task.

!`cat ${CLAUDE_PLUGIN_DATA}/notes/$ARGUMENTS/NOTE.md 2>/dev/null || echo '<empty>'`
