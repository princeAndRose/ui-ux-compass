#!/usr/bin/env python3
"""Initialize optional UI/UX Compass runtime state."""

from __future__ import annotations

import json
import os
from pathlib import Path


DEFAULT_RUNTIME_STATE = {
    "version": 1,
    "user_preferences": {
        "density_default": "medium",
        "visual_tone": ["restrained", "clear", "product-like"],
    },
    "recent_projects": {},
}


def main() -> int:
    data_dir = os.environ.get("PLUGIN_DATA")
    if not data_dir:
        print(json.dumps({"status": "skipped", "reason": "PLUGIN_DATA is not set"}))
        return 0
    root = Path(data_dir)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "ui-ux-compass-state.json"
    if not path.exists():
        path.write_text(json.dumps(DEFAULT_RUNTIME_STATE, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ready", "state": str(path)}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}))
        raise SystemExit(1)
