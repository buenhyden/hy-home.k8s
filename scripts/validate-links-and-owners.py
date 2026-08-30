#!/usr/bin/env python3
"""Validate repository-local links, indexes, current owners, and migration ledger."""

from __future__ import annotations

import argparse
import bisect
import collections
import hashlib
import html
import importlib.util
import json
import os
import posixpath
import re
import stat
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field as dataclass_field
from functools import lru_cache
from pathlib import Path
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, Sequence
from urllib.parse import unquote

import yaml

try:
    from archive_recovery import (
        ArchiveContractError,
        WORK107_LEGACY_ARCHIVE_COMMIT,
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_MIGRATION_PATH,
        WORK107_STABLE_INDEX_OVERVIEW,
        parse_work107_migration_document,
        parse_archive_envelope,
        recover_work107_legacy_envelope,
        validate_work107_migration_rows,
    )
except ModuleNotFoundError:  # Imported as a repository-root test module.
    from scripts.archive_recovery import (
        ArchiveContractError,
        WORK107_LEGACY_ARCHIVE_COMMIT,
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_MIGRATION_PATH,
        WORK107_STABLE_INDEX_OVERVIEW,
        parse_work107_migration_document,
        parse_archive_envelope,
        recover_work107_legacy_envelope,
        validate_work107_migration_rows,
    )

try:
    from archive_validation import (
        MigrationProof,
        validate_pinned_migration_recovery,
        repository_migration_proof,
        compose_migration_targets,
        MigrationDeclaration,
        ArchiveRecord,
        project_migration_declaration_fields,
        validate_archive_records,
    )
except ModuleNotFoundError:  # Imported as a repository-root test module.
    from scripts.archive_validation import (
        MigrationProof,
        validate_pinned_migration_recovery,
        repository_migration_proof,
        compose_migration_targets,
        MigrationDeclaration,
        ArchiveRecord,
        project_migration_declaration_fields,
        validate_archive_records,
    )

from document_contracts import (
    DOCUMENT_TEXT_MAX_BYTES,
    Diagnostic,
    DocumentContractError,
    DocumentProfile,
    ProgramFollowUp,
    ProgramLineage,
    ProgramRelation,
    ReferenceCurrentPack,
    ReferenceCurrentPacks,
    Registry,
    StandaloneExecution,
    _parse_ls_files_stage_z,
    _run_git,
    classify_path,
    diagnostic_sort_key,
    enumerate_target_markdown,
    load_registry,
    read_repository_text,
)
from reference_information_architecture import (
    CANONICAL_SCHEMA_PATH as RIA_SCHEMA_PATH,
    MAX_BLOB_BYTES as RIA_MAX_BLOB_BYTES,
    ContractError as RiaContractError,
    _GitError as RiaGitError,
    _read_commit_path as _read_ria_commit_path,
    load_agent_cutover_projections,
    load_contract as load_ria_contract,
    retired_baseline_protected_commit,
)


_UNSET = object()
DEBT_PATH = Path("tests/fixtures/document-contracts/semantic-compatibility-debt.json")
LEDGER_PATH = PurePosixPath(
    "docs/90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md"
)
RIA_CONTRACT_PATH = PurePosixPath(
    "docs/90.references/data/reference-information-architecture.json"
)
# History holds the combined registry at this path; the RIA commit read below
# resolves it from a pinned commit rather than from the working tree.
RETIRED_DOCUMENT_PROFILES_PATH = PurePosixPath(
    "docs/99.templates/support/document-profiles.json"
)
ROUTE_CONTRACT_PATH = PurePosixPath("docs/99.templates/contracts/route-contract.json")
DOCUMENT_TAXONOMY_MANIFEST_PATH = PurePosixPath(
    "scripts/document-taxonomy-migration.json"
)
WORK109_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/mig-0002-sdlc-document-and-governance-consolidation.md"
)
WORK054_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/"
    "mig-0003-agent-governance-control-plane-consolidation.md"
)
WORK054_WP004B_MIGRATION_PATH = PurePosixPath(
    "docs/98.archive/migrations/0004-document-authority-convergence.md"
)
ARCHIVE_INDEX_BOUNDARY = "docs/98.archive/README.md#document-index"
ARCHIVE_INDEX_PATH = PurePosixPath("docs/98.archive/README.md")
DOCUMENT_TAXONOMY_SOURCE_COMMIT = (
    "713dff1fc3de58a2d1682970a7f24faa39c14263"  # pragma: allowlist secret
)
WORK109_SOURCE_COMMIT = (
    "160ce006969ddb49965c8af193f3e9ee290e18a8"  # pragma: allowlist secret
)
WORK109_LEDGER_MARKER = "<!-- archive-migration-ledger:v1 format=json -->"
WORK109_LEDGER_FIELDS = (
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
WORK109_REPLACEMENTS = {
    PurePosixPath("docs/04.execution/README.md"): PurePosixPath(
        "docs/03.specs/README.md"
    ),
    PurePosixPath("docs/04.execution/plans/README.md"): PurePosixPath(
        "docs/99.templates/templates/sdlc/execution/plan.template.md"
    ),
    PurePosixPath("docs/04.execution/tasks/README.md"): PurePosixPath(
        "docs/99.templates/templates/sdlc/execution/task.template.md"
    ),
}
WORK109_MERGES = {
    PurePosixPath(
        "docs/00.agent-governance/rules/document-stage-routing.md"
    ): PurePosixPath("docs/00.agent-governance/rules/document-authoring.md"),
    PurePosixPath(
        "docs/00.agent-governance/rules/documentation-protocol.md"
    ): PurePosixPath("docs/00.agent-governance/rules/document-authoring.md"),
    PurePosixPath(
        "docs/00.agent-governance/rules/stage-authoring-matrix.md"
    ): PurePosixPath("docs/00.agent-governance/rules/document-authoring.md"),
    PurePosixPath("docs/00.agent-governance/rules/stage-checklists.md"): PurePosixPath(
        "docs/00.agent-governance/rules/document-authoring.md"
    ),
    PurePosixPath(
        "docs/99.templates/support/common-documentation-governance.md"
    ): PurePosixPath("docs/99.templates/support/document-lifecycle.md"),
    PurePosixPath("docs/99.templates/support/documentation-contract.md"): PurePosixPath(
        "docs/99.templates/support/document-contract.md"
    ),
    PurePosixPath("docs/99.templates/support/frontmatter-schema.md"): PurePosixPath(
        "docs/99.templates/support/document-contract.md"
    ),
    PurePosixPath("docs/99.templates/support/legacy-cleanup-rules.md"): PurePosixPath(
        "docs/99.templates/support/document-lifecycle.md"
    ),
    PurePosixPath("docs/99.templates/support/sdlc-governance.md"): PurePosixPath(
        "docs/99.templates/support/document-lifecycle.md"
    ),
    PurePosixPath("docs/99.templates/support/template-routing.md"): PurePosixPath(
        "docs/99.templates/support/document-contract.md"
    ),
}
WORK105_HISTORY_SOURCE_COMMIT = "a6fa1806364ea0472baaad0906e1b5e4ddac8602"
WORK105_COMPLETED_HISTORY_ARD_TARGETS = frozenset(
    PurePosixPath(path)
    for path in (
        "docs/02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md",
        "docs/02.architecture/requirements/0005-argo-notifications-slack.md",
        "docs/02.architecture/requirements/0006-workspace-agent-governance-platform.md",
        "docs/02.architecture/requirements/0007-current-local-gitops-platform.md",
        "docs/02.architecture/requirements/0008-workspace-document-assurance-operating-model.md",
        "docs/02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md",
        "docs/02.architecture/requirements/0010-repository-delivery-evidence-architecture.md",
        "docs/02.architecture/requirements/0011-document-taxonomy-consolidation-architecture.md",
    )
)
WORK105_IMMUTABLE_HISTORY_ARD_TARGETS = WORK105_COMPLETED_HISTORY_ARD_TARGETS | {
    PurePosixPath("docs/02.architecture/requirements/README.md")
}
WORK105_ACCEPTED_HISTORY_ADR_PATHS = frozenset(
    PurePosixPath(f"docs/02.architecture/decisions/{name}.md")
    for name in (
        "0002-argocd-helm-and-gitops-model",
        "0003-eso-vault-k8s-auth",
        "0006-cert-manager-mkcert-ca-issuer",
        "0008-istio-install-and-ingress-coexist",
        "0009-kiali-external-observability",
        "0011-argo-rollouts-progressive-delivery",
        "0012-argo-notifications-slack",
        "0013-stage-00-canonical-adapter-model",
        "0014-current-local-gitops-platform-contract",
        "0015-declarative-document-contract-registry",
        "0016-program-to-tranche-document-lineage",
        "0017-program-follow-up-lineage-semantics",
        "0018-full-body-archive-record-and-retention",
        "0019-provider-native-agent-harness-and-loop-model",
        "0020-document-lifecycle-program-closure-evidence",
        "0021-canonical-surface-routing-and-evidence-depth",
        "0022-direct-approval-standalone-execution-lineage",
        "0023-work-unit-document-taxonomy-and-governance-authority",
    )
)
WORK105_AMENDED_ACCEPTED_ADR_SHA256 = {
    PurePosixPath(
        "docs/02.architecture/decisions/0018-full-body-archive-record-and-retention.md"
    ): "e4b718b76b87157be60e824e4c8aaada01af220ebb1b3f43b04d36b1b5110285",  # pragma: allowlist secret
    PurePosixPath(
        "docs/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md"
    ): "717714ce153cbd75ca5a77beb42a24cd1b146f25b1112d492e30d9fd214348d5",  # pragma: allowlist secret
}
WORK105_LEDGER_PATH_ALIASES = {
    PurePosixPath("docs/02.architecture/requirements/README.md"): PurePosixPath(
        "docs/02.architecture/descriptions/README.md"
    ),
    **{
        source: PurePosixPath("docs/02.architecture/descriptions") / f"ad-{source.name}"
        for source in WORK105_COMPLETED_HISTORY_ARD_TARGETS
    },
    PurePosixPath(
        "docs/99.templates/templates/sdlc/architecture/ard.template.md"
    ): PurePosixPath("docs/99.templates/templates/sdlc/architecture/ad.template.md"),
}
WORK105_LEDGER_RETIRED_PATHS = frozenset(
    {PurePosixPath("docs/99.templates/templates/sdlc/specs/api-spec.template.md")}
)


@lru_cache(maxsize=4)
def _validated_work107_stable_archive_rows(
    root_value: str,
    content: bytes,
) -> tuple[dict[str, object], ...]:
    try:
        rows = parse_work107_migration_document(content)
        return validate_work107_migration_rows(Path(root_value), rows)
    except (
        ArchiveContractError,
        DocumentContractError,
        OSError,
        UnicodeError,
        ValueError,
    ):
        return ()


def _work107_stable_archive_rows(context: "Context") -> tuple[dict[str, object], ...]:
    """Load only the exact reviewed WORK-107 migration ledger from the candidate."""

    path = PurePosixPath(WORK107_MIGRATION_PATH)
    text = context.texts.get(path)
    if text is None:
        return ()
    content = text.encode("utf-8")
    return _validated_work107_stable_archive_rows(
        str(context.root.absolute()),
        content,
    )


def _work107_stable_archive_aliases(
    context: "Context",
) -> dict[PurePosixPath, PurePosixPath]:
    rows = _work107_stable_archive_rows(context)
    aliases = {
        PurePosixPath(str(row["legacy_path"])): PurePosixPath(str(row["stable_path"]))
        for row in rows
    }
    return aliases if len(aliases) == 93 and len(set(aliases.values())) == 93 else {}


def _work107_stable_archive_index_source(
    context: "Context",
    source: PurePosixPath,
) -> bool:
    """Prove the Stage 98 index is the reviewed overview/link projection."""

    if source != ARCHIVE_INDEX_PATH or source not in context.texts:
        return False
    rows = _work107_stable_archive_rows(context)
    if len(rows) != 93:
        return False
    try:
        legacy = _read_ria_commit_path(
            context.root,
            WORK107_LEGACY_ARCHIVE_COMMIT,
            Path(source.as_posix()),
        ).decode("utf-8")
    except (RiaContractError, RiaGitError, UnicodeDecodeError):
        return False
    if legacy.count(WORK107_LEGACY_INDEX_OVERVIEW) != 1:
        return False
    projected = legacy.replace(
        WORK107_LEGACY_INDEX_OVERVIEW,
        WORK107_STABLE_INDEX_OVERVIEW,
        1,
    )
    for row in rows:
        old = str(row["legacy_path"]).removeprefix("docs/98.archive/")
        new = str(row["stable_path"]).removeprefix("docs/98.archive/")
        reviewed = f"[`{old}`](./{old})"
        stable = f"[`{new}`](./{new})"
        if projected.count(reviewed) != 1:
            return False
        projected = projected.replace(reviewed, stable, 1)
    return projected == context.texts[source]


OWNER = "cross-document-validator"
LEDGER_SETTLEMENT_ID = "ria-0007-postflight-ledger"
LEDGER_SETTLEMENT_PACK_ID = "research/2026-08-08-wer"
LEDGER_SETTLEMENT_SUBJECT = "source-coverage-and-migration-ledger"
LEDGER_SETTLEMENT_FROM_COMMIT = "git-sha1:15bba3d436ee2818f29d6f6880c7d5c4901aa0fe"
LEDGER_SETTLEMENT_REASON = (
    "Record observed C1 8c0dcea558212e11ac93a0fe626cddb31315859b "
    "lifecycle closure and repository-static postflight evidence in the "
    "protected migration ledger"
)
LEDGER_SETTLEMENT_KEYS = frozenset(
    {
        "id",
        "packId",
        "fromCommit",
        "subject",
        "targetSha256",
        "targetByteLength",
        "reason",
        "transitionCommit",
    }
)
GIT_SHA1_PATTERN = re.compile(r"git-sha1:[0-9a-f]{40}")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
MAX_LEDGER_BYTES = 2_000_000
LEDGER_COLUMNS = (
    "path",
    "title",
    "profile",
    "owner-key",
    "disposition",
    "destination",
    "local-evidence",
    "official-sources",
    "observed-version",
    "applicability",
    "content-decision",
    "refresh-trigger",
    "reviewer",
    "result",
)
WERPC_DISPOSITION_COLUMNS = (
    "old path",
    "source commit",
    "topic or heading",
    "verification",
    "new owner",
    "disposition",
    "reason and evidence",
)
WERPC_DELETION_DISPOSITION = "Deleted in WERPC-008 after cutover gate"
WERPC_PREDECESSOR_PATHS = frozenset(
    {
        "docs/90.references/research/2026-07-04-wer/README.md",
        "docs/90.references/research/2026-07-04-wer/ai-agents-roster-and-gap-analysis.md",
        "docs/90.references/research/2026-07-04-wer/automation-pipeline-workflow-qa.md",
        "docs/90.references/research/2026-07-04-wer/harness-and-loop-engineering.md",
        "docs/90.references/research/2026-07-04-wer/kubernetes-infrastructure-security.md",
        "docs/90.references/research/2026-07-04-wer/provider-implementation-status.md",
        "docs/90.references/research/2026-07-04-wer/spec-sdlc-ci-qa-formatting.md",
        "docs/90.references/research/2026-07-04-wer/workspace-governance-baseline.md",
        "docs/90.references/research/2026-07-07-wer/README.md",
        "docs/90.references/research/2026-07-07-wer/ai-agents-roster-and-gap-analysis.md",
        "docs/90.references/research/2026-07-07-wer/automation-pipeline-workflow-qa.md",
        "docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md",
        "docs/90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md",
        "docs/90.references/research/2026-07-07-wer/harness-and-loop-engineering.md",
        "docs/90.references/research/2026-07-07-wer/kubernetes-infrastructure-security.md",
        "docs/90.references/research/2026-07-07-wer/provider-implementation-status.md",
        "docs/90.references/research/2026-07-07-wer/spec-sdlc-ci-qa-formatting.md",
        "docs/90.references/research/2026-07-07-wer/workspace-governance-baseline.md",
        "docs/90.references/research/2026-08-07-wer/README.md",
        "docs/90.references/research/2026-08-07-wer/agent-memory-tiers-and-management.md",
        "docs/90.references/research/2026-08-07-wer/agent-model-routing-and-configuration.md",
        "docs/90.references/research/2026-08-07-wer/documentation-architecture-and-diataxis.md",
        "docs/90.references/research/2026-08-07-wer/github-actions-and-ci-evidence.md",
        "docs/90.references/research/2026-08-07-wer/llm-wiki-and-knowledge-routing.md",
        "docs/90.references/research/2026-08-07-wer/research-consolidation-and-supersession-map.md",
    }
)
DEBT_LITERAL = {
    "ruleId": "LEDGER-MISSING",
    "path": LEDGER_PATH.as_posix(),
    "profile": "content/reference",
    "expected": "ledger exists, has the exact fourteen columns, and covers the inventory once",
    "actual": "ledger is missing",
    "ownerTask": "ADM-002",
    "removeWhen": "ledger exists, has the exact fourteen columns, and covers the inventory once",
}
GOVERNANCE_CURRENT_README = PurePosixPath("docs/00.agent-governance/README.md")
GOVERNANCE_CURRENT_HEADING = "### Current Governance Authority Index"
STATUS_MAP = {
    "draft": "draft",
    "active": "active",
    "done": "done",
    "archived": "archived",
}
OWNER_EXCLUSIONS = (
    re.compile(
        r"^docs/90\.references/(?:research|audits)/[0-9]{4}-[0-9]{2}-[0-9]{2}-[^/]+/"
    ),
    re.compile(r"^docs/90\.references/cloud-examples/"),
    re.compile(r"^examples/(?:aws|azure)/docs/"),
)
RETIRED_REFERENCE_ALIASES = {
    PurePosixPath(
        "docs/00.agent-governance/contracts/agent-role-semantics.json"
    ): PurePosixPath(".agents/registry.json"),
    PurePosixPath(
        "docs/00.agent-governance/contracts/agent-role-semantics.schema.json"
    ): PurePosixPath(".agents/contracts/agent-registry.schema.json"),
    PurePosixPath("scripts/validate-agent-role-semantics.py"): PurePosixPath(
        "scripts/validate-agent-harness-semantics.py"
    ),
    PurePosixPath("tests/fixtures/agent-role-semantics.json"): PurePosixPath(
        ".agents/registry.json"
    ),
    PurePosixPath(".github/ABOUT.md"): PurePosixPath(".github/README.md"),
}


@dataclass(frozen=True)
class DeclaredIndex:
    path: PurePosixPath
    target_pattern: re.Pattern[str]
    tree_anchor: str
    tree_root: str
    table_anchor: str
    table_mode: str
    tree_kind: str


DECLARED_INDEXES = (
    DeclaredIndex(
        PurePosixPath("docs/03.specs/README.md"),
        re.compile(r"^docs/03\.specs/[0-9]{4}-[^/]+/spec\.md$"),
        "## Document Index",
        "03.specs/",
        "### Current Spec Index",
        "section",
        "spec",
    ),
)


@dataclass(frozen=True)
class CollectionIndex:
    path: PurePosixPath
    root: PurePosixPath
    target_pattern: re.Pattern[str]
    tree_anchor: str
    tree_root: str
    table_anchor: str
    table_mode: str
    table_includes_self: bool


COLLECTION_INDEXES = (
    CollectionIndex(
        PurePosixPath("docs/90.references/research/README.md"),
        PurePosixPath("docs/90.references/research"),
        re.compile(
            r"^docs/90\.references/research/(?:README\.md|"
            r"2026-08-08-wer/[^/]+\.md)$"
        ),
        "## Item Index",
        "research/",
        "### Research Pack Index",
        "section",
        True,
    ),
    CollectionIndex(
        PurePosixPath("docs/90.references/research/2026-08-08-wer/README.md"),
        PurePosixPath("docs/90.references/research/2026-08-08-wer"),
        re.compile(r"^docs/90\.references/research/2026-08-08-wer/[^/]+\.md$"),
        "### Structure",
        "2026-08-08-wer/",
        "## Report Index",
        "section",
        False,
    ),
)


@dataclass(frozen=True)
class ProfileView:
    profile_id: str
    profile_class: str
    mode: str


@dataclass(frozen=True)
class Context:
    root: Path
    paths: tuple[PurePosixPath, ...]
    baseline_paths: frozenset[PurePosixPath]
    profiles: dict[PurePosixPath, ProfileView]
    texts: dict[PurePosixPath, str]
    metadata: dict[PurePosixPath, dict[str, Any]]
    adapter_targets: dict[PurePosixPath, PurePosixPath]
    governance_current_paths: tuple[PurePosixPath, ...]
    governance_current_states: tuple[str, ...]
    reference_current_packs: ReferenceCurrentPacks
    tracked_regular_paths: frozenset[PurePosixPath]
    ledger_bytes: bytes | None = None
    ria_contract_text: str | None = None
    route_state: str = "legacy"
    work105_history_base_commit: str = WORK105_HISTORY_SOURCE_COMMIT
    document_registry: Registry | None = None
    raw_schema: object = _UNSET
    read_current_bytes: Callable[[str, int], bytes] | None = None


@dataclass(frozen=True, order=True)
class ArchiveTransitionEdge:
    """One immutable move-current link deferred until WDTC-104."""

    source: PurePosixPath
    target: PurePosixPath


EXPECTED_ARCHIVE_TRANSITION_EDGES: tuple[ArchiveTransitionEdge, ...] = ()
REVIEWED_STAGE90_MOVE_SOURCE_BLOBS = {
    PurePosixPath(
        "docs/90.references/audits/2026-07-02-whia/harness-loop-implementation-audit.md"
    ): "39f7d5dbc4d69e53485fb0b9d482a151e9b44b86",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-02-whia/provider-harness-loop-implementation-audit.md"
    ): "0403e861994bc322fbcaaabfceb1b5c8ada02572",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-02-whia/sdlc-delivery-practices-implementation-audit.md"
    ): "693b0b2b29899b4a6a54acbb2aa697b9ff5c0818",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-02-whia/workspace-governance-implementation-audit.md"
    ): "0965758eccd42bba5e884f01270ed738c9d6410a",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-03-wdgh/workspace-document-governance-hardening-audit.md"
    ): "9f60551f8e5035cee01941a039a9be3336021916",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-04-wdcn/workspace-document-contract-normalization-audit.md"
    ): "21151b591f787179f50dbbea0cd02913acb8f2e3",  # pragma: allowlist secret
    PurePosixPath("docs/90.references/audits/2026-07-05-wea/README.md"): (
        "9a7c9c70336c7510e23634b62eb0ee7b41d0db43"  # pragma: allowlist secret
    ),
    PurePosixPath(
        "docs/90.references/audits/2026-07-05-wea/governance-harness-loop-providers.md"
    ): "84830e0fa7178f820bfb189d9f129fd34209af18",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-05-wea/implementation-roadmap-and-automation-opportunities.md"
    ): "5cf2c6b9b24ab510b3cfa48eca6f7afa7d0feec5",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-05-wea/kubernetes-infrastructure-security.md"
    ): "cdab943dcb4d9d50b5252afad13db8e0bb3ce39a",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-05-wea/sdlc-ci-qa-formatting-automation.md"
    ): "ceca294a1902fd38d33f4dec6aa0b41dc6e3ed15",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
    ): "9fc02988093b418d8e27b464d1d341ab877c5562",  # pragma: allowlist secret
    PurePosixPath("docs/90.references/research/2026-08-08-wer/README.md"): (
        "6bfec251d8927dd82f5c12b49c013a598c64d088"  # pragma: allowlist secret
    ),
    PurePosixPath("docs/90.references/research/README.md"): (
        "a21d2cfeae6dfcd4cdc98f6661c1f7a190c49523"  # pragma: allowlist secret
    ),
}
REVIEWED_STAGE90_MOVE_EDGE_COUNT = 29
IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS = {
    **REVIEWED_STAGE90_MOVE_SOURCE_BLOBS,
    PurePosixPath(
        "docs/90.references/audits/2026-07-11-weia/governance-harness-loop-providers.md"
    ): "b35dce197ca96bb9341b590ef505040e86d18577",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/audits/2026-07-11-weia/"
        "sdlc-document-lifecycle-frontmatter.md"
    ): "39cdc99f265ca91c35f1f0ede114cf626359837e",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/cloud-examples/README.md"
    ): "841d76f65390f1dfa37e282dbda8eeb6738c2d30",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/cloud-examples/aws/2026-07-12-aws-example-snapshot.md"
    ): "e4cce69bb4eab38e1d5e848217e0aabd6ea93a5b",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/cloud-examples/aws/README.md"
    ): "08a7f4d9d25bdde493dd4785e3c2ab35ed42d0b2",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md"
    ): "7d2fea31e9174306b85d017624b1ed7df9f4c358",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/cloud-examples/azure/README.md"
    ): "a3d5bea92ec2ef78115aa473e77fc044d0d8426e",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/data/agent-reference-index.md"
    ): "4c8b4a08b7965da2c9e108c9cc83a41c2d5f8439",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/llm-wiki/README.md"
    ): "3451f28cb08bab9e23a798998e00489bdf6959b8",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/llm-wiki/wiki-index.md"
    ): "0c0941ad247d91e049c7d810010feea08de4d075",  # pragma: allowlist secret
    PurePosixPath(
        "docs/90.references/research/2026-08-08-wer/"
        "documentation-architecture-and-diataxis.md"
    ): "e5f0495270e6a4b5b4aeb97401957d501989eb33",  # pragma: allowlist secret
    PurePosixPath(
        "docs/98.archive/README.md"
    ): "35b69ced14f3f5511a3b13dff35e337000297333",  # pragma: allowlist secret
}

@dataclass(frozen=True)
class ArchiveTransitionHandoff:
    """Closed transition projection to the collection archive boundary."""

    navigation_boundary: str
    edges: tuple[ArchiveTransitionEdge, ...]


@dataclass(frozen=True)
class LifecycleMarkdownEvidence:
    """Immutable lifecycle view derived by the canonical Markdown scanner."""

    path: PurePosixPath
    all_local_links: tuple[PurePosixPath, ...]
    relationship_links: tuple[PurePosixPath, ...]
    unresolved_relationship_links: tuple[PurePosixPath, ...]
    body_table_links: tuple[PurePosixPath, ...]
    relationship_section_valid: bool
    body_contract_valid: bool
    body_rows: tuple[tuple[tuple[str, str], ...], ...]
    task_terminal_evidence_valid: bool


class ConfigurationError(ValueError):
    """Malformed closed configuration or CLI state."""


def _diag(
    rule_id: str, path: PurePosixPath, profile: str, expected: str, actual: str
) -> Diagnostic:
    return Diagnostic(rule_id, path, profile, expected, actual, OWNER)


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing < 0:
        return {}
    try:
        data = yaml.safe_load(text[4:closing]) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _commonmark_splitlines(value: str, *, keepends: bool = False) -> list[str]:
    """Split only CR, LF, or CRLF without treating controls as line endings."""

    lines: list[str] = []
    cursor = 0
    for match in re.finditer(r"\r\n|\r|\n", value):
        lines.append(value[cursor : match.end() if keepends else match.start()])
        cursor = match.end()
    if cursor < len(value):
        lines.append(value[cursor:])
    return lines


def _commonmark_blank_line(value: str) -> bool:
    """Return whether a source line contains only CommonMark blank spaces."""

    return not value.strip(" \t")


def _visible_markdown(text: str) -> str:
    inline_masked = list(text)
    cursor = 0
    while cursor < len(text):
        start = text.find("<!--", cursor)
        if start < 0:
            break
        match = _INLINE_HTML_COMMENT.match(text, start)
        if match is None:
            cursor = start + 1
            continue
        line_start = text.rfind("\n", 0, start) + 1
        prefix = text[line_start:start]
        container_prefix = prefix
        while container_prefix:
            quote_content = _strip_blockquote_marker(container_prefix)
            if quote_content is not None:
                container_prefix = quote_content
                continue
            list_content = _strip_list_item_marker(container_prefix)
            if list_content is not None:
                container_prefix = list_content[0]
                continue
            break
        if (
            _source_character_escaped(text, start)
            or re.fullmatch(r" {0,3}", container_prefix) is not None
            or re.search(r"\n[ \t]*\n", match.group(0)) is not None
        ):
            cursor = match.end()
            continue
        for offset in range(start, match.end()):
            if inline_masked[offset] not in "\r\n":
                inline_masked[offset] = _INLINE_COMMENT_OPAQUE
        cursor = match.end()

    output: list[str] = []
    fence: tuple[str, int] | None = None
    comment_block = False
    for raw_line in _commonmark_splitlines("".join(inline_masked)):
        if fence is not None:
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", raw_line)
            if marker:
                token = marker.group(1)
                if (
                    token[0] == fence[0]
                    and len(token) >= fence[1]
                    and not marker.group(2).strip()
                ):
                    fence = None
            output.append("")
            continue
        if comment_block:
            output.append("")
            if "-->" in raw_line:
                comment_block = False
            continue
        comment_start = re.match(r"^ {0,3}<!--", raw_line)
        if comment_start is not None:
            output.append("")
            if raw_line.find("-->", comment_start.start() + 2) < 0:
                comment_block = True
            continue
        line = raw_line
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if token[0] == "`" and "`" in marker.group(2):
                output.append(line)
                continue
            fence = (token[0], len(token))
            output.append("")
            continue
        output.append(line)
    return "\n".join(output)


_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|"
    "iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|"
    "option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|"
    "title|tr|track|ul"
)
_HTML_BLOCK_TAG = re.compile(
    rf"^ {{0,3}}</?(?:{_HTML_BLOCK_TAGS})(?:\s|/?>|$)", re.IGNORECASE
)
_INLINE_HTML_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
_INLINE_HTML_ATTRIBUTE_NAME = r"[A-Za-z_:][A-Za-z0-9_.:-]*"
_INLINE_HTML_ATTRIBUTE_VALUE = r"""(?:[^\s"'=<>`]+|'[^']*'|"[^"]*")"""
_INLINE_HTML_ATTRIBUTE = (
    rf"[ \t\r\n]+{_INLINE_HTML_ATTRIBUTE_NAME}"
    rf"(?:[ \t\r\n]*=[ \t\r\n]*{_INLINE_HTML_ATTRIBUTE_VALUE})?"
)
_INLINE_HTML_TAG_SOURCE = (
    rf"(?:</{_INLINE_HTML_TAG_NAME}[ \t\r\n]*>|"
    rf"<{_INLINE_HTML_TAG_NAME}(?:{_INLINE_HTML_ATTRIBUTE})*"
    r"[ \t\r\n]*/?>)"
)
_INLINE_HTML_TAG = re.compile(_INLINE_HTML_TAG_SOURCE)
_HTML_COMPLETE_TAG = re.compile(rf"^ {{0,3}}{_INLINE_HTML_TAG_SOURCE}[ \t]*$")


