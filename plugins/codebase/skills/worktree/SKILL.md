---
description: "Bare clone + worktree setup under ~/.worktree/. Referenced by the work skill to prepare an isolated working tree, separate from the read-only research cache."
user-invocable: false
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cat *)
---

# Worktree Management

Prepare a repo for **work** (editing) under `~/.worktree/`, kept separate from the read-only research cache in `~/.codebase/`.

## Base Path

```
~/.worktree/{owner}/{repo}/
├── .bare/          # object store (bare clone)
├── .git            # file: "gitdir: ./.bare"
├── main/           # baseline worktree
└── {branch}/       # work worktree (branch name = directory path)
```

## Resolve Repo

Resolve the user's keyword to `<owner>/<repo>` the same way `codebase:repo` does (local `~/.worktree/*` lookup first, then `gh search repos`). Ask via AskUserQuestion on multiple matches.

## Prepare the Bare Store

```bash
ls ~/.worktree/<owner>/<repo>/.bare 2>/dev/null
```

- Exists → go to **Add a Worktree**
- Missing → set up the bare layout below

**MUST ask the user for confirmation before the initial clone.**

```bash
mkdir -p ~/.worktree/<owner>
git clone --bare https://github.com/<owner>/<repo>.git ~/.worktree/<owner>/<repo>/.bare
echo "gitdir: ./.bare" > ~/.worktree/<owner>/<repo>/.git
cd ~/.worktree/<owner>/<repo>
git worktree add main
```

## Add a Worktree

Branch name maps directly to the directory path (e.g. `feature/login` → `feature/login/`).

```bash
cd ~/.worktree/<owner>/<repo>
git fetch origin

# new branch off main:
git worktree add <branch> -b <branch> origin/main
# existing remote/local branch:
git worktree add <branch> <branch>
```

## Rules

- **MUST** ask the user before the initial bare clone.
- Branch name = worktree directory path; do not flatten slashes.
- Keep `main` and `.bare` intact.
- **Never touch `~/.codebase/`** — that is the research cache, managed by `repo`/`clear`.
