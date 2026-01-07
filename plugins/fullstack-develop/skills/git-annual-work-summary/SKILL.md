---
name: git-annual-work-summary
description: Collect and analyze Git commit history from GitHub, GitLab, and/or local git repos; filter by author and year; and generate an annual work summary/述职/自评 report draft and prompt (Markdown) using Conventional Commits semantics and business-impact framing. Use when asked to write 年度工作总结/述职 based on git commits, to summarize contributions by repo/author/year, or to produce a reusable workflow that supports both GitHub and GitLab.
---

# Git Annual Work Summary

## Workflow

1) Collect commits into a unified JSON.
- GitLab: `python3 scripts/git_annual_work_summary.py collect gitlab --year 2025 --url https://gitlab.example.com --output commits.json`
- GitHub: `python3 scripts/git_annual_work_summary.py collect github --year 2025 --url https://github.example.com --repos org/repo1,org/repo2 --output commits.json`
- Local git: `python3 scripts/git_annual_work_summary.py collect git --year 2025 --repo /path/to/repo --output commits.json`

2) (Optional) Merge multiple sources.
- `python3 scripts/git_annual_work_summary.py merge --output commits.all.json commits.gitlab.json commits.github.json`

3) Render a “ready-to-paste” prompt and a compact stats appendix.
- `python3 scripts/git_annual_work_summary.py render-prompt --year 2025 --input commits.all.json --config references/config.example.json --output prompt.ready.md`

4) Generate the report.
- Load `prompt.ready.md` and `commits*.json`, then write the report in first-person with: overview → themes (weighted) → engineering value → role/competency → summary statement.

## Notes

- If Python bytecode cache writes are blocked, prefix commands with `PYTHONPYCACHEPREFIX=.pycache`.
- GitHub/GitLab API collection requires network access and tokens; if network is restricted, collect via `collect git` from local clones as a fallback.

## Inputs to Clarify (ask user)

- Year (or date range), target language (ZH/EN), report audience (manager/committee).
- Author filter: names/emails/usernames; whether to include merge commits/bot commits.
- Core projects to “weight” more, and 1–2 lines of business context per core project.

## Output Contract

- Default to the section structure in `references/prompt_template_zh.md` (or `references/prompt_template_en.md`).
- Avoid “from commits we can see…” phrasing; write as “I…”.
- Prefer impact framing (quality, stability, delivery, efficiency, cost/risk reduction) over raw counts.

## Bundled Resources

- Script: `scripts/git_annual_work_summary.py` (collect/merge/stats/render-prompt; auto theme suggestions + core weighting hints)
- Templates: `references/prompt_template_zh.md`, `references/prompt_template_en.md`
- Config: `references/config.example.json` (supports `core.mode=auto|manual`, project context, weighting, clustering, writing preferences)
