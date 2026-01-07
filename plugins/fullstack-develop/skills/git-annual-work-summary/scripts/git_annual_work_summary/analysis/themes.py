from __future__ import annotations

from typing import Any, Dict, List, Tuple


TYPE_TO_BUCKET = {
    "feat": "Delivery & Features",
    "fix": "Stability & Bugfix",
    "refactor": "Tech Debt & Refactor",
    "perf": "Performance",
    "ci": "Engineering Efficiency",
    "build": "Engineering Efficiency",
    "chore": "Engineering Efficiency",
    "test": "Quality & Testing",
    "docs": "Documentation & Enablement",
}

TYPE_TO_BUCKET_ZH = {
    "feat": "能力建设 / 功能交付",
    "fix": "稳定性 / 问题修复",
    "refactor": "技术债治理 / 重构",
    "perf": "性能优化",
    "ci": "工程效率 / 自动化",
    "build": "工程效率 / 构建交付",
    "chore": "工程效率 / 规范化",
    "test": "质量保障 / 测试",
    "docs": "文档沉淀 / 协作效率",
}


def _project_key(project: Dict[str, Any]) -> str:
    return str(project.get("path_with_namespace") or project.get("full_name") or project.get("name") or "unknown")


def _top_n(counter: Dict[str, int], n: int) -> List[Tuple[str, int]]:
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def suggest_themes(
    projects: List[Dict[str, Any]],
    core_projects: List[str],
    core_multiplier: int,
    max_themes: int,
    min_commits_per_theme: int,
    language: str = "en",
) -> Dict[str, Any]:
    """
    Produce a lightweight theme proposal:
    - Always include per-core-project theme (all commits in that project).
    - Add cross-project themes by Conventional type bucket.
    """
    core_set = set(core_projects)
    core_items: List[Dict[str, Any]] = []
    core_subthemes: List[Dict[str, Any]] = []
    bucket_items: Dict[str, Dict[str, Any]] = {}
    total_commits_all_projects = 0
    total_core_commits = 0
    type_to_bucket = TYPE_TO_BUCKET_ZH if (language or "").lower().startswith("zh") else TYPE_TO_BUCKET

    for p in projects:
        pkey = _project_key(p)
        commits = p.get("commits") or []
        if not isinstance(commits, list):
            continue
        total_commits_all_projects += len(commits)
        if pkey in core_set:
            total_core_commits += len(commits)

        if pkey in core_set:
            by_type: Dict[str, int] = {}
            by_scope: Dict[str, int] = {}
            examples: List[str] = []
            scope_examples: Dict[str, List[str]] = {}
            type_examples: Dict[str, List[str]] = {}
            for c in commits:
                conv = (c.get("conventional") or {})
                if conv.get("is_conventional"):
                    t = conv.get("type") or "other"
                    by_type[t] = by_type.get(t, 0) + 1
                    scope = conv.get("scope")
                    if scope:
                        by_scope[scope] = by_scope.get(scope, 0) + 1
                        scope_examples.setdefault(scope, [])
                        if len(scope_examples[scope]) < 8 and c.get("title"):
                            scope_examples[scope].append(c["title"])
                    type_examples.setdefault(t, [])
                    if len(type_examples[t]) < 8 and c.get("title"):
                        type_examples[t].append(c["title"])
                if len(examples) < 12 and c.get("title"):
                    examples.append(c["title"])
            core_items.append(
                {
                    "title": f"Core Project: {pkey}",
                    "kind": "core_project",
                    "projects": [pkey],
                    "commit_count": len(commits),
                    "weight": max(1, int(core_multiplier)),
                    "top_types": _top_n(by_type, 6),
                    "top_scopes": _top_n(by_scope, 8),
                    "examples": examples,
                }
            )
            # Add a few core subthemes by scope (preferred) or type (fallback).
            top_scopes = _top_n(by_scope, 3)
            for scope, count in top_scopes:
                if count < min_commits_per_theme:
                    continue
                core_subthemes.append(
                    {
                        "title": f"{pkey} / scope: {scope}",
                        "kind": "core_project_scope",
                        "projects": [pkey],
                        "commit_count": count,
                        "weight": max(1, int(core_multiplier)),
                        "top_types": _top_n(by_type, 6),
                        "top_scopes": [(scope, count)],
                        "examples": scope_examples.get(scope, [])[:8],
                    }
                )
            if not top_scopes:
                top_types = _top_n(by_type, 3)
                for t, count in top_types:
                    if count < min_commits_per_theme:
                        continue
                    core_subthemes.append(
                        {
                            "title": f"{pkey} / type: {t}",
                            "kind": "core_project_type",
                            "projects": [pkey],
                            "commit_count": count,
                            "weight": max(1, int(core_multiplier)),
                            "top_types": [(t, count)],
                            "top_scopes": _top_n(by_scope, 6),
                            "examples": type_examples.get(t, [])[:8],
                        }
                    )

        for c in commits:
            conv = (c.get("conventional") or {})
            if not conv.get("is_conventional"):
                continue
            t = conv.get("type") or "other"
            bucket = type_to_bucket.get(t, "Other")
            item = bucket_items.setdefault(
                bucket,
                {
                    "title": bucket,
                    "kind": "cross_project_bucket",
                    "projects": set(),
                    "commit_count": 0,
                    "weight": 1,
                    "top_types": {},
                    "top_scopes": {},
                    "examples": [],
                },
            )
            item["projects"].add(pkey)
            item["commit_count"] += 1
            item["top_types"][t] = item["top_types"].get(t, 0) + 1
            scope = conv.get("scope")
            if scope:
                item["top_scopes"][scope] = item["top_scopes"].get(scope, 0) + 1
            if len(item["examples"]) < 10 and c.get("title"):
                item["examples"].append(c["title"])

    bucket_list: List[Dict[str, Any]] = []
    for item in bucket_items.values():
        if item["commit_count"] < min_commits_per_theme:
            continue
        bucket_list.append(
            {
                "title": item["title"],
                "kind": item["kind"],
                "projects": sorted(item["projects"]),
                "commit_count": item["commit_count"],
                "weight": 1,
                "top_types": _top_n(item["top_types"], 8),
                "top_scopes": _top_n(item["top_scopes"], 10),
                "examples": item["examples"],
            }
        )

    core_items.sort(key=lambda x: (-x["commit_count"], x["title"]))
    core_subthemes.sort(key=lambda x: (-x["commit_count"], x["title"]))
    bucket_list.sort(key=lambda x: (-x["commit_count"], x["title"]))
    themes = (core_items + core_subthemes + bucket_list)[: max(0, max_themes)]

    base_share = (total_core_commits / max(1, total_commits_all_projects)) if total_commits_all_projects else 0.0
    recommended_core_share = min(0.85, max(0.5, base_share * max(1, int(core_multiplier))))

    return {
        "core_projects": core_projects,
        "core_commits": total_core_commits,
        "total_commits": total_commits_all_projects,
        "core_multiplier": int(core_multiplier),
        "recommended_core_share": recommended_core_share,
        "themes": themes,
    }


