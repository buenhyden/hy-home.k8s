#!/usr/bin/env python3
"""Validate registry-owned document lifecycle events against deterministic Git bases."""

from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from types import MappingProxyType, ModuleType
from typing import Callable, Mapping, Sequence

from archive_cutover_manifest import (
    ARCHIVE_PROFILE,
    ARCHIVE_TEMPLATE,
    ARCHIVE_TEMPLATE_PROFILE,
    BASE_REGISTRY_BLOB_OID,
    BASE_REGISTRY_ID,
    BASE_REGISTRY_VERSION,
    CUTOVER_BASE_COMMIT,
    EXPECTED_ARCHIVE_PATHS,
    LEGACY_ARCHIVE_PROFILE,
    LEGACY_ARCHIVE_TEMPLATE,
    LEGACY_ARCHIVE_TEMPLATE_PROFILE,
    PROPOSED_REGISTRY_ID,
    PROPOSED_REGISTRY_BLOB_OID,
    PROPOSED_REGISTRY_VERSION,
)
from document_contracts import (
    RETIRED_REGISTRY_PATH,
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    DocumentProfile,
    Registry,
    Route,
    classify_path,
    enumerate_target_markdown,
    load_json_file,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (
    LIFECYCLE_RULE_IDS,
    SPECIFICATION_PROFILES,
    LifecycleDiagnostic,
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    LifecycleRename,
    compare_lifecycle,
    document_from_text,
    lifecycle_diagnostic_sort_key,
    validate_snapshot_documents,
)
from archive_validation import (
    MIG0002_DOCUMENT_SHA256,
    MIGRATION_DOCUMENT_MAX_BYTES,
    parse_pinned_migration_control,
    read_staged_blob_bounded,
    validate_archive_immutability,
)
from archive_recovery import (
    ArchiveContractError,
    WORK107_LEGACY_ARCHIVE_COMMIT,
    WORK107_MIGRATION_PATH,
    build_work107_migration_rows,
    parse_work107_migration_document,
    render_work107_migration_document,
    render_work107_stable_envelope,
    validate_work107_migration_rows,
    _git_capture_bounded,
)
from document_authority import (
    AuthorityError,
    REGISTRY_PATH as CURRENT_REGISTRY_PATH,
    assert_staged_authority_matches_worktree,
)


FIXTURE_PATH = PurePosixPath("tests/fixtures/document-lifecycle.json")
OBJECT_ID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
FIXED_GIT_ENVIRONMENT = {
    "GIT_AUTHOR_NAME": "Lifecycle Self Test",
    "GIT_AUTHOR_EMAIL": "lifecycle@example.invalid",
    "GIT_COMMITTER_NAME": "Lifecycle Self Test",
    "GIT_COMMITTER_EMAIL": "lifecycle@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_GRAFT_FILE": os.devnull,
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_TERMINAL_PROMPT": "0",
}
GIT_GLOBAL_ARGUMENTS = (
    "--no-replace-objects",
    "-c",
    "advice.graftFileDeprecated=false",
    "-c",
    "core.fsmonitor=false",
    "-c",
    f"core.hooksPath={os.devnull}",
    "-c",
    "user.name=Lifecycle Self Test",
    "-c",
    "user.email=lifecycle@example.invalid",
    "-c",
    "diff.renameLimit=0",
    "-c",
    "diff.renames=true",
)
GIT_CAPTURE_MAX_BYTES = 2 * 1024 * 1024
GIT_SIZE_OUTPUT_MAX_BYTES = 64
DOCUMENT_BLOB_MAX_BYTES = 1024 * 1024
EXPECTED_ENTRYPOINTS = (
    "scripts/document_lifecycle.py",
    "scripts/validate-document-lifecycle.py",
)
EXPECTED_RULE_IDS = (
    "LIFECYCLE-CREATE",
    "LIFECYCLE-DELETE",
    "LIFECYCLE-RENAME",
    "LIFECYCLE-PROFILE-CHANGE",
    "LIFECYCLE-STATE",
    "LIFECYCLE-EDGE",
    "LIFECYCLE-EVIDENCE",
    "LIFECYCLE-BASE",
    "LIFECYCLE-BASE-DEFER",
)
AGENT_ROSTER_ADMISSION_BASE_COMMIT = (
    "e324d4c1fa49ef7e508fa07c32e7f054f5a3a05e"  # pragma: allowlist secret
)
AGENT_ROSTER_ADMISSION_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/agent-roster-admission.json"
)
AGENT_HARNESS_CONTRACT_PATH = PurePosixPath(
    "docs/00.agent-governance/contracts/harness-contract.json"
)
AGENT_ROSTER_CONTRACT_PATHS = frozenset(
    {
        AGENT_ROSTER_ADMISSION_CONTRACT_PATH,
        AGENT_HARNESS_CONTRACT_PATH,
    }
)
AGENT_ROSTER_ROLE_IDS = (
    "supervisor",
    "code-reviewer",
    "doc-writer",
    "gitops-reviewer",
    "incident-responder",
    "k8s-implementer",
    "network-reviewer",
    "observability-reviewer",
    "security-auditor",
    "wiki-curator",
    "docs-researcher",
    "quality-engineer",
)
AGENT_ROSTER_SURFACE_IDS = ("local", "claude", "codex", "gemini")
AGENT_ROSTER_CANDIDATE_IDS = ("docs-researcher", "quality-engineer")
AGENT_ROSTER_BASE_DEFERRED_CLASSES = (
    "runtime",
    "provider-discovery",
    "provider-authentication",
    "hosted-ci",
    "remote",
    "live",
)
AGENT_ROSTER_DEFERRED_CLASSES = (
    "runtime",
    "provider-discovery",
    "provider-authentication",
    "model-resolution",
    "hosted-ci",
    "remote",
    "live",
    "agent-evaluation",
    "model-fitness",
)
AGENT_ROSTER_EVALUATION_CLASSES = (
    "positive",
    "negative-adversarial",
    "refusal-stop",
    "handoff",
)
AGENT_ROSTER_CUTOVER_PATHS = (
    PurePosixPath(".agents/agents/docs-researcher.md"),
    PurePosixPath(".agents/agents/quality-engineer.md"),
    PurePosixPath(".claude/agents/docs-researcher.md"),
    PurePosixPath(".claude/agents/quality-engineer.md"),
)
AGENT_ROSTER_CUTOVER_MUTATIONS = (
    "exact",
    "wrong-mode",
    "wrong-base",
    "missing-path",
    "extra-path",
    "wrong-profile",
    "base-already-contains-path",
    "wrong-admission-state",
    "wrong-admission-inventory",
    "wrong-evidence-class",
    "wrong-claim-boundary",
    "admission-verdict-preclaim",
    "promotion-authorization-preclaim",
    "runtime-preclaim",
    "missing-provider-deferred-state",
    "missing-deferred-evidence",
    "missing-live-deferred-state",
    "wrong-candidate-surface",
    "candidate-admission-preclaim",
    "candidate-admission-authority-preclaim",
    "wrong-evaluation-baseline",
    "wrong-independent-adjudication",
    "wrong-harness-inventory",
    "wrong-harness-projection",
)
AGENT_ROSTER_CONTRACT_BLOB_MUTATIONS = (
    "malformed",
    "missing",
    "non-object",
    "duplicate-key",
)

WORK105_CUTOVER_BASE_COMMIT = "a6fa1806364ea0472baaad0906e1b5e4ddac8602"
WORK105_BASE_REGISTRY_BLOB_OID = "fc9ba039906ef240d076de5eeb6c584b681ae09f"
WORK105_PROPOSED_REGISTRY_BLOB_OID = "fd842f60e801a39435600f35a27f22e1c659f1bd"
WORK105_BASE_REGISTRY_PROJECTION_SHA256 = (
    "ef2e31327be14a3117898a8c0eb661f022fd96cac4e1d3f9362925e189c63daf"  # pragma: allowlist secret
)
WORK105_PROPOSED_REGISTRY_PROJECTION_SHA256 = (
    "17d49aa94403200ea9795d8c14f3fb9137e4f266ebb91e0449b937eecea6ff50"  # pragma: allowlist secret
)
WORK105_RETIRED_PROFILE_IDS = frozenset(
    {
        "sdlc/ard",  # Retired WORK-105 base input.
        "template/sdlc/ard",  # Retired WORK-105 base input.
        "sdlc/api-spec",  # Retired WORK-105 base input.
        "template/sdlc/api-spec",  # Retired WORK-105 base input.
    }
)
WORK105_TERMINAL_PROFILE_IDS = frozenset(
    {
        "sdlc/ad",
        "template/sdlc/ad",
        "sdlc/interface",
        "template/sdlc/interface",
        "sdlc/srs",
        "template/sdlc/srs",
    }
)
WORK105_AD_CUTOVER = (
    ("0004-argo-rollouts-progressive-delivery", "active"),
    ("0005-argo-notifications-slack", "active"),
    ("0006-workspace-agent-governance-platform", "active"),
    ("0007-current-local-gitops-platform", "active"),
    ("0008-workspace-document-assurance-operating-model", "accepted"),
    ("0009-document-lifecycle-evidence-operating-model", "accepted"),
    ("0010-repository-delivery-evidence-architecture", "active"),
    ("0011-document-taxonomy-consolidation-architecture", "active"),
)
WORK105_ADR0023_PATH = PurePosixPath(
    "docs/02.architecture/decisions/"
    "0023-work-unit-document-taxonomy-and-governance-authority.md"
)
WORK105_ADR0024_PATH = PurePosixPath(
    "docs/02.architecture/decisions/"
    "0024-terminal-artifact-identity-and-archive-layout.md"
)
WORK105_LEGACY_AD0011_PATH = PurePosixPath(
    "docs/02.architecture/requirements/"
    "0011-document-taxonomy-consolidation-architecture.md"
)
WORK105_ADR0023_BASE_BLOB_OID = "6424c13f4728ff6418bcdac9796df9c5673d2124"
WORK105_ADR0023_PROPOSED_BLOB_OID = "7200ec9eb873c971876583b5ba41921d0fdfb24d"
WORK105_ADR0023_BASE_SHA256 = (
    "fadbd95c581a0874797666e200f283d0f5fdc6c103643cc653e387062adbe53a"  # pragma: allowlist secret
)
WORK105_ADR0023_PROPOSED_SHA256 = (
    "717714ce153cbd75ca5a77beb42a24cd1b146f25b1112d492e30d9fd214348d5"  # pragma: allowlist secret
)
WORK105_ADR0023_RECIPROCAL_ROW = (
    "| [ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md) | "
    "Partially supersedes only terminal Stage 98 date/mirror-path immutability; "
    "preserves transition safety, Stage 05 stability, Release exclusion, and "
    "every unrelated decision | "
    "[Spec 052](../../03.specs/052-document-taxonomy-consolidation/spec.md) |"
)

WORK107_BASE_REGISTRY_BLOB_OID = "fd842f60e801a39435600f35a27f22e1c659f1bd"
WORK107_PROPOSED_REGISTRY_BLOB_OID = "7182c40ab8ee6b40173b408ec2c366314916f1e3"
WORK107_MIGRATION_BLOB_OID = "619ddc09b38c0a0a5c8254de6fbdcf3c1deb60d6"
WORK107_MIGRATION_DOCUMENT_SHA256 = (
    "7049f8b94bdb80566ad94be5d9e9e899d7d06e1b9d31191ad769cd905717de5e"  # pragma: allowlist secret
)
WORK107_MIGRATION_TEMPLATE_PATH = PurePosixPath(
    "docs/99.templates/templates/common/archive-migration.template.md"
)
WORK107_MIGRATION_TEMPLATE_BLOB_OID = "dc3164eafd322e8139164cc16342de43fc3a72e8"
WORK108_BASE_COMMIT = "db320b596904b52e184f01cd1b56467132ac9117"
WORK108_BASE_REGISTRY_BLOB_OID = "7182c40ab8ee6b40173b408ec2c366314916f1e3"
WORK108_PROPOSED_REGISTRY_BLOB_OID = "ce8da8f205cee1bba075bef7b26079a0708324b1"
WORK108_BASE_MIGRATION_BLOB_OID = "619ddc09b38c0a0a5c8254de6fbdcf3c1deb60d6"
WORK108_PROPOSED_MIGRATION_BLOB_OID = "b304c92c9c9032ebfe3be9156bd3f808ed1f5fb9"

WORK054_WP002_BASE_COMMIT = "de72eb7d1828aeecf36bfe4ce35a892f9a8be729"
WORK054_WP002_SOURCE_COMMIT = "160ce006969ddb49965c8af193f3e9ee290e18a8"
WORK054_WP002_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/"
    "mig-0002-sdlc-document-and-governance-consolidation.md"
)
WORK054_WP002_MIGRATION_SHA256 = MIG0002_DOCUMENT_SHA256
WORK054_WP002_SPEC_ROOT = PurePosixPath(
    "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation"
)
WORK054_WP002_SPEC_PATHS = (
    WORK054_WP002_SPEC_ROOT / "spec.md",
    WORK054_WP002_SPEC_ROOT / "plan.md",
    WORK054_WP002_SPEC_ROOT / "tasks.md",
)
WORK054_WP002_DECISION_PATH = PurePosixPath(
    "docs/02.architecture/decisions/0025-four-digit-document-path-identity.md"
)
WORK054_WP002_DECISION_SHA256 = (
    "b35d625a98e1c1d3089d20b8ea56669dbbbee32934a21112a8a29e70744ed5c4"  # pragma: allowlist secret
)
WORK054_WP002_LEDGER_KEYS = (
    "legacy_path",
    "stable_path",
    "artifact_id",
    "action",
    "replacement",
    "source_commit",
    "source_blob",
    "content_sha256",
    "reason",
)
WORK054_WP002_MOVE_REASON = (
    "Normalize the active SDLC path identity from three digits to four digits "
    "without changing the artifact meaning."
)
WORK054_WP002_STAGE04_REASON = (
    "Retire the Stage 04 navigation owner after co-locating Plan and Tasks "
    "with the Stage 03 work unit."
)
WORK054_WP002_STAGE00_MERGE_REASON = (
    "Merge duplicate route-sensitive authoring guidance into the canonical "
    "Stage 00 document-authoring owner."
)
WORK054_WP002_LIFECYCLE_MERGE_REASON = (
    "Merge common lifecycle and legacy-disposition guidance into the canonical "
    "Stage 99 document-lifecycle owner."
)
WORK054_WP002_CONTRACT_MERGE_REASON = (
    "Merge route, frontmatter, and profile-selection guidance into the canonical "
    "Stage 99 document-contract owner."
)
WORK054_WP002_LEDGER_OVERVIEW = (
    "It records 141 three-to-four-digit moves, the three Stage 04 index "
    "replacements, and ten route-sensitive Stage 00/99 owner merges."
)
WORK054_WP002_STAGE04_REPLACEMENTS = MappingProxyType(
    {
        "docs/04.execution/README.md": "docs/03.specs/README.md",
        "docs/04.execution/plans/README.md": (
            "docs/99.templates/templates/sdlc/execution/plan.template.md"
        ),
        "docs/04.execution/tasks/README.md": (
            "docs/99.templates/templates/sdlc/execution/task.template.md"
        ),
    }
)
WORK054_WP002_GOVERNANCE_MERGES = MappingProxyType(
    {
        "docs/00.agent-governance/rules/document-stage-routing.md": (
            "docs/00.agent-governance/rules/document-authoring.md"
        ),
        "docs/00.agent-governance/rules/documentation-protocol.md": (
            "docs/00.agent-governance/rules/document-authoring.md"
        ),
        "docs/00.agent-governance/rules/stage-authoring-matrix.md": (
            "docs/00.agent-governance/rules/document-authoring.md"
        ),
        "docs/00.agent-governance/rules/stage-checklists.md": (
            "docs/00.agent-governance/rules/document-authoring.md"
        ),
        "docs/99.templates/support/common-documentation-governance.md": (
            "docs/99.templates/support/document-lifecycle.md"
        ),
        "docs/99.templates/support/documentation-contract.md": (
            "docs/99.templates/support/document-contract.md"
        ),
        "docs/99.templates/support/frontmatter-schema.md": (
            "docs/99.templates/support/document-contract.md"
        ),
        "docs/99.templates/support/legacy-cleanup-rules.md": (
            "docs/99.templates/support/document-lifecycle.md"
        ),
        "docs/99.templates/support/sdlc-governance.md": (
            "docs/99.templates/support/document-lifecycle.md"
        ),
        "docs/99.templates/support/template-routing.md": (
            "docs/99.templates/support/document-contract.md"
        ),
    }
)
WORK054_WP002_STANDALONE_REASON = (
    "Direct human-approved B-scope SDLC and AI-agent governance consolidation "
    "including Stage 90"
)
WORK054_WP002_LEDGER_PATTERN = re.compile(
    r"<!-- archive-migration-ledger:v1 format=json -->\n\n"
    r"```json\n(?P<ledger>\[.*?\])\n```",
    re.DOTALL,
)
WORK054_WP002_REQUIREMENT_PATTERN = re.compile(
    r"docs/01\.requirements/(?P<id>[0-9]{3})(?P<tail>-[a-z0-9-]+\.md)"
)
WORK054_WP002_SPEC_PATTERN = re.compile(
    r"docs/03\.specs/(?P<id>[0-9]{3})(?P<tail>-[a-z0-9-]+)/"
    r"(?P<name>spec|plan|tasks|agent-design)\.md"
)

WORK054_WP003_BASE_COMMIT = "128beada377f18bc9f942c8ebb3e27e1f2fdcfae"
WORK054_WP003_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/"
    "mig-0003-agent-governance-control-plane-consolidation.md"
)
WORK054_WP003_MIGRATION_SHA256 = (
    "51fe8d35febac457e562f997a711ce152a98cda67b3aec2ccd8ed08bd3ac3d42"  # pragma: allowlist secret
)
WORK054_WP003_LEDGER_KEYS = WORK054_WP002_LEDGER_KEYS
WORK054_WP003_OWNER_RETIREMENTS = (
    {
        "legacy_path": "docs/00.agent-governance/common-governance.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/harness-catalog.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "de7e7edfe177ff349cd3824aebd82418adff95d7",  # pragma: allowlist secret
        "content_sha256": "c5da620d5f6c1aa26f2e0d99769872b90c6d2ec2fdb3c03813be27992f43e4ba",  # pragma: allowlist secret
    },
    {
        "legacy_path": "docs/00.agent-governance/harness-implementation-map.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/harness-catalog.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "7e7a6d64a05be91658cc6657cd640491153a615a",  # pragma: allowlist secret
        "content_sha256": "3ea2f89c3ba17fbf0bac64533cbb5a378a85c062a020881a3844cfa190c9c218",  # pragma: allowlist secret
    },
    {
        "legacy_path": "docs/00.agent-governance/providers/agents-md.md",
        "stable_path": None,
        "artifact_id": None,
        "action": "merged",
        "replacement": "docs/00.agent-governance/providers/codex.md",
        "source_commit": WORK054_WP003_BASE_COMMIT,
        "source_blob": "06d9a7a5453ac8b6e28268850467e3e96de06dc9",  # pragma: allowlist secret
        "content_sha256": "5ea07c187ea54061f5ecc770a58a99edf40dfd73372ba8fc9e1d4ab14bf85bae",  # pragma: allowlist secret
    },
)

WORK054_WP004A_BASE_COMMIT = "0860f1723b81b407391055cbec4ca7331a8e9a73"
WORK054_WP004A_OWNER_PATHS = (
    PurePosixPath("docs/00.agent-governance/policies/document-lifecycle.md"),
    PurePosixPath("docs/00.agent-governance/sdlc.md"),
)
WORK054_WP004A_REQUIRED_CHANGED_PATHS = (
    CURRENT_REGISTRY_PATH,
    PurePosixPath("docs/99.templates/contracts/document-profile.schema.json"),
    PurePosixPath("docs/99.templates/contracts/frontmatter.schema.json"),
    PurePosixPath("docs/99.templates/contracts/route-contract.json"),
    PurePosixPath("docs/99.templates/README.md"),
    PurePosixPath("docs/00.agent-governance/README.md"),
    PurePosixPath(
        "docs/03.specs/0054-sdlc-document-and-agent-governance-"
        "consolidation/tasks.md"
    ),
    *WORK054_WP004A_OWNER_PATHS,
)


def _registry_profile_ids(raw_registry: Mapping[str, object]) -> frozenset[str]:
    profiles = raw_registry.get("profiles")
    if not isinstance(profiles, list):
        return frozenset()
    return frozenset(
        profile["id"]
        for profile in profiles
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    )


