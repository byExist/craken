<h1 align="center">codebase</h1>

<p align="center">
  어떤 GitHub 코드베이스든 조사하고 작업 — 읽기 전용으로 분석하거나, 격리된 worktree에서 브랜치를 떠 편집.
</p>

<p align="center">
  Claude Code 플러그인
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 왜 codebase인가?

현재 프로젝트가 아닌 코드로 늘 하는 두 가지: **읽기**(API 추적, 구현 비교, 버그 근본 원인 찾기)와 **고치기**(수정, 기여 프로토타이핑). codebase는 둘 다에 자리를 주되, 현재 작업 공간을 오염시키지 않습니다.

조사용 clone은 `~/.codebase/`에 받아 읽기 전용으로 둡니다. 편집은 `~/.worktree/`의 격리된 git worktree에서 일어나, 읽기와 쓰기가 충돌하지 않습니다.

## 설치

```bash
/plugin marketplace add byExist/craken
/plugin install codebase@craken
```

## 스킬

### Explore — 조사, 읽기 전용 (`~/.codebase/`)

| 스킬 | 설명 |
| --- | --- |
| `codebase:with` | repo 탐색: 구조·API·의존성·이슈 근본 원인 |
| `codebase:repo` | *(헬퍼)* 분석용 repo clone / pull / checkout |
| `codebase:clear` | 디스크 사용량 기준 조사 캐시 정리 |

### Work — 격리된 worktree에서 편집 (`~/.worktree/`)

| 스킬 | 설명 |
| --- | --- |
| `codebase:work` | 격리된 worktree에서 브랜치 생성·편집·커밋 |
| `codebase:worktree` | *(헬퍼)* bare clone + worktree 셋업 |
| `codebase:prune` | 머지된 worktree·브랜치 정리 |

## 동작 방식

```text
~/.codebase/<owner>/<repo>/          ← Explore: 읽기 전용 clone
~/.worktree/<owner>/<repo>/          ← Work: bare + worktree
├── .bare/
├── main/
└── feature/login/                   브랜치명 = 디렉토리 경로
```

조사는 최신 `main`을 읽고, 작업은 브랜치를 떠 worktree로 들어갑니다(경로가 브랜치명과 일치). 두 트리가 완전히 분리되어, 편집하는 동안에도 분석은 깨끗하게 유지됩니다.

## 라이선스

MIT.
