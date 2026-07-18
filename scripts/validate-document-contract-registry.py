#!/usr/bin/env python3
"""Validate the document-profile registry and its deterministic routing."""

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path, PurePosixPath
from typing import Any

from document_contracts import (
    BASELINE_COUNT,
    BASELINE_SHA,
    REGISTRY_PATH,
    SCHEMA_PATH,
    DocumentContractError,
    Registry,
    TargetInventory,
    classify_path,
    classify_paths,
    enumerate_target_markdown,
    load_json_file,
    load_registry,
    _parse_ls_files_stage_z,
    _parse_ls_tree_z,
    validate_registry,
)


SAMPLE_PATH = PurePosixPath(".agents/GEMINI.md")
LOCAL_AGENT_FIXTURE_FIELD = "localAgentFixtureSamplePath"
RESERVED_GEMINI_NATIVE_SURFACE_RULE = "REGISTRY_RESERVED_GEMINI_NATIVE_SURFACE"
RESERVED_GEMINI_NATIVE_SURFACE_ERROR = (
    f"{RESERVED_GEMINI_NATIVE_SURFACE_RULE}: reserved Gemini CLI native surface "
    "must remain absent from the Git index"
)
RETIRED_CLOUD_SDLC_SURFACE_RULE = "REGISTRY_RETIRED_CLOUD_SDLC_SURFACE"
RETIRED_CLOUD_SDLC_SURFACE_ERROR = (
    f"{RETIRED_CLOUD_SDLC_SURFACE_RULE}: retired cloud documentation surface "
    "must remain absent from the Git index"
)
TEMPLATE_SOURCE_PARITY_PATH = Path(
    "tests/fixtures/document-contracts/template-source-parity.json"
)
CURRENT_OWNER_SAMPLE_PATHS = (
    "docs/00.agent-governance/current-alpha.md",
    "docs/00.agent-governance/current-beta.md",
)
REFERENCE_COLLECTION_SAMPLE_PATHS = (
    "docs/90.references/audits/README.md",
    "docs/90.references/research/README.md",
)
REFERENCE_PACK_SAMPLE_PATHS = (
    "docs/90.references/audits/2026-07-11-test/README.md",
    "docs/90.references/research/2026-07-07-test/README.md",
)
REFERENCE_MEMBER_SAMPLE_PATHS = (
    "docs/90.references/audits/2026-07-11-test/audit.md",
    "docs/90.references/research/2026-07-07-test/accepted.md",
    "docs/90.references/research/2026-07-07-test/active.md",
)
LINEAGE_FIXTURE_DOCUMENTS = {
    "docs/01.requirements/005-fixture.md": ("sdlc/prd", "done", "2026-07-12"),
    "docs/01.requirements/006-fixture.md": ("sdlc/prd", "active", "2026-07-15"),
    "docs/02.architecture/requirements/0008-fixture.md": (
        "sdlc/ard",
        "accepted",
        "2026-07-12",
    ),
    "docs/02.architecture/requirements/0009-fixture.md": (
        "sdlc/ard",
        "active",
        "2026-07-15",
    ),
    "docs/02.architecture/decisions/0015-fixture.md": (
        "sdlc/adr",
        "accepted",
        "2026-07-11",
    ),
    "docs/02.architecture/decisions/0016-fixture.md": (
        "sdlc/adr",
        "accepted",
        "2026-07-12",
    ),
    "docs/02.architecture/decisions/0017-fixture.md": (
        "sdlc/adr",
        "accepted",
        "2026-07-15",
    ),
    "docs/02.architecture/decisions/0018-fixture.md": (
        "sdlc/adr",
        "active",
        "2026-07-16",
    ),
    "docs/02.architecture/decisions/0021-fixture.md": (
        "sdlc/adr",
        "accepted",
        "2026-07-17",
    ),
    "docs/02.architecture/decisions/0022-fixture.md": (
        "sdlc/adr",
        "accepted",
        "2026-07-18",
    ),
    "docs/03.specs/026-fixture/spec.md": ("sdlc/spec", "done", "2026-07-12"),
    "docs/03.specs/033-fixture/spec.md": ("sdlc/spec", "done", "2026-07-15"),
    "docs/03.specs/034-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
    "docs/03.specs/035-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
    "docs/03.specs/038-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
    "docs/03.specs/039-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
}
LINEAGE_INVALID_FIXTURE_DOCUMENTS = {
    "docs/02.architecture/decisions/0019-fixture.md": (
        "---\n"
        "title: 'Synthetic duplicate updated ADR'\n"
        "type: sdlc/adr\n"
        "status: accepted\n"
        "owner: platform\n"
        "updated: 2026-07-10\n"
        "updated: 2026-07-16\n"
        "---\n\n"
        "# Synthetic duplicate updated ADR\n"
    ),
    "docs/02.architecture/decisions/0020-fixture.md": (
        "---\n"
        "title: 'Synthetic timestamp ADR'\n"
        "type: sdlc/adr\n"
        "status: accepted\n"
        "owner: platform\n"
        "updated: 2026-07-16T10:00:00+00:00\n"
        "---\n\n"
        "# Synthetic timestamp ADR\n"
    ),
    "docs/03.specs/036-fixture/spec.md": (
        "---\n"
        "title: 'Synthetic duplicate status Spec'\n"
        "type: sdlc/spec\n"
        "status: done\n"
        "status: active\n"
        "owner: platform\n"
        "updated: 2026-07-15\n"
        "---\n\n"
        "# Synthetic duplicate status Spec\n"
    ),
}
FIXTURE_PATH = PurePosixPath("tests/fixtures/document-contracts/registry-cases.json")
README_FIXTURE_PATH = PurePosixPath(
    "tests/fixtures/document-contracts/readme-profile-cases.json"
)
EXPECTED_CASES = (
    ("valid-minimal", "none", ()),
    ("duplicate-profile-id", "duplicate-profile-id", ("REGISTRY_PROFILE_ID",)),
    ("unsupported-route-kind", "route-kind-glob", ("REGISTRY_ROUTE_KIND",)),
    ("unanchored-regex", "drop-regex-end-anchor", ("REGISTRY_ROUTE_ANCHOR",)),
    ("overlapping-route", "add-overlapping-exact-route", ("REGISTRY_ROUTE_AMBIGUOUS",)),
    ("uncovered-route", "remove-sample-route", ("REGISTRY_ROUTE_UNCOVERED",)),
    ("missing-template", "point-to-missing-template", ("REGISTRY_TEMPLATE",)),
    ("missing-body-contract", "remove-body-contract", ("REGISTRY_BODY_REQUIRED",)),
    ("unknown-body-field", "add-unknown-body-field", ("REGISTRY_BODY_FIELD",)),
    ("body-section-not-required", "change-body-section", ("REGISTRY_BODY_SECTION",)),
    (
        "body-status-outside-domain",
        "add-unknown-body-status",
        ("REGISTRY_BODY_STATUS",),
    ),
    ("empty-body-columns", "empty-body-columns", ("REGISTRY_BODY_COLUMNS",)),
    (
        "duplicate-body-columns",
        "duplicate-body-column",
        ("REGISTRY_BODY_COLUMNS",),
    ),
    (
        "unknown-body-source-profile",
        "unknown-body-source-profile",
        ("REGISTRY_BODY_SOURCE_PROFILE",),
    ),
    (
        "unknown-body-target-profile",
        "unknown-body-target-profile",
        ("REGISTRY_BODY_TARGET_PROFILE",),
    ),
    (
        "template-source-body-drift",
        "drift-template-body-contract",
        ("REGISTRY_BODY_SOURCE_DRIFT",),
    ),
    (
        "missing-native-template",
        "add-native-with-missing-template",
        ("REGISTRY_TEMPLATE",),
    ),
    (
        "overlapping-native-route",
        "add-overlapping-native-route",
        ("REGISTRY_ROUTE_AMBIGUOUS",),
    ),
    ("wrong-baseline-sha", "change-baseline-sha", ("REGISTRY_BASELINE_SHA",)),
    ("wrong-baseline-count", "change-baseline-count", ("REGISTRY_BASELINE_COUNT",)),
    (
        "malformed-governance-current-owners",
        "malform-governance-current-owners",
        ("REGISTRY_SCHEMA",),
    ),
    (
        "missing-governance-current-owners",
        "remove-governance-current-owners",
        ("REGISTRY_SCHEMA",),
    ),
    (
        "invalid-governance-current-owner-path",
        "invalidate-governance-current-owner-path",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",),
    ),
    (
        "noncanonical-governance-current-owner-path",
        "double-slash-governance-current-owner-path",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",),
    ),
    (
        "normalized-alias-governance-current-owner-duplicate",
        "normalized-alias-governance-current-owner-duplicate",
        (
            "REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",
            "REGISTRY_GOVERNANCE_CURRENT_OWNER_DUPLICATE",
        ),
    ),
    (
        "control-character-governance-current-owner-path",
        "nul-governance-current-owner-path",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_PATH",),
    ),
    (
        "duplicate-governance-current-owner",
        "duplicate-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_DUPLICATE",),
    ),
    (
        "unsorted-governance-current-owners",
        "reverse-governance-current-owners",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_ORDER",),
    ),
    (
        "missing-governance-current-owner",
        "missing-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",),
    ),
    (
        "untracked-governance-current-owner",
        "untracked-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",),
    ),
    (
        "symlink-governance-current-owner",
        "symlink-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",),
    ),
    (
        "wrong-profile-governance-current-owner",
        "wrong-profile-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",),
    ),
    (
        "non-authored-governance-current-owner",
        "non-authored-governance-current-owner",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",),
    ),
    (
        "wrong-governance-current-owner-state-contract",
        "reverse-governance-current-owner-states",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_STATE",),
    ),
    (
        "missing-governance-current-owner-state-contract",
        "remove-governance-current-owner-states",
        ("REGISTRY_GOVERNANCE_CURRENT_OWNER_STATE",),
    ),
    (
        "malformed-reference-current-packs",
        "malform-reference-current-packs",
        ("REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION",),
    ),
    (
        "missing-reference-current-packs",
        "remove-reference-current-packs",
        ("REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION",),
    ),
    (
        "duplicate-reference-pack-id",
        "duplicate-reference-pack-id",
        (
            "REGISTRY_REFERENCE_CURRENT_PACK_ID",
            "REGISTRY_REFERENCE_CURRENT_PACK_DUPLICATE",
        ),
    ),
    (
        "missing-reference-pack-collection",
        "missing-reference-pack-collection",
        ("REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION",),
    ),
    (
        "extra-reference-pack-collection",
        "extra-reference-pack-collection",
        ("REGISTRY_REFERENCE_CURRENT_PACK_DECLARATION",),
    ),
    (
        "misordered-reference-pack-id",
        "reverse-reference-pack-ids",
        (
            "REGISTRY_REFERENCE_CURRENT_PACK_ID",
            "REGISTRY_REFERENCE_CURRENT_PACK_ORDER",
        ),
    ),
    (
        "invalid-reference-pack-id",
        "invalidate-reference-pack-id",
        ("REGISTRY_REFERENCE_CURRENT_PACK_ID",),
    ),
    (
        "parent-reference-member",
        "parent-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PATH",),
    ),
    (
        "leading-dot-reference-member",
        "leading-dot-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PATH",),
    ),
    (
        "slash-reference-member",
        "slash-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PATH",),
    ),
    (
        "control-reference-member",
        "control-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PATH",),
    ),
    (
        "normalized-alias-reference-member",
        "normalized-alias-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PATH",),
    ),
    (
        "duplicate-reference-member",
        "duplicate-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_DUPLICATE",),
    ),
    (
        "unsorted-reference-members",
        "reverse-reference-members",
        ("REGISTRY_REFERENCE_CURRENT_PACK_ORDER",),
    ),
    (
        "wrong-reference-pack-state-contract",
        "wrong-reference-pack-states",
        ("REGISTRY_REFERENCE_CURRENT_PACK_STATE",),
    ),
    (
        "missing-reference-pack-state-contract",
        "remove-reference-pack-states",
        ("REGISTRY_REFERENCE_CURRENT_PACK_STATE",),
    ),
    (
        "outside-reference-profile-state",
        "outside-reference-profile-state",
        ("REGISTRY_REFERENCE_CURRENT_PACK_STATE",),
    ),
    (
        "missing-reference-member",
        "missing-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_MISSING",),
    ),
    (
        "untracked-reference-member",
        "untracked-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_MISSING",),
    ),
    (
        "symlink-reference-member",
        "symlink-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_MISSING",),
    ),
    (
        "non-regular-reference-member",
        "non-regular-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_MISSING",),
    ),
    (
        "wrong-profile-reference-member",
        "wrong-profile-reference-member",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",),
    ),
    (
        "wrong-profile-reference-pack-readme",
        "wrong-profile-reference-pack-readme",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",),
    ),
    (
        "wrong-profile-reference-collection-readme",
        "wrong-profile-reference-collection-readme",
        ("REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",),
    ),
    (
        "duplicate-program",
        "duplicate-program",
        ("REGISTRY_PROGRAM_DUPLICATE",),
    ),
    (
        "unsorted-programs",
        "reverse-programs",
        ("REGISTRY_PROGRAM_RELATION_ORDER",),
    ),
    (
        "duplicate-program-member",
        "duplicate-program-member",
        ("REGISTRY_PROGRAM_MEMBER_DUPLICATE",),
    ),
    (
        "overlapping-program-member",
        "overlap-program-member",
        ("REGISTRY_PROGRAM_MEMBER_OVERLAP",),
    ),
    (
        "noncontiguous-program-order",
        "noncontiguous-program-order",
        ("REGISTRY_PROGRAM_RELATION_ORDER",),
    ),
    ("unknown-program-prd", "unknown-program-prd", ("REGISTRY_PROGRAM_PATH",)),
    ("unknown-program-ard", "unknown-program-ard", ("REGISTRY_PROGRAM_PATH",)),
    ("unknown-program-adr", "unknown-program-adr", ("REGISTRY_PROGRAM_PATH",)),
    ("unknown-program-spec", "unknown-program-spec", ("REGISTRY_PROGRAM_PATH",)),
    ("program-state-drift", "program-state-drift", ("REGISTRY_PROGRAM_STATE",)),
    (
        "program-decision-not-accepted",
        "program-decision-not-accepted",
        ("REGISTRY_PROGRAM_DECISION",),
    ),
    (
        "program-decision-missing",
        "program-decision-missing",
        ("REGISTRY_PROGRAM_DECISION",),
    ),
    (
        "invalid-program-evidence-mode",
        "invalid-program-evidence-mode",
        ("REGISTRY_PROGRAM_EVIDENCE_MODE",),
    ),
    (
        "program-follow-up-predates-tranche",
        "program-follow-up-predates-tranche",
        ("REGISTRY_PROGRAM_CHRONOLOGY",),
    ),
    (
        "production-legacy-v5-input",
        "production-legacy-v5-input",
        ("REGISTRY_SCHEMA",),
    ),
    (
        "duplicate-program-spec-status-key",
        "duplicate-program-spec-status-key",
        ("REGISTRY_PROGRAM_STATE",),
    ),
    (
        "duplicate-program-adr-updated-key",
        "duplicate-program-adr-updated-key",
        ("REGISTRY_PROGRAM_DECISION",),
    ),
    (
        "timestamp-program-adr-updated",
        "timestamp-program-adr-updated",
        ("REGISTRY_PROGRAM_DECISION",),
    ),
    (
        "misordered-follow-up-approval",
        "misordered-follow-up-approval",
        ("REGISTRY_PROGRAM_CHRONOLOGY",),
    ),
    (
        "unknown-document-contract-field",
        "unknown-document-contract-field",
        ("REGISTRY_SCHEMA",),
    ),
    ("missing-value-contract", "missing-value-contract", ("REGISTRY_VALUE_CONTRACT",)),
    ("invalid-value-kind", "invalid-value-kind", ("REGISTRY_VALUE_CONTRACT",)),
    ("invalid-value-enum", "invalid-value-enum", ("REGISTRY_VALUE_CONTRACT",)),
    (
        "invalid-value-constant",
        "invalid-value-constant",
        ("REGISTRY_VALUE_CONTRACT",),
    ),
    (
        "invalid-value-pattern",
        "invalid-value-pattern",
        ("REGISTRY_VALUE_CONTRACT",),
    ),
    (
        "invalid-value-nullability",
        "invalid-value-nullability",
        ("REGISTRY_VALUE_CONTRACT",),
    ),
    (
        "invalid-value-condition",
        "invalid-value-condition",
        ("REGISTRY_VALUE_CONTRACT",),
    ),
    ("missing-role-decision", "missing-role-decision", ("REGISTRY_ROLE_DECISION",)),
    (
        "invalid-relationship-section",
        "invalid-relationship-section",
        ("REGISTRY_ROLE_DECISION",),
    ),
    (
        "invalid-body-requirement",
        "invalid-body-requirement",
        ("REGISTRY_ROLE_DECISION", "REGISTRY_EVIDENCE_PREDICATE"),
    ),
    ("invalid-create-admission", "invalid-create-admission", ("REGISTRY_ADMISSION",)),
    (
        "archive-admission-predicate-missing",
        "archive-admission-predicate-missing",
        ("REGISTRY_ADMISSION",),
    ),
    (
        "archive-evidence-capability-drift",
        "archive-evidence-capability-drift",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "archive-evidence-shape-drift",
        "archive-evidence-shape-drift",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    ("allow-delete", "allow-delete", ("REGISTRY_ADMISSION",)),
    ("allow-rename", "allow-rename", ("REGISTRY_ADMISSION",)),
    ("allow-profile-change", "allow-profile-change", ("REGISTRY_ADMISSION",)),
    (
        "invalid-paired-admission",
        "invalid-paired-admission",
        ("REGISTRY_ADMISSION",),
    ),
    (
        "baseline-path-on-standard",
        "baseline-path-on-standard",
        ("REGISTRY_ADMISSION",),
    ),
    (
        "duplicate-lifecycle-edge",
        "duplicate-lifecycle-edge",
        ("REGISTRY_LIFECYCLE",),
    ),
    ("invalid-lifecycle-state", "invalid-lifecycle-state", ("REGISTRY_LIFECYCLE",)),
    (
        "terminal-outgoing-edge",
        "terminal-outgoing-edge",
        ("REGISTRY_LIFECYCLE",),
    ),
    ("archived-lifecycle-edge", "archived-lifecycle-edge", ("REGISTRY_LIFECYCLE",)),
    ("missing-terminal-state", "missing-terminal-state", ("REGISTRY_LIFECYCLE",)),
    ("archived-terminal-state", "archived-terminal-state", ("REGISTRY_LIFECYCLE",)),
    (
        "unknown-evidence-profile",
        "unknown-evidence-profile",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "unknown-evidence-state",
        "unknown-evidence-state",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "executable-evidence-predicate",
        "executable-evidence-predicate",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "missing-edge-predicate-case",
        "missing-edge-predicate-case",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "duplicate-edge-predicate-case",
        "duplicate-edge-predicate-case",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "production-legacy-v6-input",
        "production-legacy-v6-input",
        ("REGISTRY_SCHEMA",),
    ),
    (
        "archive-conflicting-value-semantics",
        "archive-conflicting-value-semantics",
        ("REGISTRY_VALUE_CONTRACT",),
    ),
    (
        "evidence-capability-removal",
        "evidence-capability-removal",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    (
        "evidence-same-diff-swap",
        "evidence-same-diff-swap",
        ("REGISTRY_EVIDENCE_PREDICATE",),
    ),
    ("duplicate-json-root-key", "duplicate-json-root-key", ("REGISTRY_SCHEMA",)),
    (
        "duplicate-json-nested-key",
        "duplicate-json-nested-key",
        ("REGISTRY_SCHEMA",),
    ),
    (
        "guide-role-copied-to-runbook",
        "guide-role-copied-to-runbook",
        ("REGISTRY_ROLE_DECISION",),
    ),
    (
        "policy-role-copied-to-runbook",
        "policy-role-copied-to-runbook",
        ("REGISTRY_ROLE_DECISION",),
    ),
    (
        "incident-role-copied-to-postmortem",
        "incident-role-copied-to-postmortem",
        ("REGISTRY_ROLE_DECISION",),
    ),
    (
        "tests-role-copied-to-task",
        "tests-role-copied-to-task",
        ("REGISTRY_ROLE_DECISION",),
    ),
)

V8_MUTATIONS = frozenset(
    mutation
    for _, mutation, _ in EXPECTED_CASES
    if mutation
    in {
        "unknown-document-contract-field",
        "missing-value-contract",
        "invalid-value-kind",
        "invalid-value-enum",
        "invalid-value-constant",
        "invalid-value-pattern",
        "invalid-value-nullability",
        "invalid-value-condition",
        "missing-role-decision",
        "invalid-relationship-section",
        "invalid-body-requirement",
        "invalid-create-admission",
        "archive-admission-predicate-missing",
        "archive-evidence-capability-drift",
        "archive-evidence-shape-drift",
        "allow-delete",
        "allow-rename",
        "allow-profile-change",
        "invalid-paired-admission",
        "baseline-path-on-standard",
        "duplicate-lifecycle-edge",
        "invalid-lifecycle-state",
        "terminal-outgoing-edge",
        "archived-lifecycle-edge",
        "missing-terminal-state",
        "archived-terminal-state",
        "unknown-evidence-profile",
        "unknown-evidence-state",
        "executable-evidence-predicate",
        "missing-edge-predicate-case",
        "duplicate-edge-predicate-case",
        "production-legacy-v6-input",
        "archive-conflicting-value-semantics",
        "evidence-capability-removal",
        "evidence-same-diff-swap",
        "guide-role-copied-to-runbook",
        "policy-role-copied-to-runbook",
        "incident-role-copied-to-postmortem",
        "tests-role-copied-to-task",
    }
)

RAW_JSON_MUTATIONS = frozenset({"duplicate-json-root-key", "duplicate-json-nested-key"})


def _include_path_argument(raw: str) -> PurePosixPath:
    if raw.startswith("./"):
        raise argparse.ArgumentTypeError("include path must not start with './'")
    return PurePosixPath(raw)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--mode", choices=("compatibility", "strict"), default="compatibility"
    )
    parser.add_argument("--profile")
    parser.add_argument(
        "--include-path",
        action="append",
        default=[],
        metavar="REPOSITORY_PATH",
        type=_include_path_argument,
    )
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def _load_json(path: Path) -> Any:
    return load_json_file(path)


