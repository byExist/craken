<h1 align="center">Meta</h1>

<p align="center">
  Claude Code 자체를 만드는 전문가 스킬 모음 — skill, agent, hook, MCP 서버, rule, plugin, marketplace를 스펙에 맞게 작성하고 리뷰합니다.
</p>

<p align="center">
  Claude Code 플러그인
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 왜 meta인가?

Claude Code의 모든 구성 요소에는 각자의 포맷과 규칙이 있습니다 — `SKILL.md` frontmatter, 에이전트 정의, 훅 이벤트 매처, `.mcp.json`, 마켓플레이스 카탈로그. 기억에 의존해 정확히 작성하기는 까다롭고, 스펙은 계속 바뀝니다.

meta는 아티팩트마다 전문가 하나씩을 묶어 둡니다. Claude에게 생성이나 리뷰를 요청하면 해당 스킬이 현재 스펙으로 작동해서, 추측이 아니라 구조적으로 올바른 결과가 나옵니다.

## 설치

```bash
/plugin marketplace add byExist/craken
/plugin install meta@craken
```

## 스킬

**작성 전문가** — 한 가지 아티팩트 유형을 스펙에 맞게 생성·리뷰:

| 스킬 | 아티팩트 |
| --- | --- |
| `meta:skill` | 스킬 정의 (`SKILL.md`) |
| `meta:agent` | 작업 위임용 서브에이전트 |
| `meta:hook` | settings 파일의 훅 |
| `meta:mcp` | MCP 서버 (`.mcp.json`), 커스텀 서버, 연결 디버깅 |
| `meta:rule` | `.claude/rules/`의 모듈형 규칙 |
| `meta:plugin` | 플러그인 패키지 |
| `meta:marketplace` | 마켓플레이스 카탈로그 (`marketplace.json`) |

**워크플로:**

| 스킬 | 설명 |
| --- | --- |
| `meta:review` | 위 전문가 중 적절한 곳으로 디스패치해 하니스 아티팩트를 리뷰 |
| `meta:upgrade` | 전문가 스킬을 최신 Claude Code 스펙에 맞게 갱신 |

## 사용법

전문가 스킬은 의도로 작동합니다 — 평범한 말로 요청하면 해당 스킬이 로드됩니다:

```
"PR 요약하는 스킬 만들어줘"        → meta:skill
"이 에이전트 정의 리뷰해줘"        → meta:agent
"우리 API용 MCP 서버 설정해줘"     → meta:mcp
```

`meta:review`는 가리킨 아티팩트에 맞는 전문가를 골라주고, `meta:upgrade`는 모든 전문가를 published 스펙에 맞춰 최신으로 유지합니다.

## 라이선스

MIT.