def _work105_registry_projection_sha256(
    raw_registry: Mapping[str, object],
) -> str:
    return hashlib.sha256(
        json.dumps(
            dict(raw_registry),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def finite_work105_form_cutover_paths(
    *,
    mode: str,
    base_commit: str,
    base_registry_oid: str,
    proposed_registry_oid: str,
    base_registry: Mapping[str, object],
    proposed_registry: Mapping[str, object],
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> frozenset[PurePosixPath]:
    """Admit only the pinned, complete WORK-105 form migration event set."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != WORK105_CUTOVER_BASE_COMMIT
        or base_registry_oid != WORK105_BASE_REGISTRY_BLOB_OID
        or proposed_registry_oid != WORK105_PROPOSED_REGISTRY_BLOB_OID
    ):
        return frozenset()
    if any(
        registry.get("$id")
        != "https://hy-home.k8s/schemas/document-profiles-8.schema.json"
        or registry.get("schemaVersion") != 8
        or registry.get("routeState") != "transition"
        for registry in (base_registry, proposed_registry)
    ):
        return frozenset()
    if (
        _work105_registry_projection_sha256(base_registry)
        != WORK105_BASE_REGISTRY_PROJECTION_SHA256
        or _work105_registry_projection_sha256(proposed_registry)
        != WORK105_PROPOSED_REGISTRY_PROJECTION_SHA256
    ):
        return frozenset()
    base_profile_ids = _registry_profile_ids(base_registry)
    proposed_profile_ids = _registry_profile_ids(proposed_registry)
    if (
        base_profile_ids - proposed_profile_ids != WORK105_RETIRED_PROFILE_IDS
        or proposed_profile_ids - base_profile_ids != WORK105_TERMINAL_PROFILE_IDS
    ):
        return frozenset()

    consumed: set[PurePosixPath] = set()
    old_ad_paths: set[PurePosixPath] = set()
    new_ad_paths: set[PurePosixPath] = set()
    for token, status in WORK105_AD_CUTOVER:
        old_path = PurePosixPath(  # Retired WORK-105 base route.
            f"docs/02.architecture/requirements/{token}.md"  # Retired base route.
        )
        new_path = PurePosixPath(f"docs/02.architecture/descriptions/ad-{token}.md")
        if (
            base_documents.get(old_path)
            != LifecycleDocument(old_path, "sdlc/ard", status)  # Retired base type.
            or old_path in proposed_documents
            or new_path in base_documents
            or proposed_documents.get(new_path)
            != LifecycleDocument(new_path, "sdlc/ad", status)
        ):
            return frozenset()
        old_ad_paths.add(old_path)
        new_ad_paths.add(new_path)
        consumed.update((old_path, new_path))

    if (
        {
            path
            for path, document in base_documents.items()
            if document.profile_id == "sdlc/ard"  # Retired WORK-105 base type.
        }
        != old_ad_paths
        or {
            path
            for path, document in proposed_documents.items()
            if document.profile_id == "sdlc/ad"
        }
        != new_ad_paths
        or any(
            document.profile_id == "sdlc/api-spec"  # Retired authored base type.
            for document in (*base_documents.values(), *proposed_documents.values())
        )
    ):
        return frozenset()

    exact_forms = (
        (
            "docs/02.architecture/requirements/README.md",  # Retired base route.
            "readme/collection-index",
            "base",
        ),
        (
            "docs/02.architecture/descriptions/README.md",
            "readme/collection-index",
            "proposed",
        ),
        (
            "docs/99.templates/templates/sdlc/architecture/ard.template.md",  # Retired.
            "template/sdlc/ard",  # Retired WORK-105 base type.
            "base",
        ),
        (
            "docs/99.templates/templates/sdlc/architecture/ad.template.md",
            "template/sdlc/ad",
            "proposed",
        ),
        (
            "docs/99.templates/templates/sdlc/specs/api-spec.template.md",  # Retired.
            "template/sdlc/api-spec",  # Retired authored base type.
            "base",
        ),
        (
            "docs/99.templates/templates/sdlc/requirements/interface.template.md",
            "template/sdlc/interface",
            "proposed",
        ),
        (
            "docs/99.templates/templates/sdlc/requirements/srs.template.md",
            "template/sdlc/srs",
            "proposed",
        ),
    )
    for raw_path, profile_id, side in exact_forms:
        path = PurePosixPath(raw_path)
        present = base_documents if side == "base" else proposed_documents
        absent = proposed_documents if side == "base" else base_documents
        if (
            present.get(path) != LifecycleDocument(path, profile_id, None)
            or path in absent
        ):
            return frozenset()
        consumed.add(path)
    return frozenset(consumed)


def _git_blob_oid(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324 - Git identity


def _work107_without_outer_artifact_id(
    content: bytes, expected_artifact_id: str
) -> bytes | None:
    expected = f'artifact_id: "{expected_artifact_id}"'.encode("ascii")
    lines = content.splitlines(keepends=True)
    matches = [
        index
        for index, line in enumerate(lines)
        if line.rstrip(b"\r\n") == expected
    ]
    if len(matches) != 1 or matches[0] == 0:
        return None
    index = matches[0]
    if not lines[index - 1].startswith(b"updated:"):
        return None
    return b"".join(lines[:index] + lines[index + 1 :])


def finite_work107_archive_rehome_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_registry_oid: str,
    proposed_registry_oid: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only the reviewed 93-to-93 WORK-107 stable archive rehome."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != WORK107_LEGACY_ARCHIVE_COMMIT
        or base_registry_oid != WORK107_BASE_REGISTRY_BLOB_OID
        or proposed_registry_oid != WORK107_PROPOSED_REGISTRY_BLOB_OID
    ):
        return frozenset()

    migration_path = PurePosixPath(WORK107_MIGRATION_PATH)
    if (
        migration_path in base_blobs
        or proposed_blobs.get(migration_path) != WORK107_MIGRATION_BLOB_OID
        or WORK107_MIGRATION_TEMPLATE_PATH in base_blobs
        or proposed_blobs.get(WORK107_MIGRATION_TEMPLATE_PATH)
        != WORK107_MIGRATION_TEMPLATE_BLOB_OID
    ):
        return frozenset()
    migration_bytes = _blob_bytes(root, WORK107_MIGRATION_BLOB_OID)
    if (
        hashlib.sha256(migration_bytes).hexdigest()
        != WORK107_MIGRATION_DOCUMENT_SHA256
    ):
        return frozenset()
    rows = build_work107_migration_rows(root)
    expected_migration = _work107_without_outer_artifact_id(
        render_work107_migration_document(rows),
        "MIG-0001",
    )
    if expected_migration != migration_bytes:
        return frozenset()

    consumed: set[PurePosixPath] = {
        migration_path,
        WORK107_MIGRATION_TEMPLATE_PATH,
    }
    for row in rows:
        legacy_path = PurePosixPath(str(row["legacy_path"]))
        stable_path = PurePosixPath(str(row["stable_path"]))
        legacy_oid = str(row["legacy_envelope_blob"])
        if (
            base_blobs.get(legacy_path) != legacy_oid
            or legacy_path in proposed_blobs
            or stable_path in base_blobs
        ):
            return frozenset()
        stable_bytes = _work107_without_outer_artifact_id(
            render_work107_stable_envelope(
                _blob_bytes(root, legacy_oid),
                row,
            ),
            str(row["artifact_id"]),
        )
        if stable_bytes is None:
            return frozenset()
        if proposed_blobs.get(stable_path) != _git_blob_oid(stable_bytes):
            return frozenset()
        consumed.update((legacy_path, stable_path))
    if len(consumed) != 188:
        return frozenset()
    return frozenset(consumed)


def _work108_artifact_projection(
    path: str, base: bytes, proposed: bytes, expected_artifact_id: str
) -> bool:
    expected = f'artifact_id: "{expected_artifact_id}"'.encode("ascii")
    lines = proposed.splitlines(keepends=True)
    if not lines or lines[0].rstrip(b"\r\n") != b"---":
        return False
    try:
        frontmatter_end = next(
            index
            for index, line in enumerate(lines[1:], 1)
            if line.rstrip(b"\r\n") == b"---"
        )
    except StopIteration:
        return False
    matches = [
        index
        for index, line in enumerate(lines[:frontmatter_end])
        if line.rstrip(b"\r\n") == expected
    ]
    if len(matches) != 1:
        return False
    index = matches[0]
    return (
        index > 0
        and lines[index - 1].startswith(b"updated:")
        and b"".join(lines[:index] + lines[index + 1 :]) == base
        and PurePosixPath(path).as_posix() == path
    )


def finite_work108_artifact_identity_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_registry_oid: str,
    proposed_registry_oid: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only the reviewed WORK-108 outer artifact-ID insertion."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != WORK108_BASE_COMMIT
        or base_registry_oid != WORK108_BASE_REGISTRY_BLOB_OID
        or proposed_registry_oid != WORK108_PROPOSED_REGISTRY_BLOB_OID
    ):
        return frozenset()
    migration_path = PurePosixPath(WORK107_MIGRATION_PATH)
    if (
        base_blobs.get(migration_path) != WORK108_BASE_MIGRATION_BLOB_OID
        or proposed_blobs.get(migration_path) != WORK108_PROPOSED_MIGRATION_BLOB_OID
    ):
        return frozenset()
    base_migration = _blob_bytes(root, WORK108_BASE_MIGRATION_BLOB_OID)
    proposed_migration = _blob_bytes(root, WORK108_PROPOSED_MIGRATION_BLOB_OID)
    if not _work108_artifact_projection(
        migration_path.as_posix(),
        base_migration,
        proposed_migration,
        "MIG-0001",
    ):
        return frozenset()
    try:
        rows = validate_work107_migration_rows(
            root,
            parse_work107_migration_document(proposed_migration),
        )
    except ArchiveContractError:
        return frozenset()
    consumed = {migration_path}
    for row in rows:
        path = PurePosixPath(str(row["stable_path"]))
        base_oid = base_blobs.get(path)
        proposed_oid = proposed_blobs.get(path)
        if base_oid is None or proposed_oid is None or base_oid == proposed_oid:
            return frozenset()
        if not _work108_artifact_projection(
            path.as_posix(),
            _blob_bytes(root, base_oid),
            _blob_bytes(root, proposed_oid),
            str(row["artifact_id"]),
        ):
            return frozenset()
        consumed.add(path)
    if len(consumed) != 94:
        return frozenset()
    return frozenset(consumed)


def _work054_wp002_frontmatter_value(raw: bytes, key: str) -> str | None:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return None
    if not lines or lines[0] != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    matches: list[str] = []
    prefix = f"{key}:"
    for line in lines[1:end]:
        if not line.startswith(prefix):
            continue
        value = line[len(prefix) :].strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {'"', "'"}
        ):
            value = value[1:-1]
        matches.append(value)
    return matches[0] if len(matches) == 1 else None


def _work054_wp002_migration_rows(raw: bytes) -> tuple[dict[str, object], ...]:
    """Load only the complete, independently pinned MIG-0002 document."""

    try:
        loaded = parse_pinned_migration_control(
            WORK054_WP002_MIGRATION_PATH.as_posix(), raw
        )
    except ArchiveContractError as exc:
        raise InvocationError("WORK-054 WP-002 migration document differs") from exc
    if not all(
        isinstance(row, dict) for row in loaded
    ):
        raise InvocationError("WORK-054 WP-002 migration ledger is not a row list")
    return tuple(loaded)


def _work054_wp002_render_migration_rows(
    raw: bytes, rows: Sequence[Mapping[str, object]]
) -> bytes:
    text = raw.decode("utf-8")
    matches = tuple(WORK054_WP002_LEDGER_PATTERN.finditer(text))
    if len(matches) != 1:
        raise InvocationError("WORK-054 WP-002 migration ledger is ambiguous")
    rendered = json.dumps(list(rows), ensure_ascii=False, indent=2)
    start, end = matches[0].span("ledger")
    return (text[:start] + rendered + text[end:]).encode("utf-8")


def _work054_wp002_artifact_id(path: PurePosixPath) -> str | None:
    requirement = WORK054_WP002_REQUIREMENT_PATTERN.fullmatch(path.as_posix())
    if requirement is not None:
        return f"PRD-0{requirement.group('id')}"
    specification = WORK054_WP002_SPEC_PATTERN.fullmatch(path.as_posix())
    if specification is None:
        return None
    prefixes = {
        "spec": "SPEC",
        "plan": "PLAN",
        "tasks": "TASK",
        "agent-design": "AGENT-DESIGN",
    }
    return f"{prefixes[specification.group('name')]}-0{specification.group('id')}"


def _work054_wp002_moved_paths(
    source_blobs: Mapping[PurePosixPath, str],
) -> dict[PurePosixPath, PurePosixPath]:
    result: dict[PurePosixPath, PurePosixPath] = {}
    requirement_count = 0
    specification_count = 0
    for path in source_blobs:
        raw_path = path.as_posix()
        requirement = WORK054_WP002_REQUIREMENT_PATTERN.fullmatch(raw_path)
        if requirement is not None:
            result[path] = PurePosixPath(
                "docs/01.requirements/"
                f"0{requirement.group('id')}{requirement.group('tail')}"
            )
            requirement_count += 1
            continue
        specification = WORK054_WP002_SPEC_PATTERN.fullmatch(raw_path)
        if specification is not None:
            result[path] = PurePosixPath(
                "docs/03.specs/"
                f"0{specification.group('id')}{specification.group('tail')}/"
                f"{specification.group('name')}.md"
            )
            specification_count += 1
    if (requirement_count, specification_count, len(result)) != (8, 133, 141):
        return {}
    return result


def _work054_wp002_expected_rows(
    root: Path,
    source_blobs: Mapping[PurePosixPath, str],
) -> tuple[dict[str, object], ...]:
    moved = _work054_wp002_moved_paths(source_blobs)
    if len(moved) != 141:
        return ()
    expected: list[dict[str, object]] = []
    dispositions: dict[str, tuple[str, str | None, str | None, str | None, str]] = {
        legacy.as_posix(): (
            "moved",
            stable.as_posix(),
            _work054_wp002_artifact_id(legacy),
            None,
            WORK054_WP002_MOVE_REASON,
        )
        for legacy, stable in moved.items()
    }
    dispositions.update(
        {
            legacy: (
                "replaced",
                None,
                None,
                replacement,
                WORK054_WP002_STAGE04_REASON,
            )
            for legacy, replacement in WORK054_WP002_STAGE04_REPLACEMENTS.items()
        }
    )
    dispositions.update(
        {
            legacy: (
                "merged",
                None,
                None,
                replacement,
                (
                    WORK054_WP002_STAGE00_MERGE_REASON
                    if legacy.startswith("docs/00.agent-governance/")
                    else (
                        WORK054_WP002_LIFECYCLE_MERGE_REASON
                        if replacement.endswith("document-lifecycle.md")
                        else WORK054_WP002_CONTRACT_MERGE_REASON
                    )
                ),
            )
            for legacy, replacement in WORK054_WP002_GOVERNANCE_MERGES.items()
        }
    )
    if len(dispositions) != 154:
        return ()
    for legacy_path in sorted(dispositions):
        path = PurePosixPath(legacy_path)
        source_oid = source_blobs.get(path)
        if source_oid is None:
            return ()
        try:
            source = _blob_bytes(root, source_oid)
        except (InvocationError, OSError):
            return ()
        action, stable_path, artifact_id, replacement, reason = dispositions[
            legacy_path
        ]
        expected.append(
            {
                "legacy_path": legacy_path,
                "stable_path": stable_path,
                "artifact_id": artifact_id,
                "action": action,
                "replacement": replacement,
                "source_commit": WORK054_WP002_SOURCE_COMMIT,
                "source_blob": source_oid,
                "content_sha256": hashlib.sha256(source).hexdigest(),
                "reason": reason,
            }
        )
    return tuple(expected)


def _work054_wp002_standalone_lineage_matches(
    base_registry_raw: Mapping[str, object],
    proposed_registry_raw: Mapping[str, object],
) -> bool:
    def selected(registry: Mapping[str, object]) -> tuple[Mapping[str, object], ...]:
        executions = registry.get("standaloneExecutions")
        if not isinstance(executions, list):
            return ()
        return tuple(
            item
            for item in executions
            if isinstance(item, Mapping) and item.get("spec") == "0054"
        )

    base = selected(base_registry_raw)
    proposed = selected(proposed_registry_raw)
    if base or len(proposed) != 1:
        return False
    relation = proposed[0]
    return relation == {
        "spec": "0054",
        "plan": WORK054_WP002_SPEC_PATHS[1].as_posix(),
        "task": WORK054_WP002_SPEC_PATHS[2].as_posix(),
        "state": "active",
        "reason": WORK054_WP002_STANDALONE_REASON,
        "decision": "0022",
        "approvalMode": "spec-body-record",
    }


def finite_work054_wp002_transition_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_registry: Registry,
    proposed_registry: Registry,
    base_registry_raw: Mapping[str, object],
    proposed_registry_raw: Mapping[str, object],
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    migration_bytes: bytes | None = None,
    decision_bytes: bytes | None = None,
) -> frozenset[PurePosixPath]:
    """Admit only the evidence-complete WORK-054 WP-002 topology transition."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != WORK054_WP002_BASE_COMMIT
        or not _work054_wp002_standalone_lineage_matches(
            base_registry_raw, proposed_registry_raw
        )
    ):
        return frozenset()
    try:
        source_blobs = _tree_blob_map(root, WORK054_WP002_SOURCE_COMMIT)
    except (InvocationError, OSError):
        return frozenset()
    expected_rows = _work054_wp002_expected_rows(root, source_blobs)
    if len(expected_rows) != 154:
        return frozenset()

    migration_oid = proposed_blobs.get(WORK054_WP002_MIGRATION_PATH)
    if (
        WORK054_WP002_MIGRATION_PATH in base_blobs
        or migration_oid is None
    ):
        return frozenset()
    try:
        if migration_bytes is not None:
            raw_migration = migration_bytes
        elif mode == "staged":
            raw_migration = read_staged_blob_bounded(
                root,
                WORK054_WP002_MIGRATION_PATH.as_posix(),
                max_bytes=MIGRATION_DOCUMENT_MAX_BYTES,
            )
        else:
            raw_migration = _blob_bytes(
                root, migration_oid, max_bytes=MIGRATION_DOCUMENT_MAX_BYTES
            )
        rows = _work054_wp002_migration_rows(raw_migration)
    except (ArchiveContractError, InvocationError, OSError):
        return frozenset()
    if _git_blob_oid(raw_migration) != migration_oid or rows != expected_rows:
        return frozenset()

    consumed: set[PurePosixPath] = {WORK054_WP002_MIGRATION_PATH}
    for row in rows:
        if tuple(row) != WORK054_WP002_LEDGER_KEYS:
            return frozenset()
        legacy = PurePosixPath(str(row["legacy_path"]))
        source_oid = str(row["source_blob"])
        if (
            base_blobs.get(legacy) != source_oid
            or source_blobs.get(legacy) != source_oid
            or legacy in proposed_blobs
        ):
            return frozenset()
        consumed.add(legacy)
        if row["action"] == "moved":
            stable = PurePosixPath(str(row["stable_path"]))
            target_oid = proposed_blobs.get(stable)
            if stable in base_blobs or target_oid is None:
                return frozenset()
            try:
                base_text = _blob_text(root, source_oid, legacy)
                proposed_text = _blob_text(root, target_oid, stable)
                target_bytes = _blob_bytes(root, target_oid)
                base_document = (
                    None
                    if base_text is None
                    else document_from_text(base_registry, legacy, base_text)
                )
                proposed_document = (
                    None
                    if proposed_text is None
                    else document_from_text(proposed_registry, stable, proposed_text)
                )
            except (DocumentContractError, InvocationError, OSError):
                return frozenset()
            if (
                base_document is None
                or proposed_document is None
                or base_document.profile_id != proposed_document.profile_id
                or base_document.status != proposed_document.status
                or _work054_wp002_frontmatter_value(target_bytes, "artifact_id")
                != row["artifact_id"]
            ):
                return frozenset()
            consumed.add(stable)
        else:
            replacement = PurePosixPath(str(row["replacement"]))
            if replacement not in proposed_blobs:
                return frozenset()
            if replacement not in base_blobs:
                consumed.add(replacement)

    expected_spec_states = (
        ("sdlc/spec", "draft", "active", "SPEC-0054"),
        ("sdlc/plan", "active", "active", "PLAN-0054"),
        ("sdlc/task", "active", "active", "TASK-0054"),
    )
    for path, (profile_id, base_state, proposed_state, artifact_id) in zip(
        WORK054_WP002_SPEC_PATHS, expected_spec_states, strict=True
    ):
        base_oid = base_blobs.get(path)
        proposed_oid = proposed_blobs.get(path)
        if base_oid is None or proposed_oid is None:
            return frozenset()
        try:
            base_text = _blob_text(root, base_oid, path)
            proposed_text = _blob_text(root, proposed_oid, path)
            proposed_bytes = _blob_bytes(root, proposed_oid)
            base_document = (
                None
                if base_text is None
                else document_from_text(proposed_registry, path, base_text)
            )
            proposed_document = (
                None
                if proposed_text is None
                else document_from_text(proposed_registry, path, proposed_text)
            )
        except (DocumentContractError, InvocationError, OSError):
            return frozenset()
        if (
            base_document != LifecycleDocument(path, profile_id, base_state)
            or proposed_document != LifecycleDocument(path, profile_id, proposed_state)
            or _work054_wp002_frontmatter_value(proposed_bytes, "artifact_id")
            != artifact_id
        ):
            return frozenset()
    consumed.update(WORK054_WP002_SPEC_PATHS)

    decision_oid = proposed_blobs.get(WORK054_WP002_DECISION_PATH)
    if (
        WORK054_WP002_DECISION_PATH in base_blobs
        or decision_oid is None
    ):
        return frozenset()
    try:
        raw_decision = (
            decision_bytes
            if decision_bytes is not None
            else _blob_bytes(root, decision_oid)
        )
        decision_text = raw_decision.decode("utf-8")
        decision_document = document_from_text(
            proposed_registry,
            WORK054_WP002_DECISION_PATH,
            decision_text,
        )
    except (DocumentContractError, InvocationError, OSError, UnicodeDecodeError):
        return frozenset()
    required_decision_links = (
        "./0024-terminal-artifact-identity-and-archive-layout.md",
        "../../03.specs/0052-document-taxonomy-consolidation/spec.md",
        (
            "../../03.specs/0054-sdlc-document-and-agent-governance-"
            "consolidation/spec.md"
        ),
    )
    if (
        _git_blob_oid(raw_decision) != decision_oid
        or hashlib.sha256(raw_decision).hexdigest()
        != WORK054_WP002_DECISION_SHA256
        or decision_document
        != LifecycleDocument(
            WORK054_WP002_DECISION_PATH,
            "sdlc/adr",
            "accepted",
        )
        or _work054_wp002_frontmatter_value(raw_decision, "artifact_id")
        != "ADR-0025"
        or any(decision_text.count(link) < 1 for link in required_decision_links)
    ):
        return frozenset()
    consumed.add(WORK054_WP002_DECISION_PATH)
    return frozenset(consumed) if len(consumed) == 303 else frozenset()


def finite_work054_wp003_agent_governance_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only the exact WORK-054 WP-003 legacy owner retirements."""

    if mode not in {"staged", "ci"} or base_commit != WORK054_WP003_BASE_COMMIT:
        return frozenset()
    migration_oid = proposed_blobs.get(WORK054_WP003_MIGRATION_PATH)
    if (
        WORK054_WP003_MIGRATION_PATH in base_blobs
        or migration_oid is None
    ):
        return frozenset()
    try:
        migration_bytes = _blob_bytes(root, migration_oid)
        migration_text = migration_bytes.decode("utf-8")
    except (InvocationError, OSError, UnicodeDecodeError):
        return frozenset()
    if hashlib.sha256(migration_bytes).hexdigest() != WORK054_WP003_MIGRATION_SHA256:
        return frozenset()
    marker = "<!-- archive-migration-ledger:v1 format=json -->\n\n```json\n"
    if migration_text.count(marker) != 1:
        return frozenset()
    _prefix, remainder = migration_text.split(marker, 1)
    if remainder.count("\n```") != 1:
        return frozenset()
    raw_rows, suffix = remainder.split("\n```", 1)
    if not suffix.startswith("\n\n## Recovery\n"):
        return frozenset()
    try:
        rows = json.loads(raw_rows)
    except json.JSONDecodeError:
        return frozenset()
    if (
        not isinstance(rows, list)
        or len(rows) != len(WORK054_WP003_OWNER_RETIREMENTS)
    ):
        return frozenset()
    consumed: set[PurePosixPath] = {WORK054_WP003_MIGRATION_PATH}
    for row, expected in zip(rows, WORK054_WP003_OWNER_RETIREMENTS, strict=True):
        if not isinstance(row, Mapping) or tuple(row) != WORK054_WP003_LEDGER_KEYS:
            return frozenset()
        for key, value in expected.items():
            if row.get(key) != value:
                return frozenset()
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            return frozenset()
        legacy = PurePosixPath(str(row["legacy_path"]))
        replacement = PurePosixPath(str(row["replacement"]))
        if (
            base_blobs.get(legacy) != row["source_blob"]
            or legacy in proposed_blobs
            or replacement not in proposed_blobs
        ):
            return frozenset()
        consumed.add(legacy)
    return frozenset(consumed) if len(consumed) == 4 else frozenset()


def finite_work054_wp004a_authority_paths(
    *,
    mode: str,
    base_commit: str,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit the atomic WP-004A activation of the two current human owners."""

    if mode not in {"staged", "ci"} or base_commit != WORK054_WP004A_BASE_COMMIT:
        return frozenset()
    if any(
        proposed_blobs.get(path) is None
        or proposed_blobs.get(path) == base_blobs.get(path)
        for path in WORK054_WP004A_REQUIRED_CHANGED_PATHS
    ):
        return frozenset()
    expected = {
        path: LifecycleDocument(path, "governance/reference", "active")
        for path in WORK054_WP004A_OWNER_PATHS
    }
    if any(
        path in base_documents
        or path in base_blobs
        or proposed_documents.get(path) != document
        for path, document in expected.items()
    ):
        return frozenset()
    return frozenset(WORK054_WP004A_OWNER_PATHS)


def finite_archive_cutover_paths(
    *,
    mode: str,
    base_commit: str,
    base_registry_oid: str,
    proposed_registry_oid: str,
    base_registry: Mapping[str, object],
    proposed_registry: Mapping[str, object],
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> frozenset[PurePosixPath]:
    """Return only the exact finite ARWB-003 events admitted for consumption."""

    if (
        mode not in {"staged", "ci"}
        or base_commit != CUTOVER_BASE_COMMIT
        or base_registry_oid != BASE_REGISTRY_BLOB_OID
        or proposed_registry_oid != PROPOSED_REGISTRY_BLOB_OID
    ):
        return frozenset()
    if (
        base_registry.get("schemaVersion") != BASE_REGISTRY_VERSION
        or base_registry.get("$id") != BASE_REGISTRY_ID
        or proposed_registry.get("schemaVersion") != PROPOSED_REGISTRY_VERSION
        or proposed_registry.get("$id") != PROPOSED_REGISTRY_ID
    ):
        return frozenset()

    base_profile_ids = _registry_profile_ids(base_registry)
    proposed_profile_ids = _registry_profile_ids(proposed_registry)
    if (
        not {LEGACY_ARCHIVE_PROFILE, LEGACY_ARCHIVE_TEMPLATE_PROFILE}
        <= base_profile_ids
        or {ARCHIVE_PROFILE, ARCHIVE_TEMPLATE_PROFILE} & base_profile_ids
        or not {ARCHIVE_PROFILE, ARCHIVE_TEMPLATE_PROFILE} <= proposed_profile_ids
        or {
            LEGACY_ARCHIVE_PROFILE,
            LEGACY_ARCHIVE_TEMPLATE_PROFILE,
        }
        & proposed_profile_ids
    ):
        return frozenset()

    expected_records = frozenset(PurePosixPath(path) for path in EXPECTED_ARCHIVE_PATHS)
    common_paths = set(base_documents) & set(proposed_documents)
    profile_changes = frozenset(
        path
        for path in common_paths
        if base_documents[path].profile_id != proposed_documents[path].profile_id
    )
    if profile_changes != expected_records:
        return frozenset()
    for path in expected_records:
        base = base_documents[path]
        proposed = proposed_documents[path]
        if (
            base.profile_id != LEGACY_ARCHIVE_PROFILE
            or base.status != "archived"
            or base.state_issue is not None
            or proposed.profile_id != ARCHIVE_PROFILE
            or proposed.status != "archived"
            or proposed.state_issue is not None
        ):
            return frozenset()

    legacy_template = PurePosixPath(LEGACY_ARCHIVE_TEMPLATE)
    archive_template = PurePosixPath(ARCHIVE_TEMPLATE)
    if (
        base_documents.get(legacy_template)
        != LifecycleDocument(
            legacy_template,
            LEGACY_ARCHIVE_TEMPLATE_PROFILE,
            None,
        )
        or legacy_template in proposed_documents
        or proposed_documents.get(archive_template)
        != LifecycleDocument(
            archive_template,
            ARCHIVE_TEMPLATE_PROFILE,
            None,
        )
        or archive_template in base_documents
    ):
        return frozenset()

    if (
        frozenset(
            path
            for path, document in base_documents.items()
            if document.profile_id == LEGACY_ARCHIVE_PROFILE
        )
        != expected_records
        or frozenset(
            path
            for path, document in proposed_documents.items()
            if document.profile_id == ARCHIVE_PROFILE
        )
        != expected_records
        or frozenset(
            path
            for path, document in base_documents.items()
            if document.profile_id == LEGACY_ARCHIVE_TEMPLATE_PROFILE
        )
        != {legacy_template}
        or frozenset(
            path
            for path, document in proposed_documents.items()
            if document.profile_id == ARCHIVE_TEMPLATE_PROFILE
        )
        != {archive_template}
    ):
        return frozenset()
    return expected_records | {legacy_template, archive_template}


def _agent_projection_path(role_id: str, surface_id: str) -> str:
    if surface_id == "local":
        return f".agents/agents/{role_id}.md"
    if surface_id == "claude":
        return f".claude/agents/{role_id}.md"
    if surface_id == "codex":
        return f".codex/agents/{role_id}.toml"
    if surface_id == "gemini":
        return f".gemini/agents/{role_id}.md"
    raise ValueError(f"unknown agent surface: {surface_id}")


def _agent_inventory_matches(
    inventory: object,
    *,
    state: str,
    count_prefix: str,
    role_count: int,
    surface_count: int,
    projection_count: int,
) -> bool:
    if not isinstance(inventory, Mapping):
        return False
    if count_prefix == "":
        count_keys = ("roleCount", "surfaceCount", "adapterCount")
    elif count_prefix == "expected":
        count_keys = (
            "expectedRoleCount",
            "expectedSurfaceCount",
            "expectedProjectionCount",
        )
    else:
        return False
    role_key, surface_key, projection_key = count_keys
    return (
        inventory.get("state") == state
        and inventory.get(role_key) == role_count
        and inventory.get(surface_key) == surface_count
        and inventory.get(projection_key) == projection_count
    )


def _harness_projection_set(inventory: object) -> set[tuple[str, str, str, str]]:
    if not isinstance(inventory, Mapping):
        return set()
    projections = inventory.get("projections")
    if not isinstance(projections, list):
        return set()
    result: set[tuple[str, str, str, str]] = set()
    for projection in projections:
        if not isinstance(projection, Mapping):
            return set()
        values = (
            projection.get("roleId"),
            projection.get("surfaceId"),
            projection.get("path"),
            projection.get("admissionState"),
        )
        if not all(isinstance(value, str) for value in values):
            return set()
        if values in result:
            return set()
        result.add(values)  # type: ignore[arg-type]
    return result


def _agent_evidence_matches(
    evidence: object,
    *,
    proposed: bool,
) -> bool:
    deferred_classes = (
        AGENT_ROSTER_DEFERRED_CLASSES
        if proposed
        else AGENT_ROSTER_BASE_DEFERRED_CLASSES
    )
    expected: dict[str, object] = {
        "class": "repo-static",
        "claimBoundary": (
            "repository-static-role-and-adapter-projection-only"
            if proposed
            else "prepared-policy-and-candidate-contract-only"
        ),
        "admissionVerdict": "DEFER",
        "deferredClasses": list(deferred_classes),
        "deferredClassStates": {
            evidence_class: "DEFER"
            for evidence_class in deferred_classes
        },
    }
    if proposed:
        expected["projectionAuthorization"] = {
            "authorized": True,
            "scope": "repository-static-role-and-adapter-projection-only",
            "excludedEvidenceClasses": list(deferred_classes),
        }
    else:
        expected["promotionAuthorized"] = False
    return isinstance(evidence, Mapping) and evidence == expected


def _agent_evaluation_gate_matches(
    gate: object,
    *,
    baseline_state: str,
) -> bool:
    return isinstance(gate, Mapping) and gate == {
        "classes": list(AGENT_ROSTER_EVALUATION_CLASSES),
        "baselineState": baseline_state,
        "sameCorpusAndGraderRequired": True,
        "independentAdjudication": {
            "required": True,
            "selfAdjudicationProhibited": True,
            "adjudicatorOwner": "independent-reviewer",
            "thresholdOrder": ["quality", "safety", "cost", "latency"],
            "criticalMissBlocksPromotion": True,
        },
    }


def _agent_contracts_admit_cutover(
    base_admission: object,
    proposed_admission: object,
    base_harness: object,
    proposed_harness: object,
) -> bool:
    if not all(
        isinstance(contract, Mapping)
        for contract in (
            base_admission,
            proposed_admission,
            base_harness,
            proposed_harness,
        )
    ):
        return False
    assert isinstance(base_admission, Mapping)
    assert isinstance(proposed_admission, Mapping)
    assert isinstance(base_harness, Mapping)
    assert isinstance(proposed_harness, Mapping)

    if (
        base_admission.get("contractId")
        != "hy-home.k8s/agent-roster-admission"
        or proposed_admission.get("contractId")
        != "hy-home.k8s/agent-roster-admission"
        or base_admission.get("contractVersion") != "1.0.0"
        or proposed_admission.get("contractVersion") != "1.0.0"
        or base_admission.get("state") != "contract-only"
        or proposed_admission.get("state") != "repository-static-projected"
        or not _agent_evidence_matches(
            base_admission.get("evidence"),
            proposed=False,
        )
        or not _agent_evidence_matches(
            proposed_admission.get("evidence"),
            proposed=True,
        )
    ):
        return False
    if not _agent_inventory_matches(
        base_admission.get("currentInventory"),
        state="current",
        count_prefix="",
        role_count=10,
        surface_count=3,
        projection_count=30,
    ) or not _agent_inventory_matches(
        proposed_admission.get("currentInventory"),
        state="current",
        count_prefix="",
        role_count=12,
        surface_count=4,
        projection_count=48,
    ):
        return False

    target = proposed_admission.get("targetInventory")
    if not isinstance(target, Mapping) or (
        target.get("state"),
        target.get("roleCount"),
        target.get("surfaceCount"),
        target.get("adapterCount"),
        tuple(target.get("roleIds", ())),
        tuple(target.get("surfaceIds", ())),
    ) != (
        "achieved",
        12,
        4,
        48,
        AGENT_ROSTER_ROLE_IDS,
        AGENT_ROSTER_SURFACE_IDS,
    ):
        return False

    base_candidates = base_admission.get("candidates")
    if not isinstance(base_candidates, list) or len(base_candidates) != 2:
        return False
    if {
        candidate.get("roleId")
        for candidate in base_candidates
        if isinstance(candidate, Mapping)
    } != set(AGENT_ROSTER_CANDIDATE_IDS):
        return False
    for candidate in base_candidates:
        if not isinstance(candidate, Mapping) or not _agent_evaluation_gate_matches(
            candidate.get("evaluationGate"),
            baseline_state="required-before-promotion",
        ):
            return False

    candidates = proposed_admission.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 2:
        return False
    expected_candidates = set(AGENT_ROSTER_CANDIDATE_IDS)
    if {
        candidate.get("roleId")
        for candidate in candidates
        if isinstance(candidate, Mapping)
    } != expected_candidates:
        return False
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            return False
        role_id = candidate.get("roleId")
        if (
            role_id not in expected_candidates
            or candidate.get("decision") != "repository-static-projected"
            or candidate.get("authority")
            != "repository-static-role-and-adapter-projection-only"
            or not _agent_evaluation_gate_matches(
                candidate.get("evaluationGate"),
                baseline_state=(
                    "deferred-to-area-003-before-runtime-activation"
                ),
            )
        ):
            return False
        plan = candidate.get("surfacePlan")
        if not isinstance(plan, list) or len(plan) != 4:
            return False
        actual_plan = {
            (
                item.get("surfaceId"),
                item.get("state"),
                item.get("adapterPath"),
                item.get("leastPrivilege"),
                item.get("providerNativeMetadataRequired"),
            )
            for item in plan
            if isinstance(item, Mapping)
        }
        expected_plan = {
            (
                surface_id,
                "current",
                _agent_projection_path(str(role_id), surface_id),
                True,
                True,
            )
            for surface_id in AGENT_ROSTER_SURFACE_IDS
        }
        if actual_plan != expected_plan:
            return False

    if (
        base_harness.get("contractId") != "hy-home.k8s/agent-harness"
        or proposed_harness.get("contractId") != "hy-home.k8s/agent-harness"
        or base_harness.get("contractVersion") != "1.0.0"
        or proposed_harness.get("contractVersion") != "1.0.0"
        or not _agent_inventory_matches(
            base_harness.get("currentInventory"),
            state="current",
            count_prefix="expected",
            role_count=10,
            surface_count=3,
            projection_count=30,
        )
        or not _agent_inventory_matches(
            proposed_harness.get("currentInventory"),
            state="current",
            count_prefix="expected",
            role_count=12,
            surface_count=4,
            projection_count=48,
        )
        or not _agent_inventory_matches(
            proposed_harness.get("targetInventory"),
            state="achieved",
            count_prefix="expected",
            role_count=12,
            surface_count=4,
            projection_count=48,
        )
    ):
        return False

    current = proposed_harness.get("currentInventory")
    achieved = proposed_harness.get("targetInventory")
    for inventory, state in ((current, "current"), (achieved, "achieved")):
        if not isinstance(inventory, Mapping) or (
            inventory.get("state"),
            tuple(inventory.get("roleIds", ())),
            tuple(inventory.get("surfaceIds", ())),
        ) != (state, AGENT_ROSTER_ROLE_IDS, AGENT_ROSTER_SURFACE_IDS):
            return False
    expected_projections = {
        (
            role_id,
            surface_id,
            _agent_projection_path(role_id, surface_id),
            "current",
        )
        for role_id in AGENT_ROSTER_ROLE_IDS
        for surface_id in AGENT_ROSTER_SURFACE_IDS
    }
    return (
        _harness_projection_set(current) == expected_projections
        and _harness_projection_set(achieved) == expected_projections
    )


def finite_agent_roster_cutover_paths(
    *,
    mode: str,
    base_commit: str,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_admission: object,
    proposed_admission: object,
    base_harness: object,
    proposed_harness: object,
) -> frozenset[PurePosixPath]:
    """Admit only the exact AREA-002 repository-projection creation set."""

    expected = frozenset(AGENT_ROSTER_CUTOVER_PATHS)
    if (
        mode not in {"staged", "ci"}
        or base_commit != AGENT_ROSTER_ADMISSION_BASE_COMMIT
        or not _agent_contracts_admit_cutover(
            base_admission,
            proposed_admission,
            base_harness,
            proposed_harness,
        )
        or expected & set(base_documents)
    ):
        return frozenset()
    created_snapshot_paths = {
        path
        for path, document in proposed_documents.items()
        if path not in base_documents
        and document.profile_id
        in {"exception/local-agent-asset", "exception/provider-native-metadata"}
    }
    if created_snapshot_paths != expected:
        return frozenset()
    for path in expected:
        expected_profile = (
            "exception/local-agent-asset"
            if path.parts[0] == ".agents"
            else "exception/provider-native-metadata"
        )
        if proposed_documents.get(path) != LifecycleDocument(
            path,
            expected_profile,
            None,
        ):
            return frozenset()
    return expected


def _agent_roster_cutover_fixture_inputs(
    mutation: str,
) -> dict[str, object]:
    def admission_inventory(
        state: str,
        role_count: int,
        surface_count: int,
        adapter_count: int,
    ) -> dict[str, object]:
        return {
            "state": state,
            "roleCount": role_count,
            "surfaceCount": surface_count,
            "adapterCount": adapter_count,
        }

    def harness_inventory(
        state: str,
        role_count: int,
        surface_count: int,
        projection_count: int,
    ) -> dict[str, object]:
        return {
            "state": state,
            "expectedRoleCount": role_count,
            "expectedSurfaceCount": surface_count,
            "expectedProjectionCount": projection_count,
        }

    def evaluation_gate(baseline_state: str) -> dict[str, object]:
        return {
            "classes": list(AGENT_ROSTER_EVALUATION_CLASSES),
            "baselineState": baseline_state,
            "sameCorpusAndGraderRequired": True,
            "independentAdjudication": {
                "required": True,
                "selfAdjudicationProhibited": True,
                "adjudicatorOwner": "independent-reviewer",
                "thresholdOrder": ["quality", "safety", "cost", "latency"],
                "criticalMissBlocksPromotion": True,
            },
        }

    base_documents: dict[PurePosixPath, LifecycleDocument] = {}
    proposed_documents = {
        path: LifecycleDocument(
            path,
            (
                "exception/local-agent-asset"
                if path.parts[0] == ".agents"
                else "exception/provider-native-metadata"
            ),
            None,
        )
        for path in AGENT_ROSTER_CUTOVER_PATHS
    }
    base_admission: dict[str, object] = {
        "contractId": "hy-home.k8s/agent-roster-admission",
        "contractVersion": "1.0.0",
        "state": "contract-only",
        "currentInventory": admission_inventory("current", 10, 3, 30),
        "evidence": {
            "class": "repo-static",
            "claimBoundary": "prepared-policy-and-candidate-contract-only",
            "admissionVerdict": "DEFER",
            "promotionAuthorized": False,
            "deferredClasses": list(AGENT_ROSTER_BASE_DEFERRED_CLASSES),
            "deferredClassStates": {
                evidence_class: "DEFER"
                for evidence_class in AGENT_ROSTER_BASE_DEFERRED_CLASSES
            },
        },
        "candidates": [
            {
                "roleId": role_id,
                "evaluationGate": evaluation_gate("required-before-promotion"),
            }
            for role_id in AGENT_ROSTER_CANDIDATE_IDS
        ],
    }
    proposed_admission: dict[str, object] = {
        "contractId": "hy-home.k8s/agent-roster-admission",
        "contractVersion": "1.0.0",
        "state": "repository-static-projected",
        "evidence": {
            "class": "repo-static",
            "claimBoundary": "repository-static-role-and-adapter-projection-only",
            "admissionVerdict": "DEFER",
            "projectionAuthorization": {
                "authorized": True,
                "scope": "repository-static-role-and-adapter-projection-only",
                "excludedEvidenceClasses": list(
                    AGENT_ROSTER_DEFERRED_CLASSES
                ),
            },
            "deferredClasses": list(AGENT_ROSTER_DEFERRED_CLASSES),
            "deferredClassStates": {
                evidence_class: "DEFER"
                for evidence_class in AGENT_ROSTER_DEFERRED_CLASSES
            },
        },
        "currentInventory": admission_inventory("current", 12, 4, 48),
        "targetInventory": {
            **admission_inventory("achieved", 12, 4, 48),
            "roleIds": list(AGENT_ROSTER_ROLE_IDS),
            "surfaceIds": list(AGENT_ROSTER_SURFACE_IDS),
        },
        "candidates": [
            {
                "roleId": role_id,
                "decision": "repository-static-projected",
                "authority": "repository-static-role-and-adapter-projection-only",
                "surfacePlan": [
                    {
                        "surfaceId": surface_id,
                        "state": "current",
                        "adapterPath": _agent_projection_path(
                            role_id,
                            surface_id,
                        ),
                        "leastPrivilege": True,
                        "providerNativeMetadataRequired": True,
                    }
                    for surface_id in AGENT_ROSTER_SURFACE_IDS
                ],
                "evaluationGate": evaluation_gate(
                    "deferred-to-area-003-before-runtime-activation"
                ),
            }
            for role_id in AGENT_ROSTER_CANDIDATE_IDS
        ],
    }
    projections = [
        {
            "roleId": role_id,
            "surfaceId": surface_id,
            "path": _agent_projection_path(role_id, surface_id),
            "admissionState": "current",
        }
        for role_id in AGENT_ROSTER_ROLE_IDS
        for surface_id in AGENT_ROSTER_SURFACE_IDS
    ]
    base_harness: dict[str, object] = {
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": "1.0.0",
        "currentInventory": harness_inventory("current", 10, 3, 30),
    }
    proposed_harness: dict[str, object] = {
        "contractId": "hy-home.k8s/agent-harness",
        "contractVersion": "1.0.0",
        "currentInventory": {
            **harness_inventory("current", 12, 4, 48),
            "roleIds": list(AGENT_ROSTER_ROLE_IDS),
            "surfaceIds": list(AGENT_ROSTER_SURFACE_IDS),
            "projections": copy.deepcopy(projections),
        },
        "targetInventory": {
            **harness_inventory("achieved", 12, 4, 48),
            "roleIds": list(AGENT_ROSTER_ROLE_IDS),
            "surfaceIds": list(AGENT_ROSTER_SURFACE_IDS),
            "projections": projections,
        },
    }
    mode = "staged"
    base_commit = AGENT_ROSTER_ADMISSION_BASE_COMMIT

    if mutation == "wrong-mode":
        mode = "explicit-ref"
    elif mutation == "wrong-base":
        base_commit = "0" * 40
    elif mutation == "missing-path":
        proposed_documents.pop(AGENT_ROSTER_CUTOVER_PATHS[0])
    elif mutation == "extra-path":
        extra = PurePosixPath(".agents/agents/unrelated.md")
        proposed_documents[extra] = LifecycleDocument(
            extra,
            "exception/local-agent-asset",
            None,
        )
    elif mutation == "wrong-profile":
        path = AGENT_ROSTER_CUTOVER_PATHS[0]
        proposed_documents[path] = LifecycleDocument(path, "sdlc/spec", "active")
    elif mutation == "base-already-contains-path":
        path = AGENT_ROSTER_CUTOVER_PATHS[0]
        base_documents[path] = proposed_documents[path]
    elif mutation == "wrong-admission-state":
        proposed_admission["state"] = "contract-only"
    elif mutation == "wrong-admission-inventory":
        current = proposed_admission["currentInventory"]
        assert isinstance(current, dict)
        current["adapterCount"] = 47
    elif mutation in {
        "wrong-evidence-class",
        "wrong-claim-boundary",
        "admission-verdict-preclaim",
        "promotion-authorization-preclaim",
        "runtime-preclaim",
        "missing-provider-deferred-state",
        "missing-deferred-evidence",
        "missing-live-deferred-state",
    }:
        evidence = proposed_admission["evidence"]
        assert isinstance(evidence, dict)
        if mutation == "wrong-evidence-class":
            evidence["class"] = "runtime"
        elif mutation == "wrong-claim-boundary":
            evidence["claimBoundary"] = "repository-static-and-runtime"
        elif mutation == "admission-verdict-preclaim":
            evidence["admissionVerdict"] = "PASS"
        elif mutation == "promotion-authorization-preclaim":
            evidence["promotionAuthorization"] = evidence.pop(
                "projectionAuthorization"
            )
        elif mutation == "missing-deferred-evidence":
            evidence.pop("deferredClassStates")
        else:
            states = evidence["deferredClassStates"]
            assert isinstance(states, dict)
            if mutation == "runtime-preclaim":
                states["runtime"] = "PASS"
            elif mutation == "missing-provider-deferred-state":
                states.pop("provider-discovery")
            else:
                states.pop("live")
    elif mutation == "wrong-candidate-surface":
        candidates = proposed_admission["candidates"]
        assert isinstance(candidates, list)
        candidate = candidates[0]
        assert isinstance(candidate, dict)
        plan = candidate["surfacePlan"]
        assert isinstance(plan, list)
        surface = plan[0]
        assert isinstance(surface, dict)
        surface["adapterPath"] = ".agents/agents/wrong.md"
    elif mutation in {
        "candidate-admission-preclaim",
        "candidate-admission-authority-preclaim",
    }:
        candidates = proposed_admission["candidates"]
        assert isinstance(candidates, list)
        candidate = candidates[0]
        assert isinstance(candidate, dict)
        if mutation == "candidate-admission-preclaim":
            candidate["decision"] = "repository-static-admitted"
        else:
            candidate[
                "authority"
            ] = "repository-static-role-and-adapter-inventory-only"
    elif mutation in {
        "wrong-evaluation-baseline",
        "wrong-independent-adjudication",
    }:
        candidates = proposed_admission["candidates"]
        assert isinstance(candidates, list)
        candidate = candidates[0]
        assert isinstance(candidate, dict)
        gate = candidate["evaluationGate"]
        assert isinstance(gate, dict)
        if mutation == "wrong-evaluation-baseline":
            gate["baselineState"] = "runtime-activated"
        else:
            adjudication = gate["independentAdjudication"]
            assert isinstance(adjudication, dict)
            adjudication["required"] = False
    elif mutation == "wrong-harness-inventory":
        target = proposed_harness["targetInventory"]
        assert isinstance(target, dict)
        target["expectedProjectionCount"] = 47
    elif mutation == "wrong-harness-projection":
        current = proposed_harness["currentInventory"]
        assert isinstance(current, dict)
        current_projections = current["projections"]
        assert isinstance(current_projections, list)
        current_projections.pop()
    elif mutation != "exact":
        raise ValueError(f"unknown agent roster cutover mutation: {mutation}")

    return {
        "mode": mode,
        "base_commit": base_commit,
        "base_documents": base_documents,
        "proposed_documents": proposed_documents,
        "base_admission": base_admission,
        "proposed_admission": proposed_admission,
        "base_harness": base_harness,
        "proposed_harness": proposed_harness,
    }


def _archive_cutover_fixture_inputs(
    mode: str,
    mutation: str,
) -> dict[str, object]:
    expected_records = tuple(PurePosixPath(path) for path in EXPECTED_ARCHIVE_PATHS)
    legacy_template = PurePosixPath(LEGACY_ARCHIVE_TEMPLATE)
    archive_template = PurePosixPath(ARCHIVE_TEMPLATE)
    base_documents = {
        path: LifecycleDocument(path, LEGACY_ARCHIVE_PROFILE, "archived")
        for path in expected_records
    }
    proposed_documents = {
        path: LifecycleDocument(path, ARCHIVE_PROFILE, "archived")
        for path in expected_records
    }
    base_documents[legacy_template] = LifecycleDocument(
        legacy_template,
        LEGACY_ARCHIVE_TEMPLATE_PROFILE,
        None,
    )
    proposed_documents[archive_template] = LifecycleDocument(
        archive_template,
        ARCHIVE_TEMPLATE_PROFILE,
        None,
    )
    base_registry: dict[str, object] = {
        "$id": BASE_REGISTRY_ID,
        "schemaVersion": BASE_REGISTRY_VERSION,
        "profiles": [
            {"id": LEGACY_ARCHIVE_PROFILE},
            {"id": LEGACY_ARCHIVE_TEMPLATE_PROFILE},
        ],
    }
    proposed_registry: dict[str, object] = {
        "$id": PROPOSED_REGISTRY_ID,
        "schemaVersion": PROPOSED_REGISTRY_VERSION,
        "profiles": [
            {"id": ARCHIVE_PROFILE},
            {"id": ARCHIVE_TEMPLATE_PROFILE},
        ],
    }
    base_commit = CUTOVER_BASE_COMMIT
    base_registry_oid = BASE_REGISTRY_BLOB_OID
    proposed_registry_oid = PROPOSED_REGISTRY_BLOB_OID
    if mutation == "partial":
        proposed_documents.pop(expected_records[0])
    elif mutation == "extra":
        extra = PurePosixPath("docs/98.archive/03.specs/999-extra/spec.md")
        base_documents[extra] = LifecycleDocument(
            extra, LEGACY_ARCHIVE_PROFILE, "archived"
        )
        proposed_documents[extra] = LifecycleDocument(
            extra, ARCHIVE_PROFILE, "archived"
        )
    elif mutation == "wrong-base":
        base_commit = "0" * 40
    elif mutation == "wrong-base-registry-oid":
        base_registry_oid = "0" * 40
    elif mutation == "proposed-policy-drift":
        proposed_registry["unrelatedPolicy"] = {"mode": "changed"}
        proposed_registry_oid = "f" * 40
    elif mutation == "missing-template":
        proposed_documents.pop(archive_template)
    elif mutation == "wrong-registry-version":
        proposed_registry["schemaVersion"] = PROPOSED_REGISTRY_VERSION + 1
    elif mutation == "missing-registry-profile":
        proposed_registry["profiles"] = [{"id": ARCHIVE_PROFILE}]
    elif mutation == "unrelated-profile-change":
        unrelated = PurePosixPath("docs/03.specs/0999-unrelated/spec.md")
        base_documents[unrelated] = LifecycleDocument(unrelated, "sdlc/spec", "active")
        proposed_documents[unrelated] = LifecycleDocument(
            unrelated, "sdlc/guide", "active"
        )
    elif mutation != "exact":
        raise ValueError(f"unknown archive cutover fixture mutation: {mutation}")
    return {
        "mode": mode,
        "base_commit": base_commit,
        "base_registry_oid": base_registry_oid,
        "proposed_registry_oid": proposed_registry_oid,
        "base_registry": base_registry,
        "proposed_registry": proposed_registry,
        "base_documents": base_documents,
        "proposed_documents": proposed_documents,
    }


def _work054_wp002_transition_fixture_inputs(
    root: Path, mode: str, mutation: str
) -> dict[str, object]:
    base_blobs = dict(_tree_blob_map(root, WORK054_WP002_BASE_COMMIT))
    proposed_blobs = dict(_index_blob_map(root))
    production_registry = load_registry(root)
    base_registry_raw = dict(
        _registry_blob(
            root,
            _tree_blob_oid(root, WORK054_WP002_BASE_COMMIT, RETIRED_REGISTRY_PATH),
        )
    )
    proposed_registry_raw = dict(
        _registry_blob(root, _index_blob_oid(root, RETIRED_REGISTRY_PATH))
    )
    base_registry = _classification_registry(
        production_registry,
        base_registry_raw,
    )
    proposed_registry = _classification_registry(
        production_registry,
        proposed_registry_raw,
    )
    migration_oid = proposed_blobs.get(WORK054_WP002_MIGRATION_PATH)
    migration_bytes = (
        b"" if migration_oid is None else _blob_bytes(root, migration_oid)
    )
    decision_oid = proposed_blobs.get(WORK054_WP002_DECISION_PATH)
    decision_bytes = b"" if decision_oid is None else _blob_bytes(root, decision_oid)

    def loose_rows(raw: bytes) -> list[dict[str, object]]:
        text = raw.decode("utf-8")
        matches = tuple(WORK054_WP002_LEDGER_PATTERN.finditer(text))
        if len(matches) != 1:
            return []
        loaded = json.loads(
            matches[0].group("ledger"), object_pairs_hook=_unique_json_object
        )
        return loaded if isinstance(loaded, list) else []

    def update_migration(rows: Sequence[Mapping[str, object]]) -> None:
        nonlocal migration_bytes
        migration_bytes = _work054_wp002_render_migration_rows(
            migration_bytes, rows
        )
        proposed_blobs[WORK054_WP002_MIGRATION_PATH] = _git_blob_oid(
            migration_bytes
        )

    base_commit = WORK054_WP002_BASE_COMMIT
    if mutation == "wrong-base":
        base_commit = "0" * 40
    elif mutation == "missing-migration":
        proposed_blobs.pop(WORK054_WP002_MIGRATION_PATH, None)
    elif mutation in {
        "missing-ledger-row",
        "extra-ledger-row",
        "source-blob-drift",
        "source-digest-drift",
        "replacement-drift",
        "target-artifact-drift",
    }:
        rows = loose_rows(migration_bytes)
        if mutation == "missing-ledger-row" and rows:
            rows.pop(0)
        elif mutation == "extra-ledger-row" and rows:
            extra = dict(rows[0])
            extra["legacy_path"] = "docs/README.md"
            rows.append(extra)
        elif mutation == "source-blob-drift" and rows:
            rows[0]["source_blob"] = "0" * 40
        elif mutation == "source-digest-drift" and rows:
            rows[0]["content_sha256"] = "0" * 64
        elif mutation == "replacement-drift":
            merged = next(
                (row for row in rows if row.get("action") == "merged"), None
            )
            if merged is not None:
                merged["replacement"] = "docs/README.md"
        elif mutation == "target-artifact-drift":
            moved = next(
                (row for row in rows if row.get("action") == "moved"), None
            )
            if moved is not None:
                moved["artifact_id"] = "SPEC-9999"
        update_migration(rows)
    elif mutation == "standalone-lineage-drift":
        proposed_registry_raw["standaloneExecutions"] = [
            item
            for item in proposed_registry_raw.get("standaloneExecutions", [])
            if isinstance(item, Mapping) and item.get("spec") != "0054"
        ]
    elif mutation == "missing-spec-transition":
        proposed_blobs.pop(WORK054_WP002_SPEC_PATHS[0], None)
    elif mutation == "missing-decision":
        proposed_blobs.pop(WORK054_WP002_DECISION_PATH, None)
    elif mutation == "decision-blob-drift":
        decision_bytes += b"\n"
        proposed_blobs[WORK054_WP002_DECISION_PATH] = _git_blob_oid(decision_bytes)
    elif mutation != "exact":
        raise ValueError(f"unknown WORK-054 WP-002 mutation: {mutation}")
    return {
        "root": root,
        "mode": mode,
        "base_commit": base_commit,
        "base_registry": base_registry,
        "proposed_registry": proposed_registry,
        "base_registry_raw": base_registry_raw,
        "proposed_registry_raw": proposed_registry_raw,
        "base_blobs": base_blobs,
        "proposed_blobs": proposed_blobs,
        "migration_bytes": migration_bytes,
        "decision_bytes": decision_bytes,
    }


def _work105_form_cutover_fixture_inputs(
    root: Path,
    mode: str,
    mutation: str,
) -> dict[str, object]:
    base_registry = dict(_registry_blob(root, WORK105_BASE_REGISTRY_BLOB_OID))
    proposed_registry = dict(
        _registry_blob(root, WORK105_PROPOSED_REGISTRY_BLOB_OID)
    )
    base_documents: dict[PurePosixPath, LifecycleDocument] = {}
    proposed_documents: dict[PurePosixPath, LifecycleDocument] = {}
    for token, status in WORK105_AD_CUTOVER:
        old_path = PurePosixPath(
            f"docs/02.architecture/requirements/{token}.md"
        )
        new_path = PurePosixPath(
            f"docs/02.architecture/descriptions/ad-{token}.md"
        )
        base_documents[old_path] = LifecycleDocument(old_path, "sdlc/ard", status)
        proposed_documents[new_path] = LifecycleDocument(new_path, "sdlc/ad", status)

    exact_forms = (
        (
            PurePosixPath("docs/02.architecture/requirements/README.md"),
            "readme/collection-index",
            base_documents,
        ),
        (
            PurePosixPath("docs/02.architecture/descriptions/README.md"),
            "readme/collection-index",
            proposed_documents,
        ),
        (
            PurePosixPath(
                "docs/99.templates/templates/sdlc/architecture/ard.template.md"
            ),
            "template/sdlc/ard",
            base_documents,
        ),
        (
            PurePosixPath(
                "docs/99.templates/templates/sdlc/architecture/ad.template.md"
            ),
            "template/sdlc/ad",
            proposed_documents,
        ),
        (
            PurePosixPath(
                "docs/99.templates/templates/sdlc/specs/api-spec.template.md"
            ),
            "template/sdlc/api-spec",
            base_documents,
        ),
        (
            PurePosixPath(
                "docs/99.templates/templates/sdlc/requirements/interface.template.md"
            ),
            "template/sdlc/interface",
            proposed_documents,
        ),
        (
            PurePosixPath(
                "docs/99.templates/templates/sdlc/requirements/srs.template.md"
            ),
            "template/sdlc/srs",
            proposed_documents,
        ),
    )
    for path, profile_id, documents in exact_forms:
        documents[path] = LifecycleDocument(path, profile_id, None)

    base_commit = WORK105_CUTOVER_BASE_COMMIT
    base_registry_oid = WORK105_BASE_REGISTRY_BLOB_OID
    proposed_registry_oid = WORK105_PROPOSED_REGISTRY_BLOB_OID
    if mutation == "wrong-base":
        base_commit = "0" * 40
    elif mutation == "wrong-base-registry-oid":
        base_registry_oid = "0" * 40
    elif mutation == "wrong-proposed-registry-oid":
        proposed_registry_oid = "0" * 40
    elif mutation == "wrong-base-schema":
        base_registry["schemaVersion"] = 9
    elif mutation == "wrong-proposed-schema":
        proposed_registry["schemaVersion"] = 9
    elif mutation == "wrong-base-id":
        base_registry["$id"] = "https://example.invalid/base"
    elif mutation == "wrong-proposed-id":
        proposed_registry["$id"] = "https://example.invalid/proposed"
    elif mutation == "wrong-base-route-state":
        base_registry["routeState"] = "terminal"
    elif mutation == "wrong-proposed-route-state":
        proposed_registry["routeState"] = "terminal"
    elif mutation == "base-projection-drift":
        base_registry["unexpectedProjection"] = True
    elif mutation == "proposed-projection-drift":
        proposed_registry["unexpectedProjection"] = True
    elif mutation == "missing-ad":
        proposed_documents.pop(
            PurePosixPath(
                "docs/02.architecture/descriptions/"
                "ad-0004-argo-rollouts-progressive-delivery.md"
            )
        )
    elif mutation == "extra-ad":
        path = PurePosixPath("docs/02.architecture/descriptions/ad-9999-extra.md")
        proposed_documents[path] = LifecycleDocument(path, "sdlc/ad", "active")
    elif mutation == "wrong-status":
        path = PurePosixPath(
            "docs/02.architecture/descriptions/"
            "ad-0004-argo-rollouts-progressive-delivery.md"
        )
        proposed_documents[path] = LifecycleDocument(path, "sdlc/ad", "accepted")
    elif mutation == "missing-form":
        proposed_documents.pop(
            PurePosixPath(
                "docs/99.templates/templates/sdlc/requirements/srs.template.md"
            )
        )
    elif mutation == "wrong-form-profile":
        path = PurePosixPath(
            "docs/99.templates/templates/sdlc/requirements/srs.template.md"
        )
        proposed_documents[path] = LifecycleDocument(
            path, "template/sdlc/interface", None
        )
    elif mutation == "authored-api-instance":
        path = PurePosixPath("docs/03.specs/999-extra/api-spec.md")
        base_documents[path] = LifecycleDocument(path, "sdlc/api-spec", "active")
    elif mutation != "exact":
        raise ValueError(f"unknown WORK-105 form cutover mutation: {mutation}")
    return {
        "mode": mode,
        "base_commit": base_commit,
        "base_registry_oid": base_registry_oid,
        "proposed_registry_oid": proposed_registry_oid,
        "base_registry": base_registry,
        "proposed_registry": proposed_registry,
        "base_documents": base_documents,
        "proposed_documents": proposed_documents,
    }


def _work105_decision_evidence_fixture_inputs(
    root: Path, mutation: str
) -> dict[str, object]:
    base_text = _blob_text(
        root, WORK105_ADR0023_BASE_BLOB_OID, WORK105_ADR0023_PATH
    )
    proposed_text = _blob_text(
        root, WORK105_ADR0023_PROPOSED_BLOB_OID, WORK105_ADR0023_PATH
    )
    assert base_text is not None and proposed_text is not None
    exact_document = LifecycleDocument(WORK105_ADR0023_PATH, "sdlc/adr", "accepted")
    path = WORK105_ADR0023_PATH
    base_document: LifecycleDocument | None = exact_document
    proposed_document = exact_document
    relationship_links = (WORK105_ADR0024_PATH,)
    unresolved_links = (WORK105_LEGACY_AD0011_PATH,)
    body_table_links = (WORK105_ADR0024_PATH,)

    if mutation == "wrong-owner":
        path = WORK105_ADR0024_PATH
    elif mutation == "wrong-base-profile":
        base_document = replace(exact_document, profile_id="sdlc/ad")
    elif mutation == "wrong-proposed-status":
        proposed_document = replace(exact_document, status="active")
    elif mutation == "base-blob-drift":
        base_text += "\n"
    elif mutation == "proposed-blob-drift":
        proposed_text += "\n"
    elif mutation == "missing-reciprocal-row":
        proposed_text = proposed_text.replace(WORK105_ADR0023_RECIPROCAL_ROW, "")
    elif mutation == "missing-resolved-successor":
        relationship_links = ()
    elif mutation == "missing-table-successor":
        body_table_links = ()
    elif mutation == "extra-unresolved":
        unresolved_links += (PurePosixPath("docs/02.architecture/decisions/9999.md"),)
    elif mutation != "exact":
        raise ValueError(f"unknown WORK-105 decision evidence mutation: {mutation}")
    return {
        "path": path,
        "base_document": base_document,
        "proposed_document": proposed_document,
        "base_text": base_text,
        "proposed_text": proposed_text,
        "relationship_links": relationship_links,
        "unresolved_links": unresolved_links,
        "body_table_links": body_table_links,
    }


EXPECTED_FORWARD_CASE_NAMES = (
    "product",
    "architecture-requirement",
    "architecture-decision",
    "specification",
    "execution",
    "operations",
    "reference-governance",
)
EXPECTED_COMPARISON_CASE_NAMES = (
    "unchanged-valid-state",
    "skipped-edge",
    "reverse-edge",
    "terminal-reopen",
    "archive-reactivation",
    "same-path-profile-change",
    "same-path-unclassified-state",
    "invalid-base-state",
    "missing-proposed-state",
)
EXPECTED_ADMISSION_CASE_NAMES = (
    "draft-create-allowed",
    "archive-envelope-create-without-evidence-denied",
    "active-create-denied",
    "unclassified-create-denied",
    "unclassified-delete-denied",
    "paired-draft-create-allowed",
    "paired-active-create-allowed",
    "paired-orphan-create-denied",
    "paired-state-mismatch-denied",
    "multiple-pairs-create-denied",
    "snapshot-only-create-denied",
    "delete-denied",
    "exact-rename-single-event",
)
EXPECTED_GIT_CASE_NAMES = (
    "staged-head-index-worktree-pass",
    "staged-head-index-worktree-fail",
    "staged-add",
    "staged-delete",
    "staged-exact-rename",
    "staged-modified-rename",
    "staged-modified-governed-to-unclassified",
    "staged-modified-unclassified-to-governed",
    "staged-modified-unclassified-to-unclassified",
    "staged-governed-to-unclassified-rename",
    "staged-unclassified-to-unclassified-rename",
    "staged-unclassified-add",
    "staged-unclassified-delete",
    "staged-unclassified-modify",
    "staged-same-path-profile-change",
    "staged-unknown-type-state",
    "staged-paired-create",
    "staged-paired-create-blocked-spec",
    "staged-paired-create-ready-spec-done",
    "staged-paired-create-split-spec",
    "staged-evidence-index-invalid-worktree-valid",
    "staged-evidence-index-valid-worktree-invalid",
    "include-does-not-filter-violation",
    "staged-submodule-ignore-all",
    "ci-merge-base",
    "ci-no-merge-base",
    "ci-ambiguous-merge-base",
    "explicit-ref-pass",
    "explicit-ref-fail",
    "explicit-ref-proposed-only-evidence",
    "explicit-ref-base-only-evidence-removed",
    "ci-proposed-tree-evidence",
    "explicit-ref-submodule-ignore-all",
    "missing-ref",
    "ambiguous-ref",
    "raw-tree-ref",
    "raw-blob-ref",
    "annotated-tag-ref",
    "lightweight-commit-tag-pass",
    "git-environment-steering",
    "non-worktree-root",
    "wrong-worktree-root",
    "bare-root",
)
FINAL_TRANCHE_NEGATIVE_GIT_CASE_NAMES = (
    "staged-paired-create-blocked-spec",
    "staged-paired-create-split-spec",
)
EXPECTED_ARGUMENT_CASE_NAMES = (
    "staged-forbids-refs",
    "ci-requires-base",
    "ci-requires-to",
    "explicit-requires-from",
    "explicit-requires-to",
    "snapshot-forbids-refs",
    "invalid-mode",
)
EXPECTED_INCLUDE_CASE_NAMES = (
    "duplicate",
    "noncanonical",
    "parent",
    "non-target",
    "missing-blob",
)
EXPECTED_SNAPSHOT_CASE_NAME = "exactly-one-base-defer"
EXPECTED_ARCHIVE_CUTOVER_CASE_NAMES = (
    "exact-staged",
    "exact-ci",
    "partial-record-set",
    "extra-record",
    "wrong-base",
    "wrong-base-registry-oid",
    "proposed-policy-drift",
    "missing-template-pair",
    "wrong-registry-version",
    "missing-registry-profile-pair",
    "unrelated-profile-change",
    "snapshot-not-admitted",
    "explicit-ref-not-admitted",
)
EXPECTED_ARCHIVE_CUTOVER_MUTATIONS = frozenset(
    {
        "exact",
        "partial",
        "extra",
        "wrong-base",
        "wrong-base-registry-oid",
        "proposed-policy-drift",
        "missing-template",
        "wrong-registry-version",
        "missing-registry-profile",
        "unrelated-profile-change",
    }
)
EXPECTED_WORK105_FORM_CUTOVER_CASE_NAMES = (
    "exact-staged",
    "exact-ci",
    "wrong-mode",
    "wrong-base",
    "wrong-base-registry-oid",
    "wrong-proposed-registry-oid",
    "wrong-base-schema",
    "wrong-proposed-schema",
    "wrong-base-id",
    "wrong-proposed-id",
    "wrong-base-route-state",
    "wrong-proposed-route-state",
    "base-projection-drift",
    "proposed-projection-drift",
    "missing-ad",
    "extra-ad",
    "wrong-status",
    "missing-form",
    "wrong-form-profile",
    "authored-api-instance",
)
EXPECTED_WORK105_FORM_CUTOVER_MUTATIONS = frozenset(
    {
        "exact",
        "wrong-base",
        "wrong-base-registry-oid",
        "wrong-proposed-registry-oid",
        "wrong-base-schema",
        "wrong-proposed-schema",
        "wrong-base-id",
        "wrong-proposed-id",
        "wrong-base-route-state",
        "wrong-proposed-route-state",
        "base-projection-drift",
        "proposed-projection-drift",
        "missing-ad",
        "extra-ad",
        "wrong-status",
        "missing-form",
        "wrong-form-profile",
        "authored-api-instance",
    }
)
EXPECTED_WORK105_DECISION_EVIDENCE_CASE_NAMES = (
    "exact-reciprocal-predecessor",
    "wrong-owner",
    "wrong-base-profile",
    "wrong-proposed-status",
    "base-blob-drift",
    "proposed-blob-drift",
    "missing-reciprocal-row",
    "missing-resolved-successor",
    "missing-table-successor",
    "extra-unresolved",
)
EXPECTED_WORK105_DECISION_EVIDENCE_MUTATIONS = frozenset(
    {
        "exact",
        "wrong-owner",
        "wrong-base-profile",
        "wrong-proposed-status",
        "base-blob-drift",
        "proposed-blob-drift",
        "missing-reciprocal-row",
        "missing-resolved-successor",
        "missing-table-successor",
        "extra-unresolved",
    }
)
EXPECTED_WORK054_WP002_TRANSITION_CASE_NAMES = (
    "exact-staged",
    "exact-ci",
    "wrong-mode",
    "wrong-base",
    "missing-migration",
    "missing-ledger-row",
    "extra-ledger-row",
    "source-blob-drift",
    "source-digest-drift",
    "replacement-drift",
    "target-artifact-drift",
    "standalone-lineage-drift",
    "missing-spec-transition",
    "missing-decision",
    "decision-blob-drift",
)
EXPECTED_WORK054_WP002_TRANSITION_MUTATIONS = frozenset(
    {
        "exact",
        "wrong-base",
        "missing-migration",
        "missing-ledger-row",
        "extra-ledger-row",
        "source-blob-drift",
        "source-digest-drift",
        "replacement-drift",
        "target-artifact-drift",
        "standalone-lineage-drift",
        "missing-spec-transition",
        "missing-decision",
        "decision-blob-drift",
    }
)
FIXTURE_MUTATION_COUNT = 27
EXPECTED_EVIDENCE_ASSERTION_SHA256 = "6bd2461086ea6ff7b5aa63577f77a10441d0a3bc126ab7f6122793989c461453"  # pragma: allowlist secret
EXPECTED_EVIDENCE_VARIANTS = (
    "positive",
    "missing",
    "wrong-profile",
    "wrong-state",
    "wrong-relationship-section",
    "unchanged",
    "ambiguous-base",
    "body-contract-mismatch",
    "plain-text-path",
    "opaque-markdown",
    "orphan",
    "multiple",
)


def _dependency_ready_tranche_window(
    registry: Registry,
) -> tuple[str, str, str | None]:
    """Return the current original-tranche ready identity, state, and successor."""

    programs = [
        program for program in registry.program_lineage if program.prd_id == "0006"
    ]
    if len(programs) != 1:
        raise ValueError("PRD-0006 does not resolve one program lineage")
    program = programs[0]
    completed_count = sum(relation.state == "done" for relation in program.tranches)
    expected_states = tuple(
        "done" if index < completed_count else "active"
        for index in range(len(program.tranches))
    )
    actual_states = tuple(relation.state for relation in program.tranches)
    if actual_states != expected_states:
        raise ValueError(
            "PRD-0006 original tranche is not one contiguous done prefix "
            "followed by an active suffix"
        )
    if completed_count == len(program.tranches):
        raise ValueError("PRD-0006 has no dependency-ready original tranche")
    ready = program.tranches[completed_count]
    blocked = (
        program.tranches[completed_count + 1]
        if completed_count + 1 < len(program.tranches)
        else None
    )
    return ready.spec_id, ready.state, blocked.spec_id if blocked is not None else None


def _execution_spec_fixture_path(spec_id: str) -> PurePosixPath:
    return PurePosixPath(f"docs/03.specs/{spec_id}-evidence-fixture/spec.md")


def _registry_with_ready_spec(registry: Registry, ready_spec_id: str) -> Registry:
    """Build an isolated typed registry at one supported rollover boundary."""

    program = next(
        program for program in registry.program_lineage if program.prd_id == "0006"
    )
    ready_order = next(
        relation.order
        for relation in program.tranches
        if relation.spec_id == ready_spec_id
    )
    candidate_program = replace(
        program,
        tranches=tuple(
            replace(
                relation,
                state="done" if relation.order < ready_order else "active",
            )
            for relation in program.tranches
        ),
    )
    return replace(
        registry,
        program_lineage=tuple(
            candidate_program if item.prd_id == "0006" else item
            for item in registry.program_lineage
        ),
    )


def _self_test_dependency_ready_registry(registry: Registry) -> Registry:
    """Return an isolated final-tranche-ready registry for terminal self-tests."""

    try:
        _dependency_ready_tranche_window(registry)
    except ValueError as exc:
        if str(exc) != "PRD-0006 has no dependency-ready original tranche":
            raise
        program = next(
            program for program in registry.program_lineage if program.prd_id == "0006"
        )
        if not program.tranches or any(
            relation.state != "done" for relation in program.tranches
        ):
            raise
        return _registry_with_ready_spec(registry, program.tranches[-1].spec_id)
    return registry


class InvocationError(ValueError):
    """Invalid CLI, ref, base, Git object, or include-path provenance."""


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that returns deterministic exit 2 through ``main``."""


@dataclass(frozen=True)
class Change:
    kind: str
    path: PurePosixPath
    old_path: PurePosixPath | None = None

    @property
    def paths(self) -> tuple[PurePosixPath, ...]:
        return (self.old_path, self.path) if self.old_path is not None else (self.path,)


_LINK_VALIDATOR_MODULE: ModuleType | None = None


def _link_validator_module() -> ModuleType:
    """Load the canonical CommonMark evidence adapter once by script path."""

    global _LINK_VALIDATOR_MODULE
    if _LINK_VALIDATOR_MODULE is not None:
        return _LINK_VALIDATOR_MODULE
    path = Path(__file__).with_name("validate-links-and-owners.py")
    name = "_document_lifecycle_link_validator"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InvocationError("canonical link validator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    _LINK_VALIDATOR_MODULE = module
    return module


def _sanitized_git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment.update(FIXED_GIT_ENVIRONMENT)
    return environment


@contextlib.contextmanager
def _git_environment_scope() -> Iterator[None]:
    original = {
        key: value for key, value in os.environ.items() if key.startswith("GIT_")
    }
    for key in tuple(os.environ):
        if key.startswith("GIT_"):
            del os.environ[key]
    os.environ.update(FIXED_GIT_ENVIRONMENT)
    try:
        yield
    finally:
        for key in tuple(os.environ):
            if key.startswith("GIT_"):
                del os.environ[key]
        os.environ.update(original)


def _git_process(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    output_limit: int = GIT_CAPTURE_MAX_BYTES,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return _git_capture_bounded(
            root,
            *GIT_GLOBAL_ARGUMENTS,
            *arguments,
            stdout_limit=output_limit,
            input_bytes=input_bytes,
        )
    except ArchiveContractError as exc:
        raise InvocationError(
            f"bounded git provenance failed for "
            f"{arguments[0] if arguments else 'command'}"
        ) from exc


def _run_git(
    root: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    allow_stderr: bool = False,
    output_limit: int = GIT_CAPTURE_MAX_BYTES,
) -> bytes:
    completed = _git_process(
        root,
        arguments,
        input_bytes=input_bytes,
        output_limit=output_limit,
    )
    if completed.returncode != 0 or (completed.stderr and not allow_stderr):
        raise InvocationError(
            f"git provenance failed for {arguments[0] if arguments else 'command'}"
        )
    return completed.stdout


def _verify_repository_root(root: Path) -> None:
    resolved = root.resolve()
    top_level = _run_git(root, ("rev-parse", "--show-toplevel"))
    try:
        reported = Path(top_level.decode("utf-8").strip()).resolve()
    except UnicodeDecodeError as exc:
        raise InvocationError("Git returned a non-UTF-8 repository root") from exc
    if reported != resolved:
        raise InvocationError("--root must equal the sanitized Git worktree root")
    if _run_git(root, ("rev-parse", "--is-inside-work-tree")).strip() != b"true":
        raise InvocationError("--root is not inside a Git worktree")
    if _run_git(root, ("rev-parse", "--is-bare-repository")).strip() != b"false":
        raise InvocationError("bare repositories are not lifecycle worktrees")


def _decode_path(raw: bytes) -> PurePosixPath:
    try:
        value = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvocationError("Git returned a non-UTF-8 path") from exc
    return _normalize_path(value)


def _normalize_path(value: str) -> PurePosixPath:
    if (
        not value
        or value == "."
        or value.startswith("./")
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise InvocationError(f"noncanonical repository path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise InvocationError(f"noncanonical repository path: {value!r}")
    return path


def _approved_markdown(path: PurePosixPath) -> bool:
    if path.suffix != ".md" or not path.parts:
        return False
    if path.as_posix() == "RTK.md" or path.parts[0] in {".worktrees", "graphify-out"}:
        return False
    return path.as_posix() in ROOT_FILES or path.parts[0] in TARGET_ROOTS


def _normalize_include_paths(
    registry: Registry, values: Sequence[str]
) -> tuple[PurePosixPath, ...]:
    result: list[PurePosixPath] = []
    seen: set[PurePosixPath] = set()
    for value in values:
        path = _normalize_path(value)
        if path in seen:
            raise InvocationError(f"duplicate include path: {path.as_posix()}")
        if not _approved_markdown(path):
            raise InvocationError(
                f"include path is not governed target Markdown: {path.as_posix()}"
            )
        try:
            classify_path(registry, path)
        except DocumentContractError as exc:
            raise InvocationError(
                f"include path has no unique current registry profile: {path.as_posix()}"
            ) from exc
        seen.add(path)
        result.append(path)
    return tuple(result)


def _resolve_commit(root: Path, reference: str, label: str) -> str:
    if not reference:
        raise InvocationError(f"{label} must not be empty")
    matching_refs = _git_process(
        root,
        ("show-ref", "--", reference),
        output_limit=512,
    )
    completed = _git_process(
        root,
        ("rev-parse", "--verify", "--end-of-options", reference),
        output_limit=GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    lines = completed.stdout.decode("ascii", errors="ignore").splitlines()
    ref_lines = matching_refs.stdout.splitlines()
    if (
        matching_refs.returncode not in {0, 1}
        or len(ref_lines) > 1
        or completed.returncode != 0
        or len(lines) != 1
        or OBJECT_ID.fullmatch(lines[0]) is None
    ):
        raise InvocationError(f"{label} is missing or ambiguous")
    object_type = _run_git(root, ("cat-file", "-t", lines[0])).decode("ascii").strip()
    if object_type != "commit":
        raise InvocationError(f"{label} directly resolves to a non-commit object")
    return lines[0]


def _merge_base(root: Path, base_commit: str, to_commit: str) -> str:
    output = _run_git(root, ("merge-base", "--all", base_commit, to_commit))
    bases = output.decode("ascii", errors="ignore").splitlines()
    if len(bases) != 1 or OBJECT_ID.fullmatch(bases[0]) is None:
        raise InvocationError("CI refs do not have exactly one commit merge base")
    return bases[0]


def _parse_changes(raw: bytes) -> tuple[Change, ...]:
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git name-status output is not NUL terminated")
    changes: list[Change] = []
    cursor = 0
    while cursor < len(records) - 1:
        status_raw = records[cursor]
        cursor += 1
        try:
            status = status_raw.decode("ascii")
        except UnicodeDecodeError as exc:
            raise InvocationError("Git returned a non-ASCII change status") from exc
        if status.startswith("R") and status[1:] == "100":
            if cursor + 1 >= len(records) - 1:
                raise InvocationError("Git rename record is truncated")
            old_path = _decode_path(records[cursor])
            new_path = _decode_path(records[cursor + 1])
            cursor += 2
            changes.append(Change("R", new_path, old_path))
            continue
        if status not in {"A", "D", "M", "T"}:
            raise InvocationError(
                f"unsupported or unmerged Git change status: {status}"
            )
        if cursor >= len(records) - 1:
            raise InvocationError("Git change record is truncated")
        path = _decode_path(records[cursor])
        cursor += 1
        changes.append(Change("M" if status == "T" else status, path))
    return tuple(changes)


def _staged_changes(root: Path) -> tuple[Change, ...]:
    return _parse_changes(
        _run_git(
            root,
            (
                "diff",
                "--cached",
                "--no-ext-diff",
                "--no-textconv",
                "--ignore-submodules=none",
                "--name-status",
                "-z",
                "--find-renames=100%",
                "-l0",
                "HEAD",
                "--",
            ),
        )
    )


def _tree_changes(root: Path, base: str, proposed: str) -> tuple[Change, ...]:
    return _parse_changes(
        _run_git(
            root,
            (
                "diff",
                "--no-ext-diff",
                "--no-textconv",
                "--ignore-submodules=none",
                "--name-status",
                "-z",
                "--find-renames=100%",
                "-l0",
                base,
                proposed,
                "--",
            ),
        )
    )


def _tree_blob_oid(root: Path, commit: str, path: PurePosixPath) -> str | None:
    raw = _run_git(root, ("ls-tree", "-z", commit, "--", path.as_posix()))
    if raw == b"":
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise InvocationError(f"ambiguous tree path: {path.as_posix()}")
    try:
        header, raw_path = records[0].split(b"\t", 1)
        mode, object_type, oid = header.split(b" ", 2)
    except ValueError as exc:
        raise InvocationError("malformed git ls-tree output") from exc
    if (
        _decode_path(raw_path) != path
        or mode not in {b"100644", b"100755"}
        or object_type != b"blob"
        or OBJECT_ID.fullmatch(oid.decode("ascii", errors="ignore")) is None
    ):
        raise InvocationError(f"tree path is not one regular blob: {path.as_posix()}")
    return oid.decode("ascii")


def _index_blob_oid(root: Path, path: PurePosixPath) -> str | None:
    raw = _run_git(root, ("ls-files", "--stage", "-z", "--", path.as_posix()))
    if raw == b"":
        return None
    records = raw.split(b"\0")
    if records[-1] != b"" or len(records) != 2:
        raise InvocationError(f"ambiguous index path: {path.as_posix()}")
    try:
        header, raw_path = records[0].split(b"\t", 1)
        mode, oid, stage = header.split(b" ", 2)
    except ValueError as exc:
        raise InvocationError("malformed git ls-files output") from exc
    if (
        _decode_path(raw_path) != path
        or mode not in {b"100644", b"100755"}
        or stage != b"0"
        or OBJECT_ID.fullmatch(oid.decode("ascii", errors="ignore")) is None
    ):
        raise InvocationError(f"index path is not one stage-zero regular blob: {path}")
    return oid.decode("ascii")


def _agent_contract_blob_map(
    blob_oid: Callable[[PurePosixPath], str | None],
) -> Mapping[PurePosixPath, str]:
    result: dict[PurePosixPath, str] = {}
    for path in AGENT_ROSTER_CONTRACT_PATHS:
        oid = blob_oid(path)
        if oid is not None:
            result[path] = oid
    return MappingProxyType(result)


def _tree_blob_map(root: Path, commit: str) -> Mapping[PurePosixPath, str]:
    raw = _run_git(root, ("ls-tree", "-r", "-z", "--full-tree", commit))
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git tree inventory is not NUL terminated")
    result: dict[PurePosixPath, str] = {}
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, object_type, oid = header.split(b" ", 2)
        except ValueError as exc:
            raise InvocationError("malformed Git tree inventory") from exc
        if mode not in {b"100644", b"100755"} or object_type != b"blob":
            continue
        path = _decode_path(raw_path)
        if not _approved_markdown(path):
            continue
        value = oid.decode("ascii", errors="ignore")
        if OBJECT_ID.fullmatch(value) is None or path in result:
            raise InvocationError("ambiguous regular Markdown tree entry")
        result[path] = value
    return MappingProxyType(result)


def _index_blob_map(root: Path) -> Mapping[PurePosixPath, str]:
    raw = _run_git(root, ("ls-files", "--stage", "-z"))
    records = raw.split(b"\0")
    if not records or records[-1] != b"":
        raise InvocationError("Git index inventory is not NUL terminated")
    result: dict[PurePosixPath, str] = {}
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, oid, stage = header.split(b" ", 2)
        except ValueError as exc:
            raise InvocationError("malformed Git index inventory") from exc
        path = _decode_path(raw_path)
        if not _approved_markdown(path):
            continue
        if mode not in {b"100644", b"100755"} or stage != b"0":
            raise InvocationError(
                f"proposed Markdown is not one stage-zero regular blob: {path}"
            )
        value = oid.decode("ascii", errors="ignore")
        if OBJECT_ID.fullmatch(value) is None or path in result:
            raise InvocationError("ambiguous regular Markdown index entry")
        result[path] = value
    return MappingProxyType(result)


def _blob_text(
    root: Path,
    oid: str | None,
    path: PurePosixPath,
) -> str | None:
    if oid is None:
        return None
    raw = _blob_bytes(root, oid)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvocationError(f"document blob is not UTF-8: {path.as_posix()}") from exc


def _blob_bytes(
    root: Path,
    oid: str,
    *,
    max_bytes: int = DOCUMENT_BLOB_MAX_BYTES,
) -> bytes:
    """Read one exact Git blob without decoding or worktree substitution."""

    if (
        not isinstance(max_bytes, int)
        or isinstance(max_bytes, bool)
        or max_bytes < 0
        or max_bytes > DOCUMENT_BLOB_MAX_BYTES
    ):
        raise InvocationError("Git blob byte budget is invalid")
    size_bytes = _run_git(
        root,
        ("cat-file", "-s", oid),
        output_limit=GIT_SIZE_OUTPUT_MAX_BYTES,
    )
    try:
        size = int(size_bytes.decode("ascii", errors="strict").strip())
    except (UnicodeDecodeError, ValueError) as exc:
        raise InvocationError("Git blob size is malformed") from exc
    if size < 0 or size > max_bytes:
        raise InvocationError("Git blob exceeds its byte budget")
    payload = _run_git(
        root,
        ("cat-file", "blob", oid),
        output_limit=max_bytes,
    )
    if len(payload) != size:
        raise InvocationError("Git blob size changed during bounded read")
    return payload


def _archive_immutability_diagnostics(
    root: Path,
    base_registry: Registry,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    *,
    mode: str,
    admitted_rehome_paths: frozenset[PurePosixPath] = frozenset(),
) -> tuple[LifecycleDiagnostic, ...]:
    """Compare exact bytes for every base-selected ArchiveEnvelope record."""

    baseline: dict[str, bytes] = {}
    proposed: dict[str, bytes] = {}
    for path, oid in base_blobs.items():
        try:
            profile = classify_path(base_registry, path)
        except DocumentContractError:
            continue
        if profile.profile_id != ARCHIVE_PROFILE:
            continue
        if path in admitted_rehome_paths:
            continue
        canonical = path.as_posix()
        baseline[canonical] = _blob_bytes(root, oid)
        proposed_oid = proposed_blobs.get(path)
        if proposed_oid is not None:
            proposed[canonical] = _blob_bytes(root, proposed_oid)
    report = validate_archive_immutability(baseline, proposed)
    return tuple(
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=PurePosixPath(item.path),
            profile=ARCHIVE_PROFILE,
            expected_transition="existing archive record Git blob bytes remain identical",
            observed_transition=(
                "existing archive record deleted"
                if item.code == "ARCHIVE-IMMUTABLE-DELETION"
                else "existing archive record bytes changed"
            ),
            base_mode=mode,  # type: ignore[arg-type]
            evidence_gap=f"archive immutability rule {item.code}",
        )
        for item in report.diagnostics
    )


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise InvocationError("registry blob contains a duplicate JSON key")
        result[key] = value
    return result


def _agent_contract_blob_from_bytes(
    raw: bytes,
    path: PurePosixPath,
) -> Mapping[str, object]:
    try:
        text = raw.decode("utf-8")
        loaded = json.loads(text, object_pairs_hook=_unique_json_object)
    except (UnicodeDecodeError, json.JSONDecodeError, InvocationError) as exc:
        raise InvocationError(
            f"agent contract blob is invalid JSON: {path.as_posix()}"
        ) from exc
    if not isinstance(loaded, dict):
        raise InvocationError(
            f"agent contract blob is not an object: {path.as_posix()}"
        )
    return MappingProxyType(loaded)


def _agent_contracts_from_blob_maps(
    root: Path,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> tuple[
    Mapping[str, object],
    Mapping[str, object],
    Mapping[str, object],
    Mapping[str, object],
]:
    def load(
        blobs: Mapping[PurePosixPath, str],
        path: PurePosixPath,
        snapshot: str,
    ) -> Mapping[str, object]:
        oid = blobs.get(path)
        if oid is None:
            raise InvocationError(
                f"{snapshot} snapshot lacks agent contract blob: {path.as_posix()}"
            )
        return _agent_contract_blob_from_bytes(_blob_bytes(root, oid), path)

    return (
        load(base_blobs, AGENT_ROSTER_ADMISSION_CONTRACT_PATH, "base"),
        load(proposed_blobs, AGENT_ROSTER_ADMISSION_CONTRACT_PATH, "proposed"),
        load(base_blobs, AGENT_HARNESS_CONTRACT_PATH, "base"),
        load(proposed_blobs, AGENT_HARNESS_CONTRACT_PATH, "proposed"),
    )


def _registry_blob(
    root: Path,
    oid: str | None,
) -> Mapping[str, object]:
    text = _blob_text(root, oid, RETIRED_REGISTRY_PATH)
    if text is None:
        raise InvocationError("comparison snapshot lacks the document registry")
    try:
        loaded = json.loads(text, object_pairs_hook=_unique_json_object)
    except (json.JSONDecodeError, InvocationError) as exc:
        raise InvocationError("comparison registry blob is invalid JSON") from exc
    if not isinstance(loaded, dict):
        raise InvocationError("comparison registry blob is not an object")
    return MappingProxyType(loaded)


def _classification_registry(
    current_registry: Registry,
    raw_registry: Mapping[str, object],
) -> Registry:
    """Project snapshot-owned routes and IDs onto immutable lifecycle profiles."""

    raw_profiles = raw_registry.get("profiles")
    schema_version = raw_registry.get("schemaVersion")
    if not isinstance(raw_profiles, list) or type(schema_version) is not int:
        raise InvocationError("comparison registry profile projection is malformed")
    current_profiles = {
        profile.profile_id: profile for profile in current_registry.profiles
    }
    aliases = {
        LEGACY_ARCHIVE_PROFILE: ARCHIVE_PROFILE,
        LEGACY_ARCHIVE_TEMPLATE_PROFILE: ARCHIVE_TEMPLATE_PROFILE,
        "sdlc/ard": "sdlc/ad",  # Retired WORK-105 comparison alias.
        "template/sdlc/ard": "template/sdlc/ad",  # Retired comparison alias.
        "sdlc/api-spec": "sdlc/interface",  # Retired comparison alias.
        "template/sdlc/api-spec": "template/sdlc/interface",  # Retired alias.
    }
    projected: list[DocumentProfile] = []
    for raw_profile in raw_profiles:
        if not isinstance(raw_profile, dict):
            raise InvocationError("comparison registry contains a non-object profile")
        profile_id = raw_profile.get("id")
        raw_routes = raw_profile.get("routes")
        raw_status_domain = raw_profile.get("statusDomain")
        raw_mode = raw_profile.get("mode")
        if (
            not isinstance(profile_id, str)
            or not isinstance(raw_routes, list)
            or not isinstance(raw_status_domain, list)
            or not all(isinstance(state, str) for state in raw_status_domain)
            or not isinstance(raw_mode, str)
        ):
            raise InvocationError("comparison registry profile shape is malformed")
        source = current_profiles.get(aliases.get(profile_id, profile_id))
        if source is None:
            raise InvocationError(
                "comparison registry profile has no current lifecycle projection"
            )
        routes: list[Route] = []
        for raw_route in raw_routes:
            if not isinstance(raw_route, dict):
                raise InvocationError("comparison registry route is malformed")
            kind = raw_route.get("kind")
            value = raw_route.get("value")
            if kind not in {"exact", "regex"} or not isinstance(value, str):
                raise InvocationError("comparison registry route is malformed")
            routes.append(Route(kind=kind, value=value))  # type: ignore[arg-type]
        projected.append(
            replace(
                source,
                profile_id=profile_id,
                routes=tuple(routes),
                status_domain=tuple(raw_status_domain),
                mode=raw_mode,  # type: ignore[arg-type]
            )
        )
    return replace(
        current_registry,
        schema_version=schema_version,
        profiles=tuple(projected),
    )


def _snapshot_projection(
    root: Path,
    registry: Registry,
    blobs: Mapping[PurePosixPath, str],
) -> tuple[Mapping[PurePosixPath, LifecycleDocument], Mapping[PurePosixPath, str]]:
    documents: dict[PurePosixPath, LifecycleDocument] = {}
    texts: dict[PurePosixPath, str] = {}
    for path in sorted(blobs, key=PurePosixPath.as_posix):
        text = _blob_text(root, blobs[path], path)
        assert text is not None
        texts[path] = text
        try:
            documents[path] = document_from_text(registry, path, text)
        except DocumentContractError:
            documents[path] = LifecycleDocument(
                path=path,
                profile_id="unclassified",
                status=None,
                state_issue="no unique current registry profile",
            )
    return MappingProxyType(documents), MappingProxyType(texts)


def _body_text(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    closing = text.find("\n---\n", 4)
    return text if closing < 0 else text[closing + 5 :]


def _work105_predecessor_unresolved_links(
    *,
    path: PurePosixPath,
    base_document: LifecycleDocument | None,
    proposed_document: LifecycleDocument,
    base_text: str,
    proposed_text: str,
    relationship_links: tuple[PurePosixPath, ...],
    unresolved_links: tuple[PurePosixPath, ...],
    body_table_links: tuple[PurePosixPath, ...],
) -> tuple[PurePosixPath, ...]:
    """Admit only WORK-105's blob-pinned reciprocal predecessor evidence."""

    exact_document = LifecycleDocument(WORK105_ADR0023_PATH, "sdlc/adr", "accepted")
    exact = (
        path == WORK105_ADR0023_PATH
        and base_document == exact_document
        and proposed_document == exact_document
        and hashlib.sha256(base_text.encode("utf-8")).hexdigest()
        == WORK105_ADR0023_BASE_SHA256
        and hashlib.sha256(proposed_text.encode("utf-8")).hexdigest()
        == WORK105_ADR0023_PROPOSED_SHA256
        and proposed_text.count(WORK105_ADR0023_RECIPROCAL_ROW) == 1
        and WORK105_ADR0024_PATH in relationship_links
        and WORK105_ADR0024_PATH in body_table_links
        and unresolved_links == (WORK105_LEGACY_AD0011_PATH,)
    )
    return () if exact else unresolved_links


def _evidence_context(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
    base_texts: Mapping[PurePosixPath, str],
    proposed_texts: Mapping[PurePosixPath, str],
) -> LifecycleEvidenceContext:
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in proposed_documents.items()}
    )
    adapter = _link_validator_module()
    views: dict[PurePosixPath, LifecycleEvidenceDocument] = {}
    for path, document in proposed_documents.items():
        profile = profile_map.get(document.profile_id)
        if profile is None:
            views[path] = LifecycleEvidenceDocument(
                document=document,
                all_local_links=(),
                relationship_links=(),
                unresolved_relationship_links=(),
                body_table_links=(),
                relationship_section_valid=False,
                body_contract_valid=False,
                task_terminal_evidence_valid=False,
            )
            continue
        rendered = adapter.lifecycle_markdown_evidence(
            path, proposed_texts[path], profile, snapshot_profiles
        )
        unresolved_links = _work105_predecessor_unresolved_links(
            path=path,
            base_document=base_documents.get(path),
            proposed_document=document,
            base_text=base_texts.get(path, ""),
            proposed_text=proposed_texts[path],
            relationship_links=rendered.relationship_links,
            unresolved_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
        )
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=unresolved_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

    common = set(base_documents) & set(proposed_documents)
    status_changed = frozenset(
        path
        for path in common
        if base_documents[path].profile_id != proposed_documents[path].profile_id
        or base_documents[path].status != proposed_documents[path].status
    )
    body_changed = frozenset(
        path
        for path in common
        if _body_text(base_texts[path]) != _body_text(proposed_texts[path])
    )
    created = frozenset(set(proposed_documents) - set(base_documents))
    return LifecycleEvidenceContext(
        base_documents=base_documents,
        proposed_documents=MappingProxyType(views),
        changed_paths=frozenset(
            path
            for path in set(base_documents) | set(proposed_documents)
            if path not in common or base_texts.get(path) != proposed_texts.get(path)
        ),
        status_changed_paths=status_changed,
        body_changed_paths=body_changed | created,
        created_paths=created,
    )


def _select_changes(
    changes: Sequence[Change],
    include_paths: Sequence[PurePosixPath],
    *,
    base_oid: Callable[[PurePosixPath], str | None],
    proposed_oid: Callable[[PurePosixPath], str | None],
) -> tuple[Change, ...]:
    target_changes = [
        change
        for change in changes
        if any(_approved_markdown(path) for path in change.paths)
    ]
    if not include_paths:
        return tuple(target_changes)
    selected = list(target_changes)
    covered = {path for change in selected for path in change.paths}
    for path in include_paths:
        if path in covered:
            continue
        if base_oid(path) is None and proposed_oid(path) is None:
            raise InvocationError(
                f"included path has no base or proposed blob: {path.as_posix()}"
            )
        selected.append(Change("M", path))
    return tuple(selected)


def _comparison_documents(
    root: Path,
    base_registry: Registry,
    proposed_registry: Registry,
    changes: Sequence[Change],
    *,
    base_oid: Callable[[PurePosixPath], str | None],
    proposed_oid: Callable[[PurePosixPath], str | None],
) -> tuple[
    Mapping[PurePosixPath, LifecycleDocument],
    Mapping[PurePosixPath, LifecycleDocument],
    tuple[LifecycleRename, ...],
]:
    base_documents: dict[PurePosixPath, LifecycleDocument] = {}
    proposed_documents: dict[PurePosixPath, LifecycleDocument] = {}
    renames: list[LifecycleRename] = []

    def load(
        registry: Registry,
        path: PurePosixPath,
        oid: str | None,
    ) -> LifecycleDocument | None:
        text = _blob_text(root, oid, path)
        if text is None:
            return None
        try:
            return document_from_text(registry, path, text)
        except DocumentContractError:
            return LifecycleDocument(
                path=path,
                profile_id="unclassified",
                status=None,
                state_issue="no unique current registry profile",
            )

    for change in changes:
        if change.kind == "R":
            assert change.old_path is not None
            base = load(base_registry, change.old_path, base_oid(change.old_path))
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError("exact rename lacks a base or proposed blob")
            base_documents[change.old_path] = base
            proposed_documents[change.path] = proposed
            renames.append(LifecycleRename(change.old_path, change.path))
        elif change.kind == "A":
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if proposed is None:
                raise InvocationError(f"added path lacks proposed blob: {change.path}")
            proposed_documents[change.path] = proposed
        elif change.kind == "D":
            base = load(base_registry, change.path, base_oid(change.path))
            if base is None:
                raise InvocationError(f"deleted path lacks base blob: {change.path}")
            base_documents[change.path] = base
        else:
            base = load(base_registry, change.path, base_oid(change.path))
            proposed = load(proposed_registry, change.path, proposed_oid(change.path))
            if base is None or proposed is None:
                raise InvocationError(
                    f"modified path lacks one comparison blob: {change.path}"
                )
            base_documents[change.path] = base
            proposed_documents[change.path] = proposed
    return base_documents, proposed_documents, tuple(renames)


def _comparison_requires_evidence(
    registry: Registry,
    base_documents: Mapping[PurePosixPath, LifecycleDocument],
    proposed_documents: Mapping[PurePosixPath, LifecycleDocument],
) -> bool:
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    if any(
        document.profile_id == ARCHIVE_PROFILE and path not in base_documents
        for path, document in proposed_documents.items()
    ):
        return True
    for path in set(base_documents) & set(proposed_documents):
        base = base_documents[path]
        proposed = proposed_documents[path]
        if (
            base.profile_id != proposed.profile_id
            or base.status is None
            or proposed.status is None
            or base.status == proposed.status
        ):
            continue
        profile = profile_map.get(proposed.profile_id)
        if profile is not None and any(
            edge.from_state == base.status and edge.to_state == proposed.status
            for edge in profile.lifecycle.edges
        ):
            return True
    return any(
        document.profile_id in {"sdlc/plan", "sdlc/task"}
        and document.status in {"draft", "active"}
        for path, document in proposed_documents.items()
        if path not in base_documents
    )


def _evaluate_comparison(
    root: Path,
    registry: Registry,
    *,
    mode: str,
    from_ref: str | None = None,
    base_ref: str | None = None,
    to_ref: str | None = None,
    include_paths: Sequence[PurePosixPath] = (),
    evidence_context_factory: Callable[
        ..., LifecycleEvidenceContext
    ] = _evidence_context,
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    proposed_commit: str | None = None
    if mode == "staged":
        base_commit = _resolve_commit(root, "HEAD", "HEAD")
        base_blobs = _tree_blob_map(root, base_commit)
        proposed_blobs = _index_blob_map(root)
        changes = _staged_changes(root)
        proposed_registry_oid = _index_blob_oid(root, RETIRED_REGISTRY_PATH)
    else:
        if mode == "ci":
            assert base_ref is not None and to_ref is not None
            configured_base = _resolve_commit(root, base_ref, "base-ref")
            proposed_commit = _resolve_commit(root, to_ref, "to-ref")
            base_commit = _merge_base(root, configured_base, proposed_commit)
        elif mode == "explicit-ref":
            assert from_ref is not None and to_ref is not None
            base_commit = _resolve_commit(root, from_ref, "from-ref")
            proposed_commit = _resolve_commit(root, to_ref, "to-ref")
        else:
            raise InvocationError(f"unsupported comparison mode: {mode}")

        base_blobs = _tree_blob_map(root, base_commit)
        proposed_blobs = _tree_blob_map(root, proposed_commit)
        changes = _tree_changes(root, base_commit, proposed_commit)
        proposed_registry_oid = _tree_blob_oid(root, proposed_commit, RETIRED_REGISTRY_PATH)

    base_agent_contract_blobs: Mapping[PurePosixPath, str] = MappingProxyType({})
    proposed_agent_contract_blobs: Mapping[PurePosixPath, str] = MappingProxyType({})
    if (
        mode in {"staged", "ci"}
        and base_commit == AGENT_ROSTER_ADMISSION_BASE_COMMIT
    ):
        base_agent_contract_blobs = _agent_contract_blob_map(
            lambda path: _tree_blob_oid(root, base_commit, path)
        )
        if mode == "staged":
            proposed_agent_contract_blobs = _agent_contract_blob_map(
                lambda path: _index_blob_oid(root, path)
            )
        else:
            assert proposed_commit is not None
            proposed_agent_contract_blobs = _agent_contract_blob_map(
                lambda path: _tree_blob_oid(root, proposed_commit, path)
            )

    base_registry_oid = _tree_blob_oid(root, base_commit, RETIRED_REGISTRY_PATH)
    base_registry_raw = _registry_blob(root, base_registry_oid)
    proposed_registry_raw = _registry_blob(root, proposed_registry_oid)
    base_classification_registry = _classification_registry(registry, base_registry_raw)
    proposed_classification_registry = _classification_registry(
        registry, proposed_registry_raw
    )

    work054_wp002_consumed_paths = finite_work054_wp002_transition_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_registry=base_classification_registry,
        proposed_registry=proposed_classification_registry,
        base_registry_raw=base_registry_raw,
        proposed_registry_raw=proposed_registry_raw,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    work054_wp003_consumed_paths = finite_work054_wp003_agent_governance_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )

    work107_consumed_paths = finite_work107_archive_rehome_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_registry_oid=base_registry_oid or "",
        proposed_registry_oid=proposed_registry_oid or "",
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    work108_consumed_paths = finite_work108_artifact_identity_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_registry_oid=base_registry_oid or "",
        proposed_registry_oid=proposed_registry_oid or "",
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )

    immutability_diagnostics = _archive_immutability_diagnostics(
        root,
        base_classification_registry,
        base_blobs,
        proposed_blobs,
        mode=mode,
        admitted_rehome_paths=work107_consumed_paths | work108_consumed_paths,
    )
    if immutability_diagnostics:
        return immutability_diagnostics

    def base_oid(path: PurePosixPath) -> str | None:
        return base_blobs.get(path)

    def proposed_oid(path: PurePosixPath) -> str | None:
        return proposed_blobs.get(path)

    selected = _select_changes(
        changes,
        include_paths,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    base_documents, proposed_documents, renames = _comparison_documents(
        root,
        base_classification_registry,
        proposed_classification_registry,
        selected,
        base_oid=base_oid,
        proposed_oid=proposed_oid,
    )
    base_activation_blobs = dict(base_blobs)
    proposed_activation_blobs = dict(proposed_blobs)
    for authority_path in WORK054_WP004A_REQUIRED_CHANGED_PATHS:
        authority_base_oid = _tree_blob_oid(root, base_commit, authority_path)
        if authority_base_oid is not None:
            base_activation_blobs[authority_path] = authority_base_oid
        authority_proposed_oid = (
            _index_blob_oid(root, authority_path)
            if mode == "staged"
            else _tree_blob_oid(root, proposed_commit, authority_path)
        )
        if authority_proposed_oid is not None:
            proposed_activation_blobs[authority_path] = authority_proposed_oid
    work054_wp004a_consumed_paths = finite_work054_wp004a_authority_paths(
        mode=mode,
        base_commit=base_commit,
        base_documents=base_documents,
        proposed_documents=proposed_documents,
        base_blobs=base_activation_blobs,
        proposed_blobs=proposed_activation_blobs,
    )
    base_snapshot, base_texts = _snapshot_projection(
        root, base_classification_registry, base_blobs
    )
    proposed_snapshot, proposed_texts = _snapshot_projection(
        root, proposed_classification_registry, proposed_blobs
    )
    work105_consumed_paths = finite_work105_form_cutover_paths(
        mode=mode,
        base_commit=base_commit,
        base_registry_oid=base_registry_oid or "",
        proposed_registry_oid=proposed_registry_oid or "",
        base_registry=base_registry_raw,
        proposed_registry=proposed_registry_raw,
        base_documents=base_snapshot,
        proposed_documents=proposed_snapshot,
    )
    archive_consumed_paths = finite_archive_cutover_paths(
        mode=mode,
        base_commit=base_commit,
        base_registry_oid=base_registry_oid or "",
        proposed_registry_oid=proposed_registry_oid or "",
        base_registry=base_registry_raw,
        proposed_registry=proposed_registry_raw,
        base_documents=base_documents,
        proposed_documents=proposed_documents,
    )
    agent_consumed_paths: frozenset[PurePosixPath] = frozenset()
    if (
        mode in {"staged", "ci"}
        and base_commit == AGENT_ROSTER_ADMISSION_BASE_COMMIT
        and frozenset(AGENT_ROSTER_CUTOVER_PATHS) <= set(proposed_documents)
    ):
        try:
            (
                base_admission,
                proposed_admission,
                base_harness,
                proposed_harness,
            ) = _agent_contracts_from_blob_maps(
                root,
                base_agent_contract_blobs,
                proposed_agent_contract_blobs,
            )
        except InvocationError:
            pass
        else:
            agent_consumed_paths = finite_agent_roster_cutover_paths(
                mode=mode,
                base_commit=base_commit,
                base_documents=base_documents,
                proposed_documents=proposed_documents,
                base_admission=base_admission,
                proposed_admission=proposed_admission,
                base_harness=base_harness,
                proposed_harness=proposed_harness,
            )
    consumed_paths = (
        work054_wp002_consumed_paths
        | work054_wp003_consumed_paths
        | work054_wp004a_consumed_paths
        | work105_consumed_paths
        | work107_consumed_paths
        | work108_consumed_paths
        | archive_consumed_paths
        | agent_consumed_paths
    )

    def consume_finite_cutover(
        diagnostics: Sequence[LifecycleDiagnostic],
    ) -> tuple[LifecycleDiagnostic, ...]:
        return tuple(
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.path not in consumed_paths
        )

    if not _comparison_requires_evidence(
        proposed_classification_registry,
        base_documents,
        proposed_documents,
    ):
        return consume_finite_cutover(
            compare_lifecycle(
                proposed_classification_registry,
                base_documents,
                proposed_documents,
                renames=renames,
                base_mode=mode,  # type: ignore[arg-type]
            )
        )
    evidence = evidence_context_factory(
        proposed_classification_registry,
        base_snapshot,
        proposed_snapshot,
        base_texts,
        proposed_texts,
    )
    return consume_finite_cutover(
        compare_lifecycle(
            proposed_classification_registry,
            base_documents,
            proposed_documents,
            renames=renames,
            base_mode=mode,  # type: ignore[arg-type]
            evidence_context=evidence,
        )
    )


def _evaluate_snapshot(
    root: Path,
    registry: Registry,
    include_paths: Sequence[PurePosixPath],
) -> tuple[LifecycleDiagnostic, ...]:
    _verify_repository_root(root)
    inventory = enumerate_target_markdown(root, include_paths=tuple(include_paths))
    documents = [
        document_from_text(registry, path, read_repository_text(root, path))
        for path in inventory.current_paths
    ]
    return validate_snapshot_documents(registry, documents)


def _exit_code(diagnostics: Sequence[LifecycleDiagnostic]) -> int:
    return 1 if any(item.severity == "FAIL" for item in diagnostics) else 0


def _format_diagnostic(diagnostic: LifecycleDiagnostic) -> str:
    profile = diagnostic.profile or "-"
    return (
        f"{diagnostic.severity} {diagnostic.rule_id} {diagnostic.path.as_posix()} "
        f"profile={json.dumps(profile)} "
        f"expected={json.dumps(diagnostic.expected_transition)} "
        f"observed={json.dumps(diagnostic.observed_transition)} "
        f"base_mode={json.dumps(diagnostic.base_mode)} "
        f"evidence_gap={json.dumps(diagnostic.evidence_gap)}"
    )


def _validate_arguments(args: argparse.Namespace) -> None:
    refs = (args.from_ref, args.base_ref, args.to_ref)
    if args.mode in {"strict", "staged", "snapshot"} and any(
        ref is not None for ref in refs
    ):
        raise InvocationError(f"{args.mode} mode forbids ref flags")
    if args.mode == "ci" and (
        args.base_ref is None or args.to_ref is None or args.from_ref is not None
    ):
        raise InvocationError("ci mode requires only --base-ref and --to-ref")
    if args.mode == "explicit-ref" and (
        args.from_ref is None or args.to_ref is None or args.base_ref is not None
    ):
        raise InvocationError("explicit-ref mode requires only --from-ref and --to-ref")


def _parser() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--mode",
        choices=("strict", "staged", "ci", "explicit-ref", "snapshot"),
        default="strict",
    )
    parser.add_argument("--from-ref")
    parser.add_argument("--base-ref")
    parser.add_argument("--to-ref")
    parser.add_argument("--include-path", action="append", default=[])
    return parser