def themes_to_markdown(theme_analysis: Dict[str, Any]) -> str:
    lines: List[str] = []
    core = theme_analysis.get("core_projects") or []
    lines.append("### Suggested Work Themes (auto)")
    lines.append("")
    if core:
        lines.append(f"- Core projects (emphasize first): {', '.join(core)}")
        lines.append(
            f"- Core weighting: multiplier={theme_analysis.get('core_multiplier', 3)}, "
            f"recommended narrative share≈{int(float(theme_analysis.get('recommended_core_share', 0.6)) * 100)}%"
        )
    else:
        lines.append("- Core projects: (none)")
    lines.append("")

    themes = theme_analysis.get("themes") or []
    for idx, t in enumerate(themes, start=1):
        lines.append(f"#### {idx}. {t.get('title')}")
        lines.append(f"- Kind: {t.get('kind')}")
        lines.append(f"- Weight: {t.get('weight')}")
        lines.append(f"- Commits: {t.get('commit_count')}")
        projects = t.get("projects") or []
        if projects:
            lines.append(f"- Projects: {', '.join(projects)}")
        top_types = t.get("top_types") or []
        if top_types:
            lines.append("- Top types: " + ", ".join([f"{k}({v})" for k, v in top_types]))
        top_scopes = t.get("top_scopes") or []
        if top_scopes:
            lines.append("- Top scopes: " + ", ".join([f"{k}({v})" for k, v in top_scopes]))
        examples = t.get("examples") or []
        if examples:
            lines.append("- Example titles:")
            for ex in examples[:8]:
                lines.append(f"  - {ex}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
