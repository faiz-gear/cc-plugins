from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Tuple


def api_get_json(url: str, headers: Dict[str, str]) -> Tuple[Any, Any]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            return json.loads(data.decode("utf-8")), resp.headers
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def api_get_paginated_xnext(url: str, headers: Dict[str, str]) -> List[Any]:
    results: List[Any] = []
    next_page = "1"
    while next_page:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qs(parsed.query)
        qs["per_page"] = ["100"]
        qs["page"] = [next_page]
        new_query = urllib.parse.urlencode(qs, doseq=True)
        page_url = urllib.parse.urlunparse(parsed._replace(query=new_query))
        data, resp_headers = api_get_json(page_url, headers)
        if not isinstance(data, list):
            raise RuntimeError("Expected a list response from API")
        results.extend(data)
        next_page = resp_headers.get("X-Next-Page", "") or ""
    return results


def parse_http_link_header(value: str) -> Dict[str, str]:
    # GitHub-style: <url>; rel="next", <url>; rel="last"
    links: Dict[str, str] = {}
    for part in (value or "").split(","):
        part = part.strip()
        if not part:
            continue
        if part[0] != "<" or ">;" not in part:
            continue
        url, rest = part.split(">;", 1)
        url = url[1:].strip()
        attrs = rest.split(";")
        rel = None
        for attr in attrs:
            attr = attr.strip()
            if attr.startswith("rel="):
                rel = attr.split("=", 1)[1].strip().strip('"')
        if rel and url:
            links[rel] = url
    return links


def api_get_paginated_link(url: str, headers: Dict[str, str]) -> List[Any]:
    results: List[Any] = []
    next_url = url
    while next_url:
        data, resp_headers = api_get_json(next_url, headers)
        if not isinstance(data, list):
            raise RuntimeError("Expected a list response from API")
        results.extend(data)
        links = parse_http_link_header(resp_headers.get("Link", ""))
        next_url = links.get("next", "")
    return results

