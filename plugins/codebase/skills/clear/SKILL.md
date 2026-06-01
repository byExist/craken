---
description: "Clean up locally cached repos under ~/.codebase/. List repos with disk usage, select and remove unused ones."
disable-model-invocation: true
argument-hint: "[keyword]"
allowed-tools: Bash(du *), Bash(ls *), Bash(rmdir *), Bash(rm -rf ~/.codebase/*)
---

## Request

$ARGUMENTS

## Workflow

### Step 1: List Cached Repos

```bash
du -sh ~/.codebase/*/* 2>/dev/null | sort -rh
```

If empty, inform the user and stop.

### Step 2: Select

Present the list via AskUserQuestion (multiSelect: true).

### Step 3: Remove

Confirm selection, then delete.

```bash
rm -rf ~/.codebase/<owner>/<repo>
```

Clean up empty owner directories afterward.
