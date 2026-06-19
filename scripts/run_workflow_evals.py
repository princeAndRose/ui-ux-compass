#!/usr/bin/env python3
"""Run workflow fixtures for UI/UX Compass."""

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
    from scripts.detect_ui_surface import detect_ui_surface
    from scripts.validate_ui_intent import validate_ui_intent
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from detect_ui_surface import detect_ui_surface
    from validate_ui_intent import validate_ui_intent


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _check_equal(actual: Any, expected: Any, label: str, failures: list[str]) -> None:
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


def _contains_all(values: list[str], expected: list[str], label: str, failures: list[str]) -> None:
    haystack = "\n".join(values)
    for item in expected:
        if item not in haystack:
            failures.append(f"{label}: missing {item!r}")


def _evaluate_fixture(path: Path, repo_root: Path) -> dict[str, Any]:
    fixture = _load_json(path)
    failures: list[str] = []
    result: dict[str, Any] = {
        "id": fixture.get("id", path.stem),
        "description": fixture.get("description", ""),
        "fixture": str(path),
    }

    expected_route = fixture.get("expected_route")
    expected_validation = fixture.get("expected_validation")
    if not expected_route and not expected_validation:
        failures.append("fixture must include expected_route or expected_validation")

    if expected_route:
        if not str(fixture.get("message", "")).strip():
            failures.append("fixture with expected_route must include message")
        detected = detect_ui_surface(repo_root, str(fixture.get("message", "")))
        result["route"] = detected
        for key, expected in expected_route.items():
            _check_equal(detected.get(key), expected, f"route.{key}", failures)

    if "spec" in fixture:
        validation = validate_ui_intent(fixture["spec"])
        result["validation"] = validation
        if expected_validation:
            for key in ["status", "blocking", "recommended_next"]:
                if key in expected_validation:
                    _check_equal(validation.get(key), expected_validation[key], f"validation.{key}", failures)
            if "weak_min" in expected_validation and len(validation.get("weak", [])) < int(expected_validation["weak_min"]):
                failures.append(
                    f"validation.weak_min: expected at least {expected_validation['weak_min']}, "
                    f"got {len(validation.get('weak', []))}"
                )
            if "recommended_questions_min" in expected_validation and len(validation.get("recommended_questions", [])) < int(expected_validation["recommended_questions_min"]):
                failures.append(
                    "validation.recommended_questions_min: expected at least "
                    f"{expected_validation['recommended_questions_min']}, got {len(validation.get('recommended_questions', []))}"
                )
            _contains_all(
                validation.get("blocking_reasons", []),
                expected_validation.get("blocking_reasons_contains", []),
                "validation.blocking_reasons",
                failures,
            )
            _contains_all(
                validation.get("weak", []),
                expected_validation.get("weak_contains", []),
                "validation.weak",
                failures,
            )
    elif expected_validation:
        failures.append("fixture with expected_validation must include spec")

    result["passed"] = not failures
    result["failures"] = failures
    return result


def run_workflow_evals(fixtures_dir: Path | str, repo_root: Path | str) -> dict[str, Any]:
    root = Path(repo_root)
    directory = Path(fixtures_dir)
    if not directory.is_dir():
        return {
            "total": 0,
            "passed_count": 0,
            "passed": False,
            "failures": {"_fixtures": [f"fixtures directory does not exist: {directory}"]},
            "cases": [],
        }
    fixture_paths = sorted(directory.glob("*.json"))
    if not fixture_paths:
        return {
            "total": 0,
            "passed_count": 0,
            "passed": False,
            "failures": {"_fixtures": [f"no workflow fixtures found in {directory}"]},
            "cases": [],
        }
    cases = [_evaluate_fixture(path, root) for path in fixture_paths]
    failures = {case["id"]: case["failures"] for case in cases if not case["passed"]}
    return {
        "total": len(cases),
        "passed_count": sum(1 for case in cases if case["passed"]),
        "passed": not failures,
        "failures": failures,
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", default="evals/workflows")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = run_workflow_evals(Path(args.fixtures), Path(args.repo_root))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    enable_utf8_output()
    raise SystemExit(main())
