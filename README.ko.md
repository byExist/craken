<h1 align="center">Craken</h1>

<p align="center">
  <b>C</b>laude code + K<b>raken</b> — 촉수처럼 플러그인을 오케스트레이션하는 마켓플레이스.
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 설치

```bash
/plugin marketplace add byExist/craken
```

## 플러그인

| Plugin | Description |
| --- | --- |
| [meta](plugins/meta/README.ko.md) | Claude Code 자체 구성 요소(skill·agent·hook·MCP 등)를 작성·리뷰 |
| [codebase](plugins/codebase/README.ko.md) | 어떤 GitHub 코드베이스든 조사·작업 — 읽기 전용 분석 또는 격리 worktree 편집 |
| [voice](plugins/voice/README.ko.md) | 나만의 응답 페르소나를 직접 정의 — `/voice:new`로 만들고 `/voice:use`로 전환, 세션마다 복원 |
| [atlassian](https://github.com/byExist/craken-atlassian) | Claude에서 Jira·Confluence — 이슈·페이지 본문을 납작한 ADF가 아니라 충실한 Markdown으로 |
