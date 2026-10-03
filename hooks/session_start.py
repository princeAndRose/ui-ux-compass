#!/usr/bin/env python3
"""Initialize optional UI/UX Compass runtime state."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

def main() -> int:
    # An optional runtime cache is never project context or a source of preferences.
    # Import from the installed plugin, independently of the caller's working directory.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.update_ui_state import default_state

    data_dir = os.environ.get("PLUGIN_DATA")
    if not data_dir:
        return 0
    root = Path(data_dir)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "ui-ux-compass-state.json"
    try:
        # Exclusive creation also protects an existing cache during simultaneous starts.
        with path.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(default_state(), indent=2, ensure_ascii=False) + "\n")
    except FileExistsError:
        pass
    return 0


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"UI/UX Compass optional runtime initialization skipped: {exc}", file=sys.stderr)
    # SessionStart's supported common output shape; never inject cache content.
    print(json.dumps({"continue": True}))
