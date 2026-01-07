from __future__ import annotations

import os
import sys
from typing import Any, Callable, Dict, List


def parse_selection(raw: str, max_index: int) -> List[int]:
    selected = set()
    normalized = (raw or "").replace(" ", ",").replace("\t", ",")
    parts = [p.strip() for p in normalized.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            start_str, end_str = [s.strip() for s in part.split("-", 1)]
            if not start_str.isdigit() or not end_str.isdigit():
                raise ValueError("Ranges must be numeric, e.g. 2-5")
            start = int(start_str)
            end = int(end_str)
            if start < 1 or end < 1 or start > end or end > max_index:
                raise ValueError("Range out of bounds")
            for idx in range(start, end + 1):
                selected.add(idx)
        else:
            if not part.isdigit():
                raise ValueError("Selections must be numeric, e.g. 1,3,5")
            idx = int(part)
            if idx < 1 or idx > max_index:
                raise ValueError("Selection out of bounds")
            selected.add(idx)
    return sorted(selected)


def _can_use_curses() -> bool:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return False
    term = (os.environ.get("TERM") or "").lower()
    return bool(term and term != "dumb")


def _select_items_prompt(items: List[Dict[str, Any]], label_fn: Callable[[Dict[str, Any]], str]) -> List[Dict[str, Any]]:
    print("\nAvailable items:")
    for idx, item in enumerate(items, start=1):
        print(f"{idx:>3}. {label_fn(item)}")

    max_index = len(items)
    while True:
        raw = input("Select by number (e.g. 1 3-5) or 'all' or 'none': ").strip().lower()
        if not raw:
            continue
        if raw in {"all", "a"}:
            return items
        if raw in {"none", "n"}:
            return []
        try:
            indices = parse_selection(raw, max_index)
        except ValueError as exc:
            print(f"Invalid selection: {exc}")
            continue
        return [items[i - 1] for i in indices]


def _select_items_curses(items: List[Dict[str, Any]], label_fn: Callable[[Dict[str, Any]], str]) -> List[Dict[str, Any]]:
    import curses  # stdlib, optional on some platforms

    selected = set()
    cursor = 0
    offset = 0

    def _draw(stdscr) -> None:
        nonlocal offset
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        header = "↑/↓ move  Space toggle  a all  n none  Enter confirm  q quit"
        stdscr.addnstr(0, 0, header, max(0, width - 1))
        view_top = 2
        view_height = max(0, height - view_top - 1)

        if cursor < offset:
            offset = cursor
        if cursor >= offset + view_height:
            offset = max(0, cursor - view_height + 1)

        end = min(len(items), offset + view_height)
        for row, idx in enumerate(range(offset, end), start=view_top):
            mark = "[x]" if idx in selected else "[ ]"
            text = f"{mark} {idx + 1:>3}. {label_fn(items[idx])}"
            if idx == cursor:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addnstr(row, 0, text, max(0, width - 1))
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addnstr(row, 0, text, max(0, width - 1))

        footer = f"Selected: {len(selected)} / {len(items)}"
        stdscr.addnstr(height - 1, 0, footer, max(0, width - 1))
        stdscr.refresh()

    def _loop(stdscr):
        nonlocal cursor
        curses.curs_set(0)
        stdscr.keypad(True)
        while True:
            _draw(stdscr)
            ch = stdscr.getch()
            if ch in (curses.KEY_UP, ord("k")):
                cursor = max(0, cursor - 1)
            elif ch in (curses.KEY_DOWN, ord("j")):
                cursor = min(len(items) - 1, cursor + 1)
            elif ch in (curses.KEY_PPAGE,):
                cursor = max(0, cursor - 10)
            elif ch in (curses.KEY_NPAGE,):
                cursor = min(len(items) - 1, cursor + 10)
            elif ch in (curses.KEY_HOME,):
                cursor = 0
            elif ch in (curses.KEY_END,):
                cursor = len(items) - 1
            elif ch == ord(" "):
                if cursor in selected:
                    selected.remove(cursor)
                else:
                    selected.add(cursor)
            elif ch in (ord("a"), ord("A")):
                selected.update(range(len(items)))
            elif ch in (ord("n"), ord("N")):
                selected.clear()
            elif ch in (10, 13, curses.KEY_ENTER):
                return [items[i] for i in sorted(selected)]
            elif ch in (27, ord("q"), ord("Q")):
                return []

    return curses.wrapper(_loop)


def select_items_interactive(items: List[Dict[str, Any]], label_fn: Callable[[Dict[str, Any]], str]) -> List[Dict[str, Any]]:
    if not items:
        return []
    if _can_use_curses():
        try:
            return _select_items_curses(items, label_fn)
        except Exception:
            # Fallback to prompt selection in environments where curses is broken/unavailable.
            pass
    return _select_items_prompt(items, label_fn)