def _document(path: str, profile_id: str, status: str | None) -> LifecycleDocument:
    return LifecycleDocument(PurePosixPath(path), profile_id, status)


def _rule_ids(diagnostics: Sequence[LifecycleDiagnostic]) -> list[str]:
    return [item.rule_id for item in diagnostics]


def _fixture_link(source: PurePosixPath, target: PurePosixPath, label: str) -> str:
    relative = posixpath.relpath(target.as_posix(), source.parent.as_posix())
    return f"[{label}]({relative})"


def _opaque_fixture_link(
    source: PurePosixPath,
    target: PurePosixPath,
    label: str,
    form: int,
) -> str:
    link = _fixture_link(source, target, label)
    forms = (
        f"`{link}`",
        f"```text\n{link}\n```",
        f"<!-- {link} -->",
        f'<span data-evidence="{link}">opaque</span>',
        f"\n    {link}",
    )
    return forms[form % len(forms)]


def _evidence_fixture_text(
    profile: DocumentProfile,
    document: LifecycleDocument,
    snapshot_profiles: Mapping[PurePosixPath, str],
    relationship_targets: Sequence[PurePosixPath],
    *,
    table_targets: Sequence[PurePosixPath] = (),
    backlink_targets: Sequence[PurePosixPath] = (),
    link_mode: str = "rendered",
    opaque_form: int = 0,
    body_mismatch: bool = False,
    wrong_section: bool = False,
) -> str:
    """Build authored fixture Markdown consumed by the canonical adapter."""

    def syntax(target: PurePosixPath, label: str) -> str:
        relative = posixpath.relpath(target.as_posix(), document.path.parent.as_posix())
        if link_mode == "plain":
            return relative
        if link_mode == "opaque":
            return _opaque_fixture_link(document.path, target, label, opaque_form)
        return _fixture_link(document.path, target, label)

    sections: list[str] = []
    relationship_heading = profile.role_decision.relationship_section
    for heading in profile.headings.required:
        if wrong_section and heading == relationship_heading:
            continue
        parts = [
            f"## {heading}",
            f"Fixture {document.status or 'draft'} content for {heading}.",
        ]
        if heading == profile.headings.required[0]:
            parts.extend(
                syntax(target, f"Backlink {index + 1}")
                for index, target in enumerate(backlink_targets)
            )
        if profile.profile_id == "sdlc/task" and heading == "Task Table":
            parts.append(
                "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| FIX-001 | VAL-FIX-001 | Verify lifecycle evidence | platform | Done | Verified current authored row | [Review log](../../../README.md) |"
            )
        if heading == relationship_heading:
            if profile.body_contract is None:
                parts.extend(
                    syntax(target, f"Evidence {index + 1}")
                    for index, target in enumerate(relationship_targets)
                )
            elif body_mismatch:
                parts.append("### Lifecycle Traceability\n\nMalformed evidence table.")
            else:
                contract = profile.body_contract
                parts.append(f"### {contract.table_heading}")
                table_lines = [
                    "| " + " | ".join(contract.required_columns) + " |",
                    "| " + " | ".join("---" for _ in contract.required_columns) + " |",
                ]
                rows: list[list[str]] = []
                targets = list(relationship_targets) or [None]
                for row_number, target in enumerate(targets, start=1):
                    row = ["fixture" for _ in contract.required_columns]
                    for identifier in contract.identifier_columns:
                        index = contract.required_columns.index(identifier.column)
                        prefix = {
                            "requirement": "REQ-FIX-",
                            "criterion": "VAL-FIX-",
                            "work-item": "FIX-",
                        }[identifier.kind]
                        row[index] = f"{prefix}{row_number:03d}"
                    selected_column: str | None = None
                    if target is not None:
                        target_profile = snapshot_profiles.get(target)
                        if (
                            contract.source_link_column is not None
                            and target_profile in contract.allowed_source_profile_ids
                        ):
                            selected_column = contract.source_link_column
                        elif (
                            contract.target_link_column is not None
                            and target_profile in contract.allowed_target_profile_ids
                        ):
                            selected_column = contract.target_link_column
                        elif target_profile is None:
                            selected_column = (
                                contract.source_link_column
                                or contract.target_link_column
                            )
                    for column in (
                        contract.source_link_column,
                        contract.target_link_column,
                    ):
                        if column is None:
                            continue
                        index = contract.required_columns.index(column)
                        if column == selected_column and target is not None:
                            label = row[index]
                            row[index] = syntax(target, label)
                        else:
                            row[index] = "N/A — isolated evidence fixture"
                    if table_targets:
                        evidence_column = next(
                            (
                                column
                                for column in contract.required_columns
                                if column.casefold() == "evidence"
                            ),
                            None,
                        )
                        if evidence_column is not None:
                            row[contract.required_columns.index(evidence_column)] = (
                                " ".join(
                                    syntax(target, f"Review {index + 1}")
                                    for index, target in enumerate(table_targets)
                                )
                            )
                    rows.append(row)
                table_lines.extend("| " + " | ".join(row) + " |" for row in rows)
                parts.append("\n".join(table_lines))
        sections.append("\n\n".join(parts))
    if wrong_section:
        links = "\n".join(
            syntax(target, f"Wrong section {index + 1}")
            for index, target in enumerate(relationship_targets)
        )
        sections.append(f"## Other Relationship\n\n{links or 'No evidence.'}")
    status = document.status or "draft"
    return (
        "---\n"
        "title: 'Lifecycle evidence fixture'\n"
        f"type: {document.profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n"
        "# Lifecycle evidence fixture\n\n" + "\n\n".join(sections) + "\n"
    )


