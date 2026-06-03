---
description: "Bare clone + worktree setup under ~/.worktree/. Referenced by the work skill to prepare an isolated working tree, separate from the read-only local clones."
user-invocable: false
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Bash(echo *)
---

# Worktree Management

Prepare a repo for editing under `~/.worktree/`.

## Existing Worktrees

!`ls -d ~/.worktree/*/* 2>/dev/null`

## gh Auth

!`gh auth status 2>&1`

## Base Path

```
~/.worktree/{owner}/{repo}/
├── .bare/          # object store (bare clone) + remote-tracking refs
├── .git            # file: "gitdir: ./.bare"
└── {branch}/       # work worktree (branch name = directory path)
```

## Workflow

### Step 1: Resolve Repo

Resolve the keyword to `<owner>/<repo>` — check the **Existing Worktrees** list above first, then `gh search repos`. Ask on multiple matches.

### Step 2: Prepare the Bare Store

If `<owner>/<repo>` is not in the list above, set up the bare layout. First check **gh Auth** above; if not authenticated, guide `gh auth login` and stop. Then **MUST ask the user before cloning**:

```bash
mkdir -p ~/.worktree/<owner>
git clone --bare <url> ~/.worktree/<owner>/<repo>/.bare
echo "gitdir: ./.bare" > ~/.worktree/<owner>/<repo>/.git
```

- `<url>`: reuse the local clone's `origin` if it exists (`git -C ~/.codebase/<owner>/<repo> remote get-url origin`), so SSH aliases carry over; otherwise gh's default.
- `git clone --bare` sets no fetch refspec — add `+refs/heads/*:refs/remotes/origin/*` and `git fetch origin` so `origin/*` exists.

### Step 3: Add a Worktree

Branch name maps directly to the directory path (e.g. `feature/login` → `feature/login/`).

```bash
cd ~/.worktree/<owner>/<repo>
git fetch origin
default=$(git -C .bare symbolic-ref --short HEAD)        # whatever .bare HEAD points to (master/main)
git worktree add <branch> -b <branch> "origin/$default"  # new branch off the default
git worktree add <branch> <branch>                       # existing remote/local branch
```

## Rules

- **Stay within `~/.worktree/`** — `~/.codebase/` holds the read-only clones, owned by `repo`/`clear`.
