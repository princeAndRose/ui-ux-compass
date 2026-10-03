#!/usr/bin/env python3
"""Package controlled UI experiments and audit evidence-backed results (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

KINDS = {"hard", "heuristic", "style", "process"}
EVIDENCE = {"interaction", "screenshot", "trace", "code", "document"}
STATUSES = {"pass", "fail", "unverified", "not_applicable"}
PUBLIC = ("id", "title", "category", "design_system", "source_urls", "brief", "context", "constraints", "required_artifacts")
SAFE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def validate_scenario(case: dict) -> list[str]:
    errors = []
    for key in ("id", "title", "category", "design_system", "brief", "context", "family"):
        if not isinstance(case.get(key), str) or not case[key].strip():
            errors.append(f"{key}: expected nonempty string")
    if not SAFE_ID.fullmatch(str(case.get("id", ""))):
        errors.append("id: use letters, numbers, underscores or hyphens")
    for key in ("source_urls", "constraints", "required_artifacts"):
        values = case.get(key)
        if not isinstance(values, list) or (key == "required_artifacts" and not values) or any(not isinstance(v, str) or not v.strip() for v in values):
            errors.append(f"{key}: expected string array (required_artifacts must be nonempty)")
    if isinstance(case.get("source_urls"), list):
        for url in case["source_urls"]:
            if not isinstance(url, str) or urlparse(url).scheme != "https" or not urlparse(url).netloc:
                errors.append("source_urls: expected absolute HTTPS URLs")
    if case.get("split") not in {"development", "holdout"}:
        errors.append("split: expected development or holdout")
    if not isinstance(case.get("user_facts"), dict):
        errors.append("user_facts: expected object")
    checks = case.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks: expected nonempty array")
        return errors
    ids = []
    for i, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"checks[{i}]: expected object")
            continue
        if not isinstance(check.get("id"), str) or not SAFE_ID.fullmatch(check["id"]):
            errors.append(f"checks[{i}].id: invalid")
        ids.append(check.get("id"))
        if check.get("kind") not in KINDS or check.get("evidence") not in EVIDENCE:
            errors.append(f"checks[{i}]: invalid kind/evidence")
        if check.get("kind") == "process" and check.get("evidence") == "document":
            errors.append(f"checks[{i}]: document cannot establish process behavior; use trace")
        if not isinstance(check.get("required"), bool):
            errors.append(f"checks[{i}].required: expected boolean")
        if not isinstance(check.get("criterion"), str) or not check["criterion"].strip():
            errors.append(f"checks[{i}].criterion: expected nonempty string")
    if len(set(map(str, ids))) != len(ids):
        errors.append("checks: duplicate IDs")
    return errors


def load_scenarios(directory: Path) -> list[dict]:
    paths = sorted(directory.glob("*.json"))
    if not paths:
        raise ValueError(f"No scenarios in {directory}")
    cases, ids, families = [], set(), {}
    for path in paths:
        case = read_json(path)
        errors = validate_scenario(case)
        if errors:
            raise ValueError(f"{path}: {'; '.join(errors)}")
        if case["id"] in ids:
            raise ValueError(f"Duplicate scenario: {case['id']}")
        ids.add(case["id"])
        if case["family"] in families and families[case["family"]] != case["split"]:
            raise ValueError(f"Family {case['family']} crosses development/holdout splits")
        families[case["family"]] = case["split"]
        cases.append(case)
    return cases


def prepare_run(case: dict, out: Path, *, condition: str, model: str, revision: str,
                snapshot: str, budget_tokens: int, repeat: int) -> Path:
    errors = validate_scenario(case)
    if errors:
        raise ValueError("; ".join(errors))
    if condition not in {"A", "B", "C"} or budget_tokens <= 0 or repeat <= 0:
        raise ValueError("Condition must be A/B/C and budget/repeat must be positive")
    if not all(isinstance(v, str) and v.strip() for v in (model, revision, snapshot)):
        raise ValueError("Model, revision and snapshot must be explicit")
    if condition == "A" and revision != "none":
        raise ValueError("Condition A requires --revision none")
    if condition != "A" and revision == "none":
        raise ValueError("Conditions B/C require an immutable plugin revision or content digest")
    run = out / f"{case['id']}--{condition}--r{repeat}"
    run.mkdir(parents=True, exist_ok=False)
    (run / "evidence").mkdir()
    manifest = {
        "schema_version": 1, "run_id": run.name, "case_id": case["id"],
        "case_digest": digest(case), "condition": condition, "model": model,
        "plugin_revision": revision, "input_snapshot": snapshot,
        "budget_tokens": budget_tokens, "repeat": repeat,
        "created_at": datetime.now(timezone.utc).isoformat(), "state": "prepared",
    }
    write_json(run / "manifest.json", manifest)
    public = {key: case[key] for key in PUBLIC}
    public["instructions"] = (
        "Complete the brief using the supplied project snapshot and available tools. "
        "Save the requested artifacts and a factual execution trace. "
        "Ask the user simulator for missing facts when needed."
    )
    write_json(run / "producer/task.json", public)
    write_json(run / "private/scenario.json", case)
    write_json(run / "private/simulator.json", {"user_facts": case["user_facts"]})
    write_json(run / "private/judge-input.json", {
        "brief": public, "checks": case["checks"],
        "instructions": "Review supplied anonymous artifacts independently. Do not infer success from plans or self-assessment."
    })
    write_json(run / "private/result-template.json", {
        "schema_version": 1, "run_id": run.name,
        "judge": {"identity": "", "calibration": ""},
        "execution": {"status": "not_run", "elapsed_seconds": None, "tokens": None},
        "ratings": [{"check_id": c["id"], "status": "unverified", "score": None,
                     "reason": "", "evidence": []} for c in case["checks"]],
        "artifacts": [{"requirement": item, "path": ""} for item in case["required_artifacts"]],
    })
    return run


def evidence_file(run: Path, value: Any) -> tuple[bool, str]:
    if not isinstance(value, str) or not value.strip():
        return False, "missing evidence path"
    path = Path(value)
    if path.is_absolute():
        return False, "absolute evidence path"
    resolved = (run / path).resolve()
    if not resolved.is_relative_to((run / "evidence").resolve()) or not resolved.is_relative_to(run.resolve()):
        return False, "evidence path escapes evidence directory"
    if not resolved.is_file():
        return False, "evidence file missing"
    if resolved.stat().st_size == 0:
        return False, "evidence file empty"
    return True, ""


def validate_manifest(manifest: dict) -> list[str]:
    errors = []
    for key in ("run_id", "case_id", "case_digest", "model", "plugin_revision", "input_snapshot"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            errors.append(f"Manifest {key}: expected nonempty string")
    if manifest.get("schema_version") != 1:
        errors.append("Unsupported manifest schema_version")
    if not isinstance(manifest.get("condition"), str) or manifest["condition"] not in {"A", "B", "C"}:
        errors.append("Manifest condition must be A/B/C")
    for key in ("budget_tokens", "repeat"):
        if type(manifest.get(key)) is not int or manifest[key] <= 0:
            errors.append(f"Manifest {key}: expected positive integer")
    if (manifest.get("condition") == "A") != (manifest.get("plugin_revision") == "none"):
        errors.append("Manifest condition and plugin revision disagree")
    return errors


def audit_run(run: Path) -> dict:
    manifest = read_json(run / "manifest.json")
    manifest_errors = validate_manifest(manifest)
    if manifest_errors:
        raise ValueError("; ".join(manifest_errors))
    case = read_json(run / "private/scenario.json")
    errors = validate_scenario(case)
    if errors:
        raise ValueError("; ".join(errors))
    if manifest.get("case_id") != case.get("id") or manifest.get("case_digest") != digest(case):
        errors.append("Manifest and frozen scenario do not match")
    result_path = run / "private/result.json"
    result = read_json(result_path) if result_path.is_file() else {}
    if not result:
        errors.append("No result.json; run is prepared, not evaluated")
    if result.get("schema_version") != 1:
        errors.append("Unsupported or missing result schema_version")
    if result.get("run_id") != manifest.get("run_id"):
        errors.append("Result run_id missing or mismatched")
    judge = result.get("judge", {})
    if not isinstance(judge, dict) or any(not isinstance(judge.get(k), str) or not judge[k].strip() for k in ("identity", "calibration")):
        errors.append("Judge identity/calibration missing")
    execution = result.get("execution", {})
    if not isinstance(execution, dict) or execution.get("status") != "completed":
        errors.append("Execution not completed")
    if isinstance(execution, dict):
        for key in ("elapsed_seconds", "tokens"):
            value = execution.get(key)
            if value is not None and (type(value) not in (int, float) or not math.isfinite(value) or value < 0):
                errors.append(f"Invalid measured execution {key}")
    ratings = result.get("ratings", [])
    if not isinstance(ratings, list):
        ratings = []
        errors.append("Ratings must be an array")
    by_id = {}
    for rating in ratings:
        if not isinstance(rating, dict) or not isinstance(rating.get("check_id"), str):
            errors.append("Invalid rating entry")
            continue
        key = rating["check_id"]
        if key in by_id:
            errors.append(f"Duplicate rating: {key}")
        by_id[key] = rating
    expected = {c["id"] for c in case["checks"]}
    if set(by_id) - expected:
        errors.append(f"Unknown ratings: {sorted(set(by_id) - expected)}")
    audited = []
    for check in case["checks"]:
        rating = by_id.get(check["id"], {})
        issues = []
        status = rating.get("status", "unverified")
        score = rating.get("score")
        if not rating:
            issues.append("Missing rating")
        if status not in STATUSES:
            issues.append("Invalid status")
        if status != "unverified" and (not isinstance(rating.get("reason"), str) or not rating["reason"].strip()):
            issues.append("Missing rationale")
        if check["required"] and status == "not_applicable":
            issues.append("Required check cannot be not_applicable")
        if check["kind"] in {"heuristic", "style"} and status in {"pass", "fail"}:
            if type(score) is not int or not 0 <= score <= 3:
                issues.append("Expected integer score 0..3")
        elif score is not None:
            issues.append("Score only applies to verified heuristic/style ratings")
        refs = rating.get("evidence", [])
        if not isinstance(refs, list):
            issues.append("Evidence must be an array")
            refs = []
        valid_evidence = []
        for ref in refs:
            if not isinstance(ref, dict) or ref.get("type") != check["evidence"] or not isinstance(ref.get("locator"), str) or not ref["locator"].strip():
                issues.append("Evidence requires matching type, path and specific locator")
                continue
            valid, issue = evidence_file(run, ref.get("path"))
            if valid:
                valid_evidence.append(ref)
            else:
                issues.append(issue)
        if status != "unverified" and not valid_evidence:
            issues.append("No verified evidence")
        if errors:
            issues.append("Run-level validation failed; submitted rating is not trusted")
        if issues:
            status, score = "unverified", None
        audited.append({"check_id": check["id"], "kind": check["kind"], "required": check["required"],
                        "status": status, "score": score if status in {"pass", "fail"} else None, "issues": issues,
                        "submitted_status": rating.get("status"), "submitted_score": rating.get("score"),
                        "reason": rating.get("reason", ""), "evidence": refs,
                        "available_evidence": valid_evidence})
    artifacts = result.get("artifacts", [])
    artifact_audit = []
    for requirement in case["required_artifacts"]:
        matching = [a for a in artifacts if isinstance(a, dict) and a.get("requirement") == requirement] if isinstance(artifacts, list) else []
        valid, issue = evidence_file(run, matching[0].get("path")) if len(matching) == 1 else (False, "Missing or duplicate artifact requirement")
        artifact_audit.append({"requirement": requirement, "path": matching[0].get("path") if len(matching) == 1 else None, "verified": valid, "issue": issue})
    required = [r for r in audited if r["required"]]
    failed = any(r["status"] == "fail" for r in required)
    incomplete = bool(errors) or any(r["required"] and r["status"] == "unverified" for r in audited) or any(not a["verified"] for a in artifact_audit)
    outcome = "fail" if failed else "unverified" if incomplete else "pass"
    return {"manifest": manifest, "family": case["family"], "split": case["split"],
            "outcome": outcome, "errors": errors, "ratings": audited, "artifacts": artifact_audit,
            "execution": execution, "judge": judge, "provenance_valid": not errors,
            "dimensions": {group: dict(Counter(r["status"] for r in audited if (r["kind"] == "process") == (group == "process"))) for group in ("process", "product")}}


def report_runs(root: Path) -> dict:
    runs, invalid = [], []
    for manifest in sorted(root.glob("*/manifest.json")):
        try:
            runs.append(audit_run(manifest.parent))
        except (ValueError, KeyError, TypeError, OSError) as exc:
            invalid.append({"run": str(manifest.parent), "error": str(exc)})
    groups = defaultdict(list)
    cases = defaultdict(dict)
    for run in runs:
        m = run["manifest"]
        groups[(m["case_id"], m["condition"])].append(run)
        cases[m["case_id"]][m["condition"]] = True
    summary = []
    for (case_id, condition), values in sorted(groups.items()):
        summary.append({"case_id": case_id, "condition": condition, "repeated_runs": len(values),
                        "outcomes": dict(Counter(v["outcome"] for v in values)),
                        "family": values[0]["family"], "split": values[0]["split"],
                        "measurements": [{"repeat": v["manifest"]["repeat"],
                                          "execution": v["execution"],
                                          "provenance_valid": v["provenance_valid"]} for v in values]})
    unmatched = []
    for case_id, conditions in sorted(cases.items()):
        selected = [r["manifest"] for r in runs if r["manifest"]["case_id"] == case_id]
        controls = {(m["model"], m["input_snapshot"], m["budget_tokens"], m["case_digest"]) for m in selected}
        repeats = {c: sorted(m["repeat"] for m in selected if m["condition"] == c) for c in "ABC"}
        revisions = {c: {m["plugin_revision"] for m in selected if m["condition"] == c} for c in "ABC"}
        reasons = []
        if set(conditions) != set("ABC"):
            reasons.append("Missing A/B/C condition")
        if len(controls) != 1:
            reasons.append("Model/snapshot/budget/scenario differs")
        if repeats["A"] != repeats["B"] or repeats["B"] != repeats["C"]:
            reasons.append("Repeat sets differ")
        if any(len(v) != len(set(v)) for v in repeats.values()):
            reasons.append("Duplicate repeat identity")
        if any(len(v) > 1 for v in revisions.values()):
            reasons.append("Mixed plugin revisions within condition")
        if reasons:
            unmatched.append({"case_id": case_id, "reasons": reasons})
    return {"schema_version": 1, "run_count": len(runs), "case_count": len(cases),
            "note": "Repeated runs are nested within cases; families may also be related. No aggregate quality score or significance claim is computed. File checks establish evidence availability, not truth or judge reliability.",
            "case_conditions": summary, "unmatched_cases": unmatched, "invalid_runs": invalid, "runs": runs}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--scenarios", type=Path, default=Path("evals/scenarios"))
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--scenarios", type=Path, default=Path("evals/scenarios"))
    prepare.add_argument("--case")
    prepare.add_argument("--out", type=Path, required=True)
    prepare.add_argument("--condition", choices=list("ABC"), required=True)
    prepare.add_argument("--model", required=True)
    prepare.add_argument("--revision", required=True)
    prepare.add_argument("--snapshot", required=True)
    prepare.add_argument("--budget-tokens", type=int, required=True)
    prepare.add_argument("--repeat", type=int, default=1, help="Repeat identity, not repeat count")
    report = sub.add_parser("report")
    report.add_argument("--runs", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "report":
            result = report_runs(args.runs)
        else:
            cases = load_scenarios(args.scenarios)
            if args.command == "validate":
                result = {"valid": True, "scenarios": len(cases), "families": len({c['family'] for c in cases})}
            else:
                if args.case:
                    cases = [c for c in cases if c["id"] == args.case]
                    if not cases:
                        raise ValueError("Unknown --case")
                result = {"prepared": [str(prepare_run(c, args.out, condition=args.condition, model=args.model,
                    revision=args.revision, snapshot=args.snapshot, budget_tokens=args.budget_tokens, repeat=args.repeat)) for c in cases],
                    "executed": False}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