def _evidence_target_path(
    profile_id: str, predicate_id: str, case_index: int
) -> PurePosixPath:
    if predicate_id == "complete-product-program":
        if profile_id == "sdlc/srs":
            return PurePosixPath("docs/01.requirements/srs-006-evidence-fixture.md")
        if profile_id == "sdlc/interface":
            return PurePosixPath(
                "docs/01.requirements/ifc-006-evidence-fixture.md"
            )
        return PurePosixPath("docs/01.requirements/0006-evidence-fixture.md")
    if profile_id == "sdlc/plan":
        return PurePosixPath(
            f"docs/04.execution/plans/2099-01-01-edge-{case_index:02d}.md"
        )
    if profile_id == "sdlc/task":
        return PurePosixPath(
            f"docs/04.execution/tasks/2099-01-01-edge-{case_index:02d}.md"
        )
    return PurePosixPath(f"docs/__lifecycle_evidence__/{case_index:02d}-target.md")


def _evidence_case_context(
    registry: Registry,
    case: Mapping[str, object],
    variant: str,
    case_index: int,
) -> tuple[LifecycleDocument, LifecycleEvidenceContext]:
    profile_id = str(case["profile"])
    from_state = str(case["from"])
    to_state = str(case["to"])
    predicate_id = str(case["predicate"])
    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    target_path = _evidence_target_path(profile_id, predicate_id, case_index)
    target = LifecycleDocument(target_path, profile_id, to_state)
    documents: dict[PurePosixPath, LifecycleDocument] = {target_path: target}
    relationships: dict[PurePosixPath, list[PurePosixPath]] = {target_path: []}
    table_targets: dict[PurePosixPath, list[PurePosixPath]] = {target_path: []}

    def add(path: PurePosixPath, added_profile: str, status: str) -> PurePosixPath:
        documents[path] = LifecycleDocument(path, added_profile, status)
        relationships.setdefault(path, [])
        table_targets.setdefault(path, [])
        return path

    def previous(status: str | None) -> str | None:
        return {"active": "draft", "accepted": "active", "done": "active"}.get(
            status, status
        )

    primary_evidence: list[PurePosixPath] = []
    pair_paths: tuple[PurePosixPath, PurePosixPath] | None = None
    spec_identity: PurePosixPath | None = None
    program_owner_path: PurePosixPath | None = None

    if predicate_id == "accept-architecture":
        adr = add(
            PurePosixPath(
                f"docs/02.architecture/decisions/{case_index:04d}-fixture.md"
            ),
            "sdlc/adr",
            "accepted",
        )
        relationships[target_path].append(adr)
        relationships[adr].append(target_path)
        primary_evidence.append(adr)
    elif predicate_id == "complete-product-program":
        program = next(
            program for program in registry.program_lineage if program.prd_id == "0006"
        )
        program_owner = target_path
        if profile_id != "sdlc/prd":
            program_owner = add(
                PurePosixPath("docs/01.requirements/0006-evidence-fixture.md"),
                "sdlc/prd",
                "active",
            )
            relationships[target_path].append(program_owner)
            relationships[program_owner].append(target_path)
        program_owner_path = program_owner
        relation_paths: list[PurePosixPath] = []
        for relation in (*program.tranches, *program.follow_ups):
            relation_path = add(
                PurePosixPath(
                    f"docs/03.specs/{relation.spec_id}-evidence-fixture/spec.md"
                ),
                "sdlc/spec",
                "done",
            )
            relation_paths.append(relation_path)
        relationships[program_owner].extend(relation_paths)
        primary_evidence.extend(relation_paths)
    elif predicate_id in {
        "activate-execution-pair",
        "complete-specification",
        "complete-execution-pair",
        "accept-operated-document",
        "terminate-reviewed-reference",
    }:
        ready_spec_id, ready_spec_state, _ = _dependency_ready_tranche_window(registry)
        spec_identity = (
            target_path
            if profile_id
            in {
                "sdlc/spec",
                "sdlc/agent-design",
                "sdlc/data-model",
                "sdlc/tests",
            }
            else add(
                _execution_spec_fixture_path(ready_spec_id)
                if predicate_id == "activate-execution-pair"
                else PurePosixPath(
                    f"docs/03.specs/{900 + case_index:03d}-evidence/spec.md"
                ),
                "sdlc/spec",
                ready_spec_state
                if predicate_id == "activate-execution-pair"
                else "active",
            )
        )
        plan = (
            target_path
            if profile_id == "sdlc/plan"
            else add(
                PurePosixPath(
                    f"docs/04.execution/plans/2099-01-01-pair-{case_index:02d}.md"
                ),
                "sdlc/plan",
                "active" if predicate_id == "activate-execution-pair" else "done",
            )
        )
        task = (
            target_path
            if profile_id == "sdlc/task"
            else add(
                PurePosixPath(
                    f"docs/04.execution/tasks/2099-01-01-pair-{case_index:02d}.md"
                ),
                "sdlc/task",
                "active" if predicate_id == "activate-execution-pair" else "done",
            )
        )
        relationships[plan].extend((spec_identity, task))
        relationships[task].extend((spec_identity, plan))
        pair_paths = (plan, task)
        primary_evidence.extend(pair_paths)
        if predicate_id in {"accept-operated-document", "terminate-reviewed-reference"}:
            relationships[target_path].append(task)
            table_targets[task].append(target_path)
    else:
        if predicate_id in {"activate-heading-profile", "accept-decision-self"}:
            support_profile = "sdlc/ad" if profile_id == "sdlc/adr" else "sdlc/spec"
            support = add(
                PurePosixPath(
                    f"docs/__lifecycle_evidence__/{case_index:02d}-support.md"
                ),
                support_profile,
                "active",
            )
            relationships[target_path].append(support)
        primary_evidence.append(target_path)

    predicate_contract = next(
        predicate
        for predicate in registry.evidence_predicates
        if predicate.predicate_id == predicate_id
    )
    if "rendered-link" in predicate_contract.capabilities and not relationships.get(
        target_path
    ):
        target_profile = profile_map[profile_id]
        allowed = ()
        if target_profile.body_contract is not None:
            allowed = (
                target_profile.body_contract.allowed_source_profile_ids
                or target_profile.body_contract.allowed_target_profile_ids
            )
        support_profile = allowed[0] if allowed else "sdlc/spec"
        support = add(
            PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-rendered-support.md"
            ),
            support_profile,
            "active",
        )
        relationships[target_path].append(support)

    def remove(path: PurePosixPath) -> None:
        documents.pop(path, None)
        relationships.pop(path, None)
        table_targets.pop(path, None)

    self_requirement = any(
        "$self" in requirement.profile_ids
        for requirement in predicate_contract.evidence
    )

    def mutation_evidence_path() -> PurePosixPath:
        if self_requirement:
            return target_path
        if pair_paths is not None:
            return next(
                (path for path in pair_paths if path != target_path),
                pair_paths[0],
            )
        return primary_evidence[0] if primary_evidence else target_path

    if variant == "missing":
        if pair_paths is not None:
            plan, task = pair_paths
            if target_path in {plan, task} or profile_id in SPECIFICATION_PROFILES:
                relationships[plan] = [
                    path for path in relationships[plan] if path != task
                ]
                relationships[task] = [
                    path for path in relationships[task] if path != plan
                ]
            else:
                relationships[target_path] = [
                    path for path in relationships[target_path] if path != task
                ]
                table_targets[task] = [
                    path for path in table_targets[task] if path != target_path
                ]
        elif predicate_id == "complete-product-program" and primary_evidence:
            removed = primary_evidence[-1]
            owner = program_owner_path or target_path
            relationships[owner] = [
                path for path in relationships[owner] if path != removed
            ]
        elif predicate_id == "accept-architecture" and primary_evidence:
            removed = primary_evidence[0]
            relationships[target_path] = [
                path for path in relationships[target_path] if path != removed
            ]
        else:
            relationships[target_path] = []
    elif variant == "orphan":
        removed: PurePosixPath | None = None
        if pair_paths is not None:
            plan, task = pair_paths
            removable = plan if target_path == task else task
            remove(removable)
            removed = removable
        elif predicate_id == "complete-product-program" and primary_evidence:
            removed = primary_evidence[-1]
            remove(removed)
        elif predicate_id == "accept-architecture" and primary_evidence:
            removed = primary_evidence[0]
            remove(removed)
        else:
            missing_path = PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-orphan.md"
            )
            relationships[target_path] = [missing_path]
    elif variant == "wrong-profile":
        path = mutation_evidence_path()
        current = documents.get(path)
        if current is not None:
            wrong_profile = (
                "sdlc/prd" if current.profile_id == "sdlc/guide" else "sdlc/guide"
            )
            documents[path] = LifecycleDocument(path, wrong_profile, current.status)
    elif variant == "wrong-state":
        path = mutation_evidence_path()
        current = documents.get(path)
        if current is not None:
            documents[path] = LifecycleDocument(path, current.profile_id, "draft")
    elif variant == "multiple":
        if pair_paths is not None and spec_identity is not None:
            plan, task = pair_paths
            if target_path == plan:
                task_two = add(
                    PurePosixPath(
                        f"docs/04.execution/tasks/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/task",
                    documents[task].status or "done",
                )
                relationships[plan].append(task_two)
                relationships[task_two].extend((spec_identity, plan))
                if predicate_id in {
                    "accept-operated-document",
                    "terminate-reviewed-reference",
                }:
                    table_targets[task_two].append(target_path)
            elif target_path == task:
                plan_two = add(
                    PurePosixPath(
                        f"docs/04.execution/plans/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/plan",
                    documents[plan].status or "done",
                )
                relationships[task].append(plan_two)
                relationships[plan_two].extend((spec_identity, task))
            else:
                plan_two = add(
                    PurePosixPath(
                        f"docs/04.execution/plans/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/plan",
                    documents[plan].status or "done",
                )
                task_two = add(
                    PurePosixPath(
                        f"docs/04.execution/tasks/2099-01-02-pair-{case_index:02d}.md"
                    ),
                    "sdlc/task",
                    documents[task].status or "done",
                )
                relationships[plan_two].extend((spec_identity, task_two))
                relationships[task_two].extend((spec_identity, plan_two))
                if predicate_id in {
                    "accept-operated-document",
                    "terminate-reviewed-reference",
                }:
                    relationships[target_path].append(task_two)
                    table_targets[task_two].append(target_path)
        elif predicate_id == "complete-product-program" and primary_evidence:
            relation = primary_evidence[0]
            duplicate = add(
                relation.parent.with_name(relation.parent.name + "-duplicate")
                / "spec.md",
                "sdlc/spec",
                "done",
            )
            relationships[program_owner_path or target_path].append(duplicate)
        elif relationships.get(target_path):
            relationships[target_path].append(relationships[target_path][0])
        else:
            target_profile = profile_map[profile_id]
            allowed = ()
            if target_profile.body_contract is not None:
                allowed = (
                    target_profile.body_contract.allowed_source_profile_ids
                    or target_profile.body_contract.allowed_target_profile_ids
                )
            support_profile = allowed[0] if allowed else "sdlc/spec"
            support = add(
                PurePosixPath(
                    f"docs/__lifecycle_evidence__/{case_index:02d}-duplicate.md"
                ),
                support_profile,
                "active",
            )
            relationships[target_path].extend((support, support))

    corrupt_path = target_path
    if variant in {"plain-text-path", "opaque-markdown"} and not relationships.get(
        corrupt_path
    ):
        target_profile = profile_map[profile_id]
        allowed = ()
        if target_profile.body_contract is not None:
            allowed = (
                target_profile.body_contract.allowed_source_profile_ids
                or target_profile.body_contract.allowed_target_profile_ids
            )
        support_profile = allowed[0] if allowed else "sdlc/spec"
        support = add(
            PurePosixPath(
                f"docs/__lifecycle_evidence__/{case_index:02d}-syntax-support.md"
            ),
            support_profile,
            "active",
        )
        relationships.setdefault(corrupt_path, []).append(support)

    backlink_targets: dict[PurePosixPath, list[PurePosixPath]] = {
        path: [] for path in documents
    }
    for owner, linked_paths in relationships.items():
        owner_document = documents.get(owner)
        if owner_document is None:
            continue
        owner_profile = profile_map[owner_document.profile_id]
        contract = owner_profile.body_contract
        if contract is None or not contract.reciprocal_evidence:
            continue
        for linked_path in linked_paths:
            if linked_path in documents:
                backlink_targets[linked_path].append(owner)

    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in documents.items()}
    )
    adapter = _link_validator_module()
    views: dict[PurePosixPath, LifecycleEvidenceDocument] = {}
    for path, document in documents.items():
        profile = profile_map[document.profile_id]
        mode = (
            "plain"
            if variant == "plain-text-path" and path == corrupt_path
            else "opaque"
            if variant == "opaque-markdown" and path == corrupt_path
            else "rendered"
        )
        text = _evidence_fixture_text(
            profile,
            document,
            snapshot_profiles,
            relationships.get(path, ()),
            table_targets=table_targets.get(path, ()),
            backlink_targets=backlink_targets.get(path, ()),
            link_mode=mode,
            opaque_form=case_index,
            body_mismatch=(
                variant == "body-contract-mismatch"
                or (variant == "missing" and predicate_contract.relationship == "self")
            )
            and path == corrupt_path,
            wrong_section=(
                variant == "wrong-relationship-section"
                or (
                    variant == "body-contract-mismatch"
                    and profile.body_contract is None
                )
            )
            and path == corrupt_path,
        )
        rendered = adapter.lifecycle_markdown_evidence(
            path, text, profile, snapshot_profiles
        )
        views[path] = LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

    base_documents = {
        path: LifecycleDocument(path, document.profile_id, previous(document.status))
        for path, document in documents.items()
    }
    base_documents[target_path] = LifecycleDocument(target_path, profile_id, from_state)
    if predicate_id == "complete-product-program" and primary_evidence:
        last_relation = primary_evidence[-1]
        if last_relation in base_documents:
            base_documents[last_relation] = LifecycleDocument(
                last_relation, "sdlc/spec", "active"
            )
    body_changed = set(documents)
    if variant == "unchanged":
        if predicate_contract.same_diff == "self-status-and-body":
            body_changed.discard(target_path)
        elif predicate_contract.same_diff == "pair-created-or-status-changed":
            assert pair_paths is not None
            unchanged_member = next(path for path in pair_paths if path != target_path)
            base_documents[unchanged_member] = documents[unchanged_member]
        elif predicate_contract.same_diff == "target-and-last-relation-changed":
            for relation in primary_evidence:
                base_documents[relation] = documents[relation]
        elif predicate_contract.same_diff == "target-and-evidence-status-body-changed":
            evidence_path = primary_evidence[0]
            base_documents[evidence_path] = documents[evidence_path]
            body_changed.discard(evidence_path)
        elif predicate_contract.same_diff in {
            "target-plan-task-status-changed",
            "pair-status-changed",
        }:
            assert pair_paths is not None
            for pair_path in pair_paths:
                if pair_path != target_path:
                    base_documents[pair_path] = documents[pair_path]
    projected_documents = {path: view.document for path, view in views.items()}
    status_changed = frozenset(
        path
        for path in set(base_documents) & set(projected_documents)
        if base_documents[path].profile_id != projected_documents[path].profile_id
        or base_documents[path].status != projected_documents[path].status
    )
    body_changed_paths = frozenset(body_changed & set(projected_documents))
    changed_paths = status_changed | body_changed_paths
    return target, LifecycleEvidenceContext(
        base_documents=MappingProxyType(base_documents),
        proposed_documents=MappingProxyType(views),
        changed_paths=changed_paths,
        status_changed_paths=status_changed,
        body_changed_paths=body_changed_paths,
        created_paths=frozenset(),
    )


def _fixture_document_text(
    path: str,
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
    execution_spec_path: PurePosixPath | None = None,
) -> str:
    execution_spec = execution_spec_path or PurePosixPath(
        "docs/03.specs/0900-lifecycle-fixture/spec.md"
    )
    heading_sets = {
        "sdlc/spec": (
            "Overview",
            "Strategic Boundaries & Non-goals",
            "Contracts",
            "Core Design",
            "Data Modeling & Storage Strategy",
            "Interfaces & Data Structures",
            "Edge Cases & Error Handling",
            "Failure Modes & Fallback / Human Escalation",
            "Verification Commands",
            "Success Criteria & Verification Plan",
            "Traceability",
        ),
        "sdlc/plan": (
            "Overview",
            "Context",
            "Goals & In-Scope",
            "Non-Goals & Out-of-Scope",
            "Work Breakdown",
            "Verification Plan",
            "Risks & Mitigations",
            "Completion Criteria",
            "Traceability",
        ),
        "sdlc/task": (
            "Overview",
            "Inputs",
            "Task Table",
            "Approval and Safety Boundaries",
            "Verification Summary",
            "Traceability",
        ),
    }
    body_parts: list[str] = []
    for heading in heading_sets.get(profile_id, ()):
        body_parts.append(f"## {heading}\n\nLifecycle fixture {status} evidence.")
        if (
            profile_id == "sdlc/spec"
            and PurePosixPath(path) == execution_spec
            and heading == "Overview"
        ):
            owner = PurePosixPath(path)
            body_parts.append(
                " ".join(
                    (
                        _fixture_link(
                            owner,
                            execution_spec.with_name("plan.md"),
                            "Plan backlink",
                        ),
                        _fixture_link(
                            owner,
                            execution_spec.with_name("tasks.md"),
                            "Task backlink",
                        ),
                    )
                )
            )
        if profile_id == "sdlc/task" and heading == "Task Table":
            body_parts.append(
                "| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |\n"
                "| --- | --- | --- | --- | --- | --- | --- |\n"
                "| FIX-001 | VAL-FIX-001 | Exercise evidence | platform | Done | Verified fixture | [Log](../../../README.md) |"
            )
        if heading != "Traceability":
            continue
        body_parts.append("### Lifecycle Traceability")
        if profile_id == "sdlc/spec":
            body_parts.append(
                "| PRD requirement | Spec criterion | Verification method |\n"
                "| --- | --- | --- |\n"
                "| N/A — isolated lifecycle fixture | VAL-FIX-001 | Self-test |"
            )
        elif profile_id == "sdlc/plan":
            body_parts.append(
                "| Spec criterion | Work package | Expected Task |\n"
                "| --- | --- | --- |\n"
                f"| {_fixture_link(PurePosixPath(path), execution_spec, 'VAL-FIX-001')} | FIX-001 | [Task](tasks.md) |"
            )
        elif profile_id == "sdlc/task":
            spec_link = _fixture_link(
                PurePosixPath(path), execution_spec, "Spec evidence"
            )
            body_parts.append(
                "| Criterion / work item | Result | Evidence |\n"
                "| --- | --- | --- |\n"
                f"| {_fixture_link(PurePosixPath(path), execution_spec, 'FIX-001')} | Verified | {spec_link} |\n"
                f"| [FIX-002](plan.md) | Verified | {spec_link} |"
            )
    body = "\n\n".join(body_parts)
    return (
        "---\n"
        "title: 'Lifecycle fixture'\n"
        f"type: {claimed_profile_id or profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n"
        "# Lifecycle fixture\n"
        f"\n{body}\n"
    )


def _write_fixture_document(
    root: Path,
    path: str,
    profile_id: str,
    status: str,
    *,
    claimed_profile_id: str | None = None,
    execution_spec_path: PurePosixPath | None = None,
) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _fixture_document_text(
            path,
            profile_id,
            status,
            claimed_profile_id=claimed_profile_id,
            execution_spec_path=execution_spec_path,
        ),
        encoding="utf-8",
    )


