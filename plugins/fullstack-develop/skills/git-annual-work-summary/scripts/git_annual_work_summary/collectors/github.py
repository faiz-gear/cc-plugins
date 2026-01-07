from __future__ import annotations

import datetime as dt
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple

from ..http import api_get_json, api_get_paginated_link
from ..io import normalize_base_url
from ..models import commit_to_common


def github_headers(token: str) -> Dict[str, str]:
    token = token.strip()
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "git-annual-work-summary",
    }


def github_api_base_from_url(base_url: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    host = (parsed.netloc or "").lower()
    if host in {"github.com", "www.github.com"}:
        return "https://api.github.com"
    return base_url.rstrip("/") + "/api/v3"


def parse_year_range(year: int) -> Tuple[str, str]:
    since = dt.datetime(year, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    until = dt.datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    return since.isoformat().replace("+00:00", "Z"), until.isoformat().replace("+00:00", "Z")


def list_repos(api_base: str, headers: Dict[str, str]) -> List[Dict[str, Any]]:
    url = f"{api_base}/user/repos?affiliation=owner,collaborator,organization_member&per_page=100"
    repos = api_get_paginated_link(url, headers)
    return [r for r in repos if isinstance(r, dict)]


def collect_repo_commits(
    api_base: str,
    headers: Dict[str, str],
    full_name: str,
    year: int,
    author_login: Optional[str],
    web_base: str,
    parse_conventional_title,
) -> Dict[str, Any]:
    if "/" not in full_name:
        raise RuntimeError("GitHub repo must be in owner/repo format")
    owner, repo = full_name.split("/", 1)
    since, until = parse_year_range(year)
    qs = {
        "since": since,
        "until": until,
        "per_page": "100",
    }
    if author_login:
        qs["author"] = author_login
    url = f"{api_base}/repos/{urllib.parse.quote(owner)}/{urllib.parse.quote(repo)}/commits?{urllib.parse.urlencode(qs)}"

    commits: List[Dict[str, Any]] = []
    page = 1
    while True:
        page_url = url + f"&page={page}"
        data, resp_headers = api_get_json(page_url, headers)
        if not isinstance(data, list):
            raise RuntimeError("Expected commit list from GitHub API")
        if not data:
            break
        commits.extend([c for c in data if isinstance(c, dict)])
        link = resp_headers.get("Link", "")
        if 'rel="next"' not in link:
            break
        page += 1

    common_commits = [commit_to_common(c, "github", parse_conventional_title) for c in commits]
    web_url = f"{normalize_base_url(web_base)}/{owner}/{repo}"
    return {
        "platform": "github",
        "name": repo,
        "full_name": full_name,
        "web_url": web_url,
        "commits": common_commits,
        "commit_count": len(common_commits),
    }

