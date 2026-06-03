<h1 align="center">voice</h1>

<p align="center">
  Define your own response personas and switch between them — no presets, just the voices you make.
</p>

<p align="center">
  A Claude Code plugin
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why voice?

Claude has one default way of responding, but the voice you want shifts with the task — conclusion-first and terse for a quick check, Socratic when you're thinking something through, a careful reviewer when weighing a change. voice lets you capture each of those as a **persona** and switch between them.

Instead of shipping a fixed menu of presets, voice hands you the authoring tool: describe how you want Claude to think and respond, and `/voice:new` writes it into a reusable persona. Your personas persist across sessions and restore automatically.

## Installation

```bash
/plugin marketplace add byExist/craken
/plugin install voice@craken
```

## Skills

| Skill | What it does |
| --- | --- |
| `/voice:new` | Define a new persona through a short Q&A, then save it |
| `/voice:use <name>` | Activate a saved persona for the rest of the session |
| `/voice:list` | List saved personas and show which one is active |
| `/voice:reset` | Clear the active voice and revert to the default style |
| `/voice:remove <name>` | Delete a saved persona |

## How it works

```text
~/.claude/plugins/data/voice-craken/
├── personas/
│   ├── terse.md            ← authored by /voice:new
│   └── reviewer.md
└── state/
    └── <session-id>        ← active persona for that session
```

`/voice:new` interviews you and writes a persona file. `/voice:use` records your choice for the current session and adopts that voice. A SessionStart hook reads that choice whenever a session starts or resumes and restores the persona as context — so the voice survives restarts. Because the choice is keyed by session ID, different sessions can run different voices at once, and `/voice:reset` clears it.
