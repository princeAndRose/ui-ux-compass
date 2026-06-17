#!/usr/bin/env python3
"""Summarize UI intent from project state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from scripts.render_ui_state import render_state
    from scripts.update_ui_state import load_state, state_path
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from render_ui_state import render_state
    from update_ui_state import load_state, state_path


def summarize_ui_intent(repo_root: Path | str, state_file: Path | str | None = None) -> str:
    root = Path(repo_root)
    path = Path(state_file) if state_file else state_path(root)
    return render_state(load_state(path, root.name))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state-file")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    summary = summarize_ui_intent(Path(args.repo_root), args.state_file)
    if args.as_json:
        print(json.dumps({"summary": summary}, indent=2, ensure_ascii=False))
    else:
        print(summary, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
