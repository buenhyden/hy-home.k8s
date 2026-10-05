#!/usr/bin/env python3
"""Read the actual frozen ADR-0032 registry generation from Git history.

Current registry edits cannot reinterpret the frozen archive machinery. Local
and hosted regression validation requires this historical Git object; an absent
object is an unavailable fixture rather than permission to synthesize its facts.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "docs/99.templates/registry.json"
LEGACY_ARCHIVE_GENERATION_COMMIT = "c652331ce1c6bfddf1e670c748ce1a04b3835c33"


def legacy_asset_bytes(relative_path: str) -> bytes:
    """Read one Stage 99 asset from the Registry's immutable generation."""
    path = PurePosixPath(relative_path)
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.as_posix() != relative_path
        or not relative_path.startswith("docs/99.templates/")
    ):
        raise ValueError("frozen fixture asset must be a normalized Stage 99 path")
    return subprocess.check_output(
        [
            "git",
            "--no-replace-objects",
            "-C",
            str(ROOT),
            "cat-file",
            "blob",
            f"{LEGACY_ARCHIVE_GENERATION_COMMIT}:{relative_path}",
        ],
        stderr=subprocess.DEVNULL,
    )


def legacy_registry_bytes() -> bytes:
    """Return the exact immutable frozen-generation registry blob."""
    return legacy_asset_bytes(REGISTRY_PATH)


def legacy_registry_payload() -> dict[str, Any]:
    """Return a fresh mutable copy of the actual frozen generation."""
    return json.loads(legacy_registry_bytes())


def legacy_registry():
    """Return the frozen generation as the shared typed lifecycle view."""
    import sys

    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from document_contracts import _typed_registry_from_mapping

    return _typed_registry_from_mapping(legacy_registry_payload())
