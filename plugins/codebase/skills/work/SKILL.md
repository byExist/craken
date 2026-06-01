---
description: "Make code changes to a GitHub repo in an isolated worktree — branch, edit, and commit under ~/.worktree/. Use when editing or contributing to a repo, not just reading it."
argument-hint: "<repo-name> <branch> <request>"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## User Request

$ARGUMENTS

## Workflow

### Step 1: Parse Request

Identify from the user request:

- Target repo (one)
- Branch name for the work (ask if not given)
- The change to make

### Step 2: Prepare Worktree

Follow the `codebase:worktree` skill to set up the bare store and add a worktree for `<branch>` under `~/.worktree/<owner>/<repo>/<branch>/`.

### Step 3: Make Changes

Work **inside the worktree directory**. Use Grep/Glob to locate code, Read to inspect, then Edit/Write to apply changes. Keep edits scoped to the request.

### Step 4: Commit

Summarize the diff, then commit in the worktree:

```bash
cd ~/.worktree/<owner>/<repo>/<branch>
git add -A
git commit -m "<message>"
```

### Step 5: Push (optional)

**MUST ask the user before pushing.** Pushing to a repo you do not own needs a fork + PR flow instead.

```bash
git push -u origin <branch>
```

## Rules

- All edits happen under `~/.worktree/` — **never edit the `~/.codebase/` research cache**.
- One worktree per branch; reuse it if it already exists.
- **MUST** ask before pushing; commit locally is fine without asking.
- Cite file paths when reporting what changed.
