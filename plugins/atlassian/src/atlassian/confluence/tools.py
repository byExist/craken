"""Confluence MCP tools — pure functions, registered by server.py."""

import base64

from marklas import to_adf, to_md

from atlassian.confluence import client
from atlassian.confluence.schema.ancestor import MultiEntityResultAncestor
from atlassian.confluence.schema.analytics import ContentViews
from atlassian.confluence.schema.attachment import MultiEntityResultAttachment
from atlassian.confluence.schema.blog_post import BlogPost, MultiEntityResultBlogPost
from atlassian.confluence.schema.comment import MultiEntityResultComment
from atlassian.confluence.schema.inline_comment import MultiEntityResultInlineComment
from atlassian.confluence.schema.label import MultiEntityResultLabel
from atlassian.confluence.schema.page import (
    MultiEntityResultChildPage,
    MultiEntityResultPage,
    Page,
)
from atlassian.confluence.schema.search import SearchResults
from atlassian.confluence.schema.space import MultiEntityResultSpace, Space
from atlassian.confluence.schema.task import MultiEntityResultTask
from atlassian.confluence.schema.user import User
from atlassian.confluence.schema.version import MultiEntityResultPageVersion
from atlassian.files import read_body, write_body, write_temp


# --- User ---


def get_current_user() -> User:
    """Get the currently authenticated user."""
    return client.get_current_user()


# --- Space ---


def list_spaces(
    limit: int = 25,
    space_type: str | None = None,
    status: str | None = None,
) -> MultiEntityResultSpace:
    """List Confluence spaces."""
    return client.list_spaces(
        space_type=space_type,
        status=status,
        limit=limit,
    )


def get_space(space_id: str) -> Space:
    """Get details of a specific space."""
    return client.get_space(space_id)


# --- Page ---


def search_content(cql: str, limit: int = 25) -> SearchResults:
    """Search Confluence content using CQL query. Use get_page for full content."""
    return client.search_content(cql, limit=limit)


def list_pages(
    space_id: str,
    title: str | None = None,
    limit: int = 25,
) -> MultiEntityResultPage:
    """List pages in a space, optionally filtered by title. Body is not included; use get_page for full content."""
    result = client.list_pages(space_id, title=title, limit=limit)
    for page in result.results:
        page.body = None
    return result


def get_page(page_id: str, plain: bool = True, to_file: str | None = None) -> Page:
    """Get a Confluence page by ID. Body is Markdown. Set plain=false to preserve ADF-only features for editing.

    Pass to_file (absolute path) to write the body to that file and omit it from the
    response — edit the file, then publish with update_page(from_file=...). Use the
    returned version as expected_version to guard against concurrent edits.
    """
    page = client.get_page(page_id)
    if isinstance(page.body, dict):
        page.body = to_md(page.body, plain=plain)
    if to_file is not None and isinstance(page.body, str):
        write_body(to_file, page.body)
        page.body = None
    return page


def get_page_children(page_id: str, limit: int = 25) -> MultiEntityResultChildPage:
    """Get child pages of a specific page."""
    return client.get_page_children(page_id, limit=limit)


def get_page_descendants(
    page_id: str, limit: int = 25, depth: int | None = None
) -> MultiEntityResultChildPage:
    """Get all descendant pages (full subtree) of a page. get_page_children is one level; this is the whole tree."""
    return client.get_page_descendants(page_id, depth=depth, limit=limit)


def get_page_versions(page_id: str, limit: int = 25) -> MultiEntityResultPageVersion:
    """Get version history of a page."""
    return client.get_page_versions(page_id, limit=limit)


def get_ancestors(page_id: str) -> MultiEntityResultAncestor:
    """Get the ancestor (parent chain) of a page."""
    return client.get_ancestors(page_id)


def get_page_views(page_id: str) -> ContentViews:
    """Get the view count of a page."""
    return client.get_page_views(page_id)


def get_likes(page_id: str) -> dict[str, int]:
    """Get the like count of a page."""
    return {"count": client.get_likes_count(page_id)}


def get_attachments(page_id: str, limit: int = 25) -> MultiEntityResultAttachment:
    """Get attachments on a page."""
    return client.get_attachments(page_id, limit=limit)


def download_attachment(page_id: str, attachment_id: str) -> str:
    """Download an attachment to a temp file; returns the saved path.

    The file lands in the OS temp dir with a type-appropriate extension and
    never passes through the model's context. Copy it elsewhere to keep it.
    """
    data, content_type = client.get_attachment_content(page_id, attachment_id)
    return write_temp(data, content_type)


def search_users(cql: str, limit: int = 25) -> SearchResults:
    """Search Confluence users using CQL query."""
    return client.search_users(cql, limit=limit)