def _fixture_body_contract() -> dict[str, Any]:
    return {
        "section": "Traceability",
        "tableHeading": "Lifecycle Traceability",
        "enforcedStatuses": [],
        "requiredColumns": [
            "Requirement ID",
            "Acceptance criterion",
            "Downstream owner",
        ],
        "identifierColumns": [{"column": "Requirement ID", "kind": "requirement"}],
        "sourceLinkColumn": None,
        "targetLinkColumn": "Downstream owner",
        "allowedSourceProfileIds": [],
        "allowedTargetProfileIds": ["test/sample"],
        "reciprocalEvidence": True,
        "allowExplicitExclusion": True,
    }


def _fixture_lineage_profile(
    profile_id: str, route: str, status_domain: list[str]
) -> dict[str, Any]:
    return {
        "id": profile_id,
        "class": "sdlc",
        "mode": "authored",
        "routes": [{"kind": "regex", "value": route}],
        "frontmatter": {
            "mode": "required",
            "required": ["title", "type", "status", "owner", "updated"],
            "allowed": ["title", "type", "status", "owner", "updated"],
            "order": ["title", "type", "status", "owner", "updated"],
        },
        "statusDomain": status_domain,
        "headings": {"required": [], "allowed": []},
        "template": None,
        "sourceProfileIds": [],
        "placeholderPolicy": "forbidden",
        "appendContract": None,
        "bodyContract": None,
    }


def _fixture_standard_value_keys() -> list[dict[str, Any]]:
    return [
        {
            "key": "title",
            "kind": "string",
            "nullable": False,
            "constant": None,
            "enum": None,
            "pattern": r"\S",
            "conditional": {
                "key": "owner",
                "operator": "equals",
                "value": "platform",
                "effect": "required",
            },
        },
        {
            "key": "type",
            "kind": "string",
            "nullable": False,
            "constant": {"source": "profile-id", "value": None},
            "enum": None,
            "pattern": None,
            "conditional": None,
        },
        {
            "key": "status",
            "kind": "string",
            "nullable": False,
            "constant": None,
            "enum": {"source": "status-domain", "values": []},
            "pattern": None,
            "conditional": None,
        },
        {
            "key": "owner",
            "kind": "string",
            "nullable": False,
            "constant": None,
            "enum": None,
            "pattern": r"^[a-z][a-z0-9-]*$",
            "conditional": None,
        },
        {
            "key": "updated",
            "kind": "date",
            "nullable": False,
            "constant": None,
            "enum": None,
            "pattern": r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
            "conditional": None,
        },
    ]


def _fixture_document_contracts() -> dict[str, Any]:
    authored = [
        "governance/reference",
        "content/reference",
        "sdlc/prd",
        "sdlc/ard",
        "sdlc/adr",
        "sdlc/spec",
    ]
    snapshot = [
        "test/sample",
        "readme/collection-index",
        "readme/snapshot-pack",
        "template/sdlc/prd",
    ]
    return {
        "valueContracts": [
            {
                "id": "authored-standard",
                "profileIds": list(authored),
                "keys": _fixture_standard_value_keys(),
            },
            {"id": "frontmatter-free", "profileIds": snapshot[:-1], "keys": []},
        ],
        "roleDecisions": [
            {
                "profileIds": ["sdlc/prd"],
                "role": "product-requirement",
                "sourceProfileId": None,
                "relationshipSection": "Traceability",
                "bodyRequirement": "body-contract",
            },
            {
                "profileIds": [
                    "governance/reference",
                    "content/reference",
                    "sdlc/ard",
                    "sdlc/adr",
                    "sdlc/spec",
                ],
                "role": "fixture-authored",
                "sourceProfileId": None,
                "relationshipSection": None,
                "bodyRequirement": "none",
            },
            {
                "profileIds": snapshot[:-1],
                "role": "fixture-native",
                "sourceProfileId": None,
                "relationshipSection": None,
                "bodyRequirement": "none",
            },
        ],
        "admissionPolicies": [
            {
                "id": "authored-draft-only",
                "profileIds": list(authored),
                "create": {
                    "mode": "states",
                    "states": ["draft"],
                    "evidencePredicateId": None,
                },
                "delete": "deny",
                "rename": "deny",
                "profileChange": "deny",
                "baselinePaths": [],
            },
            {
                "id": "snapshot-only",
                "profileIds": snapshot,
                "create": {
                    "mode": "snapshot-only",
                    "states": [],
                    "evidencePredicateId": None,
                },
                "delete": "deny",
                "rename": "deny",
                "profileChange": "deny",
                "baselinePaths": [],
            },
        ],
        "lifecycleContracts": [
            {
                "id": "fixture-prd",
                "profileIds": ["sdlc/prd"],
                "terminalStates": ["active"],
                "edges": [
                    {
                        "from": "draft",
                        "to": "active",
                        "predicateId": "activate-self-body",
                    }
                ],
            },
            {
                "id": "fixture-non-lifecycle",
                "profileIds": [
                    *snapshot,
                    "governance/reference",
                    "content/reference",
                    "sdlc/ard",
                    "sdlc/adr",
                    "sdlc/spec",
                ],
                "terminalStates": [],
                "edges": [],
            },
        ],
        "evidencePredicates": [
            {
                "id": "activate-self-body",
                "profileEdges": [
                    {"profileId": "sdlc/prd", "from": "draft", "to": "active"}
                ],
                "evidence": [
                    {
                        "profileIds": ["$self"],
                        "states": ["active"],
                        "minimum": 1,
                        "maximum": 1,
                    }
                ],
                "relationship": "self",
                "cardinality": {"minimum": 1, "maximum": 1},
                "sameDiff": "self-status-and-body",
                "bodyRequirement": "body-contract",
                "capabilities": ["same-diff"],
            }
        ],
    }


def _minimal_fixture_registry() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://hy-home.k8s/schemas/document-profiles-8.schema.json",
        "schemaVersion": 8,
        "baseline": {"sha": BASELINE_SHA, "count": BASELINE_COUNT},
        "target": {"roots": [".agents"], "rootFiles": ["README.md"]},
        "profiles": [
            {
                "id": "test/sample",
                "class": "exception",
                "mode": "classification-only",
                "routes": [
                    {"kind": "exact", "value": SAMPLE_PATH.as_posix()},
                    {
                        "kind": "regex",
                        "value": (
                            "^tests/fixtures/document-contracts/self-test-.+\\.md$"
                        ),
                    },
                ],
                "frontmatter": {
                    "mode": "not-applicable",
                    "required": [],
                    "allowed": [],
                    "order": [],
                },
                "statusDomain": [],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": None,
            },
            {
                "id": "governance/reference",
                "class": "governance",
                "mode": "authored",
                "routes": [
                    {
                        "kind": "regex",
                        "value": "^docs/00\\.agent-governance/.+\\.md$",
                    }
                ],
                "frontmatter": {
                    "mode": "required",
                    "required": ["title", "type", "status", "owner", "updated"],
                    "allowed": ["title", "type", "status", "owner", "updated"],
                    "order": ["title", "type", "status", "owner", "updated"],
                },
                "statusDomain": ["draft", "active", "accepted", "done", "archived"],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": None,
            },
            {
                "id": "content/reference",
                "class": "common",
                "mode": "authored",
                "routes": [
                    {"kind": "exact", "value": path}
                    for path in REFERENCE_MEMBER_SAMPLE_PATHS
                ],
                "frontmatter": {
                    "mode": "required",
                    "required": ["title", "type", "status", "owner", "updated"],
                    "allowed": ["title", "type", "status", "owner", "updated"],
                    "order": ["title", "type", "status", "owner", "updated"],
                },
                "statusDomain": ["draft", "active", "accepted", "done", "archived"],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": None,
            },
            {
                "id": "readme/collection-index",
                "class": "readme",
                "mode": "frontmatter-free",
                "routes": [
                    {"kind": "exact", "value": path}
                    for path in REFERENCE_COLLECTION_SAMPLE_PATHS
                ],
                "frontmatter": {
                    "mode": "forbidden",
                    "required": [],
                    "allowed": [],
                    "order": [],
                },
                "statusDomain": [],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": None,
            },
            {
                "id": "readme/snapshot-pack",
                "class": "readme",
                "mode": "frontmatter-free",
                "routes": [
                    {"kind": "exact", "value": path}
                    for path in REFERENCE_PACK_SAMPLE_PATHS
                ],
                "frontmatter": {
                    "mode": "forbidden",
                    "required": [],
                    "allowed": [],
                    "order": [],
                },
                "statusDomain": [],
                "headings": {"required": [], "allowed": []},
                "template": None,
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": None,
            },
            {
                "id": "sdlc/prd",
                "class": "sdlc",
                "mode": "authored",
                "routes": [
                    {
                        "kind": "exact",
                        "value": "tests/fixtures/document-contracts/self-test-prd.md",
                    },
                    {
                        "kind": "regex",
                        "value": "^docs/01\\.requirements/[0-9]{3}-fixture\\.md$",
                    },
                ],
                "frontmatter": {
                    "mode": "required",
                    "required": ["title", "type", "status", "owner", "updated"],
                    "allowed": ["title", "type", "status", "owner", "updated"],
                    "order": ["title", "type", "status", "owner", "updated"],
                },
                "statusDomain": ["draft", "active"],
                "headings": {
                    "required": ["Overview", "Traceability"],
                    "allowed": ["Overview", "Traceability"],
                },
                "template": "tests/fixtures/document-contracts/self-test-prd.template.md",
                "sourceProfileIds": [],
                "placeholderPolicy": "forbidden",
                "appendContract": None,
                "bodyContract": _fixture_body_contract(),
            },
            {
                "id": "template/sdlc/prd",
                "class": "sdlc",
                "mode": "template",
                "routes": [
                    {
                        "kind": "exact",
                        "value": "tests/fixtures/document-contracts/self-test-prd.template.md",
                    }
                ],
                "frontmatter": {
                    "mode": "required",
                    "required": ["title", "type", "status", "owner", "updated"],
                    "allowed": ["title", "type", "status", "owner", "updated"],
                    "order": ["title", "type", "status", "owner", "updated"],
                },
                "statusDomain": ["draft", "active"],
                "headings": {
                    "required": ["Overview", "Traceability"],
                    "allowed": ["Overview", "Traceability"],
                },
                "template": "tests/fixtures/document-contracts/self-test-prd.template.md",
                "sourceProfileIds": ["sdlc/prd"],
                "placeholderPolicy": "template-only",
                "appendContract": None,
                "bodyContract": _fixture_body_contract(),
            },
            _fixture_lineage_profile(
                "sdlc/ard",
                "^docs/02\\.architecture/requirements/[0-9]{4}-fixture\\.md$",
                ["draft", "active", "accepted", "archived"],
            ),
            _fixture_lineage_profile(
                "sdlc/adr",
                "^docs/02\\.architecture/decisions/[0-9]{4}-fixture\\.md$",
                ["draft", "active", "accepted", "archived"],
            ),
            _fixture_lineage_profile(
                "sdlc/spec",
                "^docs/03\\.specs/[0-9]{3}-fixture/spec\\.md$",
                ["draft", "active", "done", "archived"],
            ),
        ],
        "governanceCurrentOwners": {
            "profileId": "governance/reference",
            "allowedStates": ["active", "accepted"],
            "paths": list(CURRENT_OWNER_SAMPLE_PATHS),
        },
        "referenceCurrentPacks": {
            "profileId": "content/reference",
            "packs": [
                {
                    "id": "audits/2026-07-11-test",
                    "allowedStates": ["done"],
                    "members": ["audit.md"],
                },
                {
                    "id": "research/2026-07-07-test",
                    "allowedStates": ["active", "accepted"],
                    "members": ["accepted.md", "active.md"],
                },
            ],
        },
        "documentContracts": _fixture_document_contracts(),
        "programLineage": {
            "programs": [
                {
                    "prd": "005",
                    "ard": "0008",
                    "tranches": [
                        {
                            "spec": "026",
                            "order": 1,
                            "state": "done",
                            "reason": "Original fixture tranche",
                            "decision": "0016",
                        }
                    ],
                    "followUps": [
                        {
                            "spec": "033",
                            "order": 1,
                            "state": "done",
                            "reason": "Historical fixture follow-up",
                            "decision": "0017",
                            "evidenceMode": "successor-record",
                        }
                    ],
                },
                {
                    "prd": "006",
                    "ard": "0009",
                    "tranches": [
                        {
                            "spec": "034",
                            "order": 1,
                            "state": "active",
                            "reason": "Current fixture tranche",
                            "decision": "0017",
                        }
                    ],
                    "followUps": [],
                },
            ]
        },
    }


def _convert_legacy_v5_fixture(raw_registry: dict[str, Any]) -> dict[str, Any]:
    """Convert the one historical v5 self-test shape; never used by production."""

    legacy = raw_registry["programLineage"]
    if (
        raw_registry.get("schemaVersion") != 5
        or raw_registry.get("$id")
        != "https://hy-home.k8s/schemas/document-profiles-5.schema.json"
        or set(legacy) != {"prd", "ard", "specs"}
    ):
        raise ValueError("not the closed legacy-v5 migration fixture")
    converted = copy.deepcopy(raw_registry)
    converted["$id"] = "https://hy-home.k8s/schemas/document-profiles-6.schema.json"
    converted["schemaVersion"] = 6
    tranches = []
    follow_ups = []
    for spec_id in legacy["specs"]:
        if spec_id == "033":
            follow_ups.append(
                {
                    "spec": spec_id,
                    "order": len(follow_ups) + 1,
                    "state": "done",
                    "reason": "Historical fixture follow-up",
                    "decision": "0017",
                    "evidenceMode": "successor-record",
                }
            )
        else:
            tranches.append(
                {
                    "spec": spec_id,
                    "order": len(tranches) + 1,
                    "state": "done",
                    "reason": "Original fixture tranche",
                    "decision": "0016",
                }
            )
    converted["programLineage"] = {
        "programs": [
            {
                "prd": legacy["prd"],
                "ard": legacy["ard"],
                "tranches": tranches,
                "followUps": follow_ups,
            }
        ]
    }
    return converted


