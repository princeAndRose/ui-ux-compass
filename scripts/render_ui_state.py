#!/usr/bin/env python3
"""Render UI/UX Compass state as Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _list(values: list[Any]) -> str:
    if not values:
        return "- None"
    lines = []
    for value in values:
        if isinstance(value, dict):
            source = value.get("source", "unknown")
            text = value.get("text", "")
            lines.append(f"- [{source}] {text}")
        else:
            lines.append(f"- {value}")
    return "\n".join(lines)


def render_state(state: dict[str, Any]) -> str:
    project = state.get("project", {})
    preferences = state.get("user_preferences", {})
    design_system = state.get("design_system", {})
    pages = state.get("pages", {})

    lines = [
        "## UI Intent Summary",
        "",
        "Project:",
        f"- Name: {project.get('name', '') or 'Unknown'}",
        f"- Summary: {project.get('summary', '') or 'Unknown'}",
        f"- Product type: {project.get('product_type', '') or 'Unknown'}",
        "",
        "User preferences:",
        f"- Density default: {preferences.get('density_default', 'medium')}",
        f"- Visual tone: {', '.join(preferences.get('visual_tone', [])) or 'Unknown'}",
        "",
        "Design system:",
        f"- Framework: {design_system.get('framework', '') or 'Unknown'}",
        f"- Router: {design_system.get('router', '') or 'Unknown'}",
        f"- Styling: {design_system.get('styling', '') or 'Unknown'}",
        "",
        "Pages:",
    ]

    if not pages:
        lines.append("- None")
    for page_id, page in pages.items():
        lines.extend([
            f"- {page_id}: {page.get('route', '') or 'No route'}",
            f"  - Status: {page.get('status', 'draft')}",
            f"  - Role: {page.get('role', '') or 'Unknown'}",
            f"  - Target user: {page.get('target_user', '') or 'Unknown'}",
            f"  - Core task: {page.get('core_task', '') or 'Unknown'}",
            "  - Decisions:",
            "\n".join(f"    {line}" for line in _list(page.get("decisions", [])).splitlines()),
            "  - Assumptions:",
            "\n".join(f"    {line}" for line in _list(page.get("assumptions", [])).splitlines()),
        ])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-file", required=True)
    args = parser.parse_args()
    state = json.loads(Path(args.state_file).read_text(encoding="utf-8"))
    print(render_state(state), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
