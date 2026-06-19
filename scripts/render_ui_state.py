#!/usr/bin/env python3
"""Render UI/UX Compass state as Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.cli_io import enable_utf8_output
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from cli_io import enable_utf8_output

try:
    from scripts.update_ui_state import migrate_state
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from update_ui_state import migrate_state


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


def _dict_lines(values: dict[str, Any]) -> list[str]:
    lines = []
    for key, value in values.items():
        if value in (None, "", [], {}):
            continue
        if isinstance(value, list):
            rendered = ", ".join(str(item) for item in value) or "Unknown"
        else:
            rendered = str(value)
        lines.append(f"- {key}: {rendered}")
    return lines or ["- None"]


def _merged_preferences(preferences: dict[str, Any]) -> dict[str, Any]:
    merged = dict(preferences.get("defaults", {}))
    merged.update(preferences.get("confirmed", {}))
    return merged


def render_state(state: dict[str, Any]) -> str:
    state = migrate_state(state)
    project = state.get("project", {})
    project_facts = project.get("facts", {})
    project_confirmed = project.get("confirmed", {})
    project_assumptions = project.get("assumptions", {})
    preferences = state.get("user_preferences", {})
    confirmed_preferences = preferences.get("confirmed", {})
    assumed_preferences = preferences.get("assumptions", {})
    preference_view = _merged_preferences(preferences)
    design_system = state.get("design_system", {})
    design_facts = design_system.get("facts", {})
    design_confirmed = design_system.get("confirmed", {})
    design_assumptions = design_system.get("assumptions", {})
    pages = state.get("pages", {})

    lines = [
        "## UI Intent Summary",
        "",
        "Project facts:",
        *_dict_lines(project_facts),
        "",
        "Confirmed project decisions:",
        *_dict_lines(project_confirmed),
        "",
        "Project assumptions:",
        *_dict_lines(project_assumptions),
        "",
        "Confirmed preferences:",
        *_dict_lines(confirmed_preferences),
        "",
        "Preference defaults:",
        f"- Density default: {preference_view.get('density_default', 'medium')}",
        f"- Visual tone: {', '.join(preference_view.get('visual_tone', [])) or 'Unknown'}",
        "",
        "Preference assumptions:",
        *_dict_lines(assumed_preferences),
        "",
        "Design system facts:",
        *_dict_lines(design_facts),
        "",
        "Confirmed design system decisions:",
        *_dict_lines(design_confirmed),
        "",
        "Design system assumptions:",
        *_dict_lines(design_assumptions),
        "",
        "Pages:",
    ]

    if not pages:
        lines.append("- None")
    for page_id, page in pages.items():
        lines.extend([
            f"- {page_id}: {page.get('route', '') or 'No route'}",
            f"  - Status: {page.get('status', 'draft')}",
            f"  - Role: {page.get('page_role', '') or page.get('role', '') or 'Unknown'}",
            f"  - Target user: {page.get('target_user', '') or 'Unknown'}",
            f"  - Core task: {page.get('core_task', '') or 'Unknown'}",
            "  - Confirmed decisions:",
            "\n".join(f"    {line}" for line in _list(page.get("decisions", [])).splitlines()),
            "  - Agent assumptions:",
            "\n".join(f"    {line}" for line in _list(page.get("assumptions", [])).splitlines()),
            "  - Open questions:",
            "\n".join(f"    {line}" for line in _list(page.get("open_questions", [])).splitlines()),
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
    enable_utf8_output()
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
