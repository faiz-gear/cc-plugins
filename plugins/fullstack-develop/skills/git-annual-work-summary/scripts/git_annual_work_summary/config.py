from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _truthy_str_list(value: Any) -> List[str]:
    if not isinstance(value, list):
        return []
    out = []
    for x in value:
        if isinstance(x, str) and x.strip():
            out.append(x.strip())
    return out


def pick_core_projects(config: Dict[str, Any], projects: List[Dict[str, Any]]) -> Tuple[List[str], Dict[str, Any]]:
    """
    Return (core_projects, meta).

    Back-compat:
    - legacy `core_projects: []`
    New schema:
    - `core: { mode: auto|manual, top_n: int, projects: [] }`
    """
    available = []
    for p in projects:
        if not isinstance(p, dict):
            continue
        key = p.get("path_with_namespace") or p.get("full_name") or p.get("name")
        if key:
            available.append(str(key))

    def resolve_manual_names(manual: List[str]) -> Tuple[List[str], Dict[str, Any]]:
        if not manual:
            return [], {"resolved": []}
        resolved = []
        mapping = {}
        for name in manual:
            if name in available:
                resolved.append(name)
                mapping[name] = name
                continue
            candidates = [k for k in available if k == name or k.endswith("/" + name) or k.split("/")[-1] == name]
            if len(candidates) == 1:
                resolved.append(candidates[0])
                mapping[name] = candidates[0]
            else:
                resolved.append(name)
                mapping[name] = None
        return resolved, {"resolved": mapping}

    legacy = _truthy_str_list(config.get("core_projects"))
    if legacy:
        resolved, meta = resolve_manual_names(legacy)
        return resolved, {"mode": "manual", "source": "core_projects", **meta}

    core_cfg = config.get("core")
    if isinstance(core_cfg, dict):
        mode = (core_cfg.get("mode") or "").lower()
        manual_raw = _truthy_str_list(core_cfg.get("projects"))
        manual, manual_meta = resolve_manual_names(manual_raw)
        if mode == "manual":
            return manual, {"mode": "manual", "source": "core.projects", **manual_meta}
        if mode == "auto":
            top_n = int(core_cfg.get("top_n") or 2)
            scored = []
            for p in projects:
                if not isinstance(p, dict):
                    continue
                key = p.get("path_with_namespace") or p.get("full_name") or p.get("name")
                if not key:
                    continue
                scored.append((str(key), int(p.get("commit_count") or 0)))
            scored.sort(key=lambda kv: (-kv[1], kv[0]))
            auto = [k for k, _ in scored[: max(0, top_n)]]
            core = manual + [p for p in auto if p not in manual]
            return core, {
                "mode": "auto",
                "source": "core",
                "top_n": top_n,
                "auto_rank": scored[: max(0, top_n)],
                **manual_meta,
            }

    return [], {"mode": "none", "source": "none"}


def core_weight_multiplier(config: Dict[str, Any]) -> int:
    weighting = config.get("weighting")
    if isinstance(weighting, dict):
        try:
            return int(weighting.get("core_multiplier") or 3)
        except (TypeError, ValueError):
            return 3
    return 3


def clustering_params(config: Dict[str, Any]) -> Dict[str, int]:
    clustering = config.get("clustering")
    if not isinstance(clustering, dict):
        return {"max_themes": 10, "min_commits_per_theme": 5}
    out = {"max_themes": 10, "min_commits_per_theme": 5}
    for k in list(out.keys()):
        try:
            out[k] = int(clustering.get(k) or out[k])
        except (TypeError, ValueError):
            pass
    return out
