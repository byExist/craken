---
description: "Clean up worktrees and branches when work is done."
argument-hint: "[keyword]"
allowed-tools: Bash(git *), Bash(ls *), Bash(cd *), Bash(rm -rf ~/.worktree/*)
---

## Worktrees (with merge status)

```!
for r in ~/.worktree/*/*/; do
  [ -e "${r}.git" ] || continue
  echo "## ${r}"
  git -C "$r" worktree list 2>/dev/null
  default=$(git -C "${r}.bare" symbolic-ref --short HEAD 2>/dev/null)
  echo "merged into ${default}:"
  git -C "$r" branch --merged "$default" 2>/dev/null | grep -vE "^\*? *${default}\$"
done
```

## Workflow

### Step 1: Select

If the block above is empty, tell the user there is nothing to prune and stop.

If the current conversation has an active `codebase:work` or `codebase:with` context (repo and branch are known), resolve the target worktree from that context and proceed to Step 2 directly.

Otherwise, present all worktrees via AskUserQuestion (multiSelect: true), flagging **merged** (safe to remove) vs **unmerged** (would lose work).

### Step 2: Remove

Confirm, then for each:

```bash
cd ~/.worktree/<owner>/<repo>
git worktree remove <branch>
git branch -d <branch>      # merged only
git worktree prune
```

Clean up empty owner directories afterward.

## Rules

- **Remove branch worktrees only — keep `.bare`.** It's the shared object store; losing it breaks every worktree.
- Default to `git branch -d` (refuses unmerged branches). Use `-D` only on explicit user confirmation.
