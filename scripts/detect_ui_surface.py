#!/usr/bin/env python3
"""Detect whether a task touches a user-facing UI surface."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SUBJECTIVE_REVIEW_TERMS = {
    "ugly",
    "cramped",
    "generic",
    "template-like",
    "template like",
    "off",
    "too busy",
    "too empty",
    "not premium",
    "not product-like",
    "hard to use",
    "looks wrong",
}

RISK_4_TERMS = {
    "landing page",
    "pricing page",
    "onboarding",
    "high fidelity",
    "high-fidelity",
    "flagship",
    "editor layout",
    "editor",
    "prototype",
}

RISK_3_TERMS = {
    "dashboard",
    "settings page",
    "admin page",
    "management page",
    "new page",
    "new flow",
    "form flow",
    "report page",
    "screen",
}

RISK_2_TERMS = {
    "empty state",
    "selected state",
    "dark mode",
    "filter",
    "table",
    "card component",
    "component",
    "responsive",
    "modal",
    "form",
    "layout spacing",
}

RISK_1_TERMS = {
    "button label",
    "label",
    "icon alignment",
    "css typo",
    "typescript error in button",
    "align icon",
}

GENERAL_UI_TERMS = {
    "ui",
    "ux",
    "page",
    "screen",
    "dashboard",
    "modal",
    "form",
    "layout",
    "sidebar",
    "header",
    "landing",
    "onboarding",
    "button",
    "css",
    "style",
    "tailwind",
    "component",
    "responsive",
    "shadcn",
    "radix",
    "mui",
    "antd",
}

NON_UI_TERMS = {
    "api",
    "database",
    "schema",
    "unit test",
    "tests",
    "infra",
    "dependency",
    "backend",
    "server",
    "retry",
    "performance",
    "pipeline",
    "platform",
    "transform",
}

EXPLICIT_UI_TERMS = {
    "page",
    "screen",
    "modal",
    "form",
    "layout",
    "sidebar",
    "header",
    "button",
    "css",
    "style",
    "tailwind",
    "component",
    "responsive",
    "empty state",
    "selected state",
    "dark mode",
    "settings page",
    "landing page",
    "pricing page",
    "new page",
    "new flow",
    "form flow",
    "editor layout",
}


def _matches_term(message: str, term: str) -> bool:
    escaped = re.escape(term).replace(r"\ ", r"\s+")
    pattern = rf"(?<![a-z0-9_-]){escaped}(?![a-z0-9_-])"
    return re.search(pattern, message, flags=re.IGNORECASE) is not None


def _contains_any(message: str, terms: set[str]) -> list[str]:
    return sorted(term for term in terms if _matches_term(message, term))


def _repo_signals(repo_root: Path) -> tuple[list[str], list[str]]:
    signals: list[str] = []
    surfaces: list[str] = []
    patterns = [
        ("app/**/page.tsx", "Next.js app route files detected"),
        ("app/**/page.jsx", "Next.js app route files detected"),
        ("pages/**/*.tsx", "Next.js pages route files detected"),
        ("src/routes/**/*", "route files detected"),
        ("src/components/**/*", "component directory detected"),
        ("components/**/*", "component directory detected"),
        ("*.css", "CSS files detected"),
        ("**/*.module.css", "CSS module files detected"),
        ("tailwind.config.*", "Tailwind config detected"),
        ("theme.*", "theme file detected"),
        ("tokens.*", "tokens file detected"),
    ]
    for pattern, signal in patterns:
        if any(repo_root.glob(pattern)):
            signals.append(signal)
            surfaces.append(pattern)
    return signals, surfaces


def detect_ui_surface(repo_root: Path | str, message: str) -> dict[str, Any]:
    root = Path(repo_root)
    normalized = message.lower()
    signals: list[str] = []
    likely_surfaces: list[str] = []

    repo_signals, surfaces = _repo_signals(root)
    likely_surfaces.extend(surfaces)
    non_ui_terms = _contains_any(normalized, NON_UI_TERMS)
    explicit_ui_terms = _contains_any(normalized, EXPLICIT_UI_TERMS)

    review_terms = _contains_any(normalized, SUBJECTIVE_REVIEW_TERMS)
    if review_terms:
        signals.extend(f"subjective UI feedback: {term}" for term in review_terms)
        return _result(True, 4, signals, likely_surfaces, "review", "ui-ux-review", repo_signals)

    if non_ui_terms and not explicit_ui_terms:
        signals.extend(f"non-UI term: {term}" for term in non_ui_terms)
        return _result(False, 0, signals, likely_surfaces, "observe", "ui-ux-compass-router", repo_signals)

    risk_4_terms = _contains_any(normalized, RISK_4_TERMS)
    if risk_4_terms:
        signals.extend(f"high-risk UI term: {term}" for term in risk_4_terms)
        return _result(True, 4, signals, likely_surfaces, "full-brief", "ui-ux-brief", repo_signals)

    risk_3_terms = _contains_any(normalized, RISK_3_TERMS)
    if risk_3_terms:
        signals.extend(f"new UI surface term: {term}" for term in risk_3_terms)
        return _result(True, 3, signals, likely_surfaces, "mini-brief", "ui-ux-brief", repo_signals)

    risk_2_terms = _contains_any(normalized, RISK_2_TERMS)
    if risk_2_terms:
        signals.extend(f"local UI ambiguity term: {term}" for term in risk_2_terms)
        mode = "assumptions-gate" if "dark mode" in risk_2_terms or "selected state" in risk_2_terms else "ask-one-question"
        return _result(True, 2, signals, likely_surfaces, mode, "ui-ux-capture-intent", repo_signals)

    risk_1_terms = _contains_any(normalized, RISK_1_TERMS)
    if risk_1_terms:
        signals.extend(f"trivial UI term: {term}" for term in risk_1_terms)
        return _result(True, 1, signals, likely_surfaces, "apply-existing-conventions", "ui-ux-compass-router", repo_signals)

    ui_terms = _contains_any(normalized, GENERAL_UI_TERMS)
    if ui_terms:
        signals.extend(f"general UI term: {term}" for term in ui_terms)
        risk = 2 if len(ui_terms) <= 2 else 3
        mode = "ask-one-question" if risk == 2 else "mini-brief"
        skill = "ui-ux-capture-intent" if risk == 2 else "ui-ux-brief"
        return _result(True, risk, signals, likely_surfaces, mode, skill, repo_signals)

    signals.extend(f"non-UI term: {term}" for term in non_ui_terms)
    return _result(False, 0, signals, likely_surfaces, "observe", "ui-ux-compass-router", repo_signals)


def _result(
    ui_related: bool,
    risk_level: int,
    signals: list[str],
    likely_surfaces: list[str],
    mode: str,
    skill: str,
    repo_signals: list[str],
) -> dict[str, Any]:
    all_signals = signals + repo_signals
    confidence = 0.15
    if risk_level == 0:
        confidence = 0.82 if signals else 0.68
    elif risk_level == 1:
        confidence = 0.72
    elif risk_level == 2:
        confidence = 0.78
    elif risk_level == 3:
        confidence = 0.86
    elif risk_level == 4:
        confidence = 0.9
    if repo_signals and ui_related:
        confidence = min(0.96, confidence + 0.05)
    return {
        "ui_related": ui_related,
        "risk_level": risk_level,
        "confidence": round(confidence, 2),
        "signals": all_signals,
        "likely_surfaces": sorted(set(likely_surfaces)),
        "recommended_mode": mode,
        "recommended_skill": skill,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--message", required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = detect_ui_surface(Path(args.repo_root), args.message)
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"UI related: {result['ui_related']}")
        print(f"Risk level: {result['risk_level']}")
        print(f"Recommended mode: {result['recommended_mode']}")
        print(f"Recommended skill: {result['recommended_skill']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
