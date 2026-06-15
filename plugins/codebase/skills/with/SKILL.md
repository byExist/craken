---
description: "Explore and understand any GitHub codebase read-only: project structure, APIs, dependency traces, and issue root causes. Use when reading or investigating a repo without editing it."
argument-hint: "<repo-name(s)> <request>"
allowed-tools: Read, Grep, Glob, Bash(gh *), Bash(git *), Bash(ls *), Bash(mkdir *), Bash(cd *), Task
---

## Setup

1. Parse the request: target repo name(s), and a branch if one is named.
2. Prepare each repo via `codebase:repo`.
3. Recall each repo's memos via `codebase:recall <owner>/<repo>`.

## Environment

- Local clones live read-only in `~/.codebase/<owner>/<repo>/` — explore freely; to change code, switch to `codebase:work`.

## Wrap-up

When the exploration is done, review what was discovered. If there is information that remains valid the next time this repo is opened — not one-off context for this task alone — present it briefly and ask the user whether to record it. If they agree, call `codebase:record <owner>/<repo>`.
