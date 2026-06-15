---
description: "Recall a repo's memos — read the index, open what fits. Referenced by the with and work skills at setup, which pass <owner>/<repo>."
user-invocable: false
allowed-tools: Read, Bash(cat *), Bash(echo *)
---

# Recall Memos

Per-repo understanding kept across sessions, written by `codebase:record`. Each memo records what was true when written, so confirm it against the current code — named files, commands, versions — before relying on it.

Below is this repo's store path and memo index. Read any memo needed for the task.

!`d="${CLAUDE_PLUGIN_DATA}/memos/$ARGUMENTS"; echo "store: $d"; cat "$d/INDEX.md" 2>/dev/null || echo '<empty>'`
