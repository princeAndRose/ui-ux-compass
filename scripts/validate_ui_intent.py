#!/usr/bin/env python3
"""Validate whether a UI Intent Spec is ready for implementation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "page_role",
    "target_user",
    "core_task",
    "first_visual_focus",
    "information_hierarchy",
    "main_cta",
    "user_flow",
    "layout_strategy",
    "visual_direction",
    "interaction_states",
    "implementation_constraints",
    "acceptance_criteria",
]

BLOCKING_FIELDS = {
    "page_role",
    "target_user",
    "core_task",
    "information_hierarchy",
    "main_cta",
    "layout_strategy",
}


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return any(_present(item) for item in value.values())
    return True


def validate_ui_intent(spec: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in REQUIRED_FIELDS if not _present(spec.get(field))]
    present_count = len(REQUIRED_FIELDS) - len(missing)
    score = round(present_count / len(REQUIRED_FIELDS), 2)
    blocking = any(field in BLOCKING_FIELDS for field in missing)
    if not missing:
        status = "pass"
        recommended_next = "implementation"
    elif blocking:
        status = "blocked"
        recommended_next = "ui-ux-brief"
    else:
        status = "pass-with-assumptions"
        recommended_next = "implementation-gate"
    return {
        "status": status,
        "score": score,
        "missing": missing,
        "blocking": blocking,
        "recommended_next": recommended_next,
    }


def _read_spec(path: str | None) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("UI intent input must be a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = validate_ui_intent(_read_spec(args.file))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
