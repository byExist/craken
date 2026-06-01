---
description: "GitHub repo clone/pull/checkout management. Referenced by the with skill when preparing code locally."
user-invocable: false
allowed-tools: Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *)
---

# Repo Management

Prepare code under `~/.codebase/`.

## Base Path

```
~/.codebase/{owner}/{repo}/
```

## Resolve Repo

Resolve the user's keyword to a target repo.

**Step 1 — Local search**

```bash
ls -d ~/.codebase/*/<keyword> 2>/dev/null
```

- Single match → use it
- Multiple matches → ask the user to choose via AskUserQuestion

**Step 2 — GitHub search (if not found locally)**

```bash
gh search repos "<keyword>" --json fullName,description,language,isArchived --limit 10
```

- Exclude repos where `isArchived: true`
- Single result → proceed directly
- Multiple results → ask the user to choose via AskUserQuestion
- **No results** → ask the user for an alternative keyword

## Check Local Existence

```bash
ls ~/.codebase/<owner>/<repo>
```

- Exists → go to **Checkout & Pull**
- Does not exist → go to **Clone**

## Clone

**MUST ask the user for confirmation before cloning.**

```bash
mkdir -p ~/.codebase/<owner>
gh repo clone <owner>/<repo> ~/.codebase/<owner>/<repo>
```

After clone, proceed to the checkout step below.

## Checkout & Pull

This step runs for both newly cloned and existing repos.

**Branch specified:**

```bash
cd ~/.codebase/<owner>/<repo>
git fetch --prune
git branch -r | grep <keyword>
```

- Single match → `git checkout <branch> && git pull`
- Multiple matches → ask the user to choose via AskUserQuestion
- No match → ask the user for an alternative branch name

**No branch specified (default):**

```bash
cd ~/.codebase/<owner>/<repo>
git checkout main 2>/dev/null || git checkout master
git pull
```

## Rules

- **MUST** ask the user via AskUserQuestion before clone
- Pull may proceed without confirmation
- Create `~/.codebase/` automatically if it does not exist
