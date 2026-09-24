#!/usr/bin/env python3
"""Registry generation fixture for the frozen ADR-0032 archive machinery.

ADR-0038 closes the sealed-record and path-ledger generation. The repository
registry now routes only the frozen records and ledgers by exact path, so no
fixture can create another one under it, which is the contract. The machinery
that still validates that frozen content keeps its regressions by exercising
synthetic records and ledgers against the registry generation that governed
them.

That generation is derived from the current registry rather than read from Git
history, so the regressions need no particular commit. The derivation reverses
exactly what ADR-0038 added: the retention class binding, the two route
disposition forms and their family, the mirrored retention alternatives, and
the exact frozen routes, together with the retention units, modes, citation
table, and legacy set that ADR-0039 added, the optional `superseded_by` key
and the `draft` to `withdrawn` edge that SPEC-0084 added, and the optional
`superseded_by` key later admitted on the Stage 05 operation profiles.
`tests/test_archive_generation_fixture.py` proves the
derivation equals the registry merged at `LEGACY_ARCHIVE_GENERATION_COMMIT`.

A regression that asserts what the current registry admits must load the
repository registry instead; this fixture never stands in for that.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = "docs/99.templates/registry.json"
LEGACY_ARCHIVE_GENERATION_COMMIT = "c652331ce1c6bfddf1e670c748ce1a04b3835c33"
ADR0038_PROFILES = frozenset(
    {
        "archive/route-tombstone",
        "archive/scope-migration",
        "common/template-archive-route-tombstone",
        "common/template-archive-scope-migration",
    }
)
ADR0038_FAMILY = "route-disposition"
SPEC0084_SUPERSEDED_BY_PROFILES = frozenset(
    {
        "sdlc/spec",
        "common/template-sdlc-spec",
    }
)
STAGE05_SUPERSEDED_BY_PROFILES = frozenset(
    {
        "operation/guide",
        "operation/policy",
        "operation/runbook",
        "common/template-operation-guide",
        "common/template-operation-policy",
        "common/template-operation-runbook",
    }
)
SPEC0084_SUPERSEDED_BY_KEY = "superseded_by"
SPEC0084_DRAFT_WITHDRAWN_FAMILY = "spec-plan"
SPEC0084_DRAFT_WITHDRAWN_EDGE = ["draft", "withdrawn"]
FROZEN_GENERATION_ROUTES = {
    "archive/tombstone": (
        r"^docs/98\.archive/(?!migrations/)(?!completed/)"
        r"(?!.*(?:/)?README\.md$).+\.md$"
    ),
    "archive/migration": r"^docs/98\.archive/migrations/[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$",
}


def _leading_group(body: str) -> tuple[list[str], str] | None:
    if not body.startswith("(?:"):
        return None
    depth, start, branches, index = 0, 3, [], 0
    while index < len(body):
        character = body[index]
        if character == "\\":
            index += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                branches.append(body[start:index])
                return branches, body[index + 1 :]
        elif character == "|" and depth == 1:
            branches.append(body[start:index])
            start = index + 1
        index += 1
    return None


def _frozen_generation_route(pattern: str) -> str:
    split = _leading_group(pattern[1:-1])
    if split is None or split[1] == "":
        return pattern
    branches, tail = split
    active = [branch for branch in branches if "98\\.archive" not in branch]
    completed = [
        branch
        for branch in branches
        if "98\\.archive" in branch and "completed" in branch
    ]
    if completed:
        stage = completed[0].rsplit("/", 1)[-1]
        mirror = r"docs/98\.archive/completed/" + stage
        return "^(?:" + "|".join([*active, mirror]) + ")" + tail + "$"
    if len(active) == 1 and len(active) < len(branches):
        return "^" + active[0] + tail + "$"
    return pattern


def legacy_registry_payload() -> dict[str, Any]:
    """Return a fresh mutable copy of the frozen generation registry."""

    payload = json.loads((ROOT / REGISTRY_PATH).read_text(encoding="utf-8"))
    for key in (
        "retention_classes",
        "retention_units",
        "retention_modes",
        "archive_citation",
        "archive_assessment",
        "legacy_rebased_retained_paths",
    ):
        payload.pop(key, None)
    payload["profiles"] = [
        profile
        for profile in payload["profiles"]
        if profile["id"] not in ADR0038_PROFILES
    ]
    payload["lifecycle_domains"] = [
        domain
        for domain in payload["lifecycle_domains"]
        if domain["family"] != ADR0038_FAMILY
    ]
    for profile in payload["profiles"]:
        profile["path_pattern"] = FROZEN_GENERATION_ROUTES.get(
            profile["id"], _frozen_generation_route(profile["path_pattern"])
        )
        if (
            profile["id"]
            in SPEC0084_SUPERSEDED_BY_PROFILES | STAGE05_SUPERSEDED_BY_PROFILES
        ):
            frontmatter = profile["frontmatter"]
            for key in ("optional", "order"):
                frontmatter[key] = [
                    name
                    for name in frontmatter[key]
                    if name != SPEC0084_SUPERSEDED_BY_KEY
                ]
    for domain in payload["lifecycle_domains"]:
        if domain["family"] == SPEC0084_DRAFT_WITHDRAWN_FAMILY:
            domain["transitions"] = [
                transition
                for transition in domain["transitions"]
                if list(transition) != SPEC0084_DRAFT_WITHDRAWN_EDGE
            ]
    return payload


def legacy_registry_bytes() -> bytes:
    """Serialize the frozen generation registry in the registry's own format."""

    return (
        json.dumps(legacy_registry_payload(), indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def legacy_registry():
    """Return the frozen generation registry as the typed lifecycle view."""

    import sys

    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from document_contracts import _typed_registry_from_mapping

    return _typed_registry_from_mapping(legacy_registry_payload())
