#!/usr/bin/env python3
"""Validate registry-owned document lifecycle events against deterministic Git bases."""

from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
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
    ROOT_FILES,
    TARGET_ROOTS,
    DocumentContractError,
    DocumentProfile,
    Registry,
    Route,
    classify_path,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
)
from document_lifecycle import (
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
    MIG0004_TERMINAL_SOURCE_COMMIT,
    MIGRATION_DOCUMENT_MAX_BYTES,
    parse_pinned_migration_control,
    read_staged_blob_bounded,
    validate_archive_immutability,
)
from archive_recovery import (
    ArchiveContractError,
    WORK107_LEGACY_ARCHIVE_COMMIT,
    WORK107_MIGRATION_PATH,
    WP004C_SEALED_TARGET_COMMIT,
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


RETIRED_REGISTRY_PATH = PurePosixPath("docs/99.templates/registry.json")
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
WORK105_BASE_REGISTRY_PROJECTION_SHA256 = "ef2e31327be14a3117898a8c0eb661f022fd96cac4e1d3f9362925e189c63daf"  # pragma: allowlist secret
WORK105_PROPOSED_REGISTRY_PROJECTION_SHA256 = "17d49aa94403200ea9795d8c14f3fb9137e4f266ebb91e0449b937eecea6ff50"  # pragma: allowlist secret
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
WORK105_ADR0023_BASE_SHA256 = "fadbd95c581a0874797666e200f283d0f5fdc6c103643cc653e387062adbe53a"  # pragma: allowlist secret
WORK105_ADR0023_PROPOSED_SHA256 = "717714ce153cbd75ca5a77beb42a24cd1b146f25b1112d492e30d9fd214348d5"  # pragma: allowlist secret
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
WORK107_MIGRATION_DOCUMENT_SHA256 = "7049f8b94bdb80566ad94be5d9e9e899d7d06e1b9d31191ad769cd905717de5e"  # pragma: allowlist secret
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
    "docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md"
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
WORK054_WP002_DECISION_SHA256 = "b35d625a98e1c1d3089d20b8ea56669dbbbee32934a21112a8a29e70744ed5c4"  # pragma: allowlist secret
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
WORK054_WP003_MIGRATION_SHA256 = "51fe8d35febac457e562f997a711ce152a98cda67b3aec2ccd8ed08bd3ac3d42"  # pragma: allowlist secret
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
        "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
    ),
    *WORK054_WP004A_OWNER_PATHS,
)
WORK054_WP004B_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/0004-document-authority-convergence.md"
)
WORK054_WP004B_REQUIREMENT_PROFILES = frozenset(
    {"sdlc/prd", "sdlc/srs", "sdlc/interface"}
)
WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE = "sdlc/requirement-package"
WORK054_WP004B_ROUTER_PATTERN = re.compile(
    r"^docs/03\.specs/[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/README\.md$"
)
WORK054_WP004B_TASK_PATTERN = re.compile(
    r"^docs/03\.specs/[0-9]{4}-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"tasks/tsk-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_SPEC_PATTERN = re.compile(
    r"^docs/03\.specs/(?P<spec>[0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"spec\.md$"
)
WORK054_WP004B_PLAN_PATTERN = re.compile(
    r"^docs/03\.specs/(?P<spec>[0-9]{4})-[a-z][a-z0-9]*(?:-[a-z0-9]+)*/"
    r"plan\.md$"
)
WORK054_WP004B_REQUIREMENT_PATTERN = re.compile(
    r"^docs/01\.requirements/(?P<identity>[0-9]{4})-[a-z0-9]+"
    r"(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_AD_PATTERN = re.compile(
    r"^docs/02\.architecture/descriptions/(?P<identity>[0-9]{4})-"
    r"[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
WORK054_WP004B_ROUTER_TASK_LINK = re.compile(
    r"^- \[`(?P<artifact>TSK-[0-9]{4}-[0-9]{4})` — "
    r"`(?P<legacy>[^`]+)`\]\((?P<path>tasks/tsk-[0-9]{4}-[a-z0-9]+"
    r"(?:-[a-z0-9]+)*\.md)\)$"
)
WORK054_WP004B_TASK_STATUSES = MappingProxyType(
    {
        "done": "done",
        "complete": "done",
        "completed": "done",
        "archived": "done",
        "transferred": "done",
        "in progress": "in-progress",
        "in-progress": "in-progress",
        "queued": "queued",
        "pending": "queued",
        "blocked": "blocked",
        "cancelled": "cancelled",
        "canceled": "cancelled",
    }
)


@dataclass(frozen=True)
class _Work054Wp004bAdmission:
    paths: frozenset[PurePosixPath]
    diagnostics: frozenset[tuple[PurePosixPath, str, str, str]]


_EMPTY_WORK054_WP004B_ADMISSION = _Work054Wp004bAdmission(frozenset(), frozenset())


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


def _wp004b_classification_registry(
    current_registry: Registry,
    projected_registry: Registry,
    *,
    authority_converged: bool,
) -> Registry:
    """Classify Requirement Packages only in trees carrying sealed MIG-0004."""

    if not authority_converged:
        return projected_registry
    current = {profile.profile_id: profile for profile in current_registry.profiles}
    projected_ids = {profile.profile_id for profile in projected_registry.profiles}
    requirement = current.get(WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE)
    if (
        requirement is None
        or WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE in projected_ids
        or not WORK054_WP004B_REQUIREMENT_PROFILES <= projected_ids
    ):
        return projected_registry
    profiles = tuple(
        profile
        for profile in projected_registry.profiles
        if profile.profile_id not in WORK054_WP004B_REQUIREMENT_PROFILES
    ) + (requirement,)
    return replace(projected_registry, profiles=profiles)


def _work054_wp004b_document(
    root: Path,
    registry: Registry,
    path: PurePosixPath,
    oid: str | None,
    *,
    profile_id: str,
    status: str | None,
    artifact_id: str | None,
    blob_reader: Callable[[str], bytes] | None = None,
) -> LifecycleDocument | None:
    if oid is None:
        return None
    try:
        raw = (blob_reader or (lambda value: _blob_bytes(root, value)))(oid)
        text = raw.decode("utf-8")
        document = document_from_text(registry, path, text)
    except (InvocationError, UnicodeDecodeError, DocumentContractError):
        return None
    if (
        document.profile_id != profile_id
        or document.status != status
        or document.state_issue is not None
    ):
        return None
    if artifact_id is None:
        return document if not text.startswith("---\n") else None
    return (
        document
        if _work054_wp002_frontmatter_value(raw, "artifact_id") == artifact_id
        else None
    )


def _work054_wp004b_table_cells(line: str) -> tuple[str, ...] | None:
    if not line.startswith("|") or not line.endswith("|"):
        return None
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    in_code = False
    for character in line[1:-1]:
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            current.append(character)
            escaped = True
        elif character == "`":
            current.append(character)
            in_code = not in_code
        elif character == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    if escaped or in_code:
        return None
    cells.append("".join(current).strip())
    return tuple(cells)


def _work054_wp004b_task_table(
    raw: bytes,
) -> tuple[str, str, tuple[tuple[str, tuple[str, ...]], ...]] | None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    marker = "\n## Task Table\n"
    if text.count(marker) != 1:
        return None
    section = re.split(r"\n#{2,6} ", text.partition(marker)[2], maxsplit=1)[0]
    blocks: list[list[str]] = []
    block: list[str] = []
    for line in section.splitlines():
        if line.startswith("|"):
            block.append(line)
        elif block:
            blocks.append(block)
            block = []
    if block:
        blocks.append(block)

    candidates: list[tuple[str, str, tuple[tuple[str, tuple[str, ...]], ...]]] = []
    for lines in blocks:
        if len(lines) < 3:
            continue
        header = _work054_wp004b_table_cells(lines[0])
        separator = _work054_wp004b_table_cells(lines[1])
        if (
            header is None
            or separator is None
            or len(header) != len(separator)
            or any(re.fullmatch(r":?-{3,}:?", cell) is None for cell in separator)
            or "id" not in {cell.lower() for cell in header}
            or "status" not in {cell.lower() for cell in header}
        ):
            continue
        rows: list[tuple[str, tuple[str, ...]]] = []
        for line in lines[2:]:
            cells = _work054_wp004b_table_cells(line)
            if cells is None or len(cells) != len(header):
                rows = []
                break
            rows.append((line, cells))
        if rows:
            candidates.append((lines[0], lines[1], tuple(rows)))
    return candidates[0] if len(candidates) == 1 else None


def _work054_wp004b_task_slug(legacy_id: str) -> str | None:
    slug = re.sub(r"[^a-z0-9]+", "-", legacy_id.lower()).strip("-")
    return slug if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) else None


def _work054_wp004b_legacy_id(raw: str) -> str:
    link = re.fullmatch(r"\[(?P<label>[A-Za-z0-9-]+)\]\([^)]*\)", raw)
    return link.group("label") if link is not None else raw


def _work054_wp004b_task_title(raw: str) -> str:
    return raw.replace("\\|", "|").replace("`", "").strip()


def _work054_wp004b_render_task(
    *,
    artifact_id: str,
    title: str,
    status: str,
    owner: str,
    updated: str,
    legacy_id: str,
    header_line: str,
    separator_line: str,
    row_line: str,
) -> bytes:
    heading_title = title.rstrip(".")
    quoted_title = json.dumps(f"{artifact_id}: {title}", ensure_ascii=False)
    lifecycle_trace = ""
    if status != "done":
        lifecycle_trace = (
            "\n### Lifecycle Traceability\n\n"
            "| Criterion / work item | Result | Evidence |\n"
            "| --- | --- | --- |\n"
            f"| N/A — legacy work item `{legacy_id}` | Preserved legacy status; "
            f"current Task is `{status}`. | Row-specific result and evidence remain "
            "in the Task Table above. |\n\n"
        )
    return (
        f"---\n"
        f"title: {quoted_title}\n"
        f"type: sdlc/task\n"
        f"status: {status}\n"
        f"owner: {owner}\n"
        f"updated: {updated}\n"
        f'artifact_id: "{artifact_id}"\n'
        f"---\n\n"
        f"# {artifact_id}: {heading_title}\n\n"
        f"## Overview\n\n"
        f"Append-only Task record for legacy work item `{legacy_id}` from the package's\n"
        f"decomposed monolithic ledger. The exact row below preserves its criterion,\n"
        f"dependency, owner, result, and evidence.\n\n"
        f"## Inputs\n\n"
        f"- [Package router](../README.md)\n"
        f"- [Owning Spec](../spec.md)\n"
        f"- [Owning Plan](../plan.md)\n"
        f"- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)\n\n"
        f"## Task Table\n\n"
        f"{header_line}\n"
        f"{separator_line}\n"
        f"{row_line}\n\n"
        f"## Approval and Safety Boundaries\n\n"
        f"The shared approval, safety, and rollback contract is preserved once in the\n"
        f"[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This\n"
        f"record does not broaden that contract.\n\n"
        f"## Verification Summary\n\n"
        f"The row-specific validation/result/evidence is preserved verbatim above. The\n"
        f"shared verification context is in the\n"
        f"[owning Plan](../plan.md#legacy-task-verification-evidence).\n\n"
        f"## Traceability\n\n"
        f"- Stable Task: `{artifact_id}`\n"
        f"- Legacy work item: `{legacy_id}`\n"
        f"{lifecycle_trace}"
        f"- Package inventory: [README](../README.md#task-records)\n"
        f"- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)\n"
    ).encode("utf-8")


def _work054_wp004b_admission(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
    base_registry: Registry,
    proposed_registry: Registry,
) -> _Work054Wp004bAdmission:
    """Admit only the cutover projected by sealed MIG-0004 authority."""

    if mode not in {"staged", "ci"} or base_commit != MIG0004_TERMINAL_SOURCE_COMMIT:
        return _EMPTY_WORK054_WP004B_ADMISSION
    blob_cache: dict[str, bytes] = {}

    def read_blob(oid: str) -> bytes:
        if oid not in blob_cache:
            blob_cache[oid] = _blob_bytes(root, oid)
        return blob_cache[oid]

    migration_oid = proposed_blobs.get(WORK054_WP004B_MIGRATION_PATH)
    if migration_oid is None or WORK054_WP004B_MIGRATION_PATH in base_blobs:
        return _EMPTY_WORK054_WP004B_ADMISSION
    try:
        migration_bytes = read_blob(migration_oid)
        rows = parse_pinned_migration_control(
            WORK054_WP004B_MIGRATION_PATH.as_posix(),
            migration_bytes,
        )
    except (ArchiveContractError, InvocationError):
        return _EMPTY_WORK054_WP004B_ADMISSION

    migration_document = _work054_wp004b_document(
        root,
        proposed_registry,
        WORK054_WP004B_MIGRATION_PATH,
        migration_oid,
        profile_id="content/archive-migration",
        status="sealed",
        artifact_id="MIG-0004",
        blob_reader=read_blob,
    )
    if migration_document is None:
        return _EMPTY_WORK054_WP004B_ADMISSION

    consumed: set[PurePosixPath] = {WORK054_WP004B_MIGRATION_PATH}
    allowed_diagnostics: set[tuple[PurePosixPath, str, str, str]] = {
        (
            WORK054_WP004B_MIGRATION_PATH,
            "LIFECYCLE-CREATE",
            "content/archive-migration",
            "absent -> sealed",
        )
    }
    task_packages: set[PurePosixPath] = set()
    requirement_paths: set[PurePosixPath] = set()
    architecture_paths: set[PurePosixPath] = set()
    agent_replacements: set[PurePosixPath] = set()
    expected_task_paths: set[PurePosixPath] = set()
    expected_task_labels: dict[PurePosixPath, tuple[str, str]] = {}
    for row in rows:
        legacy_raw = row.get("legacy_path")
        source_commit = row.get("source_commit")
        source_blob = row.get("source_blob")
        action = row.get("action")
        if (
            not isinstance(legacy_raw, str)
            or not isinstance(source_blob, str)
            or source_commit != base_commit
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        legacy = PurePosixPath(legacy_raw)
        if base_blobs.get(legacy) != source_blob:
            return _EMPTY_WORK054_WP004B_ADMISSION
        target_raw = row.get("stable_path") or row.get("replacement")
        target = PurePosixPath(target_raw) if isinstance(target_raw, str) else None
        if action == "replaced" and target == legacy:
            proposed_oid = proposed_blobs.get(legacy)
            if proposed_oid is None or proposed_oid == source_blob:
                return _EMPTY_WORK054_WP004B_ADMISSION
            requirement_match = WORK054_WP004B_REQUIREMENT_PATTERN.fullmatch(
                legacy.as_posix()
            )
            if requirement_match is None:
                return _EMPTY_WORK054_WP004B_ADMISSION
            identity = requirement_match.group("identity")
            base_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            expected_status = {
                "active": "active",
                "done": "superseded",
            }.get(base_status or "")
            if (
                expected_status is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/prd",
                    status=base_status,
                    artifact_id=f"PRD-{identity}",
                    blob_reader=read_blob,
                )
                is None
                or _work054_wp004b_document(
                    root,
                    proposed_registry,
                    legacy,
                    proposed_oid,
                    profile_id=WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE,
                    status=expected_status,
                    artifact_id=f"REQ-{identity}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            target_bytes = read_blob(proposed_oid)
            if expected_status == "superseded" and (
                _work054_wp002_frontmatter_value(target_bytes, "superseded_by")
                != "REQ-0008"
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            if identity == "0008":
                supersedes = _work054_wp002_frontmatter_value(
                    target_bytes, "supersedes"
                )
                if supersedes is None or set(
                    re.findall(r"REQ-[0-9]{4}", supersedes)
                ) != {"REQ-0005", "REQ-0006"}:
                    return _EMPTY_WORK054_WP004B_ADMISSION
            requirement_paths.add(legacy)
            consumed.add(legacy)
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-STATE",
                    WORK054_WP004B_REQUIREMENT_PACKAGE_PROFILE,
                    "sdlc/prd -> sdlc/requirement-package; "
                    "current registry classification unavailable",
                )
            )
            continue
        if target is None or target not in proposed_blobs:
            return _EMPTY_WORK054_WP004B_ADMISSION
        if legacy in proposed_blobs:
            return _EMPTY_WORK054_WP004B_ADMISSION
        if action == "moved":
            identity = row.get("artifact_id")
            match = WORK054_WP004B_AD_PATTERN.fullmatch(target.as_posix())
            base_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            if (
                match is None
                or identity != f"AD-{match.group('identity')}"
                or base_status is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/ad",
                    status=base_status,
                    artifact_id=str(identity),
                    blob_reader=read_blob,
                )
                is None
                or _work054_wp004b_document(
                    root,
                    proposed_registry,
                    target,
                    proposed_blobs[target],
                    profile_id="sdlc/ad",
                    status=base_status,
                    artifact_id=str(identity),
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            architecture_paths.add(target)
            consumed.update((legacy, target))
            if source_blob == proposed_blobs[target]:
                allowed_diagnostics.add(
                    (
                        target,
                        "LIFECYCLE-RENAME",
                        "sdlc/ad",
                        f"{legacy.as_posix()} -> {target.as_posix()}",
                    )
                )
            else:
                allowed_diagnostics.update(
                    {
                        (
                            legacy,
                            "LIFECYCLE-DELETE",
                            "sdlc/ad",
                            f"{base_status} -> absent",
                        ),
                        (
                            target,
                            "LIFECYCLE-CREATE",
                            "sdlc/ad",
                            f"absent -> {base_status}",
                        ),
                    }
                )
            continue
        if action == "replaced" and legacy.name == "tasks.md":
            if target.name != "README.md" or target in base_blobs:
                return _EMPTY_WORK054_WP004B_ADMISSION
            source_bytes = read_blob(source_blob)
            source_table = _work054_wp004b_task_table(source_bytes)
            source_status = _work054_wp002_frontmatter_value(source_bytes, "status")
            source_owner = _work054_wp002_frontmatter_value(source_bytes, "owner")
            source_updated = _work054_wp002_frontmatter_value(source_bytes, "updated")
            spec_number = legacy.parent.name[:4]
            if (
                source_table is None
                or source_status is None
                or source_owner is None
                or source_updated is None
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/task",
                    status=source_status,
                    artifact_id=f"TASK-{spec_number}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            header_line, separator_line, source_rows = source_table
            headers = _work054_wp004b_table_cells(header_line)
            assert headers is not None
            lowered_headers = tuple(cell.lower() for cell in headers)
            try:
                status_index = lowered_headers.index("status")
            except ValueError:
                return _EMPTY_WORK054_WP004B_ADMISSION
            owner_index = (
                lowered_headers.index("owner") if "owner" in lowered_headers else None
            )
            for sequence, (row_line, cells) in enumerate(source_rows, 1):
                legacy_id = _work054_wp004b_legacy_id(cells[0])
                slug = _work054_wp004b_task_slug(legacy_id)
                status = WORK054_WP004B_TASK_STATUSES.get(
                    cells[status_index].strip().lower()
                )
                row_owner = (
                    cells[owner_index].strip()
                    if owner_index is not None
                    else source_owner
                )
                artifact_id = f"TSK-{spec_number}-{sequence:04d}"
                if slug is None or status is None or not row_owner:
                    return _EMPTY_WORK054_WP004B_ADMISSION
                task_path = legacy.parent / "tasks" / f"tsk-{sequence:04d}-{slug}.md"
                task_oid = proposed_blobs.get(task_path)
                task_bytes = read_blob(task_oid) if task_oid is not None else b""
                task_table = _work054_wp004b_task_table(task_bytes)
                if task_table is None:
                    return _EMPTY_WORK054_WP004B_ADMISSION
                task_header, task_separator, task_rows = task_table
                target_cells = task_rows[0][1] if len(task_rows) == 1 else ()
                if (
                    task_header != header_line
                    or task_separator != separator_line
                    or len(task_rows) != 1
                    or len(target_cells) != len(cells)
                    or _work054_wp004b_legacy_id(target_cells[0]) != legacy_id
                    or target_cells[1] != cells[1]
                    or (
                        owner_index is not None
                        and target_cells[owner_index] != cells[owner_index]
                    )
                    or target_cells[status_index] != cells[status_index]
                    or any(not cell for cell in target_cells)
                ):
                    return _EMPTY_WORK054_WP004B_ADMISSION
                projected_row = task_rows[0][0]
                expected = _work054_wp004b_render_task(
                    artifact_id=artifact_id,
                    title=_work054_wp004b_task_title(cells[1]),
                    status=status,
                    owner=source_owner,
                    updated=source_updated,
                    legacy_id=legacy_id,
                    header_line=header_line,
                    separator_line=separator_line,
                    row_line=projected_row,
                )
                if (
                    task_oid is None
                    or task_bytes != expected
                    or _work054_wp004b_document(
                        root,
                        proposed_registry,
                        task_path,
                        task_oid,
                        profile_id="sdlc/task",
                        status=status,
                        artifact_id=artifact_id,
                        blob_reader=read_blob,
                    )
                    is None
                ):
                    return _EMPTY_WORK054_WP004B_ADMISSION
                expected_task_paths.add(task_path)
                expected_task_labels[task_path] = (artifact_id, legacy_id)
                allowed_diagnostics.add(
                    (
                        task_path,
                        "LIFECYCLE-CREATE",
                        "sdlc/task",
                        f"absent -> {status}",
                    )
                )
            task_packages.add(legacy.parent)
            consumed.update((legacy, target))
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-DELETE",
                    "sdlc/task",
                    f"{source_status} -> absent",
                )
            )
            continue
        if action == "merged" and legacy.name == "agent-design.md":
            source_status = _work054_wp002_frontmatter_value(
                read_blob(source_blob), "status"
            )
            spec_number = legacy.parent.name[:4]
            target_oid = proposed_blobs.get(target)
            if (
                source_status is None
                or target.name != "spec.md"
                or target_oid is None
                or target_oid == base_blobs.get(target)
                or _work054_wp004b_document(
                    root,
                    base_registry,
                    legacy,
                    source_blob,
                    profile_id="sdlc/agent-design",
                    status=source_status,
                    artifact_id=f"AGENT-DESIGN-{spec_number}",
                    blob_reader=read_blob,
                )
                is None
            ):
                return _EMPTY_WORK054_WP004B_ADMISSION
            agent_replacements.add(target)
            consumed.update((legacy, target))
            allowed_diagnostics.add(
                (
                    legacy,
                    "LIFECYCLE-DELETE",
                    "sdlc/agent-design",
                    f"{source_status} -> absent",
                )
            )
            continue
        return _EMPTY_WORK054_WP004B_ADMISSION

    routers = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_ROUTER_PATTERN.fullmatch(path.as_posix())
    }
    tasks = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_TASK_PATTERN.fullmatch(path.as_posix())
    }
    specs = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_SPEC_PATTERN.fullmatch(path.as_posix())
    }
    plans = {
        path
        for path in proposed_blobs
        if WORK054_WP004B_PLAN_PATTERN.fullmatch(path.as_posix())
    }
    spec_packages = {path.parent for path in specs}
    task_owners = {path.parent.parent for path in tasks}
    if (
        tasks != expected_task_paths
        or any(path in base_blobs for path in routers | tasks)
        or task_owners != task_packages
        or {path.parent for path in routers} != spec_packages
        or not task_packages <= spec_packages
        or {path.parent for path in plans} - spec_packages
        or {
            path
            for path in proposed_blobs
            if WORK054_WP004B_REQUIREMENT_PATTERN.fullmatch(path.as_posix())
        }
        != requirement_paths
        or {
            path
            for path in proposed_blobs
            if WORK054_WP004B_AD_PATTERN.fullmatch(path.as_posix())
        }
        != architecture_paths
    ):
        return _EMPTY_WORK054_WP004B_ADMISSION

    for spec_path in specs:
        spec_match = WORK054_WP004B_SPEC_PATTERN.fullmatch(spec_path.as_posix())
        assert spec_match is not None
        base_oid = base_blobs.get(spec_path)
        base_status = (
            _work054_wp002_frontmatter_value(read_blob(base_oid), "status")
            if base_oid is not None
            else None
        )
        if (
            base_oid is None
            or base_status is None
            or _work054_wp004b_document(
                root,
                proposed_registry,
                spec_path,
                proposed_blobs[spec_path],
                profile_id="sdlc/spec",
                status=base_status,
                artifact_id=f"SPEC-{spec_match.group('spec')}",
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        consumed.add(spec_path)

    for plan_path in plans:
        plan_match = WORK054_WP004B_PLAN_PATTERN.fullmatch(plan_path.as_posix())
        assert plan_match is not None
        base_oid = base_blobs.get(plan_path)
        base_status = (
            _work054_wp002_frontmatter_value(read_blob(base_oid), "status")
            if base_oid is not None
            else None
        )
        if (
            base_oid is None
            or base_status is None
            or _work054_wp004b_document(
                root,
                proposed_registry,
                plan_path,
                proposed_blobs[plan_path],
                profile_id="sdlc/plan",
                status=base_status,
                artifact_id=f"PLAN-{plan_match.group('spec')}",
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        consumed.add(plan_path)

    if not agent_replacements <= specs:
        return _EMPTY_WORK054_WP004B_ADMISSION

    for router in routers:
        router_oid = proposed_blobs[router]
        if (
            _work054_wp004b_document(
                root,
                proposed_registry,
                router,
                router_oid,
                profile_id="readme/collection-index",
                status=None,
                artifact_id=None,
                blob_reader=read_blob,
            )
            is None
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        router_text = read_blob(router_oid).decode("utf-8")
        marker = "\n## Task Records\n"
        if router_text.count(marker) != 1 or router_text.count("(spec.md)") != 1:
            return _EMPTY_WORK054_WP004B_ADMISSION
        package = router.parent
        plan_exists = package / "plan.md" in plans
        if router_text.count("(plan.md)") != int(plan_exists):
            return _EMPTY_WORK054_WP004B_ADMISSION
        section = router_text.partition(marker)[2].partition("\n## ")[0]
        links: dict[PurePosixPath, tuple[str, str]] = {}
        for line in section.splitlines():
            match = WORK054_WP004B_ROUTER_TASK_LINK.fullmatch(line)
            if match is None:
                continue
            task_path = package / match.group("path")
            if task_path in links:
                return _EMPTY_WORK054_WP004B_ADMISSION
            links[task_path] = (match.group("artifact"), match.group("legacy"))
        actual = {path for path in tasks if path.parent.parent == package}
        if (
            set(links) != actual
            or any(links[path] != expected_task_labels[path] for path in actual)
            or router_text.count("](tasks/tsk-") != len(actual)
        ):
            return _EMPTY_WORK054_WP004B_ADMISSION
        allowed_diagnostics.add(
            (
                router,
                "LIFECYCLE-CREATE",
                "readme/collection-index",
                "absent -> not-applicable",
            )
        )
    consumed.update(routers)
    consumed.update(tasks)
    return _Work054Wp004bAdmission(frozenset(consumed), frozenset(allowed_diagnostics))


def finite_work054_wp004b_document_authority_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Return paths only after exact WP-004B tree-object projection succeeds."""

    try:
        current_registry = load_registry(root)
        base_registry = _classification_registry(
            current_registry,
            _registry_blob(
                root,
                _tree_blob_oid(root, base_commit, RETIRED_REGISTRY_PATH),
            ),
        )
        proposed_registry = current_registry
    except (DocumentContractError, InvocationError):
        return frozenset()
    return _work054_wp004b_admission(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
        base_registry=base_registry,
        proposed_registry=proposed_registry,
    ).paths


def _git_blob_oid(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324 - Git identity


def _work107_without_outer_artifact_id(
    content: bytes, expected_artifact_id: str
) -> bytes | None:
    expected = f'artifact_id: "{expected_artifact_id}"'.encode("ascii")
    lines = content.splitlines(keepends=True)
    matches = [
        index for index, line in enumerate(lines) if line.rstrip(b"\r\n") == expected
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
    if hashlib.sha256(migration_bytes).hexdigest() != WORK107_MIGRATION_DOCUMENT_SHA256:
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
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
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
    if not all(isinstance(row, dict) for row in loaded):
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


def _wp004c_mig0004_paths(
    *,
    root: Path,
    mode: str,
    base_commit: str,
    base_blobs: Mapping[PurePosixPath, str],
    proposed_blobs: Mapping[PurePosixPath, str],
) -> frozenset[PurePosixPath]:
    """Admit only source-pinned WP-004C Stage99 and Spec0054 cutover rows."""

    if mode not in {"staged", "ci"}:
        return frozenset()
    migration_oid = proposed_blobs.get(WORK054_WP004B_MIGRATION_PATH)
    if migration_oid is None:
        return frozenset()
    try:
        rows = parse_pinned_migration_control(
            WORK054_WP004B_MIGRATION_PATH.as_posix(),
            _blob_bytes(root, migration_oid),
        )
    except (ArchiveContractError, InvocationError):
        return frozenset()

    cutover_rows = [row for row in rows if row.get("source_commit") == base_commit]
    task_legacy = PurePosixPath(
        "docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks.md"
    )
    stage99_rows = [
        row
        for row in cutover_rows
        if isinstance(row.get("legacy_path"), str)
        and str(row["legacy_path"]).startswith("docs/99.templates/")
        and _approved_markdown(PurePosixPath(str(row["legacy_path"])))
    ]
    task_rows = [
        row for row in cutover_rows if row.get("legacy_path") == task_legacy.as_posix()
    ]
    if len(task_rows) != 1 or not stage99_rows:
        return frozenset()

    consumed: set[PurePosixPath] = set()
    stage99_legacy: set[PurePosixPath] = set()
    for row in stage99_rows:
        legacy_raw = row.get("legacy_path")
        source_blob = row.get("source_blob")
        digest = row.get("content_sha256")
        action = row.get("action")
        target_raw = (
            row.get("stable_path") if action == "moved" else row.get("replacement")
        )
        if not all(
            isinstance(value, str)
            for value in (legacy_raw, source_blob, digest, target_raw)
        ):
            return frozenset()
        legacy = PurePosixPath(legacy_raw)
        target = PurePosixPath(target_raw)
        if (
            legacy in stage99_legacy
            or base_blobs.get(legacy) != source_blob
            or hashlib.sha256(_blob_bytes(root, source_blob)).hexdigest() != digest
            or legacy in proposed_blobs
            or target not in proposed_blobs
            or action not in {"moved", "replaced"}
            or (action == "moved" and proposed_blobs[target] != source_blob)
        ):
            return frozenset()
        stage99_legacy.add(legacy)
        consumed.update((legacy, target))

    deleted_stage99 = {
        path
        for path in base_blobs
        if path.as_posix().startswith("docs/99.templates/")
        and path not in proposed_blobs
    }
    if stage99_legacy != deleted_stage99:
        return frozenset()

    task_row = task_rows[0]
    if (
        task_row.get("action") != "replaced"
        or task_row.get("stable_path") is not None
        or task_row.get("replacement") != (task_legacy.parent / "README.md").as_posix()
        or not isinstance(task_row.get("source_blob"), str)
        or not isinstance(task_row.get("content_sha256"), str)
    ):
        return frozenset()
    source_blob = str(task_row["source_blob"])
    source = _blob_bytes(root, source_blob)
    if (
        base_blobs.get(task_legacy) != source_blob
        or hashlib.sha256(source).hexdigest() != task_row["content_sha256"]
    ):
        return frozenset()
    source_table = _work054_wp004b_task_table(source)
    source_status = _work054_wp002_frontmatter_value(source, "status")
    source_owner = _work054_wp002_frontmatter_value(source, "owner")
    source_updated = _work054_wp002_frontmatter_value(source, "updated")
    readme_path = task_legacy.parent / "README.md"
    readme_oid = proposed_blobs.get(readme_path)
    if (
        source_table is None
        or source_status is None
        or source_owner is None
        or source_updated is None
        or readme_oid is None
    ):
        return frozenset()
    header_line, separator_line, source_entries = source_table
    headers = _work054_wp004b_task_table(source)
    assert headers is not None
    parsed_header = _work054_wp004b_table_cells(header_line)
    if parsed_header is None:
        return frozenset()
    try:
        status_index = tuple(cell.lower() for cell in parsed_header).index("status")
    except ValueError:
        return frozenset()
    readme = _blob_bytes(root, readme_oid).decode("utf-8", errors="strict")
    task_links: dict[str, PurePosixPath] = {}
    for line in readme.splitlines():
        match = re.fullmatch(
            r"- \[`(?P<artifact>TSK-0054-(?P<sequence>[0-9]{4}))`\]"
            r"\((?P<relative>tasks/tsk-(?P=sequence)-[a-z0-9]+"
            r"(?:-[a-z0-9]+)*\.md)\)",
            line,
        )
        if match is None:
            continue
        artifact_id = match.group("artifact")
        path = task_legacy.parent / match.group("relative")
        if artifact_id in task_links or path in task_links.values():
            return frozenset()
        task_links[artifact_id] = path
    if len(task_links) != len(source_entries):
        return frozenset()

    expected_tasks: set[PurePosixPath] = set()
    for sequence, (row_line, cells) in enumerate(source_entries, 1):
        legacy_id = _work054_wp004b_legacy_id(cells[0])
        state = WORK054_WP004B_TASK_STATUSES.get(cells[status_index].strip().lower())
        if legacy_id is None or state is None:
            return frozenset()
        artifact_id = f"TSK-0054-{sequence:04d}"
        path = task_links.get(artifact_id)
        if path is None:
            return frozenset()
        oid = proposed_blobs.get(path)
        if oid is None:
            return frozenset()
        task_bytes = _blob_bytes(root, oid)
        task_table = _work054_wp004b_task_table(task_bytes)
        if task_table is None or path.name not in readme:
            return frozenset()
        task_header, task_separator, task_entries = task_table
        task_cells = task_entries[0][1] if len(task_entries) == 1 else ()
        task_text = task_bytes.decode("utf-8", errors="strict")
        checks = {
            "header": task_header == header_line,
            "separator": task_separator == separator_line,
            "work-row": task_cells == cells,
            "artifact-id": f'artifact_id: "{artifact_id}"' in task_text,
            "status": f"status: {state}" in task_text,
            "wp": f"**Plan label:** WP-{sequence:03d}" in task_text,
            "legacy-id": legacy_id in task_text,
            "common-contract": "../README.md#common-execution-contract" in task_text,
            "plan-link": "../plan.md" in task_text,
        }
        failed = next((name for name, valid in checks.items() if not valid), None)
        if failed is not None:
            raise InvocationError(
                f"WP004C MIG-0004 task proof failed: {path.as_posix()}:{failed}"
            )
        expected_tasks.add(path)
    actual_tasks = {
        path for path in proposed_blobs if path.parent == task_legacy.parent / "tasks"
    }
    if expected_tasks != actual_tasks:
        return frozenset()
    consumed.update((task_legacy, readme_path, *expected_tasks))
    try:
        _run_git(root, ("cat-file", "-e", f"{WP004C_SEALED_TARGET_COMMIT}^{{commit}}"))
        sealed_target_blobs = _tree_blob_map(root, WP004C_SEALED_TARGET_COMMIT)
    except InvocationError:
        return frozenset()
    for path in set(base_blobs) & set(proposed_blobs):
        if path.suffix != ".md" or base_blobs[path] == proposed_blobs[path]:
            continue
        if sealed_target_blobs.get(path) != proposed_blobs[path]:
            return frozenset()
        consumed.add(path)
    return frozenset(consumed)


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
    if WORK054_WP002_MIGRATION_PATH in base_blobs or migration_oid is None:
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
    if WORK054_WP002_DECISION_PATH in base_blobs or decision_oid is None:
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
        or hashlib.sha256(raw_decision).hexdigest() != WORK054_WP002_DECISION_SHA256
        or decision_document
        != LifecycleDocument(
            WORK054_WP002_DECISION_PATH,
            "sdlc/adr",
            "accepted",
        )
        or _work054_wp002_frontmatter_value(raw_decision, "artifact_id") != "ADR-0025"
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
    if WORK054_WP003_MIGRATION_PATH in base_blobs or migration_oid is None:
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
    if not isinstance(rows, list) or len(rows) != len(WORK054_WP003_OWNER_RETIREMENTS):
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
            evidence_class: "DEFER" for evidence_class in deferred_classes
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
        base_admission.get("contractId") != "hy-home.k8s/agent-roster-admission"
        or proposed_admission.get("contractId") != "hy-home.k8s/agent-roster-admission"
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
                baseline_state=("deferred-to-area-003-before-runtime-activation"),
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
                "excludedEvidenceClasses": list(AGENT_ROSTER_DEFERRED_CLASSES),
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
            evidence["promotionAuthorization"] = evidence.pop("projectionAuthorization")
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
            candidate["authority"] = "repository-static-role-and-adapter-inventory-only"
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
    migration_bytes = b"" if migration_oid is None else _blob_bytes(root, migration_oid)
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
        migration_bytes = _work054_wp002_render_migration_rows(migration_bytes, rows)
        proposed_blobs[WORK054_WP002_MIGRATION_PATH] = _git_blob_oid(migration_bytes)

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
            merged = next((row for row in rows if row.get("action") == "merged"), None)
            if merged is not None:
                merged["replacement"] = "docs/README.md"
        elif mutation == "target-artifact-drift":
            moved = next((row for row in rows if row.get("action") == "moved"), None)
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
    proposed_registry = dict(_registry_blob(root, WORK105_PROPOSED_REGISTRY_BLOB_OID))
    base_documents: dict[PurePosixPath, LifecycleDocument] = {}
    proposed_documents: dict[PurePosixPath, LifecycleDocument] = {}
    for token, status in WORK105_AD_CUTOVER:
        old_path = PurePosixPath(f"docs/02.architecture/requirements/{token}.md")
        new_path = PurePosixPath(f"docs/02.architecture/descriptions/ad-{token}.md")
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
    base_text = _blob_text(root, WORK105_ADR0023_BASE_BLOB_OID, WORK105_ADR0023_PATH)
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
        "sdlc/prd": "sdlc/requirement-package",  # Retired WP-004B alias.
        "sdlc/srs": "sdlc/requirement-package",  # Retired WP-004B alias.
        "sdlc/interface": "sdlc/requirement-package",  # Retired WP-004B alias.
        "sdlc/api-spec": "sdlc/requirement-package",  # Retired comparison alias.
        "sdlc/agent-design": "sdlc/spec",  # Retired WP-004C alias.
        "sdlc/tests": "sdlc/spec",  # Retired WP-004C alias.
        "governance/template-support": "governance/reference",  # Retired WP-004C alias.
        "template/sdlc/api-spec": "template/sdlc/requirement-package",  # Retired alias.
        "template/sdlc/prd": "template/sdlc/requirement-package",  # Retired WP-004C alias.
        "template/sdlc/srs": "template/sdlc/requirement-package",  # Retired WP-004C alias.
        "template/sdlc/interface": "template/sdlc/requirement-package",  # Retired WP-004C alias.
        "template/sdlc/agent-design": "template/sdlc/spec",  # Retired WP-004C alias.
        "template/sdlc/tests": "template/sdlc/spec",  # Retired WP-004C alias.
        "template/governance/template-support": "template/governance/reference",  # Retired WP-004C alias.
    }
    projected: list[DocumentProfile] = []
    for raw_profile in raw_profiles:
        if not isinstance(raw_profile, dict):
            raise InvocationError("comparison registry contains a non-object profile")
        profile_id = raw_profile.get("id")
        raw_routes = raw_profile.get("routes")
        if raw_routes is None and isinstance(raw_profile.get("pathPattern"), str):
            raw_routes = [{"kind": "regex", "value": raw_profile["pathPattern"]}]
        raw_lifecycle = raw_profile.get("lifecycle")
        raw_status_domain = raw_profile.get("statusDomain")
        if raw_status_domain is None and isinstance(raw_lifecycle, dict):
            raw_status_domain = raw_lifecycle.get("statusDomain")
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
        if profile is None or profile.body_contract is None:
            views[path] = LifecycleEvidenceDocument(
                document=document,
                all_local_links=(),
                relationship_links=(),
                unresolved_relationship_links=(),
                body_table_links=(),
                relationship_section_valid=profile is not None,
                body_contract_valid=profile is not None,
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

    base_agent_contract_blobs: Mapping[PurePosixPath, str] = MappingProxyType({})
    proposed_agent_contract_blobs: Mapping[PurePosixPath, str] = MappingProxyType({})
    if mode in {"staged", "ci"} and base_commit == AGENT_ROSTER_ADMISSION_BASE_COMMIT:
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

    # Stage 99 is terminal: compare both snapshots with the current root
    # profile authority. Historical route and flat-registry projections are
    # intentionally not lifecycle inputs.
    base_classification_registry = registry
    proposed_classification_registry = registry
    work054_wp002_consumed_paths = frozenset()
    work054_wp003_consumed_paths = finite_work054_wp003_agent_governance_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    wp004c_mig0004_consumed_paths = _wp004c_mig0004_paths(
        root=root,
        mode=mode,
        base_commit=base_commit,
        base_blobs=base_blobs,
        proposed_blobs=proposed_blobs,
    )
    work107_consumed_paths = frozenset()
    work108_consumed_paths = frozenset()

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
    work054_wp004a_consumed_paths: frozenset[PurePosixPath] = frozenset()
    base_snapshot, base_texts = _snapshot_projection(
        root, base_classification_registry, base_blobs
    )
    proposed_snapshot, proposed_texts = _snapshot_projection(
        root, proposed_classification_registry, proposed_blobs
    )
    evidence_context = evidence_context_factory(
        proposed_classification_registry,
        base_snapshot,
        proposed_snapshot,
        base_texts,
        proposed_texts,
    )
    work105_consumed_paths: frozenset[PurePosixPath] = frozenset()
    archive_consumed_paths: frozenset[PurePosixPath] = frozenset()
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
    legacy_consumed_paths = (
        work054_wp002_consumed_paths
        | work054_wp003_consumed_paths
        | work054_wp004a_consumed_paths
        | work105_consumed_paths
        | work107_consumed_paths
        | work108_consumed_paths
        | archive_consumed_paths
        | agent_consumed_paths
        | wp004c_mig0004_consumed_paths
    )

    def consume_finite_cutover(
        diagnostics: Sequence[LifecycleDiagnostic],
    ) -> tuple[LifecycleDiagnostic, ...]:
        return tuple(
            diagnostic
            for diagnostic in diagnostics
            if diagnostic.path not in legacy_consumed_paths
        )

    return consume_finite_cutover(
        compare_lifecycle(
            proposed_classification_registry,
            base_documents,
            proposed_documents,
            renames=renames,
            base_mode=mode,  # type: ignore[arg-type]
            evidence_context=evidence_context,
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
