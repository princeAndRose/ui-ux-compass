#!/usr/bin/env python3
"""Run trigger routing evals for UI/UX Compass."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

try:
    from scripts.detect_ui_surface import detect_ui_surface
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from detect_ui_surface import detect_ui_surface


QUESTION_MODES = {
    "ask-one-question",
    "assumptions-gate",
    "mini-brief",
    "full-brief",
    "review",
    "visual-direction",
}

GATE_MODES = {
    "ask-one-question",
    "assumptions-gate",
    "mini-brief",
    "full-brief",
    "review",
    "acceptance",
}


def _bool(value: str) -> bool:
    return value.strip().lower() == "true"


def _mode_matches(expected_mode: str, predicted_mode: str) -> bool:
    allowed = {part.strip() for part in expected_mode.split(" or ") if part.strip()}
    return predicted_mode in allowed


def _load_expectations(csv_path: Path) -> dict[str, Any]:
    path = csv_path.parent / "expected-routing.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _evaluate_thresholds(metrics: dict[str, Any], thresholds: dict[str, Any]) -> dict[str, str]:
    failures: dict[str, str] = {}
    if not thresholds:
        return failures

    minimum_checks = {
        "risk_within_one_rate": "risk_level_within_one",
        "mode_accuracy": "mode_accuracy",
        "subjective_feedback_to_review_rate": "subjective_feedback_to_review",
    }
    for metric_name, threshold_name in minimum_checks.items():
        if threshold_name not in thresholds:
            continue
        actual = float(metrics[metric_name])
        expected = float(thresholds[threshold_name])
        if actual < expected:
            failures[metric_name] = f"{actual} < {expected}"

    maximum_checks = {
        "false_question_rate": "false_question_rate_max",
        "risk_3_or_4_without_gate": "risk_3_or_4_without_spec_or_assumptions_gate",
    }
    for metric_name, threshold_name in maximum_checks.items():
        if threshold_name not in thresholds:
            continue
        actual = float(metrics[metric_name])
        expected = float(thresholds[threshold_name])
        if actual > expected:
            failures[metric_name] = f"{actual} > {expected}"
    return failures


def run_trigger_evals(csv_path: Path | str, repo_root: Path | str) -> dict[str, Any]:
    path = Path(csv_path)
    root = Path(repo_root)
    expectations = _load_expectations(path)
    rows: list[dict[str, Any]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            expected_risk = int(row["expected_risk"])
            expected_mode = row["expected_mode"]
            expected_should_ask = _bool(row["should_ask"])
            detected = detect_ui_surface(root, row["prompt"])
            predicted_risk = int(detected["risk_level"])
            predicted_mode = str(detected["recommended_mode"])
            predicted_should_ask = predicted_mode in QUESTION_MODES
            # Ground truth for "is this subjective UI feedback" comes from the
            # human-labeled expected mode, not from re-matching the detector's own
            # keyword list -- otherwise the eval would quietly grade the detector
            # against itself.
            subjective = expected_mode == "review"
            rows.append({
                "id": row["id"],
                "prompt": row["prompt"],
                "expected_risk": expected_risk,
                "predicted_risk": predicted_risk,
                "expected_mode": expected_mode,
                "predicted_mode": predicted_mode,
                "expected_should_ask": expected_should_ask,
                "predicted_should_ask": predicted_should_ask,
                "mode_matches": _mode_matches(expected_mode, predicted_mode),
                "risk_within_one": abs(expected_risk - predicted_risk) <= 1,
                "false_question": not expected_should_ask and predicted_should_ask,
                "risk_3_or_4_without_gate": expected_risk >= 3 and predicted_mode not in GATE_MODES,
                "subjective": subjective,
                "subjective_to_review": (not subjective) or predicted_mode == "review",
            })

    total = len(rows) or 1
    non_ask_total = sum(1 for row in rows if not row["expected_should_ask"]) or 1
    subjective_total = sum(1 for row in rows if row["subjective"]) or 1
    false_question_count = sum(1 for row in rows if row["false_question"])
    metrics = {
        "total": len(rows),
        "risk_within_one_rate": round(sum(1 for row in rows if row["risk_within_one"]) / total, 3),
        "mode_accuracy": round(sum(1 for row in rows if row["mode_matches"]) / total, 3),
        "false_question_rate": round(false_question_count / non_ask_total, 3),
        "risk_3_or_4_without_gate": sum(1 for row in rows if row["risk_3_or_4_without_gate"]),
        "subjective_feedback_to_review_rate": round(
            sum(1 for row in rows if row["subjective"] and row["subjective_to_review"]) / subjective_total,
            3,
        ),
    }
    thresholds = expectations.get("success_metrics", {})
    failures = _evaluate_thresholds(metrics, thresholds)
    result = {
        **metrics,
        "expectations": thresholds,
        "passed": not failures,
        "failures": failures,
        "cases": rows,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default="evals/trigger-cases.csv")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = run_trigger_evals(Path(args.cases), Path(args.repo_root))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
