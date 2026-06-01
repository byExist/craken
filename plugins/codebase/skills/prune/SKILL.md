---
description: "Clean up worktrees and merged branches under ~/.worktree/. List worktrees with merge status, select and remove merged or stale ones."
disable-model-invocation: true
argument-hint: "[keyword]"
allowed-tools: Bash(git *), Bash(du *), Bash(ls *), Bash(rm -rf ~/.worktree/*)
---

## Request

$ARGUMENTS

## Workflow

### Step 1: List Worktrees

For each repo under `~/.worktree/`, list worktrees and which branches are already merged into `main`:

```bash
git -C ~/.worktree/<owner>/<repo> worktree list
git -C ~/.worktree/<owner>/<repo> branch --merged main
```

If empty, inform the user and stop.

### Step 2: Select

Present the worktrees via AskUserQuestion (multiSelect: true), flagging which are **merged** (safe to remove) vs **unmerged** (would lose work).

### Step 3: Remove

Confirm selection, then for each:

```bash
cd ~/.worktree/<owner>/<repo>
git worktree remove <branch>
git branch -d <branch>      # merged only
git worktree prune
```

Clean up empty owner directories afterward.

## Rules

- **Never remove `main` or `.bare`** — removing them breaks the repo.
- Default to `git branch -d` (refuses unmerged branches). Use `-D` only on explicit user confirmation.
- Leave `~/.codebase/` alone — use `codebase:clear` for the research cache.