def _render_container_markdown(
    text: str,
    *,
    defer_indented_code: bool = False,
    paragraph_continuation_lines: frozenset[int] = frozenset(),
) -> str:
    """Render one CommonMark container while retaining soft line breaks."""

    visible = _visible_markdown(text)
    lines = _commonmark_splitlines(visible)
    output: list[str] = []
    raw_end: re.Pattern[str] | None = None
    raw_until_blank = False
    indented_code = False
    previous_blank = True
    previous_leaf_block = False
    previous_paragraph_line = False

    atx_heading = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    setext_delimiter = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic_break = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )
    definition_lines: set[int] = set()
    if not defer_indented_code:
        _, definition_spans = _reference_definitions_with_spans(
            visible,
            lazy_lines=paragraph_continuation_lines,
        )
        for start, end in definition_spans:
            first_line = visible.count("\n", 0, start)
            last_line = visible.count("\n", 0, end)
            definition_lines.update(range(first_line, last_line + 1))

    def ends_leaf_block(line: str, setext_eligible: bool) -> bool:
        return (
            atx_heading.fullmatch(line) is not None
            or thematic_break.fullmatch(line) is not None
            or (setext_eligible and setext_delimiter.fullmatch(line) is not None)
        )

    for line_index, line in enumerate(lines):
        paragraph_continuation = line_index in paragraph_continuation_lines
        if raw_end is not None:
            output.append("")
            if raw_end.search(line):
                raw_end = None
            previous_blank = not line.strip()
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        if raw_until_blank:
            output.append("")
            if not line.strip():
                raw_until_blank = False
            previous_blank = not line.strip()
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        if line_index in definition_lines:
            output.append(line)
            previous_blank = False
            previous_leaf_block = True
            previous_paragraph_line = False
            continue
        if not defer_indented_code and indented_code and not paragraph_continuation:
            if not line.strip() or line.startswith(("    ", "\t")):
                output.append("")
                previous_blank = not line.strip()
                previous_leaf_block = False
                previous_paragraph_line = False
                continue
            indented_code = False
        if (
            not defer_indented_code
            and not paragraph_continuation
            and (previous_blank or previous_leaf_block)
            and line.startswith(("    ", "\t"))
        ):
            indented_code = True
            output.append("")
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue

        start = re.match(
            r"^ {0,3}<(?P<tag>script|pre|style|textarea)(?:\s|>|$)", line, re.IGNORECASE
        )
        if start is not None:
            output.append("")
            closing = re.compile(
                rf"</{re.escape(start.group('tag'))}\s*>", re.IGNORECASE
            )
            if closing.search(line, start.end()) is None:
                raw_end = closing
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        raw_delimiters = (
            (re.match(r"^ {0,3}<\?", line), re.compile(r"\?>")),
            (re.match(r"^ {0,3}<!\[CDATA\[", line), re.compile(r"\]\]>")),
            (re.match(r"^ {0,3}<![A-Z]", line), re.compile(r">")),
        )
        matched_raw = False
        for start_match, closing in raw_delimiters:
            if start_match is None:
                continue
            output.append("")
            if closing.search(line, start_match.end()) is None:
                raw_end = closing
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            matched_raw = True
            break
        if matched_raw:
            continue
        if _HTML_BLOCK_TAG.match(line) or (
            previous_blank and _HTML_COMPLETE_TAG.match(line)
        ):
            output.append("")
            raw_until_blank = True
            previous_blank = False
            previous_leaf_block = False
            previous_paragraph_line = False
            continue
        leaf_block = not paragraph_continuation and ends_leaf_block(
            line, previous_paragraph_line
        )
        output.append(line)
        previous_blank = not line.strip()
        previous_leaf_block = leaf_block
        previous_paragraph_line = bool(line.strip()) and not leaf_block
    return "\n".join(output)