def _convert_legacy_v6_fixture(raw_registry: dict[str, Any]) -> dict[str, Any]:
    """Convert the one private v6 self-test shape; never used by production."""

    if (
        raw_registry.get("schemaVersion") != 6
        or raw_registry.get("$id")
        != "https://hy-home.k8s/schemas/document-profiles-6.schema.json"
        or "documentContracts" in raw_registry
    ):
        raise ValueError("not the closed legacy-v6 migration fixture")
    converted = copy.deepcopy(raw_registry)
    converted["$id"] = "https://hy-home.k8s/schemas/document-profiles-8.schema.json"
    converted["schemaVersion"] = 8
    converted["documentContracts"] = _fixture_document_contracts()
    return converted


def _mutate(raw_registry: dict[str, Any], mutation: str) -> None:
    profile = next(
        (
            profile
            for profile in raw_registry["profiles"]
            if any(
                route.get("kind") == "exact"
                and route.get("value") == SAMPLE_PATH.as_posix()
                for route in profile["routes"]
            )
        ),
        raw_registry["profiles"][0],
    )
    route = next(
        (
            route
            for route in profile["routes"]
            if route.get("kind") == "exact"
            and route.get("value") == SAMPLE_PATH.as_posix()
        ),
        profile["routes"][0],
    )
    if mutation == "none":
        return
    if mutation == "duplicate-profile-id":
        raw_registry["profiles"].append(copy.deepcopy(profile))
        return
    if mutation == "route-kind-glob":
        route["kind"] = "glob"
        return
    if mutation == "drop-regex-end-anchor":
        regex_route = next(
            candidate
            for candidate in profile["routes"]
            if candidate.get("kind") == "regex"
        )
        regex_route["value"] = regex_route["value"].removesuffix("$")
        return
    if mutation == "add-overlapping-exact-route":
        profile["routes"].append({"kind": "exact", "value": SAMPLE_PATH.as_posix()})
        return
    if mutation == "remove-sample-route":
        profile["routes"].remove(route)
        return
    if mutation == "point-to-missing-template":
        profile["template"] = "docs/99.templates/templates/missing-document.md"
        return
    prd_profile = next(
        candidate
        for candidate in raw_registry["profiles"]
        if candidate["id"] == "sdlc/prd"
    )
    template_profile = next(
        candidate
        for candidate in raw_registry["profiles"]
        if candidate["id"] == "template/sdlc/prd"
    )
    if mutation == "remove-body-contract":
        del prd_profile["bodyContract"]
        return
    if mutation == "add-unknown-body-field":
        prd_profile["bodyContract"]["unknownField"] = True
        return
    if mutation == "change-body-section":
        prd_profile["bodyContract"]["section"] = "Missing Section"
        template_profile["bodyContract"]["section"] = "Missing Section"
        return
    if mutation == "add-unknown-body-status":
        prd_profile["bodyContract"]["enforcedStatuses"] = ["done"]
        template_profile["bodyContract"]["enforcedStatuses"] = ["done"]
        return
    if mutation == "empty-body-columns":
        prd_profile["bodyContract"]["requiredColumns"] = []
        return
    if mutation == "duplicate-body-column":
        prd_profile["bodyContract"]["requiredColumns"].append("Requirement ID")
        return
    if mutation == "unknown-body-source-profile":
        prd_profile["bodyContract"]["sourceLinkColumn"] = "Requirement ID"
        prd_profile["bodyContract"]["allowedSourceProfileIds"] = ["missing/source"]
        template_profile["bodyContract"]["sourceLinkColumn"] = "Requirement ID"
        template_profile["bodyContract"]["allowedSourceProfileIds"] = ["missing/source"]
        return
    if mutation == "unknown-body-target-profile":
        prd_profile["bodyContract"]["allowedTargetProfileIds"] = ["missing/target"]
        template_profile["bodyContract"]["allowedTargetProfileIds"] = ["missing/target"]
        return
    if mutation == "drift-template-body-contract":
        template_profile["bodyContract"]["requiredColumns"].append("Drift")
        return
    if mutation == "add-native-with-missing-template":
        native_profile = copy.deepcopy(profile)
        missing_form = FIXTURE_PATH.with_name("missing.template.native")
        target_basename = missing_form.name.replace(".template", "", 1)
        native_profile["id"] = f"{profile['id']}-native-missing-template"
        native_profile["routes"] = [
            {
                "kind": "regex",
                "value": (
                    "^"
                    + re.escape((SAMPLE_PATH.parent / target_basename).as_posix())
                    + "$"
                ),
            }
        ]
        native_profile["template"] = missing_form.as_posix()
        raw_registry["profiles"].append(native_profile)
        for family in (
            "valueContracts",
            "roleDecisions",
            "admissionPolicies",
            "lifecycleContracts",
        ):
            group = next(
                item
                for item in raw_registry["documentContracts"][family]
                if profile["id"] in item["profileIds"]
            )
            group["profileIds"].append(native_profile["id"])
        return
    if mutation == "add-overlapping-native-route":
        native_profile = copy.deepcopy(profile)
        native_profile["id"] = f"{profile['id']}-native-route-overlap"
        native_profile["routes"] = [{"kind": "exact", "value": SAMPLE_PATH.as_posix()}]
        raw_registry["profiles"].append(native_profile)
        for family in (
            "valueContracts",
            "roleDecisions",
            "admissionPolicies",
            "lifecycleContracts",
        ):
            group = next(
                item
                for item in raw_registry["documentContracts"][family]
                if profile["id"] in item["profileIds"]
            )
            group["profileIds"].append(native_profile["id"])
        return
    if mutation == "change-baseline-sha":
        raw_registry["baseline"]["sha"] = "0" * 40
        return
    if mutation == "change-baseline-count":
        raw_registry["baseline"]["count"] += 1
        return
    if mutation == "malform-governance-current-owners":
        raw_registry["governanceCurrentOwners"] = []
        return
    if mutation == "remove-governance-current-owners":
        del raw_registry["governanceCurrentOwners"]
        return
    if mutation == "invalidate-governance-current-owner-path":
        raw_registry["governanceCurrentOwners"]["paths"][0] = "../escape.md"
        return
    if mutation == "double-slash-governance-current-owner-path":
        raw_registry["governanceCurrentOwners"]["paths"][0] = (
            "docs/00.agent-governance//current-alpha.md"
        )
        return
    if mutation == "normalized-alias-governance-current-owner-duplicate":
        raw_registry["governanceCurrentOwners"]["paths"].insert(
            1, "docs/00.agent-governance//current-alpha.md"
        )
        return
    if mutation == "nul-governance-current-owner-path":
        raw_registry["governanceCurrentOwners"]["paths"][0] = (
            "docs/00.agent-governance/current-\x00owner.md"
        )
        return
    if mutation == "duplicate-governance-current-owner":
        raw_registry["governanceCurrentOwners"]["paths"].append(
            CURRENT_OWNER_SAMPLE_PATHS[0]
        )
        return
    if mutation == "reverse-governance-current-owners":
        raw_registry["governanceCurrentOwners"]["paths"].reverse()
        return
    if mutation == "missing-governance-current-owner":
        raw_registry["governanceCurrentOwners"]["paths"][1] = (
            "docs/00.agent-governance/current-zmissing.md"
        )
        return
    if mutation == "untracked-governance-current-owner":
        raw_registry["governanceCurrentOwners"]["paths"][1] = (
            "docs/00.agent-governance/current-untracked.md"
        )
        return
    if mutation == "symlink-governance-current-owner":
        raw_registry["governanceCurrentOwners"]["paths"][1] = (
            "docs/00.agent-governance/current-symlink.md"
        )
        return
    if mutation == "wrong-profile-governance-current-owner":
        governance_profile = next(
            candidate
            for candidate in raw_registry["profiles"]
            if candidate["id"] == "governance/reference"
        )
        governance_profile["id"] = "test/wrong-governance-profile"
        for family in (
            "valueContracts",
            "roleDecisions",
            "admissionPolicies",
            "lifecycleContracts",
        ):
            group = next(
                item
                for item in raw_registry["documentContracts"][family]
                if "governance/reference" in item["profileIds"]
            )
            group["profileIds"] = [
                "test/wrong-governance-profile"
                if profile_id == "governance/reference"
                else profile_id
                for profile_id in group["profileIds"]
            ]
        return
    if mutation == "non-authored-governance-current-owner":
        governance_profile = next(
            candidate
            for candidate in raw_registry["profiles"]
            if candidate["id"] == "governance/reference"
        )
        governance_profile["mode"] = "classification-only"
        authored_admission = next(
            item
            for item in raw_registry["documentContracts"]["admissionPolicies"]
            if "governance/reference" in item["profileIds"]
        )
        snapshot_admission = next(
            item
            for item in raw_registry["documentContracts"]["admissionPolicies"]
            if item["id"] == "snapshot-only"
        )
        authored_admission["profileIds"].remove("governance/reference")
        snapshot_admission["profileIds"].append("governance/reference")
        return
    if mutation == "reverse-governance-current-owner-states":
        raw_registry["governanceCurrentOwners"]["allowedStates"].reverse()
        return
    if mutation == "remove-governance-current-owner-states":
        del raw_registry["governanceCurrentOwners"]["allowedStates"]
        return
    packs = raw_registry["referenceCurrentPacks"]["packs"]
    research = next(item for item in packs if item["id"].startswith("research/"))
    if mutation == "malform-reference-current-packs":
        raw_registry["referenceCurrentPacks"] = []
        return
    if mutation == "remove-reference-current-packs":
        del raw_registry["referenceCurrentPacks"]
        return
    if mutation == "duplicate-reference-pack-id":
        packs[1] = copy.deepcopy(packs[0])
        return
    if mutation == "missing-reference-pack-collection":
        packs.pop()
        return
    if mutation == "extra-reference-pack-collection":
        packs.append(copy.deepcopy(packs[1]))
        packs[2]["id"] = "research/2026-07-08-extra"
        return
    if mutation == "reverse-reference-pack-ids":
        packs.reverse()
        return
    if mutation == "invalidate-reference-pack-id":
        research["id"] = "research/not-a-date"
        return
    if mutation == "parent-reference-member":
        research["members"][0] = "../accepted.md"
        return
    if mutation == "leading-dot-reference-member":
        research["members"][0] = "./accepted.md"
        return
    if mutation == "slash-reference-member":
        research["members"][0] = "nested/accepted.md"
        return
    if mutation == "control-reference-member":
        research["members"][0] = "accepted-\x00.md"
        return
    if mutation == "normalized-alias-reference-member":
        research["members"][0] = "accepted//.md"
        return
    if mutation == "duplicate-reference-member":
        research["members"].append(research["members"][0])
        return
    if mutation == "reverse-reference-members":
        research["members"].reverse()
        return
    if mutation == "wrong-reference-pack-states":
        research["allowedStates"].reverse()
        return
    if mutation == "remove-reference-pack-states":
        del research["allowedStates"]
        return
    if mutation == "outside-reference-profile-state":
        research["allowedStates"] = ["active", "unknown"]
        return
    if mutation == "missing-reference-member":
        research["members"][0] = "missing.md"
        research["members"].sort()
        return
    if mutation == "untracked-reference-member":
        research["members"][0] = "untracked.md"
        research["members"].sort()
        return
    if mutation == "symlink-reference-member":
        research["members"][0] = "symlink.md"
        research["members"].sort()
        return
    if mutation == "non-regular-reference-member":
        research["members"][0] = "directory.md"
        research["members"].sort()
        return
    if mutation == "wrong-profile-reference-member":
        target = REFERENCE_MEMBER_SAMPLE_PATHS[1]
        content_profile = next(
            item
            for item in raw_registry["profiles"]
            if item["id"] == "content/reference"
        )
        content_profile["routes"] = [
            route for route in content_profile["routes"] if route["value"] != target
        ]
        profile["routes"].append({"kind": "exact", "value": target})
        return
    if mutation == "wrong-profile-reference-pack-readme":
        target = REFERENCE_PACK_SAMPLE_PATHS[1]
        pack_profile = next(
            item
            for item in raw_registry["profiles"]
            if item["id"] == "readme/snapshot-pack"
        )
        pack_profile["routes"] = [
            route for route in pack_profile["routes"] if route["value"] != target
        ]
        profile["routes"].append({"kind": "exact", "value": target})
        return
    if mutation == "wrong-profile-reference-collection-readme":
        target = REFERENCE_COLLECTION_SAMPLE_PATHS[1]
        collection_profile = next(
            item
            for item in raw_registry["profiles"]
            if item["id"] == "readme/collection-index"
        )
        collection_profile["routes"] = [
            route for route in collection_profile["routes"] if route["value"] != target
        ]
        profile["routes"].append({"kind": "exact", "value": target})
        return
    programs = raw_registry["programLineage"]["programs"]
    original = programs[0]
    current = programs[1]
    if mutation == "duplicate-program":
        duplicate = copy.deepcopy(current)
        duplicate["prd"] = original["prd"]
        duplicate["ard"] = original["ard"]
        duplicate["tranches"][0]["spec"] = "035"
        programs.insert(1, duplicate)
        return
    if mutation == "reverse-programs":
        programs.reverse()
        return
    if mutation == "duplicate-program-member":
        duplicate = copy.deepcopy(original["tranches"][0])
        duplicate["order"] = 2
        original["tranches"].append(duplicate)
        return
    if mutation == "overlap-program-member":
        overlap = copy.deepcopy(original["followUps"][0])
        overlap.pop("evidenceMode")
        overlap["order"] = 2
        overlap["decision"] = "0016"
        original["tranches"].append(overlap)
        return
    if mutation == "noncontiguous-program-order":
        original["tranches"][0]["order"] = 2
        return
    if mutation == "unknown-program-prd":
        current["prd"] = "999"
        return
    if mutation == "unknown-program-ard":
        current["ard"] = "9999"
        return
    if mutation == "unknown-program-adr":
        current["tranches"][0]["decision"] = "9999"
        return
    if mutation == "unknown-program-spec":
        current["tranches"][0]["spec"] = "999"
        return
    if mutation == "program-state-drift":
        original["tranches"][0]["state"] = "active"
        return
    if mutation == "program-decision-not-accepted":
        current["tranches"][0]["decision"] = "0018"
        return
    if mutation == "program-decision-missing":
        del current["tranches"][0]["decision"]
        return
    if mutation == "invalid-program-evidence-mode":
        original["followUps"][0]["evidenceMode"] = "implicit"
        return
    if mutation == "program-follow-up-predates-tranche":
        original["followUps"][0]["decision"] = "0015"
        original["followUps"][0]["evidenceMode"] = "reciprocal-body"
        return
    if mutation == "production-legacy-v5-input":
        raw_registry["$id"] = (
            "https://hy-home.k8s/schemas/document-profiles-5.schema.json"
        )
        raw_registry["schemaVersion"] = 5
        raw_registry["programLineage"] = {
            "prd": "005",
            "ard": "0008",
            "specs": ["026", "033"],
        }
        return
    if mutation == "duplicate-program-spec-status-key":
        current["tranches"][0]["spec"] = "036"
        return
    if mutation == "duplicate-program-adr-updated-key":
        current["tranches"][0]["decision"] = "0019"
        return
    if mutation == "timestamp-program-adr-updated":
        current["tranches"][0]["decision"] = "0020"
        return
    if mutation == "misordered-follow-up-approval":
        current["followUps"] = [
            {
                "spec": "038",
                "order": 1,
                "state": "active",
                "reason": "Later-approved fixture follow-up declared first",
                "decision": "0022",
                "evidenceMode": "reciprocal-body",
            },
            {
                "spec": "039",
                "order": 2,
                "state": "active",
                "reason": "Earlier-approved fixture follow-up declared second",
                "decision": "0021",
                "evidenceMode": "reciprocal-body",
            },
        ]
        return
    contracts = raw_registry.get("documentContracts")
    if mutation == "unknown-document-contract-field":
        contracts["expression"] = "allow()"
        return
    if mutation == "missing-value-contract":
        group = next(
            item
            for item in contracts["valueContracts"]
            if "sdlc/prd" in item["profileIds"]
        )
        group["profileIds"].remove("sdlc/prd")
        return
    role_copy_profiles = {
        "guide-role-copied-to-runbook": ("sdlc/guide", "sdlc/runbook"),
        "policy-role-copied-to-runbook": ("sdlc/policy", "sdlc/runbook"),
        "incident-role-copied-to-postmortem": (
            "sdlc/incident",
            "sdlc/postmortem",
        ),
        "tests-role-copied-to-task": ("sdlc/tests", "sdlc/task"),
    }
    if mutation in role_copy_profiles:
        source_profile, target_profile = role_copy_profiles[mutation]
        source = next(
            item
            for item in contracts["roleDecisions"]
            if source_profile in item["profileIds"]
        )
        target = next(
            item
            for item in contracts["roleDecisions"]
            if target_profile in item["profileIds"]
        )
        target["role"] = source["role"]
        return
    value_group = next(
        item for item in contracts["valueContracts"] if "sdlc/prd" in item["profileIds"]
    )
    value_keys = {item["key"]: item for item in value_group["keys"]}
    if mutation == "invalid-value-kind":
        value_keys["title"]["kind"] = "yaml"
        return
    if mutation == "invalid-value-enum":
        value_keys["status"]["enum"]["values"] = ["draft"]
        return
    if mutation == "invalid-value-constant":
        value_keys["type"]["constant"]["value"] = "sdlc/wrong"
        return
    if mutation == "invalid-value-pattern":
        value_keys["title"]["pattern"] = "("
        return
    if mutation == "invalid-value-nullability":
        value_keys["title"]["nullable"] = "sometimes"
        return
    if mutation == "invalid-value-condition":
        value_keys["title"]["conditional"] = {
            "key": "missing",
            "operator": "equals",
            "value": "x",
            "effect": "required",
        }
        return
    role = next(
        item for item in contracts["roleDecisions"] if "sdlc/prd" in item["profileIds"]
    )
    if mutation == "missing-role-decision":
        role["profileIds"].remove("sdlc/prd")
        return
    if mutation == "invalid-relationship-section":
        role["relationshipSection"] = "Related Documents"
        return
    if mutation == "invalid-body-requirement":
        role["bodyRequirement"] = "heading-set"
        return
    admission = next(
        item
        for item in contracts["admissionPolicies"]
        if "sdlc/prd" in item["profileIds"]
    )
    if mutation == "invalid-create-admission":
        admission["create"]["states"] = ["active"]
        return
    if mutation == "archive-admission-predicate-missing":
        archive_admission = next(
            item
            for item in contracts["admissionPolicies"]
            if item["id"] == "archive-envelope-only"
        )
        archive_admission["create"]["evidencePredicateId"] = None
        return
    if mutation in {
        "archive-evidence-capability-drift",
        "archive-evidence-shape-drift",
    }:
        archive_predicate = next(
            item
            for item in contracts["evidencePredicates"]
            if item["id"] == "archive-source-removal"
        )
        if mutation == "archive-evidence-capability-drift":
            archive_predicate["capabilities"].remove("source-removal")
        else:
            archive_predicate["relationship"] = "self"
        return
    if mutation == "allow-delete":
        admission["delete"] = "allow"
        return
    if mutation == "allow-rename":
        admission["rename"] = "allow"
        return
    if mutation == "allow-profile-change":
        admission["profileChange"] = "allow"
        return
    if mutation == "invalid-paired-admission":
        paired = next(
            item
            for item in contracts["admissionPolicies"]
            if item["id"] == "execution-reciprocal-pair"
        )
        admission["profileIds"].remove("sdlc/prd")
        paired["profileIds"].append("sdlc/prd")
        return
    if mutation == "baseline-path-on-standard":
        admission["baselinePaths"].append("docs/example.md")
        return
    lifecycle = next(
        item
        for item in contracts["lifecycleContracts"]
        if "sdlc/prd" in item["profileIds"]
    )
    if mutation == "duplicate-lifecycle-edge":
        lifecycle["edges"].append(copy.deepcopy(lifecycle["edges"][0]))
        return
    if mutation == "invalid-lifecycle-state":
        lifecycle["edges"][0]["from"] = ""
        return
    if mutation in {"terminal-outgoing-edge", "archived-lifecycle-edge"}:
        edge = (
            {"from": "done", "to": "active", "predicateId": "activate-self-body"}
            if mutation == "terminal-outgoing-edge"
            else {
                "from": "active",
                "to": "archived",
                "predicateId": "activate-self-body",
            }
        )
        lifecycle["edges"].append(edge)
        predicate = next(
            item
            for item in contracts["evidencePredicates"]
            if item["id"] == "activate-self-body"
        )
        predicate["profileEdges"].append(
            {"profileId": "sdlc/prd", "from": edge["from"], "to": edge["to"]}
        )
        return
    if mutation == "missing-terminal-state":
        lifecycle["terminalStates"] = []
        return
    if mutation == "archived-terminal-state":
        lifecycle["terminalStates"].append("archived")
        return
    predicate = next(
        item
        for item in contracts["evidencePredicates"]
        if item["id"] == "activate-self-body"
    )
    if mutation == "unknown-evidence-profile":
        predicate["evidence"][0]["profileIds"] = ["sdlc/unknown"]
        return
    if mutation == "unknown-evidence-state":
        predicate["evidence"][0]["states"] = ["accepted"]
        return
    if mutation == "executable-evidence-predicate":
        predicate["expression"] = "document.status == 'active'"
        return
    if mutation == "missing-edge-predicate-case":
        predicate["profileEdges"].pop()
        return
    if mutation == "duplicate-edge-predicate-case":
        predicate["profileEdges"].append(copy.deepcopy(predicate["profileEdges"][0]))
        return
    if mutation == "production-legacy-v6-input":
        raw_registry["$id"] = (
            "https://hy-home.k8s/schemas/document-profiles-6.schema.json"
        )
        raw_registry["schemaVersion"] = 6
        del raw_registry["documentContracts"]
        return
    if mutation == "archive-conflicting-value-semantics":
        archive_values = next(
            item
            for item in contracts["valueContracts"]
            if item["id"] == "archive-record"
        )
        archive_reason = next(
            item for item in archive_values["keys"] if item["key"] == "archive_reason"
        )
        archive_reason["constant"] = {"source": "literal", "value": "superseded"}
        return
    if mutation == "evidence-capability-removal":
        predicate["capabilities"].remove("same-diff")
        return
    if mutation == "evidence-same-diff-swap":
        predicate["sameDiff"] = "pair-status-changed"
        return
    raise ValueError(f"unsupported fixture mutation: {mutation}")


