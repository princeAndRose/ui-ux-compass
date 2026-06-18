#!/usr/bin/env python3
"""Validate whether a UI Intent Spec is ready for implementation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.cli_io import enable_utf8_output
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from cli_io import enable_utf8_output


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

UNKNOWN_MARKERS = {
    "?",
    "n/a",
    "na",
    "not sure",
    "tbd",
    "todo",
    "unknown",
    "不确定",
    "待定",
    "未知",
}

GENERIC_FILLER = {
    "beautiful",
    "clean",
    "clean and modern",
    "focused tooling",
    "good",
    "intuitive",
    "modern",
    "nice",
    "polished",
    "premium",
    "simple",
    "standard",
    "user friendly",
    "user-friendly",
}

REQUIRED_USER_FLOW_PARTS = ["entry", "action", "feedback"]
REQUIRED_VISUAL_DIRECTION_PARTS = ["density", "tone", "structure"]
REQUIRED_STATE_PARTS = ["loading", "empty", "error"]

QUESTION_HINTS = {
    "page_role": "What role should this surface play in the product?",
    "target_user": "Who is the primary user for this surface?",
    "core_task": "What is the main task the user must complete here?",
    "first_visual_focus": "What should the user notice first?",
    "information_hierarchy.p0": "What P0 information must be visually dominant?",
    "main_cta": "What is the primary action, or is this intentionally read-only?",
    "user_flow": "How does the user enter, act, and receive feedback in this flow?",
    "layout_strategy": "Which layout archetype fits the task and density?",
    "visual_direction": "What density, tone, and structure should guide the visual direction?",
    "interaction_states": "Which loading, empty, and error states are required or explicitly not applicable?",
    "acceptance_criteria": "What two concrete checks will prove the UI is done?",
}


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and not _is_unknown(value)
    if isinstance(value, list):
        return any(_present(item) for item in value)
    if isinstance(value, dict):
        return any(_present(item) for item in value.values())
    return True


def _normalize_text(value: Any) -> str:
    return str(value).strip().lower().replace("_", " ").replace("-", " ")


def _is_unknown(value: Any) -> bool:
    if isinstance(value, str):
        normalized = _normalize_text(value)
        return normalized in UNKNOWN_MARKERS
    if isinstance(value, list):
        return bool(value) and all(_is_unknown(item) for item in value)
    if isinstance(value, dict):
        return bool(value) and all(_is_unknown(item) for item in value.values())
    return False


def _is_generic_text(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    normalized = _normalize_text(value)
    return normalized in GENERIC_FILLER


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict_has_present(value: Any, key: str) -> bool:
    return isinstance(value, dict) and _present(value.get(key))


def _main_cta_can_be_empty(spec: dict[str, Any]) -> bool:
    context = " ".join(str(spec.get(field, "")) for field in ["page_role", "core_task", "layout_strategy"]).lower()
    context_allows_no_action = any(term in context for term in ["read-only", "read only", "readonly", "report", "analytics", "monitor"])
    justification = str(spec.get("main_cta_justification", "") or spec.get("primary_action_justification", "")).lower()
    explicit_no_action = any(
        term in justification
        for term in ["read-only", "read only", "readonly", "no primary", "no cta", "no action", "not applicable"]
    )
    return context_allows_no_action and (spec.get("no_primary_action") is True or explicit_no_action)


def _missing_required_fields(spec: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_FIELDS:
        if field == "main_cta" and _main_cta_can_be_empty(spec):
            continue
        if not _present(spec.get(field)):
            missing.append(field)
    return missing


def _information_hierarchy_issues(spec: dict[str, Any]) -> tuple[list[str], list[str]]:
    weak: list[str] = []
    blocking: list[str] = []
    hierarchy = spec.get("information_hierarchy")
    if not isinstance(hierarchy, dict):
        blocking.append("information_hierarchy must define p0/p1/p2 priorities.")
        return weak, blocking
    if not _present(hierarchy.get("p0")):
        blocking.append("information_hierarchy.p0 must be non-empty.")
    return weak, blocking


def _user_flow_issues(spec: dict[str, Any]) -> list[str]:
    flow = spec.get("user_flow")
    if not isinstance(flow, dict):
        return ["user_flow must include entry, action, and feedback."]
    return [f"user_flow.{part} is missing." for part in REQUIRED_USER_FLOW_PARTS if not _present(flow.get(part))]


def _visual_direction_issues(spec: dict[str, Any]) -> list[str]:
    direction = spec.get("visual_direction")
    if isinstance(direction, dict):
        return [
            f"visual_direction.{part} is missing."
            for part in REQUIRED_VISUAL_DIRECTION_PARTS
            if not _present(direction.get(part)) or _is_generic_text(direction.get(part))
        ]
    if not _present(direction):
        return ["visual_direction must include density, tone, and structure."]
    return ["visual_direction should name density, tone, and structure instead of a single generic phrase."]


def _state_has_coverage(states: Any, state: str, justifications: Any) -> bool:
    if isinstance(states, list):
        normalized = {_normalize_text(item) for item in states if isinstance(item, str)}
        return state in normalized
    if isinstance(states, dict):
        if _present(states.get(state)):
            return True
        value = states.get(f"{state}_justification")
        if _present(value):
            return True
    return isinstance(justifications, dict) and _present(justifications.get(state))


def _state_issues(spec: dict[str, Any]) -> list[str]:
    states = spec.get("interaction_states")
    justifications = spec.get("state_justifications")
    return [
        f"interaction_states.{state} is missing or lacks a not-applicable justification."
        for state in REQUIRED_STATE_PARTS
        if not _state_has_coverage(states, state, justifications)
    ]


def _acceptance_criteria_issues(spec: dict[str, Any]) -> list[str]:
    criteria = [
        item
        for item in _as_list(spec.get("acceptance_criteria"))
        if _present(item) and not _is_generic_text(item) and len(str(item).strip()) >= 20
    ]
    if len(criteria) < 2:
        return ["acceptance_criteria must include at least two concrete checks."]
    return []


def _layout_strategy_issues(spec: dict[str, Any]) -> list[str]:
    strategy = spec.get("layout_strategy")
    if _present(strategy) and _is_generic_text(strategy):
        return ["layout_strategy is too generic to guide implementation."]
    return []


def _recommended_questions(missing: list[str], weak: list[str], blocking_reasons: list[str]) -> list[str]:
    questions: list[str] = []
    issue_text = " ".join([*missing, *weak, *blocking_reasons]).lower()
    for key, question in QUESTION_HINTS.items():
        if key in issue_text and question not in questions:
            questions.append(question)
    return questions[:5]


def validate_ui_intent(spec: dict[str, Any]) -> dict[str, Any]:
    missing = _missing_required_fields(spec)
    weak: list[str] = []
    blocking_reasons: list[str] = []
    hierarchy_weak, hierarchy_blocking = _information_hierarchy_issues(spec)
    weak.extend(hierarchy_weak)
    blocking_reasons.extend(hierarchy_blocking)
    weak.extend(_user_flow_issues(spec))
    weak.extend(_visual_direction_issues(spec))
    weak.extend(_state_issues(spec))
    weak.extend(_acceptance_criteria_issues(spec))
    weak.extend(_layout_strategy_issues(spec))

    for field in BLOCKING_FIELDS:
        if field == "main_cta" and _main_cta_can_be_empty(spec):
            continue
        if field in missing:
            blocking_reasons.append(f"{field} is required before implementation.")
        elif _is_unknown(spec.get(field)):
            blocking_reasons.append(f"{field} is explicitly unknown.")

    present_count = len(REQUIRED_FIELDS) - len(missing)
    weak_penalty = min(len(weak), len(REQUIRED_FIELDS)) * 0.03
    score = round(max(0, (present_count / len(REQUIRED_FIELDS)) - weak_penalty), 2)
    blocking = bool(blocking_reasons)
    if not missing and not weak and not blocking:
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
        "weak": weak,
        "blocking": blocking,
        "blocking_reasons": blocking_reasons,
        "recommended_questions": _recommended_questions(missing, weak, blocking_reasons),
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
    enable_utf8_output()
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
