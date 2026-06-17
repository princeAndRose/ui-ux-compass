#!/usr/bin/env python3
"""Read, merge, and write UI/UX Compass project state."""

from __future__ import annotations

import argparse
import json
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_TYPES = {"user-confirmed", "project-fact", "agent-assumption"}

PROJECT_FIELDS = {"name", "summary", "product_type", "target_users", "primary_use_cases", "anti_goals"}
DESIGN_SYSTEM_FIELDS = {"framework", "router", "styling", "ui_library", "tokens", "component_dirs", "notes"}
SOURCE_SECTION_KEYS = {"facts", "confirmed", "assumptions", "defaults"}

DEFAULT_USER_PREFERENCES = {
    "density_default": "medium",
    "visual_tone": ["restrained", "clear", "product-like"],
    "layout_preferences": [],
    "color_preferences": [],
    "component_preferences": [],
    "anti_patterns": [
        "generic SaaS landing page",
        "overused gradients",
        "heavy shadows",
        "meaningless illustrations",
        "equal-weight cards everywhere",
    ],
}


def default_page() -> dict[str, Any]:
    return {
        "route": "",
        "surface_type": "",
        "status": "draft",
        "page_role": "",
        "target_user": "",
        "core_task": "",
        "first_visual_focus": "",
        "information_hierarchy": {"p0": [], "p1": [], "p2": [], "deferred": []},
        "main_cta": "",
        "user_flow": {"entry": "", "decision": "", "action": "", "feedback": "", "error_path": ""},
        "layout_strategy": "",
        "visual_direction": "",
        "interaction_states": [],
        "responsive_strategy": "",
        "accessibility_notes": [],
        "implementation_constraints": [],
        "anti_goals": [],
        "acceptance_criteria": [],
        "open_questions": [],
        "decisions": [],
        "assumptions": [],
        "last_review": None,
    }


def default_state(project_name: str = "") -> dict[str, Any]:
    return {
        "version": 2,
        "project": {
            "facts": {
                "name": project_name,
                "summary": "",
                "product_type": "",
                "target_users": [],
                "primary_use_cases": [],
                "anti_goals": [],
            },
            "confirmed": {},
            "assumptions": {},
        },
        "user_preferences": {
            "defaults": deepcopy(DEFAULT_USER_PREFERENCES),
            "confirmed": {},
            "assumptions": {},
        },
        "design_system": {
            "facts": {
                "framework": "",
                "router": "",
                "styling": "",
                "ui_library": "",
                "tokens": [],
                "component_dirs": [],
                "notes": [],
            },
            "confirmed": {},
            "assumptions": {},
        },
        "pages": {},
    }


def state_path(repo_root: Path) -> Path:
    return repo_root / ".ui-ux-compass" / "state.json"


def load_state(path: Path, project_name: str = "") -> dict[str, Any]:
    if not path.is_file():
        return default_state(project_name)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("state file must contain a JSON object")
    return _deep_merge(default_state(project_name), migrate_state(payload, project_name))


def _deep_merge(base: Any, patch: Any) -> Any:
    if isinstance(base, dict) and isinstance(patch, dict):
        merged = deepcopy(base)
        for key, value in patch.items():
            merged[key] = _deep_merge(merged.get(key), value)
        return merged
    return deepcopy(patch)


def _legacy_values(section: dict[str, Any], fields: set[str]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in section.items() if key in fields}


def _normalize_source_section(section: Any, fields: set[str], default_bucket: str) -> dict[str, Any]:
    normalized = {"facts": {}, "confirmed": {}, "assumptions": {}}
    if not isinstance(section, dict):
        return normalized
    has_source_buckets = any(key in section for key in SOURCE_SECTION_KEYS)
    if has_source_buckets:
        for key in ("facts", "confirmed", "assumptions"):
            if isinstance(section.get(key), dict):
                normalized[key] = deepcopy(section[key])
        legacy = _legacy_values(section, fields)
        if legacy:
            normalized[default_bucket] = _deep_merge(normalized.get(default_bucket, {}), legacy)
        return normalized
    normalized[default_bucket] = _legacy_values(section, fields)
    return normalized


def migrate_state(payload: dict[str, Any], project_name: str = "") -> dict[str, Any]:
    migrated = default_state(project_name)
    migrated["version"] = 2
    migrated["project"] = _deep_merge(
        migrated["project"],
        _normalize_source_section(payload.get("project", {}), PROJECT_FIELDS, "facts"),
    )

    preferences = payload.get("user_preferences", {})
    if isinstance(preferences, dict) and any(key in preferences for key in SOURCE_SECTION_KEYS):
        migrated["user_preferences"] = _deep_merge(migrated["user_preferences"], preferences)
    elif isinstance(preferences, dict):
        migrated["user_preferences"]["confirmed"] = _legacy_values(preferences, set(DEFAULT_USER_PREFERENCES))

    migrated["design_system"] = _deep_merge(
        migrated["design_system"],
        _normalize_source_section(payload.get("design_system", {}), DESIGN_SYSTEM_FIELDS, "facts"),
    )

    pages = payload.get("pages", {})
    if isinstance(pages, dict):
        migrated["pages"] = deepcopy(pages)
    return migrated


def _append_sourced(items: list[Any], source: str, target: list[dict[str, str]]) -> None:
    for item in items:
        if isinstance(item, dict):
            text = str(item.get("text", "")).strip()
            item_source = str(item.get("source", source)).strip() or source
        else:
            text = str(item).strip()
            item_source = source
        if text:
            entry = {"source": item_source, "text": text}
            if entry not in target:
                target.append(entry)


