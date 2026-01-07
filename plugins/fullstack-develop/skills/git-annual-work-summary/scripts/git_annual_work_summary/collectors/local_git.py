from __future__ import annotations

import datetime as dt
import os
import subprocess
from typing import Any, Dict, List, Tuple

from ..models import commit_to_common


def parse_year_range(year: int) -> Tuple[str, str]:
    since = dt.datetime(year, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    until = dt.datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=dt.timezone.utc)
    return since.isoformat().replace("+00:00", "Z"), until.isoformat().replace("+00:00", "Z")


def _run_git(args: List[str], cwd: str) -> str:
    try:
        proc = subprocess.run(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git is not installed or not on PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(exc.stderr.strip() or "git command failed") from exc
    return proc.stdout


def collect_repo_commits(repo_path: str, year: int, parse_conventional_title) -> Dict[str, Any]:
    repo_path = os.path.abspath(repo_path)
    since, until = parse_year_range(year)

    fmt = "%H%x1f%an%x1f%ae%x1f%aI%x1f%s%x1f%b%x1e"
    out = _run_git(
        ["git", "log", f"--since={since}", f"--until={until}", f"--pretty=format:{fmt}"],
        cwd=repo_path,
    )
    commits: List[Dict[str, Any]] = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split("\x1f")
        if len(parts) < 6:
            continue
        sha, author_name, author_email, author_date, subject, body = parts[:6]
        title = subject.strip()
        msg = (title + "\n\n" + body.strip()).strip()
        commit = {
            "hash": sha,
            "author_name": author_name,
            "author_email": author_email,
            "committed_date": author_date,
            "title": title,
            "message": msg,
        }
        commits.append(commit_to_common(commit, "git", parse_conventional_title))

    remote = None
    try:
        remote = _run_git(["git", "remote", "get-url", "origin"], cwd=repo_path).strip() or None
    except Exception:
        remote = None
    name = os.path.basename(repo_path.rstrip("/"))
    return {
        "platform": "git",
        "name": name,
        "repo_path": repo_path,
        "remote": remote,
        "web_url": remote,
        "commits": commits,
        "commit_count": len(commits),
    }