def _normalize_component(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(
        r"-+",
        "-",
        "".join(character if character.isalnum() else "-" for character in normalized),
    ).strip("-")


def _profile_view(profile: DocumentProfile) -> ProfileView:
    return ProfileView(profile.profile_id, profile.profile_class, profile.mode)


def _terminal_governance_current_owners(
    registry: Registry,
    paths: Sequence[PurePosixPath],
    profiles: Mapping[PurePosixPath, ProfileView],
    metadata: Mapping[PurePosixPath, Mapping[str, Any]],
) -> tuple[tuple[PurePosixPath, ...], tuple[str, ...]]:
    """Derive Stage 00 current owners from the terminal profile lifecycle."""

    owner_profiles = tuple(
        profile
        for profile in registry.profiles
        if profile.profile_id == "governance/reference"
    )
    lifecycle_domain = (
        owner_profiles[0].lifecycle_domain if len(owner_profiles) == 1 else None
    )
    allowed_states = (
        tuple(
            state
            for state, validation_class in lifecycle_domain.states
            if validation_class == "current"
        )
        if lifecycle_domain is not None
        else ()
    )
    if (
        len(owner_profiles) != 1
        or owner_profiles[0].mode != "authored"
        or not allowed_states
        or not set(allowed_states).issubset(owner_profiles[0].status_domain)
    ):
        raise ConfigurationError(
            "terminal governance current-owner profile is unavailable"
        )
    current = tuple(
        sorted(
            path
            for path in paths
            if profiles[path].profile_id == "governance/reference"
            and profiles[path].mode == "authored"
            and str(metadata[path].get("status", "")).casefold() in allowed_states
        )
    )
    if not current:
        raise ConfigurationError("terminal governance current-owner set is empty")
    return current, allowed_states


def _terminal_reference_current_packs(
    registry: Registry,
    contract: Mapping[str, Any],
    paths: Sequence[PurePosixPath],
    profiles: Mapping[PurePosixPath, ProfileView],
    metadata: Mapping[PurePosixPath, Mapping[str, Any]],
) -> ReferenceCurrentPacks:
    """Derive Stage 90 current packs from the schema-validated RIA owner."""

    reference_profiles = tuple(
        profile
        for profile in registry.profiles
        if profile.profile_id == "content/reference"
    )
    baselines = contract.get("currentPackBaselines")
    if (
        len(reference_profiles) != 1
        or reference_profiles[0].mode not in {"authored", "classification-only"}
        or not isinstance(baselines, Mapping)
        or not baselines
    ):
        raise ConfigurationError("terminal reference Current-pack owner is unavailable")
    status_domain = reference_profiles[0].status_domain
    packs: list[ReferenceCurrentPack] = []
    for pack_id, baseline in sorted(baselines.items()):
        if (
            not isinstance(pack_id, str)
            or re.fullmatch(r"[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)+", pack_id)
            is None
            or not isinstance(baseline, str)
            or GIT_SHA1_PATTERN.fullmatch(baseline) is None
        ):
            raise ConfigurationError("terminal reference Current-pack identity differs")
        pack_root = PurePosixPath("docs/90.references") / pack_id
        pack_readme = pack_root / "README.md"
        collection_readme = pack_root.parent / "README.md"
        if pack_readme not in paths or collection_readme not in paths:
            raise ConfigurationError(
                "terminal reference Current-pack router is missing"
            )
        members = tuple(
            sorted(
                path.name
                for path in paths
                if path.parent == pack_root
                and path != pack_readme
                and path.suffix == ".md"
                and profiles[path].profile_id == "content/reference"
                and profiles[path].mode in {"authored", "classification-only"}
            )
        )
        member_states = {
            str(metadata[pack_root / member].get("status", "")).casefold()
            for member in members
        }
        if (
            not members
            or "" in member_states
            or not member_states.issubset(status_domain)
        ):
            raise ConfigurationError(
                "terminal reference Current-pack members are malformed"
            )
        allowed_states = tuple(
            state for state in status_domain if state in member_states
        )
        packs.append(
            ReferenceCurrentPack(
                id=pack_id,
                allowed_states=allowed_states,
                members=members,
            )
        )
    return ReferenceCurrentPacks(
        profile_id=reference_profiles[0].profile_id,
        packs=tuple(packs),
    )


def _held_context_inputs(
    registry: Registry | None,
    raw_schema: object,
    read_current_bytes: Callable[[str, int], bytes] | None,
) -> bool:
    if registry is None and raw_schema is _UNSET and read_current_bytes is None:
        return False
    if (
        not isinstance(registry, Registry)
        or not isinstance(raw_schema, dict)
        or not callable(read_current_bytes)
    ):
        raise ConfigurationError("held historical inputs are incomplete")
    return True


def _held_context_bytes(
    read_current_bytes: Callable[[str, int], bytes],
    path: PurePosixPath,
    max_bytes: int,
) -> bytes:
    payload = read_current_bytes(path.as_posix(), max_bytes)
    if type(payload) is not bytes or len(payload) > max_bytes:
        raise ConfigurationError("held historical bytes are invalid or oversized")
    return payload


def _build_context(
    root: Path,
    include_paths: tuple[PurePosixPath, ...] = (),
    *,
    registry: Registry | None = None,
    raw_schema: object = _UNSET,
    read_current_bytes: Callable[[str, int], bytes] | None = None,
    read_symlink: Callable[[str], str] | None = None,
) -> Context:
    root = root.absolute()
    held = _held_context_inputs(registry, raw_schema, read_current_bytes)
    if (held and not callable(read_symlink)) or (not held and read_symlink is not None):
        raise ConfigurationError("held historical symlink inputs are incomplete")
    if not held:
        registry = load_registry(root)
    inventory = enumerate_target_markdown(root, include_paths=include_paths)
    profiles: dict[PurePosixPath, ProfileView] = {}
    texts: dict[PurePosixPath, str] = {}
    metadata: dict[PurePosixPath, dict[str, Any]] = {}
    ledger_bytes: bytes | None = None
    for path in inventory.current_paths:
        profile = classify_path(registry, path)
        profiles[path] = _profile_view(profile)
        if held:
            assert read_current_bytes is not None
            try:
                text = _held_context_bytes(
                    read_current_bytes, path, DOCUMENT_TEXT_MAX_BYTES
                ).decode("utf-8", errors="strict")
            except UnicodeError as exc:
                raise ConfigurationError("held historical text is not UTF-8") from exc
        else:
            text = read_repository_text(root, path)
        texts[path] = text
        metadata[path] = _frontmatter(text)
        if path == LEDGER_PATH:
            ledger_bytes = text.encode("utf-8")
    try:
        if held:
            assert read_current_bytes is not None
            ria_bytes = _held_context_bytes(
                read_current_bytes, RIA_CONTRACT_PATH, RIA_MAX_BLOB_BYTES
            )
            ria_schema_bytes = _held_context_bytes(
                read_current_bytes, PurePosixPath(RIA_SCHEMA_PATH), RIA_MAX_BLOB_BYTES
            )
            ria_contract = load_ria_contract(
                root,
                Path(RIA_CONTRACT_PATH),
                contract_bytes=ria_bytes,
                schema_bytes=ria_schema_bytes,
            )
            ria_contract_text = ria_bytes.decode("utf-8", errors="strict")
        else:
            ria_contract = load_ria_contract(root, Path(RIA_CONTRACT_PATH.as_posix()))
            ria_contract_text = read_repository_text(root, RIA_CONTRACT_PATH)
    except (
        DocumentContractError,
        RiaContractError,
        RiaGitError,
        OSError,
        ValueError,
    ) as exc:
        raise ConfigurationError(
            "terminal reference Current-pack authority is unavailable"
        ) from exc
    adapters: dict[PurePosixPath, PurePosixPath] = {}
    for adapter in inventory.current_symlink_paths:
        raw_target = (
            read_symlink(adapter.as_posix()) if held else os.readlink(root / adapter)
        )
        if not isinstance(raw_target, str):
            raise ConfigurationError("held historical symlink target is invalid")
        normalized = posixpath.normpath(
            posixpath.join(adapter.parent.as_posix(), raw_target)
        )
        if (
            normalized == ".."
            or normalized.startswith("../")
            or normalized.startswith("/")
        ):
            raise ConfigurationError(
                f"symlink adapter escapes repository: {adapter.as_posix()}"
            )
        adapters[adapter] = PurePosixPath(normalized)
    tracked_regular_paths = frozenset(
        entry.path
        for entry in _parse_ls_files_stage_z(
            _run_git(root, ("ls-files", "--stage", "-z"))
        )
        if entry.stage == 0 and entry.mode in {"100644", "100755"}
    )
    governance_current_paths, governance_current_states = (
        _terminal_governance_current_owners(
            registry,
            inventory.current_paths,
            profiles,
            metadata,
        )
    )
    reference_current_packs = _terminal_reference_current_packs(
        registry,
        ria_contract,
        inventory.current_paths,
        profiles,
        metadata,
    )
    return Context(
        root,
        inventory.current_paths,
        frozenset(inventory.baseline_paths),
        profiles,
        texts,
        metadata,
        adapters,
        governance_current_paths,
        governance_current_states,
        reference_current_packs,
        tracked_regular_paths,
        ledger_bytes,
        ria_contract_text,
        getattr(registry, "route_state", "terminal"),
        document_registry=registry if held else None,
        raw_schema=raw_schema,
        read_current_bytes=read_current_bytes,
    )


def _normalize_reference_label(
    value: str,
    *,
    raw_pua_encoded: bool = False,
    opaque_tokens: Sequence[tuple[int, int, str]] = (),
) -> str:
    """Normalize a CommonMark reference label for deterministic lookup."""

    logical: list[str] = []
    raw_length = 0
    tokens_by_start = {start: (end, source) for start, end, source in opaque_tokens}
    cursor = 0
    while cursor < len(value):
        opaque = tokens_by_start.get(cursor)
        if opaque is not None:
            token_end, source = opaque
            logical.append(source)
            raw_length += token_end - cursor
            cursor = token_end
            continue
        character = value[cursor]
        if (
            raw_pua_encoded
            and character == _RAW_PUA_ESCAPE
            and cursor + 1 < len(value)
            and _RAW_PUA_START <= ord(value[cursor + 1]) <= _RAW_PUA_END
        ):
            logical.extend(value[cursor : cursor + 2])
            raw_length += 1
            cursor += 2
            continue
        logical.append(character)
        raw_length += 1
        cursor += 1
    if raw_length > 999:
        return ""
    return re.sub(r"\s+", " ", "".join(logical).strip()).casefold()


def _markdown_escapable(character: str) -> bool:
    """Return whether CommonMark permits backslash-unescaping this ASCII byte."""

    codepoint = ord(character)
    return (
        33 <= codepoint <= 47
        or 58 <= codepoint <= 64
        or 91 <= codepoint <= 96
        or 123 <= codepoint <= 126
    )


_HTML_CHARACTER_REFERENCE = re.compile(
    r"&(?:#[xX][0-9A-Fa-f]{1,6}|#[0-9]{1,7}|"
    r"[A-Za-z][A-Za-z0-9]{1,31});"
)


def _markdown_character_reference(
    value: str, start: int, end: int
) -> tuple[str, int] | None:
    """Decode one unescaped CommonMark character reference."""

    match = _HTML_CHARACTER_REFERENCE.match(value, start, end)
    if match is None:
        return None
    candidate = match.group(0)
    if not candidate.startswith("&#") and candidate[1:] not in html.entities.html5:
        return None
    return html.unescape(candidate), match.end()


def _merge_source_spans(
    spans: Iterable[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    """Merge ordered source ownership spans."""

    merged: list[tuple[int, int]] = []
    for start, end in sorted(spans):
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return tuple(merged)


@dataclass(frozen=True)
class IntervalSweep:
    spans: tuple[tuple[int, int], ...]
    steps: int


@dataclass(frozen=True)
class BacktickCloserScan:
    closer_ends: dict[int, int]
    steps: int


def _ordered_indexed_intervals(
    intervals: Sequence[tuple[int, int]],
) -> list[tuple[int, tuple[int, int]]]:
    """Sort intervals for a sweep while retaining their source order."""

    return sorted(
        enumerate(intervals),
        key=lambda item: (item[1][0], item[1][1], item[0]),
    )


def _intervals_not_contained(
    candidates: Sequence[tuple[int, int]],
    containers: Sequence[tuple[int, int]],
) -> IntervalSweep:
    """Keep intervals not enclosed by any container in O(n log n)."""

    ordered_containers = sorted(containers)
    ordered_candidates = _ordered_indexed_intervals(candidates)
    keep = [True] * len(candidates)
    container_index = 0
    furthest_end = -1
    steps = 0
    for original_index, (candidate_start, candidate_end) in ordered_candidates:
        while (
            container_index < len(ordered_containers)
            and ordered_containers[container_index][0] <= candidate_start
        ):
            furthest_end = max(
                furthest_end,
                ordered_containers[container_index][1],
            )
            container_index += 1
            steps += 1
        steps += 1
        if furthest_end >= candidate_end:
            keep[original_index] = False
    return IntervalSweep(
        tuple(interval for index, interval in enumerate(candidates) if keep[index]),
        steps,
    )


def _intervals_not_overlapping(
    candidates: Sequence[tuple[int, int]],
    blockers: Sequence[tuple[int, int]],
) -> IntervalSweep:
    """Keep intervals disjoint from blockers with one ordered overlap sweep."""

    ordered_blockers = sorted(blockers)
    keep = [True] * len(candidates)
    blocker_index = 0
    steps = 0
    for original_index, (candidate_start, candidate_end) in _ordered_indexed_intervals(
        candidates
    ):
        while (
            blocker_index < len(ordered_blockers)
            and ordered_blockers[blocker_index][1] <= candidate_start
        ):
            blocker_index += 1
            steps += 1
        steps += 1
        if (
            blocker_index < len(ordered_blockers)
            and ordered_blockers[blocker_index][0] < candidate_end
        ):
            keep[original_index] = False
    return IntervalSweep(
        tuple(interval for index, interval in enumerate(candidates) if keep[index]),
        steps,
    )


def _backtick_closer_scan(
    text: str,
    syntax_owned_spans: Sequence[tuple[int, int]],
) -> BacktickCloserScan:
    """Pair unowned backtick runs with one monotonic ownership cursor."""

    owned = _merge_source_spans(syntax_owned_spans)
    closer_ends: dict[int, int] = {}
    owned_index = 0
    steps = 0

    def scan_segment(start: int, end: int) -> None:
        nonlocal owned_index, steps
        runs: list[tuple[int, int, int]] = []
        cursor = start
        while cursor < end:
            steps += 1
            while owned_index < len(owned) and owned[owned_index][1] <= cursor:
                owned_index += 1
                steps += 1
            if (
                owned_index < len(owned)
                and owned[owned_index][0] <= cursor < owned[owned_index][1]
            ):
                cursor = min(end, owned[owned_index][1])
                continue
            if text[cursor] != "`":
                cursor += 1
                continue
            run_start = cursor
            while cursor < end and text[cursor] == "`":
                cursor += 1
            runs.append((run_start, cursor, cursor - run_start))

        nearest: dict[int, int] = {}
        for index in range(len(runs) - 1, -1, -1):
            run_start, _, run_length = runs[index]
            escaped = _source_character_escaped(text, run_start)
            opener_start = run_start + 1 if escaped else run_start
            opener_length = run_length - 1 if escaped else run_length
            if opener_length > 0:
                closer_index = nearest.get(opener_length)
                if closer_index is not None:
                    closer_ends[opener_start] = runs[closer_index][1]
            # A backslash-prefixed raw run remains a full-length closer for
            # already-open code even though only its tail can open code.
            nearest[run_length] = index

    segment_start = 0
    for boundary in re.finditer(r"\n[ \t]*\n", text):
        scan_segment(segment_start, boundary.start())
        segment_start = boundary.end()
    scan_segment(segment_start, len(text))
    return BacktickCloserScan(closer_ends, steps)


def _backtick_closer_ends(
    text: str,
    syntax_owned_spans: Sequence[tuple[int, int]],
) -> dict[int, int]:
    """Map each unowned backtick run to its next equal-length closer."""

    return _backtick_closer_scan(text, syntax_owned_spans).closer_ends


def _inline_code_spans(
    text: str,
    *,
    syntax_owned_spans: Sequence[tuple[int, int]] | None = None,
) -> tuple[tuple[int, int], ...]:
    """Return run-length code spans after higher-priority syntax ownership."""

    owned = (
        _inline_syntax_owned_spans(text)
        if syntax_owned_spans is None
        else _merge_source_spans(syntax_owned_spans)
    )
    closer_ends = _backtick_closer_ends(text, owned)
    spans: list[tuple[int, int]] = []
    consumed_until = -1
    for opener, closer_end in sorted(closer_ends.items()):
        if opener < consumed_until or _source_character_escaped(text, opener):
            continue
        spans.append((opener, closer_end))
        consumed_until = closer_end
    return tuple(spans)


def _mask_inline_code_spans(text: str) -> str:
    """Mask code spans after higher-priority syntax claims its backticks."""

    masked = list(text)
    for start, end in _inline_code_spans(text):
        for offset in range(start, end):
            if masked[offset] != "\n":
                masked[offset] = " "
    return "".join(masked)


@dataclass(frozen=True)
class MarkdownLink:
    start: int
    end: int
    label: str
    target: str


@dataclass(frozen=True)
class RenderedLocalLink:
    """Filesystem-free resolution from the canonical rendered Markdown parser.

    Payload-derived target values are intentionally excluded from the default
    representation so importing validators cannot disclose document content in
    logs or exception rendering.
    """

    kind: str
    raw_target: str = dataclass_field(repr=False)
    target: PurePosixPath | None = dataclass_field(repr=False)


@dataclass(frozen=True)
class BracketSuppression:
    suppressed: frozenset[int]
    steps: int


def _nested_link_suppression(
    parents: dict[int, int | None],
    candidate_openers: frozenset[int],
    resolved_images: frozenset[int],
    source_consumed: frozenset[int],
) -> BracketSuppression:
    """Propagate image and nested-link suppression through the bracket tree."""

    nodes = sorted(parents)
    image_blocked: dict[int, bool] = {}
    eligible_candidates: set[int] = set()
    suppressed = set(candidate_openers.intersection(source_consumed))
    steps = 0
    for opener in nodes:
        parent = parents[opener]
        blocked = parent is not None and (
            parent in resolved_images or image_blocked.get(parent, False)
        )
        image_blocked[opener] = blocked
        if opener in candidate_openers:
            if blocked:
                suppressed.add(opener)
            elif opener not in source_consumed:
                eligible_candidates.add(opener)
        steps += 1

    has_eligible_descendant: dict[int, bool] = {}
    for opener in reversed(nodes):
        descendant = has_eligible_descendant.get(opener, False)
        if opener in eligible_candidates and descendant:
            suppressed.add(opener)
        subtree_has_candidate = descendant or opener in eligible_candidates
        parent = parents[opener]
        if subtree_has_candidate and parent is not None:
            has_eligible_descendant[parent] = True
        steps += 1
    return BracketSuppression(frozenset(suppressed), steps)


def _bracket_pairs(
    value: str,
    *,
    code_spans: Sequence[tuple[int, int]] | None = None,
) -> tuple[dict[int, int], dict[int, int | None]]:
    """Pair brackets and record their containing opener in closing order."""

    stack: list[int] = []
    pairs: dict[int, int] = {}
    parents: dict[int, int | None] = {}
    active_code_spans = (
        _inline_code_spans(value) if code_spans is None else tuple(code_spans)
    )
    code_index = 0
    cursor = 0
    while cursor < len(value):
        while (
            code_index < len(active_code_spans)
            and cursor >= active_code_spans[code_index][1]
        ):
            code_index += 1
        if (
            code_index < len(active_code_spans)
            and active_code_spans[code_index][0]
            <= cursor
            < active_code_spans[code_index][1]
        ):
            cursor = active_code_spans[code_index][1]
            continue
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if character == "[":
            stack.append(cursor)
        elif character == "]" and stack:
            opener = stack.pop()
            pairs[opener] = cursor
            parents[opener] = stack[-1] if stack else None
        cursor += 1
    return pairs, parents


def _source_character_escaped(value: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and value[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


_INLINE_HTML_COMMENT = re.compile(
    r"(?:<!---->|<!--(?:-?[^>-])(?:-?[^-])*?-->)",
    re.DOTALL,
)
_INLINE_COMMENT_OPAQUE = "\U000f0000"
_INLINE_HTML_SPECIAL = (
    _INLINE_HTML_COMMENT,
    re.compile(r"<\?[\s\S]*?\?>"),
    re.compile(r"<![A-Z][\s\S]*?>"),
    re.compile(r"<!\[CDATA\[[\s\S]*?\]\]>"),
)
_RAW_PUA_START = 0xE000
_RAW_PUA_END = 0xF8FF
_RAW_PUA_ESCAPE = chr(_RAW_PUA_START)
_INLINE_HTML_OPAQUE_START = _RAW_PUA_START + 1
_INLINE_HTML_OPAQUE_BASE = _RAW_PUA_END - _INLINE_HTML_OPAQUE_START + 1
_INLINE_HTML_TOKEN_IDS: dict[str, int] = {}
_INLINE_HTML_TOKEN_SOURCES: dict[str, str] = {}


class OpaqueMarkdown(str):
    """HTML-opaque Markdown with encoded-to-source offset provenance."""

    source_offsets: tuple[int, ...]
    opaque_tokens: tuple[tuple[int, int, str], ...]
    opaque_token_starts: tuple[int, ...]
    raw_pua_encoded: bool
    lazy_lines: frozenset[int]

    def __new__(
        cls,
        value: str,
        source_offsets: tuple[int, ...],
        *,
        opaque_tokens: tuple[tuple[int, int, str], ...] = (),
        lazy_lines: frozenset[int] = frozenset(),
    ) -> "OpaqueMarkdown":
        instance = super().__new__(cls, value)
        instance.source_offsets = source_offsets
        instance.opaque_tokens = tuple(
            sorted(opaque_tokens, key=lambda token: (token[0], token[1]))
        )
        instance.opaque_token_starts = tuple(
            token[0] for token in instance.opaque_tokens
        )
        instance.raw_pua_encoded = True
        instance.lazy_lines = lazy_lines
        return instance


@dataclass(frozen=True)
class ReferenceLabelNormalization:
    label: str
    steps: int


def _opaque_token_lower_bound(starts: Sequence[int], target: int) -> tuple[int, int]:
    """Return a deterministic bisect-left result and comparison count."""

    lower = 0
    upper = len(starts)
    steps = 0
    while lower < upper:
        steps += 1
        middle = (lower + upper) // 2
        if starts[middle] < target:
            lower = middle + 1
        else:
            upper = middle
    return lower, steps


def _normalize_reference_label_span_scan(
    value: str, start: int, end: int
) -> ReferenceLabelNormalization:
    """Normalize one label after an indexed opaque-token interval lookup."""

    opaque_tokens: tuple[tuple[int, int, str], ...] = ()
    steps = 0
    if isinstance(value, OpaqueMarkdown):
        token_index, steps = _opaque_token_lower_bound(value.opaque_token_starts, start)
        if token_index > 0:
            token_index -= 1
        contained: list[tuple[int, int, str]] = []
        while token_index < len(value.opaque_tokens):
            token_start, token_end, source = value.opaque_tokens[token_index]
            if token_start >= end:
                break
            steps += 1
            if start <= token_start and token_end <= end:
                contained.append((token_start - start, token_end - start, source))
            token_index += 1
        opaque_tokens = tuple(contained)
    return ReferenceLabelNormalization(
        _normalize_reference_label(
            value[start:end],
            raw_pua_encoded=bool(getattr(value, "raw_pua_encoded", False)),
            opaque_tokens=opaque_tokens,
        ),
        steps,
    )


def _normalize_reference_label_span(value: str, start: int, end: int) -> str:
    """Normalize one label span with structured opaque-token provenance."""

    return _normalize_reference_label_span_scan(value, start, end).label


def _inline_link_destination_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Commit inline suffix ownership once in monotonic source order."""

    closer_ends = _backtick_closer_ends(value, ())
    html_ends = dict(_raw_inline_html_token_spans(value))
    _, definition_spans = _reference_definitions_with_spans(value)
    definition_ends = dict(definition_spans)
    hard_boundary_starts = tuple(
        match.start() for match in re.finditer(r"\n[ \t]*\n", value)
    )

    def label_crosses_hard_boundary(start: int, end: int) -> bool:
        index = bisect.bisect_left(hard_boundary_starts, start)
        return index < len(hard_boundary_starts) and hard_boundary_starts[index] < end

    failed_starts: set[int] = set()
    stack: list[int] = []
    suffix_spans: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(value):
        definition_end = definition_ends.get(cursor)
        if definition_end is not None:
            cursor = definition_end
            continue
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if character == "`":
            run_end = cursor + 1
            while run_end < len(value) and value[run_end] == "`":
                run_end += 1
            closer_end = closer_ends.get(cursor)
            if closer_end is not None:
                cursor = closer_end
            else:
                cursor = run_end
            continue
        html_end = html_ends.get(cursor)
        if html_end is not None:
            cursor = html_end
            continue
        if character == "[":
            stack.append(cursor)
            cursor += 1
            continue
        if character != "]" or not stack:
            cursor += 1
            continue

        opener = stack.pop()
        suffix_start = cursor + 1
        if (
            suffix_start >= len(value)
            or value[suffix_start] != "("
            or label_crosses_hard_boundary(opener + 1, cursor)
        ):
            cursor += 1
            continue
        destination_start = suffix_start + 1
        parsed = (
            None
            if destination_start in failed_starts
            else _inline_link_destination(value, destination_start, failed_starts)
        )
        if parsed is None:
            cursor += 1
            continue
        _, suffix_end = parsed
        suffix_spans.append((suffix_start, suffix_end))
        cursor = suffix_end
    return tuple(suffix_spans)


def _reference_definition_destination_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return destination/title portions of fully valid definitions."""

    _, definition_spans = _reference_definitions_with_spans(value)
    spans: list[tuple[int, int]] = []
    for definition_start, definition_end in definition_spans:
        cursor = definition_start
        while cursor < definition_end and value[cursor] == " ":
            cursor += 1
        if cursor >= definition_end or value[cursor] != "[":
            continue
        cursor += 1
        while cursor < definition_end:
            if (
                value[cursor] == "\\"
                and cursor + 1 < definition_end
                and _markdown_escapable(value[cursor + 1])
            ):
                cursor += 2
                continue
            if (
                value[cursor] == "]"
                and cursor + 1 < definition_end
                and value[cursor + 1] == ":"
            ):
                spans.append((cursor + 1, definition_end))
                break
            cursor += 1
    return tuple(spans)


def _inline_link_syntax_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return valid raw inline/reference destination and title ownership."""

    return _merge_source_spans(
        (
            *_inline_link_destination_spans(value),
            *_reference_definition_destination_spans(value),
        )
    )


def _raw_inline_html_token_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return every quote-aware raw HTML token candidate."""

    spans: list[tuple[int, int]] = []
    cursor = 0
    while cursor < len(value):
        token_start = value.find("<", cursor)
        if token_start < 0:
            break
        if _source_character_escaped(value, token_start):
            cursor = token_start + 1
            continue
        match = _INLINE_HTML_TAG.match(value, token_start)
        if match is None:
            match = next(
                (
                    candidate
                    for pattern in _INLINE_HTML_SPECIAL
                    if (candidate := pattern.match(value, token_start)) is not None
                ),
                None,
            )
        if match is None:
            cursor = token_start + 1
            continue
        if re.search(r"\n[ \t]*\n", match.group(0)) is not None:
            cursor = token_start + 1
            continue
        token_end = match.end()
        spans.append((token_start, token_end))
        cursor = token_end
    return tuple(spans)


def _inline_syntax_ownership(
    value: str,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    """Resolve nested link-suffix and HTML-token ownership by containment."""

    link_candidates = _inline_link_syntax_spans(value)
    html_candidates = _raw_inline_html_token_spans(value)
    html_spans = _intervals_not_contained(html_candidates, link_candidates).spans
    link_spans = _intervals_not_contained(link_candidates, html_spans).spans
    return link_spans, html_spans


def _inline_syntax_owned_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return raw link and HTML spans whose backticks are syntax-owned."""

    link_spans, html_spans = _inline_syntax_ownership(value)
    return _merge_source_spans((*link_spans, *html_spans))


def _inline_html_token_spans(
    value: str,
) -> tuple[tuple[int, int], ...]:
    """Return HTML candidates not rendered inside resulting code spans."""

    link_spans, raw_html_spans = _inline_syntax_ownership(value)
    syntax_owned = _merge_source_spans((*link_spans, *raw_html_spans))
    code_spans = _inline_code_spans(value, syntax_owned_spans=syntax_owned)
    return _intervals_not_overlapping(raw_html_spans, code_spans).spans


def _mask_inline_html_tokens(value: str) -> OpaqueMarkdown:
    """Namespace raw BMP PUA input and replace inline HTML with opaque IDs."""

    output: list[str] = []
    source_offsets: list[int] = []
    opaque_tokens: list[tuple[int, int, str]] = []
    cursor = 0

    def append_raw(start: int, end: int) -> None:
        for index in range(start, end):
            character = value[index]
            if _RAW_PUA_START <= ord(character) <= _RAW_PUA_END:
                output.extend((_RAW_PUA_ESCAPE, character))
                source_offsets.extend((index, index))
            else:
                output.append(character)
                source_offsets.append(index)

    for token_start, token_end in _inline_html_token_spans(value):
        append_raw(cursor, token_start)
        token = value[token_start:token_end]
        token_id = _INLINE_HTML_TOKEN_IDS.setdefault(token, len(_INLINE_HTML_TOKEN_IDS))
        opaque = list(token)
        opaque_positions = [
            index for index, character in enumerate(token) if character not in "\r\n"
        ]
        if token_id >= _INLINE_HTML_OPAQUE_BASE ** len(opaque_positions):
            raise ConfigurationError("inline HTML opaque identity exhausted")
        remaining = token_id
        for position in reversed(opaque_positions):
            opaque[position] = chr(
                _INLINE_HTML_OPAQUE_START + remaining % _INLINE_HTML_OPAQUE_BASE
            )
            remaining //= _INLINE_HTML_OPAQUE_BASE
        identity = "".join(opaque)
        source = _INLINE_HTML_TOKEN_SOURCES.setdefault(identity, token)
        if source != token:
            raise ConfigurationError("inline HTML opaque identity collision")
        encoded_start = len(output)
        output.extend(identity)
        opaque_tokens.append((encoded_start, len(output), token))
        source_offsets.extend(range(token_start, token_end))
        cursor = token_end
    append_raw(cursor, len(value))
    return OpaqueMarkdown(
        "".join(output),
        tuple(source_offsets),
        opaque_tokens=tuple(opaque_tokens),
        lazy_lines=getattr(value, "lazy_lines", frozenset()),
    )


def _decode_raw_pua_namespace(value: str) -> str:
    """Decode injectively escaped raw BMP PUA characters."""

    output: list[str] = []
    cursor = 0
    while cursor < len(value):
        if (
            value[cursor] == _RAW_PUA_ESCAPE
            and cursor + 1 < len(value)
            and _RAW_PUA_START <= ord(value[cursor + 1]) <= _RAW_PUA_END
        ):
            output.append(value[cursor + 1])
            cursor += 2
            continue
        output.append(value[cursor])
        cursor += 1
    return "".join(output)


def _rendered_inline_html_text(value: str) -> str:
    """Drop inline HTML markup while preserving its visible child text."""

    output: list[str] = []
    cursor = 0
    for token_start, token_end in _inline_html_token_spans(value):
        output.append(value[cursor:token_start])
        cursor = token_end
    output.append(value[cursor:])
    return "".join(output).replace(_INLINE_COMMENT_OPAQUE, "")


def _image_bracket_opener(value: str, opener: int) -> bool:
    return (
        opener > 0
        and value[opener - 1] == "!"
        and not _source_character_escaped(value, opener - 1)
    )


def _ascii_control(character: str) -> bool:
    """Return whether one character is an ASCII control byte."""

    codepoint = ord(character)
    return codepoint <= 0x1F or codepoint == 0x7F


def _markdown_link_separator_end(value: str, start: int, end: int) -> tuple[int, bool]:
    """Consume CommonMark space/tab plus at most one line ending."""

    cursor = start
    while cursor < end and value[cursor] in " \t":
        cursor += 1
    if cursor < end and value[cursor] in "\r\n":
        if value[cursor] == "\r" and cursor + 1 < end and value[cursor + 1] == "\n":
            cursor += 2
        else:
            cursor += 1
        while cursor < end and value[cursor] in " \t":
            cursor += 1
    return cursor, cursor > start


def _markdown_destination(value: str, start: int, end: int) -> tuple[str, int] | None:
    """Parse one destination and return its unescaped value and end offset."""

    cursor, _ = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return "", cursor
    if value[cursor] == "<":
        cursor += 1
        target: list[str] = []
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == ">":
                return "".join(target), cursor + 1
            if character in {"\r", "\n", "<"}:
                return None
            target.append(character)
            cursor += 1
        return None

    target = []
    depth = 0
    while cursor < end:
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < end
            and _markdown_escapable(value[cursor + 1])
        ):
            target.append(value[cursor + 1])
            cursor += 2
            continue
        if character == "&":
            reference = _markdown_character_reference(value, cursor, end)
            if reference is not None:
                decoded, cursor = reference
                target.append(decoded)
                continue
        if character == " " or _ascii_control(character):
            if depth == 0 and character in " \t\r\n":
                break
            return None
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                return None
            depth -= 1
        target.append(character)
        cursor += 1
    return ("".join(target), cursor) if depth == 0 else None


def _markdown_title_end(value: str, start: int, end: int) -> int | None:
    """Return the offset after one quoted/parenthesized Markdown title."""

    cursor = start
    opener = value[cursor]
    closer = {'"': '"', "'": "'", "(": ")"}.get(opener)
    if closer is None:
        return None
    cursor += 1
    while cursor < end:
        character = value[cursor]
        if (
            character == "\\"
            and cursor + 1 < end
            and _markdown_escapable(value[cursor + 1])
        ):
            cursor += 2
            continue
        if opener == "(" and character == "(":
            return None
        if character == closer:
            return cursor + 1
        cursor += 1
    return None


def _valid_markdown_title(value: str, start: int, end: int) -> bool:
    """Accept an empty remainder or exactly one quoted/parenthesized title."""

    cursor, _ = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return True
    title_end = _markdown_title_end(value, cursor, end)
    if title_end is None:
        return False
    cursor, _ = _markdown_link_separator_end(value, title_end, end)
    return cursor == end


def _link_destination(value: str, start: int, end: int) -> str | None:
    """Parse a destination and validate its complete optional-title remainder."""

    parsed = _markdown_destination(value, start, end)
    if parsed is None:
        return None
    target, consumed = parsed
    if consumed == end:
        return target
    _, separated = _markdown_link_separator_end(value, consumed, end)
    if not separated:
        return None
    return target if _valid_markdown_title(value, consumed, end) else None


def _inline_link_destination(
    value: str, start: int, failed_starts: set[int] | None = None
) -> tuple[str, int] | None:
    """Consume an inline destination, optional title, and real outer closer."""

    end = len(value)
    cursor, leading_space = _markdown_link_separator_end(value, start, end)
    if cursor >= end:
        return None

    target: list[str] = []
    empty_destination_title = False
    unmatched_openers = [start - 1]
    if value[cursor] == "<":
        cursor += 1
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == ">":
                cursor += 1
                break
            if character in {"\r", "\n", "<"}:
                return None
            target.append(character)
            cursor += 1
        else:
            return None
    elif value[cursor] == ")":
        return "", cursor + 1
    elif leading_space and value[cursor] in {'"', "'", "("}:
        empty_destination_title = True
    else:
        depth = 0
        while cursor < end:
            character = value[cursor]
            if (
                character == "\\"
                and cursor + 1 < end
                and _markdown_escapable(value[cursor + 1])
            ):
                target.append(value[cursor + 1])
                cursor += 2
                continue
            if character == "&":
                reference = _markdown_character_reference(value, cursor, end)
                if reference is not None:
                    decoded, cursor = reference
                    target.append(decoded)
                    continue
            if character == " " or _ascii_control(character):
                if depth == 0 and character in " \t\r\n":
                    break
                return None
            if character == "(":
                depth += 1
                unmatched_openers.append(cursor)
            elif character == ")":
                if depth == 0:
                    return "".join(target), cursor + 1
                depth -= 1
                unmatched_openers.pop()
            target.append(character)
            cursor += 1
        if depth != 0:
            if failed_starts is not None:
                failed_starts.update(opener + 1 for opener in unmatched_openers)
            return None

    if empty_destination_title:
        title_end = _markdown_title_end(value, cursor, end)
        if title_end is None:
            return None
        cursor, _ = _markdown_link_separator_end(value, title_end, end)
        if cursor >= end or value[cursor] != ")":
            return None
        return "", cursor + 1

    if cursor < end and value[cursor] == ")":
        return "".join(target), cursor + 1
    separator_end, separated = _markdown_link_separator_end(value, cursor, end)
    if cursor >= end or not separated:
        return None
    cursor = separator_end
    if cursor < end and value[cursor] == ")":
        return "".join(target), cursor + 1
    if cursor >= end:
        return None
    title_end = _markdown_title_end(value, cursor, end)
    if title_end is None:
        return None
    cursor, _ = _markdown_link_separator_end(value, title_end, end)
    if cursor >= end or value[cursor] != ")":
        return None
    return "".join(target), cursor + 1


def _reference_definitions_with_spans(
    value: str,
    *,
    lazy_lines: frozenset[int] | None = None,
) -> tuple[dict[str, str], tuple[tuple[int, int], ...]]:
    """Parse valid definitions and their complete, offset-stable source spans."""

    if lazy_lines is None:
        lazy_lines = getattr(value, "lazy_lines", frozenset())
    definitions: dict[str, str] = {}
    spans: list[tuple[int, int]] = []
    lines: list[tuple[str, int, int]] = []
    offset = 0
    for source_line in _commonmark_splitlines(value, keepends=True):
        line = source_line.rstrip("\r\n")
        lines.append((line, offset, offset + len(line)))
        offset += len(source_line)

    def parse_definition(
        index: int,
    ) -> tuple[str, str, int, int] | None:
        line, definition_start, definition_end = lines[index]

        opener = len(line) - len(line.lstrip(" "))
        if opener > 3 or opener >= len(line) or line[opener] != "[":
            return None

        label_start = opener + 1
        label_end: int | None = None
        label_end_index = index
        while label_end_index < len(lines):
            label_line = lines[label_end_index][0]
            if label_end_index > index and _commonmark_blank_line(label_line):
                return None
            cursor = label_start if label_end_index == index else 0
            while cursor < len(label_line):
                character = label_line[cursor]
                if (
                    character == "\\"
                    and cursor + 1 < len(label_line)
                    and _markdown_escapable(label_line[cursor + 1])
                ):
                    cursor += 2
                    continue
                if character == "[":
                    return None
                if character == "]":
                    label_end = cursor
                    break
                cursor += 1
            if label_end is not None:
                break
            label_end_index += 1
        if (
            label_end is None
            or label_end + 1 >= len(lines[label_end_index][0])
            or lines[label_end_index][0][label_end + 1] != ":"
        ):
            return None

        label = _normalize_reference_label_span(
            value,
            lines[index][1] + label_start,
            lines[label_end_index][1] + label_end,
        )
        if not label:
            return None

        def continuation_content(source: str) -> str | None:
            """Return content indented by at most four visual columns."""

            continuation_cursor = 0
            column = 0
            while (
                continuation_cursor < len(source)
                and source[continuation_cursor] in " \t"
            ):
                if source[continuation_cursor] == " ":
                    next_column = column + 1
                else:
                    next_column = column + (4 - column % 4)
                if next_column > 4:
                    return None
                column = next_column
                continuation_cursor += 1
            content = source[continuation_cursor:]
            return content if content else None

        def title_end_index(first_title: str, first_index: int) -> int | None:
            if not first_title or first_title[0] not in {'"', "'", "("}:
                return None
            closer = ")" if first_title[0] == "(" else first_title[0]
            title_index = first_index
            source = first_title
            title_cursor = 1
            while True:
                while title_cursor < len(source):
                    character = source[title_cursor]
                    if (
                        character == "\\"
                        and title_cursor + 1 < len(source)
                        and _markdown_escapable(source[title_cursor + 1])
                    ):
                        title_cursor += 2
                        continue
                    if first_title[0] == "(" and character == "(":
                        return None
                    if character == closer:
                        if source[title_cursor + 1 :].strip(" \t"):
                            return None
                        return title_index
                    title_cursor += 1
                title_index += 1
                if title_index >= len(lines) or _commonmark_blank_line(
                    lines[title_index][0]
                ):
                    return None
                source = lines[title_index][0]
                title_cursor = 0

        label_line, _, definition_end = lines[label_end_index]
        after_colon = label_line[label_end + 2 :]
        destination = after_colon.lstrip(" \t")
        destination_index = label_end_index
        span_end = definition_end
        if not destination:
            if label_end_index + 1 >= len(lines):
                return None
            continuation = continuation_content(lines[label_end_index + 1][0])
            if continuation is None:
                return None
            destination = continuation
            destination_index = label_end_index + 1
            span_end = lines[destination_index][2]

        parsed = _markdown_destination(destination, 0, len(destination))
        if parsed is None:
            return None
        target, consumed = parsed
        separator_end, separated = _markdown_link_separator_end(
            destination, consumed, len(destination)
        )
        if consumed < len(destination) and not separated:
            return None
        title_on_destination = separator_end < len(destination)
        definition_end_index = destination_index
        if title_on_destination:
            title = destination[separator_end:]
            parsed_title_index = title_end_index(title, destination_index)
            if parsed_title_index is None:
                return None
            definition_end_index = parsed_title_index
            span_end = lines[parsed_title_index][2]
        elif destination_index + 1 < len(lines):
            title = continuation_content(lines[destination_index + 1][0])
            if title is not None and title[0] in {'"', "'", "("}:
                parsed_title_index = title_end_index(title, destination_index + 1)
                if parsed_title_index is not None:
                    definition_end_index = parsed_title_index
                    span_end = lines[parsed_title_index][2]

        return (
            label,
            target,
            span_end,
            definition_end_index,
        )

    index = 0
    paragraph_open = False
    atx_heading = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    setext_delimiter = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic_break = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )
    while index < len(lines):
        line, definition_start, _ = lines[index]
        if not line.strip():
            paragraph_open = False
            index += 1
            continue
        if (
            atx_heading.fullmatch(line) is not None
            or thematic_break.fullmatch(line) is not None
            or (
                paragraph_open
                and index not in lazy_lines
                and setext_delimiter.fullmatch(line) is not None
            )
        ):
            paragraph_open = False
            index += 1
            continue
        if paragraph_open:
            index += 1
            continue
        parsed = parse_definition(index)
        if parsed is None:
            paragraph_open = True
            index += 1
            continue
        label, target, span_end, definition_end_index = parsed
        definitions.setdefault(label, target)
        spans.append((definition_start, span_end))
        index = definition_end_index + 1
    return definitions, tuple(spans)


def _reference_definitions(value: str) -> dict[str, str]:
    """Parse first-wins rendered definitions, including continued targets."""

    definitions, _ = _reference_definitions_with_spans(value)
    return definitions


def _mask_source_spans(value: str, spans: Sequence[tuple[int, int]]) -> str:
    """Mask exact source spans while preserving line and character offsets."""

    masked = list(value)
    for start, end in spans:
        for index in range(start, end):
            if masked[index] not in {"\r", "\n"}:
                masked[index] = " "
    result = "".join(masked)
    if isinstance(value, OpaqueMarkdown):
        return OpaqueMarkdown(
            result,
            value.source_offsets,
            opaque_tokens=value.opaque_tokens,
            lazy_lines=value.lazy_lines,
        )
    return result


def _crosses_hard_inline_boundary(value: str) -> bool:
    return re.search(r"\n[ \t]*\n", value) is not None


def _scan_markdown_links(
    value: str, definitions: dict[str, str]
) -> tuple[MarkdownLink, ...]:
    """Resolve link/image bracket state in closing-token order."""

    brackets, parents = _bracket_pairs(value)
    hard_boundary_starts = tuple(
        match.start() for match in re.finditer(r"\n[ \t]*\n", value)
    )

    def crosses_hard_boundary(start: int, end: int) -> bool:
        index = bisect.bisect_left(hard_boundary_starts, start)
        return index < len(hard_boundary_starts) and hard_boundary_starts[index] < end

    candidates: dict[int, MarkdownLink] = {}
    resolved_images: set[int] = set()
    consumed: set[int] = set()
    consumed_source_spans: list[tuple[int, int]] = []
    failed_inline_starts: set[int] = set()
    for opener, label_end in brackets.items():
        if opener in consumed:
            continue
        if crosses_hard_boundary(opener + 1, label_end):
            continue
        suffix = label_end + 1
        candidate: MarkdownLink | None = None
        inline_consumed = False
        if suffix < len(value) and value[suffix] == "(":
            destination_start = suffix + 1
            parsed = (
                None
                if destination_start in failed_inline_starts
                else _inline_link_destination(
                    value, destination_start, failed_inline_starts
                )
            )
            if parsed is not None:
                target, link_end = parsed
                if not crosses_hard_boundary(suffix + 1, link_end - 1):
                    candidate = MarkdownLink(opener, link_end, "", target)
                    inline_consumed = True
            if candidate is None:
                key = _normalize_reference_label_span(value, opener + 1, label_end)
                if key and key in definitions:
                    candidate = MarkdownLink(opener, suffix, "", definitions[key])
        elif suffix < len(value) and value[suffix] == "[":
            reference_end = brackets.get(suffix)
            if reference_end is not None:
                explicit_reference = suffix + 1 < reference_end
                key_start, key_end = (
                    (suffix + 1, reference_end)
                    if explicit_reference
                    else (opener + 1, label_end)
                )
                key = _normalize_reference_label_span(value, key_start, key_end)
                if (
                    not crosses_hard_boundary(key_start, key_end)
                    and bool(key)
                    and key in definitions
                ):
                    candidate = MarkdownLink(
                        opener,
                        reference_end + 1,
                        "",
                        definitions[key],
                    )
                    consumed.add(suffix)
        else:
            after = suffix
            while after < len(value) and value[after] in " \t":
                after += 1
            key = _normalize_reference_label_span(value, opener + 1, label_end)
            if after < len(value) and value[after] == ":":
                continue
            if key and key in definitions:
                candidate = MarkdownLink(opener, suffix, "", definitions[key])
        if candidate is None:
            continue
        if inline_consumed:
            consumed_source_spans.append((suffix, candidate.end))
        if _image_bracket_opener(value, opener):
            resolved_images.add(opener)
            continue

        candidates[opener] = candidate

    merged_spans: list[tuple[int, int]] = []
    for start, end in sorted(consumed_source_spans):
        if merged_spans and start <= merged_spans[-1][1]:
            merged_spans[-1] = (
                merged_spans[-1][0],
                max(end, merged_spans[-1][1]),
            )
        else:
            merged_spans.append((start, end))
    source_consumed: set[int] = set()
    span_index = 0
    for opener in sorted(brackets):
        while span_index < len(merged_spans) and opener >= merged_spans[span_index][1]:
            span_index += 1
        if (
            span_index < len(merged_spans)
            and merged_spans[span_index][0] < opener < merged_spans[span_index][1]
        ):
            source_consumed.add(opener)
    resolved_images.difference_update(source_consumed)

    suppressed = _nested_link_suppression(
        parents,
        frozenset(candidates),
        frozenset(resolved_images),
        frozenset(source_consumed),
    ).suppressed

    return tuple(
        MarkdownLink(
            link.start,
            link.end,
            value[opener + 1 : brackets[opener]],
            link.target,
        )
        for opener in sorted(candidates)
        if opener not in suppressed
        for link in (candidates[opener],)
    )


def _extract_rendered_links(
    rendered: str, *, definitions_rendered: str | None = None
) -> tuple[str, ...]:
    """Extract links from an already block-rendered Markdown view."""

    visible_lazy_lines = getattr(rendered, "lazy_lines", frozenset())
    visible = _mask_inline_html_tokens(rendered)
    definition_lazy_lines = (
        getattr(definitions_rendered, "lazy_lines", frozenset())
        if definitions_rendered is not None
        else visible_lazy_lines
    )
    definition_source = (
        _mask_inline_html_tokens(definitions_rendered)
        if definitions_rendered is not None
        else visible
    )
    definitions, definition_spans = _reference_definitions_with_spans(
        definition_source,
        lazy_lines=definition_lazy_lines,
    )
    if definitions_rendered is not None:
        _, definition_spans = _reference_definitions_with_spans(
            visible,
            lazy_lines=visible_lazy_lines,
        )
    scan_source = _mask_source_spans(visible, definition_spans)
    code_masked = _mask_inline_code_spans(scan_source)
    return tuple(
        _decode_raw_pua_namespace(link.target)
        for link in _scan_markdown_links(scan_source, definitions)
        if code_masked[link.start] != " "
    )


def _extract_links(
    text: str, *, definitions_text: str | None = None
) -> tuple[str, ...]:
    rendered = _rendered_markdown(text)
    definitions_rendered = (
        _rendered_markdown(definitions_text) if definitions_text is not None else None
    )
    return _extract_rendered_links(rendered, definitions_rendered=definitions_rendered)


def _local_destination(
    source: PurePosixPath, raw: str
) -> tuple[str, PurePosixPath | None]:
    value = raw
    lowered = value.casefold()
    if lowered.startswith("file:"):
        return "LINK-FILE-URI", None
    if value.startswith("//"):
        return "external", None
    if value.startswith("/") or re.match(r"^[A-Za-z]:[/\\]", value):
        return "LINK-ABSOLUTE", None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return "external", None
    path_part = value.split("#", 1)[0].split("?", 1)[0]
    path_part = unquote(path_part)
    if not path_part:
        return "anchor", source
    normalized = posixpath.normpath(posixpath.join(source.parent.as_posix(), path_part))
    if normalized == ".." or normalized.startswith("../"):
        return "LINK-ESCAPE", None
    return "local", PurePosixPath(normalized)


def rendered_local_links(
    markdown: str,
    source_path: str | PurePosixPath,
) -> tuple[RenderedLocalLink, ...]:
    """Resolve rendered Markdown links without consulting the filesystem.

    This is the narrow public adapter for validators that need the canonical
    CommonMark renderer and local-destination semantics but own a different
    storage context, such as an immutable Git source tree.  Callers decide how
    a resolved local path exists; this function never opens or stats it.
    """

    if not isinstance(markdown, str):
        raise TypeError("markdown must be text")
    raw_source = (
        source_path.as_posix()
        if isinstance(source_path, PurePosixPath)
        else source_path
    )
    if not isinstance(raw_source, str) or not raw_source:
        raise ValueError("source_path must be a repository-relative POSIX path")
    source = PurePosixPath(raw_source)
    if (
        not source.parts
        or source.is_absolute()
        or source.as_posix() != raw_source
        or "." in source.parts
        or ".." in source.parts
        or "\\" in raw_source
        or any(ord(character) < 32 or ord(character) == 127 for character in raw_source)
    ):
        raise ValueError(
            "source_path must be a canonical repository-relative POSIX path"
        )

    return tuple(
        RenderedLocalLink(kind=kind, raw_target=raw, target=target)
        for raw in _extract_links(markdown)
        for kind, target in (_local_destination(source, raw),)
    )


def _path_exists_without_dereference(
    root: Path, path: PurePosixPath, adapters: dict[PurePosixPath, PurePosixPath]
) -> bool:
    current = root
    relative = PurePosixPath()
    for index, part in enumerate(path.parts):
        current = current / part
        relative = relative / part
        try:
            mode = current.lstat().st_mode
        except (FileNotFoundError, OSError):
            return False
        if stat.S_ISLNK(mode):
            if relative not in adapters:
                return False
            if index == len(path.parts) - 1:
                return True
            canonical = adapters[relative].joinpath(*path.parts[index + 1 :])
            return _path_exists_without_dereference(root, canonical, adapters)
    return True


def _is_current_authority(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    return profile.mode == "authored" and status in {"active", "accepted"}


def _work109_expected_stable_path(
    legacy: PurePosixPath,
) -> PurePosixPath | None:
    """Return the sole four-digit active route admitted for one legacy path."""

    value = legacy.as_posix()
    requirement = re.fullmatch(
        r"docs/01\.requirements/(?P<id>[0-9]{3})(?P<tail>-[a-z0-9]+(?:-[a-z0-9]+)*\.md)",
        value,
    )
    if requirement is not None:
        return PurePosixPath(
            "docs/01.requirements/"
            f"{int(requirement.group('id')):04d}{requirement.group('tail')}"
        )
    work_unit = re.fullmatch(
        r"docs/03\.specs/(?P<id>[0-9]{3})"
        r"(?P<tail>-[a-z0-9]+(?:-[a-z0-9]+)*/"
        r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.md)",
        value,
    )
    if work_unit is not None:
        return PurePosixPath(
            f"docs/03.specs/{int(work_unit.group('id')):04d}{work_unit.group('tail')}"
        )
    return None


def _work109_git_blob_oid(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()  # noqa: S324


@lru_cache(maxsize=8)
def _commit_path_evidence(
    root_value: str,
    commit: str,
    paths: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    """Read immutable Git provenance once per exact commit/path projection."""

    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RiaGitError("commit evidence differs")
    requests: list[str] = []
    for value in paths:
        path = PurePosixPath(value)
        if (
            path.as_posix() != value
            or path.is_absolute()
            or ".." in path.parts
            or "\n" in value
            or "\r" in value
        ):
            raise RiaGitError("commit path evidence differs")
        requests.append(f"{commit}:{value}")
    completed = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=Path(root_value),
        input=("\n".join(requests) + "\n").encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0 or completed.stderr:
        raise RiaGitError("commit evidence differs")
    output = completed.stdout
    cursor = 0
    evidence: list[tuple[str, str]] = []
    for _ in requests:
        header_end = output.find(b"\n", cursor)
        if header_end < 0:
            raise RiaGitError("commit evidence differs")
        header = output[cursor:header_end].decode("ascii", "strict").split()
        if (
            len(header) != 3
            or re.fullmatch(r"[0-9a-f]{40}", header[0]) is None
            or header[1] != "blob"
            or not header[2].isdigit()
        ):
            raise RiaGitError("commit evidence differs")
        size = int(header[2])
        start = header_end + 1
        end = start + size
        if end >= len(output) or output[end : end + 1] != b"\n":
            raise RiaGitError("commit evidence differs")
        payload = output[start:end]
        evidence.append((header[0], hashlib.sha256(payload).hexdigest()))
        cursor = end + 1
    if cursor != len(output):
        raise RiaGitError("commit evidence differs")
    return tuple(evidence)


def _work109_migration_projection(
    context: Context,
) -> tuple[
    dict[PurePosixPath, PurePosixPath],
    dict[PurePosixPath, PurePosixPath],
    dict[PurePosixPath, PurePosixPath],
]:
    """Validate MIG-0002 and return its exact move/replace/merge maps."""

    if (
        WORK109_MIGRATION_PATH not in context.paths
        or WORK109_MIGRATION_PATH not in context.tracked_regular_paths
    ):
        raise ConfigurationError("WORK-109 migration ledger is unavailable")
    metadata = context.metadata.get(WORK109_MIGRATION_PATH, {})
    if (
        metadata.get("artifact_id") != "MIG-0002"
        or metadata.get("migration_id") != "MIG-0002"
        or metadata.get("status") != "accepted"
    ):
        raise ConfigurationError("WORK-109 migration ledger identity differs")
    text = context.texts.get(WORK109_MIGRATION_PATH)
    marker = f"{WORK109_LEDGER_MARKER}\n\n```json\n"
    if text is None or text.count(marker) != 1:
        raise ConfigurationError("WORK-109 migration ledger contract differs")
    prefix, remainder = text.split(marker, 1)
    if not prefix or remainder.count("\n```") != 1:
        raise ConfigurationError("WORK-109 migration ledger contract differs")
    raw, suffix = remainder.split("\n```", 1)
    if not suffix.startswith("\n"):
        raise ConfigurationError("WORK-109 migration ledger contract differs")
    try:
        rows = json.loads(raw)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ConfigurationError("WORK-109 migration ledger contract differs") from exc
    if not isinstance(rows, list) or len(rows) != 154:
        raise ConfigurationError("WORK-109 migration ledger row count differs")
    legacy_values = [
        row.get("legacy_path") if isinstance(row, Mapping) else None for row in rows
    ]
    if (
        any(not isinstance(value, str) for value in legacy_values)
        or legacy_values != sorted(legacy_values)
        or len(set(legacy_values)) != len(legacy_values)
    ):
        raise ConfigurationError("WORK-109 migration ledger order differs")
    try:
        source_evidence = _commit_path_evidence(
            str(context.root.absolute()),
            WORK109_SOURCE_COMMIT,
            tuple(legacy_values),
        )
    except (RiaContractError, RiaGitError):
        raise ConfigurationError("WORK-109 migration ledger source differs") from None

    wp004b_targets = _work054_wp004b_targets(context)
    successors = _generic_migration_targets(context)
    aliases: dict[PurePosixPath, PurePosixPath] = {}
    replacements: dict[PurePosixPath, PurePosixPath] = {}
    merges: dict[PurePosixPath, PurePosixPath] = {}
    stable_paths: set[PurePosixPath] = set()
    pre_cutover_stable_paths: set[PurePosixPath] = set()
    for row, (source_blob, content_sha256) in zip(
        rows,
        source_evidence,
        strict=True,
    ):
        if (
            not isinstance(row, Mapping)
            or tuple(row) != WORK109_LEDGER_FIELDS
            or row.get("source_commit") != WORK109_SOURCE_COMMIT
            or not isinstance(row.get("source_blob"), str)
            or re.fullmatch(r"[0-9a-f]{40}", row["source_blob"]) is None
            or not isinstance(row.get("content_sha256"), str)
            or re.fullmatch(r"[0-9a-f]{64}", row["content_sha256"]) is None
            or not isinstance(row.get("reason"), str)
            or not row["reason"].strip()
        ):
            raise ConfigurationError("WORK-109 migration ledger entry differs")
        legacy_value = row["legacy_path"]
        if not isinstance(legacy_value, str):
            raise ConfigurationError("WORK-109 migration ledger path differs")
        legacy = PurePosixPath(legacy_value)
        if (
            legacy.as_posix() != legacy_value
            or legacy.is_absolute()
            or ".." in legacy.parts
        ):
            raise ConfigurationError("WORK-109 migration ledger path differs")
        if source_blob != row["source_blob"] or content_sha256 != row["content_sha256"]:
            raise ConfigurationError("WORK-109 migration ledger source differs")

        if row.get("action") == "moved":
            stable_value = row.get("stable_path")
            artifact_id = row.get("artifact_id")
            expected = _work109_expected_stable_path(legacy)
            has_wp004b_cutover = expected in wp004b_targets
            current_target = (
                wp004b_targets.get(expected) if expected is not None else None
            )
            if current_target is None:
                current_target = expected
            current_target = successors.get(current_target, current_target)
            if (
                not isinstance(stable_value, str)
                or expected is None
                or stable_value != expected.as_posix()
                or row.get("replacement") is not None
                or not isinstance(artifact_id, str)
                or expected in pre_cutover_stable_paths
                or current_target not in context.tracked_regular_paths
                or not _path_exists_without_dereference(
                    context.root, current_target, context.adapter_targets
                )
                or (
                    not has_wp004b_cutover
                    and context.metadata.get(expected, {}).get("artifact_id")
                    != artifact_id
                )
            ):
                raise ConfigurationError(
                    f"WORK-109 migration ledger target differs: {legacy.as_posix()}"
                )
            aliases[legacy] = current_target
            stable_paths.add(current_target)
            pre_cutover_stable_paths.add(expected)
            continue

        action = row.get("action")
        replacement_value = row.get("replacement")
        expected_map = WORK109_REPLACEMENTS if action == "replaced" else WORK109_MERGES
        expected_replacement = expected_map.get(legacy)
        current_replacement = (
            wp004b_targets.get(expected_replacement)
            if expected_replacement is not None
            else None
        )
        if current_replacement is None:
            current_replacement = expected_replacement
        current_replacement = successors.get(current_replacement, current_replacement)
        if (
            action not in {"replaced", "merged"}
            or row.get("stable_path") is not None
            or row.get("artifact_id") is not None
            or not isinstance(replacement_value, str)
            or expected_replacement is None
            or replacement_value != expected_replacement.as_posix()
            or current_replacement not in context.tracked_regular_paths
            or not _path_exists_without_dereference(
                context.root, current_replacement, context.adapter_targets
            )
        ):
            raise ConfigurationError("WORK-109 migration ledger replacement differs")
        if action == "replaced":
            replacements[legacy] = current_replacement
        else:
            merges[legacy] = current_replacement

    if (
        len(aliases) != 141
        or len(pre_cutover_stable_paths) != 141
        or set(replacements) != set(WORK109_REPLACEMENTS)
        or set(merges) != set(WORK109_MERGES)
    ):
        raise ConfigurationError("WORK-109 migration ledger coverage differs")
    return aliases, replacements, merges


def _work054_wp004b_targets(
    context: Context,
) -> dict[PurePosixPath, PurePosixPath]:
    """Return terminal targets from MIG-0004's row-level recovery proof."""

    if (
        WORK054_WP004B_MIGRATION_PATH not in context.paths
        or WORK054_WP004B_MIGRATION_PATH not in context.tracked_regular_paths
    ):
        raise ConfigurationError("WORK-054 WP-004B migration ledger is unavailable")
    text = context.texts.get(WORK054_WP004B_MIGRATION_PATH)
    if text is None:
        raise ConfigurationError("WORK-054 WP-004B migration ledger differs")
    try:
        rows = validate_pinned_migration_recovery(
            context.root,
            WORK054_WP004B_MIGRATION_PATH.as_posix(),
            text.encode("utf-8"),
        )
    except (ArchiveContractError, OSError, UnicodeError, ValueError) as exc:
        raise ConfigurationError(
            "WORK-054 WP-004B migration recovery proof differs"
        ) from exc
    targets: dict[PurePosixPath, PurePosixPath] = {}
    for row in rows:
        action = row.get("action")
        legacy_value = row.get("legacy_path")
        target_value = (
            row.get("stable_path") if action == "moved" else row.get("replacement")
        )
        if not isinstance(legacy_value, str) or not isinstance(target_value, str):
            raise ConfigurationError("WORK-054 WP-004B migration row differs")
        legacy = PurePosixPath(legacy_value)
        target = PurePosixPath(target_value)
        if (
            legacy.as_posix() != legacy_value
            or target.as_posix() != target_value
            or legacy.is_absolute()
            or target.is_absolute()
            or ".." in legacy.parts
            or ".." in target.parts
            or legacy in targets
            or target not in context.tracked_regular_paths
            or not _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            )
        ):
            raise ConfigurationError("WORK-054 WP-004B migration target differs")
        targets[legacy] = target
    return targets


def _work109_four_digit_aliases(
    context: Context,
) -> dict[PurePosixPath, PurePosixPath]:
    """Return only the exact active-route moves from validated MIG-0002."""

    aliases, _, _ = _work109_migration_projection(context)
    return aliases


def _context_migration_proof(context: Context) -> MigrationProof:
    registry = getattr(context, "document_registry", None)
    raw_schema = getattr(context, "raw_schema", _UNSET)
    read_current_bytes = getattr(context, "read_current_bytes", None)
    try:
        if _held_context_inputs(registry, raw_schema, read_current_bytes):
            return repository_migration_proof(
                context.root,
                registry=registry,
                raw_schema=raw_schema,
                read_current_bytes=read_current_bytes,
            )
        return repository_migration_proof(context.root)
    except (ArchiveContractError, OSError, ValueError) as exc:
        raise ConfigurationError("generic migration recovery proof differs") from exc


def _generic_migration_targets(context: Context) -> dict[PurePosixPath, PurePosixPath]:
    proof = _context_migration_proof(context)
    return {
        PurePosixPath(source): PurePosixPath(target)
        for source, target in proof.targets.items()
    }


def _work054_wp003_owner_merges(
    context: Context,
) -> dict[PurePosixPath, PurePosixPath]:
    """Use the recovery owner for MIG-0003 source proof, not another parser."""

    if (
        WORK054_MIGRATION_PATH not in context.paths
        or WORK054_MIGRATION_PATH not in context.tracked_regular_paths
    ):
        raise ConfigurationError("WORK-054 WP-003 migration ledger is unavailable")
    text = context.texts.get(WORK054_MIGRATION_PATH)
    if text is None:
        raise ConfigurationError("WORK-054 WP-003 migration ledger is unavailable")
    try:
        rows = validate_pinned_migration_recovery(
            context.root, WORK054_MIGRATION_PATH.as_posix(), text.encode("utf-8")
        )
    except (ArchiveContractError, OSError, ValueError) as exc:
        raise ConfigurationError("WORK-054 WP-003 recovery proof differs") from exc
    successors = _generic_migration_targets(context)
    result: dict[PurePosixPath, PurePosixPath] = {}
    for row in rows:
        legacy = PurePosixPath(str(row["legacy_path"]))
        replacement = PurePosixPath(str(row["replacement"]))
        terminal = successors.get(replacement, replacement)
        if (
            terminal not in context.tracked_regular_paths
            or not _path_exists_without_dereference(
                context.root, terminal, context.adapter_targets
            )
        ):
            raise ConfigurationError("WORK-054 WP-003 migration target differs")
        result[legacy] = terminal
    return result


@lru_cache(maxsize=1)
def _load_document_taxonomy_migration() -> Any:
    """Load the reviewed migration tool under one private canonical identity."""

    path = (
        Path(__file__).resolve(strict=True).with_name("migrate-document-work-units.py")
    )
    name = "_links_document_taxonomy_migration"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ConfigurationError("archive transition manifest validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
        if Path(str(getattr(module, "__file__", ""))).resolve(strict=True) != path:
            raise ConfigurationError(
                "archive transition manifest validator is unavailable"
            )
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


@lru_cache(maxsize=2)
def _reviewed_taxonomy_manifest(root: Path) -> Any:
    """Return only a clean stage-zero, fully validated reviewed manifest."""

    module = _load_document_taxonomy_migration()
    try:
        snapshot = module.load_reviewed_manifest_snapshot(
            root,
            validate_repository=False,
        )
    except module.MigrationAbort as exc:
        raise ConfigurationError(
            "archive transition manifest contract differs"
        ) from exc
    document = snapshot.document
    if document.source_commit != DOCUMENT_TAXONOMY_SOURCE_COMMIT:
        raise ConfigurationError("archive transition manifest source commit differs")
    return document


def _document_taxonomy_transition_manifest(
    context: Context,
) -> tuple[
    dict[PurePosixPath, str],
    dict[PurePosixPath, PurePosixPath],
    frozenset[PurePosixPath],
]:
    """Load the exact temporary 132-entry handoff without broad path waivers."""

    if DOCUMENT_TAXONOMY_MANIFEST_PATH not in context.tracked_regular_paths:
        raise ConfigurationError("archive transition manifest is not tracked")
    document = _reviewed_taxonomy_manifest(context.root)
    if (
        document.source_commit != DOCUMENT_TAXONOMY_SOURCE_COMMIT
        or len(document.entries) != 132
    ):
        raise ConfigurationError("archive transition manifest contract differs")
    four_digit_aliases = _work109_four_digit_aliases(context)

    expected_keys = [
        "source",
        "target",
        "workUnit",
        "disposition",
        "sourceBlob",
        "reviewed",
    ]
    manifest_source_values: list[str] = []
    for entry in document.entries:
        if not isinstance(entry, Mapping) or list(entry) != expected_keys:
            raise ConfigurationError("archive transition manifest entry differs")
        source_value = entry["source"]
        if not isinstance(source_value, str):
            raise ConfigurationError("archive transition manifest entry differs")
        source = PurePosixPath(source_value)
        if (
            source.as_posix() != source_value
            or source.is_absolute()
            or ".." in source.parts
        ):
            raise ConfigurationError("archive transition manifest path differs")
        manifest_source_values.append(source_value)
    try:
        manifest_source_evidence = _commit_path_evidence(
            str(context.root.absolute()),
            DOCUMENT_TAXONOMY_SOURCE_COMMIT,
            tuple(manifest_source_values),
        )
    except (RiaContractError, RiaGitError):
        raise ConfigurationError("archive transition manifest source differs") from None
    move_blobs: dict[PurePosixPath, str] = {}
    move_targets: dict[PurePosixPath, PurePosixPath] = {}
    archive_sources: set[PurePosixPath] = set()
    targets: set[PurePosixPath] = set()
    for entry, (source_blob, _) in zip(
        document.entries,
        manifest_source_evidence,
        strict=True,
    ):
        source_value = entry["source"]
        target_value = entry["target"]
        if (
            not isinstance(source_value, str)
            or not isinstance(target_value, str)
            or not isinstance(entry["workUnit"], str)
            or not entry["workUnit"]
            or entry["disposition"] not in {"move-current", "archive-unique"}
            or not isinstance(entry["sourceBlob"], str)
            or re.fullmatch(r"[0-9a-f]{40}", entry["sourceBlob"]) is None
            or entry["reviewed"] is not True
        ):
            raise ConfigurationError("archive transition manifest entry differs")
        source = PurePosixPath(source_value)
        target = PurePosixPath(target_value)
        if (
            source.as_posix() != source_value
            or target.as_posix() != target_value
            or source.is_absolute()
            or target.is_absolute()
            or ".." in source.parts
            or ".." in target.parts
            or len(source.parts) != 4
            or source.parts[:2] != ("docs", "04.execution")
            or source.parts[2] not in {"plans", "tasks"}
            or source.suffix != ".md"
            or source in move_blobs
            or source in archive_sources
            or target in targets
        ):
            raise ConfigurationError("archive transition manifest path differs")
        if source_blob != entry["sourceBlob"]:
            raise ConfigurationError("archive transition manifest source differs")
        if entry["disposition"] == "move-current":
            if (
                len(target.parts) != 4
                or target.parts[:2] != ("docs", "03.specs")
                or target.name not in {"plan.md", "tasks.md"}
            ):
                raise ConfigurationError("archive transition move target differs")
            stable_target = four_digit_aliases.get(target)
            if stable_target is None:
                raise ConfigurationError(
                    "archive transition move target lacks exact MIG-0002 evidence"
                )
            move_blobs[source] = entry["sourceBlob"]
            move_targets[source] = stable_target
            target = stable_target
        else:
            expected_target = PurePosixPath("docs", "98.archive", *source.parts[1:])
            if target != expected_target:
                raise ConfigurationError("archive transition archive target differs")
            archive_sources.add(source)
        targets.add(target)
    if len(move_blobs) != 82 or len(archive_sources) != 50:
        raise ConfigurationError("archive transition manifest counts differ")
    return move_blobs, move_targets, frozenset(archive_sources)


def _git_sha1_blob_bytes(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()  # noqa: S324


def _git_sha1_blob(text: str) -> str:
    return _git_sha1_blob_bytes(text.encode("utf-8"))


def _archive_transition_handoff(context: Context) -> ArchiveTransitionHandoff:
    """Project exact frozen-source edges only while the registry is transition."""

    if context.route_state != "transition":
        return ArchiveTransitionHandoff(ARCHIVE_INDEX_BOUNDARY, ())
    move_blobs, _, archive_sources = _document_taxonomy_transition_manifest(context)
    if (
        ARCHIVE_INDEX_PATH not in context.paths
        or ARCHIVE_INDEX_PATH not in context.tracked_regular_paths
        or not _path_exists_without_dereference(
            context.root, ARCHIVE_INDEX_PATH, context.adapter_targets
        )
    ):
        raise ConfigurationError("archive transition index boundary is unavailable")
    edges: set[ArchiveTransitionEdge] = set()
    for source, source_blob in move_blobs.items():
        text = context.texts.get(source)
        if (
            text is None
            or source not in context.paths
            or source not in context.tracked_regular_paths
            or _git_sha1_blob(text) != source_blob
        ):
            continue
        for raw in _extract_links(text):
            kind, target = _local_destination(source, raw)
            if kind == "local" and target in archive_sources:
                assert target is not None
                edges.add(ArchiveTransitionEdge(source, target))
    ordered_edges = tuple(sorted(edges))
    if ordered_edges != EXPECTED_ARCHIVE_TRANSITION_EDGES:
        raise ConfigurationError("archive transition deferred edge set differs")
    return ArchiveTransitionHandoff(ARCHIVE_INDEX_BOUNDARY, ordered_edges)


def _archive_transition_target(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> str | None:
    """Resolve one admitted transition edge to the collection index anchor."""

    handoff = _archive_transition_handoff(context)
    edge = ArchiveTransitionEdge(source, target)
    return handoff.navigation_boundary if edge in handoff.edges else None


def _reviewed_stage90_move_edges(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
) -> frozenset[ArchiveTransitionEdge]:
    """Admit only legacy move edges frozen by reviewed Stage 90 blobs."""

    if context.route_state != "transition":
        return frozenset()
    edges: set[ArchiveTransitionEdge] = set()
    contributing_sources: set[PurePosixPath] = set()
    for source, expected_blob in REVIEWED_STAGE90_MOVE_SOURCE_BLOBS.items():
        text = context.texts.get(source)
        if (
            text is None
            or source not in context.tracked_regular_paths
            or _git_sha1_blob(text) != expected_blob
        ):
            raise ConfigurationError(
                "reviewed Stage 90 move source differs from its frozen blob"
            )
        for raw in _extract_links(text):
            kind, target = _local_destination(source, raw)
            if kind != "local" or target not in move_targets:
                continue
            assert target is not None
            if _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            ):
                continue
            replacement = move_targets[target]
            if (
                replacement not in context.tracked_regular_paths
                or not _path_exists_without_dereference(
                    context.root, replacement, context.adapter_targets
                )
            ):
                raise ConfigurationError(
                    "reviewed Stage 90 move replacement is unavailable"
                )
            edges.add(ArchiveTransitionEdge(source, target))
            contributing_sources.add(source)
    if len(edges) != REVIEWED_STAGE90_MOVE_EDGE_COUNT or contributing_sources != set(
        REVIEWED_STAGE90_MOVE_SOURCE_BLOBS
    ):
        raise ConfigurationError("reviewed Stage 90 move edge set differs")
    return frozenset(edges)


def _immutable_historical_redirects(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
) -> dict[PurePosixPath, PurePosixPath]:
    """Compose exact current/archive replacements without a general alias."""

    aliases, replacements, merges = _work109_migration_projection(context)
    redirects = {
        **aliases,
        **replacements,
        **merges,
        **move_targets,
        **WORK105_LEDGER_PATH_ALIASES,
        **RETIRED_REFERENCE_ALIASES,
    }
    for legacy_archive, stable_archive in _work107_stable_archive_aliases(
        context
    ).items():
        redirects.setdefault(legacy_archive, stable_archive)
        if legacy_archive.parts[:2] == ("docs", "98.archive"):
            original = PurePosixPath("docs", *legacy_archive.parts[2:])
            redirects.setdefault(original, stable_archive)
    wp004b_targets = _work054_wp004b_targets(context)
    redirects = {
        source: wp004b_targets.get(target, target)
        for source, target in redirects.items()
    }
    redirects.update(wp004b_targets)
    return redirects


def _reviewed_immutable_historical_alias_edges(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
) -> dict[ArchiveTransitionEdge, PurePosixPath]:
    """Resolve only source-blob-pinned immutable Stage 90/98 links."""

    return _reviewed_source_pinned_alias_edges(
        context,
        move_targets,
        source_blobs=IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS,
        expected_source_count=None,
        expected_edge_count=None,
        contract_name="immutable historical alias",
    )


def _terminal_historical_source_boundary(
    context: Context,
    source: PurePosixPath,
) -> str | None:
    """Return the validated Git boundary for one frozen Stage 90 source path."""

    if (
        context.ria_contract_text is None
        or source not in context.paths
        or source not in context.tracked_regular_paths
    ):
        return None
    try:
        contract = json.loads(context.ria_contract_text)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ConfigurationError(
            "terminal historical source authority is malformed"
        ) from exc
    if not isinstance(contract, Mapping):
        raise ConfigurationError("terminal historical source authority is malformed")

    candidates: list[
        tuple[PurePosixPath, str, frozenset[str] | None, frozenset[str] | None]
    ] = []
    snapshot = contract.get("snapshotGuard")
    if not isinstance(snapshot, Mapping):
        raise ConfigurationError("terminal historical source authority is malformed")
    snapshot_commit = snapshot.get("sourceCommit")
    snapshot_ids = snapshot.get("historicalPackIds")
    if (
        not isinstance(snapshot_commit, str)
        or GIT_SHA1_PATTERN.fullmatch(snapshot_commit) is None
        or not isinstance(snapshot_ids, list)
        or not snapshot_ids
        or any(not isinstance(pack_id, str) for pack_id in snapshot_ids)
        or len(snapshot_ids) != len(set(snapshot_ids))
    ):
        raise ConfigurationError("terminal historical source authority is malformed")
    for pack_id in snapshot_ids:
        candidates.append(
            (
                PurePosixPath("docs/90.references") / pack_id,
                snapshot_commit.removeprefix("git-sha1:"),
                None,
                None,
            )
        )

    retired = contract.get("retiredCurrentPackBaselines")
    if not isinstance(retired, list):
        raise ConfigurationError("terminal historical source authority is malformed")
    for entry in retired:
        if not isinstance(entry, Mapping):
            raise ConfigurationError(
                "terminal historical source authority is malformed"
            )
        pack_id = entry.get("id")
        encoded_commit = entry.get("sourceCommit")
        members = entry.get("members")
        allowed_states = entry.get("allowedStates")
        if (
            not isinstance(pack_id, str)
            or not isinstance(encoded_commit, str)
            or GIT_SHA1_PATTERN.fullmatch(encoded_commit) is None
            or not isinstance(members, list)
            or not members
            or any(
                not isinstance(member, str)
                or PurePosixPath(member).name != member
                or PurePosixPath(member).suffix != ".md"
                for member in members
            )
            or len(members) != len(set(members))
            or not isinstance(allowed_states, list)
            or not allowed_states
            or any(not isinstance(state, str) for state in allowed_states)
            or len(allowed_states) != len(set(allowed_states))
        ):
            raise ConfigurationError(
                "terminal historical source authority is malformed"
            )
        candidates.append(
            (
                PurePosixPath("docs/90.references") / pack_id,
                retired_baseline_protected_commit(contract, entry),
                frozenset(members),
                frozenset(allowed_states),
            )
        )

    matches: list[str] = []
    for pack_root, boundary, exact_members, allowed_states in candidates:
        if source == pack_root / "README.md":
            profile = context.profiles.get(source)
            if profile is not None and profile.profile_id == "readme/snapshot-pack":
                matches.append(boundary)
            continue
        if source.parent != pack_root or source.suffix != ".md":
            continue
        profile = context.profiles.get(source)
        status = context.metadata.get(source, {}).get("status")
        if profile is None or profile.profile_id != "content/reference":
            continue
        if exact_members is not None and source.name not in exact_members:
            continue
        if allowed_states is not None and status not in allowed_states:
            continue
        if allowed_states is None and status not in {
            "draft",
            "active",
            "accepted",
            "done",
            "archived",
        }:
            continue
        matches.append(boundary)
    if len(matches) > 1:
        raise ConfigurationError("terminal historical source authority is ambiguous")
    return matches[0] if matches else None


def _terminal_frozen_manifest_source(
    context: Context,
    source: PurePosixPath,
) -> bool:
    """Admit one byte-frozen cloud snapshot source from the reviewed manifest."""

    expected_blob = IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS.get(source)
    cloud_root = PurePosixPath("docs/90.references/cloud-examples")
    if (
        expected_blob is None
        or not source.is_relative_to(cloud_root)
        or source not in context.paths
        or source not in context.tracked_regular_paths
    ):
        return False
    profile = context.profiles.get(source)
    if profile is None or profile.profile_id not in {
        "content/reference",
        "readme/collection-index",
        "readme/snapshot-pack",
    }:
        return False
    text = context.texts.get(source)
    return text is not None and _git_sha1_blob(text) == expected_blob


def _reviewed_source_pinned_alias_edges(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
    *,
    source_blobs: Mapping[PurePosixPath, str],
    expected_source_count: int | None,
    expected_edge_count: int | None,
    contract_name: str,
    exact_redirects: Mapping[PurePosixPath, PurePosixPath] | None = None,
    expected_occurrence_count: int | None = None,
) -> dict[ArchiveTransitionEdge, PurePosixPath]:
    """Resolve source-pinned historical aliases with optional finite totals."""

    if context.route_state != "transition":
        return {}
    redirects = (
        dict(exact_redirects)
        if exact_redirects is not None
        else _immutable_historical_redirects(context, move_targets)
    )
    edges: dict[ArchiveTransitionEdge, PurePosixPath] = {}
    contributing_sources: set[PurePosixPath] = set()
    occurrence_count = 0
    for source, expected_blob in source_blobs.items():
        text = context.texts.get(source)
        source_matches = text is not None and _git_sha1_blob(text) == expected_blob
        if (
            text is None
            or source not in context.tracked_regular_paths
            or not source_matches
        ):
            raise ConfigurationError(
                f"{contract_name} source differs from its frozen blob"
            )
        for raw in _extract_links(text):
            kind, target = _local_destination(source, raw)
            if kind != "local" or target is None:
                continue
            replacement = redirects.get(target)
            if replacement is None or _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            ):
                continue
            if (
                replacement not in context.tracked_regular_paths
                or not _path_exists_without_dereference(
                    context.root, replacement, context.adapter_targets
                )
            ):
                raise ConfigurationError(f"{contract_name} replacement is unavailable")
            edges[ArchiveTransitionEdge(source, target)] = replacement
            contributing_sources.add(source)
            occurrence_count += 1
    if (
        (
            expected_source_count is not None
            and len(source_blobs) != expected_source_count
        )
        or contributing_sources != set(source_blobs)
        or (expected_edge_count is not None and len(edges) != expected_edge_count)
        or (
            expected_occurrence_count is not None
            and occurrence_count != expected_occurrence_count
        )
    ):
        raise ConfigurationError(
            f"{contract_name} edge set differs "
            f"(sources {len(source_blobs)}/{expected_source_count} "
            f"edges {len(edges)}/{expected_edge_count} "
            f"occurrences {occurrence_count}/{expected_occurrence_count})"
        )
    return edges


@dataclass(frozen=True)
class ArchivePayloadProof:
    """One Archive-owned payload removed from instruction scanning only."""

    input_bytes: bytes = dataclass_field(repr=False)
    remaining_text: str = dataclass_field(repr=False)


@dataclass(frozen=True)
class HistoricalMigrationProof:
    """Exact historical bytes and terminal dispositions; never a status waiver."""

    terminal_targets: Mapping[str, str]
    consumers: Mapping[str, bytes] = dataclass_field(repr=False)
    rendered_dispositions: Mapping[tuple[str, str], str]
    literal_dispositions: Mapping[tuple[str, str], str] = dataclass_field(
        default_factory=dict
    )
    document_registry: Registry | None = None
    declarations: Mapping[str, MigrationDeclaration] = dataclass_field(
        default_factory=dict
    )
    archive_payloads: Mapping[str, ArchivePayloadProof] = dataclass_field(
        default_factory=dict
    )


def repository_historical_migration_proof(
    root: Path,
    *,
    registry: Registry | None = None,
    raw_schema: object = _UNSET,
    read_current_bytes: Callable[[str, int], bytes] | None = None,
    read_symlink: Callable[[str], str] | None = None,
) -> HistoricalMigrationProof:
    """Expose the existing link owner's verified historical interpretations."""

    if (
        registry is None
        and raw_schema is _UNSET
        and read_current_bytes is None
        and read_symlink is None
    ):
        context = _build_context(root)
    else:
        context = _build_context(
            root,
            registry=registry,
            raw_schema=raw_schema,
            read_current_bytes=read_current_bytes,
            read_symlink=read_symlink,
        )
    _, move_targets, _ = _document_taxonomy_transition_manifest(context)
    return _historical_migration_proof(context, move_targets)


def _historical_migration_proof(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
) -> HistoricalMigrationProof:
    proof = _context_migration_proof(context)
    generic_targets = {
        PurePosixPath(source): PurePosixPath(target)
        for source, target in proof.targets.items()
    }
    aliases, replacements, work109_merges = _work109_migration_projection(context)
    archive_aliases = _work107_stable_archive_aliases(context)
    if PurePosixPath(WORK107_MIGRATION_PATH) in context.paths and not archive_aliases:
        raise ConfigurationError("historical archive migration proof differs")
    migration_projections = (
        move_targets,
        aliases,
        replacements,
        work109_merges,
        archive_aliases,
        _work054_wp003_owner_merges(context),
        _work054_wp004b_targets(context),
        generic_targets,
    )
    try:
        composed = compose_migration_targets(
            tuple(
                {
                    source.as_posix(): target.as_posix()
                    for source, target in projection.items()
                }
                for projection in migration_projections
            )
        )
    except ArchiveContractError as exc:
        raise ConfigurationError("historical migration composition differs") from exc
    redirects = dict(composed)
    # These older unique cutovers are not Migration rows. Their current
    # successors still require a tracked regular artifact, not a status label.
    for source, target in RETIRED_REFERENCE_ALIASES.items():
        terminal = redirects.get(target.as_posix(), target.as_posix())
        if PurePosixPath(terminal) in context.tracked_regular_paths:
            redirects[source.as_posix()] = terminal

    declarations = dict(proof.declarations)
    # Each old ledger's complete owner proof ran above. This view removes only
    # typed path fields; no old or new ledger receives a whole-document waiver.
    for record in (
        PurePosixPath(WORK107_MIGRATION_PATH),
        WORK109_MIGRATION_PATH,
        WORK054_MIGRATION_PATH,
        WORK054_WP004B_MIGRATION_PATH,
    ):
        if record in context.paths:
            declarations[record.as_posix()] = project_migration_declaration_fields(
                context.texts[record].encode("utf-8"), redirects
            )

    consumers: dict[str, bytes] = {}
    for source in context.paths:
        raw = context.texts.get(source, "").encode("utf-8")
        boundary = _terminal_historical_source_boundary(context, source)
        if boundary is not None:
            try:
                historical = _read_ria_commit_path(
                    context.root, boundary, Path(source.as_posix())
                )
            except (RiaContractError, RiaGitError) as exc:
                raise ConfigurationError(
                    "historical reference source proof is unavailable"
                ) from exc
            if historical != raw:
                raise ConfigurationError("historical reference source bytes differ")
            consumers[source.as_posix()] = historical
        elif _terminal_frozen_manifest_source(context, source):
            consumers[source.as_posix()] = raw
    for name, raw in proof.consumers.items():
        source = PurePosixPath(name)
        # A consumer a sealed row retires is absent from the current tree by
        # design.  Its reviewed disposition is still composed below from the
        # historical bytes the proof carries, which is where the evidence lives.
        if name in proof.retired_consumers:
            consumers[name] = raw
            continue
        if (
            source not in context.tracked_regular_paths
            or source not in context.paths
            or context.texts.get(source, "").encode("utf-8") != raw
        ):
            raise ConfigurationError("historical migration consumer source differs")
        consumers[name] = raw

    edges: dict[tuple[str, str], str] = {}
    literals: dict[tuple[str, str], str] = {}
    for name, raw in consumers.items():
        source = PurePosixPath(name)
        for link in rendered_local_links(raw.decode("utf-8", "strict"), source):
            if link.kind != "local" or link.target is None:
                continue
            target = link.target.as_posix()
            terminal = redirects.get(target)
            if terminal is None or _path_exists_without_dereference(
                context.root, link.target, context.adapter_targets
            ):
                continue
            if (
                PurePosixPath(terminal) not in context.tracked_regular_paths
                or not _path_exists_without_dereference(
                    context.root, PurePosixPath(terminal), context.adapter_targets
                )
            ):
                raise ConfigurationError("historical replacement is unavailable")
            edges[(name, target)] = terminal
        for (owner, target), disposition in getattr(proof, "references", {}).items():
            if owner != name:
                continue
            if disposition.kind == "literal-path":
                literals[owner, target] = disposition.terminal_path
            elif disposition.kind == "symlink-view" and target in {
                link.target.as_posix()
                for link in rendered_local_links(raw.decode("utf-8", "strict"), source)
                if link.kind == "local" and link.target is not None
            }:
                existing = edges.get((owner, target))
                if existing is not None and existing != disposition.terminal_path:
                    raise ConfigurationError(
                        "historical view disposition conflicts with existing owner"
                    )
                edges[owner, target] = disposition.terminal_path
        if (
            name in proof.consumers
            and not any(owner == name for owner, _ in edges)
            and not any(owner == name for owner, _ in literals)
        ):
            raise ConfigurationError(
                "historical migration consumer has no reviewed disposition"
            )
    archive_payloads = _archive_payload_proofs(context)
    return HistoricalMigrationProof(
        MappingProxyType(redirects),
        MappingProxyType(consumers),
        MappingProxyType(edges),
        MappingProxyType(literals),
        proof.proposed_registry,
        MappingProxyType(declarations),
        archive_payloads,
    )


def _archive_payload_proofs(
    context: Context,
) -> Mapping[str, ArchivePayloadProof]:
    """Prove stable Archive payloads without reopening the held candidates."""

    rows = _work107_stable_archive_rows(context)
    stable_paths = frozenset(str(row["stable_path"]) for row in rows)
    records_by_path = {
        path.as_posix(): ArchiveRecord(path.as_posix(), text.encode("utf-8"))
        for path in context.paths
        if path in context.tracked_regular_paths
        and path in context.profiles
        and context.profiles[path].profile_id == "content/archive"
        and (text := context.texts.get(path)) is not None
    }
    report = validate_archive_records(
        context.root,
        tuple(records_by_path.values()),
        stable_archive_paths=stable_paths,
    )
    if not report.valid:
        raise ConfigurationError("historical archive owner validation failed")

    proofs: dict[str, ArchivePayloadProof] = {}
    rows_by_stable_path = {str(row["stable_path"]): row for row in rows}
    for archive_path, record in sorted(records_by_path.items()):
        try:
            parsed = parse_archive_envelope(record.content)
        except ArchiveContractError as exc:
            raise ConfigurationError("historical archive input differs") from exc
        if archive_path in stable_paths:
            try:
                historical = recover_work107_legacy_envelope(
                    context.root, rows_by_stable_path[archive_path]
                )
            except ArchiveContractError as exc:
                raise ConfigurationError(
                    "historical archive provenance differs"
                ) from exc
            if (
                parsed.metadata.get("original_path")
                != historical.metadata.get("original_path")
                or parsed.metadata.get("source_commit")
                != historical.metadata.get("source_commit")
                or parsed.metadata.get("source_blob")
                != historical.metadata.get("source_blob")
                or parsed.metadata.get("content_sha256")
                != historical.metadata.get("content_sha256")
                or parsed.payload != historical.payload
            ):
                raise ConfigurationError("historical archive provenance differs")
        remaining = record.content[: len(record.content) - len(parsed.payload)]
        try:
            remaining_text = remaining.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ConfigurationError("historical archive input differs") from exc
        proofs[archive_path] = ArchivePayloadProof(record.content, remaining_text)
    return MappingProxyType(proofs)


def _reviewed_work054_historical_owner_edges(
    context: Context,
    move_targets: Mapping[PurePosixPath, PurePosixPath],
) -> dict[ArchiveTransitionEdge, PurePosixPath]:
    proof = _historical_migration_proof(context, move_targets)
    return {
        ArchiveTransitionEdge(
            PurePosixPath(source), PurePosixPath(target)
        ): PurePosixPath(terminal)
        for (source, target), terminal in proof.rendered_dispositions.items()
    }


def _link_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    archive_handoff = _archive_transition_handoff(context)
    deferred_archive_edges = frozenset(archive_handoff.edges)
    _, move_targets, _ = _document_taxonomy_transition_manifest(context)
    reviewed_stage90_move_edges = _reviewed_stage90_move_edges(context, move_targets)
    reviewed_historical_alias_edges = _reviewed_immutable_historical_alias_edges(
        context,
        move_targets,
    )
    reviewed_work054_owner_edges = _reviewed_work054_historical_owner_edges(
        context,
        move_targets,
    )
    for source in context.paths:
        profile = context.profiles[source].profile_id
        if profile == "content/archive":
            # ArchiveEnvelope.v1 payload links are historical evidence. Their
            # authority is resolved against source_commit/original_path by the
            # archive validator, never against the current worktree.
            continue
        for raw in _extract_links(context.texts[source]):
            kind, target = _local_destination(source, raw)
            if kind in {"external", "anchor"}:
                continue
            if kind.startswith("LINK-"):
                diagnostics.append(
                    _diag(
                        kind,
                        source,
                        profile,
                        "repository-relative local link",
                        kind.removeprefix("LINK-").casefold(),
                    )
                )
                continue
            assert target is not None
            if not _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            ):
                if (
                    ArchiveTransitionEdge(source, target)
                    in reviewed_historical_alias_edges
                ):
                    continue
                if (
                    ArchiveTransitionEdge(source, target)
                    in reviewed_work054_owner_edges
                ):
                    continue
                if ArchiveTransitionEdge(source, target) in reviewed_stage90_move_edges:
                    continue
                if ArchiveTransitionEdge(source, target) in deferred_archive_edges:
                    continue
                if _work105_immutable_history_ard_link(context, source, target):
                    continue
                if _work105_accepted_history_ard_link(context, source, target):
                    continue
                if _work105_completed_history_ard_link(context, source, target):
                    continue
                if _protected_historical_predecessor_link(context, source, target):
                    continue
                if _migrated_directory_link(context, source, target):
                    continue
                diagnostics.append(
                    _diag(
                        "LINK-BROKEN",
                        source,
                        profile,
                        "existing repository target",
                        target.as_posix(),
                    )
                )
                continue
            if (
                _is_current_authority(context, source)
                and target.as_posix().startswith("docs/98.archive/")
                and target != PurePosixPath("docs/98.archive/README.md")
            ):
                diagnostics.append(
                    _diag(
                        "LINK-ARCHIVE-BYPASS",
                        source,
                        profile,
                        "archive index boundary",
                        "direct archive target",
                    )
                )
    return diagnostics


def _fenced_blocks(text: str) -> tuple[str, ...]:
    blocks: list[str] = []
    fence: tuple[str, int] | None = None
    lines: list[str] = []
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
                lines = []
            elif (
                token[0] == fence[0]
                and len(token) >= fence[1]
                and not marker.group(2).strip()
            ):
                blocks.append("\n".join(lines))
                fence = None
                lines = []
            continue
        if fence is not None:
            lines.append(line)
    return tuple(blocks)


def _markdown_without_html_comments(text: str) -> str:
    """Remove HTML comments outside fences while preserving line positions."""
    output: list[str] = []
    fence: tuple[str, int] | None = None
    in_comment = False
    for raw_line in text.splitlines():
        if fence is not None:
            output.append(raw_line)
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", raw_line)
            if marker:
                token = marker.group(1)
                if (
                    token[0] == fence[0]
                    and len(token) >= fence[1]
                    and not marker.group(2).strip()
                ):
                    fence = None
            continue

        visible: list[str] = []
        cursor = 0
        while cursor < len(raw_line):
            if in_comment:
                end = raw_line.find("-->", cursor)
                if end < 0:
                    cursor = len(raw_line)
                    continue
                cursor = end + 3
                in_comment = False
                continue
            start = raw_line.find("<!--", cursor)
            if start < 0:
                visible.append(raw_line[cursor:])
                break
            visible.append(raw_line[cursor:start])
            cursor = start + 4
            in_comment = True

        line = "".join(visible)
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            fence = (token[0], len(token))
        output.append(line)
    return "\n".join(output)


def _gfm_table_cells(line: str) -> list[str]:
    """Split one GFM table row without treating escaped pipes as delimiters."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []

    def escaped(index: int) -> bool:
        backslashes = 0
        cursor = index - 1
        while cursor >= 0 and stripped[cursor] == "\\":
            backslashes += 1
            cursor -= 1
        return backslashes % 2 == 1

    cells: list[str] = []
    current: list[str] = []
    for index, character in enumerate(stripped):
        if character == "|" and not escaped(index):
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    cells.append("".join(current).strip())
    if cells and cells[0] == "":
        cells.pop(0)
    if stripped.endswith("|") and not escaped(len(stripped) - 1) and cells[-1] == "":
        cells.pop()
    return cells


def _exact_heading_section(text: str, heading: str) -> str | None:
    visible_lines = _visible_markdown(text).splitlines()
    raw_lines = text.splitlines()
    matches = [index for index, line in enumerate(visible_lines) if line == heading]
    if len(matches) != 1:
        return None
    start = matches[0]
    level = len(heading) - len(heading.lstrip("#"))
    end = len(raw_lines)
    for index in range(start + 1, len(visible_lines)):
        candidate = re.match(r"^(#{1,6})\s", visible_lines[index])
        if candidate and len(candidate.group(1)) <= level:
            end = index
            break
    return "\n".join(raw_lines[start + 1 : end])


def _exact_rendered_heading_section(text: str, heading: str) -> str | None:
    """Slice one root heading from the same rendered block view as links."""

    lines = _rendered_container_lines(text)
    matches = [
        index
        for index, line in enumerate(lines)
        if line.depth == 0 and line.text == heading
    ]
    if len(matches) != 1:
        return None
    start = matches[0]
    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        candidate = re.match(r"^(#{1,6})\s", line.text)
        if line.depth == 0 and candidate and len(candidate.group(1)) <= level:
            end = index
            break
    return _join_rendered_container_lines(lines[start + 1 : end])


def _after_exact_heading(text: str, heading: str) -> str | None:
    visible_lines = _visible_markdown(text).splitlines()
    raw_lines = text.splitlines()
    matches = [index for index, line in enumerate(visible_lines) if line == heading]
    if len(matches) != 1:
        return None
    return "\n".join(raw_lines[matches[0] + 1 :])


def _tree_targets(declaration: DeclaredIndex, text: str) -> list[PurePosixPath]:
    section = _exact_heading_section(text, declaration.tree_anchor)
    if section is None:
        return []
    expected_root = declaration.tree_root
    block = next(
        (
            item
            for item in _fenced_blocks(section)
            if item.splitlines() and item.splitlines()[0] == expected_root
        ),
        "",
    )
    base = declaration.path.parent
    targets: list[PurePosixPath] = []
    if declaration.tree_kind == "spec":
        pending: str | None = None
        for line in block.splitlines():
            folder = re.match(r"^[│ ]*[├└]── ([0-9]{4}-[^/]+)/$", line)
            if folder:
                pending = folder.group(1)
                continue
            if pending and re.match(r"^[│ ]*[├└]── spec\.md$", line):
                targets.append(base / pending / "spec.md")
                pending = None
    else:
        for name in re.findall(r"^[├└]── ([^/\n]+\.md)$", block, re.MULTILINE):
            if name != "README.md":
                targets.append(base / name)
    return targets


def _table_rows(
    declaration: DeclaredIndex, text: str
) -> list[tuple[PurePosixPath, str]]:
    section = (
        _after_exact_heading(text, declaration.table_anchor)
        if declaration.table_mode == "after"
        else _exact_heading_section(text, declaration.table_anchor)
    )
    if section is None:
        return []
    lines = _visible_markdown(section).splitlines()
    table_started = False
    rows: list[tuple[PurePosixPath, str]] = []
    for line in lines:
        if not table_started:
            if line.startswith("|") and "---" not in line:
                table_started = True
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        links = re.findall(r"\]\((\./[^)]+\.md)\)", cells[0])
        if len(links) != 1:
            continue
        kind, target = _local_destination(declaration.path, links[0])
        if kind != "local" or target is None:
            continue
        status = cells[2].strip("` ") if len(cells) > 2 else ""
        rows.append((target, status))
    return rows


def _index_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    path_set = set(context.paths)
    for declaration in DECLARED_INDEXES:
        profile = context.profiles[declaration.path].profile_id
        actual = sorted(
            (
                p
                for p in context.paths
                if declaration.target_pattern.fullmatch(p.as_posix())
                and p != declaration.path
            ),
            key=lambda p: p.as_posix(),
        )
        actual_set = set(actual)
        tree = _tree_targets(declaration, context.texts[declaration.path])
        rows = _table_rows(declaration, context.texts[declaration.path])
        row_counter = collections.Counter(path for path, _ in rows)
        tree_counter = collections.Counter(tree)
        for target, count in sorted(
            row_counter.items(), key=lambda item: item[0].as_posix()
        ):
            target_key = target.as_posix()
            if count > 1:
                diagnostics.append(
                    _diag(
                        "INDEX-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; {count} rows",
                    )
                )
            if target not in actual_set:
                diagnostics.append(
                    _diag(
                        "INDEX-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; declared target",
                        f"target={target_key}; non-target row",
                    )
                )
        for target in actual:
            target_key = target.as_posix()
            if row_counter[target] == 0:
                diagnostics.append(
                    _diag(
                        "INDEX-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; row is missing",
                    )
                )
            for row_target, row_status in rows:
                if row_target != target:
                    continue
                expected_status = str(
                    context.metadata[target].get("status", "")
                ).casefold()
                actual_status = STATUS_MAP.get(row_status.casefold(), "")
                if actual_status != expected_status:
                    diagnostics.append(
                        _diag(
                            "INDEX-STATUS",
                            declaration.path,
                            profile,
                            f"target={target_key}; status={expected_status}",
                            f"target={target_key}; status={actual_status or 'unknown'}",
                        )
                    )
                break
        for target in sorted(actual_set | set(tree), key=lambda p: p.as_posix()):
            if tree_counter[target] != (1 if target in actual_set else 0):
                target_key = target.as_posix()
                diagnostics.append(
                    _diag(
                        "INDEX-TREE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one declared tree target",
                        f"target={target_key}; {tree_counter[target]} entries",
                    )
                )
        # A resolved row that is not even in the inventory is stale regardless of disk state.
        if any(
            target not in path_set and target not in actual_set for target, _ in rows
        ):
            pass
    return diagnostics


_COLLECTION_TREE_LINE = re.compile(
    r"^(?P<indent>(?:│   |    )*)(?:├── |└── )"
    r"(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<directory>/)?"
    r"(?:\s+#\s+.*)?$"
)


def _collection_tree_targets(
    declaration: CollectionIndex, text: str
) -> tuple[list[PurePosixPath], bool]:
    section = _exact_heading_section(text, declaration.tree_anchor)
    if section is None:
        return [], False
    comment_visible_section = _markdown_without_html_comments(section)
    blocks = [
        block
        for block in _fenced_blocks(comment_visible_section)
        if block.splitlines() and block.splitlines()[0] == declaration.tree_root
    ]
    if len(blocks) != 1:
        return [], False
    stack: list[str] = []
    targets: list[PurePosixPath] = []
    valid = True
    for line in blocks[0].splitlines()[1:]:
        if not line.strip():
            continue
        match = _COLLECTION_TREE_LINE.fullmatch(line)
        if match is None:
            valid = False
            continue
        indent = match.group("indent")
        depth = len(indent) // 4
        name = match.group("name")
        if name in {".", ".."}:
            valid = False
            continue
        if match.group("directory"):
            if depth > len(stack):
                valid = False
                continue
            stack[depth:] = [name]
            continue
        if depth > len(stack):
            valid = False
            continue
        relative = (*stack[:depth], name)
        target = declaration.root.joinpath(*relative)
        if declaration.target_pattern.fullmatch(target.as_posix()) is None:
            valid = False
            continue
        targets.append(target)
    return targets, valid


def _first_visible_table(
    text: str,
) -> tuple[list[str], list[list[str]]] | None:
    lines = _visible_markdown(text).splitlines()
    for index in range(len(lines) - 1):
        header_line = lines[index]
        delimiter_line = lines[index + 1]
        if (
            re.match(r"^ {0,3}\|", header_line) is None
            or re.match(r"^ {0,3}\|", delimiter_line) is None
        ):
            continue
        header = _gfm_table_cells(header_line)
        delimiter = _gfm_table_cells(delimiter_line)
        if len(header) != len(delimiter) or not header:
            continue
        if not all(re.fullmatch(r":?-+:?", cell) for cell in delimiter):
            continue
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip():
                break
            if re.match(r"^ {0,3}\|", row_line) is None:
                break
            cells = _gfm_table_cells(row_line)
            rows.append((cells + [""] * len(header))[: len(header)])
        return header, rows
    return None


BODY_LINK_EXCLUSION = re.compile(r"^N/A — \S(?:.*\S)?$")
BODY_IDENTIFIER_PATTERNS = {
    "requirement": re.compile(r"^REQ-[A-Z0-9-]+-[0-9]{2,3}$"),
    "criterion": re.compile(r"^VAL-[A-Z0-9-]+-[0-9]{3}$"),
    "work-item": re.compile(r"^[A-Z][A-Z0-9-]+-[0-9]{3}$"),
}


def _body_identifier_text(cell: str) -> str:
    """Normalize the same plain, code, or full-link identifier forms."""

    value = cell.strip()
    link = re.fullmatch(r"\[([^\]\n]+)\]\([^\n)]+\)", value)
    if link:
        value = link.group(1).strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def _body_contract_link_is_enforced(
    path: PurePosixPath,
    profile: DocumentProfile,
    status: str,
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...],
) -> bool:
    if body_contracts not in {"registry", "audit"}:
        raise ConfigurationError("body_contracts must be registry or audit")
    if profile.body_contract is None or profile.mode != "authored":
        return False
    if body_contracts == "audit":
        in_scope = not path_prefixes or any(
            path == prefix or prefix in path.parents for prefix in path_prefixes
        )
        return in_scope and status in {"draft", "active"}
    return status in profile.body_contract.enforced_statuses


def _body_contract_rows(
    text: str, profile: DocumentProfile
) -> list[dict[str, str]] | None:
    """Return a shape-valid lifecycle table; local validation owns shape errors."""

    contract = profile.body_contract
    if contract is None:
        return None
    section = _exact_heading_section(text, f"## {contract.section}")
    table_section = (
        None
        if section is None
        else _exact_heading_section(section, f"### {contract.table_heading}")
    )
    if table_section is None:
        return None
    table = _first_visible_table(table_section)
    if table is None or tuple(table[0]) != contract.required_columns:
        return None
    header, rows = table
    if not rows:
        return None
    return [dict(zip(header, row, strict=True)) for row in rows]


def lifecycle_markdown_evidence(
    path: PurePosixPath,
    text: str,
    profile: DocumentProfile,
    snapshot_profiles: Mapping[PurePosixPath, str],
) -> LifecycleMarkdownEvidence:
    """Return lifecycle evidence without reading the filesystem.

    The caller owns Git provenance and passes one immutable proposed-snapshot
    text plus the complete selected-profile projection. This adapter only
    reuses the canonical CommonMark renderer, link extractor, heading slicer,
    and body-table parser already owned by this validator.
    """

    def local_links(raw_links: Iterable[str]) -> tuple[PurePosixPath, ...]:
        resolved: list[PurePosixPath] = []
        for raw_link in raw_links:
            kind, target = _local_destination(path, raw_link)
            if kind in {"local", "anchor"} and target is not None:
                resolved.append(target)
        return tuple(resolved)

    def selected_local_links(raw_links: Iterable[str]) -> tuple[PurePosixPath, ...]:
        return tuple(
            target for target in local_links(raw_links) if target in snapshot_profiles
        )

    all_links = local_links(_extract_links(text))
    rendered_lines = _rendered_container_lines(text)
    root_h2 = tuple(
        line.text[3:].strip()
        for line in rendered_lines
        if line.depth == 0
        and line.text.startswith("## ")
        and not line.text.startswith("### ")
    )
    required_headings_valid = all(
        _exact_rendered_heading_section(text, f"## {heading}") is not None
        for heading in profile.headings.required
    )
    allowed_headings_valid = all(
        heading in profile.headings.allowed for heading in root_h2
    )
    relationship_links: tuple[PurePosixPath, ...] = ()
    unresolved_relationship_links: tuple[PurePosixPath, ...] = ()
    relationship_section_valid = False
    body_rows: tuple[tuple[tuple[str, str], ...], ...] = ()
    body_table_links: tuple[PurePosixPath, ...] = ()
    body_contract_valid = False

    if profile.body_contract is not None:
        contract = profile.body_contract
        rows = _body_contract_rows(text, profile)
        relationship_section = _exact_rendered_heading_section(
            text, f"## {contract.section}"
        )
        relationship_section_valid = relationship_section is not None
        body_contract_valid = (
            required_headings_valid and allowed_headings_valid and rows is not None
        )
        collected: list[PurePosixPath] = []
        unresolved: list[PurePosixPath] = []
        if rows is not None:
            body_rows = tuple(tuple(row.items()) for row in rows)
            projection_columns = (
                ("Evidence",)
                if profile.profile_id == "sdlc/task"
                and "Evidence" in contract.required_columns
                else tuple(
                    column
                    for column in (
                        contract.source_link_column,
                        contract.target_link_column,
                    )
                    if column is not None
                )
            )
            projected_raw_links = tuple(
                raw_link
                for row in rows
                for column in projection_columns
                for raw_link in _extract_links(row[column], definitions_text=text)
            )
            projected_links = local_links(projected_raw_links)
            body_table_links = tuple(
                target for target in projected_links if target in snapshot_profiles
            )
            if profile.profile_id == "sdlc/task":
                unresolved.extend(
                    target
                    for target in projected_links
                    if target not in snapshot_profiles
                )
            for row in rows:
                if any(not value.strip() for value in row.values()):
                    body_contract_valid = False
                for identifier in contract.identifier_columns:
                    value = _body_identifier_text(row[identifier.column])
                    if value.startswith("N/A"):
                        if (
                            not contract.allow_explicit_exclusion
                            or BODY_LINK_EXCLUSION.fullmatch(value) is None
                        ):
                            body_contract_valid = False
                    elif (
                        BODY_IDENTIFIER_PATTERNS[identifier.kind].fullmatch(value)
                        is None
                    ):
                        body_contract_valid = False
            link_columns = (
                (contract.source_link_column, contract.allowed_source_profile_ids),
                (contract.target_link_column, contract.allowed_target_profile_ids),
            )
            for row in rows:
                for column, allowed_profiles in link_columns:
                    if column is None:
                        continue
                    cell = row[column].strip()
                    if cell.startswith("N/A"):
                        if (
                            not contract.allow_explicit_exclusion
                            or BODY_LINK_EXCLUSION.fullmatch(cell) is None
                        ):
                            body_contract_valid = False
                        continue
                    raw_links = _extract_links(cell, definitions_text=text)
                    resolved = local_links(raw_links)
                    if not raw_links or len(resolved) != len(raw_links):
                        body_contract_valid = False
                        continue
                    for target in resolved:
                        if target not in snapshot_profiles:
                            unresolved.append(target)
                            body_contract_valid = False
                        elif snapshot_profiles.get(target) not in allowed_profiles:
                            body_contract_valid = False
                        else:
                            collected.append(target)
        relationship_links = tuple(collected)
        unresolved_relationship_links = tuple(unresolved)
    else:
        relationship_section_valid = required_headings_valid and allowed_headings_valid
        body_contract_valid = relationship_section_valid

    task_terminal_valid = True
    if profile.profile_id == "sdlc/task":
        task_section = _exact_heading_section(text, "## Task Table")
        task_table = _first_visible_table(task_section or "")
        task_terminal_valid = False
        if task_table is not None:
            header, rows = task_table
            required = {"Status", "Result", "Evidence"}
            if required.issubset(header) and rows:
                positions = {value: header.index(value) for value in required}
                placeholder = re.compile(
                    r"(?i)^(?:|pending|not executed|not recorded|named repository "
                    r"evidence|tbd|todo|n/?a|[-—])$"
                )
                task_terminal_valid = all(
                    row[positions["Status"]].strip().casefold() in {"done", "archived"}
                    and placeholder.fullmatch(row[positions["Result"]].strip()) is None
                    and placeholder.fullmatch(row[positions["Evidence"]].strip())
                    is None
                    for row in rows
                )

    return LifecycleMarkdownEvidence(
        path=path,
        all_local_links=all_links,
        relationship_links=relationship_links,
        unresolved_relationship_links=unresolved_relationship_links,
        body_table_links=body_table_links,
        relationship_section_valid=relationship_section_valid,
        body_contract_valid=body_contract_valid,
        body_rows=body_rows,
        task_terminal_evidence_valid=task_terminal_valid,
    )


def _links_back_to(
    context: Context, owner: PurePosixPath, expected: PurePosixPath
) -> bool:
    for raw_link in _extract_links(context.texts[owner]):
        kind, target = _local_destination(owner, raw_link)
        if kind in {"local", "anchor"} and target == expected:
            return True
    return False


PROGRAM_LINEAGE_ROADMAP = PurePosixPath(
    "docs/90.references/audits/2026-07-11-weia/remediation-roadmap.md"
)
PROGRAM_LINEAGE_OVERLAY_HEADING = (
    "### 2026-07-15 template lifecycle disposition overlay"
)
PROGRAM_MUTABLE_STATES = frozenset({"draft", "active"})
PROGRAM_CURRENT_EXECUTION_STATES = frozenset(
    {"draft", "active", "queued", "in-progress", "blocked"}
)
PROGRAM_CURRENT_TASK_STATES = frozenset({"queued", "in-progress", "blocked"})
PROGRAM_TASK_STATUS_DOMAIN = frozenset(
    {"queued", "in-progress", "blocked", "done", "cancelled"}
)
PROGRAM_PATHS = {
    "sdlc/prd": re.compile(r"^docs/01\.requirements/({identifier})-[^/]+\.md$"),
    "sdlc/ad": re.compile(
        r"^docs/02\.architecture/descriptions/ad-({identifier})-[^/]+\.md$"
    ),
    "sdlc/adr": re.compile(
        r"^docs/02\.architecture/decisions/({identifier})-[^/]+\.md$"
    ),
    "sdlc/spec": re.compile(r"^docs/03\.specs/({identifier})-[^/]+/spec\.md$"),
}
PROGRAM_TRANSITION_OWNER_CONTRACTS = {
    "sdlc/prd": (
        "sdlc/requirement-package",
        re.compile(r"^docs/01\.requirements/({identifier})-[^/]+\.md$"),
    ),
    "sdlc/ad": (
        "sdlc/ad",
        re.compile(r"^docs/02\.architecture/descriptions/({identifier})-[^/]+\.md$"),
    ),
}
PROGRAM_LIFECYCLE_AUTHORITY = {
    "prd": "draft -> active -> done | archived",
    "ad/adr": "draft -> active -> accepted | archived",
    "spec": "draft -> active -> done | archived",
    "plan/task": "draft -> active -> done | archived",
    "operations": "draft -> active -> accepted | archived",
    "archive record": "archived only",
}


def _program_owner_path(
    context: Context, profile_id: str, identifier: str
) -> PurePosixPath | None:
    """Resolve one numeric owner from the already bounded tracked inventory."""

    owner_profile_id = profile_id
    pattern_template = PROGRAM_PATHS[profile_id].pattern
    if (
        context.route_state == "transition"
        and profile_id in PROGRAM_TRANSITION_OWNER_CONTRACTS
    ):
        owner_profile_id, pattern = PROGRAM_TRANSITION_OWNER_CONTRACTS[profile_id]
        pattern_template = pattern.pattern
    pattern = re.compile(pattern_template.format(identifier=re.escape(identifier)))
    matches = tuple(
        path
        for path in context.paths
        if context.profiles[path].profile_id == owner_profile_id
        and pattern.fullmatch(path.as_posix()) is not None
    )
    return matches[0] if len(matches) == 1 else None


def _program_local_targets(
    context: Context, source: PurePosixPath
) -> frozenset[PurePosixPath]:
    """Return rendered, normalized, repository-local targets for one owner."""

    targets: set[PurePosixPath] = set()
    accepted_history = _work105_accepted_history_source(context, source)
    transition_aliases: dict[PurePosixPath, PurePosixPath] = {}
    if accepted_history and context.route_state == "transition":
        transition_aliases, _, _ = _work109_migration_projection(context)
    for raw_link in _extract_links(context.texts.get(source, "")):
        kind, target = _local_destination(source, raw_link)
        if kind == "local" and target is not None:
            if target in WORK105_LEDGER_PATH_ALIASES and accepted_history:
                target = WORK105_LEDGER_PATH_ALIASES[target]
            elif target in transition_aliases:
                target = transition_aliases[target]
            targets.add(target)
    return frozenset(targets)


def _program_status(context: Context, path: PurePosixPath | None) -> str:
    if path is None:
        return ""
    value = context.metadata.get(path, {}).get("status", "")
    return value if isinstance(value, str) else ""


def _reference_definition_labels(text: str) -> frozenset[str]:
    """Collect only rendered definitions with a fully valid destination/title."""

    rendered = _mask_inline_html_tokens(_rendered_markdown(text))
    return frozenset(_reference_definitions(rendered))


def _rendered_inline_cell_text(value: str, definitions: frozenset[str]) -> str:
    """Replace rendered links using a code-masked offset-stable scan."""

    visible = _mask_inline_html_tokens(value)
    links = _scan_markdown_links(visible, {label: "" for label in definitions})
    code_masked = _mask_inline_code_spans(visible)
    output: list[str] = []
    cursor = 0

    def source_start(encoded_index: int) -> int:
        if encoded_index >= len(visible.source_offsets):
            return len(value)
        return visible.source_offsets[encoded_index]

    def source_end(encoded_index: int) -> int:
        if encoded_index <= 0:
            return 0
        return visible.source_offsets[encoded_index - 1] + 1

    for link in links:
        if code_masked[link.start] == " ":
            continue
        output.append(value[cursor : source_start(link.start)])
        encoded_label_start = link.start + 1
        encoded_label_end = encoded_label_start + len(link.label)
        output.append(
            value[source_start(encoded_label_start) : source_end(encoded_label_end)]
        )
        cursor = source_end(link.end)
    output.append(value[cursor:])
    return "".join(output)


def _rendered_character_reference_text(value: str) -> str:
    """Decode rendered character references outside code and escapes."""

    visible = _mask_inline_code_spans(value)
    output: list[str] = []
    cursor = 0
    while cursor < len(value):
        if (
            visible[cursor] == "\\"
            and cursor + 1 < len(value)
            and _markdown_escapable(value[cursor + 1])
        ):
            output.append(value[cursor + 1])
            cursor += 2
            continue
        if visible[cursor] == "&":
            reference = _markdown_character_reference(value, cursor, len(value))
            if reference is not None:
                decoded, cursor = reference
                output.append(decoded)
                continue
        output.append(value[cursor])
        cursor += 1
    return "".join(output)


def _normalized_lifecycle_cell(
    value: str, definitions: frozenset[str] = frozenset()
) -> str:
    rendered = _rendered_inline_cell_text(value, definitions)
    rendered = _rendered_inline_html_text(rendered)
    rendered = _rendered_character_reference_text(rendered)
    normalized = unicodedata.normalize("NFKC", rendered).casefold()
    normalized = normalized.replace("\\|", "|").replace("→", "->")
    normalized = re.sub(r"[`*_]+", "", normalized)
    normalized = re.sub(r"\s*->\s*", " -> ", normalized)
    normalized = re.sub(r"\s*\|\s*", " | ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _optional_gfm_table_cells(line: str) -> list[str]:
    """Parse a GFM table row with optional leading and trailing pipes."""

    stripped = line.strip()
    if "|" not in stripped:
        return []
    return _gfm_table_cells(stripped if stripped.startswith("|") else f"| {stripped}")


def _strip_blockquote_marker(line: str) -> str | None:
    """Strip one explicit blockquote marker from a rendered container line."""

    marker = re.match(r"^ {0,3}>[ \t]?(.*)$", line)
    return marker.group(1) if marker is not None else None


def _strip_list_item_marker(line: str) -> tuple[str, int] | None:
    """Return first-line content and continuation indent for one list item."""

    leading = re.match(r"^ {0,3}", line)
    assert leading is not None
    marker = re.match(r"(?:[*+-]|\d{1,9}[.)])", line[leading.end() :])
    if marker is None:
        return None
    marker_text = marker.group(0)
    cursor = leading.end() + marker.end()
    marker_end_column = leading.end() + len(marker_text)
    whitespace_start = cursor
    column = marker_end_column
    while cursor < len(line) and line[cursor] in " \t":
        column = column + 1 if line[cursor] == " " else ((column // 4) + 1) * 4
        cursor += 1
    body = line[cursor:]
    if body and cursor == whitespace_start:
        return None
    if not body:
        padding = 1
        content = ""
    elif column - marker_end_column <= 4:
        padding = column - marker_end_column
        content = body
    else:
        padding = 1
        content = " " * (column - marker_end_column - 1) + body
    content_indent = marker_end_column + padding
    return content, content_indent


def _strip_indentation_columns(line: str, required: int) -> str | None:
    """Strip visual indentation columns, preserving a tab's overshoot."""

    column = 0
    cursor = 0
    while cursor < len(line) and column < required:
        character = line[cursor]
        if character == " ":
            next_column = column + 1
        elif character == "\t":
            next_column = ((column // 4) + 1) * 4
        else:
            return None
        cursor += 1
        if next_column > required:
            return " " * (next_column - required) + line[cursor:]
        column = next_column
    return line[cursor:] if column == required else None


def _starts_lazy_continuation_block(line: str) -> bool:
    """Return whether an unmarked line starts a real container/block boundary."""

    if line.startswith(("    ", "\t")):
        return True
    if _strip_blockquote_marker(line) is not None:
        return True
    if _strip_list_item_marker(line) is not None:
        return True
    if re.match(r"^ {0,3}(?:`{3,}|~{3,})", line) is not None:
        return True
    if re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", line) is not None:
        return True
    if (
        re.fullmatch(
            r" {0,3}(?:(?:\*[ \t]*){3,}|"
            r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})",
            line,
        )
        is not None
    ):
        return True
    if re.match(r"^ {0,3}(?:<!--|<\?|<!\[CDATA\[|<![A-Z])", line) is not None:
        return True
    return _HTML_BLOCK_TAG.match(line) is not None or (
        _HTML_COMPLETE_TAG.match(line) is not None
    )


def _is_lazy_paragraph_line(line: str) -> bool:
    return bool(line.strip()) and not _starts_lazy_continuation_block(line)


def _is_lazy_paragraph_continuation(line: str) -> bool:
    """Admit indentation as text while a container paragraph remains open."""

    return bool(line.strip()) and (
        line.startswith(("    ", "\t")) or not _starts_lazy_continuation_block(line)
    )


def _explicit_container_paragraph_state(line: str, previous_paragraph: bool) -> bool:
    """Track paragraphs for explicitly owned quote/list continuation lines."""

    if previous_paragraph and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", line):
        return False
    return _is_lazy_paragraph_line(line)


def _owned_container_paragraph_state(
    lines: Sequence[str],
    previous_paragraph: bool,
    *,
    lazy_continuation: bool = False,
    lazy_lines: frozenset[int] = frozenset(),
) -> bool:
    """Close paragraph state when owned lines end in a valid definition."""

    value = "\n".join(lines)
    _, definition_spans = _reference_definitions_with_spans(
        value,
        lazy_lines=lazy_lines,
    )
    if any(end == len(value) for _, end in definition_spans):
        return False
    if lazy_continuation:
        return True
    return _explicit_container_paragraph_state(lines[-1], previous_paragraph)


@dataclass(frozen=True)
class RenderedBlockLine:
    container_id: int
    depth: int
    text: str
    lazy_continuation: bool = False


class RenderedMarkdown(str):
    """Rendered text carrying line provenance needed by later block scans."""

    lazy_lines: frozenset[int]

    def __new__(
        cls,
        value: str,
        lazy_lines: frozenset[int] = frozenset(),
    ) -> "RenderedMarkdown":
        instance = super().__new__(cls, value)
        instance.lazy_lines = lazy_lines
        return instance


def _rendered_container_lines(text: str) -> tuple[RenderedBlockLine, ...]:
    """Render containers outside-in so outer opaque state hides descendants."""

    contents = _commonmark_splitlines(
        _render_container_markdown(text, defer_indented_code=True)
    )
    depths = [0] * len(contents)
    container_paths: list[tuple[int, ...]] = [()] * len(contents)
    lazy_continuations = [False] * len(contents)
    next_container_id = 0
    while True:
        changed = False
        index = 0
        while index < len(contents):
            depth = depths[index]
            container_path = container_paths[index]
            stripped = _strip_blockquote_marker(contents[index])
            if stripped is not None:
                end = index + 1
                stripped_lines = [stripped]
                stripped_lazy = [lazy_continuations[index]]
                paragraph_open = _owned_container_paragraph_state(
                    stripped_lines,
                    False,
                    lazy_lines=frozenset(
                        offset for offset, lazy in enumerate(stripped_lazy) if lazy
                    ),
                )
                while (
                    end < len(contents)
                    and depths[end] == depth
                    and container_paths[end] == container_path
                ):
                    candidate = _strip_blockquote_marker(contents[end])
                    if candidate is not None:
                        stripped_lines.append(candidate)
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    if paragraph_open and _is_lazy_paragraph_continuation(
                        contents[end]
                    ):
                        stripped_lines.append(contents[end])
                        lazy_continuations[end] = True
                        stripped_lazy.append(True)
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_continuation=True,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    break
            else:
                list_item = _strip_list_item_marker(contents[index])
                if list_item is None:
                    index += 1
                    continue
                first_line, content_indent = list_item
                end = index + 1
                stripped_lines = [first_line]
                stripped_lazy = [lazy_continuations[index]]
                paragraph_open = _owned_container_paragraph_state(
                    stripped_lines,
                    False,
                    lazy_lines=frozenset(
                        offset for offset, lazy in enumerate(stripped_lazy) if lazy
                    ),
                )
                while (
                    end < len(contents)
                    and depths[end] == depth
                    and container_paths[end] == container_path
                ):
                    continuation = contents[end]
                    if not continuation.strip():
                        stripped_lines.append("")
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = False
                        end += 1
                        continue
                    stripped_continuation = _strip_indentation_columns(
                        continuation, content_indent
                    )
                    if stripped_continuation is not None:
                        stripped_lines.append(stripped_continuation)
                        stripped_lazy.append(lazy_continuations[end])
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    if paragraph_open and _is_lazy_paragraph_continuation(continuation):
                        stripped_lines.append(continuation)
                        lazy_continuations[end] = True
                        stripped_lazy.append(True)
                        paragraph_open = _owned_container_paragraph_state(
                            stripped_lines,
                            paragraph_open,
                            lazy_continuation=True,
                            lazy_lines=frozenset(
                                offset
                                for offset, lazy in enumerate(stripped_lazy)
                                if lazy
                            ),
                        )
                        end += 1
                        continue
                    break
            visible = _render_container_markdown(
                "\n".join(stripped_lines),
                defer_indented_code=True,
                paragraph_continuation_lines=frozenset(
                    offset for offset, lazy in enumerate(stripped_lazy) if lazy
                ),
            ).split("\n")
            visible.extend("" for _ in range(len(stripped_lines) - len(visible)))
            child_container_id = next_container_id
            next_container_id += 1
            for offset, line in enumerate(visible[: len(stripped_lines)]):
                position = index + offset
                contents[position] = line
                depths[position] += 1
                container_paths[position] = (
                    *container_path,
                    child_container_id,
                )
            changed = True
            index = end
        if not changed:
            break

    rendered: list[RenderedBlockLine] = []
    index = 0
    container_id = 0
    while index < len(contents):
        depth = depths[index]
        container_path = container_paths[index]
        end = index + 1
        while (
            end < len(contents)
            and depths[end] == depth
            and container_paths[end] == container_path
        ):
            end += 1
        visible = _render_container_markdown(
            "\n".join(contents[index:end]),
            paragraph_continuation_lines=frozenset(
                position - index
                for position in range(index, end)
                if lazy_continuations[position]
            ),
        ).split("\n")
        visible.extend("" for _ in range(end - index - len(visible)))
        rendered.extend(
            RenderedBlockLine(
                container_id,
                depth,
                line,
                lazy_continuations[index + offset],
            )
            for offset, line in enumerate(visible[: end - index])
        )
        index = end
        container_id += 1
    return tuple(rendered)


def _join_rendered_container_lines(
    lines: Sequence[RenderedBlockLine],
) -> str:
    """Join rendered lines with CommonMark/GFM inline-block boundaries."""

    def same_container(left: int, right: int) -> bool:
        return (
            lines[left].container_id == lines[right].container_id
            and lines[left].depth == lines[right].depth
        )

    table_lines: set[int] = set()
    table_index = 0
    while table_index < len(lines) - 1:
        header = _optional_gfm_table_cells(lines[table_index].text)
        delimiter = _optional_gfm_table_cells(lines[table_index + 1].text)
        if (
            same_container(table_index, table_index + 1)
            and not lines[table_index].lazy_continuation
            and not lines[table_index + 1].lazy_continuation
            and header
            and len(header) == len(delimiter)
            and all(re.fullmatch(r":?-+:?", cell) for cell in delimiter)
        ):
            cursor = table_index + 2
            table_lines.update({table_index, table_index + 1})
            while (
                cursor < len(lines)
                and same_container(table_index, cursor)
                and not lines[cursor].lazy_continuation
                and _optional_gfm_table_cells(lines[cursor].text)
            ):
                table_lines.add(cursor)
                cursor += 1
            table_index = cursor
            continue
        table_index += 1

    atx = re.compile(r" {0,3}#{1,6}(?:[ \t]+.*)?")
    list_item = re.compile(r" {0,3}(?:[*+-]|\d{1,9}[.)])(?:[ \t]+.*)?")
    setext = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
    thematic = re.compile(
        r" {0,3}(?:(?:\*[ \t]*){3,}|"
        r"(?:_[ \t]*){3,}|(?:-[ \t]*){3,})"
    )

    definition_lines: set[int] = set()
    definition_end_lines: set[int] = set()
    segment_start = 0
    while segment_start < len(lines):
        segment_end = segment_start + 1
        while segment_end < len(lines) and same_container(segment_start, segment_end):
            segment_end += 1
        segment = "\n".join(line.text for line in lines[segment_start:segment_end])
        _, definition_spans = _reference_definitions_with_spans(
            segment,
            lazy_lines=frozenset(
                offset
                for offset, line in enumerate(lines[segment_start:segment_end])
                if line.lazy_continuation
            ),
        )
        for definition_start, definition_end in definition_spans:
            first_line = segment.count("\n", 0, definition_start)
            last_line = segment.count("\n", 0, definition_end)
            definition_lines.update(
                range(
                    segment_start + first_line,
                    segment_start + last_line + 1,
                )
            )
            definition_end_lines.add(segment_start + last_line)
        segment_start = segment_end

    paragraph_continuation_lines: set[int] = set()
    segment_start = 0
    while segment_start < len(lines):
        segment_end = segment_start + 1
        while segment_end < len(lines) and same_container(segment_start, segment_end):
            segment_end += 1
        paragraph_open = False
        for index in range(segment_start, segment_end):
            value = lines[index].text
            if not value.strip():
                paragraph_open = False
                continue
            if index in definition_lines:
                paragraph_open = False
                continue
            if (
                atx.fullmatch(value) is not None
                or thematic.fullmatch(value) is not None
                or (
                    paragraph_open
                    and not lines[index].lazy_continuation
                    and setext.fullmatch(value) is not None
                )
            ):
                paragraph_open = False
                continue
            if paragraph_open:
                paragraph_continuation_lines.add(index)
            paragraph_open = True
        segment_start = segment_end

    def starts_inline_block(value: str) -> bool:
        return any(
            pattern.fullmatch(value) is not None
            for pattern in (atx, list_item, setext, thematic)
        )

    def ends_inline_block(value: str) -> bool:
        return any(
            pattern.fullmatch(value) is not None for pattern in (atx, setext, thematic)
        )

    def hard_bound_table_cells(value: str) -> str:
        output: list[str] = []
        backslashes = 0
        for character in value:
            if character == "|" and backslashes % 2 == 0:
                output.append("|\n\n")
            else:
                output.append(character)
            backslashes = backslashes + 1 if character == "\\" else 0
        return "".join(output)

    output: list[str] = []
    output_lazy_lines: set[int] = set()
    output_line = 0

    def append_output(value: str, *, lazy: bool = False) -> None:
        nonlocal output_line
        if output:
            output_line += 1
        if lazy:
            output_lazy_lines.add(output_line)
        output.append(value)
        output_line += value.count("\n")

    for index, line in enumerate(lines):
        marker_boundary = (
            index not in definition_lines
            and not line.lazy_continuation
            and starts_inline_block(line.text)
        )
        previous_marker_boundary = (
            index > 0
            and index - 1 not in definition_lines
            and not lines[index - 1].lazy_continuation
            and ends_inline_block(lines[index - 1].text)
        )
        setext_content_boundary = (
            index + 1 < len(lines)
            and same_container(index, index + 1)
            and index not in definition_lines
            and index + 1 not in definition_lines
            and index not in paragraph_continuation_lines
            and not lines[index + 1].lazy_continuation
            and setext.fullmatch(lines[index + 1].text) is not None
        )
        definition_end_boundary = (
            index > 0
            and index - 1 in definition_end_lines
            and index not in definition_lines
        )
        if index > 0 and (
            not same_container(index - 1, index)
            or marker_boundary
            or previous_marker_boundary
            or setext_content_boundary
            or definition_end_boundary
            or index in table_lines
        ):
            append_output("")
        append_output(
            hard_bound_table_cells(line.text) if index in table_lines else line.text,
            lazy=line.lazy_continuation,
        )
    return RenderedMarkdown(
        "\n".join(output),
        frozenset(output_lazy_lines),
    )


def _rendered_markdown(text: str) -> str:
    """Return one container-aware rendered Markdown view."""

    return _join_rendered_container_lines(_rendered_container_lines(text))


def _visible_tables(text: str) -> tuple[tuple[list[str], list[list[str]]], ...]:
    """Parse all visible GFM-shaped tables, preserving overflow cells."""

    lines = _rendered_container_lines(text)
    tables: list[tuple[list[str], list[list[str]]]] = []
    index = 0
    while index < len(lines) - 1:
        header_line = lines[index]
        delimiter_line = lines[index + 1]
        header = _optional_gfm_table_cells(header_line.text)
        delimiter = _optional_gfm_table_cells(delimiter_line.text)
        if (
            header_line.container_id != delimiter_line.container_id
            or header_line.depth != delimiter_line.depth
            or header_line.lazy_continuation
            or delimiter_line.lazy_continuation
            or not header
            or len(header) != len(delimiter)
            or not all(re.fullmatch(r":?-+:?", cell) for cell in delimiter)
        ):
            index += 1
            continue
        rows: list[list[str]] = []
        cursor = index + 2
        while cursor < len(lines):
            row_line = lines[cursor]
            cells = _optional_gfm_table_cells(row_line.text)
            if (
                row_line.container_id != header_line.container_id
                or row_line.depth != header_line.depth
                or row_line.lazy_continuation
                or not cells
            ):
                break
            rows.append(cells)
            cursor += 1
        tables.append((header, rows))
        index = cursor
    return tuple(tables)


def _has_duplicate_lifecycle_authority(text: str) -> bool:
    """Detect the complete Stage 99 lifecycle map after rendered normalization."""

    definitions = _reference_definition_labels(text)
    for header, rows in _visible_tables(text):
        normalized_header = tuple(
            _normalized_lifecycle_cell(cell, definitions) for cell in header
        )
        if (
            normalized_header.count("document family") != 1
            or normalized_header.count("lifecycle transition") != 1
        ):
            continue
        family_index = normalized_header.index("document family")
        transition_index = normalized_header.index("lifecycle transition")
        required_width = max(family_index, transition_index) + 1
        normalized_rows: dict[str, set[str]] = collections.defaultdict(set)
        for row in rows:
            if len(row) < required_width:
                continue
            family = _normalized_lifecycle_cell(row[family_index], definitions)
            transition = _normalized_lifecycle_cell(row[transition_index], definitions)
            normalized_rows[family].add(transition)
        if all(
            transition in normalized_rows.get(family, set())
            for family, transition in PROGRAM_LIFECYCLE_AUTHORITY.items()
        ):
            return True
    return False


def _program_reciprocal_diagnostics(
    context: Context,
    program: ProgramLineage,
    relation: ProgramRelation,
    *,
    follow_up: bool,
) -> list[Diagnostic]:
    spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
    prd = _program_owner_path(context, "sdlc/prd", program.prd_id)
    ard = _program_owner_path(context, "sdlc/ad", program.ad_id)
    decision = _program_owner_path(context, "sdlc/adr", relation.decision_id)
    if spec is None or prd is None or ard is None or (follow_up and decision is None):
        return []
    required_from_spec = {prd, ard}
    if follow_up:
        assert decision is not None
        required_from_spec.add(decision)
    missing: list[str] = []
    spec_targets = _program_local_targets(context, spec)
    for label, target in (("PRD", prd), ("AD", ard), ("ADR", decision)):
        if (
            target is not None
            and target in required_from_spec
            and target not in spec_targets
        ):
            missing.append(f"Spec->{label}")
    for label, upstream in (("PRD", prd), ("AD", ard), ("ADR", decision)):
        if (
            upstream is not None
            and (
                _program_status(context, upstream) in PROGRAM_MUTABLE_STATES
                or (follow_up and label == "ADR")
            )
            and spec not in _program_local_targets(context, upstream)
        ):
            missing.append(f"{label}->Spec")
    if not missing:
        return []
    return [
        _diag(
            "PROGRAM-LINEAGE-RECIPROCAL",
            spec,
            context.profiles[spec].profile_id,
            "rendered reciprocal links required by the mutable relation",
            ", ".join(sorted(missing)),
        )
    ]


def _historical_exception_diagnostics(
    context: Context,
    program: ProgramLineage,
    follow_up: ProgramFollowUp,
) -> list[Diagnostic]:
    if context.route_state == "terminal":
        return []
    if follow_up.evidence_mode != "successor-record":
        return []
    spec = _program_owner_path(context, "sdlc/spec", follow_up.spec_id)
    prd = _program_owner_path(context, "sdlc/prd", program.prd_id)
    ard = _program_owner_path(context, "sdlc/ad", program.ad_id)
    decision = _program_owner_path(context, "sdlc/adr", follow_up.decision_id)
    exact_relation = (
        program.prd_id == "0005"
        and program.ad_id == "0008"
        and follow_up.spec_id == "0033"
        and follow_up.decision_id == "0017"
        and follow_up.state == "done"
    )
    move_targets: dict[PurePosixPath, PurePosixPath] = {}
    reviewed_alias_edges: dict[ArchiveTransitionEdge, PurePosixPath] = {}
    if context.route_state == "transition":
        _, move_targets, _ = _document_taxonomy_transition_manifest(context)
        reviewed_alias_edges = _reviewed_immutable_historical_alias_edges(
            context, move_targets
        )

    def source_pinned_targets(source: PurePosixPath) -> set[PurePosixPath]:
        return {
            reviewed_alias_edges.get(ArchiveTransitionEdge(source, target), target)
            for raw_link in _extract_links(context.texts.get(source, ""))
            for kind, target in (_local_destination(source, raw_link),)
            if kind == "local" and target is not None
        }

    adr_agrees = (
        spec is not None
        and prd is not None
        and ard is not None
        and decision is not None
        and _program_status(context, decision) == "accepted"
        and {spec, prd, ard}.issubset(source_pinned_targets(decision))
    )
    roadmap_section = (
        _exact_rendered_heading_section(
            context.texts.get(PROGRAM_LINEAGE_ROADMAP, ""),
            PROGRAM_LINEAGE_OVERLAY_HEADING,
        )
        if PROGRAM_LINEAGE_ROADMAP in context.texts
        else None
    )
    overlay_targets = (
        {
            target
            for raw_link in _extract_rendered_links(roadmap_section)
            for kind, target in [_local_destination(PROGRAM_LINEAGE_ROADMAP, raw_link)]
            if kind == "local" and target is not None
        }
        if roadmap_section is not None
        else set()
    )
    projected_overlay_targets = {
        reviewed_alias_edges.get(
            ArchiveTransitionEdge(PROGRAM_LINEAGE_ROADMAP, target), target
        )
        for target in overlay_targets
    }
    overlay_agrees = (
        spec is not None
        and roadmap_section is not None
        and spec in projected_overlay_targets
    )
    if exact_relation and adr_agrees and overlay_agrees:
        return []
    owner = spec or decision or prd or PROGRAM_LINEAGE_ROADMAP
    profile = (
        context.profiles[owner].profile_id if owner in context.profiles else "sdlc/spec"
    )
    return [
        _diag(
            "PROGRAM-LINEAGE-HISTORICAL-EXCEPTION",
            owner,
            profile,
            "exact PRD-0005/AD-0008/Spec-033/ADR-0017 registry, ADR, and Current-overlay agreement",
            "successor-record evidence is incomplete or outside the named exception",
        )
    ]


def _current_execution_link_graph(
    context: Context,
) -> dict[PurePosixPath, frozenset[PurePosixPath]]:
    """Return rendered local links for every current Plan/Task node."""

    return {
        path: _program_local_targets(context, path)
        for path in context.paths
        if context.profiles[path].profile_id in {"sdlc/plan", "sdlc/task"}
        and _program_status(context, path) in PROGRAM_CURRENT_EXECUTION_STATES
    }


def _program_package_task_projection(
    context: Context,
    spec: PurePosixPath,
) -> tuple[
    tuple[PurePosixPath, ...],
    tuple[PurePosixPath, ...],
    bool,
]:
    """Return one Spec package's exact Task inventory and current subset."""

    task_root = spec.parent / "tasks"
    task_name = re.compile(r"^tsk-[0-9]{4}-[^/]+\.md$")
    package_tasks = tuple(
        sorted(
            (
                path
                for path in context.paths
                if path.parent == task_root
                and context.profiles[path].profile_id == "sdlc/task"
            ),
            key=lambda item: item.as_posix(),
        )
    )
    current_tasks = tuple(
        path
        for path in package_tasks
        if _program_status(context, path) in PROGRAM_CURRENT_TASK_STATES
    )
    router = spec.parent / "README.md"
    router_targets = tuple(
        target
        for raw_link in _extract_links(context.texts.get(router, ""))
        for kind, target in (_local_destination(router, raw_link),)
        if kind == "local" and target is not None
        if target in context.profiles
        and context.profiles[target].profile_id == "sdlc/task"
    )
    spec_identifier = spec.parent.name[:4]
    identities_complete = all(
        task.name[4:8] == f"{sequence:04d}"
        and context.metadata[task].get("artifact_id")
        == f"TSK-{spec_identifier}-{sequence:04d}"
        for sequence, task in enumerate(package_tasks, start=1)
    )
    router_complete = (
        router in context.paths
        and context.profiles[router].profile_id == "readme/collection-index"
        and bool(package_tasks)
        and all(task_name.fullmatch(path.name) is not None for path in package_tasks)
        and identities_complete
        and all(
            _program_status(context, path) in PROGRAM_TASK_STATUS_DOMAIN
            for path in package_tasks
        )
        and len(router_targets) == len(set(router_targets))
        and set(router_targets) == set(package_tasks)
    )
    return package_tasks, current_tasks, router_complete


@dataclass
class CurrentExecutionIndex:
    graph: dict[PurePosixPath, frozenset[PurePosixPath]]
    adjacency: dict[PurePosixPath, frozenset[PurePosixPath]]
    incoming: dict[PurePosixPath, frozenset[PurePosixPath]]
    component_by_node: dict[PurePosixPath, tuple[PurePosixPath, ...]]
    component_cache: dict[
        tuple[PurePosixPath, tuple[PurePosixPath, ...]],
        tuple[PurePosixPath, ...],
    ]
    steps: int


@dataclass(frozen=True)
class ExecutionComponentScan:
    paths: tuple[PurePosixPath, ...]
    steps: int


def _current_execution_index(
    graph: dict[PurePosixPath, frozenset[PurePosixPath]],
) -> CurrentExecutionIndex:
    """Index execution adjacency and connected components once."""

    frozen_graph = {path: frozenset(targets) for path, targets in graph.items()}
    adjacency = {path: set() for path in frozen_graph}
    incoming: dict[PurePosixPath, set[PurePosixPath]] = {}
    steps = 0
    for source, targets in frozen_graph.items():
        for target in targets:
            steps += 1
            incoming.setdefault(target, set()).add(source)
            if target in frozen_graph:
                adjacency[source].add(target)
                adjacency[target].add(source)

    component_by_node: dict[PurePosixPath, tuple[PurePosixPath, ...]] = {}
    visited: set[PurePosixPath] = set()
    for root in frozen_graph:
        steps += 1
        if root in visited:
            continue
        visited.add(root)
        pending = [root]
        members: list[PurePosixPath] = []
        while pending:
            source = pending.pop()
            members.append(source)
            steps += 1
            for candidate in adjacency[source]:
                steps += 1
                if candidate not in visited:
                    visited.add(candidate)
                    pending.append(candidate)
        component = tuple(sorted(members, key=lambda item: item.as_posix()))
        for member in members:
            component_by_node[member] = component
            steps += 1

    return CurrentExecutionIndex(
        frozen_graph,
        {path: frozenset(targets) for path, targets in adjacency.items()},
        {path: frozenset(sources) for path, sources in incoming.items()},
        component_by_node,
        {},
        steps,
    )


def _current_execution_component_scan(
    spec: PurePosixPath,
    spec_targets: frozenset[PurePosixPath],
    index: CurrentExecutionIndex,
) -> ExecutionComponentScan:
    """Close one Spec's execution seeds through cached graph components."""

    execution_targets = tuple(
        sorted(
            (target for target in spec_targets if target in index.graph),
            key=lambda item: item.as_posix(),
        )
    )
    cache_key = (spec, execution_targets)
    cached = index.component_cache.get(cache_key)
    if cached is not None:
        return ExecutionComponentScan(cached, 0)

    seeds = set(index.incoming.get(spec, ()))
    seeds.update(execution_targets)
    members: set[PurePosixPath] = set()
    seen_components: set[PurePosixPath] = set()
    steps = len(seeds)
    for seed in sorted(seeds, key=lambda item: item.as_posix()):
        component = index.component_by_node[seed]
        representative = component[0]
        if representative in seen_components:
            continue
        seen_components.add(representative)
        members.update(component)
        steps += len(component)
    result = tuple(sorted(members, key=lambda item: item.as_posix()))
    index.component_cache[cache_key] = result
    return ExecutionComponentScan(result, steps)


def _current_execution_component(
    context: Context,
    spec: PurePosixPath,
    index: CurrentExecutionIndex,
) -> tuple[PurePosixPath, ...]:
    """Close the current execution component seeded only by one relation Spec.

    A Plan/Task node is in scope when a rendered local link joins it directly
    to the Spec or transitively to another scoped execution node. Disconnected
    components therefore remain outside this program relation.
    """

    return _current_execution_component_scan(
        spec,
        _program_local_targets(context, spec),
        index,
    ).paths


def _program_execution_diagnostics(
    context: Context,
    program: ProgramLineage,
    graph: dict[PurePosixPath, frozenset[PurePosixPath]],
    execution_index: CurrentExecutionIndex,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    relations = (*program.tranches, *program.follow_ups)
    dependency_ready = next(
        (
            relation
            for relation in program.tranches
            if relation.state not in {"done", "archived"}
        ),
        None,
    )
    for relation in relations:
        spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
        if spec is None:
            continue
        component = _current_execution_component(context, spec, execution_index)
        plans = tuple(
            path
            for path in component
            if context.profiles[path].profile_id == "sdlc/plan"
        )
        tasks = tuple(
            path
            for path in component
            if context.profiles[path].profile_id == "sdlc/task"
        )
        direct_spec_links = all(spec in graph[path] for path in component)
        execution_state_matches = all(
            _program_status(context, path) == relation.state for path in component
        )
        reciprocal_pair = (
            len(plans) == 1
            and len(tasks) == 1
            and tasks[0] in graph[plans[0]]
            and plans[0] in graph[tasks[0]]
        )
        valid_execution_pair = (
            len(plans) == 1
            and len(tasks) == 1
            and direct_spec_links
            and execution_state_matches
            and reciprocal_pair
        )
        package_tasks, current_package_tasks, router_complete = (
            _program_package_task_projection(context, spec)
        )
        package_task_targets = {
            task: _program_local_targets(context, task) for task in package_tasks
        }
        plan_targets = (
            graph.get(plans[0], frozenset()) if len(plans) == 1 else frozenset()
        )
        package_direct_spec_links = (
            len(plans) == 1
            and spec in plan_targets
            and all(spec in package_task_targets[task] for task in package_tasks)
        )
        package_reciprocal = (
            len(plans) == 1
            and bool(package_tasks)
            and all(plans[0] in package_task_targets[task] for task in package_tasks)
            and any(task in plan_targets for task in package_tasks)
        )
        package_component_complete = len(plans) == 1 and set(tasks) == set(
            current_package_tasks
        )
        package_statuses = tuple(
            _program_status(context, task) for task in package_tasks
        )
        package_state_matches = (
            len(plans) == 1
            and _program_status(context, plans[0]) == relation.state
            and (
                (
                    relation.state == "draft"
                    and bool(package_statuses)
                    and all(
                        status in PROGRAM_CURRENT_TASK_STATES
                        for status in package_statuses
                    )
                    and (
                        all(status == "queued" for status in package_statuses)
                        or (
                            relation == dependency_ready
                            and "in-progress" in package_statuses
                        )
                    )
                )
                or (
                    relation.state == "active"
                    and (
                        (
                            bool(current_package_tasks)
                            and "in-progress" in package_statuses
                            and all(
                                status in PROGRAM_CURRENT_TASK_STATES
                                for status in package_statuses
                            )
                        )
                        or (
                            not current_package_tasks
                            and bool(package_statuses)
                            and all(
                                status in {"done", "cancelled"}
                                for status in package_statuses
                            )
                        )
                    )
                )
            )
        )
        valid_execution_package = (
            router_complete
            and package_component_complete
            and package_direct_spec_links
            and package_reciprocal
            and package_state_matches
        )
        valid_execution = valid_execution_pair or valid_execution_package
        valid_ready_state = relation == dependency_ready and (
            not component or valid_execution
        )
        valid_blocked_state = relation != dependency_ready and (
            not component
            or (
                not isinstance(relation, ProgramFollowUp)
                and relation.state == "draft"
                and valid_execution
            )
        )
        if valid_ready_state or valid_blocked_state:
            continue
        diagnostics.append(
            _diag(
                "PROGRAM-LINEAGE-EXECUTION-GATE",
                spec,
                context.profiles[spec].profile_id,
                "zero current execution component; or one closed reciprocal Plan/Task component with direct own-Spec links and relation-state parity for the first unfinished original tranche; draft original successors may retain one such draft pair while follow-ups remain component-free",
                f"component={len(component)}, plans={len(plans)}, tasks={len(tasks)}, direct-spec={direct_spec_links}, execution-state={execution_state_matches}, reciprocal={reciprocal_pair}, dependency-ready-original={relation == dependency_ready}",
            )
        )
    return diagnostics


def _unowned_active_execution_diagnostics(
    context: Context,
    execution_index: CurrentExecutionIndex,
    program_owned_paths: set[PurePosixPath],
) -> list[Diagnostic]:
    """Reject active execution components not seeded by a registry Spec."""

    diagnostics: list[Diagnostic] = []
    reported_components: set[PurePosixPath] = set()
    for path in sorted(execution_index.graph, key=lambda item: item.as_posix()):
        if _program_status(context, path) != "active" or path in program_owned_paths:
            continue
        component = execution_index.component_by_node[path]
        representative = component[0]
        if representative in reported_components:
            continue
        reported_components.add(representative)
        active_paths = tuple(
            candidate
            for candidate in component
            if _program_status(context, candidate) == "active"
            and candidate not in program_owned_paths
        )
        owner = active_paths[0] if active_paths else path
        diagnostics.append(
            _diag(
                "PROGRAM-LINEAGE-EXECUTION-GATE",
                owner,
                context.profiles[owner].profile_id,
                "every active Plan/Task component connected to one registry relation Spec",
                f"unowned active execution component={len(component)}, active={len(active_paths)}",
            )
        )
    return diagnostics


STANDALONE_DECISION_PATH = PurePosixPath(
    "docs/02.architecture/decisions/"
    "0022-direct-approval-standalone-execution-lineage.md"
)
_STANDALONE_DECISION_SPEC_LINK = re.compile(
    r"\]\(\.\./\.\./03\.specs/(?P<spec>[0-9]{4})-[a-z0-9-]+/spec\.md\)"
)


STANDALONE_APPROVAL_STATEMENTS = {
    "0053": (
        "Direct human approval on 2026-08-08 authorizes this standalone execution relation.",
        "No separate PRD or AD is required or part of this standalone lifecycle.",
    ),
    "0054": (
        "Direct human approval on 2026-08-13 authorizes this standalone execution relation.",
        "No separate PRD or Architecture Description is required or part of this standalone lifecycle.",
    ),
    "0062": (
        "Direct human approval on 2026-08-20 authorizes this standalone execution relation.",
        "No separate PRD or Architecture Description is required or part of this standalone lifecycle.",
    ),
    "0063": (
        "Direct human approval on 2026-08-29 authorizes this standalone execution relation.",
        "No separate PRD or Architecture Description is required or part of this standalone lifecycle.",
    ),
    "0064": (
        "Direct human approval on 2026-08-30 authorizes this standalone execution relation.",
        "No separate PRD or Architecture Description is required or part of this standalone lifecycle.",
    ),
}


def _standalone_decision_roster_diagnostics(
    context: Context,
    standalone_executions: Sequence[StandaloneExecution],
) -> list[Diagnostic]:
    """Refuse a standalone roster its accepted decision does not match.

    ADR-0022 names the relations in prose and the registry declares them for
    machines.  Nothing compared the two, so the decision came to link seven
    Specs the registry never held, each with an approval sentence pinned in
    this module: declaring any one of them later would have satisfied
    STANDALONE-EXECUTION-APPROVAL with no human approving it.  A Spec the
    decision links is a Spec the registry declares.  An execution the registry
    cannot hold is named in the decision without a link.
    """

    text = context.texts.get(STANDALONE_DECISION_PATH)
    if text is None:
        return [
            _diag(
                "STANDALONE-DECISION-ROSTER",
                STANDALONE_DECISION_PATH,
                "sdlc/adr",
                "the accepted standalone-execution decision",
                "the decision is absent or untracked",
            )
        ]
    linked = {
        match.group("spec") for match in _STANDALONE_DECISION_SPEC_LINK.finditer(text)
    }
    declared = {relation.spec_id for relation in standalone_executions}
    if linked != declared:
        return [
            _diag(
                "STANDALONE-DECISION-ROSTER",
                STANDALONE_DECISION_PATH,
                "sdlc/adr",
                f"linked Specs equal to the declared roster {sorted(declared)}",
                f"linked={sorted(linked)}",
            )
        ]
    return []


def _standalone_execution_diagnostics(
    context: Context,
    standalone_executions: Sequence[StandaloneExecution],
    graph: dict[PurePosixPath, frozenset[PurePosixPath]],
    execution_index: CurrentExecutionIndex,
) -> tuple[list[Diagnostic], set[PurePosixPath]]:
    diagnostics: list[Diagnostic] = []
    owned_paths: set[PurePosixPath] = set()
    for relation in standalone_executions:
        spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
        decision = _program_owner_path(context, "sdlc/adr", relation.decision_id)
        plan = relation.plan_path
        task = relation.task_path
        owners = (
            (spec, "sdlc/spec"),
            (decision, "sdlc/adr"),
            (plan, "sdlc/plan"),
            (task, "sdlc/task"),
        )
        if any(
            path is None
            or path not in context.profiles
            or context.profiles[path].profile_id != profile_id
            for path, profile_id in owners
        ):
            continue
        assert spec is not None and decision is not None
        for path in (spec, plan, task):
            actual_state = _program_status(context, path)
            task_current_state = (
                path == task
                and relation.state == "active"
                and actual_state in PROGRAM_CURRENT_TASK_STATES
            )
            if actual_state != relation.state and not task_current_state:
                diagnostics.append(
                    _diag(
                        "STANDALONE-EXECUTION-STATE",
                        path,
                        context.profiles[path].profile_id,
                        relation.state,
                        actual_state,
                    )
                )
        spec_targets = _program_local_targets(context, spec)
        decision_targets = _program_local_targets(context, decision)
        if decision not in spec_targets or spec not in decision_targets:
            diagnostics.append(
                _diag(
                    "STANDALONE-EXECUTION-ADR",
                    spec,
                    "sdlc/spec",
                    "reciprocal rendered Spec/accepted-ADR links",
                    "standalone decision reciprocity is incomplete",
                )
            )
        spec_text = context.texts[spec]
        approval_statements = STANDALONE_APPROVAL_STATEMENTS.get(relation.spec_id)
        if approval_statements is None or any(
            statement not in spec_text for statement in approval_statements
        ):
            diagnostics.append(
                _diag(
                    "STANDALONE-EXECUTION-APPROVAL",
                    spec,
                    "sdlc/spec",
                    "the exact direct-human approval and no-separate-PRD/AD statements",
                    "one or both standalone approval statements are absent",
                )
            )
        plan_targets = _program_local_targets(context, plan)
        task_targets = _program_local_targets(context, task)
        reciprocal = task in plan_targets and plan in task_targets
        own_spec = spec in plan_targets and spec in task_targets
        if not reciprocal or not own_spec:
            diagnostics.append(
                _diag(
                    "STANDALONE-EXECUTION-RECIPROCAL",
                    plan,
                    "sdlc/plan",
                    "the exact reciprocal Plan/Task pair with direct owning-Spec links",
                    f"plan-task-reciprocal={reciprocal}, direct-own-spec={own_spec}",
                )
            )
        foreign_specs = sorted(
            {
                target
                for target in (*plan_targets, *task_targets)
                if target in context.profiles
                and context.profiles[target].profile_id == "sdlc/spec"
                and target != spec
            },
            key=lambda item: item.as_posix(),
        )
        if foreign_specs:
            diagnostics.append(
                _diag(
                    "STANDALONE-EXECUTION-SPEC-BOUNDARY",
                    plan,
                    "sdlc/plan",
                    "no rendered Plan/Task link to another Spec",
                    repr([path.as_posix() for path in foreign_specs]),
                )
            )
        if relation.state == "active":
            component = _current_execution_component(context, spec, execution_index)
            owned_paths.update(component)
            if plan not in component or task not in component:
                diagnostics.append(
                    _diag(
                        "STANDALONE-EXECUTION-COMPONENT",
                        spec,
                        "sdlc/spec",
                        "declared active Plan and Task included in the execution component",
                        repr([path.as_posix() for path in component]),
                    )
                )
        else:
            owned_paths.update({plan, task})
    return diagnostics, owned_paths


def _program_lineage_diagnostics(
    context: Context,
    program_lineage: Sequence[ProgramLineage],
    standalone_executions: Sequence[StandaloneExecution] = (),
) -> list[Diagnostic]:
    """Validate registry relations against immutable bodies and current evidence."""

    diagnostics: list[Diagnostic] = []
    graph = _current_execution_link_graph(context)
    execution_index = _current_execution_index(graph)
    program_owned_paths: set[PurePosixPath] = set()
    for program in program_lineage:
        for relation in (*program.tranches, *program.follow_ups):
            spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
            if spec is not None:
                program_owned_paths.update(
                    _current_execution_component(context, spec, execution_index)
                )
    diagnostics.extend(
        _standalone_decision_roster_diagnostics(context, standalone_executions)
    )
    standalone_diagnostics, standalone_owned_paths = _standalone_execution_diagnostics(
        context,
        standalone_executions,
        graph,
        execution_index,
    )
    diagnostics.extend(standalone_diagnostics)
    program_owned_paths.update(standalone_owned_paths)
    for program in program_lineage:
        for relation in (*program.tranches, *program.follow_ups):
            spec = _program_owner_path(context, "sdlc/spec", relation.spec_id)
            actual_state = _program_status(context, spec)
            if spec is None or actual_state != relation.state:
                owner = spec or _program_owner_path(context, "sdlc/prd", program.prd_id)
                if owner is not None:
                    diagnostics.append(
                        _diag(
                            "PROGRAM-LINEAGE-STATE",
                            owner,
                            context.profiles[owner].profile_id,
                            relation.state,
                            actual_state or "missing Spec owner",
                        )
                    )
            if relation.state not in PROGRAM_MUTABLE_STATES:
                continue
            if isinstance(relation, ProgramFollowUp):
                if relation.evidence_mode == "reciprocal-body":
                    diagnostics.extend(
                        _program_reciprocal_diagnostics(
                            context, program, relation, follow_up=True
                        )
                    )
            else:
                diagnostics.extend(
                    _program_reciprocal_diagnostics(
                        context, program, relation, follow_up=False
                    )
                )
        for follow_up in program.follow_ups:
            diagnostics.extend(
                _historical_exception_diagnostics(context, program, follow_up)
            )
        diagnostics.extend(
            _program_execution_diagnostics(
                context,
                program,
                graph,
                execution_index,
            )
        )
    diagnostics.extend(
        _unowned_active_execution_diagnostics(
            context,
            execution_index,
            program_owned_paths,
        )
    )
    for path in context.paths:
        if path.as_posix().startswith(
            "docs/00.agent-governance/"
        ) and _has_duplicate_lifecycle_authority(context.texts[path]):
            diagnostics.append(
                _diag(
                    "PROGRAM-LINEAGE-DUPLICATE-AUTHORITY",
                    path,
                    context.profiles[path].profile_id,
                    "Stage 99 registry/schema/governance pointers without an exact lifecycle owner table",
                    "complete normalized lifecycle transition table",
                )
            )
    return diagnostics


def _body_contract_link_diagnostics(
    context: Context,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str,
    path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Validate registry-owned relationship cells and reciprocal evidence."""

    if body_contracts not in {"registry", "audit"}:
        raise ConfigurationError("body_contracts must be registry or audit")
    diagnostics: list[Diagnostic] = []
    known_paths = set(context.paths)
    for path in context.paths:
        view = context.profiles[path]
        profile = profiles_by_id.get(view.profile_id)
        if profile is None:
            continue
        status_value = context.metadata[path].get("status", "")
        status = status_value if isinstance(status_value, str) else ""
        if not _body_contract_link_is_enforced(
            path, profile, status, body_contracts, path_prefixes
        ):
            continue
        contract = profile.body_contract
        assert contract is not None
        rows = _body_contract_rows(context.texts[path], profile)
        if rows is None:
            continue
        link_columns = (
            (
                "source",
                contract.source_link_column,
                contract.allowed_source_profile_ids,
            ),
            (
                "target",
                contract.target_link_column,
                contract.allowed_target_profile_ids,
            ),
        )
        for row_number, row in enumerate(rows, start=1):
            for direction, column, allowed_profile_ids in link_columns:
                if column is None:
                    continue
                cell = row[column].strip()
                if cell.startswith("N/A"):
                    if (
                        not contract.allow_explicit_exclusion
                        or BODY_LINK_EXCLUSION.fullmatch(cell) is None
                    ):
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-EXCLUSION",
                                path,
                                profile.profile_id,
                                "N/A — followed by a reviewable reason",
                                f"row {row_number}, {column}: {cell}",
                            )
                        )
                    continue
                raw_links = _extract_links(cell, definitions_text=context.texts[path])
                if not raw_links:
                    diagnostics.append(
                        _diag(
                            f"BODY-LINK-{direction.upper()}",
                            path,
                            profile.profile_id,
                            f"a repository-local link or explicit exclusion in {column}",
                            f"row {row_number}: {cell}",
                        )
                    )
                    continue
                for raw_link in raw_links:
                    kind, target = _local_destination(path, raw_link)
                    if kind not in {"local", "anchor"} or target not in known_paths:
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-BROKEN",
                                path,
                                profile.profile_id,
                                "a tracked local lifecycle document",
                                raw_link,
                            )
                        )
                        continue
                    assert target is not None
                    target_view = context.profiles[target]
                    if target_view.profile_id not in allowed_profile_ids:
                        diagnostics.append(
                            _diag(
                                f"BODY-LINK-{direction.upper()}-PROFILE",
                                path,
                                profile.profile_id,
                                json.dumps(allowed_profile_ids),
                                target_view.profile_id,
                            )
                        )
                        continue
                    target_profile = profiles_by_id[target_view.profile_id]
                    target_status_value = context.metadata[target].get("status", "")
                    target_status = (
                        target_status_value
                        if isinstance(target_status_value, str)
                        else ""
                    )
                    reciprocal_in_scope = _body_contract_link_is_enforced(
                        target,
                        target_profile,
                        target_status,
                        body_contracts,
                        path_prefixes,
                    )
                    if (
                        contract.reciprocal_evidence
                        and reciprocal_in_scope
                        and not _links_back_to(context, target, path)
                    ):
                        diagnostics.append(
                            _diag(
                                "BODY-LINK-RECIPROCAL",
                                path,
                                profile.profile_id,
                                f"{target.as_posix()} links back to {path.as_posix()}",
                                f"row {row_number}, {column}: missing reciprocal evidence",
                            )
                        )
    return sorted(diagnostics, key=diagnostic_sort_key)


def _first_cell_target(owner: PurePosixPath, cell: str) -> PurePosixPath | None:
    match = re.fullmatch(r"\[[^\]\n]+\]\(([^)]+)\)", cell)
    if match is None:
        return None
    raw = match.group(1).strip()
    if "?" in raw or "#" in raw:
        return None
    kind, target = _local_destination(owner, raw)
    return target if kind == "local" else None


def _collection_table_targets(
    declaration: CollectionIndex, text: str
) -> tuple[list[PurePosixPath], bool]:
    section = (
        _after_exact_heading(text, declaration.table_anchor)
        if declaration.table_mode == "after"
        else _exact_heading_section(text, declaration.table_anchor)
    )
    if section is None:
        return [], False
    table = _first_visible_table(section)
    if table is None:
        return [], False
    _, rows = table
    targets: list[PurePosixPath] = []
    for row in rows:
        target = _first_cell_target(declaration.path, row[0])
        if target is None:
            return [], False
        targets.append(target)
    return targets, True


def _collection_index_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for declaration in COLLECTION_INDEXES:
        profile = context.profiles[declaration.path].profile_id
        expected = {
            path
            for path in context.tracked_regular_paths
            if declaration.target_pattern.fullmatch(path.as_posix())
        }
        tree, tree_valid = _collection_tree_targets(
            declaration, context.texts[declaration.path]
        )
        rows, table_valid = _collection_table_targets(
            declaration, context.texts[declaration.path]
        )
        expected_rows = set(expected)
        if not declaration.table_includes_self:
            expected_rows.discard(declaration.path)
        if not tree_valid or not table_valid:
            diagnostics.append(
                _diag(
                    "COLLECTION-INDEX-PARSE",
                    declaration.path,
                    profile,
                    "one exact heading, bounded tree, and first-cell link table",
                    "collection index grammar is missing or malformed",
                )
            )
            continue
        tree_counter = collections.Counter(tree)
        row_counter = collections.Counter(rows)
        for target in sorted(expected | set(tree), key=lambda item: item.as_posix()):
            target_key = target.as_posix()
            if target in expected and tree_counter[target] == 0:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one tree entry",
                        f"target={target_key}; entry is missing",
                    )
                )
            if target not in expected and tree_counter[target]:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; tracked canonical artifact",
                        f"target={target_key}; stale tree entry",
                    )
                )
            if tree_counter[target] > 1:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-TREE-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one tree entry",
                        f"target={target_key}; {tree_counter[target]} entries",
                    )
                )
        for target in sorted(
            expected_rows | set(rows), key=lambda item: item.as_posix()
        ):
            target_key = target.as_posix()
            if target in expected_rows and row_counter[target] == 0:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-MISSING",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; row is missing",
                    )
                )
            if target not in expected_rows and row_counter[target]:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-STALE",
                        declaration.path,
                        profile,
                        f"target={target_key}; tracked canonical artifact",
                        f"target={target_key}; stale table row",
                    )
                )
            if row_counter[target] > 1:
                diagnostics.append(
                    _diag(
                        "COLLECTION-INDEX-ROW-DUPLICATE",
                        declaration.path,
                        profile,
                        f"target={target_key}; one table row",
                        f"target={target_key}; {row_counter[target]} rows",
                    )
                )
    return diagnostics


def _owner_candidate(context: Context, path: PurePosixPath) -> bool:
    profile = context.profiles[path]
    status = str(context.metadata[path].get("status", "")).casefold()
    if profile.mode != "authored" or profile.profile_class in {"readme", "exception"}:
        return False
    if profile.profile_id == "content/archive" or status not in {
        "active",
        "accepted",
    }:
        return False
    return not any(pattern.match(path.as_posix()) for pattern in OWNER_EXCLUSIONS)


def _traceability_lineage(context: Context, path: PurePosixPath) -> str:
    visible = _visible_markdown(context.texts[path])
    match = re.search(
        r"^## Traceability\s*$([\s\S]*?)(?=^## |\Z)", visible, re.MULTILINE
    )
    if match:
        for raw in _extract_links(match.group(1), definitions_text=visible):
            kind, target = _local_destination(path, raw)
            if (
                kind == "local"
                and target is not None
                and (
                    re.fullmatch(
                        r"docs/01\.requirements/[0-9]{4}-[^/]+\.md", target.as_posix()
                    )
                    or re.fullmatch(
                        r"docs/03\.specs/[0-9]{4}-[^/]+/spec\.md", target.as_posix()
                    )
                )
            ):
                return _normalize_component(target.as_posix())
    value = path.as_posix()
    if re.fullmatch(r"docs/01\.requirements/[^/]+\.md", value):
        raw = path.stem
    elif re.fullmatch(r"docs/03\.specs/[^/]+/spec\.md", value):
        raw = path.parent.name
    elif re.fullmatch(r"docs/04\.execution/(?:plans|tasks)/[^/]+\.md", value):
        raw = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    else:
        raw = value.removesuffix(".md")
    return _normalize_component(raw)


def _owner_key(context: Context, path: PurePosixPath) -> tuple[str, Diagnostic | None]:
    if not _owner_candidate(context, path):
        return "", None
    metadata = context.metadata[path]
    role = _normalize_component(str(metadata.get("type", "")))
    scope = _normalize_component(str(metadata.get("title", "")))
    suffixes = (
        "product-requirements",
        "architecture-requirements",
        "architecture-decision-record",
        "technical-specification",
        "implementation-plan",
    )
    if scope.startswith("task-"):
        scope = scope[5:]
    else:
        for suffix in suffixes:
            if scope == suffix:
                scope = ""
                break
            if scope.endswith("-" + suffix):
                scope = scope[: -(len(suffix) + 1)]
                break
    lineage = _traceability_lineage(context, path)
    if not role or not scope or not lineage:
        return "", _diag(
            "OWNER-KEY-MISSING",
            path,
            context.profiles[path].profile_id,
            "role|scope|lineage",
            "empty owner-key component",
        )
    return f"{role}|{scope}|{lineage}", None


def _owner_state(context: Context) -> tuple[dict[PurePosixPath, str], list[Diagnostic]]:
    keys: dict[PurePosixPath, str] = {}
    diagnostics: list[Diagnostic] = []
    grouped: dict[str, list[PurePosixPath]] = collections.defaultdict(list)
    for path in context.paths:
        key, diagnostic = _owner_key(context, path)
        keys[path] = key
        if diagnostic:
            diagnostics.append(diagnostic)
        elif key:
            grouped[key].append(path)
    for key, paths in sorted(grouped.items()):
        if len(paths) > 1:
            ordered = sorted(path.as_posix() for path in paths)
            diagnostics.append(
                _diag(
                    "OWNER-DUPLICATE",
                    min(paths, key=lambda p: p.as_posix()),
                    context.profiles[paths[0]].profile_id,
                    "one current owner",
                    json.dumps(ordered, ensure_ascii=False),
                )
            )
    return keys, diagnostics


def _owner_diagnostics(context: Context) -> list[Diagnostic]:
    return _owner_state(context)[1]


def _governance_mirror_rows(
    context: Context,
) -> list[tuple[PurePosixPath, str]] | None:
    readme = context.texts.get(GOVERNANCE_CURRENT_README)
    if readme is None:
        return None
    visible = _visible_markdown(readme).splitlines()
    headings = [
        index
        for index, line in enumerate(visible)
        if line == GOVERNANCE_CURRENT_HEADING
    ]
    if len(headings) != 1:
        return None
    parent_h2 = next(
        (line for line in reversed(visible[: headings[0]]) if re.match(r"^##\s", line)),
        "",
    )
    if parent_h2 != "## Document Index":
        return None
    cursor = headings[0] + 1
    while cursor < len(visible) and not visible[cursor].strip():
        cursor += 1
    if cursor >= len(visible) or visible[cursor] != "| Document | Lifecycle |":
        return None
    cursor += 1
    if cursor >= len(visible) or visible[cursor] != "| --- | --- |":
        return None
    cursor += 1
    rows: list[tuple[PurePosixPath, str]] = []
    while cursor < len(visible):
        line = visible[cursor]
        if re.match(r"^#{1,3}\s", line):
            break
        if not line.strip():
            cursor += 1
            continue
        match = re.fullmatch(
            r"\| \[`([^`]+)`\]\(([^\s?#)]+)\) \| `([^`]+)` \|",
            line,
        )
        if match is None:
            return None
        kind, target = _local_destination(GOVERNANCE_CURRENT_README, match.group(2))
        if kind != "local" or target is None or match.group(1) != target.name:
            return None
        rows.append((target, match.group(3).casefold()))
        cursor += 1
    return rows


def _governance_current_owner_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not context.governance_current_paths:
        return diagnostics
    declared = set(context.governance_current_paths)
    allowed = set(context.governance_current_states)
    for path in context.governance_current_paths:
        if path not in context.paths:
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_MISSING",
                    path,
                    "governance/reference",
                    "declared tracked governance/reference document",
                    "declared path is missing",
                )
            )
            continue
        profile = context.profiles[path]
        if profile.profile_id != "governance/reference" or profile.mode != "authored":
            diagnostics.append(
                _diag(
                    "REGISTRY_GOVERNANCE_CURRENT_OWNER_PROFILE",
                    path,
                    profile.profile_id,
                    "authored governance/reference",
                    f"{profile.mode} {profile.profile_id}",
                )
            )
            continue
        status = str(context.metadata[path].get("status", "")).casefold()
        if status not in allowed:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-STATUS",
                    path,
                    profile.profile_id,
                    "active or accepted",
                    status or "missing",
                )
            )

    for path in context.paths:
        profile = context.profiles[path]
        if profile.profile_id != "governance/reference" or profile.mode != "authored":
            continue
        status = str(context.metadata[path].get("status", "")).casefold()
        if status in allowed and path not in declared:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-UNDECLARED",
                    path,
                    profile.profile_id,
                    "active or accepted Stage 00 authority declared in the registry",
                    "current authority is undeclared",
                )
            )
        elif status in {"done", "archived"} and path not in declared:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-OWNER-ROUTE",
                    path,
                    profile.profile_id,
                    "draft candidate or declared active/accepted current authority",
                    f"undeclared {status} document in the current Stage 00 route",
                )
            )

    mirror_rows = _governance_mirror_rows(context)
    if mirror_rows is None:
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-MISSING",
                GOVERNANCE_CURRENT_README,
                context.profiles.get(
                    GOVERNANCE_CURRENT_README,
                    ProfileView("readme/stage-index", "readme", "frontmatter-free"),
                ).profile_id,
                "one exact Current Governance Authority Index table",
                "heading or table is missing or malformed",
            )
        )
        return diagnostics

    declared_order = list(context.governance_current_paths)
    declared_set = set(declared_order)
    row_paths = [path for path, _ in mirror_rows]
    row_counter = collections.Counter(row_paths)
    for path in declared_order:
        if row_counter[path] == 0:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-MISSING",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"one row for {path.as_posix()}",
                    "declared owner row is missing",
                )
            )
    for path in sorted(set(row_paths) - declared_set, key=lambda item: item.as_posix()):
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-STALE",
                GOVERNANCE_CURRENT_README,
                "readme/stage-index",
                "registry-declared current authority row",
                f"stale row for {path.as_posix()}",
            )
        )
    for path, count in sorted(row_counter.items(), key=lambda item: item[0].as_posix()):
        if count > 1:
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-DUPLICATE",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"one row for {path.as_posix()}",
                    f"{count} rows",
                )
            )
    for path, status in mirror_rows:
        expected_status = str(
            context.metadata.get(path, {}).get("status", "")
        ).casefold()
        if (
            path in declared_set
            and expected_status in allowed
            and (status not in allowed or status != expected_status)
        ):
            diagnostics.append(
                _diag(
                    "GOVERNANCE-INDEX-STATUS",
                    GOVERNANCE_CURRENT_README,
                    "readme/stage-index",
                    f"{path.as_posix()} lifecycle matches active/accepted frontmatter",
                    status or "missing",
                )
            )
    if (
        len(row_paths) == len(declared_order)
        and collections.Counter(row_paths) == collections.Counter(declared_order)
        and row_paths != declared_order
    ):
        diagnostics.append(
            _diag(
                "GOVERNANCE-INDEX-ORDER",
                GOVERNANCE_CURRENT_README,
                "readme/stage-index",
                "rows in registry declaration order",
                "row order differs",
            )
        )
    return diagnostics


def _reference_collection_rows(
    context: Context, collection: str
) -> list[PurePosixPath] | None:
    declaration = next(
        pack
        for pack in context.reference_current_packs.packs
        if pack.id.startswith(collection + "/")
    )
    heading = (
        "### Research Pack Index"
        if collection == "research"
        else "### Audit Pack Registry"
    )
    expected_parent = "## Item Index"
    text = context.texts.get(declaration.collection_readme)
    if text is None:
        return None
    visible = _visible_markdown(text).splitlines()
    matches = [index for index, line in enumerate(visible) if line == heading]
    if len(matches) != 1:
        return None
    parent = next(
        (line for line in reversed(visible[: matches[0]]) if re.match(r"^##\s", line)),
        "",
    )
    if parent != expected_parent:
        return None
    section = _exact_heading_section(text, heading)
    table = _first_visible_table(section or "")
    if table is None:
        return None
    header, rows = table
    role_indexes = [
        index
        for index, cell in enumerate(header)
        if cell.casefold() in {"status", "pack role"}
    ]
    if len(role_indexes) != 1:
        return None
    current: list[PurePosixPath] = []
    for row in rows:
        if row[role_indexes[0]].casefold() != "current pack":
            continue
        target = _first_cell_target(declaration.collection_readme, row[0])
        if target is None:
            return None
        current.append(target)
    return current


def _reference_pack_rows(
    context: Context, pack_readme: PurePosixPath
) -> list[tuple[PurePosixPath, str]] | None:
    text = context.texts.get(pack_readme)
    if text is None:
        return None
    section = _exact_heading_section(text, "## Report Index")
    table = _first_visible_table(section or "")
    if table is None:
        return None
    header, rows = table
    lifecycle_indexes = [
        index for index, cell in enumerate(header) if cell.casefold() == "lifecycle"
    ]
    if len(lifecycle_indexes) != 1:
        return None
    lifecycle_index = lifecycle_indexes[0]
    parsed: list[tuple[PurePosixPath, str]] = []
    for row in rows:
        target = _first_cell_target(pack_readme, row[0])
        if target is None:
            return None
        if (
            target.parent != pack_readme.parent
            or target == pack_readme
            or target.suffix != ".md"
        ):
            continue
        match = re.fullmatch(r"`([a-z][a-z0-9-]*)`", row[lifecycle_index])
        if match is None:
            parsed.append((target, ""))
        else:
            parsed.append((target, match.group(1)))
    return parsed


def _reference_current_pack_diagnostics(context: Context) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not context.reference_current_packs.packs:
        return diagnostics
    for pack in context.reference_current_packs.packs:
        collection = pack.id.split("/", 1)[0]
        collection_profile = context.profiles[pack.collection_readme].profile_id
        current_rows = _reference_collection_rows(context, collection)
        if current_rows is None:
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-COLLECTION-MISSING",
                    pack.collection_readme,
                    collection_profile,
                    f"one Current pack row for {pack.pack_readme.as_posix()}",
                    "heading or table is missing or malformed",
                )
            )
        else:
            counter = collections.Counter(current_rows)
            if counter[pack.pack_readme] == 0:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-COLLECTION-MISSING",
                        pack.collection_readme,
                        collection_profile,
                        f"one Current pack row for {pack.pack_readme.as_posix()}",
                        "declared Current row is missing",
                    )
                )
            for target in sorted(
                set(current_rows) - {pack.pack_readme}, key=lambda item: item.as_posix()
            ):
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-COLLECTION-STALE",
                        pack.collection_readme,
                        collection_profile,
                        f"Current pack target={pack.pack_readme.as_posix()}",
                        f"Current pack target={target.as_posix()}",
                    )
                )
            for target, count in sorted(
                counter.items(), key=lambda item: item[0].as_posix()
            ):
                if count > 1 or len(current_rows) > 1:
                    diagnostics.append(
                        _diag(
                            "REFERENCE-PACK-COLLECTION-DUPLICATE",
                            pack.collection_readme,
                            collection_profile,
                            "one visible Current pack row",
                            f"target={target.as_posix()}; total={len(current_rows)}; count={count}",
                        )
                    )

        declared_order = list(pack.member_paths)
        declared = set(declared_order)
        tracked = {
            path
            for path in context.paths
            if path.parent == pack.pack_readme.parent
            and path != pack.pack_readme
            and path.suffix == ".md"
            and context.profiles[path].profile_id
            == context.reference_current_packs.profile_id
            and context.profiles[path].mode == "authored"
        }
        for path in sorted(tracked - declared, key=lambda item: item.as_posix()):
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-OWNER-UNDECLARED",
                    path,
                    context.profiles[path].profile_id,
                    f"member declared in Current pack {pack.id}",
                    "tracked direct member is undeclared",
                )
            )
        for path in declared_order:
            profile = context.profiles.get(path)
            if (
                profile is None
                or profile.profile_id != context.reference_current_packs.profile_id
                or profile.mode not in {"authored", "classification-only"}
            ):
                diagnostics.append(
                    _diag(
                        "REGISTRY_REFERENCE_CURRENT_PACK_PROFILE",
                        path,
                        profile.profile_id
                        if profile
                        else context.reference_current_packs.profile_id,
                        f"authorized {context.reference_current_packs.profile_id}",
                        "declared member is missing or has the wrong profile",
                    )
                )
                continue
            status = str(context.metadata[path].get("status", "")).casefold()
            if status not in pack.allowed_states:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-OWNER-STATUS",
                        path,
                        profile.profile_id,
                        f"status in {list(pack.allowed_states)!r}",
                        status or "missing",
                    )
                )

        rows = _reference_pack_rows(context, pack.pack_readme)
        pack_profile = context.profiles[pack.pack_readme].profile_id
        if rows is None:
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-MISSING",
                    pack.pack_readme,
                    pack_profile,
                    "one exact Report Index with one Lifecycle column",
                    "heading or table is missing or malformed",
                )
            )
            continue
        row_paths = [path for path, _ in rows]
        row_counter = collections.Counter(row_paths)
        for path in declared_order:
            if row_counter[path] == 0:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-MISSING",
                        pack.pack_readme,
                        pack_profile,
                        f"one row for {path.as_posix()}",
                        "declared member row is missing",
                    )
                )
        for path in sorted(set(row_paths) - declared, key=lambda item: item.as_posix()):
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-STALE",
                    pack.pack_readme,
                    pack_profile,
                    "registry-declared direct sibling",
                    f"stale row for {path.as_posix()}",
                )
            )
        for path, count in sorted(
            row_counter.items(), key=lambda item: item[0].as_posix()
        ):
            if count > 1:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-DUPLICATE",
                        pack.pack_readme,
                        pack_profile,
                        f"one row for {path.as_posix()}",
                        f"{count} rows",
                    )
                )
        for path, lifecycle in rows:
            if path not in declared:
                continue
            expected_status = str(
                context.metadata.get(path, {}).get("status", "")
            ).casefold()
            if lifecycle != expected_status:
                diagnostics.append(
                    _diag(
                        "REFERENCE-PACK-INDEX-STATUS",
                        pack.pack_readme,
                        pack_profile,
                        f"{path.as_posix()} lifecycle={expected_status}",
                        f"lifecycle={lifecycle or 'malformed'}",
                    )
                )
        if (
            len(row_paths) == len(declared_order)
            and collections.Counter(row_paths) == collections.Counter(declared_order)
            and row_paths != declared_order
        ):
            diagnostics.append(
                _diag(
                    "REFERENCE-PACK-INDEX-ORDER",
                    pack.pack_readme,
                    pack_profile,
                    "member rows in registry order",
                    "member row order differs",
                )
            )
    return diagnostics


def _ledger_rows(text: str) -> tuple[tuple[str, ...] | None, list[list[str]]]:
    lines = _visible_markdown(text).splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        columns = tuple(cell.strip().casefold() for cell in line.strip("|").split("|"))
        if "path" not in columns:
            continue
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.startswith("|"):
                break
            rows.append([cell.strip() for cell in row_line.strip("|").split("|")])
        return columns, rows
    return None, []


def _werpc_predecessor_disposition_map(
    text: str,
) -> dict[PurePosixPath, PurePosixPath] | None:
    """Return exact predecessor-to-current owners for a complete deletion ledger."""

    lines = _visible_markdown(text).splitlines()
    rows: list[list[str]] | None = None
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        columns = tuple(cell.strip().casefold() for cell in line.strip("|").split("|"))
        if columns != WERPC_DISPOSITION_COLUMNS:
            continue
        rows = []
        for row_line in lines[index + 2 :]:
            if not row_line.startswith("|"):
                break
            rows.append([cell.strip() for cell in row_line.strip("|").split("|")])
        break
    if rows is None:
        return None
    dispositions: dict[PurePosixPath, PurePosixPath] = {}
    for row in rows:
        if len(row) != 7:
            return None
        (
            raw_path,
            source_commit,
            _topic,
            verification,
            new_owner,
            disposition,
            reason,
        ) = row
        if (
            not raw_path.startswith("`")
            or not raw_path.endswith("`")
            or not source_commit.startswith("`")
            or not source_commit.endswith("`")
            or re.fullmatch(r"[0-9a-f]{40}", source_commit[1:-1]) is None
            or not verification
            or not new_owner.startswith("`")
            or not new_owner.endswith("`")
            or not new_owner[1:-1]
            or disposition != WERPC_DELETION_DISPOSITION
            or not reason
        ):
            return None
        old_path = PurePosixPath(raw_path[1:-1])
        owner_name = new_owner[1:-1]
        owner_path = (
            PurePosixPath("docs/90.references/research/2026-08-08-wer") / owner_name
        )
        if (
            old_path in dispositions
            or owner_name != PurePosixPath(owner_name).name
            or owner_path.suffix != ".md"
        ):
            return None
        dispositions[old_path] = owner_path
    if frozenset(path.as_posix() for path in dispositions) != WERPC_PREDECESSOR_PATHS:
        return None
    return dispositions


def _werpc_predecessor_dispositions(text: str) -> frozenset[str] | None:
    """Return the exact predecessor set only for a complete deletion ledger."""

    dispositions = _werpc_predecessor_disposition_map(text)
    if dispositions is None:
        return None
    return frozenset(path.as_posix() for path in dispositions)


def _migrated_directory_link(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> bool:
    """Admit a removed directory whose every held file moved to a proved owner.

    The migration ledger is file-scoped: every row carries a source blob, so a
    directory can never own a row of its own. A historical document may still
    link the directory it observed. Such a link is proved, not waived, when the
    directory is gone, its files are dispositioned from one sealed commit, and
    each of those files resolves to a different current tracked owner.
    """

    posix = target.as_posix()
    prefix = posix + "/"
    proof = _context_migration_proof(context)
    commits = {
        disposition.source_commit
        for path, disposition in proof.dispositions.items()
        if path.startswith(prefix)
    }
    if len(commits) != 1:
        return False
    (commit,) = commits
    try:
        tree = _run_git(
            context.root, ("ls-tree", "-d", "--name-only", "-z", commit, "--", posix)
        )
        listing = _run_git(
            context.root, ("ls-tree", "-r", "--name-only", "-z", commit, "--", posix)
        )
    except (OSError, ValueError, subprocess.SubprocessError):
        return False
    if not [entry for entry in tree.split(b"\0") if entry]:
        return False
    held = [entry.decode("utf-8") for entry in listing.split(b"\0") if entry]
    if not held:
        return False
    for entry in held:
        owner = proof.targets.get(entry)
        if owner is None or owner == entry:
            return False
        if PurePosixPath(owner) not in context.tracked_regular_paths:
            return False
    return True


def _protected_historical_predecessor_link(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> bool:
    """Prove one missing target is immutable RIA-protected historical evidence."""

    if (
        target.as_posix() not in WERPC_PREDECESSOR_PATHS
        or context.ria_contract_text is None
        or LEDGER_PATH not in context.texts
    ):
        return False
    dispositions = _werpc_predecessor_disposition_map(context.texts[LEDGER_PATH])
    if dispositions is None:
        return False
    new_owner = dispositions.get(target)
    if (
        new_owner is None
        or new_owner not in context.paths
        or new_owner not in context.tracked_regular_paths
    ):
        return False
    try:
        contract = json.loads(context.ria_contract_text)
    except (json.JSONDecodeError, UnicodeError):
        return False
    baselines = contract.get("currentPackBaselines")
    if not isinstance(baselines, dict):
        return False
    for pack in context.reference_current_packs.packs:
        protected_paths = (pack.pack_readme, *pack.member_paths)
        if source not in protected_paths:
            continue
        encoded = baselines.get(pack.id)
        if not isinstance(encoded, str) or GIT_SHA1_PATTERN.fullmatch(encoded) is None:
            return False
        oid = encoded.removeprefix("git-sha1:")
        try:
            registry_bytes = _read_ria_commit_path(
                context.root,
                oid,
                Path(RETIRED_DOCUMENT_PROFILES_PATH.as_posix()),
            )
            source_bytes = _read_ria_commit_path(
                context.root,
                oid,
                Path(source.as_posix()),
            )
            baseline_registry = json.loads(registry_bytes.decode("utf-8", "strict"))
        except (
            RiaContractError,
            RiaGitError,
            UnicodeDecodeError,
            json.JSONDecodeError,
        ):
            return False
        reference_packs = baseline_registry.get("referenceCurrentPacks")
        if not isinstance(reference_packs, dict):
            return False
        if (
            reference_packs.get("profileId")
            != context.reference_current_packs.profile_id
        ):
            return False
        raw_packs = reference_packs.get("packs")
        if not isinstance(raw_packs, list):
            return False
        expected_pack = {
            "id": pack.id,
            "allowedStates": list(pack.allowed_states),
            "members": list(pack.members),
        }
        if expected_pack not in raw_packs:
            return False
        return source_bytes == context.texts[source].encode("utf-8")
    boundary = _terminal_historical_source_boundary(context, source)
    if boundary is None:
        return False
    try:
        source_bytes = _read_ria_commit_path(
            context.root,
            boundary,
            Path(source.as_posix()),
        )
    except (RiaContractError, RiaGitError):
        return False
    return source_bytes == context.texts[source].encode("utf-8")


def _work105_accepted_history_source(
    context: Context,
    source: PurePosixPath,
) -> bool:
    """Return true only for the exact reviewed accepted-ADR history corpus."""

    if (
        source not in WORK105_ACCEPTED_HISTORY_ADR_PATHS
        or context.metadata.get(source, {}).get("status") != "accepted"
        or source not in context.texts
    ):
        return False
    source_bytes = context.texts[source].encode("utf-8")
    projected = _work108_without_history_artifact_id(source, source_bytes)
    if projected is not None:
        source_bytes = projected
    amended_digest = WORK105_AMENDED_ACCEPTED_ADR_SHA256.get(source)
    if amended_digest is not None:
        return hashlib.sha256(source_bytes).hexdigest() == amended_digest
    try:
        pinned = _read_ria_commit_path(
            context.root,
            context.work105_history_base_commit,
            Path(source.as_posix()),
        )
    except (RiaContractError, RiaGitError):
        return False
    return source_bytes == pinned


def _work108_without_history_artifact_id(
    path: PurePosixPath, raw: bytes
) -> bytes | None:
    canonical = path.as_posix()
    decision = re.fullmatch(
        r"docs/02\.architecture/decisions/(?P<id>[0-9]{4})-[a-z0-9]+"
        r"(?:-[a-z0-9]+)*\.md",
        canonical,
    )
    stage03 = re.fullmatch(
        r"docs/03\.specs/(?P<id>[0-9]{3})-[a-z0-9]+(?:-[a-z0-9]+)*/"
        r"(?P<leaf>spec|plan|tasks)\.md",
        canonical,
    )
    if decision is not None:
        expected_id = f"ADR-{decision.group('id')}"
    elif stage03 is not None:
        prefix = {"spec": "SPEC", "plan": "PLAN", "tasks": "TASK"}[
            stage03.group("leaf")
        ]
        expected_id = f"{prefix}-{stage03.group('id')}"
    else:
        return None
    expected = f'artifact_id: "{expected_id}"'.encode("ascii")
    lines = raw.splitlines(keepends=True)
    if not lines or lines[0].rstrip(b"\r\n") != b"---":
        return None
    try:
        frontmatter_end = next(
            index
            for index, line in enumerate(lines[1:], 1)
            if line.rstrip(b"\r\n") == b"---"
        )
    except StopIteration:
        return None
    matches = [
        index
        for index, line in enumerate(lines[:frontmatter_end])
        if line.rstrip(b"\r\n") == expected
    ]
    if len(matches) != 1 or matches[0] == 0:
        return None
    index = matches[0]
    if not lines[index - 1].startswith(b"updated:"):
        return None
    return b"".join(lines[:index] + lines[index + 1 :])


def _work105_accepted_history_ard_link(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> bool:
    """Admit reviewed accepted-ADR links to the exact retired ARD corpus."""

    return (
        target in WORK105_COMPLETED_HISTORY_ARD_TARGETS
        and _work105_accepted_history_source(context, source)
    )


def _work105_completed_history_ard_link(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> bool:
    """Admit only exact pinned-base done-document links to the eight retired ARDs."""

    if (
        target not in WORK105_COMPLETED_HISTORY_ARD_TARGETS
        or source not in context.tracked_regular_paths
        or context.metadata.get(source, {}).get("status") != "done"
        or source not in context.texts
    ):
        return False
    try:
        source_bytes = _read_ria_commit_path(
            context.root,
            context.work105_history_base_commit,
            Path(source.as_posix()),
        )
    except (RiaContractError, RiaGitError):
        return False
    current = context.texts[source].encode("utf-8")
    projected = _work108_without_history_artifact_id(source, current)
    return source_bytes == (projected if projected is not None else current)


def _work105_immutable_history_ard_link(
    context: Context,
    source: PurePosixPath,
    target: PurePosixPath,
) -> bool:
    """Preserve exact pinned Stage 90/98 links without rewriting history."""

    if (
        not any(
            source.is_relative_to(root)
            for root in (
                PurePosixPath("docs/90.references"),
                PurePosixPath("docs/98.archive"),
            )
        )
        or target not in WORK105_IMMUTABLE_HISTORY_ARD_TARGETS
        or source not in context.texts
    ):
        return False
    if source == ARCHIVE_INDEX_PATH and _work107_stable_archive_index_source(
        context, source
    ):
        return True
    try:
        source_bytes = _read_ria_commit_path(
            context.root,
            context.work105_history_base_commit,
            Path(source.as_posix()),
        )
    except (RiaContractError, RiaGitError):
        return False
    return source_bytes == context.texts[source].encode("utf-8")


def _ledger_protected_drift() -> Diagnostic:
    return _diag(
        "LEDGER-PROTECTED-DRIFT",
        LEDGER_PATH,
        "content/reference",
        "settled RIA identity/provenance metadata and protected ledger bytes",
        "settled metadata or protected bytes differ",
    )


def _project_settled_ledger_bytes(
    context: Context,
    ledger_bytes: bytes,
) -> bytes | None:
    try:
        projections = load_agent_cutover_projections(context.root, None)
    except (RiaContractError, RiaGitError):
        return None
    projection = projections.get(Path(LEDGER_PATH.as_posix()))
    if projection is None:
        return ledger_bytes
    replacements = projection.get("literalReplacements")
    if (
        not isinstance(replacements, list)
        or len(replacements) != 1
        or not isinstance(replacements[0], Mapping)
    ):
        return None
    migration = replacements[0]
    try:
        text = ledger_bytes.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return None
    source = str(migration["from"])
    target = str(migration["to"])
    count = int(migration["count"])
    if text.count(source) != 0 or text.count(target) != count:
        return None
    return text.replace(target, source).encode("utf-8")


def _ledger_protection_state(context: Context) -> tuple[bool, Diagnostic | None]:
    """Return whether the terminal RIA settlement seals the ledger inventory."""

    if context.ria_contract_text is None:
        return False, None
    try:
        contract = json.loads(context.ria_contract_text)
    except (json.JSONDecodeError, UnicodeError):
        return True, _ledger_protected_drift()
    if not isinstance(contract, dict):
        return True, _ledger_protected_drift()
    settlements = contract.get("baselineSettlements")
    if settlements is None or settlements == []:
        return False, None
    if (
        not isinstance(settlements, list)
        or len(settlements) != 1
        or not isinstance(settlements[0], dict)
    ):
        return True, _ledger_protected_drift()
    settlement = settlements[0]
    transition_commit = settlement.get("transitionCommit")
    target_sha256 = settlement.get("targetSha256")
    target_byte_length = settlement.get("targetByteLength")
    reason = settlement.get("reason")
    baselines = contract.get("currentPackBaselines")
    if (
        set(settlement) != LEDGER_SETTLEMENT_KEYS
        or contract.get("baselineTransitions") != []
        or settlement.get("id") != LEDGER_SETTLEMENT_ID
        or settlement.get("packId") != LEDGER_SETTLEMENT_PACK_ID
        or settlement.get("subject") != LEDGER_SETTLEMENT_SUBJECT
        or settlement.get("fromCommit") != LEDGER_SETTLEMENT_FROM_COMMIT
        or not isinstance(transition_commit, str)
        or GIT_SHA1_PATTERN.fullmatch(transition_commit) is None
        or not isinstance(baselines, dict)
        or baselines.get(LEDGER_SETTLEMENT_PACK_ID) != transition_commit
        or not isinstance(target_sha256, str)
        or SHA256_PATTERN.fullmatch(target_sha256) is None
        or not isinstance(target_byte_length, int)
        or isinstance(target_byte_length, bool)
        or not 1 <= target_byte_length <= MAX_LEDGER_BYTES
        or reason != LEDGER_SETTLEMENT_REASON
    ):
        return True, _ledger_protected_drift()
    ledger_bytes = context.ledger_bytes
    if ledger_bytes is None and LEDGER_PATH in context.texts:
        ledger_bytes = context.texts[LEDGER_PATH].encode("utf-8")
    if ledger_bytes is not None:
        ledger_bytes = _project_settled_ledger_bytes(context, ledger_bytes)
    if (
        ledger_bytes is None
        or len(ledger_bytes) != target_byte_length
        or hashlib.sha256(ledger_bytes).hexdigest() != target_sha256
    ):
        return True, _ledger_protected_drift()
    return True, None


def _ledger_diagnostics(context: Context) -> list[Diagnostic]:
    protected, protected_drift = _ledger_protection_state(context)
    if protected_drift is not None:
        return [protected_drift]
    expected_literal = DEBT_LITERAL["expected"]
    if LEDGER_PATH not in context.paths or LEDGER_PATH not in context.texts:
        return [
            _diag(
                "LEDGER-MISSING",
                LEDGER_PATH,
                "content/reference",
                expected_literal,
                DEBT_LITERAL["actual"],
            )
        ]
    if context.route_state == "terminal":
        return []
    columns, rows = _ledger_rows(context.texts[LEDGER_PATH])
    if columns != LEDGER_COLUMNS:
        return [
            _diag(
                "LEDGER-INCOMPLETE",
                LEDGER_PATH,
                "content/reference",
                "exact ordered fourteen columns",
                "ledger columns differ",
            )
        ]
    diagnostics: list[Diagnostic] = []
    ledger_paths: list[str] = []
    for row in rows:
        if len(row) != 14:
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "fourteen cells per row",
                    f"{len(row)} cells",
                )
            )
            continue
        raw_path = row[0]
        if not (raw_path.startswith("`") and raw_path.endswith("`")):
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "backtick repository path",
                    "path cell format",
                )
            )
            continue
        ledger_paths.append(raw_path[1:-1])
        required_indexes = [index for index in range(14) if index != 3]
        if any(not row[index] for index in required_indexes):
            diagnostics.append(
                _diag(
                    "LEDGER-INCOMPLETE",
                    LEDGER_PATH,
                    "content/reference",
                    "complete ledger row",
                    "empty required cell",
                )
            )
    counter = collections.Counter(ledger_paths)
    if not protected:
        # The ledger records one authored-document migration. Its coverage
        # obligation is the baseline corpus that migration moved, not documents
        # authored by later programs. Scoping to the baseline keeps the ledger a
        # record of what happened instead of forcing invented rows for paths
        # that were never migrated.
        inventory_paths = {
            path.as_posix() for path in context.paths if path in context.baseline_paths
        }
        for missing in sorted(inventory_paths - set(counter)):
            diagnostics.append(
                _diag(
                    "LEDGER-MISSING",
                    LEDGER_PATH,
                    "content/reference",
                    "one row per inventory path",
                    "inventory row is missing",
                )
            )
        archived_original_paths: set[str] = set()
        try:
            raw_registry = json.loads(
                read_repository_text(context.root, ROUTE_CONTRACT_PATH)
            )
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError):
            raw_registry = {}
        raw_namespaces = (
            raw_registry.get("archiveNamespaces", ())
            if isinstance(raw_registry, dict)
            else ()
        )
        if isinstance(raw_namespaces, list):
            for namespace in raw_namespaces:
                raw_records = (
                    namespace.get("records", ()) if isinstance(namespace, dict) else ()
                )
                if not isinstance(raw_records, list):
                    continue
                for raw_target in raw_records:
                    if not isinstance(raw_target, str):
                        continue
                    target = PurePosixPath(raw_target)
                    if (
                        target.as_posix() != raw_target
                        or len(target.parts) <= 2
                        or target.parts[:2] != ("docs", "98.archive")
                        or target.name == "README.md"
                        or not _path_exists_without_dereference(
                            context.root, target, context.adapter_targets
                        )
                    ):
                        continue
                    try:
                        target_mode = (context.root / target).lstat().st_mode
                    except OSError:
                        continue
                    if stat.S_ISREG(target_mode):
                        archived_original_paths.add(
                            PurePosixPath("docs", *target.parts[2:]).as_posix()
                        )
        known_paths = (
            inventory_paths
            | {path.as_posix() for path in context.paths}
            | archived_original_paths
        )
        wp004b_targets = (
            _work054_wp004b_targets(context)
            if context.route_state == "transition"
            else {}
        )
        work105_targets = {
            source: wp004b_targets.get(target, target)
            for source, target in WORK105_LEDGER_PATH_ALIASES.items()
        }
        if all(
            target in context.tracked_regular_paths
            and _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            )
            for target in work105_targets.values()
        ):
            known_paths |= {source.as_posix() for source in work105_targets}
        if not any(
            profile.profile_id == "sdlc/api-spec"
            for profile in context.profiles.values()
        ) and all(path not in context.paths for path in WORK105_LEDGER_RETIRED_PATHS):
            known_paths |= {path.as_posix() for path in WORK105_LEDGER_RETIRED_PATHS}
        if context.route_state == "transition":
            _, move_targets, _ = _document_taxonomy_transition_manifest(context)
            if all(
                target in context.tracked_regular_paths
                and _path_exists_without_dereference(
                    context.root, target, context.adapter_targets
                )
                for target in move_targets.values()
            ):
                known_paths |= {source.as_posix() for source in move_targets}
            work109_moves, work109_replacements, work109_merges = (
                _work109_migration_projection(context)
            )
            work109_ledger_redirects = {
                **work109_moves,
                **work109_replacements,
                **work109_merges,
            }
            if all(
                target in context.tracked_regular_paths
                and _path_exists_without_dereference(
                    context.root, target, context.adapter_targets
                )
                for target in work109_ledger_redirects.values()
            ):
                known_paths |= {
                    source.as_posix() for source in work109_ledger_redirects
                }
            work109_aliases, work109_replacements, work109_merges = (
                _work109_migration_projection(context)
            )
            work109_targets = {
                **work109_aliases,
                **work109_replacements,
                **work109_merges,
            }
            work109_targets.update(_work054_wp003_owner_merges(context))
            if all(
                target in context.tracked_regular_paths
                and _path_exists_without_dereference(
                    context.root, target, context.adapter_targets
                )
                for target in work109_targets.values()
            ):
                known_paths |= {source.as_posix() for source in work109_targets}
            if all(
                target in context.tracked_regular_paths
                and _path_exists_without_dereference(
                    context.root, target, context.adapter_targets
                )
                for target in wp004b_targets.values()
            ):
                known_paths |= {source.as_posix() for source in wp004b_targets}
        stable_archive_aliases = _work107_stable_archive_aliases(context)
        if stable_archive_aliases and all(
            target in context.tracked_regular_paths
            and _path_exists_without_dereference(
                context.root, target, context.adapter_targets
            )
            for target in stable_archive_aliases.values()
        ):
            known_paths |= {source.as_posix() for source in stable_archive_aliases}
            known_paths |= {
                PurePosixPath("docs", *source.parts[2:]).as_posix()
                for source in stable_archive_aliases
                if source.parts[:2] == ("docs", "98.archive")
            }
        unknown_paths = set(counter) - known_paths
        predecessor_unknown = unknown_paths & WERPC_PREDECESSOR_PATHS
        if predecessor_unknown:
            dispositions = _werpc_predecessor_dispositions(context.texts[LEDGER_PATH])
            if dispositions is None or not predecessor_unknown <= dispositions:
                diagnostics.append(
                    _diag(
                        "LEDGER-PREDECESSOR-DISPOSITION",
                        LEDGER_PATH,
                        "content/reference",
                        "complete exact predecessor source, owner, and deletion dispositions",
                        "historical predecessor disposition is missing or malformed",
                    )
                )
            unknown_paths -= predecessor_unknown
        for unknown in sorted(unknown_paths):
            diagnostics.append(
                _diag(
                    "LEDGER-UNKNOWN-PATH",
                    LEDGER_PATH,
                    "content/reference",
                    "tracked inventory path",
                    "unknown ledger path",
                )
            )
    if any(count > 1 for count in counter.values()):
        diagnostics.append(
            _diag(
                "LEDGER-INCOMPLETE",
                LEDGER_PATH,
                "content/reference",
                "unique path rows",
                "duplicate ledger path",
            )
        )
    return diagnostics


def _load_debt(
    root: Path,
    raw: Any | None = None,
    *,
    mode: str = "strict",
) -> dict[str, Any]:
    """Require the canonical retired semantic-debt source state."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    if raw is not None or (root / DEBT_PATH).exists():
        raise ConfigurationError(
            "DEBT-SOURCE-REINTRODUCED: semantic compatibility debt must remain absent"
        )
    if mode == "compatibility":
        raise ConfigurationError(
            "DEBT-SOURCE-MISSING: semantic compatibility debt is retired"
        )
    return {
        "schemaVersion": 1,
        "owner": "Spec 030",
        "growthAllowed": False,
        "items": [],
    }


def _apply_debt(
    root: Path,
    diagnostics: Iterable[Diagnostic],
    mode: str,
    contract: Any | None = None,
) -> list[tuple[str, Diagnostic]]:
    _load_debt(root, contract, mode=mode)
    return [
        ("FAIL", diagnostic)
        for diagnostic in sorted(diagnostics, key=diagnostic_sort_key)
    ]


def _raw_diagnostics(
    context: Context,
    registry: Registry,
    profiles_by_id: dict[str, DocumentProfile],
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    diagnostics = _link_diagnostics(context)
    diagnostics.extend(
        _body_contract_link_diagnostics(
            context,
            profiles_by_id,
            body_contracts,
            body_contract_path_prefixes,
        )
    )
    diagnostics.extend(_index_diagnostics(context))
    diagnostics.extend(_collection_index_diagnostics(context))
    diagnostics.extend(_governance_current_owner_diagnostics(context))
    diagnostics.extend(_reference_current_pack_diagnostics(context))
    diagnostics.extend(_owner_diagnostics(context))
    diagnostics.extend(_ledger_diagnostics(context))
    diagnostics.extend(
        _program_lineage_diagnostics(
            context,
            registry.program_lineage,
            registry.standalone_executions,
        )
    )
    return sorted(diagnostics, key=diagnostic_sort_key)


def validate_cross_document_contracts(
    root: Path,
    mode: str,
    body_contracts: str = "registry",
    body_contract_path_prefixes: tuple[PurePosixPath, ...] = (),
    include_paths: tuple[PurePosixPath, ...] = (),
) -> list[Diagnostic]:
    """Return deterministic raw cross-document diagnostics."""

    if mode not in {"compatibility", "strict"}:
        raise ConfigurationError("mode must be compatibility or strict")
    context = _build_context(root, include_paths=include_paths)
    _load_debt(context.root, mode=mode)
    registry = load_registry(context.root)
    profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
    return _raw_diagnostics(
        context,
        registry,
        profiles_by_id,
        body_contracts,
        body_contract_path_prefixes,
    )


def _inventory_documents(context: Context) -> list[dict[str, Any]]:
    owner_keys, _ = _owner_state(context)
    documents: list[dict[str, Any]] = []
    for path in context.paths:
        profile = context.profiles[path]
        metadata = context.metadata[path]
        documents.append(
            {
                "path": path.as_posix(),
                "profile": profile.profile_id,
                "profileClass": profile.profile_class,
                "mode": profile.mode,
                "title": str(metadata.get("title", "")),
                "status": str(metadata.get("status", "")),
                "ownerKey": owner_keys[path],
                "origin": "baseline"
                if path in context.baseline_paths
                else "program-created",
            }
        )
    return documents


def _diagnostic_json(outcome: str, diagnostic: Diagnostic) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "ruleId": diagnostic.rule_id,
        "path": diagnostic.path.as_posix(),
        "profile": diagnostic.profile,
        "expected": diagnostic.expected,
        "actual": diagnostic.actual,
        "owner": diagnostic.owner,
        "debtToken": "",
    }


def _envelope(
    mode: str,
    counts: dict[str, int],
    documents: list[dict[str, Any]],
    rows: list[tuple[str, Diagnostic]],
) -> dict[str, Any]:
    outcome = (
        "FAIL"
        if any(value == "FAIL" for value, _ in rows)
        else ("DEFER" if rows else "PASS")
    )
    return {
        "schemaVersion": 1,
        "mode": mode,
        "outcome": outcome,
        "counts": counts,
        "documents": documents,
        "diagnostics": [
            _diagnostic_json(value, diagnostic) for value, diagnostic in rows
        ],
    }


def _text_rows(rows: list[tuple[str, Diagnostic]]) -> list[str]:
    if not rows:
        return [
            'PASS CROSS-DOCUMENT . cross-document expected="valid" actual="valid" owner="cross-document-validator"'
        ]
    return [
        f"{outcome} {item.rule_id} {item.path.as_posix()} {item.profile} "
        f"expected={json.dumps(item.expected, ensure_ascii=False)} "
        f"actual={json.dumps(item.actual, ensure_ascii=False)} "
        f"owner={json.dumps(item.owner)}"
        for outcome, item in rows
    ]


def _body_contract_path_prefix(value: str) -> PurePosixPath:
    """Parse one normalized repository-relative body-contract scope."""

    path = PurePosixPath(value)
    if (
        not value
        or value == "."
        or value != path.as_posix()
        or value.startswith("./")
        or path.is_absolute()
        or re.match(r"^[A-Za-z]:[/\\]", value) is not None
        or ".." in path.parts
        or "\\" in value
    ):
        raise argparse.ArgumentTypeError(
            "body-contract path prefix must be normalized and repository-relative"
        )
    return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("strict",), default="strict")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument(
        "--body-contracts",
        choices=("registry", "audit"),
        default="registry",
        help="respect registry status scopes or audit all draft/active body contracts",
    )
    parser.add_argument(
        "--body-contract-path-prefix",
        action="append",
        default=[],
        type=_body_contract_path_prefix,
        help=(
            "limit forced audit enforcement to a repeatable normalized "
            "repository-relative prefix"
        ),
    )
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--include-path", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.inventory and args.format != "json":
            raise ConfigurationError("--inventory requires --format json")
        include_paths = tuple(PurePosixPath(value) for value in args.include_path)
        context = _build_context(args.root, include_paths)
        registry = load_registry(context.root)
        profiles_by_id = {profile.profile_id: profile for profile in registry.profiles}
        inventory = enumerate_target_markdown(context.root, include_paths=include_paths)
        counts = {
            "baseline": len(inventory.baseline_paths),
            "current": len(inventory.current_paths),
            "new": len(inventory.new_paths),
            "documents": len(inventory.current_paths),
        }
        if args.inventory:
            diagnostics = (
                _link_diagnostics(context)
                + _body_contract_link_diagnostics(
                    context,
                    profiles_by_id,
                    args.body_contracts,
                    tuple(args.body_contract_path_prefix),
                )
                + _index_diagnostics(context)
                + _collection_index_diagnostics(context)
                + _governance_current_owner_diagnostics(context)
                + _reference_current_pack_diagnostics(context)
                + _owner_diagnostics(context)
            )
            rows = [
                ("FAIL", item) for item in sorted(diagnostics, key=diagnostic_sort_key)
            ]
            envelope = _envelope(
                "inventory", counts, _inventory_documents(context), rows
            )
            print(json.dumps(envelope, ensure_ascii=False, separators=(",", ":")))
            return int(bool(rows))
        diagnostics = _raw_diagnostics(
            context,
            registry,
            profiles_by_id,
            args.body_contracts,
            tuple(args.body_contract_path_prefix),
        )
        rows = _apply_debt(context.root, diagnostics, args.mode)
        if args.format == "json":
            print(
                json.dumps(
                    _envelope(args.mode, counts, [], rows),
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        else:
            print("\n".join(_text_rows(rows)))
        return int(any(outcome == "FAIL" for outcome, _ in rows))
    except (
        ConfigurationError,
        DocumentContractError,
        OSError,
        ValueError,
        yaml.YAMLError,
    ) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
