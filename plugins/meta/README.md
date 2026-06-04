<h1 align="center">Meta</h1>

<p align="center">
  Expert skills for building Claude Code itself — author and review skills, agents, hooks, MCP servers, rules, plugins, and marketplaces, to spec.
</p>

<p align="center">
  A Claude Code plugin
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why meta?

Every Claude Code building block has its own format and rules — a `SKILL.md` frontmatter, an agent definition, a hook event matcher, an `.mcp.json`, a marketplace catalog. Getting them right from memory is error-prone, and the spec keeps moving.

meta bundles one expert per artifact. Ask Claude to create or review any of them and the matching skill kicks in with the current spec — so the result is correct by construction, not by guesswork.

## Installation

```bash
/plugin marketplace add byExist/craken
/plugin install meta@craken
```

## Skills

**Authoring experts** — create or review one artifact type, to spec:

| Skill | Artifact |
| --- | --- |
| `meta:skill` | Skill definitions (`SKILL.md`) |
| `meta:agent` | Sub-agents for task delegation |
| `meta:hook` | Hooks in settings files |
| `meta:mcp` | MCP servers (`.mcp.json`), custom servers, connection debugging |
| `meta:rule` | Modular rules in `.claude/rules/` |
| `meta:plugin` | Plugin packages |
| `meta:marketplace` | Marketplace catalogs (`marketplace.json`) |

**Workflow:**

| Skill | What it does |
| --- | --- |
| `meta:review` | Reviews a harness artifact by dispatching to the right expert above |
| `meta:upgrade` | Refreshes the experts so their guidance tracks the latest Claude Code spec |

## Usage

The experts trigger on intent — ask in plain language and the matching skill loads:

```
"Create a skill that summarizes PRs"   → meta:skill
"Review this agent definition"         → meta:agent
"Set up an MCP server for our API"     → meta:mcp
```

`meta:review` picks the right expert for whatever artifact you point it at; `meta:upgrade` keeps them all current with the published spec.

## License

MIT.
