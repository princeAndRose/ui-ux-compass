#!/usr/bin/env python3
"""Inspect frontend framework and design-system conventions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKIP_DIRS = {
    ".git",
    ".cache",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
}
MAX_CSS_BYTES_PER_FILE = 20000
MAX_CSS_BYTES_TOTAL = 200000


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_skipped(root: Path, path: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in parts)


def _iter_files(root: Path, pattern: str):
    for path in root.glob(pattern):
        if path.is_file() and not _is_skipped(root, path):
            yield path


def _read_css_sample(paths) -> str:
    chunks: list[str] = []
    remaining = MAX_CSS_BYTES_TOTAL
    for path in paths:
        if remaining <= 0:
            break
        limit = min(MAX_CSS_BYTES_PER_FILE, remaining)
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            chunk = handle.read(limit)
        chunks.append(chunk)
        remaining -= len(chunk)
    return "\n".join(chunks)


def _load_package_json(root: Path) -> dict[str, Any]:
    path = root / "package.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _dependencies(package: dict[str, Any]) -> dict[str, str]:
    deps: dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = package.get(key)
        if isinstance(value, dict):
            deps.update({str(k): str(v) for k, v in value.items()})
    return deps


def inspect_design_system(repo_root: Path | str) -> dict[str, Any]:
    root = Path(repo_root)
    package = _load_package_json(root)
    deps = _dependencies(package)
    dep_names = set(deps)

    framework = "unknown"
    if "next" in dep_names:
        framework = "next"
    elif "nuxt" in dep_names:
        framework = "nuxt"
    elif "svelte" in dep_names or "@sveltejs/kit" in dep_names:
        framework = "svelte"
    elif "vue" in dep_names:
        framework = "vue"
    elif "react" in dep_names:
        framework = "react"

    router = "unknown"
    if (root / "app").is_dir():
        router = "app-router"
    elif (root / "pages").is_dir() or (root / "src" / "pages").is_dir():
        router = "pages-router"
    elif (root / "src" / "routes").is_dir():
        router = "file-routes"

    styling: list[str] = []
    if "tailwindcss" in dep_names or any(_iter_files(root, "tailwind.config.*")):
        styling.append("tailwind")
    if any(_iter_files(root, "**/*.module.css")):
        styling.append("css-modules")
    if "sass" in dep_names or any(_iter_files(root, "**/*.scss")):
        styling.append("sass")
    if "styled-components" in dep_names:
        styling.append("styled-components")
    if "@emotion/react" in dep_names or "@emotion/styled" in dep_names:
        styling.append("emotion")

    ui_library: list[str] = []
    if (root / "components.json").is_file() or "class-variance-authority" in dep_names:
        ui_library.append("shadcn-ui")
    if any(name.startswith("@radix-ui/") for name in dep_names):
        ui_library.append("radix")
    if "@mui/material" in dep_names:
        ui_library.append("mui")
    if "antd" in dep_names:
        ui_library.append("ant-design")
    if "@chakra-ui/react" in dep_names:
        ui_library.append("chakra")

    token_patterns = [
        "tailwind.config.*",
        "theme.*",
        "tokens.*",
        "src/**/tokens.*",
        "src/**/theme.*",
        "src/styles/globals.css",
        "app/globals.css",
    ]
    tokens = sorted({_rel(root, path) for pattern in token_patterns for path in _iter_files(root, pattern)})

    component_candidates = [
        root / "src" / "components" / "ui",
        root / "src" / "components",
        root / "components" / "ui",
        root / "components",
        root / "src" / "ui",
    ]
    component_dirs = [_rel(root, path) for path in component_candidates if path.is_dir()]

    package_manager = "unknown"
    if (root / "pnpm-lock.yaml").is_file():
        package_manager = "pnpm"
    elif (root / "yarn.lock").is_file():
        package_manager = "yarn"
    elif (root / "package-lock.json").is_file():
        package_manager = "npm"
    elif (root / "bun.lockb").is_file() or (root / "bun.lock").is_file():
        package_manager = "bun"

    css_text = _read_css_sample(_iter_files(root, "**/*.css"))
    conventions = {
        "package_manager": package_manager,
        "uses_css_variables": "var(--" in css_text or ":root" in css_text,
        "has_dark_mode": ".dark" in css_text or "dark:" in css_text or "next-themes" in dep_names,
        "class_utility_style": "tailwind" if "tailwind" in styling else "unknown",
        "has_storybook": any(name.startswith("@storybook/") or name == "storybook" for name in dep_names),
    }

    notes: list[str] = []
    if "shadcn-ui" in ui_library:
        notes.append("Prefer existing shadcn/ui components before introducing new primitives.")
    if "tailwind" in styling:
        notes.append("Prefer existing Tailwind tokens and CSS variables.")
    if not component_dirs:
        notes.append("No obvious component directory detected.")

    return {
        "framework": framework,
        "router": router,
        "styling": styling,
        "ui_library": ui_library,
        "tokens": tokens,
        "component_dirs": component_dirs,
        "conventions": conventions,
        "notes": notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = inspect_design_system(Path(args.repo_root))
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
