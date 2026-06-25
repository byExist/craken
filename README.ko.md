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

### 내장

| Plugin | Description |
| --- | --- |
| [codebase](plugins/codebase/README.ko.md) | GitHub 코드베이스를 읽기 전용으로 조사하거나 격리된 worktree에서 편집 |
| [voice](plugins/voice/README.ko.md) | `/voice:new`와 `/voice:use`로 나만의 응답 페르소나를 정의·전환하고 세션마다 복원 |

### 연동

| Plugin | Description |
| --- | --- |
| [atlassian](https://github.com/byExist/craken-atlassian) | Jira·Confluence 본문을 납작한 ADF 대신 충실한 Markdown으로 읽고 씀 |
| [slack](https://github.com/byExist/craken-slack) | Slack 채널·스레드·메시지·사용자를 공식 SDK로 읽고 검색 |
| [datadog](https://github.com/byExist/craken-datadog) | Datadog 로그·APM 트레이스·메트릭·모니터·인시던트를 읽기 전용으로 조회 |