def _ordered_rule_ids(diagnostics: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item.rule_id for item in diagnostics))


def _assert_inventory_safety(root: Path) -> None:
    fixture_dir = root / "tests/fixtures/document-contracts"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="document-contract-",
        suffix=".md",
        dir=fixture_dir,
        delete=False,
    ) as handle:
        handle.write("# Explicit include self-test\n")
        candidate = Path(handle.name)

    try:
        relative = PurePosixPath(candidate.relative_to(root).as_posix())
        inventory = enumerate_target_markdown(root, include_paths=(relative,))
        if relative not in inventory.current_paths:
            raise AssertionError(
                "explicit untracked Markdown include was not inventoried"
            )
    finally:
        candidate.unlink(missing_ok=True)

    rejected = (
        (PurePosixPath("_workspace/document-contract-ignored.md"), "ignored"),
        (PurePosixPath(".codex/skills"), "symlink"),
    )
    for path, expected_fragment in rejected:
        try:
            enumerate_target_markdown(root, include_paths=(path,))
        except ValueError as exc:
            if expected_fragment not in str(exc):
                raise AssertionError(
                    f"{path}: expected {expected_fragment!r} rejection, got {exc!r}"
                ) from exc
        else:
            raise AssertionError(f"unsafe explicit include was accepted: {path}")


def _assert_program_lineage_projection(registry: Registry) -> None:
    immutable_actual = tuple(
        (
            program.prd_id,
            program.ard_id,
            tuple(
                (
                    relation.spec_id,
                    relation.order,
                    relation.decision_id,
                )
                for relation in program.tranches
            ),
            tuple(
                (
                    relation.spec_id,
                    relation.order,
                    relation.decision_id,
                    relation.evidence_mode,
                )
                for relation in program.follow_ups
            ),
        )
        for program in registry.program_lineage
    )
    immutable_expected = (
        (
            "005",
            "0008",
            tuple(
                (f"{spec_id:03d}", order, "0016")
                for order, spec_id in enumerate(range(26, 33), 1)
            ),
            (("033", 1, "0017", "successor-record"),),
        ),
        (
            "006",
            "0009",
            (
                ("034", 1, "0017"),
                ("035", 2, "0017"),
                ("036", 3, "0017"),
                ("037", 4, "0017"),
                ("038", 5, "0017"),
                ("039", 6, "0017"),
                ("040", 7, "0017"),
            ),
            (),
        ),
    )
    if immutable_actual != immutable_expected:
        raise AssertionError("production program-lineage immutable projection differs")

    def assert_state_contract(candidate: Registry) -> None:
        for program in candidate.program_lineage:
            states = tuple(relation.state for relation in program.tranches)
            completed = tuple(state == "done" for state in states)
            if states and completed != tuple(
                index < sum(completed) for index in range(len(states))
            ):
                raise AssertionError(
                    f"PRD-{program.prd_id} original tranche is not one "
                    "contiguous done prefix followed by an active suffix"
                )
            if any(state not in {"done", "active"} for state in states):
                raise AssertionError(
                    f"PRD-{program.prd_id} original tranche state domain differs"
                )
        historical = next(
            program for program in candidate.program_lineage if program.prd_id == "005"
        )
        if any(relation.state != "done" for relation in historical.tranches):
            raise AssertionError("PRD-005 historical original tranche is not terminal")
        if any(relation.state != "done" for relation in historical.follow_ups):
            raise AssertionError("PRD-005 historical follow-up is not terminal")

    # Keep mutable relation state separate from immutable lineage identity.
    # Cross-document strict validation owns current Spec-to-relation parity;
    # this self-test owns the typed registry's contiguous state invariant and
    # both first-unfinished positions used by the current rollover.
    assert_state_contract(registry)
    current = next(
        program for program in registry.program_lineage if program.prd_id == "006"
    )
    for ready_spec_id in ("035", "036"):
        ready_order = next(
            relation.order
            for relation in current.tranches
            if relation.spec_id == ready_spec_id
        )
        candidate_program = replace(
            current,
            tranches=tuple(
                replace(
                    relation,
                    state="done" if relation.order < ready_order else "active",
                )
                for relation in current.tranches
            ),
        )
        candidate = replace(
            registry,
            program_lineage=tuple(
                candidate_program if program.prd_id == "006" else program
                for program in registry.program_lineage
            ),
        )
        assert_state_contract(candidate)

    invalid_program = replace(
        current,
        tranches=tuple(
            replace(relation, state="done" if relation.order in {1, 3} else "active")
            for relation in current.tranches
        ),
    )
    invalid_candidate = replace(
        registry,
        program_lineage=tuple(
            invalid_program if program.prd_id == "006" else program
            for program in registry.program_lineage
        ),
    )
    try:
        assert_state_contract(invalid_candidate)
    except AssertionError:
        pass
    else:
        raise AssertionError("noncontiguous original-tranche state mutation accepted")


