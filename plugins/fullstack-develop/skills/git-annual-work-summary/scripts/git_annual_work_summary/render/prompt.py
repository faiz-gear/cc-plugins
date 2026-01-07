from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple

from ..analysis.stats import compute_stats
from ..analysis.themes import suggest_themes, themes_to_markdown
from ..config import clustering_params, core_weight_multiplier, pick_core_projects
from ..io import render_template


def render_prompt_markdown(
    *,
    input_path: str,
    data: Dict[str, Any],
    config: Dict[str, Any],
    year: int,
    language: str,
    template_path: str,
) -> Tuple[str, Dict[str, Any]]:
    with open(template_path, "r", encoding="utf-8") as f:
        template_text = f.read()

    projects = data.get("projects") or []
    core_projects, core_meta = pick_core_projects(config, projects)
    multiplier = core_weight_multiplier(config)
    cluster = clustering_params(config)

    authors = config.get("authors") or (data.get("filters") or {}).get("authors") or []
    authors_str = ", ".join(authors) if authors else "(no filter)"
    core_str = ", ".join(core_projects) if core_projects else "(none)"

    project_context = config.get("project_context") or {}
    ctx_lines: List[str] = []
    if isinstance(project_context, dict) and project_context:
        for k in core_projects:
            v = project_context.get(k)
            if v:
                ctx_lines.append(f"- {k}: {v}")
        for k, v in project_context.items():
            if k in core_projects:
                continue
            ctx_lines.append(f"- {k}: {v}")
    project_context_str = "\n".join(ctx_lines).strip() if ctx_lines else ""

    # Always recompute stats to reflect any merge/file edits.
    stats = data.get("stats")
    if not isinstance(stats, dict):
        stats = compute_stats(projects, year, authors)

    theme_analysis = suggest_themes(
        projects=projects,
        core_projects=core_projects,
        core_multiplier=multiplier,
        max_themes=cluster["max_themes"],
        min_commits_per_theme=cluster["min_commits_per_theme"],
        language=language,
    )

    prompt_body = render_template(
        template_text,
        {
            "YEAR": str(year),
            "AUTHORS": authors_str,
            "CORE_PROJECTS": core_str,
            "PROJECT_CONTEXT": project_context_str or "(not provided)",
            "INPUT_JSON_PATH": os.path.abspath(input_path),
        },
    ).rstrip() + "\n"

    meta = {
        "core_projects": core_projects,
        "core_meta": core_meta,
        "weighting": {"core_multiplier": multiplier},
        "clustering": cluster,
        "language": language,
    }

    out_text = (
        prompt_body
        + "\n---\n\n"
        + themes_to_markdown(theme_analysis)
        + "\n---\n\n"
        + "### Appendix: stats (from input JSON)\n\n"
        + "```json\n"
        + json.dumps(stats, ensure_ascii=False, indent=2)
        + "\n```\n"
    )
    return out_text, meta
