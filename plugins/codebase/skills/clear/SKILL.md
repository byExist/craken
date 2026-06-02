---
description: "Clean up locally cached repos under ~/.codebase/. List repos with disk usage, select and remove unused ones."
disable-model-invocation: true
argument-hint: "[keyword]"
allowed-tools: Bash(du *), Bash(ls *), Bash(rmdir *), Bash(rm -rf ~/.codebase/*)
---

## Cached Repos (disk usage)

!`du -sh ~/.codebase/*/* 2>/dev/null | sort -rh`

## Workflow

### Step 1: Select

If the list above is empty, tell the user there is nothing to clean and stop. Otherwise present it via AskUserQuestion (multiSelect: true); if a keyword was given, pre-filter to matching repos.

### Step 2: Remove

Confirm the selection, then delete:

```bash
rm -rf ~/.codebase/<owner>/<repo>
```

Clean up empty owner directories afterward.
