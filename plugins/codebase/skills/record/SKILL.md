---
description: "Record a repo memo after exploration or work is done — what a read or checkout didn't surface. Referenced by the with and work skills, which pass <owner>/<repo>."
user-invocable: false
allowed-tools: Read, Write, Edit, Bash(cat *), Bash(echo *), Bash(mkdir *)
---

# Record a Memo

## Store

```
${CLAUDE_PLUGIN_DATA}/memos/<owner>/<repo>/
├── INDEX.md      # index
└── <memo>.md     # one memo each
```

This repo's store path and current index:

!`d="${CLAUDE_PLUGIN_DATA}/memos/$ARGUMENTS"; echo "store: $d"; cat "$d/INDEX.md" 2>/dev/null || echo '<empty>'`

## INDEX.md

```
- [<title>](<memo>.md) — <summary>
...
```

## <memo>.md

What a read or checkout of this repo doesn't surface — an understanding you had to work out, or a setup step a fresh checkout needs. One memo, one topic — a topic is one concern, not one fact. Keep a concern's steps and angles together; split only when two concerns mix.

## When to record

Only after the exploration or work is complete — not mid-task. Then review what's worth keeping: an understanding you had to work out and would re-derive on a later visit, a setup step a fresh checkout needed — or anything the user explicitly asks you to record. Show the proposed memo for the user's review before writing. Create the store if it doesn't exist, and update INDEX.md alongside.
