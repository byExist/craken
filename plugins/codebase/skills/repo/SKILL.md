---
description: "GitHub repo clone/pull/checkout management. Referenced by the with skill when preparing code locally."
user-invocable: false
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *)
---

# Repo Management

Prepare code under `~/.codebase/`.

## Local Cache

!`ls -d ~/.codebase/*/* 2>/dev/null`

## gh Auth

!`gh auth status 2>&1`

## Base Path

```
~/.codebase/{owner}/{repo}/
```

## Workflow

### Step 1: Resolve Repo

Resolve the user's keyword to a target repo.

1. **Local first** — match against the **Local Cache** list above. Single match → use it; multiple → ask via AskUserQuestion.
2. **GitHub search** (only if not cached) — first check **gh Auth** above; if not authenticated, guide the user to run `gh auth login` and stop. Then:

   ```bash
   gh search repos "<keyword>" --json fullName,description,language,isArchived --limit 10
   ```

   Exclude `isArchived: true`; single result → proceed; multiple → ask; none → ask for another keyword.

### Step 2: Clone or Checkout & Pull

If the repo is in the Local Cache, check it out and pull. Otherwise clone it first (**MUST ask the user before cloning**; gh Auth above must be authenticated):

```bash
mkdir -p ~/.codebase/<owner>
gh repo clone <owner>/<repo> ~/.codebase/<owner>/<repo>
```

Then check out the branch the user named, or the default branch (main/master) if none, and pull.
