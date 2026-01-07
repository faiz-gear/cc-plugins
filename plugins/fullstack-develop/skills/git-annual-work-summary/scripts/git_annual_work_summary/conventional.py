from __future__ import annotations

import re
from typing import Any, Dict


CONVENTIONAL_RE = re.compile(
    r"^(?P<type>[a-zA-Z][a-zA-Z0-9-]*)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?:\s+(?P<desc>.+)$"
)


def parse_conventional_title(title: str) -> Dict[str, Any]:
    raw = (title or "").strip()
    match = CONVENTIONAL_RE.match(raw)
    if not match:
        return {"is_conventional": False, "raw": raw}
    return {
        "is_conventional": True,
        "type": (match.group("type") or "").lower(),
        "scope": match.group("scope") or None,
        "breaking": bool(match.group("breaking")),
        "description": match.group("desc") or "",
        "raw": raw,
    }

