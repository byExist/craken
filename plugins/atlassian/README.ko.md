<h1 align="center">atlassian</h1>

<p align="center">
  Claude에서 Jira·Confluence 다루기 — 이슈·페이지 본문을 납작해진 ADF가 아니라 구조가 살아있는 Markdown으로.
</p>

<p align="center">
  Claude Code 플러그인
</p>

<p align="center">
  <a href="README.md">English</a>
</p>

---

## 왜 atlassian인가?

Jira와 Confluence Cloud는 모든 서식 텍스트 — 이슈 설명, 댓글, 페이지 — 를 **ADF(Atlassian Document Format)**, 중첩된 JSON 트리로 저장합니다. `Fixed in **v2.1** — see PROJ-42` 같은 한 줄짜리 노트도 중첩된 `type` / `content` / `marks` 객체 더미로 부풀어서, ADF를 그대로 LLM에 건네면 실제 내용이 구조적 비계에 파묻힙니다.

흔한 우회법은 읽을 때 **ADF를 평문으로 납작하게** 만드는 것입니다 — 표·링크·헤딩·서식이 슬그머니 사라지며 — 한 방향만 제대로 다룹니다.

atlassian은 대신 모든 본문을 [marklas](https://github.com/byExist/marklas), **AST 기반 GitHub Flavored Markdown ↔ ADF 변환기**로 거쳐 구조가 왕복에서 살아남게 합니다:

- **읽기** — 본문이 표·링크·중첩 리스트·코드블록이 살아있는 충실한 **Markdown**으로 돌아옵니다. 납작한 덤프가 아닙니다.
- **쓰기** — **Markdown**으로 작성하면 marklas가 유효한 ADF로 조립합니다.

그 충실한 왕복이 atlassian의 초점입니다 — Markdown으로 읽고, Markdown으로 쓰며, 구조는 보존됩니다.

쓰기 도구(생성/수정/삭제)는 **기본 활성**입니다. 엄격한 read-only(탐색 전용) 세션이 필요하면 `/plugin config atlassian`에서 끌 수 있습니다.

## 설치

atlassian은 MCP 서버를 [uv](https://docs.astral.sh/uv/)로 실행하므로, uv가 설치되어 `PATH`에 있어야 합니다:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux — Windows는 uv 문서 참조
```

플러그인을 추가·설치합니다:

```bash
/plugin marketplace add byExist/craken
/plugin install atlassian@craken
```

그다음 Atlassian Cloud 자격 증명을 `/plugin config atlassian`에서 설정합니다:

| 설정 | 필수 | 설명 |
| --- | --- | --- |
| Atlassian site URL | ✅ | 사이트 주소, 예: `https://your-company.atlassian.net` |
| Atlassian account email | ✅ | 계정 이메일 |
| Atlassian API token | ✅ | [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens)에서 발급 — OS 키체인에 저장 |

첫 기동 시 uv가 의존성을 로컬 virtualenv에 설치합니다. **쓰기 도구는 기본 활성**이며, read-only로 사용하려면 `/plugin config atlassian`에서 끌 수 있습니다.

> **Cloud 전용.** Jira REST v3(ADF)와 Confluence v2(`atlas_doc_format`)에 의존하므로 Server / Data Center는 지원하지 않습니다.

## 도구

쓰기 도구는 기본 포함이며, read-only로 사용하려면 `/plugin config atlassian`에서 끌 수 있습니다. 본문은 양방향 모두 Markdown입니다. 주요 도구:

| Jira (`jira_*`) | Confluence (`confluence_*`) |
| --- | --- |
| `search_issues` — JQL 검색 | `search_content` — CQL 검색 |
| `get_issue` — 상세 조회 | `get_page` — 본문 조회 |
| `create_issue` | `create_page` |
| `transition_issue` — 상태 변경 | `move_page` — 트리 이동 |
| `add_comment` | `add_comment` |

그 외 보드·스프린트·에픽·워크로그·링크·필드·레이블·첨부·인라인 댓글·블로그 글·태스크 등 — 전체는 아래에.

<details>
<summary><b>전체 도구</b></summary>

**Jira** (`jira_*`)

- **Issue** — `search_issues` `get_issue` `get_changelogs` `get_transitions` `get_issue_type_metadata` `list_issue_types` `create_issue` `update_issue` `delete_issue` `assign_issue` `transition_issue`
- **Comment** — `get_comments` `add_comment` `edit_comment` `delete_comment`
- **Worklog** — `get_worklogs` `add_worklog` `update_worklog` `delete_worklog`
- **Issue link** — `get_link_types` `create_issue_link` `remove_issue_link`
- **Remote link** — `get_remote_issue_links` `create_remote_issue_link` `delete_remote_issue_link`
- **Watcher** — `get_watchers` `add_watcher` `remove_watcher`
- **Board** — `list_boards` `get_board_issues` `get_backlog_issues`
- **Sprint** — `list_sprints` `get_sprint` `get_sprint_issues` `create_sprint` `update_sprint` `delete_sprint` `move_issues_to_sprint` `move_to_backlog`
- **Epic** — `get_epic_issues` `get_epic` `link_to_epic`
- **Project** — `list_projects` `get_project` `get_project_versions` `get_project_components` `get_project_statuses` `create_version` `update_version` `delete_version`
- **Field** — `search_fields`
- **Label** — `get_labels`
- **Attachment** — `download_attachment` `upload_attachment`
- **User** — `get_current_user` `search_users`

**Confluence** (`confluence_*`)

- **Page** — `search_content` `get_page` `list_pages` `get_page_children` `get_page_descendants` `get_ancestors` `get_page_versions` `get_page_views` `get_likes` `create_page` `update_page` `delete_page` `move_page` `copy_page` `restore_page_version`
- **Blog post** — `list_blog_posts` `get_blog_post` `create_blog_post` `update_blog_post` `delete_blog_post`
- **Comment** — `get_comments` `add_comment` `edit_comment` `delete_comment` `reply_to_comment` `get_comment_replies`
- **Inline comment** — `get_inline_comments` `create_inline_comment` `resolve_inline_comment` `delete_inline_comment` `get_inline_comment_replies`
- **Label** — `get_labels` `add_label` `remove_label`
- **Attachment** — `get_attachments` `download_attachment` `upload_attachment` `delete_attachment`
- **Task** — `get_tasks` `update_task`
- **Space** — `list_spaces` `get_space`
- **User** — `get_current_user` `search_users`

</details>

## 라이선스

MIT.
