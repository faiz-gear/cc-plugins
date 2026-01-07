from __future__ import annotations

import datetime as dt
import json
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def normalize_base_url(raw: str) -> str:
    url = (raw or "").strip()
    if not url:
        return ""
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url.rstrip("/")


def load_env_file(path: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue
                if len(value) >= 2 and value[0] == value[-1] and value.startswith(("'", '"')):
                    value = value[1:-1]
                values[key] = value
    except FileNotFoundError:
        return {}
    return values


def parse_csv(value: Optional[str]) -> List[str]:
    if not value:
        return []
    items: List[str] = []
    for part in value.split(","):
        part = part.strip()
        if part:
            items.append(part)
    return items


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise RuntimeError("Expected a JSON object at root")
    return value


def write_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def render_template(template_text: str, mapping: Dict[str, str]) -> str:
    out = template_text
    for k, v in mapping.items():
        out = out.replace("{{" + k + "}}", v)
    return out