def _git_fixture(root: Path, *arguments: str, input_bytes: bytes | None = None) -> str:
    return _run_git(root, arguments, input_bytes=input_bytes).decode("utf-8").strip()


def _init_fixture_repo(root: Path) -> None:
    _git_fixture(root, "init", "-q")


def _commit_fixture(root: Path, message: str) -> str:
    _git_fixture(root, "add", "--all")
    _git_fixture(root, "commit", "-q", "--allow-empty", "-m", message)
    return _git_fixture(root, "rev-parse", "HEAD")


def _configure_submodule_ignore_fixture(root: Path, path: str) -> None:
    (root / ".gitmodules").write_text(
        f'[submodule "governed"]\n\tpath = {path}\n\turl = ./unused\n\tignore = all\n',
        encoding="utf-8",
    )
    _git_fixture(root, "config", "diff.ignoreSubmodules", "all")


def _write_invalid_evidence_document(
    root: Path, path: str, profile_id: str, status: str
) -> None:
    destination = root / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "---\n"
        "title: 'Invalid evidence fixture'\n"
        f"type: {profile_id}\n"
        f"status: {status}\n"
        "owner: platform\n"
        "updated: 2099-01-01\n"
        "---\n\n# Invalid evidence fixture\n",
        encoding="utf-8",
    )


