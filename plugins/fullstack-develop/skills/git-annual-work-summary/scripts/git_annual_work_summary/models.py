from __future__ import annotations

from typing import Any, Dict


def short_hash(value: str) -> str:
    return value[:8] if value else value


def commit_to_common(commit: Dict[str, Any], platform: str, parse_conventional_title) -> Dict[str, Any]:
    title = (commit.get("title") or commit.get("message") or "").split("\n", 1)[0].strip()
    committed_date = commit.get("committed_date") or commit.get("date") or commit.get("created_at")
    author_name = (
        commit.get("author_name")
        or commit.get("author", {}).get("name")
        or commit.get("commit", {}).get("author", {}).get("name")
    )
    author_email = (
        commit.get("author_email")
        or commit.get("author", {}).get("email")
        or commit.get("commit", {}).get("author", {}).get("email")
    )
    author_username = commit.get("author", {}).get("login") if isinstance(commit.get("author"), dict) else None
    message = commit.get("message") or commit.get("commit", {}).get("message") or title
    web_url = commit.get("web_url") or commit.get("html_url")
    commit_id = commit.get("id") or commit.get("sha") or commit.get("hash")
    conventional = parse_conventional_title(title)
    return {
        "id": commit_id,
        "short_id": short_hash(commit_id or ""),
        "title": title,
        "message": message,
        "author_name": author_name,
        "author_email": author_email,
        "author_username": author_username,
        "committed_date": committed_date,
        "web_url": web_url,
        "platform": platform,
        "conventional": conventional,
    }

