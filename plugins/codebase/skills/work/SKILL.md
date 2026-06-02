---
description: "Make code changes to a GitHub repo in an isolated worktree — branch, edit, and commit under ~/.worktree/. Use when editing or contributing to a repo, not just reading it."
argument-hint: "<repo-name> <branch> <request>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo, branch (ask if not given), the change.
2. If it isn't the user's own repo, fork it first — the worktree clones the fork, and you PR back to the upstream.
3. Prepare the worktree via `codebase:worktree` → `~/.worktree/<owner>/<repo>/<branch>/`.
4. Before editing, confirm the commit author in `.bare` (`git config --show-origin user.email`): a global default → set an owner-scoped `includeIf "gitdir:~/.worktree/<owner>/"`; a conditional or local config → leave it.

## Environment

- Work inside `~/.worktree/<owner>/<repo>/<branch>/`.
- `~/.codebase/` stays read-only here — it's the research cache.