def _write_architecture_evidence_pair(
    root: Path,
    registry: Registry,
    *,
    ard_status: str,
    adr_status: str,
    linked: bool,
) -> tuple[str, str]:
    ard_path = PurePosixPath(
        "docs/02.architecture/descriptions/ad-0900-evidence-fixture.md"
    )
    adr_path = PurePosixPath("docs/02.architecture/decisions/0900-evidence-fixture.md")
    documents = {
        ard_path: LifecycleDocument(ard_path, "sdlc/ad", ard_status),
        adr_path: LifecycleDocument(adr_path, "sdlc/adr", adr_status),
    }
    snapshot_profiles = MappingProxyType(
        {path: document.profile_id for path, document in documents.items()}
    )
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    for path, document in documents.items():
        relations = (
            (adr_path,)
            if linked and path == ard_path
            else (ard_path,)
            if linked and path == adr_path
            else ()
        )
        text = _evidence_fixture_text(
            profiles[document.profile_id],
            document,
            snapshot_profiles,
            relations,
        )
        destination = root / path.as_posix()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
    return ard_path.as_posix(), adr_path.as_posix()


def _git_case(
    name: str,
    root: Path,
    registry: Registry,
    contract_root: Path,
) -> tuple[int, list[str]]:
    fixture_registry = root / RETIRED_REGISTRY_PATH
    fixture_registry.parent.mkdir(parents=True, exist_ok=True)
    fixture_registry.write_bytes((contract_root / RETIRED_REGISTRY_PATH).read_bytes())
    spec_path = "docs/03.specs/0900-example/spec.md"
    case_registry = registry
    ready_spec_id, ready_spec_state, blocked_spec_id = _dependency_ready_tranche_window(
        case_registry
    )
    if (
        name in FINAL_TRANCHE_NEGATIVE_GIT_CASE_NAMES
        and blocked_spec_id is None
    ):
        programs = [
            program
            for program in registry.program_lineage
            if program.prd_id == "0006"
        ]
        if len(programs) != 1:
            raise ValueError("negative pair fixture requires one PRD-0006 program")
        tranche_ids = tuple(relation.spec_id for relation in programs[0].tranches)
        try:
            ready_index = tranche_ids.index(ready_spec_id)
        except ValueError as exc:
            raise ValueError(
                "negative pair fixture ready tranche is not original"
            ) from exc
        if ready_index == 0:
            raise ValueError("negative pair fixture has no previous original tranche")
        case_registry = _registry_with_ready_spec(
            registry, tranche_ids[ready_index - 1]
        )
        (
            ready_spec_id,
            ready_spec_state,
            blocked_spec_id,
        ) = _dependency_ready_tranche_window(case_registry)
        if blocked_spec_id is None:
            raise ValueError("negative pair fixture fallback has no successor tranche")
    ready_spec_path = _execution_spec_fixture_path(ready_spec_id)
    blocked_spec_path = (
        _execution_spec_fixture_path(blocked_spec_id)
        if blocked_spec_id is not None
        else None
    )
    if name in {
        "staged-head-index-worktree-pass",
        "staged-head-index-worktree-fail",
        "staged-delete",
        "staged-exact-rename",
        "staged-modified-rename",
        "staged-modified-governed-to-unclassified",
        "staged-governed-to-unclassified-rename",
        "staged-same-path-profile-change",
        "staged-unknown-type-state",
        "explicit-ref-pass",
        "explicit-ref-fail",
        "ci-merge-base",
        "include-does-not-filter-violation",
        "git-environment-steering",
        "staged-submodule-ignore-all",
        "explicit-ref-submodule-ignore-all",
        "staged-evidence-index-invalid-worktree-valid",
        "staged-evidence-index-valid-worktree-invalid",
    }:
        _write_fixture_document(root, spec_path, "sdlc/spec", "draft")
    if name in {
        "staged-paired-create",
        "staged-paired-create-ready-spec-done",
        "staged-paired-create-split-spec",
    }:
        _write_fixture_document(
            root,
            ready_spec_path.as_posix(),
            "sdlc/spec",
            "done"
            if name == "staged-paired-create-ready-spec-done"
            else ready_spec_state,
            execution_spec_path=ready_spec_path,
        )
    if name == "staged-paired-create-blocked-spec":
        if blocked_spec_path is None:
            raise ValueError("blocked-pair fixture requires one successor tranche")
        _write_fixture_document(
            root,
            blocked_spec_path.as_posix(),
            "sdlc/spec",
            "active",
            execution_spec_path=blocked_spec_path,
        )
    if name == "staged-paired-create-split-spec":
        if blocked_spec_path is None:
            raise ValueError("split-pair fixture requires one successor tranche")
        _write_fixture_document(
            root,
            blocked_spec_path.as_posix(),
            "sdlc/spec",
            "active",
            execution_spec_path=blocked_spec_path,
        )
    if name in {
        "staged-modified-unclassified-to-governed",
        "staged-modified-unclassified-to-unclassified",
        "staged-unclassified-to-unclassified-rename",
        "staged-unclassified-delete",
        "staged-unclassified-modify",
    }:
        _write_fixture_document(
            root,
            "docs/__unclassified__/source.md",
            "sdlc/spec",
            "draft",
        )
    if name == "include-does-not-filter-violation":
        _write_fixture_document(
            root,
            "docs/03.specs/0901-clean/spec.md",
            "sdlc/spec",
            "draft",
        )
    if name in {
        "staged-submodule-ignore-all",
        "explicit-ref-submodule-ignore-all",
    }:
        _configure_submodule_ignore_fixture(root, spec_path)
    base_commit = _commit_fixture(root, "base")

    if name == "staged-head-index-worktree-pass":
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-head-index-worktree-fail":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-add":
        _write_fixture_document(root, spec_path, "sdlc/spec", "draft")
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-delete":
        (root / spec_path).unlink()
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-exact-rename":
        new_path = "docs/03.specs/0901-example/spec.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-rename":
        new_path = "docs/03.specs/0901-example/spec.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-governed-to-unclassified":
        new_path = "docs/__unclassified__/destination.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-unclassified-to-governed":
        old_path = "docs/__unclassified__/source.md"
        (root / spec_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", old_path, spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-modified-unclassified-to-unclassified":
        old_path = "docs/__unclassified__/source.md"
        new_path = "docs/__unclassified__/destination.md"
        _git_fixture(root, "mv", old_path, new_path)
        _write_fixture_document(root, new_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-governed-to-unclassified-rename":
        new_path = "docs/__unclassified__/renamed.md"
        (root / new_path).parent.mkdir(parents=True, exist_ok=True)
        _git_fixture(root, "mv", spec_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-to-unclassified-rename":
        old_path = "docs/__unclassified__/source.md"
        new_path = "docs/__unclassified__/destination.md"
        _git_fixture(root, "mv", old_path, new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-add":
        new_path = "docs/__unclassified__/new.md"
        _write_fixture_document(root, new_path, "sdlc/spec", "draft")
        _git_fixture(root, "add", "--", new_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-delete":
        old_path = "docs/__unclassified__/source.md"
        (root / old_path).unlink()
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unclassified-modify":
        path = "docs/__unclassified__/source.md"
        _write_fixture_document(root, path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-same-path-profile-change":
        _write_fixture_document(
            root,
            spec_path,
            "sdlc/spec",
            "active",
            claimed_profile_id="sdlc/guide",
        )
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-unknown-type-state":
        _write_fixture_document(
            root,
            spec_path,
            "sdlc/spec",
            "active",
            claimed_profile_id="sdlc/unknown",
        )
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name in {
        "staged-paired-create",
        "staged-paired-create-ready-spec-done",
    }:
        _write_fixture_document(
            root,
            ready_spec_path.with_name("plan.md").as_posix(),
            "sdlc/plan",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _write_fixture_document(
            root,
            ready_spec_path.with_name("tasks.md").as_posix(),
            "sdlc/task",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-paired-create-blocked-spec":
        assert blocked_spec_path is not None
        plan_path = blocked_spec_path.with_name("plan.md").as_posix()
        task_path = blocked_spec_path.with_name("tasks.md").as_posix()
        _write_fixture_document(
            root,
            plan_path,
            "sdlc/plan",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _write_fixture_document(
            root,
            task_path,
            "sdlc/task",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, case_registry, mode="staged")
    elif name == "staged-paired-create-split-spec":
        assert blocked_spec_path is not None
        plan_path = ready_spec_path.with_name("plan.md").as_posix()
        task_path = blocked_spec_path.with_name("tasks.md").as_posix()
        _write_fixture_document(
            root,
            plan_path,
            "sdlc/plan",
            "active",
            execution_spec_path=ready_spec_path,
        )
        _write_fixture_document(
            root,
            task_path,
            "sdlc/task",
            "active",
            execution_spec_path=blocked_spec_path,
        )
        _git_fixture(root, "add", "--all")
        diagnostics = _evaluate_comparison(root, case_registry, mode="staged")
    elif name == "staged-evidence-index-invalid-worktree-valid":
        _write_invalid_evidence_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "staged-evidence-index-valid-worktree-invalid":
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _git_fixture(root, "add", "--", spec_path)
        _write_invalid_evidence_document(root, spec_path, "sdlc/spec", "active")
        diagnostics = _evaluate_comparison(root, registry, mode="staged")
    elif name == "include-does-not-filter-violation":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="staged",
            include_paths=(PurePosixPath("docs/03.specs/0901-clean/spec.md"),),
        )
    elif name == "staged-submodule-ignore-all":
        _git_fixture(
            root,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{base_commit},{spec_path}",
        )
        try:
            _evaluate_comparison(root, registry, mode="staged")
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "explicit-ref-submodule-ignore-all":
        _git_fixture(
            root,
            "update-index",
            "--add",
            "--cacheinfo",
            f"160000,{base_commit},{spec_path}",
        )
        _git_fixture(root, "commit", "-q", "-m", "gitlink proposed")
        proposed = _git_fixture(root, "rev-parse", "HEAD")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=base_commit,
                to_ref=proposed,
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name in {"explicit-ref-pass", "explicit-ref-fail"}:
        base = _git_fixture(root, "rev-parse", "HEAD")
        status = "active" if name.endswith("pass") else "done"
        _write_fixture_document(root, spec_path, "sdlc/spec", status)
        proposed = _commit_fixture(root, "proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref=base,
            to_ref=proposed,
        )
    elif name in {
        "explicit-ref-proposed-only-evidence",
        "explicit-ref-base-only-evidence-removed",
    }:
        proposed_only = name == "explicit-ref-proposed-only-evidence"
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="active",
            adr_status="active",
            linked=not proposed_only,
        )
        base = _commit_fixture(root, "architecture evidence base")
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="accepted",
            adr_status="accepted",
            linked=proposed_only,
        )
        proposed = _commit_fixture(root, "architecture evidence proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref=base,
            to_ref=proposed,
        )
    elif name == "ci-proposed-tree-evidence":
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="active",
            adr_status="active",
            linked=False,
        )
        configured_base = _commit_fixture(root, "CI evidence base")
        _write_architecture_evidence_pair(
            root,
            registry,
            ard_status="accepted",
            adr_status="accepted",
            linked=True,
        )
        proposed = _commit_fixture(root, "CI evidence proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="ci",
            base_ref=configured_base,
            to_ref=proposed,
        )
    elif name == "ci-merge-base":
        _git_fixture(root, "branch", "proposed")
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        configured_base = _commit_fixture(root, "base advanced")
        _git_fixture(root, "switch", "-q", "proposed")
        _write_fixture_document(root, spec_path, "sdlc/spec", "active")
        _commit_fixture(root, "proposed")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="ci",
            base_ref=configured_base,
            to_ref="proposed",
        )
    elif name == "ci-no-merge-base":
        base = _git_fixture(root, "rev-parse", "HEAD")
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        orphan = _git_fixture(root, "commit-tree", tree, "-m", "orphan")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="ci",
                base_ref=base,
                to_ref=orphan,
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "ci-ambiguous-merge-base":
        common = _git_fixture(root, "rev-parse", "HEAD")
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        left = _git_fixture(root, "commit-tree", tree, "-p", common, "-m", "left")
        right = _git_fixture(root, "commit-tree", tree, "-p", common, "-m", "right")
        merge_left = _git_fixture(
            root,
            "commit-tree",
            tree,
            "-p",
            left,
            "-p",
            right,
            "-m",
            "merge-left",
        )
        merge_right = _git_fixture(
            root,
            "commit-tree",
            tree,
            "-p",
            right,
            "-p",
            left,
            "-m",
            "merge-right",
        )
        resolver_calls = 0

        def unexpected_evidence_resolver(*args: object) -> LifecycleEvidenceContext:
            nonlocal resolver_calls
            resolver_calls += 1
            raise AssertionError("evidence resolver ran before unique base selection")

        try:
            _evaluate_comparison(
                root,
                registry,
                mode="ci",
                base_ref=merge_left,
                to_ref=merge_right,
                evidence_context_factory=unexpected_evidence_resolver,
            )
        except InvocationError:
            return (
                (2, ["LIFECYCLE-BASE"])
                if resolver_calls == 0
                else (1, ["LIFECYCLE-EVIDENCE"])
            )
        return 0, []
    elif name == "missing-ref":
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="refs/heads/missing",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "ambiguous-ref":
        _git_fixture(root, "branch", "ambiguous")
        _git_fixture(root, "tag", "ambiguous")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="ambiguous",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "raw-tree-ref":
        tree = _git_fixture(root, "rev-parse", "HEAD^{tree}")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=tree,
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "raw-blob-ref":
        blob = _git_fixture(root, "hash-object", "-w", "--stdin", input_bytes=b"blob")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref=blob,
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "annotated-tag-ref":
        _git_fixture(root, "tag", "-a", "annotated", "-m", "annotated")
        try:
            _evaluate_comparison(
                root,
                registry,
                mode="explicit-ref",
                from_ref="annotated",
                to_ref="HEAD",
            )
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "lightweight-commit-tag-pass":
        _git_fixture(root, "tag", "lightweight", "HEAD")
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode="explicit-ref",
            from_ref="lightweight",
            to_ref="HEAD",
        )
    elif name == "git-environment-steering":
        _write_fixture_document(root, spec_path, "sdlc/spec", "done")
        _git_fixture(root, "add", "--", spec_path)
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-alternate-"
        ) as directory:
            alternate = Path(directory)
            _init_fixture_repo(alternate)
            _commit_fixture(alternate, "clean alternate")
            attack_values = {
                "GIT_DIR": str(alternate / ".git"),
                "GIT_WORK_TREE": str(alternate),
                "GIT_INDEX_FILE": str(alternate / ".git" / "index"),
            }
            previous = {key: os.environ.get(key) for key in attack_values}
            try:
                os.environ.update(attack_values)
                caller_environment = dict(os.environ)
                diagnostics = _evaluate_comparison(root, registry, mode="staged")
                if os.environ != caller_environment:
                    raise InvocationError("Git adapter changed the caller environment")
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    snapshot_exit = main(
                        ["--root", str(contract_root), "--mode", "snapshot"]
                    )
                if snapshot_exit != 0 or os.environ != caller_environment:
                    raise InvocationError(
                        "registry/inventory Git environment scope differs"
                    )
            finally:
                for key, value in previous.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
    elif name == "wrong-worktree-root":
        nested = root / "nested"
        nested.mkdir()
        try:
            _evaluate_comparison(nested, registry, mode="staged")
        except InvocationError:
            return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "non-worktree-root":
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-non-worktree-"
        ) as directory:
            try:
                _verify_repository_root(Path(directory))
            except InvocationError:
                return 2, ["LIFECYCLE-BASE"]
        return 0, []
    elif name == "bare-root":
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-bare-"
        ) as directory:
            bare = Path(directory)
            _git_fixture(bare, "init", "--bare", "-q")
            try:
                _verify_repository_root(bare)
            except InvocationError:
                return 2, ["LIFECYCLE-BASE"]
        return 0, []
    else:
        raise AssertionError(f"unknown Git fixture: {name}")
    return _exit_code(diagnostics), _rule_ids(diagnostics)


