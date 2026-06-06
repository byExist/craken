"""JIRA MCP tools — pure functions, registered by server.py."""

from marklas import to_adf, to_md

from atlassian.jira import client
from atlassian.jira.schema.attachment import Attachment
from atlassian.jira.schema.board import PageBeanBoard
from atlassian.jira.schema.changelog import PageBeanChangelog
from atlassian.jira.schema.comment import PageOfComments
from atlassian.jira.schema.common import IssueTypeDetails, IssueTypeWithStatus
from atlassian.jira.schema.component import Component
from atlassian.jira.schema.epic import Epic
from atlassian.jira.schema.field import PageBeanField
from atlassian.jira.schema.issue import (
    CreatedIssue,
    IssueBean,
    SearchAndReconcileResults,
    SearchResults,
)
from atlassian.jira.schema.issue_type_meta import PageOfCreateMetaIssueTypes
from atlassian.jira.schema.label import PageBeanLabel
from atlassian.jira.schema.link_type import IssueLinkTypes
from atlassian.jira.schema.project import PageBeanProject, Project
from atlassian.jira.schema.remote_link import RemoteIssueLink
from atlassian.jira.schema.sprint import SprintBean, SprintPage
from atlassian.jira.schema.transition import Transitions
from atlassian.jira.schema.user import User
from atlassian.jira.schema.version import PageBeanVersion
from atlassian.jira.schema.watcher import Watchers
from atlassian.jira.schema.worklog import PageOfWorklogs
from atlassian.files import read_body, read_bytes, write_body, write_temp


# --- User ---


def get_current_user() -> User:
    """Get the currently authenticated user."""
    return client.get_current_user()


def search_users(query: str, limit: int = 50) -> list[User]:
    """Search for users by name or email."""
    return client.search_users(query, max_results=limit)


# --- Project ---


