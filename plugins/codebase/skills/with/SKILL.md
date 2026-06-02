---
description: "Work with any GitHub codebase. Explore project structure, find APIs, trace dependencies, and analyze issue root causes."
argument-hint: "<repo-name(s)> <request>"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo name(s), and a branch if one is named.
2. Prepare each repo under `~/.codebase/<owner>/<repo>/` via `codebase:repo` (use the named branch when checking out).

## Environment

- Prepared repos live read-only in `~/.codebase/<owner>/<repo>/` — explore freely, but never edit here (use `codebase:work` to change code).