def _is_string_list(value: object, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(isinstance(item, str) for item in value)
    )


def _is_rule_id_list(value: object) -> bool:
    return _is_string_list(value) and all(
        rule_id in LIFECYCLE_RULE_IDS for rule_id in value
    )


def _is_exit_code(value: object) -> bool:
    return type(value) is int and value in {0, 1, 2}


def _is_document_triple(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 3
        and isinstance(value[0], str)
        and isinstance(value[1], str)
        and (isinstance(value[2], str) or value[2] is None)
    )


def _fixture_contract_failures(fixture: object, registry: Registry) -> list[str]:
    failures: list[str] = []
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    if type(fixture.get("schemaVersion")) is not int or fixture["schemaVersion"] != 1:
        return ["fixture schemaVersion must be integer 1"]

    expected_root_keys = {
        "schemaVersion",
        "requiredEntrypoints",
        "ruleIds",
        "forwardContracts",
        "comparisonCases",
        "admissionCases",
        "gitCases",
        "argumentCases",
        "includePathCases",
        "evidenceCases",
        "archiveCutoverCases",
        "work054Wp002TransitionCases",
        "work105FormCutoverCases",
        "work105DecisionEvidenceCases",
        "snapshotCase",
    }
    if set(fixture) != expected_root_keys:
        failures.append("fixture root keys differ")

    fixture_entrypoints = fixture.get("requiredEntrypoints")
    if not _is_string_list(fixture_entrypoints):
        failures.append("fixture entrypoints must be a list of strings")
    elif tuple(fixture_entrypoints) != EXPECTED_ENTRYPOINTS:
        failures.append("fixture entrypoints or order differ")

    fixture_rule_ids = fixture.get("ruleIds")
    if not _is_string_list(fixture_rule_ids):
        failures.append("stable lifecycle rule IDs must be a list of strings")
    elif (
        tuple(fixture_rule_ids) != EXPECTED_RULE_IDS
        or frozenset(fixture_rule_ids) != LIFECYCLE_RULE_IDS
    ):
        failures.append("stable lifecycle rule IDs or order differ")

    group_contracts = (
        (
            "forwardContracts",
            EXPECTED_FORWARD_CASE_NAMES,
            {"name", "profiles", "edges"},
        ),
        (
            "comparisonCases",
            EXPECTED_COMPARISON_CASE_NAMES,
            {"name", "base", "proposed", "expectedRuleIds"},
        ),
        (
            "gitCases",
            EXPECTED_GIT_CASE_NAMES,
            {"name", "expectedExit", "expectedRuleIds"},
        ),
        (
            "argumentCases",
            EXPECTED_ARGUMENT_CASE_NAMES,
            {
                "name",
                "argv",
                "expectedExit",
                "expectedRuleIds",
                "expectedBaseMode",
            },
        ),
        (
            "includePathCases",
            EXPECTED_INCLUDE_CASE_NAMES,
            {"name", "values", "expectedExit"},
        ),
        (
            "archiveCutoverCases",
            EXPECTED_ARCHIVE_CUTOVER_CASE_NAMES,
            {"name", "mode", "mutation", "expectedAdmittedCount"},
        ),
        (
            "work054Wp002TransitionCases",
            EXPECTED_WORK054_WP002_TRANSITION_CASE_NAMES,
            {"name", "mode", "mutation", "expectedAdmittedCount"},
        ),
        (
            "work105FormCutoverCases",
            EXPECTED_WORK105_FORM_CUTOVER_CASE_NAMES,
            {"name", "mode", "mutation", "expectedAdmittedCount"},
        ),
        (
            "work105DecisionEvidenceCases",
            EXPECTED_WORK105_DECISION_EVIDENCE_CASE_NAMES,
            {"name", "mutation", "expectedUnresolvedCount"},
        ),
    )
    for group_name, expected_names, expected_keys in group_contracts:
        cases = fixture.get(group_name)
        if not isinstance(cases, list):
            failures.append(f"{group_name} must be a list")
            continue
        actual_names = tuple(
            case.get("name") if isinstance(case, dict) else None for case in cases
        )
        if actual_names != expected_names:
            failures.append(f"{group_name} names or order differ")
        for case in cases:
            if not isinstance(case, dict):
                failures.append(f"{group_name} contains a non-object case")
                continue
            case_name = case.get("name")
            if set(case) != expected_keys:
                failures.append(f"{group_name} keys differ: {case_name}")

            if group_name == "forwardContracts":
                profiles = case.get("profiles")
                edges = case.get("edges")
                if not _is_string_list(profiles, nonempty=True):
                    failures.append(f"forwardContracts profiles differ: {case_name}")
                if not (
                    isinstance(edges, list)
                    and bool(edges)
                    and all(
                        isinstance(edge, list)
                        and len(edge) == 2
                        and all(isinstance(state, str) for state in edge)
                        for edge in edges
                    )
                ):
                    failures.append(f"forwardContracts edges differ: {case_name}")
            elif group_name == "comparisonCases":
                if not _is_document_triple(case.get("base")):
                    failures.append(f"comparisonCases base differs: {case_name}")
                if not _is_document_triple(case.get("proposed")):
                    failures.append(f"comparisonCases proposed differs: {case_name}")
                if not _is_rule_id_list(case.get("expectedRuleIds")):
                    failures.append(f"comparisonCases rule IDs differ: {case_name}")
            elif group_name == "gitCases":
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"gitCases exit differs: {case_name}")
                if not _is_rule_id_list(case.get("expectedRuleIds")):
                    failures.append(f"gitCases rule IDs differ: {case_name}")
            elif group_name == "argumentCases":
                if not _is_string_list(case.get("argv")):
                    failures.append(f"argumentCases argv differs: {case_name}")
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"argumentCases exit differs: {case_name}")
                expected_rules = case.get("expectedRuleIds")
                if not _is_rule_id_list(expected_rules):
                    failures.append(f"argumentCases rule IDs differ: {case_name}")
                elif (
                    expected_rules != ["LIFECYCLE-BASE"]
                    and not (
                        case_name == "invalid-mode"
                        and expected_rules == []
                    )
                ):
                    failures.append(f"argumentCases base rule differs: {case_name}")
                expected_base_mode = case.get("expectedBaseMode")
                if not isinstance(
                    expected_base_mode, str
                ) or expected_base_mode not in {
                    "staged",
                    "ci",
                    "explicit-ref",
                    "snapshot",
                    "unknown",
                    "argparse",
                }:
                    failures.append(f"argumentCases base mode differs: {case_name}")
                elif case_name != "invalid-mode" and expected_base_mode == "argparse":
                    failures.append(f"argumentCases base mode differs: {case_name}")
            elif group_name == "includePathCases":
                if not _is_string_list(case.get("values"), nonempty=True):
                    failures.append(f"includePathCases values differ: {case_name}")
                if not _is_exit_code(case.get("expectedExit")):
                    failures.append(f"includePathCases exit differs: {case_name}")
            elif group_name == "archiveCutoverCases":
                if case.get("mode") not in {
                    "staged",
                    "ci",
                    "snapshot",
                    "explicit-ref",
                }:
                    failures.append(f"archiveCutoverCases mode differs: {case_name}")
                if case.get("mutation") not in EXPECTED_ARCHIVE_CUTOVER_MUTATIONS:
                    failures.append(
                        f"archiveCutoverCases mutation differs: {case_name}"
                    )
                if case.get("expectedAdmittedCount") not in {0, 33}:
                    failures.append(f"archiveCutoverCases count differs: {case_name}")
            elif group_name == "work105FormCutoverCases":
                if case.get("mode") not in {
                    "staged",
                    "ci",
                    "snapshot",
                    "explicit-ref",
                }:
                    failures.append(
                        f"work105FormCutoverCases mode differs: {case_name}"
                    )
                if (
                    case.get("mutation")
                    not in EXPECTED_WORK105_FORM_CUTOVER_MUTATIONS
                ):
                    failures.append(
                        f"work105FormCutoverCases mutation differs: {case_name}"
                    )
                if case.get("expectedAdmittedCount") not in {0, 23}:
                    failures.append(
                        f"work105FormCutoverCases count differs: {case_name}"
                    )
            elif group_name == "work054Wp002TransitionCases":
                if case.get("mode") not in {
                    "staged",
                    "ci",
                    "snapshot",
                    "explicit-ref",
                }:
                    failures.append(
                        f"work054Wp002TransitionCases mode differs: {case_name}"
                    )
                if (
                    case.get("mutation")
                    not in EXPECTED_WORK054_WP002_TRANSITION_MUTATIONS
                ):
                    failures.append(
                        "work054Wp002TransitionCases mutation differs: "
                        f"{case_name}"
                    )
                if case.get("expectedAdmittedCount") not in {0, 303}:
                    failures.append(
                        f"work054Wp002TransitionCases count differs: {case_name}"
                    )
            elif group_name == "work105DecisionEvidenceCases":
                if (
                    case.get("mutation")
                    not in EXPECTED_WORK105_DECISION_EVIDENCE_MUTATIONS
                ):
                    failures.append(
                        f"work105DecisionEvidenceCases mutation differs: {case_name}"
                    )
                if case.get("expectedUnresolvedCount") not in {0, 1, 2}:
                    failures.append(
                        f"work105DecisionEvidenceCases count differs: {case_name}"
                    )

    admission_cases = fixture.get("admissionCases")
    if not isinstance(admission_cases, list):
        failures.append("admissionCases must be a list")
    else:
        actual_names = tuple(
            case.get("name") if isinstance(case, dict) else None
            for case in admission_cases
        )
        if actual_names != EXPECTED_ADMISSION_CASE_NAMES:
            failures.append("admissionCases names or order differ")
        for case in admission_cases:
            if not isinstance(case, dict):
                failures.append("admissionCases contains a non-object case")
                continue
            case_name = case.get("name")
            operation = case.get("operation", "create")
            operation_is_valid = isinstance(operation, str) and operation in {
                "create",
                "delete",
                "rename",
            }
            expected_keys = {"name", "documents", "expectedRuleIds"}
            if operation_is_valid and operation in {"delete", "rename"}:
                expected_keys.add("operation")
            if set(case) != expected_keys:
                failures.append(f"admissionCases keys differ: {case_name}")
            if not operation_is_valid:
                failures.append(f"admissionCases operation differs: {case_name}")
            documents = case.get("documents")
            if not (
                isinstance(documents, list)
                and bool(documents)
                and all(_is_document_triple(document) for document in documents)
            ):
                failures.append(f"admissionCases documents differ: {case_name}")
            if not _is_rule_id_list(case.get("expectedRuleIds")):
                failures.append(f"admissionCases rule IDs differ: {case_name}")

    evidence_cases = fixture.get("evidenceCases")
    if not isinstance(evidence_cases, list):
        failures.append("evidenceCases must be a list")
    else:
        for case in evidence_cases:
            if not isinstance(case, dict):
                failures.append("evidenceCases contains a non-object case")
                continue
            if set(case) != {
                "name",
                "profile",
                "from",
                "to",
                "predicate",
                "variants",
            }:
                failures.append(f"evidenceCases keys differ: {case.get('name')}")
                continue
            profile_id = case.get("profile")
            from_state = case.get("from")
            to_state = case.get("to")
            predicate = case.get("predicate")
            name = case.get("name")
            if not all(
                isinstance(value, str)
                for value in (name, profile_id, from_state, to_state, predicate)
            ):
                failures.append("evidenceCases scalar values must be strings")
            elif name != f"{profile_id}:{from_state}->{to_state}":
                failures.append(f"evidenceCases name differs: {name}")
            variants = case.get("variants")
            if (
                not _is_string_list(variants, nonempty=True)
                or tuple(variants) != EXPECTED_EVIDENCE_VARIANTS
            ):
                failures.append(f"evidenceCases variants differ: {name}")

    snapshot = fixture.get("snapshotCase")
    if not isinstance(snapshot, dict):
        failures.append("snapshotCase must be an object")
    else:
        if set(snapshot) != {"name", "expectedExit", "expectedRuleIds"}:
            failures.append("snapshotCase keys differ")
        if snapshot.get("name") != EXPECTED_SNAPSHOT_CASE_NAME:
            failures.append("snapshotCase name differs")
        if not _is_exit_code(snapshot.get("expectedExit")):
            failures.append("snapshotCase exit differs")
        if not _is_rule_id_list(snapshot.get("expectedRuleIds")):
            failures.append("snapshotCase rule IDs differ")

    if failures:
        return failures

    fixture_projection = [
        (profile_id, edge[0], edge[1])
        for contract in fixture["forwardContracts"]
        for profile_id in contract["profiles"]
        for edge in contract["edges"]
    ]
    production_projection = [
        (profile.profile_id, edge.from_state, edge.to_state)
        for profile in registry.profiles
        for edge in profile.lifecycle.edges
    ]
    if len(fixture_projection) != len(set(fixture_projection)):
        failures.append("fixture lifecycle edge projection contains duplicates")
    if sorted(fixture_projection) != sorted(production_projection):
        failures.append("fixture lifecycle edge projection differs from production")
    evidence_projection = [
        (case["profile"], case["from"], case["to"], case["predicate"])
        for case in fixture["evidenceCases"]
    ]
    production_evidence_projection = [
        (
            profile.profile_id,
            edge.from_state,
            edge.to_state,
            edge.predicate_id,
        )
        for profile in registry.profiles
        for edge in profile.lifecycle.edges
    ]
    if len(evidence_projection) != len(set(evidence_projection)):
        failures.append("fixture evidence edge projection contains duplicates")
    if evidence_projection != production_evidence_projection:
        failures.append("fixture evidence edge projection differs from production")
    if len(evidence_projection) != 44 or len(registry.evidence_predicates) != 11:
        failures.append("production evidence inventory is not 44 edges/11 predicates")
    if len({item[0] for item in evidence_projection}) != 20:
        failures.append("production evidence profile inventory is not 20")
    return failures


def _fixture_mutation_probe_failures(
    fixture: dict[str, object], registry: Registry
) -> list[str]:
    probes: list[tuple[str, dict[str, object]]] = []

    missing_operations = copy.deepcopy(fixture)
    missing_operations["forwardContracts"] = [
        case
        for case in missing_operations["forwardContracts"]
        if case["name"] != "operations"
    ]
    probes.append(("missing operations family", missing_operations))

    missing_skip = copy.deepcopy(fixture)
    missing_skip["comparisonCases"] = [
        case
        for case in missing_skip["comparisonCases"]
        if case["name"] != "skipped-edge"
    ]
    probes.append(("missing skipped edge", missing_skip))

    missing_active_create = copy.deepcopy(fixture)
    missing_active_create["admissionCases"] = [
        case
        for case in missing_active_create["admissionCases"]
        if case["name"] != "active-create-denied"
    ]
    probes.append(("missing active create denial", missing_active_create))

    missing_archive_cutover = copy.deepcopy(fixture)
    missing_archive_cutover["archiveCutoverCases"] = [
        case
        for case in missing_archive_cutover["archiveCutoverCases"]
        if case["name"] != "partial-record-set"
    ]
    probes.append(("missing archive cutover denial", missing_archive_cutover))

    missing_work054_transition = copy.deepcopy(fixture)
    missing_work054_transition["work054Wp002TransitionCases"] = [
        case
        for case in missing_work054_transition["work054Wp002TransitionCases"]
        if case["name"] != "source-digest-drift"
    ]
    probes.append(
        ("missing WORK-054 WP-002 transition denial", missing_work054_transition)
    )

    missing_work105_cutover = copy.deepcopy(fixture)
    missing_work105_cutover["work105FormCutoverCases"] = [
        case
        for case in missing_work105_cutover["work105FormCutoverCases"]
        if case["name"] != "wrong-proposed-registry-oid"
    ]
    probes.append(("missing WORK-105 form cutover denial", missing_work105_cutover))

    missing_work105_decision_evidence = copy.deepcopy(fixture)
    missing_work105_decision_evidence["work105DecisionEvidenceCases"] = [
        case
        for case in missing_work105_decision_evidence[
            "work105DecisionEvidenceCases"
        ]
        if case["name"] != "extra-unresolved"
    ]
    probes.append(
        (
            "missing WORK-105 decision evidence denial",
            missing_work105_decision_evidence,
        )
    )

    duplicate_case = copy.deepcopy(fixture)
    duplicate_case["gitCases"].append(copy.deepcopy(duplicate_case["gitCases"][0]))
    probes.append(("duplicate Git case", duplicate_case))

    unknown_case = copy.deepcopy(fixture)
    unknown_case["includePathCases"][0]["name"] = "unknown-case"
    probes.append(("unknown include case", unknown_case))

    malformed_member = copy.deepcopy(fixture)
    malformed_member["admissionCases"][0] = None
    probes.append(("malformed list member", malformed_member))

    null_comparison_base = copy.deepcopy(fixture)
    null_comparison_base["comparisonCases"][0]["base"] = None
    probes.append(("null comparison base", null_comparison_base))

    null_admission_documents = copy.deepcopy(fixture)
    null_admission_documents["admissionCases"][0]["documents"] = None
    probes.append(("null admission documents", null_admission_documents))

    malformed_status = copy.deepcopy(fixture)
    malformed_status["comparisonCases"][0]["proposed"][2] = 7
    probes.append(("malformed comparison status", malformed_status))

    malformed_exit = copy.deepcopy(fixture)
    malformed_exit["gitCases"][0]["expectedExit"] = None
    probes.append(("malformed expected exit", malformed_exit))

    malformed_nested_member = copy.deepcopy(fixture)
    malformed_nested_member["argumentCases"][0]["argv"][0] = None
    probes.append(("malformed argv member", malformed_nested_member))

    unhashable_base_mode = copy.deepcopy(fixture)
    unhashable_base_mode["argumentCases"][0]["expectedBaseMode"] = []
    probes.append(("unhashable argument base mode", unhashable_base_mode))

    unhashable_operation = copy.deepcopy(fixture)
    unhashable_operation["admissionCases"][0]["operation"] = {}
    probes.append(("unhashable admission operation", unhashable_operation))

    missing_evidence_edge = copy.deepcopy(fixture)
    missing_evidence_edge["evidenceCases"].pop()
    probes.append(("missing evidence edge", missing_evidence_edge))

    duplicate_evidence_edge = copy.deepcopy(fixture)
    duplicate_evidence_edge["evidenceCases"].append(
        copy.deepcopy(duplicate_evidence_edge["evidenceCases"][0])
    )
    probes.append(("duplicate evidence edge", duplicate_evidence_edge))

    unknown_evidence_predicate = copy.deepcopy(fixture)
    unknown_evidence_predicate["evidenceCases"][0]["predicate"] = "unknown"
    probes.append(("unknown evidence predicate", unknown_evidence_predicate))

    swapped_evidence_edges = copy.deepcopy(fixture)
    (
        swapped_evidence_edges["evidenceCases"][0],
        swapped_evidence_edges["evidenceCases"][1],
    ) = (
        swapped_evidence_edges["evidenceCases"][1],
        swapped_evidence_edges["evidenceCases"][0],
    )
    probes.append(("swapped evidence edges", swapped_evidence_edges))

    missing_evidence_variant = copy.deepcopy(fixture)
    missing_evidence_variant["evidenceCases"][0]["variants"].pop()
    probes.append(("missing evidence variant", missing_evidence_variant))

    extra_evidence_variant = copy.deepcopy(fixture)
    extra_evidence_variant["evidenceCases"][0]["variants"].append("extra")
    probes.append(("extra evidence variant", extra_evidence_variant))

    reordered_evidence_variants = copy.deepcopy(fixture)
    reordered_evidence_variants["evidenceCases"][0]["variants"].reverse()
    probes.append(("reordered evidence variants", reordered_evidence_variants))

    null_evidence_variants = copy.deepcopy(fixture)
    null_evidence_variants["evidenceCases"][0]["variants"] = None
    probes.append(("null evidence variants", null_evidence_variants))

    non_string_evidence_variant = copy.deepcopy(fixture)
    non_string_evidence_variant["evidenceCases"][0]["variants"][0] = []
    probes.append(("non-string evidence variant", non_string_evidence_variant))

    null_evidence_case = copy.deepcopy(fixture)
    null_evidence_case["evidenceCases"][0] = None
    probes.append(("null evidence case", null_evidence_case))

    failures: list[str] = []
    for name, candidate in probes:
        if not _fixture_contract_failures(candidate, registry):
            failures.append(f"fixture mutation accepted: {name}")
    return failures


EVIDENCE_REGRESSION_COUNT = 5