def create_page(
    space_id: str,
    title: str,
    content: str | None = None,
    parent_id: str | None = None,
    from_file: str | None = None,
) -> str:
    """Create a new Confluence page. Content is Markdown, or pass from_file to read it from a local file (not both)."""
    if content and from_file:
        raise ValueError("provide either content or from_file, not both")
    if from_file is not None:
        content = read_body(from_file)
    adf = to_adf(content) if content else None
    client.create_page(
        space_id,
        title,
        body=adf,
        parent_id=parent_id,
    )
    return "OK"


def update_page(
    page_id: str,
    title: str,
    content: str | None = None,
    from_file: str | None = None,
    expected_version: int | None = None,
) -> str:
    """Update an existing Confluence page. Content is Markdown, or pass from_file to read it from a local file.

    Pass expected_version (from get_page) to refuse the write if the page changed
    since you fetched it, instead of clobbering the newer version.
    """
    if content and from_file:
        raise ValueError("provide either content or from_file, not both")
    if from_file is not None:
        content = read_body(from_file)
    if content is None:
        raise ValueError("provide either content or from_file")
    current = client.get_page(page_id)
    current_version = current.version.number if current.version else 0
    if expected_version is not None and current_version != expected_version:
        raise ValueError(
            f"version conflict: page is now at {current_version}, but your edits are based "
            f"on {expected_version}; re-fetch with get_page and reapply"
        )
    client.update_page(
        page_id,
        title,
        body=to_adf(content),
        version_number=(current_version or 0) + 1,
    )
    return "OK"


# --- Blog post ---


def list_blog_posts(
    space_id: str | None = None, limit: int = 25
) -> MultiEntityResultBlogPost:
    """List blog posts, optionally filtered by space. Body is not included; use get_blog_post for full content."""
    result = client.list_blog_posts(space_id=space_id, limit=limit)
    for post in result.results:
        post.body = None
    return result


def get_blog_post(
    blog_post_id: str, plain: bool = True, to_file: str | None = None
) -> BlogPost:
    """Get a blog post by ID. Body is Markdown. Set plain=false to preserve ADF-only features for editing.

    Pass to_file (absolute path) to write the body to that file and omit it from the
    response — edit the file, then publish with update_blog_post(from_file=...). Use the
    returned version as expected_version to guard against concurrent edits.
    """
    post = client.get_blog_post(blog_post_id)
    if isinstance(post.body, dict):
        post.body = to_md(post.body, plain=plain)
    if to_file is not None and isinstance(post.body, str):
        write_body(to_file, post.body)
        post.body = None
    return post


def create_blog_post(
    space_id: str,
    title: str,
    content: str | None = None,
    from_file: str | None = None,
) -> str:
    """Create a new blog post. Content is Markdown, or pass from_file to read it from a local file (not both)."""
    if content and from_file:
        raise ValueError("provide either content or from_file, not both")
    if from_file is not None:
        content = read_body(from_file)
    client.create_blog_post(
        space_id,
        title,
        body=to_adf(content) if content else None,
    )
    return "OK"


def update_blog_post(
    blog_post_id: str,
    title: str,
    content: str | None = None,
    from_file: str | None = None,
    expected_version: int | None = None,
) -> str:
    """Update a blog post. Content is Markdown, or pass from_file to read it from a local file.

    Pass expected_version (from get_blog_post) to refuse the write if it changed
    since you fetched it, instead of clobbering the newer version.
    """
    if content and from_file:
        raise ValueError("provide either content or from_file, not both")
    if from_file is not None:
        content = read_body(from_file)
    if content is None:
        raise ValueError("provide either content or from_file")
    current = client.get_blog_post(blog_post_id)
    current_version = current.version.number if current.version else 0
    if expected_version is not None and current_version != expected_version:
        raise ValueError(
            f"version conflict: blog post is now at {current_version}, but your edits are based "
            f"on {expected_version}; re-fetch with get_blog_post and reapply"
        )
    client.update_blog_post(
        blog_post_id,
        title,
        body=to_adf(content),
        version_number=(current_version or 0) + 1,
    )
    return "OK"


def delete_blog_post(blog_post_id: str) -> str:
    """Delete a blog post."""
    client.delete_blog_post(blog_post_id)
    return "OK"


# --- Comment ---


def get_comments(
    page_id: str, limit: int = 25, plain: bool = True
) -> MultiEntityResultComment:
    """Get comments on a page. Body is Markdown. Set plain=false to preserve ADF-only features for editing."""
    result = client.get_comments(page_id, limit=limit)
    for comment in result.results:
        if isinstance(comment.body, dict):
            comment.body = to_md(comment.body, plain=plain)
    return result


def add_comment(page_id: str, content: str) -> str:
    """Add a comment to a page. Content is Markdown."""
    client.add_comment(page_id, body=to_adf(content))
    return "OK"


def edit_comment(comment_id: str, content: str) -> str:
    """Edit an existing footer comment. Content is Markdown."""
    version = client.get_comment_version(comment_id)
    client.edit_comment(
        comment_id,
        body=to_adf(content),
        version_number=version + 1,
    )
    return "OK"


def delete_comment(comment_id: str) -> str:
    """Delete a footer comment."""
    client.delete_comment(comment_id)
    return "OK"


