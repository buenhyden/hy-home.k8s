#!/usr/bin/env python3
"""Registry generation fixture for the frozen ADR-0032 archive machinery.

ADR-0038 closes the sealed-record and path-ledger generation. The repository
registry now routes only the frozen records and ledgers by exact path, so no
fixture can create another one under it, which is the contract. The machinery
that still validates that frozen content keeps its regressions by exercising
synthetic records and ledgers against the registry generation that governed
them: the one on the default branch at `LEGACY_ARCHIVE_GENERATION_COMMIT`, the
last merged commit before ADR-0038 moved the routes.

A regression that asserts what the current registry admits must load the
repository registry instead; this fixture never stands in for that.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "docs/99.templates/registry.json"
LEGACY_ARCHIVE_GENERATION_COMMIT = "c652331ce1c6bfddf1e670c748ce1a04b3835c33"


def legacy_registry_bytes() -> bytes:
    """Return the exact registry blob of the frozen archive generation."""

    completed = subprocess.run(
        [
            "git",
            "--no-replace-objects",
            "-C",
            str(ROOT),
            "cat-file",
            "blob",
            f"{LEGACY_ARCHIVE_GENERATION_COMMIT}:{REGISTRY_PATH}",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "legacy archive generation registry is unavailable: "
            + completed.stderr.decode("utf-8", errors="replace")
        )
    return completed.stdout


def legacy_registry_payload() -> dict[str, Any]:
    """Return a fresh mutable copy of the frozen generation registry."""

    return json.loads(legacy_registry_bytes())


def legacy_registry():
    """Return the frozen generation registry as the typed lifecycle view."""

    import sys

    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from document_contracts import _typed_registry_from_mapping

    return _typed_registry_from_mapping(legacy_registry_payload())
