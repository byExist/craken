---
description: "Make code changes to a GitHub repo in an isolated worktree — branch, edit, and commit under ~/.worktree/. Use when editing or contributing to a repo, not just reading it."
argument-hint: "<repo-name> <branch> <request>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo, branch (ask if not given), the change.
2. Prepare the worktree via `codebase:worktree` → `~/.worktree/<owner>/<repo>/<branch>/`.
3. Recall this repo's memo via `codebase:memo <owner>/<repo>`.

## Environment

- Work inside `~/.worktree/<owner>/<repo>/<branch>/`.
- `~/.codebase/` stays read-only here — it holds the local clones.
