---
description: "Work with any GitHub codebase. Explore project structure, find APIs, trace dependencies, and analyze issue root causes."
argument-hint: "<repo-name(s)> <request>"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## User Request

$ARGUMENTS

## Workflow

### Step 1: Parse Request

Identify from the user request:

- Related repo name(s) (one or more)
- Task type (structure exploration, API search, dependency tracing, issue analysis, etc.)

### Step 2: Prepare Code

Follow the `codebase:repo` skill instructions to prepare repos under `~/.codebase/<owner>/<repo>/`.
If the user mentions a specific branch, use it as the target branch when following the checkout step.

### Step 3: Analyze

Analyze the prepared code to answer the user's request.
Use Grep and Glob to locate relevant files before reading.

### Step 4: Report Results

- Cite file paths and line numbers as evidence
- Present results in a structured format
- For multi-repo results, organize by repo
