<h1 align="center">Voice</h1>

<p align="center">
  나만의 응답 페르소나를 정의하고 전환 — 프리셋 없이, 직접 만든 목소리로.
</p>

<p align="center">
  Claude Code 플러그인
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 왜 voice인가?

Claude의 기본 응답 방식은 하나지만, 원하는 목소리는 작업마다 달라집니다 — 빠른 확인엔 결론부터 간결하게, 무언가를 따져볼 땐 소크라테스식으로, 변경을 저울질할 땐 신중한 리뷰어처럼. voice는 그 각각을 **페르소나**로 담아 전환하게 해줍니다.

정해진 프리셋 메뉴를 주는 대신, voice는 저작 도구를 건넵니다: Claude가 어떻게 생각하고 답하길 원하는지 설명하면 `/voice:new`가 그걸 재사용 가능한 페르소나로 적어둡니다. 고른 voice는 세션을 재개할 때 자동으로 복원됩니다.

## 설치

```bash
/plugin marketplace add byExist/craken
/plugin install voice@craken
```

선택적으로 `/plugin config voice`에서 기본 voice를 지정할 수 있습니다 — `/voice:use`로 voice를 고르지 않은 세션(새 세션 포함)이 시작할 때 불러옵니다:

| 설정 | 필수 | 설명 |
| --- | --- | --- |
| default | | 저장된 페르소나 이름(`/voice:list` 참고). 비우면 없습니다. |

## 스킬

| 스킬 | 설명 |
| --- | --- |
| `/voice:new` | 짧은 질답으로 새 페르소나를 정의하고 저장 |
| `/voice:use <name>` | 저장된 페르소나를 세션 동안 활성화 |
| `/voice:list` | 저장된 페르소나 목록과 활성 페르소나 표시 |
| `/voice:reset` | 활성 voice 해제, 기본 스타일로 복귀 |
| `/voice:remove <name>` | 저장된 페르소나 삭제 |

## 동작 방식

```text
~/.claude/plugins/data/voice-craken/
├── personas/
│   ├── terse.md            ← /voice:new로 저작됨
│   └── reviewer.md
└── state/
    └── <session-id>        ← 그 세션의 활성 페르소나
```

`/voice:new`가 질답으로 페르소나 파일을 적습니다. `/voice:use`는 현재 세션의 선택을 기록하고 그 목소리를 채택합니다. SessionStart hook이 세션이 시작·재개될 때마다 그 선택을 읽어 페르소나를 context로 복원하므로, 목소리가 재시작을 견딥니다. 선택이 세션 ID로 구분되기에 서로 다른 세션이 동시에 다른 목소리를 쓸 수 있습니다. `/voice:reset`은 선택을 해제하며, 지정된 기본 voice가 있으면 그쪽으로 되돌아갑니다.