def _evidence_regression_failures(
    registry: Registry, evidence_cases: Sequence[Mapping[str, object]]
) -> list[str]:
    """Close the concrete bypasses reproduced by independent review."""

    failures: list[str] = []
    profiles = {profile.profile_id: profile for profile in registry.profiles}
    adapter = _link_validator_module()

    def render_view(
        document: LifecycleDocument,
        text: str,
        snapshot_profiles: Mapping[PurePosixPath, str],
    ) -> LifecycleEvidenceDocument:
        rendered = adapter.lifecycle_markdown_evidence(
            document.path,
            text,
            profiles[document.profile_id],
            snapshot_profiles,
        )
        return LifecycleEvidenceDocument(
            document=document,
            all_local_links=rendered.all_local_links,
            relationship_links=rendered.relationship_links,
            unresolved_relationship_links=rendered.unresolved_relationship_links,
            body_table_links=rendered.body_table_links,
            relationship_section_valid=rendered.relationship_section_valid,
            body_contract_valid=rendered.body_contract_valid,
            task_terminal_evidence_valid=rendered.task_terminal_evidence_valid,
        )

    prd_path = PurePosixPath("docs/01.requirements/0999-reciprocal-fixture.md")
    spec_path = PurePosixPath("docs/03.specs/0999-reciprocal-fixture/spec.md")
    prd = LifecycleDocument(prd_path, "sdlc/prd", "active")
    spec = LifecycleDocument(spec_path, "sdlc/spec", "active")
    snapshot_profiles = MappingProxyType(
        {prd_path: prd.profile_id, spec_path: spec.profile_id}
    )
    prd_text = _evidence_fixture_text(
        profiles[prd.profile_id], prd, snapshot_profiles, (spec_path,)
    )
    spec_without_backlink = _evidence_fixture_text(
        profiles[spec.profile_id], spec, snapshot_profiles, ()
    )
    no_backlink_views = MappingProxyType(
        {
            prd_path: render_view(prd, prd_text, snapshot_profiles),
            spec_path: render_view(spec, spec_without_backlink, snapshot_profiles),
        }
    )
    base_documents = MappingProxyType(
        {
            prd_path: LifecycleDocument(prd_path, "sdlc/prd", "draft"),
            spec_path: spec,
        }
    )
    no_backlink_context = LifecycleEvidenceContext(
        base_documents=base_documents,
        proposed_documents=no_backlink_views,
        changed_paths=frozenset({prd_path}),
        status_changed_paths=frozenset({prd_path}),
        body_changed_paths=frozenset({prd_path}),
        created_paths=frozenset(),
    )
    no_backlink_actual = compare_lifecycle(
        registry,
        {prd_path: base_documents[prd_path]},
        {prd_path: prd},
        base_mode="explicit-ref",
        evidence_context=no_backlink_context,
    )
    no_backlink_expected = (
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=prd_path,
            profile="sdlc/prd",
            expected_transition="predicate activate-self-body for draft -> active",
            observed_transition=f"evidence paths {[prd_path.as_posix()]!r}",
            base_mode="explicit-ref",
            evidence_gap=(
                f"reciprocal body evidence is missing from {spec_path.as_posix()}"
            ),
        ),
    )
    if no_backlink_actual != no_backlink_expected:
        failures.append(f"regression reciprocal-body: {no_backlink_actual!r}")

    spec_with_backlink = _evidence_fixture_text(
        profiles[spec.profile_id],
        spec,
        snapshot_profiles,
        (),
        backlink_targets=(prd_path,),
    )
    forged_views = MappingProxyType(
        {
            prd_path: no_backlink_views[prd_path],
            spec_path: render_view(spec, spec_with_backlink, snapshot_profiles),
        }
    )
    forged_base = MappingProxyType(
        {
            prd_path: LifecycleDocument(prd_path, "sdlc/prd", "done"),
            spec_path: spec,
        }
    )
    forged_context = LifecycleEvidenceContext(
        base_documents=forged_base,
        proposed_documents=forged_views,
        changed_paths=frozenset({prd_path}),
        status_changed_paths=frozenset({prd_path}),
        body_changed_paths=frozenset({prd_path}),
        created_paths=frozenset({prd_path}),
    )
    forged_actual = compare_lifecycle(
        registry,
        {prd_path: LifecycleDocument(prd_path, "sdlc/prd", "draft")},
        {prd_path: prd},
        base_mode="explicit-ref",
        evidence_context=forged_context,
    )
    forged_expected = (
        LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-EVIDENCE",
            path=prd_path,
            profile="sdlc/prd",
            expected_transition="predicate activate-self-body for draft -> active",
            observed_transition=f"evidence paths {[prd_path.as_posix()]!r}",
            base_mode="explicit-ref",
            evidence_gap=(
                "created-path projection differs from canonical snapshots; "
                "base evidence projection differs from transition source"
            ),
        ),
    )
    if forged_actual != forged_expected:
        failures.append(f"regression forged-context: {forged_actual!r}")

    reference_path = PurePosixPath(
        "docs/90.references/research/2099-01-01-heading-fixture.md"
    )
    support_path = PurePosixPath("docs/03.specs/0998-heading-fixture/spec.md")
    reference = LifecycleDocument(reference_path, "content/reference", "active")
    support = LifecycleDocument(support_path, "sdlc/spec", "active")
    heading_profiles = MappingProxyType(
        {reference_path: reference.profile_id, support_path: support.profile_id}
    )
    reference_text = _evidence_fixture_text(
        profiles[reference.profile_id],
        reference,
        heading_profiles,
        (support_path,),
    )
    reference_text += "\n## Unsupported Lifecycle Heading\n\nRejected.\n"
    heading_view = render_view(reference, reference_text, heading_profiles)
    if heading_view.body_contract_valid:
        failures.append("regression unsupported-root-h2: adapter accepted heading")
    heading_context = LifecycleEvidenceContext(
        base_documents=MappingProxyType(
            {
                reference_path: LifecycleDocument(
                    reference_path, "content/reference", "draft"
                ),
                support_path: support,
            }
        ),
        proposed_documents=MappingProxyType(
            {
                reference_path: heading_view,
                support_path: render_view(
                    support,
                    _evidence_fixture_text(
                        profiles[support.profile_id],
                        support,
                        heading_profiles,
                        (),
                    ),
                    heading_profiles,
                ),
            }
        ),
        changed_paths=frozenset({reference_path}),
        status_changed_paths=frozenset({reference_path}),
        body_changed_paths=frozenset({reference_path}),
        created_paths=frozenset(),
    )
    heading_actual = compare_lifecycle(
        registry,
        {reference_path: heading_context.base_documents[reference_path]},
        {reference_path: reference},
        base_mode="explicit-ref",
        evidence_context=heading_context,
    )
    if (
        len(heading_actual) != 1
        or heading_actual[0].evidence_gap
        != f"body contract mismatch at {reference_path.as_posix()}"
    ):
        failures.append(f"regression unsupported-root-h2: {heading_actual!r}")

    task_path = PurePosixPath("docs/04.execution/tasks/2099-01-01-terminal.md")
    task = LifecycleDocument(task_path, "sdlc/task", "done")
    terminal_profiles = MappingProxyType({task_path: task.profile_id})
    task_text = _evidence_fixture_text(
        profiles[task.profile_id], task, terminal_profiles, ()
    )
    real_terminal = render_view(task, task_text, terminal_profiles)
    placeholder_text = task_text.replace(
        "[Review log](../../../README.md)", "Named repository evidence"
    )
    placeholder_terminal = render_view(task, placeholder_text, terminal_profiles)
    if (
        not real_terminal.task_terminal_evidence_valid
        or placeholder_terminal.task_terminal_evidence_valid
    ):
        failures.append(
            "regression task-terminal-placeholder: canonical phrase/link differs"
        )

    operated_index, operated_case = next(
        (index, case)
        for index, case in enumerate(evidence_cases)
        if case["predicate"] == "accept-operated-document"
    )
    operated_target, operated_context = _evidence_case_context(
        registry, operated_case, "positive", operated_index
    )
    operated_views = dict(operated_context.proposed_documents)
    operated_task_path = next(
        path
        for path, view in operated_views.items()
        if view.document.profile_id == "sdlc/task"
    )
    operated_task = operated_views[operated_task_path].document
    operated_profiles = MappingProxyType(
        {path: view.document.profile_id for path, view in operated_views.items()}
    )
    operated_relationships = operated_views[operated_task_path].relationship_links
    task_with_evidence = _evidence_fixture_text(
        profiles[operated_task.profile_id],
        operated_task,
        operated_profiles,
        operated_relationships,
        table_targets=(operated_target.path,),
    )
    evidence_link = _fixture_link(operated_task_path, operated_target.path, "Review 1")
    result_link = _fixture_link(
        operated_task_path, operated_target.path, "Result target"
    )
    task_with_result_only = task_with_evidence.replace(evidence_link, "Verified")
    task_with_result_only = task_with_result_only.replace(
        "| fixture | Verified |", f"| {result_link} | Verified |"
    )
    result_only_view = render_view(
        operated_task, task_with_result_only, operated_profiles
    )
    if (
        operated_target.path in result_only_view.body_table_links
        or operated_target.path not in result_only_view.all_local_links
    ):
        failures.append("regression task-result-column: adapter projection differs")
    operated_views[operated_task_path] = result_only_view
    result_context = LifecycleEvidenceContext(
        base_documents=operated_context.base_documents,
        proposed_documents=MappingProxyType(operated_views),
        changed_paths=operated_context.changed_paths,
        status_changed_paths=operated_context.status_changed_paths,
        body_changed_paths=operated_context.body_changed_paths,
        created_paths=operated_context.created_paths,
    )
    result_actual = compare_lifecycle(
        registry,
        {
            operated_target.path: LifecycleDocument(
                operated_target.path,
                operated_target.profile_id,
                operated_case["from"],
            )
        },
        {operated_target.path: operated_target},
        base_mode="explicit-ref",
        evidence_context=result_context,
    )
    if _rule_ids(result_actual) != ["LIFECYCLE-EVIDENCE"]:
        failures.append(f"regression task-result-column: {result_actual!r}")

    return failures


def _ambiguous_base_edge_failures(
    registry: Registry, evidence_cases: Sequence[Mapping[str, object]]
) -> list[str]:
    """Run an edge-shaped public CI base gate for every production edge."""

    failures: list[str] = []
    invoked_edges: list[tuple[str, str, str]] = []
    expected_edges = [
        (str(case["profile"]), str(case["from"]), str(case["to"]))
        for case in evidence_cases
    ]
    for case_index, case in enumerate(evidence_cases):
        with tempfile.TemporaryDirectory(
            prefix="document-lifecycle-ambiguous-evidence-"
        ) as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            profile_id = str(case["profile"])
            from_state = str(case["from"])
            to_state = str(case["to"])
            edge = (profile_id, from_state, to_state)
            invoked_edges.append(edge)
            target_path = _evidence_target_path(
                profile_id, str(case["predicate"]), case_index
            )
            _write_fixture_document(
                repo, target_path.as_posix(), profile_id, from_state
            )
            common = _commit_fixture(repo, f"common {case['name']}")
            base_tree = _git_fixture(repo, "rev-parse", "HEAD^{tree}")
            left = _git_fixture(
                repo, "commit-tree", base_tree, "-p", common, "-m", "left"
            )
            right = _git_fixture(
                repo, "commit-tree", base_tree, "-p", common, "-m", "right"
            )
            _write_fixture_document(repo, target_path.as_posix(), profile_id, to_state)
            _git_fixture(repo, "add", "--", target_path.as_posix())
            proposed_tree = _git_fixture(repo, "write-tree")
            merge_left = _git_fixture(
                repo,
                "commit-tree",
                base_tree,
                "-p",
                left,
                "-p",
                right,
                "-m",
                "merge-left",
            )
            merge_right = _git_fixture(
                repo,
                "commit-tree",
                proposed_tree,
                "-p",
                right,
                "-p",
                left,
                "-m",
                "merge-right",
            )
            resolver_calls = 0

            def unexpected_evidence_resolver(
                *args: object,
            ) -> LifecycleEvidenceContext:
                nonlocal resolver_calls
                resolver_calls += 1
                raise AssertionError(
                    "evidence resolver ran before unique base selection"
                )

            try:
                _evaluate_comparison(
                    repo,
                    registry,
                    mode="ci",
                    base_ref=merge_left,
                    to_ref=merge_right,
                    include_paths=(target_path,),
                    evidence_context_factory=unexpected_evidence_resolver,
                )
            except InvocationError as exc:
                if str(exc) != "CI refs do not have exactly one commit merge base":
                    failures.append(
                        f"evidence {case['name']}/ambiguous-base: "
                        f"base error differs: {exc}"
                    )
            else:
                failures.append(
                    f"evidence {case['name']}/ambiguous-base: base gate passed"
                )
            if resolver_calls != 0:
                failures.append(
                    f"evidence {case['name']}/ambiguous-base: "
                    f"resolver calls {resolver_calls}"
                )
    if invoked_edges != expected_edges or len(set(invoked_edges)) != 44:
        failures.append(
            "ambiguous-base did not invoke the exact 44 unique profile/state edges"
        )
    return failures


def _evidence_assertion_run(
    registry: Registry,
    evidence_cases: Sequence[Mapping[str, object]],
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    """Build the exact 528-case diagnostic projection for one lineage state."""

    projection: list[dict[str, object]] = []
    ambiguous_controls: list[str] = []
    failures: list[str] = []
    for case_index, case in enumerate(evidence_cases):
        for variant_value in case["variants"]:
            variant = str(variant_value)
            if variant == "ambiguous-base":
                ambiguous_controls.append(str(case["name"]))
                diagnostics = (
                    LifecycleDiagnostic(
                        severity="FAIL",
                        rule_id="LIFECYCLE-BASE",
                        path=PurePosixPath("."),
                        profile="",
                        expected_transition=(
                            "valid invocation, unique commit refs, and one "
                            "comparison base"
                        ),
                        observed_transition=(
                            "CI refs do not have exactly one commit merge base"
                        ),
                        base_mode="ci",
                        evidence_gap="argument or Git provenance",
                    ),
                )
                target_path = _evidence_target_path(
                    str(case["profile"]), str(case["predicate"]), case_index
                )
                expected_rules = ["LIFECYCLE-BASE"]
            else:
                target, evidence_context = _evidence_case_context(
                    registry, case, variant, case_index
                )
                target_path = target.path
                base_target = LifecycleDocument(
                    target.path, target.profile_id, str(case["from"])
                )
                diagnostics = compare_lifecycle(
                    registry,
                    {target.path: base_target},
                    {target.path: target},
                    base_mode="explicit-ref",
                    evidence_context=evidence_context,
                )
                expected_rules = [] if variant == "positive" else ["LIFECYCLE-EVIDENCE"]
            actual_rules = _rule_ids(diagnostics)
            if actual_rules != expected_rules:
                failures.append(
                    f"evidence {case['name']}/{variant}: "
                    f"expected {expected_rules}, actual {actual_rules}"
                )
            if variant not in {"positive", "ambiguous-base"} and len(diagnostics) != 1:
                failures.append(
                    f"evidence {case['name']}/{variant}: diagnostic count differs"
                )
            projection.append(
                {
                    "case": case["name"],
                    "profile": case["profile"],
                    "from": case["from"],
                    "to": case["to"],
                    "predicate": case["predicate"],
                    "variant": variant,
                    "target": target_path.as_posix(),
                    "diagnostics": [
                        {
                            "severity": diagnostic.severity,
                            "ruleId": diagnostic.rule_id,
                            "path": diagnostic.path.as_posix(),
                            "profile": diagnostic.profile,
                            "expectedTransition": diagnostic.expected_transition,
                            "observedTransition": diagnostic.observed_transition,
                            "baseMode": diagnostic.base_mode,
                            "evidenceGap": diagnostic.evidence_gap,
                        }
                        for diagnostic in diagnostics
                    ],
                }
            )
    return projection, ambiguous_controls, failures


def _evidence_assertion_sha256(projection: Sequence[Mapping[str, object]]) -> str:
    return hashlib.sha256(
        json.dumps(
            projection,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _run_self_test(root: Path) -> list[str]:
    failures: list[str] = []
    fixture = load_json_file(root / FIXTURE_PATH, diagnostic_path=FIXTURE_PATH)
    registry = load_registry(root)
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    contract_failures = _fixture_contract_failures(fixture, registry)
    failures.extend(contract_failures)
    if contract_failures:
        return failures
    failures.extend(_fixture_mutation_probe_failures(fixture, registry))
    evidence_registry = _self_test_dependency_ready_registry(registry)
    for entrypoint in fixture.get("requiredEntrypoints", []):
        if not (root / entrypoint).is_file():
            failures.append(f"missing public entrypoint: {entrypoint}")

    profile_map = {profile.profile_id: profile for profile in registry.profiles}
    forward_count = 0
    for contract in fixture.get("forwardContracts", []):
        literal_edges = {tuple(edge) for edge in contract["edges"]}
        for profile_id in contract["profiles"]:
            profile = profile_map.get(profile_id)
            if profile is None:
                failures.append(f"forward {contract['name']}: unknown {profile_id}")
                continue
            production_edges = {
                (edge.from_state, edge.to_state) for edge in profile.lifecycle.edges
            }
            if production_edges != literal_edges:
                failures.append(
                    f"forward {contract['name']}/{profile_id}: literal edge set differs"
                )
                continue
            for from_state, to_state in contract["edges"]:
                path = PurePosixPath(f"docs/__lifecycle__/{forward_count}.md")
                diagnostics = compare_lifecycle(
                    registry,
                    {path: LifecycleDocument(path, profile_id, from_state)},
                    {path: LifecycleDocument(path, profile_id, to_state)},
                    base_mode="explicit-ref",
                )
                if diagnostics:
                    failures.append(
                        f"forward {contract['name']}/{profile_id}/{from_state}-{to_state}: rejected"
                    )
                forward_count += 1

    evidence_cases = fixture.get("evidenceCases", [])
    failures.extend(_ambiguous_base_edge_failures(evidence_registry, evidence_cases))
    (
        evidence_assertion_projection,
        ambiguous_edge_controls,
        evidence_assertion_failures,
    ) = _evidence_assertion_run(evidence_registry, evidence_cases)
    failures.extend(evidence_assertion_failures)
    if len(ambiguous_edge_controls) != 44 or len(set(ambiguous_edge_controls)) != 44:
        failures.append("ambiguous-base edge projection is not exactly 44 unique edges")
    evidence_assertion_sha256 = _evidence_assertion_sha256(
        evidence_assertion_projection
    )
    if (
        len(evidence_assertion_projection) != 528
        or evidence_assertion_sha256 != EXPECTED_EVIDENCE_ASSERTION_SHA256
    ):
        failures.append(
            "evidence exact assertion projection differs: "
            f"count={len(evidence_assertion_projection)} "
            f"sha256={evidence_assertion_sha256}"
        )

    current_ready_spec_id, current_ready_state, _ = _dependency_ready_tranche_window(
        evidence_registry
    )
    if current_ready_state != "active":
        failures.append("current dependency-ready original tranche is not active")
    # The main projection above and named staged-paired-create case below prove
    # the current boundary.  Fixed 035/036 proofs that are not current still
    # run; after production advances to 037 or later, both fixed proofs run.
    fixed_proof_ids = {"0035", "0036"} - {current_ready_spec_id}
    for ready_spec_id in sorted(fixed_proof_ids):
        rollover_registry = _registry_with_ready_spec(registry, ready_spec_id)
        actual_ready_spec_id, actual_ready_state, _ = _dependency_ready_tranche_window(
            rollover_registry
        )
        if (actual_ready_spec_id, actual_ready_state) != (ready_spec_id, "active"):
            failures.append(
                f"rollover {ready_spec_id}: dependency-ready projection differs"
            )
            continue
        (
            rollover_projection,
            rollover_controls,
            rollover_failures,
        ) = _evidence_assertion_run(rollover_registry, evidence_cases)
        if rollover_failures:
            failures.extend(
                f"rollover {ready_spec_id}: {failure}" for failure in rollover_failures
            )
        rollover_sha256 = _evidence_assertion_sha256(rollover_projection)
        if (
            len(rollover_projection) != 528
            or rollover_sha256 != EXPECTED_EVIDENCE_ASSERTION_SHA256
            or len(rollover_controls) != 44
            or len(set(rollover_controls)) != 44
        ):
            failures.append(
                f"rollover {ready_spec_id}: evidence exact assertion projection "
                f"differs: count={len(rollover_projection)} sha256={rollover_sha256}"
            )
        with tempfile.TemporaryDirectory(
            prefix=f"document-lifecycle-rollover-{ready_spec_id}-"
        ) as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            try:
                pair_exit, pair_rules = _git_case(
                    "staged-paired-create", repo, rollover_registry, root
                )
            except (InvocationError, OSError, ValueError) as exc:
                failures.append(f"rollover {ready_spec_id}: paired create error {exc}")
            else:
                if pair_exit != 0 or pair_rules:
                    failures.append(
                        f"rollover {ready_spec_id}: paired create differs "
                        f"exit={pair_exit} rules={pair_rules}"
                    )
    prd006_program = next(
        program for program in registry.program_lineage if program.prd_id == "0006"
    )
    final_tranche_registry = _registry_with_ready_spec(
        registry, prd006_program.tranches[-1].spec_id
    )
    for case_name in FINAL_TRANCHE_NEGATIVE_GIT_CASE_NAMES:
        with tempfile.TemporaryDirectory(
            prefix=f"document-lifecycle-final-tranche-{case_name}-"
        ) as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            try:
                actual_exit, actual_rules = _git_case(
                    case_name, repo, final_tranche_registry, root
                )
            except (InvocationError, OSError, ValueError) as exc:
                failures.append(
                    f"final tranche {case_name}: unexpected error {exc}"
                )
                continue
        if actual_exit != 1 or actual_rules != [
            "LIFECYCLE-EVIDENCE",
            "LIFECYCLE-EVIDENCE",
        ]:
            failures.append(
                f"final tranche {case_name}: expected exit=1 and two "
                f"LIFECYCLE-EVIDENCE rules, actual exit={actual_exit} "
                f"rules={actual_rules}"
            )
    failures.extend(_evidence_regression_failures(evidence_registry, evidence_cases))

    for case in fixture.get("archiveCutoverCases", []):
        admitted = finite_archive_cutover_paths(
            **_archive_cutover_fixture_inputs(case["mode"], case["mutation"])
        )
        if len(admitted) != case["expectedAdmittedCount"]:
            failures.append(
                f"archive cutover {case['name']}: expected admitted count "
                f"{case['expectedAdmittedCount']}, actual {len(admitted)}"
            )

    for case in fixture.get("work054Wp002TransitionCases", []):
        admitted = finite_work054_wp002_transition_paths(
            **_work054_wp002_transition_fixture_inputs(
                root, case["mode"], case["mutation"]
            )
        )
        if len(admitted) != case["expectedAdmittedCount"]:
            failures.append(
                f"WORK-054 WP-002 transition {case['name']}: expected admitted "
                f"count {case['expectedAdmittedCount']}, actual {len(admitted)}"
            )

    for case in fixture.get("work105FormCutoverCases", []):
        admitted = finite_work105_form_cutover_paths(
            **_work105_form_cutover_fixture_inputs(
                root, case["mode"], case["mutation"]
            )
        )
        if len(admitted) != case["expectedAdmittedCount"]:
            failures.append(
                f"WORK-105 form cutover {case['name']}: expected admitted count "
                f"{case['expectedAdmittedCount']}, actual {len(admitted)}"
            )

    for case in fixture.get("work105DecisionEvidenceCases", []):
        unresolved = _work105_predecessor_unresolved_links(
            **_work105_decision_evidence_fixture_inputs(root, case["mutation"])
        )
        if len(unresolved) != case["expectedUnresolvedCount"]:
            failures.append(
                f"WORK-105 decision evidence {case['name']}: expected unresolved "
                f"count {case['expectedUnresolvedCount']}, actual {len(unresolved)}"
            )

    for mutation in AGENT_ROSTER_CUTOVER_MUTATIONS:
        admitted = finite_agent_roster_cutover_paths(
            **_agent_roster_cutover_fixture_inputs(mutation)
        )
        expected_count = len(AGENT_ROSTER_CUTOVER_PATHS) if mutation == "exact" else 0
        if len(admitted) != expected_count:
            failures.append(
                f"agent roster cutover {mutation}: expected admitted count "
                f"{expected_count}, actual {len(admitted)}"
            )

    invalid_agent_contract_blobs = {
        "malformed": b"{",
        "non-object": b"[]",
        "duplicate-key": b'{"state":"one","state":"two"}',
    }
    for mutation in AGENT_ROSTER_CONTRACT_BLOB_MUTATIONS:
        try:
            if mutation == "missing":
                _agent_contracts_from_blob_maps(root, {}, {})
            else:
                _agent_contract_blob_from_bytes(
                    invalid_agent_contract_blobs[mutation],
                    AGENT_ROSTER_ADMISSION_CONTRACT_PATH,
                )
        except InvocationError:
            continue
        failures.append(f"agent contract blob {mutation}: mutation was accepted")

    for case in fixture.get("comparisonCases", []):
        base = _document(*case["base"])
        proposed = _document(*case["proposed"])
        actual = _rule_ids(
            compare_lifecycle(
                registry,
                {base.path: base},
                {proposed.path: proposed},
                base_mode="explicit-ref",
            )
        )
        if actual != case["expectedRuleIds"]:
            failures.append(
                f"comparison {case['name']}: expected {case['expectedRuleIds']}, actual {actual}"
            )

    for case in fixture.get("admissionCases", []):
        documents = [_document(*item) for item in case["documents"]]
        operation = case.get("operation", "create")
        if operation == "create":
            diagnostics = compare_lifecycle(
                registry,
                {},
                {item.path: item for item in documents},
                base_mode="staged",
            )
        elif operation == "delete":
            diagnostics = compare_lifecycle(
                registry,
                {item.path: item for item in documents},
                {},
                base_mode="staged",
            )
        elif operation == "rename":
            base, proposed = documents
            diagnostics = compare_lifecycle(
                registry,
                {base.path: base},
                {proposed.path: proposed},
                renames=(LifecycleRename(base.path, proposed.path),),
                base_mode="staged",
            )
        else:
            failures.append(f"admission {case['name']}: unknown operation")
            continue
        actual = _rule_ids(diagnostics)
        if actual != case["expectedRuleIds"]:
            failures.append(
                f"admission {case['name']}: expected {case['expectedRuleIds']}, actual {actual}"
            )

    for case in fixture.get("gitCases", []):
        with tempfile.TemporaryDirectory(prefix="document-lifecycle-") as directory:
            repo = Path(directory)
            _init_fixture_repo(repo)
            try:
                actual_exit, actual_rules = _git_case(
                    case["name"], repo, evidence_registry, root
                )
            except (InvocationError, OSError, ValueError) as exc:
                failures.append(f"git {case['name']}: unexpected error {exc}")
                continue
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"git {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )
        if actual_rules != case["expectedRuleIds"]:
            failures.append(
                f"git {case['name']}: expected rules {case['expectedRuleIds']}, actual {actual_rules}"
            )

    for case in fixture.get("argumentCases", []):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                actual_exit = main(["--root", str(root), *case["argv"]])
            except SystemExit as exc:
                actual_exit = int(exc.code) if isinstance(exc.code, int) else 2
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"argument {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )
        error_line = stderr.getvalue().strip()
        if case["expectedBaseMode"] == "argparse":
            if (
                not error_line.startswith("usage:")
                or "invalid choice" not in error_line
            ):
                failures.append(
                    f"argument {case['name']}: argparse diagnostic differs"
                )
        elif (
            not error_line.startswith("FAIL LIFECYCLE-BASE . ")
            or f"base_mode={json.dumps(case['expectedBaseMode'])}" not in error_line
            or "profile=" not in error_line
            or "expected=" not in error_line
            or "observed=" not in error_line
            or "evidence_gap=" not in error_line
        ):
            failures.append(
                f"argument {case['name']}: base diagnostic envelope differs"
            )

    for case in fixture.get("includePathCases", []):
        try:
            paths = _normalize_include_paths(registry, case["values"])
            if case["name"] == "missing-blob":
                with tempfile.TemporaryDirectory(
                    prefix="document-lifecycle-include-"
                ) as directory:
                    repo = Path(directory)
                    _init_fixture_repo(repo)
                    _commit_fixture(repo, "base")
                    _evaluate_comparison(
                        repo,
                        registry,
                        mode="staged",
                        include_paths=paths,
                    )
            actual_exit = 0
        except (InvocationError, DocumentContractError, OSError, ValueError):
            actual_exit = 2
        if actual_exit != case["expectedExit"]:
            failures.append(
                f"include {case['name']}: expected exit {case['expectedExit']}, actual {actual_exit}"
            )

    snapshot = fixture["snapshotCase"]
    diagnostics = _evaluate_snapshot(root, registry, ())
    actual_rules = _rule_ids(diagnostics)
    if (
        _exit_code(diagnostics) != snapshot["expectedExit"]
        or actual_rules != snapshot["expectedRuleIds"]
        or sum(item.severity == "DEFER" for item in diagnostics) != 1
    ):
        failures.append(
            f"snapshot {snapshot['name']}: expected one DEFER only, actual {actual_rules}"
        )
    if any(item.rule_id == "LIFECYCLE-EVIDENCE" for item in diagnostics):
        failures.append("snapshot evaluated DSLC-004 evidence predicates")
    return failures


def _execute(root: Path, args: argparse.Namespace) -> int:
    _verify_repository_root(root)
    if args.mode == "staged":
        assert_staged_authority_matches_worktree(root, CURRENT_REGISTRY_PATH)
    registry = load_registry(root)
    include_paths = _normalize_include_paths(registry, args.include_path)
    if args.mode == "snapshot":
        diagnostics = _evaluate_snapshot(root, registry, include_paths)
    else:
        comparison_mode = "staged" if args.mode == "strict" else args.mode
        diagnostics = _evaluate_comparison(
            root,
            registry,
            mode=comparison_mode,
            from_ref=args.from_ref,
            base_ref=args.base_ref,
            to_ref=args.to_ref,
            include_paths=include_paths,
        )
    for diagnostic in sorted(diagnostics, key=lifecycle_diagnostic_sort_key):
        print(_format_diagnostic(diagnostic))
    result = _exit_code(diagnostics)
    if result == 0 and not diagnostics:
        print(f"PASS lifecycle validation mode={args.mode}")
    return result


def main(argv: Sequence[str] | None = None) -> int:
    error_mode = "unknown"
    try:
        args = _parser().parse_args(argv)
        if args.mode in {"strict", "staged", "ci", "explicit-ref", "snapshot"}:
            error_mode = args.mode
        _validate_arguments(args)
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise InvocationError("--root must be an existing directory")
        with _git_environment_scope():
            return _execute(root, args)
    except (
        AuthorityError,
        InvocationError,
        DocumentContractError,
        OSError,
        ValueError,
    ) as exc:
        diagnostic = LifecycleDiagnostic(
            severity="FAIL",
            rule_id="LIFECYCLE-BASE",
            path=PurePosixPath("."),
            profile="",
            expected_transition=(
                "valid invocation, unique commit refs, and one comparison base"
            ),
            observed_transition=str(exc),
            base_mode=error_mode,  # type: ignore[arg-type]
            evidence_gap="argument or Git provenance",
        )
        print(_format_diagnostic(diagnostic), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
