---
description: "Save non-obvious findings from exploration or work as repo memos."
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

This repo's store path and current index (create if absent):

!`d="${CLAUDE_PLUGIN_DATA}/memos/$ARGUMENTS"; echo "store: $d"; cat "$d/INDEX.md" 2>/dev/null || echo '<empty>'`

## INDEX.md

```
- [<title>](<memo>.md) — <summary>
...
```

## <memo>.md

One memo, one topic — a topic is one concern, not one fact. Keep a concern's steps and angles together; split only when two concerns mix.