def list_projects(
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanProject:
    """List JIRA projects. Use get_project instead if you already know the project key."""
    return client.list_projects(start_at=start_at, max_results=limit)


def get_project(project_key: str) -> Project:
    """Get details of a specific project."""
    return client.get_project(project_key)


def get_project_versions(
    project_key: str,
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanVersion:
    """Get versions (releases) of a project."""
    return client.get_project_versions(
        project_key, start_at=start_at, max_results=limit
    )


def get_project_components(project_key: str) -> list[Component]:
    """Get components of a project."""
    return client.get_project_components(project_key)


def get_project_statuses(project_key: str) -> list[IssueTypeWithStatus]:
    """Get the statuses available per issue type in a project. Useful for finding JQL status values."""
    return client.get_project_statuses(project_key)


# --- Issue ---


def search_issues(
    jql: str,
    limit: int = 50,
    next_page_token: str | None = None,
) -> SearchAndReconcileResults:
    """Search JIRA issues using JQL query. Description is not included; use get_issue for full detail."""
    result = client.search_issues(
        jql, max_results=limit, next_page_token=next_page_token
    )
    for issue in result.issues:
        if issue.fields:
            issue.fields.description = None
    return result


def get_issue(
    issue_key: str,
    plain: bool = True,
    to_file: str | None = None,
) -> IssueBean:
    """Get details of a specific JIRA issue. Description is Markdown. Set plain=false to preserve ADF-only features for editing.

    Pass to_file (absolute path) to write the description to that file and omit it
    from the response — edit the file, then publish with update_issue(from_file=...).
    """
    issue = client.get_issue(issue_key)
    if issue.fields and isinstance(issue.fields.description, dict):
        issue.fields.description = to_md(issue.fields.description, plain=plain)
    if (
        to_file is not None
        and issue.fields
        and isinstance(issue.fields.description, str)
    ):
        write_body(to_file, issue.fields.description)
        issue.fields.description = None
    return issue


def create_issue(
    project_key: str,
    summary: str,
    issue_type: str = "Task",
    description: str | None = None,
    assignee: str | None = None,
    from_file: str | None = None,
) -> CreatedIssue:
    """Create a new JIRA issue. Description is Markdown, or pass from_file to read it from a local file (not both)."""
    if description and from_file:
        raise ValueError("provide either description or from_file, not both")
    if from_file is not None:
        description = read_body(from_file)
    return client.create_issue(
        project_key,
        summary,
        issue_type=issue_type,
        description=to_adf(description) if description else None,
        assignee=assignee,
    )


def update_issue(
    issue_key: str,
    summary: str | None = None,
    description: str | None = None,
    from_file: str | None = None,
) -> str:
    """Update an existing JIRA issue. Description is Markdown, or pass from_file to read it from a local file (not both)."""
    if description and from_file:
        raise ValueError("provide either description or from_file, not both")
    if from_file is not None:
        description = read_body(from_file)
    client.update_issue(
        issue_key,
        summary=summary,
        description=to_adf(description) if description else None,
    )
    return "OK"


def change_issue_type(
    issue_key: str,
    issue_type: str,
    parent: str | None = None,
) -> str:
    """Change an issue's type. Moving down a level (e.g. to a subtask) requires parent; moving up detaches the existing parent. Jumps across two levels and demoting an issue that has children are not supported."""
    current = client.get_issue(issue_key)
    cur = current.fields.issue_type if current.fields else None
    if cur is None or cur.name is None or cur.hierarchy_level is None:
        raise ValueError(f"cannot determine the current type of {issue_key}")
    if cur.name == issue_type:
        return f"already '{issue_type}'; no change"

    target = next((t for t in client.list_issue_types() if t.name == issue_type), None)
    if target is None:
        raise ValueError(
            f"unknown issue type '{issue_type}'; use list_issue_types to see valid names"
        )
    if target.hierarchy_level is None:
        raise ValueError(f"cannot determine the hierarchy level of '{issue_type}'")

    diff = target.hierarchy_level - cur.hierarchy_level
    if abs(diff) >= 2:
        raise ValueError(
            f"cannot change '{cur.name}' to '{issue_type}' across multiple hierarchy levels"
        )
    if diff < 0:
        if parent is None:
            raise ValueError(
                f"changing '{cur.name}' to '{issue_type}' moves it down a level and "
                "requires parent (the key of the issue one level up)"
            )
        client.change_issue_type(issue_key, issue_type=issue_type, parent_key=parent)
    elif diff > 0:
        if parent is not None:
            raise ValueError(
                f"changing to '{issue_type}' moves it up a level and takes no parent "
                "(the existing parent is removed)"
            )
        client.change_issue_type(issue_key, issue_type=issue_type, clear_parent=True)
    else:
        if parent is not None:
            raise ValueError(
                f"changing to '{issue_type}' stays at the same level and takes no parent"
            )
        client.change_issue_type(issue_key, issue_type=issue_type)
    return "OK"


def assign_issue(issue_key: str, assignee: str | None = None) -> str:
    """Assign an issue to a user, or unassign if assignee is null."""
    client.assign_issue(issue_key, assignee)
    return "OK"


def delete_issue(issue_key: str) -> str:
    """Delete a JIRA issue."""
    client.delete_issue(issue_key)
    return "OK"


def get_changelogs(
    issue_key: str,
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanChangelog:
    """Get the changelog (field change history) of an issue."""
    return client.get_changelogs(issue_key, start_at=start_at, max_results=limit)


def get_issue_type_metadata(
    project_key: str,
    start_at: int = 0,
    limit: int = 50,
) -> PageOfCreateMetaIssueTypes:
    """Get available issue types for creating issues in a project."""
    return client.get_issue_type_metadata(
        project_key, start_at=start_at, max_results=limit
    )


def list_issue_types() -> list[IssueTypeDetails]:
    """List all issue types available to the user (Bug, Task, Story, etc.).

    Use get_issue_type_metadata for what's creatable in a specific project.
    """
    return client.list_issue_types()


def download_attachment(attachment_id: str) -> str:
    """Download an attachment to a temp file; returns the saved path.

    The file lands in the OS temp dir with a type-appropriate extension and
    never passes through the model's context. Copy it elsewhere to keep it.
    """
    data, content_type = client.get_attachment_content(attachment_id)
    return write_temp(data, content_type)


def upload_attachment(issue_key: str, file_path: str) -> list[Attachment]:
    """Attach a local file to an issue. Pass an absolute path."""
    data, filename = read_bytes(file_path)
    return client.add_attachment(issue_key, data, filename)


# --- Transition ---


def get_transitions(
    issue_key: str,
) -> Transitions:
    """Get available status transitions for an issue."""
    return client.get_transitions(issue_key)


def transition_issue(issue_key: str, transition_id: str) -> str:
    """Transition an issue to a new status."""
    client.transition_issue(issue_key, transition_id)
    return "OK"


# --- Comment ---


def get_comments(
    issue_key: str,
    start_at: int = 0,
    limit: int = 50,
    plain: bool = True,
) -> PageOfComments:
    """Get comments on an issue. Body is Markdown. Set plain=false to preserve ADF-only features for editing."""
    result = client.get_comments(issue_key, start_at=start_at, max_results=limit)
    for comment in result.comments:
        if isinstance(comment.body, dict):
            comment.body = to_md(comment.body, plain=plain)
    return result


def add_comment(issue_key: str, body: str) -> str:
    """Add a comment to an issue. Body is Markdown."""
    client.add_comment(issue_key, body=to_adf(body))
    return "OK"


def edit_comment(issue_key: str, comment_id: str, body: str) -> str:
    """Edit an existing comment. Body is Markdown."""
    client.update_comment(issue_key, comment_id, body=to_adf(body))
    return "OK"


def delete_comment(issue_key: str, comment_id: str) -> str:
    """Delete a comment from an issue."""
    client.delete_comment(issue_key, comment_id)
    return "OK"


# --- Link ---


def get_link_types() -> IssueLinkTypes:
    """Get available issue link types."""
    return client.get_link_types()


def create_issue_link(
    link_type: str,
    inward_issue_key: str,
    outward_issue_key: str,
) -> str:
    """Create a link between two issues."""
    client.create_issue_link(link_type, inward_issue_key, outward_issue_key)
    return "OK"


def remove_issue_link(link_id: str) -> str:
    """Remove a link between two issues."""
    client.delete_issue_link(link_id)
    return "OK"


# --- Remote Link ---


def get_remote_issue_links(issue_key: str) -> list[RemoteIssueLink]:
    """Get remote links (e.g. GitHub PRs, Confluence pages) on an issue."""
    return client.get_remote_issue_links(issue_key)


def create_remote_issue_link(
    issue_key: str,
    url: str,
    title: str,
    relationship: str | None = None,
) -> str:
    """Create a remote link on an issue."""
    client.create_remote_issue_link(
        issue_key,
        url=url,
        title=title,
        relationship=relationship,
    )
    return "OK"


def delete_remote_issue_link(issue_key: str, link_id: str) -> str:
    """Delete a remote link from an issue."""
    client.delete_remote_issue_link(issue_key, link_id)
    return "OK"


# --- Watcher ---


def get_watchers(issue_key: str) -> Watchers:
    """Get watchers of an issue."""
    return client.get_watchers(issue_key)


def add_watcher(issue_key: str, account_id: str) -> str:
    """Add a watcher to an issue."""
    client.add_watcher(issue_key, account_id)
    return "OK"


def remove_watcher(issue_key: str, account_id: str) -> str:
    """Remove a watcher from an issue."""
    client.remove_watcher(issue_key, account_id)
    return "OK"


# --- Field ---


def search_fields(
    query: str | None = None,
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanField:
    """Search JIRA fields (system and custom). Useful for finding field IDs for JQL."""
    return client.search_fields(query=query, start_at=start_at, max_results=limit)


def get_labels(
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanLabel:
    """Get all labels used across JIRA issues."""
    return client.get_labels(start_at=start_at, max_results=limit)


# --- Board ---


def list_boards(
    project_key: str | None = None,
    board_type: str | None = None,
    start_at: int = 0,
    limit: int = 50,
) -> PageBeanBoard:
    """List agile boards, optionally filtered by project or type."""
    return client.list_boards(
        project_key=project_key,
        board_type=board_type,
        start_at=start_at,
        max_results=limit,
    )


def get_board_issues(
    board_id: str,
    start_at: int = 0,
    limit: int = 50,
) -> SearchResults:
    """Get issues on an agile board. Description is not included; use get_issue for full detail."""
    result = client.get_board_issues(
        int(board_id),
        start_at=start_at,
        max_results=limit,
    )
    for issue in result.issues:
        if issue.fields:
            issue.fields.description = None
    return result


def get_backlog_issues(
    board_id: str,
    start_at: int = 0,
    limit: int = 50,
) -> SearchResults:
    """Get backlog issues (not assigned to any sprint) on a board. Description is not included; use get_issue for full detail."""
    result = client.get_backlog_issues(
        int(board_id),
        start_at=start_at,
        max_results=limit,
    )
    for issue in result.issues:
        if issue.fields:
            issue.fields.description = None
    return result


def get_epic_issues(
    epic_key: str,
    start_at: int = 0,
    limit: int = 50,
) -> SearchResults:
    """Get issues belonging to an epic. Description is not included; use get_issue for full detail."""
    result = client.get_epic_issues(
        epic_key,
        start_at=start_at,
        max_results=limit,
    )
    for issue in result.issues:
        if issue.fields:
            issue.fields.description = None
    return result


def get_epic(epic_key: str) -> Epic:
    """Get details of an epic (name, summary, done status)."""
    return client.get_epic(epic_key)


# --- Sprint ---


def list_sprints(
    board_id: str,
    state: str | None = None,
    start_at: int = 0,
    limit: int = 50,
) -> SprintPage:
    """List sprints for a board, optionally filtered by state."""
    return client.list_sprints(
        int(board_id),
        state=state,
        start_at=start_at,
        max_results=limit,
    )


def get_sprint_issues(
    sprint_id: str,
    start_at: int = 0,
    limit: int = 50,
) -> SearchResults:
    """Get issues in a specific sprint. Description is not included; use get_issue for full detail."""
    result = client.get_sprint_issues(
        int(sprint_id),
        start_at=start_at,
        max_results=limit,
    )
    for issue in result.issues:
        if issue.fields:
            issue.fields.description = None
    return result


def get_sprint(sprint_id: str) -> SprintBean:
    """Get details of a specific sprint."""
    return client.get_sprint(int(sprint_id))


def move_issues_to_sprint(sprint_id: str, issue_keys: list[str]) -> str:
    """Move issues to a sprint."""
    client.move_issues_to_sprint(int(sprint_id), issue_keys=issue_keys)
    return "OK"


def create_sprint(
    board_id: str,
    name: str,
    goal: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """Create a new sprint on a board."""
    client.create_sprint(
        int(board_id),
        name,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
    )
    return "OK"


def update_sprint(
    sprint_id: str,
    name: str | None = None,
    state: str | None = None,
    goal: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    """Update a sprint's name, state, goal, or dates."""
    client.update_sprint(
        int(sprint_id),
        name=name,
        state=state,
        goal=goal,
        start_date=start_date,
        end_date=end_date,
    )
    return "OK"


def delete_sprint(sprint_id: str) -> str:
    """Delete a sprint."""
    client.delete_sprint(int(sprint_id))
    return "OK"


def link_to_epic(epic_key: str, issue_keys: list[str]) -> str:
    """Link issues to an epic."""
    client.link_to_epic(epic_key, issue_keys=issue_keys)
    return "OK"


def move_to_backlog(issue_keys: list[str]) -> str:
    """Move issues from sprints back to the backlog."""
    client.move_to_backlog(issue_keys=issue_keys)
    return "OK"


# --- Worklog ---


def get_worklogs(
    issue_key: str,
    start_at: int = 0,
    limit: int = 50,
    plain: bool = True,
) -> PageOfWorklogs:
    """Get worklog entries on an issue. Comment is Markdown. Set plain=false to preserve ADF-only features for editing."""
    result = client.get_worklogs(issue_key, start_at=start_at, max_results=limit)
    for wl in result.worklogs:
        if isinstance(wl.comment, dict):
            wl.comment = to_md(wl.comment, plain=plain)
    return result


def add_worklog(
    issue_key: str,
    time_spent: str,
    started: str | None = None,
    comment: str | None = None,
) -> str:
    """Add a worklog entry to an issue. Comment is Markdown."""
    client.add_worklog(
        issue_key,
        time_spent=time_spent,
        started=started,
        comment=to_adf(comment) if comment else None,
    )
    return "OK"


def update_worklog(
    issue_key: str,
    worklog_id: str,
    time_spent: str | None = None,
    started: str | None = None,
    comment: str | None = None,
) -> str:
    """Update a worklog entry. Comment is Markdown."""
    client.update_worklog(
        issue_key,
        worklog_id,
        time_spent=time_spent,
        started=started,
        comment=to_adf(comment) if comment else None,
    )
    return "OK"


def delete_worklog(issue_key: str, worklog_id: str) -> str:
    """Delete a worklog entry from an issue."""
    client.delete_worklog(issue_key, worklog_id)
    return "OK"


# --- Version ---


def create_version(
    project_key: str,
    name: str,
    description: str | None = None,
    start_date: str | None = None,
    release_date: str | None = None,
    released: bool = False,
) -> str:
    """Create a new version (release) in a project."""
    client.create_version(
        project_key,
        name,
        description=description,
        start_date=start_date,
        release_date=release_date,
        released=released,
    )
    return "OK"


def update_version(
    version_id: str,
    name: str | None = None,
    description: str | None = None,
    start_date: str | None = None,
    release_date: str | None = None,
    released: bool | None = None,
) -> str:
    """Update a version (release). Set released=true to mark it released."""
    client.update_version(
        version_id,
        name=name,
        description=description,
        start_date=start_date,
        release_date=release_date,
        released=released,
    )
    return "OK"


def delete_version(version_id: str) -> str:
    """Delete a version (release)."""
    client.delete_version(version_id)
    return "OK"
