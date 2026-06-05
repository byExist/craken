<h1 align="center">Codebase</h1>

<p align="center">
  Explore and work on any GitHub codebase — research it read-only, or branch and edit it in isolated worktrees.
</p>

<p align="center">
  A Claude Code plugin
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why codebase?

Two things you constantly do with code that isn't your current project: **read it** (trace an API, compare implementations, find a bug's root cause) and **change it** (fix something, prototype a contribution). codebase gives both a home without polluting your current workspace.

Research clones land in `~/.codebase/` and stay read-only. Edits happen in isolated git worktrees under `~/.worktree/`, so reading and writing never collide.

## Installation

```bash
/plugin marketplace add byExist/craken
/plugin install codebase@craken
```

## Skills

### Explore — research, read-only (`~/.codebase/`)

| Skill | What it does |
| --- | --- |
| `codebase:with` | Explore a repo: structure, APIs, dependencies, issue root causes |
| `codebase:repo` | *(helper)* clone / pull / checkout a repo for analysis |
| `codebase:memo` | *(helper)* recall/record what reading the repo doesn't surface |
| `codebase:clear` | Clean up the research cache by disk usage |

### Work — edit in isolated worktrees (`~/.worktree/`)

| Skill | What it does |
| --- | --- |
| `codebase:work` | Branch, edit, and commit a repo in an isolated worktree |
| `codebase:worktree` | *(helper)* set up a bare clone + worktree |
| `codebase:notes` | *(helper)* recall/record what it takes to work the repo |
| `codebase:prune` | Remove merged worktrees and branches |

## How it works

```text
~/.codebase/<owner>/<repo>/          ← Explore: read-only clone
~/.worktree/<owner>/<repo>/          ← Work: bare + worktrees
├── .bare/
├── main/
└── feature/login/                   branch name = directory path
```

Exploring reads the latest `main`; working branches off into a worktree whose path mirrors the branch name. The two trees stay fully separate, so analysis stays clean while you edit.

Alongside, each repo accrues **memo** (read-side) and **notes** (work-side) in the plugin's data dir, keyed by `<owner>/<repo>` — recalled automatically on later visits so the same context isn't re-derived.
