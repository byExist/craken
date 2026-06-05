<h1 align="center">Atlassian</h1>

<p align="center">
  Jira & Confluence in Claude — issue and page bodies as faithful Markdown, not flattened ADF.
</p>

<p align="center">
  A Claude Code plugin
</p>

<p align="center">
  <a href="README.ko.md">한국어</a>
</p>

---

## Why atlassian?

Jira and Confluence Cloud keep every rich-text field — issue descriptions, comments, pages — as **ADF (Atlassian Document Format)**, a nested JSON tree. A one-line note like `Fixed in **v2.1** — see PROJ-42` already expands into a stack of nested `type` / `content` / `marks` objects, so handing ADF straight to an LLM buries the real content under structural scaffolding.

The usual workaround is to **flatten ADF to plain text** on read — which quietly drops tables, links, headings, and formatting — and to handle just one direction well.

atlassian instead routes every body through [marklas](https://github.com/byExist/marklas), an **AST-based GitHub-Flavored-Markdown ↔ ADF converter**, so structure survives the round trip:

- **Read** — bodies arrive as faithful **Markdown**, with tables, links, nested lists, and code blocks intact — not a flattened dump.
- **Write** — you author **Markdown**, and marklas assembles valid ADF.

That faithful round trip is atlassian's focus — Markdown in, Markdown out, structure preserved.

Write tools (create / update / delete) are **off by default** — only read tools are exposed, so a fresh session is strictly read-only.

## Installation

atlassian runs its MCP server through [uv](https://docs.astral.sh/uv/), so uv must be installed and on your `PATH`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux — see the uv docs for Windows
```

Add and install the plugin:

```bash
/plugin marketplace add byExist/craken
/plugin install atlassian@craken
```

atlassian installs **disabled** by default. Enable it from `/plugin`, which prompts for your Atlassian Cloud credentials — or set them anytime with `/plugin config atlassian`:

| Setting | Required | Description |
| --- | --- | --- |
| Atlassian site URL | ✅ | Your site, e.g. `https://your-company.atlassian.net` |
| Atlassian account email | ✅ | Account email |
| Atlassian API token | ✅ | Create one at [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens) — stored in your OS keychain |

On first launch, uv provisions the dependencies into a local virtualenv. **Write tools are off by default** — turn them on with `/plugin config atlassian` when you need to write.

> **Cloud only.** Built on Jira REST v3 (ADF) and Confluence v2 (`atlas_doc_format`), so Server / Data Center isn't supported.

## Tools

Highlights:

| Jira (`jira_*`) | Confluence (`confluence_*`) |
| --- | --- |
| `search_issues` — search by JQL | `search_content` — search by CQL |
| `get_issue` — full detail | `get_page` — full body |
| `create_issue` | `create_page` |
| `transition_issue` — change status | `move_page` — move in tree |
| `add_comment` | `add_comment` |

Plus boards, sprints, epics, worklogs, links, fields, labels, attachments, inline comments, blog posts, and tasks — full list below.

<details>
<summary><b>All tools</b></summary>

**Jira** (`jira_*`)

- **Issue** — `search_issues` `get_issue` `get_changelogs` `get_transitions` `get_issue_type_metadata` `list_issue_types` `create_issue` `update_issue` `change_issue_type` `delete_issue` `assign_issue` `transition_issue`
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

## License

MIT.
