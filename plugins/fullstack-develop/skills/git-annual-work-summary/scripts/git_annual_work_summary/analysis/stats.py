from __future__ import annotations

import datetime as dt
import re
from typing import Any, Dict, List, Tuple


ISO_Z_RE = re.compile(r"Z$")


def compute_stats(projects: List[Dict[str, Any]], year: int, authors: List[str]) -> Dict[str, Any]:
    by_type: Dict[str, int] = {}
    by_scope: Dict[str, int] = {}
    by_project: Dict[str, int] = {}
    by_month: Dict[str, int] = {}
    by_platform: Dict[str, int] = {}
    non_conventional = 0
    breaking_changes = 0
    total = 0
    examples_by_project: Dict[str, List[str]] = {}

    for project in projects:
        key = project.get("path_with_namespace") or project.get("full_name") or project.get("name") or "unknown"
        platform = project.get("platform") or "unknown"
        commits = project.get("commits") or []
        for c in commits:
            total += 1
            by_project[key] = by_project.get(key, 0) + 1
            by_platform[platform] = by_platform.get(platform, 0) + 1
            conv = (c.get("conventional") or {})
            if conv.get("is_conventional"):
                t = conv.get("type") or "other"
                by_type[t] = by_type.get(t, 0) + 1
                scope = conv.get("scope")
                if scope:
                    by_scope[scope] = by_scope.get(scope, 0) + 1
                if conv.get("breaking"):
                    breaking_changes += 1
            else:
                non_conventional += 1

            date_str = c.get("committed_date") or ""
            month = None
            try:
                s = date_str.replace("Z", "+00:00") if ISO_Z_RE.search(date_str) else date_str
                parsed = dt.datetime.fromisoformat(s)
                month = f"{parsed.year:04d}-{parsed.month:02d}"
            except ValueError:
                month = None
            if month:
                by_month[month] = by_month.get(month, 0) + 1
            if len(examples_by_project.get(key, [])) < 8:
                examples_by_project.setdefault(key, []).append(c.get("title") or "")

    def sort_dict(d: Dict[str, int]) -> List[Tuple[str, int]]:
        return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))

    return {
        "year": year,
        "authors_filter": authors,
        "total_commits": total,
        "non_conventional_commits": non_conventional,
        "breaking_changes": breaking_changes,
        "by_platform": sort_dict(by_platform),
        "by_project": sort_dict(by_project),
        "by_type": sort_dict(by_type),
        "by_scope": sort_dict(by_scope)[:20],
        "by_month": sorted(by_month.items(), key=lambda kv: kv[0]),
        "examples_by_project": examples_by_project,
    }


def format_stats_markdown(stats: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"# Commit Stats ({stats.get('year', '')})")
    lines.append("")
    lines.append(f"- Total commits: {stats.get('total_commits', 0)}")
    lines.append(f"- Non-conventional commits: {stats.get('non_conventional_commits', 0)}")
    lines.append(f"- Breaking changes: {stats.get('breaking_changes', 0)}")
    lines.append("")

    def table(title: str, rows: List[Tuple[str, int]]) -> None:
        if not rows:
            return
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| Key | Count |")
        lines.append("| --- | ---: |")
        for k, v in rows:
            lines.append(f"| {k} | {v} |")
        lines.append("")

    table("By Platform", stats.get("by_platform") or [])
    table("By Project", (stats.get("by_project") or [])[:30])
    table("By Type (Conventional Commits)", stats.get("by_type") or [])

    scopes = stats.get("by_scope") or []
    if scopes:
        table("Top Scopes", scopes)

    months = stats.get("by_month") or []
    if months:
        lines.append("## By Month")
        lines.append("")
        lines.append("| Month | Count |")
        lines.append("| --- | ---: |")
        for k, v in months:
            lines.append(f"| {k} | {v} |")
        lines.append("")

    examples = stats.get("examples_by_project") or {}
    if isinstance(examples, dict) and examples:
        lines.append("## Examples (first few titles per project)")
        lines.append("")
        for project, titles in examples.items():
            if not titles:
                continue
            lines.append(f"### {project}")
            for t in titles[:8]:
                if t:
                    lines.append(f"- {t}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"