def _assert_document_contract_projection(registry: Registry) -> None:
    if registry.schema_version != 8 or len(registry.profiles) != 64:
        raise AssertionError("production v8 profile projection differs")
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    expected_predicate_order = (
        "archive-source-removal",
        "activate-self-body",
        "activate-heading-profile",
        "activate-execution-pair",
        "complete-product-program",
        "accept-architecture",
        "accept-decision-self",
        "complete-specification",
        "complete-execution-pair",
        "accept-operated-document",
        "terminate-reviewed-reference",
    )
    if (
        tuple(predicate.predicate_id for predicate in registry.evidence_predicates)
        != expected_predicate_order
    ):
        raise AssertionError("production evidence-predicate order differs")

    def edges(
        profile_ids: tuple[str, ...], from_state: str, to_state: str
    ) -> set[tuple[str, str, str]]:
        return {(profile_id, from_state, to_state) for profile_id in profile_ids}

    specifications = (
        "sdlc/spec",
        "sdlc/api-spec",
        "sdlc/agent-design",
        "sdlc/data-model",
        "sdlc/tests",
    )
    operations = (
        "sdlc/guide",
        "sdlc/policy",
        "sdlc/runbook",
        "sdlc/incident",
        "sdlc/postmortem",
    )
    references = (
        "content/reference",
        "governance/reference",
        "governance/memory",
        "governance/template-support",
    )
    expected_edges = {
        "archive-source-removal": set(),
        "activate-self-body": edges(
            ("sdlc/prd", "sdlc/ard", "sdlc/adr", *specifications, *operations),
            "draft",
            "active",
        ),
        "activate-heading-profile": edges(references, "draft", "active"),
        "activate-execution-pair": edges(("sdlc/plan", "sdlc/task"), "draft", "active"),
        "complete-product-program": edges(("sdlc/prd",), "active", "done"),
        "accept-architecture": edges(("sdlc/ard",), "active", "accepted"),
        "accept-decision-self": edges(("sdlc/adr",), "active", "accepted"),
        "complete-specification": edges(specifications, "active", "done"),
        "complete-execution-pair": edges(("sdlc/plan", "sdlc/task"), "active", "done"),
        "accept-operated-document": edges(operations, "active", "accepted"),
        "terminate-reviewed-reference": (
            edges(references, "active", "accepted")
            | edges(references, "active", "done")
        ),
    }
    actual_edges = {
        predicate.predicate_id: {
            (edge.profile_id, edge.from_state, edge.to_state)
            for edge in predicate.profile_edges
        }
        for predicate in registry.evidence_predicates
    }
    if actual_edges != expected_edges:
        raise AssertionError("production exact edge/predicate projection differs")

    standard_sources = (
        "sdlc/prd",
        "sdlc/ard",
        "sdlc/adr",
        "sdlc/spec",
        "sdlc/api-spec",
        "sdlc/agent-design",
        "sdlc/data-model",
        "sdlc/tests",
        "sdlc/plan",
        "sdlc/task",
        "sdlc/guide",
        "sdlc/policy",
        "sdlc/runbook",
        "sdlc/incident",
        "sdlc/postmortem",
        "content/reference",
        "governance/reference",
        "governance/memory",
        "governance/template-support",
    )
    standard_templates = (
        "template/content/reference",
        "template/sdlc/adr",
        "template/sdlc/ard",
        "template/sdlc/plan",
        "template/sdlc/task",
        "template/sdlc/guide",
        "template/sdlc/incident",
        "template/sdlc/policy",
        "template/sdlc/postmortem",
        "template/sdlc/runbook",
        "template/sdlc/prd",
        "template/sdlc/agent-design",
        "template/sdlc/api-spec",
        "template/sdlc/data-model",
        "template/sdlc/spec",
        "template/sdlc/tests",
        "template/governance/memory",
        "template/governance/reference",
        "template/governance/template-support",
    )
    empty_sources = (
        "governance/progress-ledger",
        "readme/repository",
        "readme/stage-index",
        "readme/collection-index",
        "readme/implementation",
        "readme/snapshot-pack",
        "readme/workspace-staging",
        "exception/root-provider-shim",
        "exception/local-agent-asset",
        "exception/repository-runtime-baseline",
        "exception/provider-native-metadata",
        "exception/github-native-control",
        "exception/native-contract-openapi",
        "exception/native-contract-graphql",
        "exception/native-contract-protobuf",
        "exception/generated-record",
        "exception/program-non-target",
    )
    empty_templates = (
        "template/readme/repository",
        "template/readme/stage-index",
        "template/readme/collection-index",
        "template/readme/implementation",
        "template/readme/snapshot-pack",
        "template/readme/workspace-staging",
        "governance/progress-entry",
    )

    def key_signature(item: Any) -> tuple[Any, ...]:
        return (
            item.key,
            item.kind,
            item.nullable,
            (
                None
                if item.constant is None
                else (item.constant.source, item.constant.value)
            ),
            (None if item.enum is None else (item.enum.source, item.enum.values)),
            item.pattern,
            (
                None
                if item.conditional is None
                else (
                    item.conditional.key,
                    item.conditional.operator,
                    item.conditional.value,
                    item.conditional.effect,
                )
            ),
        )

    standard_keys = (
        ("title", "string", False, None, None, r"\S", None),
        ("type", "string", False, ("profile-id", None), None, None, None),
        (
            "status",
            "string",
            False,
            None,
            ("status-domain", ()),
            None,
            None,
        ),
        ("owner", "string", False, None, None, r"^[a-z][a-z0-9-]*$", None),
        (
            "updated",
            "date",
            False,
            None,
            None,
            r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
            None,
        ),
    )
    archive_keys = (
        *standard_keys[:2],
        ("status", "string", False, ("literal", "archived"), None, None, None),
        *standard_keys[3:],
        (
            "original_type",
            "string",
            False,
            None,
            None,
            r"^[a-z][a-z0-9-]*(?:/[a-z0-9-]+)?$",
            None,
        ),
        ("original_path", "string", False, None, None, r"^[^/\\].+", None),
        (
            "archived_on",
            "date",
            False,
            None,
            None,
            r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$",
            None,
        ),
        (
            "archive_reason",
            "string",
            False,
            None,
            (
                "literal",
                (
                    "superseded",
                    "consolidated",
                    "completed-lineage",
                    "retired",
                    "abandoned",
                    "duplicate",
                ),
            ),
            None,
            None,
        ),
        ("replacement", "string", True, None, None, r"^[^/\\].+", None),
        (
            "source_commit",
            "string",
            False,
            None,
            None,
            r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$",
            None,
        ),
        (
            "source_blob",
            "string",
            False,
            None,
            None,
            r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$",
            None,
        ),
        (
            "content_sha256",
            "string",
            False,
            None,
            None,
            r"^[0-9a-f]{64}$",
            None,
        ),
    )
    expected_value_projection: dict[str, tuple[Any, ...]] = {}
    for profile_id in (*standard_sources, *standard_templates):
        expected_value_projection[profile_id] = (
            "authored-standard",
            standard_sources,
            standard_keys,
        )
    for profile_id in (
        "content/archive",
        "template/content/archive",
    ):
        expected_value_projection[profile_id] = (
            "archive-record",
            ("content/archive",),
            archive_keys,
        )
    for profile_id in (*empty_sources, *empty_templates):
        expected_value_projection[profile_id] = (
            "frontmatter-free-or-native",
            empty_sources,
            (),
        )
    actual_value_projection = {
        profile_id: (
            profile.value_contract.contract_id,
            profile.value_contract.profile_ids,
            tuple(key_signature(item) for item in profile.value_contract.keys),
        )
        for profile_id, profile in profiles.items()
    }
    if actual_value_projection != expected_value_projection:
        raise AssertionError("production complete value projection differs")

    expected_roles: dict[str, tuple[str, str | None, str | None, str]] = {
        "sdlc/prd": ("product-requirement", None, "Traceability", "body-contract"),
        "sdlc/ard": ("architecture-requirement", None, "Traceability", "body-contract"),
        "sdlc/adr": ("architecture-decision", None, "Traceability", "body-contract"),
        "sdlc/spec": (
            "implementation-specification",
            None,
            "Traceability",
            "body-contract",
        ),
        "sdlc/api-spec": ("api-specification", None, "Traceability", "body-contract"),
        "sdlc/agent-design": ("agent-design", None, "Traceability", "body-contract"),
        "sdlc/data-model": ("data-model", None, "Traceability", "body-contract"),
        "sdlc/tests": ("test-contract", None, "Traceability", "body-contract"),
        "sdlc/plan": ("execution-plan", None, "Traceability", "body-contract"),
        "sdlc/task": ("execution-task", None, "Traceability", "body-contract"),
        "sdlc/guide": ("operator-guide", None, "Traceability", "body-contract"),
        "sdlc/policy": ("control-policy", None, "Traceability", "body-contract"),
        "sdlc/runbook": ("operator-runbook", None, "Traceability", "body-contract"),
        "sdlc/incident": (
            "incident-fact-record",
            None,
            "Traceability",
            "body-contract",
        ),
        "sdlc/postmortem": (
            "post-incident-analysis",
            None,
            "Traceability",
            "body-contract",
        ),
        "content/reference": ("reference", None, "Related Documents", "heading-set"),
        "content/archive": (
            "archive-record",
            None,
            None,
            "none",
        ),
        "governance/reference": (
            "governance-reference",
            None,
            "Related Documents",
            "heading-set",
        ),
        "governance/memory": (
            "governance-memory",
            None,
            "Related Progress",
            "heading-set",
        ),
        "governance/template-support": (
            "template-support",
            None,
            "Related Documents",
            "heading-set",
        ),
        "governance/progress-ledger": ("progress-ledger", None, None, "none"),
        "readme/repository": (
            "repository-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
        "readme/stage-index": (
            "stage-index-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
        "readme/collection-index": (
            "collection-index-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
        "readme/implementation": (
            "implementation-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
        "readme/snapshot-pack": (
            "snapshot-pack-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
        "readme/workspace-staging": (
            "workspace-staging-readme",
            None,
            "Related Documents",
            "heading-set",
        ),
    }
    for profile_id in (
        "exception/root-provider-shim",
        "exception/local-agent-asset",
        "exception/repository-runtime-baseline",
        "exception/provider-native-metadata",
        "exception/github-native-control",
        "exception/generated-record",
        "exception/program-non-target",
    ):
        expected_roles[profile_id] = ("native-repository-surface", None, None, "none")
    for profile_id in (
        "exception/native-contract-openapi",
        "exception/native-contract-graphql",
        "exception/native-contract-protobuf",
    ):
        expected_roles[profile_id] = ("native-machine-contract", None, None, "none")
    template_sources = {
        "template/content/archive": "content/archive",
        "template/governance/memory": "governance/memory",
        "template/readme/repository": "readme/repository",
        "template/readme/stage-index": "readme/stage-index",
        "template/readme/collection-index": "readme/collection-index",
        "template/readme/implementation": "readme/implementation",
        "template/readme/snapshot-pack": "readme/snapshot-pack",
        "template/readme/workspace-staging": "readme/workspace-staging",
        "template/content/reference": "content/reference",
        "template/sdlc/adr": "sdlc/adr",
        "template/sdlc/ard": "sdlc/ard",
        "template/sdlc/plan": "sdlc/plan",
        "template/sdlc/task": "sdlc/task",
        "template/sdlc/guide": "sdlc/guide",
        "template/sdlc/incident": "sdlc/incident",
        "template/sdlc/policy": "sdlc/policy",
        "template/sdlc/postmortem": "sdlc/postmortem",
        "template/sdlc/runbook": "sdlc/runbook",
        "template/sdlc/prd": "sdlc/prd",
        "template/sdlc/agent-design": "sdlc/agent-design",
        "template/sdlc/api-spec": "sdlc/api-spec",
        "template/sdlc/data-model": "sdlc/data-model",
        "template/sdlc/spec": "sdlc/spec",
        "template/sdlc/tests": "sdlc/tests",
        "governance/progress-entry": "governance/progress-ledger",
        "template/governance/reference": "governance/reference",
        "template/governance/template-support": "governance/template-support",
    }
    for template_id, source_id in template_sources.items():
        role, _, relationship, body_requirement = expected_roles[source_id]
        expected_roles[template_id] = (
            role,
            source_id,
            relationship,
            body_requirement,
        )
    actual_roles = {
        profile_id: (
            profile.role_decision.role,
            profile.role_decision.source_profile_id,
            profile.role_decision.relationship_section,
            profile.role_decision.body_requirement,
        )
        for profile_id, profile in profiles.items()
    }
    if actual_roles != expected_roles or len(expected_roles) != 64:
        raise AssertionError("production complete role/source projection differs")

    authored_draft = tuple(
        profile_id
        for profile_id in standard_sources
        if profile_id not in {"sdlc/plan", "sdlc/task"}
    )
    snapshot_profiles = (
        "governance/progress-ledger",
        "readme/repository",
        "readme/stage-index",
        "readme/collection-index",
        "readme/implementation",
        "readme/snapshot-pack",
        "readme/workspace-staging",
        "exception/root-provider-shim",
        "exception/local-agent-asset",
        "exception/repository-runtime-baseline",
        "exception/provider-native-metadata",
        "exception/github-native-control",
        "exception/native-contract-openapi",
        "exception/native-contract-graphql",
        "exception/native-contract-protobuf",
        "exception/generated-record",
        "exception/program-non-target",
        "template/content/archive",
        "template/governance/memory",
        "template/readme/repository",
        "template/readme/stage-index",
        "template/readme/collection-index",
        "template/readme/implementation",
        "template/readme/snapshot-pack",
        "template/readme/workspace-staging",
        "template/content/reference",
        "template/sdlc/adr",
        "template/sdlc/ard",
        "template/sdlc/plan",
        "template/sdlc/task",
        "template/sdlc/guide",
        "template/sdlc/incident",
        "template/sdlc/policy",
        "template/sdlc/postmortem",
        "template/sdlc/runbook",
        "template/sdlc/prd",
        "template/sdlc/agent-design",
        "template/sdlc/api-spec",
        "template/sdlc/data-model",
        "template/sdlc/spec",
        "template/sdlc/tests",
        "governance/progress-entry",
        "template/governance/reference",
        "template/governance/template-support",
    )

    def admission_signature(
        policy_id: str,
        group: tuple[str, ...],
        mode: str,
        states: tuple[str, ...],
        baseline: tuple[str, ...] = (),
    ) -> tuple[Any, ...]:
        return (policy_id, group, mode, states, "deny", "deny", "deny", baseline)

    expected_admissions: dict[str, tuple[Any, ...]] = {}
    for profile_id in authored_draft:
        expected_admissions[profile_id] = admission_signature(
            "authored-draft-only", authored_draft, "states", ("draft",)
        )
    for profile_id in ("sdlc/plan", "sdlc/task"):
        expected_admissions[profile_id] = admission_signature(
            "execution-reciprocal-pair",
            ("sdlc/plan", "sdlc/task"),
            "paired",
            ("draft", "active"),
        )
    expected_admissions["content/archive"] = admission_signature(
        "archive-envelope-only",
        ("content/archive",),
        "archive-envelope",
        ("archived",),
    )
    for profile_id in snapshot_profiles:
        expected_admissions[profile_id] = admission_signature(
            "snapshot-only", snapshot_profiles, "snapshot-only", ()
        )
    actual_admissions = {
        profile_id: (
            profile.admission.policy_id,
            profile.admission.profile_ids,
            profile.admission.create.mode,
            profile.admission.create.states,
            profile.admission.delete,
            profile.admission.rename,
            profile.admission.profile_change,
            tuple(path.as_posix() for path in profile.admission.baseline_paths),
        )
        for profile_id, profile in profiles.items()
    }
    if actual_admissions != expected_admissions or len(expected_admissions) != 64:
        raise AssertionError("production complete admission projection differs")

    lifecycle_groups = (
        (
            "product",
            ("sdlc/prd",),
            ("done",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "done", "complete-product-program"),
            ),
        ),
        (
            "architecture-requirement",
            ("sdlc/ard",),
            ("accepted",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "accepted", "accept-architecture"),
            ),
        ),
        (
            "architecture-decision",
            ("sdlc/adr",),
            ("accepted",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "accepted", "accept-decision-self"),
            ),
        ),
        (
            "specification",
            specifications,
            ("done",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "done", "complete-specification"),
            ),
        ),
        (
            "execution",
            ("sdlc/plan", "sdlc/task"),
            ("done",),
            (
                ("draft", "active", "activate-execution-pair"),
                ("active", "done", "complete-execution-pair"),
            ),
        ),
        (
            "operations",
            operations,
            ("accepted",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "accepted", "accept-operated-document"),
            ),
        ),
        (
            "reference-governance",
            references,
            ("accepted", "done"),
            (
                ("draft", "active", "activate-heading-profile"),
                ("active", "accepted", "terminate-reviewed-reference"),
                ("active", "done", "terminate-reviewed-reference"),
            ),
        ),
        ("archive-record", ("content/archive",), ("archived",), ()),
        ("non-lifecycle", snapshot_profiles, (), ()),
    )
    expected_lifecycles: dict[str, tuple[Any, ...]] = {}
    for contract_id, group, terminals, lifecycle_edges in lifecycle_groups:
        signature = (contract_id, group, terminals, lifecycle_edges)
        for profile_id in group:
            expected_lifecycles[profile_id] = signature
    actual_lifecycles = {
        profile_id: (
            profile.lifecycle.contract_id,
            profile.lifecycle.profile_ids,
            profile.lifecycle.terminal_states,
            tuple(
                (edge.from_state, edge.to_state, edge.predicate_id)
                for edge in profile.lifecycle.edges
            ),
        )
        for profile_id, profile in profiles.items()
    }
    if actual_lifecycles != expected_lifecycles or len(expected_lifecycles) != 64:
        raise AssertionError("production complete lifecycle projection differs")

    def edge_rows(
        profile_ids: tuple[str, ...], from_state: str, to_state: str
    ) -> tuple[tuple[str, str, str], ...]:
        return tuple((profile_id, from_state, to_state) for profile_id in profile_ids)

    expected_predicates = {
        "archive-source-removal": (
            (),
            (),
            "archive-source",
            (1, 1),
            "source-removed-and-mirror-created",
            "none",
            ("archive-envelope", "same-diff", "source-removal"),
        ),
        "activate-self-body": (
            edge_rows(
                ("sdlc/prd", "sdlc/ard", "sdlc/adr", *specifications, *operations),
                "draft",
                "active",
            ),
            (("$self",), ("active",), 1, 1),
            "self",
            (1, 1),
            "self-status-and-body",
            "body-contract",
            ("same-diff",),
        ),
        "activate-heading-profile": (
            edge_rows(references, "draft", "active"),
            (("$self",), ("active",), 1, 1),
            "role-decision",
            (1, 1),
            "self-status-and-body",
            "heading-set",
            ("rendered-link", "same-diff"),
        ),
        "activate-execution-pair": (
            edge_rows(("sdlc/plan", "sdlc/task"), "draft", "active"),
            (("sdlc/plan",), ("active",), 1, 1, ("sdlc/task",), ("active",), 1, 1),
            "pair",
            (2, 2),
            "pair-created-or-status-changed",
            "body-contract",
            ("rendered-link", "reciprocal-link", "same-diff"),
        ),
        "complete-product-program": (
            edge_rows(("sdlc/prd",), "active", "done"),
            (("sdlc/spec",), ("done",), 1, None),
            "program-lineage",
            (1, None),
            "target-and-last-relation-changed",
            "body-contract",
            ("program-lineage-closed", "same-diff"),
        ),
        "accept-architecture": (
            edge_rows(("sdlc/ard",), "active", "accepted"),
            (("sdlc/adr",), ("accepted",), 1, None),
            "role-decision",
            (1, None),
            "target-and-evidence-status-body-changed",
            "body-contract",
            ("rendered-link", "reciprocal-link", "same-diff"),
        ),
        "accept-decision-self": (
            edge_rows(("sdlc/adr",), "active", "accepted"),
            (("$self",), ("accepted",), 1, 1),
            "self",
            (1, 1),
            "self-status-and-body",
            "body-contract",
            ("rendered-link", "same-diff"),
        ),
        "complete-specification": (
            edge_rows(specifications, "active", "done"),
            (("sdlc/plan",), ("done",), 1, 1, ("sdlc/task",), ("done",), 1, 1),
            "pair",
            (2, 2),
            "target-plan-task-status-changed",
            "body-contract",
            ("rendered-link", "reciprocal-link", "same-diff"),
        ),
        "complete-execution-pair": (
            edge_rows(("sdlc/plan", "sdlc/task"), "active", "done"),
            (("sdlc/plan",), ("done",), 1, 1, ("sdlc/task",), ("done",), 1, 1),
            "pair",
            (2, 2),
            "pair-status-changed",
            "body-contract",
            ("rendered-link", "reciprocal-link", "task-terminal-evidence", "same-diff"),
        ),
        "accept-operated-document": (
            edge_rows(operations, "active", "accepted"),
            (("sdlc/plan",), ("done",), 1, 1, ("sdlc/task",), ("done",), 1, 1),
            "pair",
            (2, 2),
            "target-plan-task-status-changed",
            "body-contract",
            ("rendered-link", "same-diff"),
        ),
        "terminate-reviewed-reference": (
            tuple(
                (profile_id, "active", state)
                for profile_id in references
                for state in ("accepted", "done")
            ),
            (("sdlc/plan",), ("done",), 1, 1, ("sdlc/task",), ("done",), 1, 1),
            "role-decision",
            (2, 2),
            "target-plan-task-status-changed",
            "heading-set",
            ("rendered-link", "same-diff"),
        ),
    }
    actual_predicates = {
        predicate.predicate_id: (
            tuple(
                (edge.profile_id, edge.from_state, edge.to_state)
                for edge in predicate.profile_edges
            ),
            tuple(
                component
                for item in predicate.evidence
                for component in (
                    item.profile_ids,
                    item.states,
                    item.minimum,
                    item.maximum,
                )
            ),
            predicate.relationship,
            (predicate.minimum, predicate.maximum),
            predicate.same_diff,
            predicate.body_requirement,
            predicate.capabilities,
        )
        for predicate in registry.evidence_predicates
    }
    if actual_predicates != expected_predicates:
        raise AssertionError(
            "production complete evidence predicate projection differs"
        )

    expected_null_body_roles = {
        "content/reference": ("Related Documents", "heading-set"),
        "content/archive": (None, "none"),
        "governance/reference": ("Related Documents", "heading-set"),
        "governance/memory": ("Related Progress", "heading-set"),
        "governance/template-support": ("Related Documents", "heading-set"),
    }
    actual_null_body_roles = {
        profile_id: (
            profiles[profile_id].role_decision.relationship_section,
            profiles[profile_id].role_decision.body_requirement,
        )
        for profile_id in expected_null_body_roles
    }
    if actual_null_body_roles != expected_null_body_roles:
        raise AssertionError("production null-body role decision projection differs")
    if (
        profiles["template/sdlc/prd"].role_decision.source_profile_id != "sdlc/prd"
        or profiles["template/sdlc/prd"].value_contract.contract_id
        != "authored-standard"
        or profiles["template/sdlc/prd"].admission.create.mode != "snapshot-only"
    ):
        raise AssertionError("canonical form inheritance projection differs")
    archive = profiles["content/archive"].admission
    if (
        archive.create.mode != "archive-envelope"
        or archive.create.states != ("archived",)
        or archive.baseline_paths
        or {archive.delete, archive.rename, archive.profile_change} != {"deny"}
    ):
        raise AssertionError("production archive envelope admission projection differs")
    if sum(len(profile.lifecycle.edges) for profile in registry.profiles) != 42:
        raise AssertionError("production lifecycle edge count differs")


def _assert_parser_safety() -> None:
    oid = b"0" * 40
    negative_cases = (
        (
            _parse_ls_tree_z,
            b"100600 blob " + oid + b"\tdocs/a.md\0",
            "noncanonical git ls-tree mode",
        ),
        (
            _parse_ls_tree_z,
            b"100644 tree " + oid + b"\tdocs/a.md\0",
            "impossible git ls-tree mode/type pair",
        ),
        (
            _parse_ls_tree_z,
            b"100644 blob " + (b"g" * 40) + b"\tdocs/a.md\0",
            "lowercase hexadecimal",
        ),
        (
            _parse_ls_tree_z,
            b"100644 blob " + (b"0" * 41) + b"\tdocs/a.md\0",
            "exactly 40 or 64",
        ),
        (
            _parse_ls_files_stage_z,
            b"040000 " + oid + b" 0\tdocs\0",
            "noncanonical git ls-files mode",
        ),
        (
            _parse_ls_files_stage_z,
            b"100644 " + (b"G" * 40) + b" 0\tdocs/a.md\0",
            "lowercase hexadecimal",
        ),
        (
            _parse_ls_files_stage_z,
            b"100644 " + (b"0" * 63) + b" 0\tdocs/a.md\0",
            "exactly 40 or 64",
        ),
    )
    for parser, raw, expected_fragment in negative_cases:
        try:
            parser(raw)
        except ValueError as exc:
            if expected_fragment not in str(exc):
                raise AssertionError(
                    f"expected {expected_fragment!r}, got {str(exc)!r}"
                ) from exc
        else:
            raise AssertionError(
                f"parser accepted invalid record requiring {expected_fragment!r}"
            )


def _current_form_paths(root: Path) -> tuple[PurePosixPath, ...]:
    """Inventory the complete proposed worktree form snapshot."""

    forms_root = root / "docs/99.templates/templates"
    return tuple(
        sorted(
            (
                PurePosixPath(path.relative_to(root).as_posix())
                for path in forms_root.rglob("*")
                if path.is_file() and ".template." in path.name
            ),
            key=lambda path: path.as_posix(),
        )
    )


