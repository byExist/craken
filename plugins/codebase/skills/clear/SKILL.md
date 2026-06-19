---
description: "Free up disk by removing locally cloned repos that are no longer needed."
argument-hint: "[keyword]"
allowed-tools: Bash(du *), Bash(ls *), Bash(rmdir *), Bash(rm -rf ~/.codebase/*)
---

## Local Clones (disk usage)

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
