from __future__ import annotations

import argparse
import datetime as dt
import getpass
import os
import sys
from typing import Any, Dict, List, Optional

from .analysis.stats import compute_stats, format_stats_markdown
from .collectors import gitlab as gitlab_collector
from .collectors import github as github_collector
from .collectors import local_git as local_git_collector
from .conventional import parse_conventional_title
from .interactive import select_items_interactive
from .io import load_env_file, normalize_base_url, parse_csv, read_json, utc_now_iso, write_json
from .render.prompt import render_prompt_markdown


def filter_commits_by_authors(projects: List[Dict[str, Any]], authors: List[str]) -> List[Dict[str, Any]]:
    if not authors:
        return projects
    selected = set(a.strip() for a in authors if a.strip())
    filtered: List[Dict[str, Any]] = []
    for p in projects:
        commits = p.get("commits") or []
        kept = []
        for c in commits:
            if (c.get("author_name") in selected) or (c.get("author_email") in selected) or (c.get("author_username") in selected):
                kept.append(c)
        updated = dict(p)
        updated["commits"] = kept
        updated["commit_count"] = len(kept)
        filtered.append(updated)
    return filtered


def merge_inputs(inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
    projects: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    seen = set()
    year = None
    for data in inputs:
        if year is None:
            year = data.get("year")
        for err in data.get("errors") or []:
            errors.append(err)
        for p in data.get("projects") or []:
            key = (
                (p.get("platform") or "unknown"),
                p.get("path_with_namespace") or p.get("full_name") or p.get("repo_path") or p.get("name"),
            )
            if key in seen:
                for existing in projects:
                    existing_key = (
                        (existing.get("platform") or "unknown"),
                        existing.get("path_with_namespace") or existing.get("full_name") or existing.get("repo_path") or existing.get("name"),
                    )
                    if existing_key != key:
                        continue
                    existing_commits = existing.get("commits") or []
                    existing_ids = set((c.get("id") for c in existing_commits if c.get("id")))
                    for c in p.get("commits") or []:
                        cid = c.get("id")
                        if cid and cid in existing_ids:
                            continue
                        existing_commits.append(c)
                        if cid:
                            existing_ids.add(cid)
                    existing["commits"] = existing_commits
                    existing["commit_count"] = len(existing_commits)
                    break
                continue
            seen.add(key)
            projects.append(p)
    if year is None:
        year = dt.datetime.utcnow().year
    return {"generated_at": utc_now_iso(), "year": year, "projects": projects, "errors": errors}


def cmd_collect_gitlab(args: argparse.Namespace) -> int:
    env = load_env_file(args.env) if args.env else {}
    year = args.year
    base_url = normalize_base_url(args.url or os.environ.get("GITLAB_URL") or env.get("GITLAB_URL") or "")
    if not base_url:
        base_url = normalize_base_url(input("GitLab URL (e.g. https://gitlab.example.com): ").strip())
    if not base_url:
        print("Missing GitLab URL", file=sys.stderr)
        return 2

    token = args.token or os.environ.get(args.token_env) or env.get(args.token_env)
    if not token and not args.non_interactive:
        token = getpass.getpass(f"GitLab token ({args.token_env}): ").strip() or None
    if not token:
        print(f"Missing GitLab token (env {args.token_env})", file=sys.stderr)
        return 2

    api_base = base_url + "/api/v4"
    headers = gitlab_collector.gitlab_headers(token)

    projects_meta: List[Dict[str, Any]] = []
    if args.projects:
        for pid in parse_csv(args.projects):
            projects_meta.append({"id": pid, "path_with_namespace": pid})
    else:
        print(f"Discovering GitLab projects from events in {year}...")
        try:
            projects_meta = gitlab_collector.list_contributed_projects(api_base, headers, year)
        except Exception as exc:
            print(f"Failed to discover projects: {exc}", file=sys.stderr)
            return 1
        if not args.non_interactive:
            projects_meta = select_items_interactive(
                projects_meta,
                lambda p: f"{p.get('path_with_namespace') or p.get('name') or 'unknown'} (id: {p.get('id')})",
            )

    collected: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for p in projects_meta:
        pid = str(p.get("id") or "").strip()
        if not pid:
            continue
        display = p.get("path_with_namespace") or p.get("name") or pid
        print(f"Collecting GitLab commits: {display}")
        try:
            collected.append(gitlab_collector.collect_project_commits(api_base, headers, pid, year, parse_conventional_title))
        except Exception as exc:
            errors.append({"platform": "gitlab", "project": display, "error": str(exc)})

    authors = parse_csv(args.authors)
    filtered = filter_commits_by_authors(collected, authors)
    stats = compute_stats(filtered, year, authors)
    out = {
        "version": 1,
        "generated_at": utc_now_iso(),
        "platforms": ["gitlab"],
        "gitlab_url": base_url,
        "year": year,
        "filters": {"authors": authors},
        "projects": filtered,
        "stats": stats,
        "errors": errors,
    }
    write_json(args.output, out)
    print(f"Wrote {args.output}")
    return 0


def cmd_collect_github(args: argparse.Namespace) -> int:
    env = load_env_file(args.env) if args.env else {}
    year = args.year
    base_url = normalize_base_url(args.url or os.environ.get("GITHUB_URL") or env.get("GITHUB_URL") or "https://github.com")
    api_base = normalize_base_url(args.api_url) if args.api_url else github_collector.github_api_base_from_url(base_url)

    token = args.token or os.environ.get(args.token_env) or os.environ.get("GH_TOKEN") or env.get(args.token_env) or env.get("GH_TOKEN")
    if not token and not args.non_interactive:
        token = getpass.getpass(f"GitHub token ({args.token_env}/GH_TOKEN): ").strip() or None
    if not token:
        print(f"Missing GitHub token (env {args.token_env} or GH_TOKEN)", file=sys.stderr)
        return 2

    headers = github_collector.github_headers(token)
    repos = parse_csv(args.repos)
    if not repos and args.discover:
        print("Discovering GitHub repositories from your accessible repo list...")
        try:
            discovered = github_collector.list_repos(api_base, headers)
        except Exception as exc:
            print(f"Failed to discover repos: {exc}", file=sys.stderr)
            return 1
        if not args.include_forks:
            discovered = [r for r in discovered if not r.get("fork")]
        if args.owner:
            discovered = [r for r in discovered if (r.get("owner") or {}).get("login") == args.owner]
        if args.non_interactive:
            repos = [r.get("full_name") for r in discovered if r.get("full_name")]
        else:
            selected = select_items_interactive(
                discovered,
                lambda r: f"{r.get('full_name')} ({'fork' if r.get('fork') else 'repo'})",
            )
            repos = [r.get("full_name") for r in selected if r.get("full_name")]

    if not repos:
        print("Missing --repos (comma-separated owner/repo), or use --discover to select from your accessible repos.", file=sys.stderr)
        return 2

    collected: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for full_name in repos:
        print(f"Collecting GitHub commits: {full_name}")
        try:
            collected.append(
                github_collector.collect_repo_commits(
                    api_base,
                    headers,
                    full_name,
                    year,
                    args.user,
                    base_url,
                    parse_conventional_title,
                )
            )
        except Exception as exc:
            errors.append({"platform": "github", "repo": full_name, "error": str(exc)})

    authors = parse_csv(args.authors)
    filtered = filter_commits_by_authors(collected, authors)
    stats = compute_stats(filtered, year, authors)
    out = {
        "version": 1,
        "generated_at": utc_now_iso(),
        "platforms": ["github"],
        "github_url": base_url,
        "github_api_base": api_base,
        "year": year,
        "filters": {"authors": authors, "github_user": args.user},
        "projects": filtered,
        "stats": stats,
        "errors": errors,
    }
    write_json(args.output, out)
    print(f"Wrote {args.output}")
    return 0


def cmd_collect_git(args: argparse.Namespace) -> int:
    year = args.year
    repos = args.repo or []
    if not repos:
        print("Missing --repo (can be repeated)", file=sys.stderr)
        return 2
    collected: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    for repo_path in repos:
        print(f"Collecting local git commits: {repo_path}")
        try:
            collected.append(local_git_collector.collect_repo_commits(repo_path, year, parse_conventional_title))
        except Exception as exc:
            errors.append({"platform": "git", "repo_path": repo_path, "error": str(exc)})

    authors = parse_csv(args.authors)
    filtered = filter_commits_by_authors(collected, authors)
    stats = compute_stats(filtered, year, authors)
    out = {
        "version": 1,
        "generated_at": utc_now_iso(),
        "platforms": ["git"],
        "year": year,
        "filters": {"authors": authors},
        "projects": filtered,
        "stats": stats,
        "errors": errors,
    }
    write_json(args.output, out)
    print(f"Wrote {args.output}")
    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    inputs = [read_json(p) for p in args.inputs]
    merged = merge_inputs(inputs)
    year = int(merged.get("year") or dt.datetime.utcnow().year)
    stats = compute_stats(merged.get("projects") or [], year, [])
    merged["version"] = 1
    merged["stats"] = stats
    write_json(args.output, merged)
    print(f"Wrote {args.output}")
    return 0


def cmd_render_prompt(args: argparse.Namespace) -> int:
    data = read_json(args.input)
    year = args.year or int(data.get("year") or dt.datetime.utcnow().year)
    config: Dict[str, Any] = read_json(args.config) if args.config else {}

    language = (args.language or config.get("language") or "zh").lower()
    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(os.path.dirname(here))
    template_path = args.template
    if not template_path:
        template_path = os.path.join(skill_root, "references", "prompt_template_zh.md" if language.startswith("zh") else "prompt_template_en.md")

    out_text, _meta = render_prompt_markdown(
        input_path=args.input,
        data=data,
        config=config,
        year=year,
        language=language,
        template_path=template_path,
    )
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out_text)
    print(f"Wrote {args.output}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    data = read_json(args.input)
    stats = data.get("stats") or compute_stats(data.get("projects") or [], int(data.get("year") or dt.datetime.utcnow().year), [])
    text = format_stats_markdown(stats)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote {args.output}")
    else:
        sys.stdout.write(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="git_annual_work_summary", description="Collect commits and prepare annual work summary prompts.")
    sub = p.add_subparsers(dest="cmd", required=True)

    collect = sub.add_parser("collect", help="Collect commits from a source")
    collect_sub = collect.add_subparsers(dest="source", required=True)

    gl = collect_sub.add_parser("gitlab", help="Collect from GitLab API")
    gl.add_argument("--year", type=int, required=True)
    gl.add_argument("--url", help="GitLab base URL (e.g. https://gitlab.example.com)")
    gl.add_argument("--token", help="GitLab token (or set env)")
    gl.add_argument("--token-env", default="GITLAB_TOKEN", help="Env var name for GitLab token")
    gl.add_argument("--projects", help="Comma-separated project ids or paths (skip discovery)")
    gl.add_argument("--authors", help="Comma-separated author names/emails/usernames to keep")
    gl.add_argument("--output", required=True)
    gl.add_argument("--env", default=".env", help="Optional env file to load (default: .env)")
    gl.add_argument("--non-interactive", action="store_true")
    gl.set_defaults(func=cmd_collect_gitlab)

    gh = collect_sub.add_parser("github", help="Collect from GitHub API")
    gh.add_argument("--year", type=int, required=True)
    gh.add_argument("--url", help="GitHub base URL (default: https://github.com or GITHUB_URL)")
    gh.add_argument("--api-url", help="GitHub API base URL (default derived from --url)")
    gh.add_argument("--token", help="GitHub token (or set env)")
    gh.add_argument("--token-env", default="GITHUB_TOKEN", help="Env var name for GitHub token")
    gh.add_argument("--user", help="GitHub login to use as 'author' filter in API calls")
    gh.add_argument("--repos", help="Comma-separated owner/repo list")
    gh.add_argument("--discover", action="store_true", help="Discover repos via API and select interactively")
    gh.add_argument("--owner", help="Filter discovered repos by owner login")
    gh.add_argument("--include-forks", action="store_true", help="Include forks when discovering repos")
    gh.add_argument("--authors", help="Comma-separated author names/emails/usernames to keep (post-filter)")
    gh.add_argument("--output", required=True)
    gh.add_argument("--env", default=".env", help="Optional env file to load (default: .env)")
    gh.add_argument("--non-interactive", action="store_true")
    gh.set_defaults(func=cmd_collect_github)

    gg = collect_sub.add_parser("git", help="Collect from local git repos via git log")
    gg.add_argument("--year", type=int, required=True)
    gg.add_argument("--repo", action="append", help="Repo path (repeatable)", required=True)
    gg.add_argument("--authors", help="Comma-separated author names/emails/usernames to keep")
    gg.add_argument("--output", required=True)
    gg.set_defaults(func=cmd_collect_git)

    merge = sub.add_parser("merge", help="Merge multiple collected JSON files")
    merge.add_argument("--output", required=True)
    merge.add_argument("inputs", nargs="+")
    merge.set_defaults(func=cmd_merge)

    rp = sub.add_parser("render-prompt", help="Render a ready-to-paste prompt with stats+themes appendix")
    rp.add_argument("--year", type=int, help="Override year shown in template")
    rp.add_argument("--input", required=True, help="Input commits JSON")
    rp.add_argument("--config", help="Config JSON (core projects, context, language)")
    rp.add_argument("--language", help="zh/en (overrides config)")
    rp.add_argument("--template", help="Prompt template path (optional)")
    rp.add_argument("--output", required=True)
    rp.set_defaults(func=cmd_render_prompt)

    st = sub.add_parser("stats", help="Print or write a Markdown stats summary")
    st.add_argument("--input", required=True, help="Input commits JSON")
    st.add_argument("--output", help="Output Markdown file (default: stdout)")
    st.set_defaults(func=cmd_stats)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
