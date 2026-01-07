#!/usr/bin/env python3
import os
import sys


def main() -> int:
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, scripts_dir)
    from git_annual_work_summary.cli import main as cli_main  # noqa: WPS433

    return int(cli_main())


if __name__ == "__main__":
    raise SystemExit(main())
