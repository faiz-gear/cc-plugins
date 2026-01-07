from __future__ import annotations

import datetime as dt
import urllib.parse
from typing import Any, Dict, List, Tuple

from ..http import api_get_json, api_get_paginated_xnext
from ..models import commit_to_common


def gitlab_headers(token: str) -> Dict[str, str]:
    return {"PRIVATE-TOKEN": token.strip(), "Accept": "application/json"}


def parse_year_range(year: int) -> Tuple[str, str]:
    since = dt.datetime(year, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    until = dt.datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    return since.isoformat().replace("+00:00", "Z"), until.isoformat().replace("+00:00", "Z")


def get_current_user(api_base: str, headers: Dict[str, str]) -> Dict[str, Any]:
    user_url = f"{api_base}/user"
    user_info, _ = api_get_json(user_url, headers)
    if not isinstance(user_info, dict):
        raise RuntimeError("Expected user profile from GitLab API")
    return user_info


def list_contributed_projects(api_base: str, headers: Dict[str, str], year: int) -> List[Dict[str, Any]]:
    user_info = get_current_user(api_base, headers)
    user_id = user_info.get("id")
    if not user_id:
        raise RuntimeError("Unable to determine user id from GitLab")

    after = f"{year}-01-01"
    before = f"{year + 1}-01-01"
    events_url = (
        f"{api_base}/users/{user_id}/events"
        f"?after={urllib.parse.quote(after)}&before={urllib.parse.quote(before)}"
    )
    events = api_get_paginated_xnext(events_url, headers)
    seen = set()
    project_ids: List[int] = []
    for event in events:
        if not isinstance(event, dict):
            continue
        project_id = event.get("project_id")
        if project_id and project_id not in seen:
            seen.add(project_id)
            project_ids.append(project_id)

    projects: List[Dict[str, Any]] = []
    for project_id in project_ids:
        project_info, _ = api_get_json(f"{api_base}/projects/{project_id}", headers)
        if isinstance(project_info, dict):
            projects.append(project_info)
    return projects


def _project_id_to_api_path(project_id: str) -> str:
    return project_id if project_id.isdigit() else urllib.parse.quote(project_id, safe="")


def collect_project_commits(
    api_base: str,
    headers: Dict[str, str],
    project_id: str,
    year: int,
    parse_conventional_title,
) -> Dict[str, Any]:
    project_api_id = _project_id_to_api_path(project_id)
    project_url = f"{api_base}/projects/{project_api_id}"
    project_info, _ = api_get_json(project_url, headers)
    if not isinstance(project_info, dict):
        raise RuntimeError("Expected project object from GitLab API")

    since, until = parse_year_range(year)
    commits_url = (
        f"{api_base}/projects/{project_api_id}/repository/commits"
        f"?since={urllib.parse.quote(since)}&until={urllib.parse.quote(until)}&all=true"
    )
    commits = api_get_paginated_xnext(commits_url, headers)

    unique: List[Dict[str, Any]] = []
    seen_ids = set()
    for c in commits:
        if not isinstance(c, dict):
            continue
        cid = c.get("id")
        if not cid or cid in seen_ids:
            continue
        seen_ids.add(cid)
        unique.append(c)

    common_commits = [commit_to_common(c, "gitlab", parse_conventional_title) for c in unique]
    return {
        "platform": "gitlab",
        "id": project_info.get("id"),
        "name": project_info.get("name"),
        "path_with_namespace": project_info.get("path_with_namespace"),
        "web_url": project_info.get("web_url"),
        "commits": common_commits,
        "commit_count": len(common_commits),
    }

