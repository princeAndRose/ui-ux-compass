#!/usr/bin/env python3
"""Extract common frontend route structures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PAGE_FILENAMES = {"page.tsx", "page.jsx", "page.ts", "page.js"}
LAYOUT_FILENAMES = {"layout.tsx", "layout.jsx", "layout.ts", "layout.js"}
PAGES_EXTENSIONS = {".tsx", ".jsx", ".ts", ".js", ".mdx"}


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _segment_to_route(segment: str) -> str | None:
    if segment.startswith("(") and segment.endswith(")"):
        return None
    if segment.startswith("@"):
        return None
    if segment.startswith("[[...") and segment.endswith("]]"):
        return f":{segment[5:-2]}*"
    if segment.startswith("[...") and segment.endswith("]"):
        return f":{segment[4:-1]}*"
    if segment.startswith("[") and segment.endswith("]"):
        return f":{segment[1:-1]}"
    return segment


def _parts_to_route(parts: tuple[str, ...]) -> str:
    route_parts = []
    for part in parts:
        converted = _segment_to_route(part)
        if converted:
            route_parts.append(converted)
    return "/" + "/".join(route_parts) if route_parts else "/"


def extract_routes(repo_root: Path | str) -> dict[str, Any]:
    root = Path(repo_root)
    routes: list[dict[str, str]] = []
    layout_files: list[str] = []

    for base_name in ("app", "src/app"):
        base = root / base_name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.name in PAGE_FILENAMES:
                route = _parts_to_route(path.parent.relative_to(base).parts)
                routes.append({"path": route, "file": _rel(root, path), "type": "page"})
            elif path.name in LAYOUT_FILENAMES:
                layout_files.append(_rel(root, path))

    for base_name in ("pages", "src/pages"):
        base = root / base_name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in PAGES_EXTENSIONS:
                continue
            if path.name.startswith("_") or path.parent.name == "api":
                continue
            parts = path.relative_to(base).with_suffix("").parts
            if parts[-1] == "index":
                parts = parts[:-1]
            route = _parts_to_route(parts)
            routes.append({"path": route, "file": _rel(root, path), "type": "page"})

    unique_routes = []
    seen = set()
    for route in sorted(routes, key=lambda item: (item["path"], item["file"])):
        key = (route["path"], route["file"], route["type"])
        if key not in seen:
            seen.add(key)
            unique_routes.append(route)

    return {"routes": unique_routes, "layout_files": sorted(set(layout_files))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = extract_routes(Path(args.repo_root))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)