def reply_to_comment(page_id: str, parent_comment_id: str, content: str) -> str:
    """Reply to an existing footer comment. Content is Markdown."""
    client.reply_to_comment(page_id, parent_comment_id, body=to_adf(content))
    return "OK"


def get_comment_replies(
    comment_id: str, limit: int = 25, plain: bool = True
) -> MultiEntityResultComment:
    """Get replies to a footer comment. Body is Markdown. Set plain=false to preserve ADF-only features."""
    result = client.get_comment_children(comment_id, limit=limit)
    for comment in result.results:
        if isinstance(comment.body, dict):
            comment.body = to_md(comment.body, plain=plain)
    return result


# --- Inline Comment ---


def get_inline_comments(
    page_id: str, limit: int = 25, plain: bool = True
) -> MultiEntityResultInlineComment:
    """Get inline comments on a page. Body is Markdown. Set plain=false to preserve ADF-only features for editing."""
    result = client.get_inline_comments(page_id, limit=limit)
    for comment in result.results:
        if isinstance(comment.body, dict):
            comment.body = to_md(comment.body, plain=plain)
    return result


def create_inline_comment(
    page_id: str,
    content: str,
    inline_marker_ref: str | None = None,
    inline_original_selection: str | None = None,
) -> str:
    """Create an inline comment on a page. Content is Markdown."""
    client.create_inline_comment(
        page_id,
        body=to_adf(content),
        inline_marker_ref=inline_marker_ref,
        inline_original_selection=inline_original_selection,
    )
    return "OK"


def resolve_inline_comment(comment_id: str) -> str:
    """Resolve an inline comment."""
    client.resolve_inline_comment(comment_id)
    return "OK"


def delete_inline_comment(comment_id: str) -> str:
    """Delete an inline comment."""
    client.delete_inline_comment(comment_id)
    return "OK"


def get_inline_comment_replies(
    comment_id: str, limit: int = 25, plain: bool = True
) -> MultiEntityResultInlineComment:
    """Get replies to an inline comment. Body is Markdown. Set plain=false to preserve ADF-only features."""
    result = client.get_inline_comment_children(comment_id, limit=limit)
    for comment in result.results:
        if isinstance(comment.body, dict):
            comment.body = to_md(comment.body, plain=plain)
    return result


# --- Label ---


def get_labels(page_id: str) -> MultiEntityResultLabel:
    """Get labels attached to a page."""
    return client.get_labels(page_id)


def add_label(page_id: str, label: str) -> str:
    """Add a label to a page."""
    client.add_label(page_id, label)
    return "OK"


def remove_label(page_id: str, label: str) -> str:
    """Remove a label from a page."""
    client.remove_label(page_id, label)
    return "OK"


# --- Attachment ---


def upload_attachment(
    page_id: str, filename: str, data_base64: str, comment: str | None = None
) -> str:
    """Upload an attachment to a page. Data is base64-encoded."""
    raw = base64.b64decode(data_base64)
    client.upload_attachment(page_id, filename=filename, data=raw, comment=comment)
    return "OK"


def delete_attachment(attachment_id: str) -> str:
    """Delete an attachment."""
    client.delete_attachment(attachment_id)
    return "OK"


# --- Page management ---


def delete_page(page_id: str) -> str:
    """Delete a Confluence page."""
    client.delete_page(page_id)
    return "OK"


def move_page(page_id: str, position: str, target_id: str) -> str:
    """Move a page in the page tree. Position: 'before', 'after', 'append'."""
    client.move_page(page_id, position, target_id)
    return "OK"


def copy_page(
    page_id: str,
    destination_type: str,
    destination_value: str,
    title: str | None = None,
) -> str:
    """Copy a page (with attachments and labels) to a new location.

    destination_type: 'parent_page' (value = parent page id), 'space' (value = space key),
    or 'existing_page' (value = page id). Pass title to rename the copy.
    """
    client.copy_page(
        page_id,
        destination_type=destination_type,
        destination_value=destination_value,
        title=title,
    )
    return "OK"


def restore_page_version(
    page_id: str, version_number: int, message: str | None = None
) -> str:
    """Restore a page to a previous version (from get_page_versions)."""
    client.restore_page_version(
        page_id,
        version_number,
        message=message or f"Restored to version {version_number}",
    )
    return "OK"


# --- Task ---


def get_tasks(
    page_id: str | None = None,
    status: str | None = None,
    limit: int = 25,
    plain: bool = True,
) -> MultiEntityResultTask:
    """Get inline tasks (action items), optionally filtered by page or status ('complete'/'incomplete'). Body is Markdown."""
    result = client.list_tasks(page_id=page_id, status=status, limit=limit)
    for task in result.results:
        if isinstance(task.body, dict):
            task.body = to_md(task.body, plain=plain)
    return result


def update_task(task_id: str, status: str) -> str:
    """Update a task's status. Status: 'complete' or 'incomplete'."""
    client.update_task(task_id, status)
    return "OK"
