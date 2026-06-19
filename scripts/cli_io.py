#!/usr/bin/env python3
"""Shared CLI helpers for the UI/UX Compass scripts."""

from __future__ import annotations

import sys
from typing import Any


def _enable_utf8(stream: Any) -> None:
    """Reconfigure a single stream to UTF-8 when it supports it."""
    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is None:
        return
    try:
        reconfigure(encoding="utf-8")
    except (ValueError, OSError):  # pragma: no cover - exotic or detached streams
        pass


def enable_utf8_output() -> None:
    """Emit UTF-8 on stdout/stderr so CJK JSON renders on any console.

    The scripts print JSON with ``ensure_ascii=False``. On a console whose
    default encoding is not UTF-8 -- the legacy Windows code page, for example
    -- that turns Chinese signals into mojibake. Python 3.7+ text streams expose
    ``reconfigure``; anything that does not is left untouched.
    """
    _enable_utf8(sys.stdout)
    _enable_utf8(sys.stderr)
