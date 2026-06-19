---
description: "Make code changes to a GitHub repo in an isolated worktree."
argument-hint: "<repo-name> <branch> <request>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo, the change, and the branch — its name and whether it's new or existing (ask if unclear).
2. Prepare the worktree via `codebase:worktree`.
3. Recall this repo's memos via `codebase:recall <owner>/<repo>`.

## Environment

- Work inside `~/.worktree/<owner>/<repo>/<branch>/`.
- `~/.codebase/` stays read-only here — it holds the local clones.

## Wrap-up

When the work is committed, review the implementation. If there is environment or tooling friction that could recur in future work — and is not already in the memos — present it briefly and ask the user whether to record it. If they agree, call `codebase:record <owner>/<repo>`.