def _assert_native_form_profiles(
    registry: Any, native_form_paths: tuple[PurePosixPath, ...]
) -> None:
    native_forms = set(native_form_paths)
    profiles_by_form: dict[PurePosixPath, list[Any]] = {
        path: [] for path in native_form_paths
    }
    for profile in registry.profiles:
        if profile.template in native_forms:
            profiles_by_form[profile.template].append(profile)

    for template_path, form_profiles in profiles_by_form.items():
        if len(form_profiles) != 1:
            raise AssertionError(
                f"{template_path}: native form must have one distinct registry profile"
            )
        profile = form_profiles[0]
        template_basename = template_path.name
        if template_basename.count(".template") != 1:
            raise AssertionError(
                f"{template_path}: native form basename must contain one .template infix"
            )
        target_basename = template_basename.replace(".template", "", 1)
        expected_route_suffix = re.escape(target_basename) + "$"
        if (
            profile.mode != "classification-only"
            or len(profile.routes) != 1
            or profile.routes[0].kind != "regex"
            or not profile.routes[0].value.startswith("^")
            or not profile.routes[0].value.endswith(expected_route_suffix)
        ):
            raise AssertionError(
                f"{template_path}: native profile must have one anchored regex route "
                f"ending in the template-derived target basename {target_basename!r}"
            )


def _assert_retired_cloud_sdlc_routes_uncovered(registry: Any) -> None:
    probes = (
        PurePosixPath("examples/aws/docs/01.requirements/new-cloud-prd.md"),
        PurePosixPath("examples/azure/docs/03.specs/new-cloud-spec/spec.md"),
        PurePosixPath("examples/aws/docs/05.operations/runbooks/new-cloud-runbook.md"),
        PurePosixPath("examples/azure/docs/README.md"),
    )
    for path in probes:
        try:
            classify_path(registry, path)
        except DocumentContractError as exc:
            if "REGISTRY_ROUTE_UNCOVERED" not in _ordered_rule_ids(exc.diagnostics):
                raise AssertionError(
                    f"{path}: retired cloud route probe returned wrong rule"
                ) from exc
        else:
            raise AssertionError(f"{path}: retired cloud path must remain uncovered")


def _assert_tracked_local_agent_fixture_sample(root: Path, registry: Any) -> None:
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", SAMPLE_PATH.as_posix()],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.stdout.strip() != SAMPLE_PATH.as_posix():
        raise AssertionError(
            "local agent fixture sample must be one exact tracked path"
        )
    actual_profile = classify_path(registry, SAMPLE_PATH).profile_id
    if actual_profile != "exception/local-agent-asset":
        raise AssertionError(
            f"{SAMPLE_PATH}: expected local agent asset, got {actual_profile!r}"
        )


def _assert_reserved_gemini_native_surfaces_absent(root: Path) -> None:
    """Reject reserved Gemini CLI native paths using index metadata only."""
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--",
            ".gemini/agents",
            ".gemini/settings.json",
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stdout and not completed.stdout.endswith(b"\0"):
        raise AssertionError(
            f"{RESERVED_GEMINI_NATIVE_SURFACE_RULE}: Git index inventory must be NUL terminated"
        )
    if completed.stdout:
        raise AssertionError(RESERVED_GEMINI_NATIVE_SURFACE_ERROR)


