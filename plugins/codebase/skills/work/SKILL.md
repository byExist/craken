---
description: "Make code changes to a GitHub repo in an isolated worktree — branch, edit, and commit under ~/.worktree/. Use when editing or contributing to a repo, not just reading it."
argument-hint: "<repo-name> <branch> <request>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo, the change, and the branch — its name and whether it's new or existing (ask if unclear).
2. Prepare the worktree via `codebase:worktree`; it resolves the keyword to `<owner>/<repo>` → `~/.worktree/<owner>/<repo>/<branch>/`. Use that `<owner>/<repo>` for the steps below.
3. Recall this repo's memos via `codebase:recall <owner>/<repo>`.

## Environment

- Work inside `~/.worktree/<owner>/<repo>/<branch>/`.
- `~/.codebase/` stays read-only here — it holds the local clones.

## Wrap-up

When the work is committed, record anything worth keeping via `codebase:record <owner>/<repo>`.