def _normalize_page_keys(page: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(page)
    if "role" in normalized and "page_role" not in normalized:
        normalized["page_role"] = normalized["role"]
    normalized.pop("role", None)
    return normalized


def _merge_source_aware_section(section: dict[str, Any], patch_section: dict[str, Any], source: str, section_name: str) -> dict[str, Any]:
    merged = deepcopy(section)
    if section_name in {"project", "design_system"}:
        allowed_buckets = {
            "project-fact": {"facts"},
            "user-confirmed": {"confirmed"},
            "agent-assumption": {"assumptions"},
        }[source]
    elif section_name == "user_preferences":
        allowed_buckets = {
            "user-confirmed": {"confirmed"},
            "project-fact": {"assumptions"},
            "agent-assumption": {"assumptions"},
        }[source]
    else:
        allowed_buckets = {"assumptions"}

    for bucket in SOURCE_SECTION_KEYS:
        if bucket not in patch_section:
            continue
        value = patch_section.get(bucket)
        if not value:
            continue
        if bucket not in allowed_buckets:
            raise ValueError(f"{source} patch cannot write {section_name}.{bucket}")
        if not isinstance(value, dict):
            raise ValueError(f"patch.{section_name}.{bucket} must be an object")
        merged[bucket] = _deep_merge(merged.get(bucket, {}), value)

    if section_name == "project":
        if source == "project-fact":
            bucket = "facts"
        elif source == "user-confirmed":
            bucket = "confirmed"
        else:
            bucket = "assumptions"
    elif section_name == "design_system":
        if source == "project-fact":
            bucket = "facts"
        elif source == "user-confirmed":
            bucket = "confirmed"
        else:
            bucket = "assumptions"
    elif section_name == "user_preferences":
        bucket = "confirmed" if source == "user-confirmed" else "assumptions"
    else:
        bucket = "assumptions"
    values = {key: value for key, value in patch_section.items() if key not in SOURCE_SECTION_KEYS}
    if values:
        merged[bucket] = _deep_merge(merged.get(bucket, {}), values)
    return merged


def _append_assumed_fields(page_patch: dict[str, Any], source: str, assumptions: list[dict[str, str]]) -> None:
    for key, value in page_patch.items():
        if key in {"decisions", "assumptions", "id", "page_id", "source"}:
            continue
        if value in (None, "", [], {}):
            continue
        text = f"{key}: {json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value}"
        _append_sourced([text], source, assumptions)


def merge_patch(state: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    source = patch.get("source")
    if source not in SOURCE_TYPES:
        raise ValueError("patch must include source: user-confirmed, project-fact, or agent-assumption")

    merged = migrate_state(state)
    for top_key in ("project", "user_preferences", "design_system"):
        if isinstance(patch.get(top_key), dict):
            merged[top_key] = _merge_source_aware_section(merged.get(top_key, {}), patch[top_key], source, top_key)

    pages = patch.get("pages", {})
    if pages is not None and not isinstance(pages, dict):
        raise ValueError("patch.pages must be an object")

    for page_id, page_patch in pages.items():
        if not isinstance(page_patch, dict):
            raise ValueError(f"patch page {page_id} must be an object")
        page_patch = _normalize_page_keys(page_patch)
        existing_page = _normalize_page_keys(merged["pages"].get(page_id, {}))
        page = _deep_merge(default_page(), existing_page)
        decisions = list(page.get("decisions", []))
        assumptions = list(page.get("assumptions", []))
        if source in {"user-confirmed", "project-fact"}:
            for key, value in page_patch.items():
                if key in {"decisions", "assumptions"}:
                    continue
                page[key] = _deep_merge(page.get(key), value)
            _append_sourced(page_patch.get("decisions", []), source, decisions)
            _append_sourced(page_patch.get("assumptions", []), "agent-assumption", assumptions)
        else:
            _append_assumed_fields(page_patch, source, assumptions)
            _append_sourced(page_patch.get("decisions", []), source, assumptions)
            _append_sourced(page_patch.get("assumptions", []), source, assumptions)
        page["decisions"] = decisions
        page["assumptions"] = assumptions
        merged["pages"][page_id] = page

    merged["version"] = 2
    return merged


def write_state(path: Path, state: dict[str, Any], create: bool = False) -> None:
    if not path.parent.exists():
        if not create:
            raise FileNotFoundError("state directory does not exist; rerun with --create to create it")
        path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        shutil.copy2(path, path.with_suffix(f".{stamp}.bak"))
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state-file")
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("get")
    merge_parser = sub.add_parser("merge")
    merge_parser.add_argument("--patch", required=True)
    add_page_parser = sub.add_parser("add-page")
    add_page_parser.add_argument("--page", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root)
    path = Path(args.state_file) if args.state_file else state_path(root)
    state = load_state(path, root.name)

    if args.command == "get":
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return 0

    if args.command == "merge":
        patch = json.loads(Path(args.patch).read_text(encoding="utf-8"))
        state = merge_patch(state, patch)
        write_state(path, state, args.create)
        print(json.dumps({"status": "updated", "path": str(path)}, indent=2))
        return 0

    if args.command == "add-page":
        page = json.loads(Path(args.page).read_text(encoding="utf-8"))
        page_id = page.get("id") or page.get("page_id")
        if not isinstance(page_id, str) or not page_id.strip():
            raise ValueError("page must include id or page_id")
        patch = {"source": page.get("source", "agent-assumption"), "pages": {page_id: page}}
        state = merge_patch(state, patch)
        write_state(path, state, args.create)
        print(json.dumps({"status": "updated", "path": str(path), "page_id": page_id}, indent=2))
        return 0

    raise ValueError(f"unknown command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