def _assert_reserved_gemini_native_surface_mutation_proofs() -> None:
    for reserved_path in (
        PurePosixPath(".gemini/agents/fixture-agent.md"),
        PurePosixPath(".gemini/settings.json"),
    ):
        with tempfile.TemporaryDirectory(
            prefix="document-registry-gemini-reserved-"
        ) as directory:
            fixture_root = Path(directory)
            subprocess.run(["git", "init", "--quiet"], cwd=fixture_root, check=True)
            target = fixture_root / reserved_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("{}\n", encoding="utf-8")

            # The guard is index-scoped: an untracked local file is not a
            # repository declaration and therefore remains outside this rule.
            _assert_reserved_gemini_native_surfaces_absent(fixture_root)
            subprocess.run(
                ["git", "add", "--", reserved_path.as_posix()],
                cwd=fixture_root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                _assert_reserved_gemini_native_surfaces_absent(fixture_root)
            except AssertionError as exc:
                if str(exc) != RESERVED_GEMINI_NATIVE_SURFACE_ERROR:
                    raise AssertionError(
                        "reserved Gemini native surface guard returned an unstable error"
                    ) from exc
            else:
                raise AssertionError(
                    "reserved Gemini native surface guard accepted a tracked mutation"
                )


def _assert_retired_cloud_sdlc_surfaces_absent(root: Path) -> None:
    """Reject retired cloud documentation trees using Git-index metadata only."""
    completed = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--",
            "examples/aws/docs",
            "examples/azure/docs",
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.stdout and not completed.stdout.endswith(b"\0"):
        raise AssertionError(
            f"{RETIRED_CLOUD_SDLC_SURFACE_RULE}: Git index inventory must be NUL terminated"
        )
    if completed.stdout:
        raise AssertionError(RETIRED_CLOUD_SDLC_SURFACE_ERROR)


def _assert_retired_cloud_sdlc_surface_mutation_proofs() -> None:
    for retired_path in (
        PurePosixPath("examples/aws/docs/01.requirements/new-cloud-prd.md"),
        PurePosixPath("examples/azure/docs/03.specs/new-cloud-spec/spec.md"),
        PurePosixPath("examples/aws/docs/05.operations/runbooks/new-cloud-runbook.md"),
        PurePosixPath("examples/azure/docs/README.md"),
    ):
        with tempfile.TemporaryDirectory(
            prefix="document-registry-retired-cloud-"
        ) as directory:
            fixture_root = Path(directory)
            subprocess.run(["git", "init", "--quiet"], cwd=fixture_root, check=True)
            target = fixture_root / retired_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Retired cloud path probe\n", encoding="utf-8")

            _assert_retired_cloud_sdlc_surfaces_absent(fixture_root)
            subprocess.run(
                ["git", "add", "--", retired_path.as_posix()],
                cwd=fixture_root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                _assert_retired_cloud_sdlc_surfaces_absent(fixture_root)
            except AssertionError as exc:
                if str(exc) != RETIRED_CLOUD_SDLC_SURFACE_ERROR:
                    raise AssertionError(
                        "retired cloud surface guard returned an unstable error"
                    ) from exc
            else:
                raise AssertionError(
                    "retired cloud surface guard accepted a tracked mutation"
                )


def _assert_adapter_surface_routes(
    root: Path, raw_registry: dict[str, Any], registry: Any
) -> None:
    probes = {
        PurePosixPath(".agents/GEMINI.md"): "exception/local-agent-asset",
        PurePosixPath(".agents/agents/code-reviewer.md"): "exception/local-agent-asset",
        PurePosixPath(".claude/CLAUDE.md"): "exception/repository-runtime-baseline",
        PurePosixPath(".codex/CODEX.md"): "exception/repository-runtime-baseline",
        PurePosixPath(".claude/agents/code-reviewer.md"): (
            "exception/provider-native-metadata"
        ),
    }
    for path, expected_profile in probes.items():
        actual_profile = classify_path(registry, path).profile_id
        if actual_profile != expected_profile:
            raise AssertionError(
                f"{path}: expected {expected_profile!r}, got {actual_profile!r}"
            )

    try:
        classify_path(registry, PurePosixPath(".gemini/agents/code-reviewer.md"))
    except DocumentContractError as exc:
        if _ordered_rule_ids(exc.diagnostics) != ("REGISTRY_ROUTE_UNCOVERED",):
            raise AssertionError(
                ".gemini/** uncovered probe returned wrong rule"
            ) from exc
    else:
        raise AssertionError(
            ".gemini/** must remain outside the tracked adapter contract"
        )

    broad_registry = copy.deepcopy(raw_registry)
    provider_profile = next(
        profile
        for profile in broad_registry["profiles"]
        if profile["id"] == "exception/provider-native-metadata"
    )
    provider_profile["routes"][0]["value"] = r"^\.(?:agents|claude)/.+\.md$"
    try:
        broad_candidate = validate_registry(root, broad_registry)
        classify_path(broad_candidate, PurePosixPath(".agents/GEMINI.md"))
    except DocumentContractError as exc:
        if "REGISTRY_ROUTE_AMBIGUOUS" not in _ordered_rule_ids(exc.diagnostics):
            raise AssertionError(
                "broad provider route probe returned wrong rule"
            ) from exc
    else:
        raise AssertionError("broad provider route must be rejected as ambiguous")

    missing_route_registry = copy.deepcopy(raw_registry)
    missing_route_registry["profiles"] = [
        profile
        for profile in missing_route_registry["profiles"]
        if profile["id"] != "exception/local-agent-asset"
    ]
    for family in (
        "valueContracts",
        "roleDecisions",
        "admissionPolicies",
        "lifecycleContracts",
    ):
        for group in missing_route_registry["documentContracts"][family]:
            if "exception/local-agent-asset" in group["profileIds"]:
                group["profileIds"].remove("exception/local-agent-asset")
    try:
        missing_route_candidate = validate_registry(root, missing_route_registry)
        classify_path(missing_route_candidate, PurePosixPath(".agents/GEMINI.md"))
    except DocumentContractError as exc:
        if "REGISTRY_ROUTE_UNCOVERED" not in _ordered_rule_ids(exc.diagnostics):
            raise AssertionError(
                "local route removal probe returned wrong rule"
            ) from exc
    else:
        raise AssertionError(
            "removing the local agent route must leave tracked paths uncovered"
        )


def _assert_template_source_parity(registry: Any) -> None:
    """Require every ordinary Markdown form to equal its canonical source."""

    profiles = {profile.profile_id: profile for profile in registry.profiles}
    for profile in registry.profiles:
        if profile.mode != "template" or profile.append_contract is not None:
            continue
        if len(profile.source_profile_ids) != 1:
            raise AssertionError(
                f"{profile.profile_id}: template/source cardinality differs"
            )
        source_id = profile.source_profile_ids[0]
        source = profiles.get(source_id)
        if source is None:
            raise AssertionError(
                f"{profile.profile_id}: template/source profile is unknown"
            )
        comparisons = (
            (
                "frontmatter",
                (
                    profile.frontmatter.mode,
                    profile.frontmatter.required,
                    profile.frontmatter.allowed,
                ),
                (
                    source.frontmatter.mode,
                    source.frontmatter.required,
                    source.frontmatter.allowed,
                ),
            ),
            (
                "frontmatter-order",
                profile.frontmatter.order,
                source.frontmatter.order,
            ),
            ("status", profile.status_domain, source.status_domain),
            ("headings", profile.headings, source.headings),
            ("class", profile.profile_class, source.profile_class),
            ("body", profile.body_contract, source.body_contract),
            ("value-contract", profile.value_contract, source.value_contract),
        )
        role_actual = (
            profile.role_decision.role,
            profile.role_decision.source_profile_id,
            profile.role_decision.relationship_section,
            profile.role_decision.body_requirement,
        )
        role_expected = (
            source.role_decision.role,
            source_id,
            source.role_decision.relationship_section,
            source.role_decision.body_requirement,
        )
        if role_actual != role_expected:
            raise AssertionError(
                f"{profile.profile_id}: template/source role-decision parity differs"
            )
        for label, actual, expected in comparisons:
            if actual != expected:
                raise AssertionError(
                    f"{profile.profile_id}: template/source {label} parity differs"
                )


def _assert_template_source_mutation_proofs(
    root: Path, raw_registry: dict[str, Any]
) -> int:
    """Exercise each independent form/source parity failure surface."""

    fixture = _load_json(root / TEMPLATE_SOURCE_PARITY_PATH)
    cases = fixture.get("cases")
    if (
        fixture.get("schemaVersion") != 1
        or not isinstance(cases, list)
        or len(cases) != 11
    ):
        raise AssertionError("template/source parity fixture schema differs")
    expected_keys = {"name", "mutation", "expectedSignal"}
    names = [case.get("name") for case in cases]
    if len(names) != len(set(names)):
        raise AssertionError("template/source parity case names are not unique")

    for case in cases:
        if not isinstance(case, dict) or set(case) != expected_keys:
            raise AssertionError(f"invalid template/source parity case: {case!r}")
        mutated = copy.deepcopy(raw_registry)
        profile = next(
            item for item in mutated["profiles"] if item["id"] == "template/sdlc/prd"
        )
        mutation = case["mutation"]
        if mutation == "frontmatter":
            profile["frontmatter"]["allowed"].append("legacy")
        elif mutation == "order":
            profile["frontmatter"]["order"][0:2] = ["type", "title"]
        elif mutation == "status":
            profile["statusDomain"].append("legacy")
        elif mutation == "headings":
            profile["headings"]["allowed"].append("Legacy")
        elif mutation == "class":
            profile["class"] = "common"
        elif mutation == "body":
            profile["bodyContract"]["allowExplicitExclusion"] = False
        elif mutation == "value-contract":
            standard = next(
                item
                for item in mutated["documentContracts"]["valueContracts"]
                if "sdlc/prd" in item["profileIds"]
            )
            drift = copy.deepcopy(standard)
            drift["id"] = "template-prd-value-drift"
            drift["profileIds"] = ["template/sdlc/prd"]
            owner = next(item for item in drift["keys"] if item["key"] == "owner")
            owner["pattern"] = "^platform$"
            mutated["documentContracts"]["valueContracts"].append(drift)
        elif mutation == "source-cardinality":
            profile["sourceProfileIds"] = ["sdlc/prd", "sdlc/spec"]
        elif mutation == "missing-source":
            profile["sourceProfileIds"] = []
        elif mutation == "duplicate-source":
            profile["sourceProfileIds"] = ["sdlc/prd", "sdlc/prd"]
        elif mutation == "unknown-source":
            profile["sourceProfileIds"] = ["sdlc/unknown"]
        else:
            raise AssertionError(f"unknown template/source parity mutation: {mutation}")

        signal = ""
        try:
            candidate = validate_registry(root, mutated)
            _assert_template_source_parity(candidate)
        except DocumentContractError as exc:
            signal = ",".join(_ordered_rule_ids(exc.diagnostics))
        except AssertionError as exc:
            signal = str(exc)
        if case["expectedSignal"] not in signal:
            raise AssertionError(
                f"template/source parity {case['name']}: "
                f"expected {case['expectedSignal']!r}, got {signal!r}"
            )
    return len(cases)


def _assert_role_inheritance_mutation_proof(
    root: Path, raw_registry: dict[str, Any]
) -> None:
    """Reject a template that bypasses its canonical source role decision."""

    mutated = copy.deepcopy(raw_registry)
    runbook_role = next(
        item
        for item in mutated["documentContracts"]["roleDecisions"]
        if "sdlc/runbook" in item["profileIds"]
    )
    runbook_role["profileIds"].append("template/sdlc/guide")
    try:
        validate_registry(root, mutated)
    except DocumentContractError as exc:
        actual = _ordered_rule_ids(exc.diagnostics)
    else:
        actual = ()
    if actual != ("REGISTRY_ROLE_DECISION",):
        raise AssertionError(
            "direct template role assignment must return REGISTRY_ROLE_DECISION"
        )


def _assert_positive_coverage(
    root: Path, raw_registry: dict[str, Any], fixture: dict[str, Any]
) -> tuple[int, int]:
    registry = validate_registry(root, raw_registry)
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    _assert_template_source_parity(registry)
    _assert_retired_cloud_sdlc_routes_uncovered(registry)
    _assert_tracked_local_agent_fixture_sample(root, registry)
    _assert_adapter_surface_routes(root, raw_registry, registry)

    routing_cases = fixture.get("routingCases")
    if not isinstance(routing_cases, list) or len(routing_cases) != 6:
        raise AssertionError("routingCases must contain the six independent probes")
    routing_keys = {"path", "expectedProfile", "expectedRuleIds"}
    for row in routing_cases:
        if not isinstance(row, dict) or set(row) != routing_keys:
            raise AssertionError(f"invalid routingCases row: {row!r}")
        path = PurePosixPath(row["path"])
        expected_profile = row["expectedProfile"]
        expected_rules = tuple(row["expectedRuleIds"])
        actual_profile: str | None = None
        actual_rules: tuple[str, ...] = ()
        try:
            actual_profile = classify_path(registry, path).profile_id
        except DocumentContractError as exc:
            actual_rules = _ordered_rule_ids(exc.diagnostics)
        if actual_profile != expected_profile or actual_rules != expected_rules:
            raise AssertionError(
                f"{path}: expected profile={expected_profile!r} rules={expected_rules!r}; "
                f"actual profile={actual_profile!r} rules={actual_rules!r}"
            )

    current_form_paths = _current_form_paths(root)
    declared_form_paths = tuple(
        sorted(
            {profile.template for profile in registry.profiles if profile.template},
            key=lambda path: path.as_posix(),
        )
    )
    if declared_form_paths != current_form_paths:
        raise AssertionError(
            "registry template paths must equal the current canonical form inventory: "
            f"missing={sorted(set(current_form_paths) - set(declared_form_paths), key=str)!r} "
            f"extra={sorted(set(declared_form_paths) - set(current_form_paths), key=str)!r}"
        )

    markdown_form_paths = tuple(
        path for path in current_form_paths if path.suffix == ".md"
    )
    native_form_paths = tuple(
        path for path in current_form_paths if path.suffix != ".md"
    )
    if len(markdown_form_paths) != 27 or len(native_form_paths) != 3:
        raise AssertionError(
            "canonical form inventory must contain 27 Markdown and three native forms"
        )

    covered_template_profiles: set[str] = set()
    ordinary_source_less_profiles: list[str] = []
    append_profiles: set[str] = set()
    for path in markdown_form_paths:
        profile = classify_path(registry, path)
        if profile.mode != "template":
            raise AssertionError(f"{profile.profile_id}: expected template mode")
        if profile.placeholder_policy != "template-only":
            raise AssertionError(
                f"{profile.profile_id}: expected template-only placeholder policy"
            )
        if len(profile.routes) != 1 or (
            profile.routes[0].kind != "exact"
            or profile.routes[0].value != path.as_posix()
        ):
            raise AssertionError(
                f"{profile.profile_id}: expected one exact route to {path.as_posix()}"
            )
        if profile.template != path:
            raise AssertionError(
                f"{profile.profile_id}: template must equal its exact route"
            )
        covered_template_profiles.add(profile.profile_id)
        if profile.append_contract is not None:
            append_profiles.add(profile.profile_id)
            if profile.profile_id != "governance/progress-entry":
                raise AssertionError(
                    f"{profile.profile_id}: unexpected append contract"
                )
            append_contract = profile.append_contract
            if (
                profile.source_profile_ids != ("governance/progress-ledger",)
                or append_contract.parent_profile_id != "governance/progress-ledger"
                or append_contract.parent_h2 != "Work Entries"
                or append_contract.entry_heading_level != 3
                or append_contract.section_heading_level != 4
                or append_contract.required_sections
                != ("Metadata", "Progress", "Memory", "Evidence", "Handoff")
            ):
                raise AssertionError(
                    "governance/progress-entry append contract does not match "
                    "the ledger H3/H4 contract"
                )
            continue
        if not profile.source_profile_ids:
            ordinary_source_less_profiles.append(profile.profile_id)
            continue
        for source_id in profile.source_profile_ids:
            source = profiles.get(source_id)
            if source is None:
                raise AssertionError(
                    f"{profile.profile_id}: unknown source profile {source_id!r}"
                )
            inherited = (
                profile.profile_class,
                profile.frontmatter,
                profile.status_domain,
                profile.headings,
                profile.body_contract,
            )
            expected = (
                source.profile_class,
                source.frontmatter,
                source.status_domain,
                source.headings,
                source.body_contract,
            )
            if inherited != expected:
                raise AssertionError(
                    f"{profile.profile_id}: inherited contract differs from {source_id}"
                )

    if ordinary_source_less_profiles:
        raise AssertionError(
            "ordinary templates must declare a source profile: "
            f"{ordinary_source_less_profiles!r}"
        )

    declared_template_profiles = {
        profile.profile_id
        for profile in registry.profiles
        if profile.mode == "template"
    }
    if covered_template_profiles != declared_template_profiles:
        raise AssertionError(
            "registry-derived Markdown forms must equal declared template profiles"
        )
    if append_profiles != {"governance/progress-entry"}:
        raise AssertionError(
            "governance/progress-entry must be the sole append-contract template"
        )

    _assert_native_form_profiles(registry, native_form_paths)

    native_drift = copy.deepcopy(raw_registry)
    native_form_strings = {path.as_posix() for path in native_form_paths}
    native_profile = next(
        profile
        for profile in native_drift["profiles"]
        if profile["template"] in native_form_strings
    )
    native_profile["routes"][0]["value"] = (
        native_profile["routes"][0]["value"][:-1] + "-drift$"
    )
    try:
        _assert_native_form_profiles(
            validate_registry(root, native_drift), native_form_paths
        )
    except AssertionError as exc:
        if "template-derived target basename" not in str(exc):
            raise AssertionError(
                "native route/template drift returned an unstable diagnostic"
            ) from exc
    else:
        raise AssertionError("native route/template drift mutation was accepted")

    return len(profiles), len(current_form_paths)


def _strip_multiline_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove HTML comments while retaining visible text around them."""
    visible: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                return "".join(visible), True
            cursor = end + 3
            in_comment = False
            continue
        start = line.find("<!--", cursor)
        if start < 0:
            visible.append(line[cursor:])
            break
        visible.append(line[cursor:start])
        cursor = start + 4
        in_comment = True
    return "".join(visible), in_comment


def _extract_markdown_structure(
    markdown: str,
) -> tuple[list[tuple[int, str]], bool]:
    """Extract ATX headings and report an unclosed matching fence."""
    headings: list[tuple[int, str]] = []
    fence_character: str | None = None
    fence_length = 0
    in_comment = False
    opening_fence = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")

    for raw_line in markdown.splitlines():
        if fence_character is not None:
            closing_fence = re.compile(
                rf"^ {{0,3}}{re.escape(fence_character)}"
                rf"{{{fence_length},}}[ \t]*$"
            )
            if closing_fence.match(raw_line):
                fence_character = None
                fence_length = 0
            continue

        line, in_comment = _strip_multiline_html_comments(raw_line, in_comment)
        fence_match = opening_fence.match(line)
        if fence_match:
            marker = fence_match.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            continue

        heading_match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if not heading_match:
            continue
        heading_text = heading_match.group(2).strip()
        heading_text = re.sub(r"[ \t]+#+[ \t]*$", "", heading_text).strip()
        headings.append((len(heading_match.group(1)), heading_text))

    return headings, fence_character is not None


def extract_markdown_headings(markdown: str) -> list[tuple[int, str]]:
    """Shared fence/comment-aware heading extraction for README validation."""
    headings, _ = _extract_markdown_structure(markdown)
    return headings


def _evaluate_readme_document(
    document: str, required_h2: tuple[str, ...], allowed_h2: tuple[str, ...]
) -> tuple[str, ...]:
    """Evaluate the bounded README handoff fixture, not production semantics."""
    rule_ids: list[str] = []
    if re.match(r"^---\n.*?\n---(?:\n|$)", document, re.DOTALL):
        rule_ids.append("README_FRONTMATTER")

    headings, unclosed_fence = _extract_markdown_structure(document)
    h1 = [text for level, text in headings if level == 1]
    h2 = [text for level, text in headings if level == 2]
    if len(h1) != 1:
        rule_ids.append("README_H1")
    if len(h2) != len(set(h2)):
        rule_ids.append("README_H2_DUPLICATE")
    if any(heading not in allowed_h2 for heading in h2):
        rule_ids.append("README_H2_UNSUPPORTED")
    if any(heading not in h2 for heading in required_h2):
        rule_ids.append("README_H2_REQUIRED")
    if unclosed_fence:
        rule_ids.append("README_FENCE")
    return tuple(rule_ids)


def _is_readme_path(path: PurePosixPath) -> bool:
    return path.name == "README.md"


def _readme_inventory_exact_error(
    tracked_paths: set[PurePosixPath], declared_paths: set[PurePosixPath]
) -> str | None:
    missing = sorted(path.as_posix() for path in declared_paths - tracked_paths)
    extra = sorted(path.as_posix() for path in tracked_paths - declared_paths)
    if not missing and not extra:
        return None
    return (
        "README tracked set differs from fixture-declared final set: "
        f"missing={missing!r} extra={extra!r}"
    )


def _readme_profile_ids(registry: Any) -> set[str]:
    return {
        profile.profile_id
        for profile in registry.profiles
        if profile.profile_id.startswith("readme/")
        and profile.profile_class == "readme"
        and profile.mode == "frontmatter-free"
    }


def _assert_readme_family_contract(
    root: Path,
    registry: Any,
    *,
    fixture: dict[str, Any] | None = None,
    inventory: TargetInventory | None = None,
) -> tuple[int, int, int]:
    if fixture is None:
        fixture = _load_json(root / README_FIXTURE_PATH)
    if inventory is None:
        inventory = enumerate_target_markdown(root)
    if not isinstance(fixture, dict) or set(fixture) != {
        "schemaVersion",
        "activePaths",
        "retiredPaths",
        "cases",
    }:
        raise AssertionError("README profile fixture schema mismatch")
    active_rows = fixture.get("activePaths")
    retired_rows = fixture.get("retiredPaths")
    cases = fixture.get("cases")
    if (
        fixture.get("schemaVersion") != 3
        or not isinstance(active_rows, list)
        or not isinstance(retired_rows, list)
        or not isinstance(cases, list)
    ):
        raise AssertionError("README profile fixture schema mismatch")

    for rows in (active_rows, retired_rows):
        for row in rows:
            if not isinstance(row, dict):
                raise AssertionError("README fixture path rows must be objects")
            raw_path = row.get("path")
            if not isinstance(raw_path, str) or not raw_path:
                raise AssertionError(f"invalid README fixture path: {raw_path!r}")
    active_order = [row["path"] for row in active_rows]
    retired_order = [row["path"] for row in retired_rows]
    if active_order != sorted(active_order) or len(active_order) != len(
        set(active_order)
    ):
        raise AssertionError("README activePaths must be sorted and unique")
    if retired_order != sorted(retired_order) or len(retired_order) != len(
        set(retired_order)
    ):
        raise AssertionError("README retiredPaths must be sorted and unique")
    if len(active_rows) != 52 or len(retired_rows) != 20:
        raise AssertionError("README fixture must contain exact active52 and retired20")

    active_keys = {"path", "profile", "requiredH2", "allowedH2", "new"}
    retired_keys = active_keys | {"retiredBy", "destination"}
    active_paths = {PurePosixPath(path) for path in active_order}
    retired_paths = {PurePosixPath(path) for path in retired_order}
    if active_paths & retired_paths:
        raise AssertionError("README activePaths and retiredPaths must be disjoint")

    baseline_readmes = {
        path for path in inventory.baseline_paths if _is_readme_path(path)
    }
    tracked_readmes = {
        path for path in inventory.current_paths if _is_readme_path(path)
    }
    new_readmes = {path for path in inventory.new_paths if _is_readme_path(path)}
    readme_profile_ids = _readme_profile_ids(registry)
    readme_profiles = {
        profile.profile_id: profile
        for profile in registry.profiles
        if profile.profile_id in readme_profile_ids
    }
    rows_by_path: dict[PurePosixPath, dict[str, Any]] = {}
    for lifecycle, rows, expected_keys in (
        ("active", active_rows, active_keys),
        ("retired", retired_rows, retired_keys),
    ):
        for row in rows:
            if set(row) != expected_keys:
                raise AssertionError(f"invalid README {lifecycle} path row: {row!r}")
            raw_path = row.get("path")
            if not isinstance(raw_path, str) or not raw_path:
                raise AssertionError(f"invalid README fixture path: {raw_path!r}")
            path = PurePosixPath(raw_path)
            if (
                path.as_posix() != raw_path
                or path.is_absolute()
                or ".." in path.parts
                or not _is_readme_path(path)
            ):
                raise AssertionError(f"invalid README fixture path: {raw_path!r}")
            if path in rows_by_path:
                raise AssertionError(f"duplicate README fixture path: {path}")
            rows_by_path[path] = row
            if lifecycle == "active":
                profile = classify_path(registry, path)
                if profile.profile_id != row["profile"]:
                    raise AssertionError(
                        f"{path}: README fixture profile {row['profile']!r} differs "
                        f"from registry {profile.profile_id!r}"
                    )
                if profile.profile_id not in readme_profile_ids:
                    raise AssertionError(
                        f"{path}: README fixture selected a non-authored profile"
                    )
            else:
                if row["profile"] != "readme/snapshot-pack":
                    raise AssertionError(
                        f"{path}: retired README historical profile must be readme/snapshot-pack"
                    )
                profile = readme_profiles[row["profile"]]
                try:
                    classify_path(registry, path)
                except DocumentContractError as exc:
                    if "REGISTRY_ROUTE_UNCOVERED" not in _ordered_rule_ids(
                        exc.diagnostics
                    ):
                        raise AssertionError(
                            f"{path}: retired README returned wrong route rule"
                        ) from exc
                else:
                    raise AssertionError(
                        f"{path}: retired README must remain uncovered"
                    )
            if list(profile.headings.required) != row["requiredH2"]:
                raise AssertionError(
                    f"{path}: README required headings differ from registry"
                )
            if list(profile.headings.allowed) != row["allowedH2"]:
                raise AssertionError(
                    f"{path}: README allowed headings differ from registry"
                )
            if not isinstance(row["new"], bool):
                raise AssertionError(f"{path}: README new flag must be boolean")
            expected_new = path not in baseline_readmes
            if row["new"] is not expected_new:
                raise AssertionError(
                    f"{path}: README new flag differs from immutable baseline inventory"
                )
            if lifecycle == "active":
                if path not in tracked_readmes or not (root / path).is_file():
                    raise AssertionError(f"README active path is absent: {path}")
                continue
            if row["retiredBy"] != "ADM-006":
                raise AssertionError(f"{path}: README retirement owner must be ADM-006")
            destination = row["destination"]
            if not isinstance(destination, str) or not destination:
                raise AssertionError(
                    f"{path}: README retirement destination is invalid"
                )
            destination_path = PurePosixPath(destination)
            if (
                destination_path.as_posix() != destination
                or destination_path.is_absolute()
                or ".." in destination_path.parts
                or not (root / destination_path).is_file()
            ):
                raise AssertionError(
                    f"{path}: README retirement destination is missing or invalid"
                )
            if raw_path.startswith("examples/aws/docs/"):
                provider = "aws"
            elif raw_path.startswith("examples/azure/docs/"):
                provider = "azure"
            else:
                raise AssertionError(
                    f"{path}: README retirement path is outside ADM-006"
                )
            expected_destination = PurePosixPath(
                "docs/90.references/cloud-examples/"
                f"{provider}/2026-07-12-{provider}-example-snapshot.md"
            )
            if destination_path != expected_destination:
                raise AssertionError(
                    f"{path}: README retirement destination has wrong provider"
                )
            if path in tracked_readmes or (root / path).exists():
                raise AssertionError(f"README retired path is still current: {path}")

    active_baseline = active_paths & baseline_readmes
    active_program_created = active_paths - baseline_readmes
    if len(baseline_readmes) != 67:
        raise AssertionError("README immutable baseline must contain exact 67 paths")
    if len(active_baseline) != 47 or len(active_program_created) != 5:
        raise AssertionError(
            "README activePaths must contain 47 baseline and five program-created paths"
        )
    if retired_paths - baseline_readmes:
        raise AssertionError(
            "README retiredPaths must belong to the immutable baseline"
        )
    if active_baseline | retired_paths != baseline_readmes:
        raise AssertionError(
            "README active baseline plus retired paths must reconstruct baseline67"
        )
    if active_program_created != new_readmes:
        raise AssertionError(
            "README program-created active paths must equal the current new inventory"
        )
    inventory_error = _readme_inventory_exact_error(tracked_readmes, active_paths)
    if inventory_error is not None:
        raise AssertionError(inventory_error)
    selected_tracked = {
        path
        for path in inventory.current_paths
        if classify_path(registry, path).profile_id in readme_profile_ids
    }
    if selected_tracked != active_paths:
        raise AssertionError(
            "README family selected path set differs from fixture activePaths: "
            f"extra={sorted(path.as_posix() for path in selected_tracked - active_paths)!r} "
            f"missing={sorted(path.as_posix() for path in active_paths - selected_tracked)!r}"
        )

    expected_cases = (
        ("valid-profile", ()),
        ("frontmatter-forbidden", ("README_FRONTMATTER",)),
        ("duplicate-h1", ("README_H1",)),
        ("duplicate-h2", ("README_H2_DUPLICATE",)),
        ("unsupported-h2", ("README_H2_UNSUPPORTED",)),
        ("missing-required-h2", ("README_H2_REQUIRED",)),
        ("fenced-heading-ignored", ()),
        ("unclosed-fence", ("README_FENCE",)),
    )
    expected_by_name = dict(expected_cases)
    case_keys = {"name", "path", "document", "expected_rule_ids"}
    actual_case_names: list[str] = []
    for case in cases:
        if not isinstance(case, dict) or set(case) != case_keys:
            raise AssertionError(f"invalid README fixture case: {case!r}")
        name = case.get("name")
        actual_case_names.append(name)
        document = case.get("document")
        if not isinstance(document, str) or not document:
            raise AssertionError(f"README fixture case has invalid document: {case!r}")
        if "\\n" in document:
            raise AssertionError(
                f"README fixture case contains literal backslash-n: {name!r}"
            )
        raw_case_path = case.get("path")
        if not isinstance(raw_case_path, str) or not raw_case_path:
            raise AssertionError(f"README fixture case has invalid path: {case!r}")
        path = PurePosixPath(raw_case_path)
        row = rows_by_path.get(path)
        if row is None or path not in active_paths:
            raise AssertionError(
                f"README fixture case must reference activePaths: {case['path']}"
            )
        expected_rule_ids = expected_by_name.get(name)
        if (
            not isinstance(case.get("expected_rule_ids"), list)
            or tuple(case["expected_rule_ids"]) != expected_rule_ids
        ):
            raise AssertionError(f"README fixture case rule IDs differ for {name!r}")
        actual_rule_ids = _evaluate_readme_document(
            document,
            tuple(row["requiredH2"]),
            tuple(row["allowedH2"]),
        )
        if actual_rule_ids != expected_rule_ids:
            raise AssertionError(
                f"README fixture case {name!r} expected {expected_rule_ids!r}, "
                f"got {actual_rule_ids!r}"
            )
    if tuple(actual_case_names) != tuple(name for name, _ in expected_cases):
        raise AssertionError(
            "README fixture case names differ from the eight-case contract"
        )
    return len(baseline_readmes), len(active_paths | retired_paths), len(active_paths)


def _assert_readme_fixture_mutation_proofs(
    root: Path,
    raw_registry: dict[str, Any],
    registry: Any,
    fixture: dict[str, Any],
    inventory: TargetInventory,
) -> None:
    def expect_rejection(
        label: str,
        candidate_fixture: dict[str, Any],
        *,
        candidate_registry: Any = registry,
        candidate_inventory: TargetInventory = inventory,
        expected_message: str | None = None,
    ) -> None:
        try:
            _assert_readme_family_contract(
                root,
                candidate_registry,
                fixture=candidate_fixture,
                inventory=candidate_inventory,
            )
        except AssertionError as exc:
            if expected_message is not None and str(exc) != expected_message:
                raise AssertionError(
                    f"README fixture mutation proof {label} produced unexpected "
                    f"diagnostic: {exc}"
                ) from exc
            return
        raise AssertionError(f"README fixture mutation proof accepted {label}")

    literal_newline = copy.deepcopy(fixture)
    literal_newline["cases"][0]["document"] += "\\n"
    expect_rejection("a literal backslash-n document", literal_newline)

    invalid_document = copy.deepcopy(fixture)
    invalid_document["cases"][0]["document"] = ""
    expect_rejection("an invalid empty document", invalid_document)

    numeric_active_path = copy.deepcopy(fixture)
    numeric_active_path["activePaths"][0]["path"] = 7
    expect_rejection(
        "a numeric activePaths path",
        numeric_active_path,
        expected_message="invalid README fixture path: 7",
    )

    missing_retired_path = copy.deepcopy(fixture)
    missing_retired_path["retiredPaths"][0].pop("path")
    expect_rejection(
        "a missing retiredPaths path",
        missing_retired_path,
        expected_message="invalid README fixture path: None",
    )

    wrong_case_semantics = copy.deepcopy(fixture)
    duplicate_h1 = next(
        case for case in wrong_case_semantics["cases"] if case["name"] == "duplicate-h1"
    )
    duplicate_h1["document"] = wrong_case_semantics["cases"][0]["document"]
    expect_rejection("changed case semantics", wrong_case_semantics)

    swapped_flags = copy.deepcopy(fixture)
    existing = next(row for row in swapped_flags["activePaths"] if row["new"] is False)
    future = next(row for row in swapped_flags["activePaths"] if row["new"] is True)
    existing["new"], future["new"] = True, False
    expect_rejection("swapped existing/future flags", swapped_flags)

    changed_disposition = copy.deepcopy(fixture)
    changed_disposition["retiredPaths"][0]["profile"] = "readme/repository"
    expect_rejection("changed retired disposition", changed_disposition)

    overlap = copy.deepcopy(fixture)
    overlap_row = copy.deepcopy(overlap["retiredPaths"][0])
    overlap_row.pop("retiredBy")
    overlap_row.pop("destination")
    overlap["activePaths"].append(overlap_row)
    overlap["activePaths"].sort(key=lambda row: row["path"])
    expect_rejection("active/retired overlap", overlap)

    partial_retirement = copy.deepcopy(fixture)
    partial_retirement["retiredPaths"].pop()
    expect_rejection("partial nineteen-path retirement", partial_retirement)

    unknown_retirement = copy.deepcopy(fixture)
    unknown_retirement["retiredPaths"][0]["path"] = (
        "examples/aws/docs/unknown-retirement/README.md"
    )
    unknown_retirement["retiredPaths"].sort(key=lambda row: row["path"])
    expect_rejection("unknown retirement path", unknown_retirement)

    wrong_owner = copy.deepcopy(fixture)
    wrong_owner["retiredPaths"][0]["retiredBy"] = "ADM-007"
    expect_rejection("wrong retirement owner", wrong_owner)

    missing_destination = copy.deepcopy(fixture)
    missing_destination["retiredPaths"][0]["destination"] = (
        "docs/90.references/cloud-examples/aws/missing-snapshot.md"
    )
    expect_rejection("missing retirement destination", missing_destination)

    wrong_provider = copy.deepcopy(fixture)
    aws_retired = next(
        row
        for row in wrong_provider["retiredPaths"]
        if row["path"].startswith("examples/aws/")
    )
    aws_retired["destination"] = (
        "docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md"
    )
    expect_rejection("wrong-provider retirement destination", wrong_provider)

    unsorted_active = copy.deepcopy(fixture)
    unsorted_active["activePaths"][0], unsorted_active["activePaths"][1] = (
        unsorted_active["activePaths"][1],
        unsorted_active["activePaths"][0],
    )
    expect_rejection("unsorted activePaths", unsorted_active)

    duplicate_retired = copy.deepcopy(fixture)
    duplicate_retired["retiredPaths"][-1] = copy.deepcopy(
        duplicate_retired["retiredPaths"][0]
    )
    duplicate_retired["retiredPaths"].sort(key=lambda row: row["path"])
    expect_rejection("duplicate retiredPaths", duplicate_retired)

    retired_case = copy.deepcopy(fixture)
    retired_case["cases"][0]["path"] = retired_case["retiredPaths"][0]["path"]
    expect_rejection("parser case referencing retired path", retired_case)

    declared_new_paths = sorted(
        (
            PurePosixPath(row["path"])
            for row in fixture["activePaths"]
            if row["new"] is True
        ),
        key=lambda path: path.as_posix(),
    )
    if len(declared_new_paths) != 5:
        raise AssertionError(
            "README fixture mutation proof requires exact five program-created paths"
        )
    missing_paths = set(declared_new_paths[:2])
    missing_declared_inventory = TargetInventory(
        baseline_paths=inventory.baseline_paths,
        current_paths=tuple(
            path for path in inventory.current_paths if path not in missing_paths
        ),
        new_paths=tuple(
            path for path in inventory.new_paths if path not in missing_paths
        ),
        baseline_symlink_paths=inventory.baseline_symlink_paths,
        current_symlink_paths=inventory.current_symlink_paths,
    )
    expect_rejection(
        "fixture-declared active paths missing from current inventory",
        fixture,
        candidate_inventory=missing_declared_inventory,
        expected_message=(
            "README active path is absent: "
            f"{sorted(missing_paths, key=lambda path: path.as_posix())[0]}"
        ),
    )

    retired_path = PurePosixPath(fixture["retiredPaths"][0]["path"])
    retired_current_inventory = TargetInventory(
        baseline_paths=inventory.baseline_paths,
        current_paths=tuple(
            sorted(
                (*inventory.current_paths, retired_path),
                key=lambda path: path.as_posix(),
            )
        ),
        new_paths=inventory.new_paths,
        baseline_symlink_paths=inventory.baseline_symlink_paths,
        current_symlink_paths=inventory.current_symlink_paths,
    )
    expect_rejection(
        "retired path reintroduced into current inventory",
        fixture,
        candidate_inventory=retired_current_inventory,
    )

    extra_path = PurePosixPath("docs/undeclared-bridge/README.md")
    broad_raw_registry = copy.deepcopy(raw_registry)
    repository_profile = next(
        profile
        for profile in broad_raw_registry["profiles"]
        if profile["id"] == "readme/repository"
    )
    repository_profile["routes"].append(
        {
            "kind": "regex",
            "value": r"^docs/undeclared-[^/]+/README\.md$",
        }
    )
    broad_registry = validate_registry(root, broad_raw_registry)
    swapped_path = declared_new_paths[0]
    equal_count_swap_inventory = TargetInventory(
        baseline_paths=inventory.baseline_paths,
        current_paths=tuple(
            sorted(
                (
                    *(path for path in inventory.current_paths if path != swapped_path),
                    extra_path,
                ),
                key=lambda path: path.as_posix(),
            )
        ),
        new_paths=tuple(
            sorted(
                (
                    *(path for path in inventory.new_paths if path != swapped_path),
                    extra_path,
                ),
                key=lambda path: path.as_posix(),
            )
        ),
        baseline_symlink_paths=inventory.baseline_symlink_paths,
        current_symlink_paths=inventory.current_symlink_paths,
    )
    expect_rejection(
        "an equal-count missing-and-extra active README swap",
        fixture,
        candidate_registry=broad_registry,
        candidate_inventory=equal_count_swap_inventory,
    )


def _self_test(root: Path) -> int:
    raw_registry = _load_json(root / REGISTRY_PATH)
    fixture = _load_json(root / FIXTURE_PATH)
    actual_contract = tuple(
        (case.get("name"), case.get("mutation"), tuple(case.get("expected", ())))
        for case in fixture.get("cases", ())
    )
    if (
        fixture.get("schemaVersion") != 8
        or fixture.get(LOCAL_AGENT_FIXTURE_FIELD) != SAMPLE_PATH.as_posix()
        or actual_contract != EXPECTED_CASES
    ):
        print("FAIL document contract registry self-test: fixture contract mismatch")
        return 1

    with tempfile.TemporaryDirectory(prefix="document-registry-current-owner-") as tmp:
        fixture_root = Path(tmp)
        schema_target = fixture_root / SCHEMA_PATH
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / SCHEMA_PATH, schema_target)
        for raw_path in CURRENT_OWNER_SAMPLE_PATHS:
            target = fixture_root / raw_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Synthetic current authority\n", encoding="utf-8")
        for raw_path in (
            *REFERENCE_COLLECTION_SAMPLE_PATHS,
            *REFERENCE_PACK_SAMPLE_PATHS,
            *REFERENCE_MEMBER_SAMPLE_PATHS,
        ):
            target = fixture_root / raw_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# Synthetic reference contract\n", encoding="utf-8")
        fixture_template = (
            fixture_root / "tests/fixtures/document-contracts/self-test-prd.template.md"
        )
        fixture_template.parent.mkdir(parents=True, exist_ok=True)
        fixture_template.write_text("# Synthetic PRD form\n", encoding="utf-8")
        for raw_path, (
            document_type,
            status,
            updated,
        ) in LINEAGE_FIXTURE_DOCUMENTS.items():
            target = fixture_root / raw_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "---\n"
                f"title: 'Synthetic {raw_path}'\n"
                f"type: {document_type}\n"
                f"status: {status}\n"
                "owner: platform\n"
                f"updated: {updated}\n"
                "---\n\n"
                "# Synthetic lineage owner\n",
                encoding="utf-8",
            )
        for raw_path, content in LINEAGE_INVALID_FIXTURE_DOCUMENTS.items():
            target = fixture_root / raw_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        untracked = fixture_root / "docs/00.agent-governance/current-untracked.md"
        untracked.write_text("# Untracked synthetic authority\n", encoding="utf-8")
        symlink = fixture_root / "docs/00.agent-governance/current-symlink.md"
        symlink.symlink_to("current-alpha.md")
        research_root = fixture_root / "docs/90.references/research/2026-07-07-test"
        (research_root / "untracked.md").write_text(
            "# Untracked synthetic reference\n", encoding="utf-8"
        )
        (research_root / "symlink.md").symlink_to("accepted.md")
        (research_root / "directory.md").mkdir()
        subprocess.run(["git", "init", "--quiet"], cwd=fixture_root, check=True)
        subprocess.run(
            [
                "git",
                "add",
                "--",
                *CURRENT_OWNER_SAMPLE_PATHS,
                "docs/00.agent-governance/current-symlink.md",
                *REFERENCE_COLLECTION_SAMPLE_PATHS,
                *REFERENCE_PACK_SAMPLE_PATHS,
                *REFERENCE_MEMBER_SAMPLE_PATHS,
                "docs/90.references/research/2026-07-07-test/symlink.md",
                *LINEAGE_FIXTURE_DOCUMENTS,
                *LINEAGE_INVALID_FIXTURE_DOCUMENTS,
            ],
            cwd=fixture_root,
            check=True,
        )
        for name, mutation, expected in EXPECTED_CASES:
            if mutation in RAW_JSON_MUTATIONS:
                duplicate_path = fixture_root / f"{mutation}.json"
                duplicate_path.write_text(
                    (
                        '{"schemaVersion": 8, "schemaVersion": 8}\n'
                        if mutation == "duplicate-json-root-key"
                        else '{"outer": {"value": 1, "value": 2}}\n'
                    ),
                    encoding="utf-8",
                )
                try:
                    _load_json(duplicate_path)
                except DocumentContractError as exc:
                    actual = _ordered_rule_ids(exc.diagnostics)
                else:
                    actual = ()
                if actual != expected:
                    print(
                        f"FAIL document contract registry self-test: {name}: "
                        f"expected {list(expected)!r}, got {list(actual)!r}"
                    )
                    return 1
                continue
            mutated = (
                copy.deepcopy(raw_registry)
                if mutation in V8_MUTATIONS
                else _minimal_fixture_registry()
            )
            _mutate(mutated, mutation)
            diagnostics = ()
            try:
                validation_root = root if mutation in V8_MUTATIONS else fixture_root
                registry = validate_registry(validation_root, mutated)
            except DocumentContractError as exc:
                diagnostics = exc.diagnostics
            else:
                diagnostics = classify_paths(registry, (SAMPLE_PATH,))
            actual = _ordered_rule_ids(diagnostics)
            if actual != expected:
                print(
                    f"FAIL document contract registry self-test: {name}: "
                    f"expected {list(expected)!r}, got {list(actual)!r}"
                )
                return 1

        legacy = _minimal_fixture_registry()
        legacy["$id"] = "https://hy-home.k8s/schemas/document-profiles-5.schema.json"
        legacy["schemaVersion"] = 5
        del legacy["documentContracts"]
        legacy["programLineage"] = {
            "prd": "005",
            "ard": "0008",
            "specs": ["026", "033"],
        }
        legacy_v6 = _convert_legacy_v5_fixture(legacy)
        registry_target = fixture_root / REGISTRY_PATH
        registry_target.parent.mkdir(parents=True, exist_ok=True)
        registry_target.write_text(
            json.dumps(legacy_v6, indent=2) + "\n", encoding="utf-8"
        )
        try:
            load_registry(fixture_root)
        except DocumentContractError as exc:
            if _ordered_rule_ids(exc.diagnostics) != ("REGISTRY_SCHEMA",):
                print(
                    "FAIL document contract registry self-test: "
                    "production legacy-v6 rejection returned wrong rule"
                )
                return 1
        else:
            print(
                "FAIL document contract registry self-test: "
                "production loader accepted legacy-v6 input"
            )
            return 1
        migrated = validate_registry(
            fixture_root, _convert_legacy_v6_fixture(legacy_v6)
        )
        if (
            len(migrated.program_lineage) != 1
            or tuple(item.spec_id for item in migrated.program_lineage[0].tranches)
            != ("026",)
            or tuple(item.spec_id for item in migrated.program_lineage[0].follow_ups)
            != ("033",)
        ):
            print(
                "FAIL document contract registry self-test: "
                "private v5-to-v6-to-v8 fixture conversion projection differs"
            )
            return 1

    try:
        _assert_reserved_gemini_native_surface_mutation_proofs()
        _assert_retired_cloud_sdlc_surface_mutation_proofs()
        _assert_parser_safety()
        _assert_inventory_safety(root)
        parity_case_count = _assert_template_source_mutation_proofs(root, raw_registry)
        _assert_role_inheritance_mutation_proof(root, raw_registry)
        profile_count, template_count = _assert_positive_coverage(
            root, raw_registry, fixture
        )
        registry = validate_registry(root, raw_registry)
        _assert_program_lineage_projection(registry)
        _assert_document_contract_projection(registry)
        readme_fixture = _load_json(root / README_FIXTURE_PATH)
        inventory = enumerate_target_markdown(root)
        _assert_readme_family_contract(
            root,
            registry,
            fixture=readme_fixture,
            inventory=inventory,
        )
        _assert_readme_fixture_mutation_proofs(
            root,
            raw_registry,
            registry,
            readme_fixture,
            inventory,
        )
    except (AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry self-test: {exc}")
        return 1

    print(
        "PASS document contract registry self-test: "
        f"{len(EXPECTED_CASES)} cases, {profile_count} profiles, {template_count} templates; "
        f"template/source parity {parity_case_count}/11, README fixture 8/8, "
        "private v5/v6 migration fixture, mutation probes passed"
    )
    return 0


def _print_diagnostic(diagnostic: Any) -> None:
    print(
        f"FAIL {diagnostic.rule_id} {diagnostic.path.as_posix()}: "
        f"expected {diagnostic.expected}; actual {diagnostic.actual}"
    )


def main() -> int:
    args = _parse_args()
    root = args.root.absolute()
    if args.self_test:
        return _self_test(root)

    try:
        registry = load_registry(root)
        _assert_template_source_parity(registry)
        _assert_reserved_gemini_native_surfaces_absent(root)
        _assert_retired_cloud_sdlc_surfaces_absent(root)
        profile_ids = {profile.profile_id for profile in registry.profiles}
        is_readme_family = args.profile == "readme"
        if args.profile and not is_readme_family and args.profile not in profile_ids:
            raise ValueError(f"unknown profile: {args.profile}")
        inventory = enumerate_target_markdown(
            root, include_paths=tuple(args.include_path)
        )
        readme_counts = (
            _assert_readme_family_contract(root, registry, inventory=inventory)
            if is_readme_family
            else None
        )
    except DocumentContractError as exc:
        for diagnostic in exc.diagnostics:
            _print_diagnostic(diagnostic)
        return 1
    except (AssertionError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"FAIL document contract registry: {exc}")
        return 1

    diagnostics = classify_paths(registry, inventory.current_paths)
    uncovered_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_UNCOVERED" for diagnostic in diagnostics
    )
    ambiguous_count = sum(
        diagnostic.rule_id == "REGISTRY_ROUTE_AMBIGUOUS" for diagnostic in diagnostics
    )
    if diagnostics:
        for diagnostic in diagnostics:
            _print_diagnostic(diagnostic)
    print(
        f"baseline={len(inventory.baseline_paths)} "
        f"new={len(inventory.new_paths)} "
        f"programs={len(registry.program_lineage)} "
        f"uncovered={uncovered_count} ambiguous={ambiguous_count}"
    )
    if diagnostics:
        return 1

    selected_count = len(inventory.current_paths)
    if args.profile:
        if args.profile == "readme":
            baseline_count, declared_final_count, selected_count = readme_counts
            print(
                f"README baseline={baseline_count} active_current={selected_count} "
                f"retired={declared_final_count - selected_count} "
                f"declared_total={declared_final_count} schema=3 exact_set=yes "
                "uncovered=0 ambiguous=0"
            )
        else:
            selected_count = sum(
                classify_path(registry, path).profile_id == args.profile
                for path in inventory.current_paths
            )
    print(
        f"PASS document contract registry: {selected_count} paths "
        f"({args.mode}, tracked-only plus explicit includes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
