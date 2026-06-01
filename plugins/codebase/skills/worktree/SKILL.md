---
description: "Bare clone + worktree setup under ~/.worktree/. Referenced by the work skill to prepare an isolated working tree, separate from the read-only research cache."
user-invocable: false
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cat *)
---

# Worktree Management

Prepare a repo for **work** (editing) under `~/.worktree/`, separate from the read-only research cache in `~/.codebase/`.

## Existing Worktrees

!`ls -d ~/.worktree/*/* 2>/dev/null`

## gh Auth

!`gh auth status 2>&1`

## Base Path

```
~/.worktree/{owner}/{repo}/
├── .bare/          # object store (bare clone)
├── .git            # file: "gitdir: ./.bare"
├── main/           # baseline worktree
└── {branch}/       # work worktree (branch name = directory path)
```

## Workflow

### Step 1: Resolve Repo

Resolve the keyword to `<owner>/<repo>` — check the **Existing Worktrees** list above first, then `gh search repos` (as in `codebase:repo`). Ask on multiple matches.

### Step 2: Prepare the Bare Store

If `<owner>/<repo>` is not in the list above, set up the bare layout. First check **gh Auth** above; if not authenticated, guide `gh auth login` and stop. Then **MUST ask the user before cloning**:

```bash
mkdir -p ~/.worktree/<owner>
git clone --bare https://github.com/<owner>/<repo>.git ~/.worktree/<owner>/<repo>/.bare
echo "gitdir: ./.bare" > ~/.worktree/<owner>/<repo>/.git
cd ~/.worktree/<owner>/<repo>
git worktree add main
```

### Step 3: Add a Worktree

Branch name maps directly to the directory path (e.g. `feature/login` → `feature/login/`).

```bash
cd ~/.worktree/<owner>/<repo>
git fetch origin
git worktree add <branch> -b <branch> origin/main   # new branch off main
git worktree add <branch> <branch>                   # existing remote/local branch
```

## Rules

- **Never touch `~/.codebase/`** — that is the research cache, managed by `repo`/`clear`.
