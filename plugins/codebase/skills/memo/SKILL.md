---
description: "Recall and record what a read of a repo doesn't surface, kept across sessions. Referenced by the with skill, which passes <owner>/<repo>."
user-invocable: false
allowed-tools: Read, Write, Edit, Bash(cat *), Bash(echo *), Bash(mkdir *)
---

# Repo Memo

## Store

```
${CLAUDE_PLUGIN_DATA}/memos/<owner>/<repo>/
├── INDEX.md      # index
└── <memo>.md     # one memo each
```

Per-repo understanding kept across sessions.

## INDEX.md

```
- [<title>](<memo>.md) — <summary>
...
```

## <memo>.md

What a read of this repo doesn't surface. One memo, one topic — a topic is one concern, not one fact. Keep a concern's steps and angles together; split only when two concerns mix.

## Recording

Record an understanding a read won't surface that you had to work out and would re-derive on a later visit — or anything the user explicitly asks you to record. Show the proposed memo for the user's review before writing. Create the store if it doesn't exist.

## Recall

Each memo records what was true when written, so confirm it against the current code before relying on it.

Below is this repo's INDEX.md. Read any memo that fits the task.

!`cat ${CLAUDE_PLUGIN_DATA}/memos/$ARGUMENTS/INDEX.md 2>/dev/null || echo '<empty>'`
