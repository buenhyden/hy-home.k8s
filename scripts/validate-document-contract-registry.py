#!/usr/bin/env python3
"""Validate the document-profile registry and its deterministic routing."""

from __future__ import annotations

import argparse
import bisect
import copy
import hashlib
import importlib.util
import json
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

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
PROGRAM_LINEAGE_PROJECTION_FIXTURE_FIELD = "productionProgramLineageProjection"
WORK105_CONSUMER_DISPOSITION_FIXTURE_FIELD = "work105ConsumerDisposition"
WORK106_ARTIFACT_FIXTURE_FIELD = "work106ArtifactIdentityCases"
WORK106_LEDGER_FIXTURE_FIELD = "work106MigrationLedger"
WORK105_CONSUMER_BASE_COMMIT = "a6fa1806364ea0472baaad0906e1b5e4ddac8602"
WORK105_CONSUMER_PATTERNS = (
    {
        "id": "ard",
        "regex": (
            r"sdlc/ard|template/sdlc/ard|ard\.template\.md|"
            r"02\.architecture/requirements|Architecture Reference Document|"
            r"(^|[^A-Za-z0-9_])ARD([^A-Za-z0-9_]|$)|ard_id|\"ard\""
        ),
        "scope": "tracked-text-lines",
    },
    {
        "id": "authored-api-spec",
        "regex": (
            r"sdlc/api-spec|template/sdlc/api-spec|api-spec\.template\.md|"
            r"(^|/)api-spec\.md|OpenAPI Specification|"
            r"openapi\.template\.yaml|schema\.template\.graphql|"
            r"service\.template\.proto|native-surface-cases\.json"
        ),
        "scope": "tracked-text-lines",
    },
)
WORK105_CONSUMER_RECORD_KEYS = {
    "patternId",
    "path",
    "line",
    "matchedLineSha256",
    "occurrenceCount",
    "consumerClass",
    "disposition",
    "target",
    "reason",
}

WORK106_LEDGER_FIELDS = frozenset(
    {
        "schema_version",
        "migration_id",
        "legacy_path",
        "stable_path",
        "artifact_id",
        "action",
        "replacement",
        "source_commit",
        "legacy_archive_commit",
        "legacy_envelope_blob",
        "source_blob",
        "content_sha256",
        "record_kind",
        "reason",
    }
)
WORK106_OBJECT_ID = re.compile(r"^[0-9a-f]{40}$")
WORK106_CONTENT_DIGEST = re.compile(r"^[0-9a-f]{64}$")
WORK106_MIGRATION_ID = re.compile(r"^MIG-[0-9]{4}$")
WORK106_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
WORK106_TOMBSTONE_TYPES = {
    "01.requirements": frozenset({"PRD", "SRS", "IFC"}),
    "02.architecture": frozenset({"AD", "ADR"}),
    "03.specs": frozenset(
        {"SPEC", "AGENT-DESIGN", "DATA-MODEL", "TESTS", "PLAN", "TASK"}
    ),
    "05.operations": frozenset(
        {"GUIDE", "POLICY", "RUNBOOK", "INCIDENT", "POSTMORTEM"}
    ),
}
WORK108_MANDATORY_PROFILE_IDS = frozenset(
    {
        "sdlc/prd",
        "sdlc/srs",
        "sdlc/interface",
        "sdlc/ad",
        "sdlc/adr",
        "sdlc/spec",
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
        "content/archive",
        "content/archive-migration",
    }
)


@dataclass(frozen=True)
class Work106ArtifactIdentity:
    artifact_id: str
    change_id: str | None = None
    migration_id: str | None = None
    record_kind: str | None = None
WORK105_STAGED_INVENTORY_BYTES = 4 * 1024 * 1024
WORK105_STAGED_ENTRY_LIMIT = 20_000
WORK105_STAGED_PATH_BYTES = 4096
WORK105_STAGED_BLOB_BYTES = 8 * 1024 * 1024
WORK105_STAGED_AGGREGATE_BYTES = 64 * 1024 * 1024
WORK105_STAGED_OBJECT_LIMIT = 20_000
WORK105_GIT_HEADER_BYTES = 256
WORK105_OBJECT_ID = re.compile(rb"[0-9a-f]{40}|[0-9a-f]{64}")
WORK105_SEMANTIC_BOUNDARY = re.compile(
    r'(?<!\\)"|[,;:|<>{}\[\]\t]|[.!?](?=\s)'
)
WORK105_WIKI_GENERATOR_PATH = "scripts/generate-llm-wiki-index.sh"
WORK105_WIKI_GENERATOR_BASE_ROW = (
    "| Architecture requirements | [Architecture Requirements README]"
    "(../../02.architecture/requirements/README.md) | Owns ARD-style "
    "architecture requirement index | Architecture requirement changes |"
)
WORK105_WIKI_GENERATOR_CURRENT_ROW = (
    "| Architecture descriptions | [Architecture Descriptions README]"
    "(../../02.architecture/descriptions/README.md) | Owns the AD "
    "architecture-description index | Architecture-description changes |"
)
WORK105_WIKI_GENERATOR_BASE_ROW_ASSIGNMENT = (
    f"TRANSITION_BASE_ROW='{WORK105_WIKI_GENERATOR_BASE_ROW}'"
)
WORK105_WIKI_GENERATOR_HEADER_LINES = (
    'TRANSITION_BASE_OUTPUT_OID="5a1482bd94df7f52d3ba22f20e9304c29d61862c"',  # pragma: allowlist secret
    'TRANSITION_CURRENT_OUTPUT_OID="add8ff6c918674aad36e55ebff188f582bb9cd03"',  # pragma: allowlist secret
    'TRANSITION_REGISTRY_OID="ce8da8f205cee1bba075bef7b26079a0708324b1"',  # pragma: allowlist secret
    'TRANSITION_MANIFEST_OID="d82466f99b093dc39092a3f36d1c55452a45a7ed"',  # pragma: allowlist secret
    'TRANSITION_MIGRATION_OID="b304c92c9c9032ebfe3be9156bd3f808ed1f5fb9"',  # pragma: allowlist secret
    WORK105_WIKI_GENERATOR_BASE_ROW_ASSIGNMENT,
    f"TRANSITION_CURRENT_ROW='{WORK105_WIKI_GENERATOR_CURRENT_ROW}'",
)
WORK105_WIKI_GENERATOR_PROJECTION_LINES = (
    '  awk -v base="$TRANSITION_BASE_ROW" -v current="$TRANSITION_CURRENT_ROW" \'',
    "    BEGIN { replacements = 0 }",
    "    $0 == base {",
    "      print current",
    "      replacements++",
    "      next",
    "    }",
    "    { print }",
    "    END { if (replacements != 1) exit 1 }",
    "  ' \"$OUTPUT_PATH\" >\"$projection\" || return 1",
    '  [[ "$(blob_oid "$projection")" == "$TRANSITION_CURRENT_OUTPUT_OID" ]] '
    "|| return 1",
    '  cmp -s "$projection" "$generated"',
)
WORK105_WIKI_GENERATOR_REVIEWED_LITERALS = (
    WORK105_WIKI_GENERATOR_HEADER_LINES + WORK105_WIKI_GENERATOR_PROJECTION_LINES
)
WORK105_COMPLETED_HISTORY_PATHS = frozenset(
    {
        "docs/03.specs/019-template-path-numbering-contract/plan.md",
        "docs/03.specs/019-template-path-numbering-contract/spec.md",
    }
)
WORK105_ACCEPTED_BASE_HISTORY_PATHS = frozenset(
    {
        "docs/02.architecture/decisions/0002-argocd-helm-and-gitops-model.md",
        "docs/02.architecture/decisions/0003-eso-vault-k8s-auth.md",
        "docs/02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md",
        "docs/02.architecture/decisions/0008-istio-install-and-ingress-coexist.md",
        "docs/02.architecture/decisions/0009-kiali-external-observability.md",
        "docs/02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md",
        "docs/02.architecture/decisions/0012-argo-notifications-slack.md",
        "docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md",
        "docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md",
        "docs/02.architecture/decisions/0015-declarative-document-contract-registry.md",
        "docs/02.architecture/decisions/0016-program-to-tranche-document-lineage.md",
        "docs/02.architecture/decisions/0017-program-follow-up-lineage-semantics.md",
        "docs/02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md",
        "docs/02.architecture/decisions/0020-document-lifecycle-program-closure-evidence.md",
        "docs/02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md",
        "docs/02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md",
    }
)
WORK105_PROGRESS_PATH = "docs/00.agent-governance/memory/progress.md"
WORK105_MIGRATION_CONTRACT_PATHS = frozenset(
    {
        WORK105_PROGRESS_PATH,
        "docs/01.requirements/008-workspace-document-taxonomy-consolidation.md",
        "docs/02.architecture/decisions/0024-terminal-artifact-identity-and-archive-layout.md",
        "docs/03.specs/052-document-taxonomy-consolidation/plan.md",
        "docs/03.specs/052-document-taxonomy-consolidation/spec.md",
        "docs/03.specs/052-document-taxonomy-consolidation/tasks.md",
    }
)
WORK105_PINNED_LEGACY_HISTORY_PATHS = frozenset(
    {
        "docs/02.architecture/decisions/0018-full-body-archive-record-and-retention.md",
        "docs/02.architecture/decisions/0023-work-unit-document-taxonomy-and-governance-authority.md",
        "scripts/archive_cutover_manifest.py",
        "scripts/validate-active-corpus-eligibility.py",
        "scripts/validate-active-corpus-migrations.py",
        "scripts/validate-active-corpus-residue-closure.py",
        "tests/test_active_corpus_eligibility.py",
        "tests/test_active_corpus_migrations.py",
        "tests/test_active_corpus_retention.py",
    }
)
PRD_008_IMMUTABLE_PROJECTION = (
    "008",
    "0011",
    (("052", 1, "0024"),),
    (),
)
GEMINI_NATIVE_CURRENT_SURFACE_RULE = "REGISTRY_GEMINI_NATIVE_CURRENT_SURFACE"
GEMINI_NATIVE_CURRENT_SURFACE_ERROR = (
    f"{GEMINI_NATIVE_CURRENT_SURFACE_RULE}: Gemini CLI native surface must be "
    "a closed repository-static current projection"
)
DOCUMENT_REGISTRY_ROOT_ERROR = (
    "REGISTRY_ROOT_BOUNDARY: repository root must be an existing non-symlink directory"
)
GEMINI_SETTINGS_SCHEMA_URL = (
    "https://raw.githubusercontent.com/google-gemini/gemini-cli/main/"
    "schemas/settings.schema.json"
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
    "docs/02.architecture/descriptions/ad-0008-fixture.md": (
        "sdlc/ad",
        "accepted",
        "2026-07-12",
    ),
    "docs/02.architecture/descriptions/ad-0009-fixture.md": (
        "sdlc/ad",
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
    "docs/03.specs/037-fixture/spec.md": ("sdlc/spec", "active", "2026-07-18"),
    "docs/03.specs/038-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
    "docs/03.specs/039-fixture/spec.md": ("sdlc/spec", "active", "2026-07-15"),
    "docs/03.specs/037-fixture/plan.md": (
        "sdlc/plan",
        "active",
        "2026-07-18",
    ),
    "docs/03.specs/037-fixture/tasks.md": (
        "sdlc/task",
        "active",
        "2026-07-18",
    ),
    "docs/03.specs/038-fixture/plan.md": (
        "sdlc/plan",
        "active",
        "2026-07-18",
    ),
    "docs/03.specs/038-fixture/tasks.md": (
        "sdlc/task",
        "active",
        "2026-07-18",
    ),
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
    (
        "standalone-missing-approval-mode",
        "standalone-missing-approval-mode",
        ("REGISTRY_STANDALONE_APPROVAL_MODE",),
    ),
    (
        "standalone-duplicate-spec",
        "standalone-duplicate-spec",
        ("REGISTRY_STANDALONE_DUPLICATE",),
    ),
    (
        "standalone-program-overlap",
        "standalone-program-overlap",
        ("REGISTRY_STANDALONE_OVERLAP",),
    ),
    (
        "standalone-wrong-plan-path",
        "standalone-wrong-plan-path",
        ("REGISTRY_STANDALONE_PATH",),
    ),
    (
        "standalone-missing-plan-owner",
        "standalone-missing-plan-owner",
        ("REGISTRY_STANDALONE_PATH",),
    ),
    (
        "standalone-missing-task-owner",
        "standalone-missing-task-owner",
        ("REGISTRY_STANDALONE_PATH",),
    ),
    (
        "standalone-task-profile-mismatch",
        "standalone-task-profile-mismatch",
        ("REGISTRY_STANDALONE_PATH",),
    ),
    (
        "standalone-missing-decision-owner",
        "standalone-missing-decision-owner",
        ("REGISTRY_STANDALONE_PATH",),
    ),
    (
        "standalone-unsorted-specs",
        "standalone-unsorted-specs",
        ("REGISTRY_STANDALONE_ORDER",),
    ),
    (
        "standalone-duplicate-plan",
        "standalone-duplicate-plan",
        ("REGISTRY_STANDALONE_DUPLICATE",),
    ),
    (
        "standalone-duplicate-task",
        "standalone-duplicate-task",
        ("REGISTRY_STANDALONE_DUPLICATE",),
    ),
    (
        "standalone-state-drift",
        "standalone-state-drift",
        ("REGISTRY_STANDALONE_STATE",),
    ),
    (
        "standalone-decision-not-accepted",
        "standalone-decision-not-accepted",
        ("REGISTRY_STANDALONE_DECISION",),
    ),
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
    parser.add_argument("--mode", choices=("strict",), default="strict")
    parser.add_argument(
        "--route-state", choices=("legacy", "transition", "terminal")
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
        "sdlc/ad",
        "sdlc/adr",
        "sdlc/spec",
        "sdlc/plan",
        "sdlc/task",
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
                    "sdlc/ad",
                    "sdlc/adr",
                    "sdlc/spec",
                    "sdlc/plan",
                    "sdlc/task",
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
                "profileIds": [
                    profile_id
                    for profile_id in authored
                    if profile_id not in {"sdlc/plan", "sdlc/task"}
                ],
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
                "id": "execution-reciprocal-pair",
                "profileIds": ["sdlc/plan", "sdlc/task"],
                "create": {
                    "mode": "paired",
                    "states": ["draft", "active"],
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
                    "sdlc/ad",
                    "sdlc/adr",
                    "sdlc/spec",
                    "sdlc/plan",
                    "sdlc/task",
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
        "routeState": "legacy",
        "archiveContractVersion": 2,
        "archiveNamespaces": [
            {
                "id": "arwb-base",
                "policy": "exact-immutable",
                "records": [
                    f"docs/98.archive/fixture/arwb-{index:02d}.md"
                    for index in range(31)
                ],
            },
            {
                "id": "acer-additive",
                "policy": "exact-immutable",
                "records": [
                    f"docs/98.archive/fixture/acer-{index:02d}.md"
                    for index in range(12)
                ],
            },
            {
                "id": "wdtc-execution",
                "policy": "exact-reviewed-manifest",
                "records": [
                    f"docs/98.archive/fixture/wdtc-{index:02d}.md"
                    for index in range(50)
                ],
            },
            {
                "id": "progress-snapshot",
                "policy": "append-only-unique",
                "records": [],
            },
        ],
        "retiredRouteEvidence": {
            "routeSegment": "04.execution",
            "profiles": [
                {
                    "id": "stage90/immutable-retired-route-evidence",
                    "paths": [],
                    "routes": [],
                },
                {
                    "id": "stage98/immutable-retired-route-evidence",
                    "paths": [],
                    "routes": [],
                },
            ],
        },
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
                "sdlc/ad",
                "^docs/02\\.architecture/descriptions/ad-[0-9]{4}-fixture\\.md$",
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
            _fixture_lineage_profile(
                "sdlc/plan",
                "^docs/03\\.specs/[0-9]{3}-fixture/plan\\.md$",
                ["draft", "active", "done", "archived"],
            ),
            _fixture_lineage_profile(
                "sdlc/task",
                "^docs/03\\.specs/[0-9]{3}-fixture/tasks\\.md$",
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
                    "ad": "0008",
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
                    "ad": "0009",
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
        "standaloneExecutions": [
            {
                "spec": "037",
                "plan": "docs/03.specs/037-fixture/plan.md",
                "task": "docs/03.specs/037-fixture/tasks.md",
                "state": "active",
                "reason": "Direct approval fixture",
                "decision": "0022",
                "approvalMode": "spec-body-record",
            }
        ],
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
                "ad": legacy["ard"],
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
    research = next(
        (item for item in packs if item["id"].startswith("research/")), None
    )
    if research is None:
        # The research collection is retired from the Current-pack registry.
        # Mutation proofs still need a second pack, so rebuild the retired one
        # from its tracked members for the mutated copy only.
        research = {
            "id": "research/2026-08-08-wer",
            "allowedStates": ["active", "accepted"],
            "members": [
                "agent-memory-tiers-and-management.md",
                "agent-model-routing-and-configuration.md",
                "ai-agents-and-agency-agents.md",
                "ci-cd-github-actions-and-qa.md",
                "documentation-architecture-and-diataxis.md",
                "harness-and-loop-engineering.md",
                "kubernetes-infrastructure-and-security.md",
                "llm-wiki-and-knowledge-routing.md",
                "provider-implementation-status.md",
                "source-coverage-and-migration-ledger.md",
                "spec-driven-sdlc-and-document-contracts.md",
                "workspace-governance-and-common-agent-environment.md",
            ],
        }
        packs.append(research)
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
        packs.clear()
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
    original = next(program for program in programs if program["prd"] == "005")
    current = next(program for program in programs if program["prd"] == "006")
    if mutation == "duplicate-program":
        duplicate = copy.deepcopy(current)
        duplicate["prd"] = original["prd"]
        duplicate["ad"] = original["ad"]
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
        current["ad"] = "9999"
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
    standalone = raw_registry.get("standaloneExecutions", [])
    if mutation == "standalone-missing-approval-mode":
        del standalone[0]["approvalMode"]
        return
    if mutation == "standalone-duplicate-spec":
        duplicate = copy.deepcopy(standalone[0])
        duplicate["plan"] = "docs/03.specs/039-fixture/plan.md"
        duplicate["task"] = "docs/03.specs/039-fixture/tasks.md"
        standalone.append(duplicate)
        return
    if mutation == "standalone-program-overlap":
        standalone[0]["spec"] = "034"
        return
    if mutation == "standalone-wrong-plan-path":
        standalone[0]["plan"] = "docs/03.specs/037-fixture/tasks.md"
        return
    if mutation == "standalone-missing-plan-owner":
        standalone[0]["plan"] = "docs/03.specs/099-fixture/plan.md"
        return
    if mutation == "standalone-missing-task-owner":
        standalone[0]["task"] = "docs/03.specs/099-fixture/tasks.md"
        return
    if mutation == "standalone-task-profile-mismatch":
        target = standalone[0]["task"]
        plan_profile = next(
            item for item in raw_registry["profiles"] if item["id"] == "sdlc/plan"
        )
        task_profile = next(
            item for item in raw_registry["profiles"] if item["id"] == "sdlc/task"
        )
        plan_profile["routes"].append({"kind": "exact", "value": target})
        task_profile["routes"] = [
            {
                "kind": "exact",
                "value": "docs/03.specs/038-fixture/tasks.md",
            }
        ]
        return
    if mutation == "standalone-missing-decision-owner":
        standalone[0]["decision"] = "0099"
        return
    if mutation == "standalone-unsorted-specs":
        earlier = copy.deepcopy(standalone[0])
        earlier.update(
            {
                "spec": "038",
                "plan": "docs/03.specs/038-fixture/plan.md",
                "task": "docs/03.specs/038-fixture/tasks.md",
            }
        )
        standalone.insert(0, earlier)
        return
    if mutation == "standalone-duplicate-plan":
        duplicate = copy.deepcopy(standalone[0])
        duplicate["spec"] = "038"
        duplicate["task"] = "docs/03.specs/038-fixture/tasks.md"
        standalone.append(duplicate)
        return
    if mutation == "standalone-duplicate-task":
        duplicate = copy.deepcopy(standalone[0])
        duplicate["spec"] = "038"
        duplicate["plan"] = "docs/03.specs/038-fixture/plan.md"
        standalone.append(duplicate)
        return
    if mutation == "standalone-state-drift":
        standalone[0]["state"] = "done"
        return
    if mutation == "standalone-decision-not-accepted":
        standalone[0]["decision"] = "0018"
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
        predicate["profileEdges"].extend(
            {
                "profileId": profile_id,
                "from": edge["from"],
                "to": edge["to"],
            }
            for profile_id in lifecycle["profileIds"]
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


def _assert_program_lineage_projection(
    registry: Registry,
    fixture_prd_008_projection: tuple[Any, ...],
) -> None:
    immutable_expected = (
        (
            "003",
            "0006",
            (
                ("041", 1, "0013"),
                ("042", 2, "0013"),
                ("043", 3, "0013"),
                ("044", 4, "0013"),
                ("045", 5, "0013"),
                ("046", 6, "0013"),
            ),
            (),
        ),
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
        (
            "007",
            "0010",
            (
                ("047", 1, "0021"),
                ("048", 2, "0021"),
                ("049", 3, "0021"),
                ("050", 4, "0021"),
                ("051", 5, "0021"),
            ),
            (),
        ),
        (
            *fixture_prd_008_projection,
        ),
    )

    if fixture_prd_008_projection != PRD_008_IMMUTABLE_PROJECTION:
        raise AssertionError("production PRD-008 lineage fixture differs")

    def assert_immutable_projection(candidate: Registry) -> None:
        immutable_actual = tuple(
            (
                program.prd_id,
                program.ad_id,
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
            for program in candidate.program_lineage
        )
        if immutable_actual != immutable_expected:
            raise AssertionError(
                "production program-lineage immutable projection differs"
            )

    assert_immutable_projection(registry)

    program_007 = next(
        program for program in registry.program_lineage if program.prd_id == "007"
    )
    missing_tranche_program = replace(
        program_007,
        tranches=program_007.tranches[:-1],
    )
    missing_tranche_candidate = replace(
        registry,
        program_lineage=tuple(
            missing_tranche_program if program.prd_id == "007" else program
            for program in registry.program_lineage
        ),
    )
    try:
        assert_immutable_projection(missing_tranche_candidate)
    except AssertionError:
        pass
    else:
        raise AssertionError("missing PRD-007 tranche mutation accepted")

    def assert_state_contract(candidate: Registry) -> None:
        for program in candidate.program_lineage:
            states = tuple(relation.state for relation in program.tranches)
            if any(state not in {"done", "active", "draft"} for state in states):
                raise AssertionError(
                    f"PRD-{program.prd_id} original tranche state domain differs"
                )
            rank = {"done": 0, "active": 1, "draft": 2}
            if any(
                rank[current] > rank[following]
                for current, following in zip(states, states[1:])
            ):
                raise AssertionError(
                    f"PRD-{program.prd_id} original tranche is not one "
                    "contiguous done prefix followed by at most one active "
                    "relation and a draft suffix"
                )
            if states.count("active") > 1:
                raise AssertionError(
                    f"PRD-{program.prd_id} original tranche has more than one "
                    "active relation"
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
    # two synthetic first-unfinished positions used by rollover validation.
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
                    state=(
                        "done"
                        if relation.order < ready_order
                        else "active"
                        if relation.order == ready_order
                        else "draft"
                    ),
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

    multiple_active_program = replace(
        current,
        tranches=tuple(
            replace(
                relation,
                state=(
                    "done"
                    if relation.order < 2
                    else "active"
                    if relation.order <= 3
                    else "draft"
                ),
            )
            for relation in current.tranches
        ),
    )
    multiple_active_candidate = replace(
        registry,
        program_lineage=tuple(
            multiple_active_program if program.prd_id == "006" else program
            for program in registry.program_lineage
        ),
    )
    try:
        assert_state_contract(multiple_active_candidate)
    except AssertionError:
        pass
    else:
        raise AssertionError("multiple-active original-tranche mutation accepted")


def _assert_document_contract_projection(registry: Registry) -> None:
    if (
        registry.schema_version != 8
        or registry.route_state != "transition"
        or len(registry.profiles) != 69
    ):
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
            (
                "sdlc/prd",
                "sdlc/srs",
                "sdlc/interface",
                "sdlc/ad",
                "sdlc/adr",
                *specifications,
                *operations,
            ),
            "draft",
            "active",
        ),
        "activate-heading-profile": edges(references, "draft", "active"),
        "activate-execution-pair": edges(("sdlc/plan", "sdlc/task"), "draft", "active"),
        "complete-product-program": edges(
            ("sdlc/prd", "sdlc/srs", "sdlc/interface"), "active", "done"
        ),
        "accept-architecture": edges(("sdlc/ad",), "active", "accepted"),
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

    terminal_sources = (
        "sdlc/prd",
        "sdlc/srs",
        "sdlc/interface",
        "sdlc/ad",
        "sdlc/adr",
        "sdlc/spec",
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
    )
    standard_sources = (
        "content/reference",
        "governance/reference",
        "governance/memory",
        "governance/template-support",
    )
    terminal_templates = (
        "template/sdlc/prd",
        "template/sdlc/srs",
        "template/sdlc/interface",
        "template/sdlc/ad",
        "template/sdlc/adr",
        "template/sdlc/spec",
        "template/sdlc/agent-design",
        "template/sdlc/data-model",
        "template/sdlc/tests",
        "template/sdlc/plan",
        "template/sdlc/task",
        "template/sdlc/guide",
        "template/sdlc/policy",
        "template/sdlc/runbook",
        "template/sdlc/incident",
        "template/sdlc/postmortem",
    )
    standard_templates = (
        "template/content/reference",
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
        "native/document-migration-manifest",
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
    terminal_keys = (
        *standard_keys,
        (
            "artifact_id",
            "string",
            False,
            None,
            None,
            r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$",
            None,
        ),
    )
    archive_keys = (
        *standard_keys[:2],
        ("status", "string", False, ("literal", "archived"), None, None, None),
        *standard_keys[3:],
        (
            "artifact_id",
            "string",
            False,
            None,
            None,
            r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$",
            None,
        ),
        (
            "change_id",
            "string",
            True,
            None,
            None,
            r"^CHG-[0-9]{4}$",
            None,
        ),
        (
            "original_artifact_id",
            "string",
            True,
            None,
            None,
            r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$",
            None,
        ),
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
    archive_migration_keys = (
        *standard_keys[:2],
        ("status", "string", False, ("literal", "accepted"), None, None, None),
        *standard_keys[3:],
        (
            "artifact_id",
            "string",
            False,
            None,
            None,
            r"^MIG-[0-9]{4}$",
            None,
        ),
        (
            "migration_id",
            "string",
            False,
            None,
            None,
            r"^MIG-[0-9]{4}$",
            None,
        ),
    )
    expected_value_projection: dict[str, tuple[Any, ...]] = {}
    for profile_id in terminal_sources:
        expected_value_projection[profile_id] = (
            "authored-terminal-identity",
            terminal_sources,
            terminal_keys,
        )
    for profile_id in terminal_templates:
        expected_value_projection[profile_id] = (
            "template-terminal-authored",
            terminal_templates,
            standard_keys,
        )
    for profile_id in (*standard_sources, *standard_templates):
        expected_value_projection[profile_id] = (
            "authored-standard",
            standard_sources,
            standard_keys,
        )
    expected_value_projection["content/archive"] = (
        "archive-record",
        ("content/archive",),
        archive_keys,
    )
    expected_value_projection["template/content/archive"] = (
        "template-terminal-archive-record",
        ("template/content/archive",),
        tuple(item for item in archive_keys if item[0] != "artifact_id"),
    )
    expected_value_projection["content/archive-migration"] = (
        "archive-migration",
        ("content/archive-migration",),
        archive_migration_keys,
    )
    expected_value_projection["template/content/archive-migration"] = (
        "template-terminal-archive-migration",
        ("template/content/archive-migration",),
        tuple(item for item in archive_migration_keys if item[0] != "artifact_id"),
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
        "sdlc/srs": ("system-requirement", None, "Traceability", "body-contract"),
        "sdlc/interface": (
            "interface-requirement",
            None,
            "Traceability",
            "body-contract",
        ),
        "sdlc/ad": ("architecture-description", None, "Traceability", "body-contract"),
        "sdlc/adr": ("architecture-decision", None, "Traceability", "body-contract"),
        "sdlc/spec": (
            "implementation-specification",
            None,
            "Traceability",
            "body-contract",
        ),
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
        "content/archive-migration": (
            "archive-migration",
            None,
            "Recovery",
            "heading-set",
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
        "native/document-migration-manifest",
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
        "template/content/archive-migration": "content/archive-migration",
        "template/governance/memory": "governance/memory",
        "template/readme/repository": "readme/repository",
        "template/readme/stage-index": "readme/stage-index",
        "template/readme/collection-index": "readme/collection-index",
        "template/readme/implementation": "readme/implementation",
        "template/readme/snapshot-pack": "readme/snapshot-pack",
        "template/readme/workspace-staging": "readme/workspace-staging",
        "template/content/reference": "content/reference",
        "template/sdlc/adr": "sdlc/adr",
        "template/sdlc/ad": "sdlc/ad",
        "template/sdlc/plan": "sdlc/plan",
        "template/sdlc/task": "sdlc/task",
        "template/sdlc/guide": "sdlc/guide",
        "template/sdlc/incident": "sdlc/incident",
        "template/sdlc/policy": "sdlc/policy",
        "template/sdlc/postmortem": "sdlc/postmortem",
        "template/sdlc/runbook": "sdlc/runbook",
        "template/sdlc/prd": "sdlc/prd",
        "template/sdlc/interface": "sdlc/interface",
        "template/sdlc/srs": "sdlc/srs",
        "template/sdlc/agent-design": "sdlc/agent-design",
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
    if actual_roles != expected_roles or len(expected_roles) != 69:
        raise AssertionError("production complete role/source projection differs")

    authored_draft = (
        "sdlc/prd",
        "sdlc/interface",
        "sdlc/srs",
        *tuple(
            profile_id
            for profile_id in terminal_sources
            if profile_id
            not in {"sdlc/prd", "sdlc/srs", "sdlc/interface", "sdlc/plan", "sdlc/task"}
        ),
        *standard_sources,
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
        "native/document-migration-manifest",
        "exception/native-contract-openapi",
        "exception/native-contract-graphql",
        "exception/native-contract-protobuf",
        "exception/generated-record",
        "exception/program-non-target",
        "template/content/archive",
        "template/content/archive-migration",
        "template/governance/memory",
        "template/readme/repository",
        "template/readme/stage-index",
        "template/readme/collection-index",
        "template/readme/implementation",
        "template/readme/snapshot-pack",
        "template/readme/workspace-staging",
        "template/content/reference",
        "template/sdlc/adr",
        "template/sdlc/ad",
        "template/sdlc/plan",
        "template/sdlc/task",
        "template/sdlc/guide",
        "template/sdlc/incident",
        "template/sdlc/policy",
        "template/sdlc/postmortem",
        "template/sdlc/runbook",
        "template/sdlc/prd",
        "template/sdlc/interface",
        "template/sdlc/srs",
        "template/sdlc/agent-design",
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
    expected_admissions["content/archive-migration"] = admission_signature(
        "archive-migration-control",
        ("content/archive-migration",),
        "states",
        ("accepted",),
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
    if actual_admissions != expected_admissions or len(expected_admissions) != 69:
        raise AssertionError("production complete admission projection differs")

    lifecycle_groups = (
        (
            "product",
            ("sdlc/prd", "sdlc/srs", "sdlc/interface"),
            ("done",),
            (
                ("draft", "active", "activate-self-body"),
                ("active", "done", "complete-product-program"),
            ),
        ),
        (
            "architecture-requirement",
            ("sdlc/ad",),
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
        (
            "archive-migration",
            ("content/archive-migration",),
            ("accepted",),
            (),
        ),
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
    if actual_lifecycles != expected_lifecycles or len(expected_lifecycles) != 69:
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
                (
                    "sdlc/prd",
                    "sdlc/srs",
                    "sdlc/interface",
                    "sdlc/ad",
                    "sdlc/adr",
                    *specifications,
                    *operations,
                ),
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
            edge_rows(
                ("sdlc/prd", "sdlc/srs", "sdlc/interface"),
                "active",
                "done",
            ),
            (("sdlc/spec",), ("done",), 1, None),
            "program-lineage",
            (1, None),
            "target-and-last-relation-changed",
            "body-contract",
            ("program-lineage-closed", "same-diff"),
        ),
        "accept-architecture": (
            edge_rows(("sdlc/ad",), "active", "accepted"),
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
        != "template-terminal-authored"
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
    if sum(len(profile.lifecycle.edges) for profile in registry.profiles) != 44:
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


def _repo_path_without_symlinks(
    root: Path,
    relative: PurePosixPath,
    *,
    final_kind: str,
) -> Path:
    if relative.is_absolute() or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    strict_root = _assert_repository_root_directory(
        root,
        error=GEMINI_NATIVE_CURRENT_SURFACE_ERROR,
    )

    candidate = strict_root
    for index, part in enumerate(relative.parts):
        candidate = candidate / part
        try:
            mode = candidate.lstat().st_mode
        except OSError as exc:
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
        if stat.S_ISLNK(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        is_final = index == len(relative.parts) - 1
        if not is_final and not stat.S_ISDIR(mode):
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        if is_final:
            if final_kind == "directory" and not stat.S_ISDIR(mode):
                raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
            if final_kind == "file" and not stat.S_ISREG(mode):
                raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    try:
        candidate.resolve(strict=True).relative_to(strict_root)
    except (OSError, ValueError) as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    return candidate


def _assert_repository_root_directory(
    root: Path,
    *,
    error: str = DOCUMENT_REGISTRY_ROOT_ERROR,
) -> Path:
    absolute_root = root.absolute()
    try:
        mode = absolute_root.lstat().st_mode
    except OSError as exc:
        raise AssertionError(error) from exc
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise AssertionError(error)
    try:
        return absolute_root.resolve(strict=True)
    except OSError as exc:
        raise AssertionError(error) from exc


def _load_gemini_settings_json(path: Path) -> dict[str, Any]:
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
            result[key] = value
        return result

    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    except AssertionError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    if not isinstance(payload, dict):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    return payload


def _expected_gemini_settings_json() -> dict[str, Any]:
    return {
        "$schema": GEMINI_SETTINGS_SCHEMA_URL,
        "agents": {"overrides": {}},
    }


def _harness_current_role_ids(root: Path) -> tuple[str, ...]:
    harness = _load_json(
        root / "docs/00.agent-governance/contracts/harness-contract.json"
    )
    try:
        inventory = harness["currentInventory"]
        role_ids = tuple(inventory["roleIds"])
    except (KeyError, TypeError) as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    if (
        inventory.get("state") != "current"
        or inventory.get("expectedRoleCount") != 12
        or inventory.get("expectedSurfaceCount") != 4
        or inventory.get("expectedProjectionCount") != 48
        or len(role_ids) != 12
        or len(role_ids) != len(set(role_ids))
        or any(not isinstance(role_id, str) or not role_id for role_id in role_ids)
    ):
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
    return role_ids


def _assert_gemini_native_current_surface(root: Path) -> None:
    """Prove repo-static Gemini current files without claiming runtime readiness."""
    strict_root = _assert_repository_root_directory(
        root,
        error=GEMINI_NATIVE_CURRENT_SURFACE_ERROR,
    )
    role_ids = _harness_current_role_ids(strict_root)
    agents_dir = _repo_path_without_symlinks(
        strict_root,
        PurePosixPath(".gemini/agents"),
        final_kind="directory",
    )
    settings_path = _repo_path_without_symlinks(
        strict_root,
        PurePosixPath(".gemini/settings.json"),
        final_kind="file",
    )

    expected_names = {f"{role_id}.md" for role_id in role_ids}
    try:
        entries = tuple(agents_dir.iterdir())
    except OSError as exc:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
    actual_names: set[str] = set()
    for entry in entries:
        try:
            mode = entry.lstat().st_mode
        except OSError as exc:
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR) from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode) or entry.suffix != ".md":
            raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)
        actual_names.add(entry.name)
    if actual_names != expected_names:
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)

    settings = _load_gemini_settings_json(settings_path)
    if settings != _expected_gemini_settings_json():
        raise AssertionError(GEMINI_NATIVE_CURRENT_SURFACE_ERROR)


def _write_minimal_gemini_surface(root: Path, role_ids: tuple[str, ...]) -> None:
    agents_dir = root / ".gemini/agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for role_id in role_ids:
        (agents_dir / f"{role_id}.md").write_text(
            f"---\nname: {role_id}\n---\n\n# {role_id}\n",
            encoding="utf-8",
        )
    (root / ".gemini/settings.json").write_text(
        json.dumps(_expected_gemini_settings_json(), indent=2) + "\n",
        encoding="utf-8",
    )


def _assert_gemini_native_current_surface_mutation_proofs(root: Path) -> None:
    role_ids = _harness_current_role_ids(root)
    mutation_names = (
        "root-symlink",
        "agents-dir-symlink",
        "missing-agent",
        "extra-agent",
        "symlink-agent",
        "missing-settings",
        "settings-symlink",
        "malformed-settings",
        "duplicate-settings-key",
        "unknown-settings-key",
        "nonempty-agent-overrides",
    )
    for mutation_name in mutation_names:
        with tempfile.TemporaryDirectory(
            prefix="document-registry-gemini-current-"
        ) as directory:
            fixture_root = Path(directory)
            source_harness = root / "docs/00.agent-governance/contracts"
            target_harness = fixture_root / "docs/00.agent-governance/contracts"
            target_harness.mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                source_harness / "harness-contract.json",
                target_harness / "harness-contract.json",
            )
            _write_minimal_gemini_surface(fixture_root, role_ids)
            _assert_gemini_native_current_surface(fixture_root)
            probe_root = fixture_root

            if mutation_name == "root-symlink":
                probe_root = fixture_root / "repository-root-link"
                probe_root.symlink_to(fixture_root, target_is_directory=True)
            elif mutation_name == "agents-dir-symlink":
                shutil.rmtree(fixture_root / ".gemini/agents")
                outside = fixture_root / "outside-agents"
                outside.mkdir()
                (outside / f"{role_ids[0]}.md").write_text(
                    "# outside\n", encoding="utf-8"
                )
                (fixture_root / ".gemini/agents").symlink_to(outside)
            elif mutation_name == "missing-agent":
                (fixture_root / ".gemini/agents" / f"{role_ids[0]}.md").unlink()
            elif mutation_name == "extra-agent":
                (fixture_root / ".gemini/agents/extra-reviewer.md").write_text(
                    "# extra\n", encoding="utf-8"
                )
            elif mutation_name == "symlink-agent":
                target = fixture_root / ".gemini/agents" / f"{role_ids[0]}.md"
                target.unlink()
                target.symlink_to(f"{role_ids[1]}.md")
            elif mutation_name == "missing-settings":
                (fixture_root / ".gemini/settings.json").unlink()
            elif mutation_name == "settings-symlink":
                (fixture_root / ".gemini/settings.json").unlink()
                (fixture_root / ".gemini/settings.json").symlink_to(
                    "agents/code-reviewer.md"
                )
            elif mutation_name == "malformed-settings":
                (fixture_root / ".gemini/settings.json").write_text(
                    "{\n", encoding="utf-8"
                )
            elif mutation_name == "duplicate-settings-key":
                (fixture_root / ".gemini/settings.json").write_text(
                    (
                        '{"$schema":"'
                        + GEMINI_SETTINGS_SCHEMA_URL
                        + '","agents":{"overrides":{}},"agents":{}}\n'
                    ),
                    encoding="utf-8",
                )
            elif mutation_name == "unknown-settings-key":
                settings = _expected_gemini_settings_json()
                settings["hooks"] = {}
                (fixture_root / ".gemini/settings.json").write_text(
                    json.dumps(settings) + "\n", encoding="utf-8"
                )
            elif mutation_name == "nonempty-agent-overrides":
                settings = _expected_gemini_settings_json()
                settings["agents"]["overrides"]["supervisor"] = {"model": "auto"}
                (fixture_root / ".gemini/settings.json").write_text(
                    json.dumps(settings) + "\n", encoding="utf-8"
                )

            try:
                _assert_gemini_native_current_surface(probe_root)
            except AssertionError as exc:
                if str(exc) != GEMINI_NATIVE_CURRENT_SURFACE_ERROR:
                    raise AssertionError(
                        "Gemini native current surface guard returned an unstable error"
                    ) from exc
            else:
                raise AssertionError(
                    f"Gemini native current surface guard accepted {mutation_name}"
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
        PurePosixPath(".gemini/agents/code-reviewer.md"): (
            "exception/provider-native-metadata"
        ),
    }
    for path, expected_profile in probes.items():
        actual_profile = classify_path(registry, path).profile_id
        if actual_profile != expected_profile:
            raise AssertionError(
                f"{path}: expected {expected_profile!r}, got {actual_profile!r}"
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
        source_required = source.frontmatter.required
        source_allowed = source.frontmatter.allowed
        source_order = source.frontmatter.order
        source_value_contract = source.value_contract
        if source_id in WORK108_MANDATORY_PROFILE_IDS:
            source_required = tuple(
                key for key in source_required if key != "artifact_id"
            )
            source_allowed = tuple(key for key in source_allowed if key != "artifact_id")
            source_order = tuple(key for key in source_order if key != "artifact_id")
            source_value_contract = replace(
                source_value_contract,
                keys=tuple(
                    item
                    for item in source_value_contract.keys
                    if item.key != "artifact_id"
                ),
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
                    source_required,
                    source_allowed,
                ),
            ),
            (
                "frontmatter-order",
                profile.frontmatter.order,
                source_order,
            ),
            ("status", profile.status_domain, source.status_domain),
            ("headings", profile.headings, source.headings),
            ("class", profile.profile_class, source.profile_class),
            ("body", profile.body_contract, source.body_contract),
            (
                "value-contract",
                profile.value_contract.keys,
                source_value_contract.keys,
            ),
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
            template_contract = next(
                item
                for item in mutated["documentContracts"]["valueContracts"]
                if item["id"] == "template-terminal-authored"
            )
            owner = next(
                item for item in template_contract["keys"] if item["key"] == "owner"
            )
            owner["pattern"] = "^platform$"
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
    if len(markdown_form_paths) != 29 or len(native_form_paths) != 3:
        raise AssertionError(
            "canonical form inventory must contain 29 Markdown and three native forms"
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
            source_frontmatter = source.frontmatter
            if source_id in WORK108_MANDATORY_PROFILE_IDS:
                source_frontmatter = replace(
                    source_frontmatter,
                    required=tuple(
                        key for key in source_frontmatter.required if key != "artifact_id"
                    ),
                    allowed=tuple(
                        key for key in source_frontmatter.allowed if key != "artifact_id"
                    ),
                    order=tuple(
                        key for key in source_frontmatter.order if key != "artifact_id"
                    ),
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
                source_frontmatter,
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
    return path.name == "README.md" and path != PurePosixPath(".github/README.md")


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
    if len(active_rows) != 51 or len(retired_rows) != 23:
        raise AssertionError("README fixture must contain exact active51 and retired23")

    active_keys = {"path", "profile", "requiredH2", "allowedH2", "new"}
    retired_keys = active_keys | {"retiredBy", "destination"}
    active_paths = {PurePosixPath(path) for path in active_order}
    retired_paths = {PurePosixPath(path) for path in retired_order}
    if active_paths & retired_paths:
        raise AssertionError("README activePaths and retiredPaths must be disjoint")

    baseline_readmes = {
        path for path in inventory.baseline_paths if _is_readme_path(path)
    }
    work105_readme_renames = {
        PurePosixPath("docs/02.architecture/requirements/README.md"):
            PurePosixPath("docs/02.architecture/descriptions/README.md"),
        PurePosixPath("examples/aws/docs/02.architecture/requirements/README.md"):
            PurePosixPath("examples/aws/docs/02.architecture/descriptions/README.md"),
        PurePosixPath("examples/azure/docs/02.architecture/requirements/README.md"):
            PurePosixPath("examples/azure/docs/02.architecture/descriptions/README.md"),
    }
    conceptual_baseline_readmes = {
        work105_readme_renames.get(path, path) for path in baseline_readmes
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
                if row["retiredBy"] == "WERPC-008":
                    try:
                        routed_profile = classify_path(registry, path)
                    except DocumentContractError as exc:
                        raise AssertionError(
                            f"{path}: WERPC retired README route is invalid"
                        ) from exc
                    if routed_profile.profile_id != row["profile"]:
                        raise AssertionError(
                            f"{path}: WERPC retired README route differs from profile"
                        )
                else:
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
            expected_new = path not in conceptual_baseline_readmes
            if row["new"] is not expected_new:
                raise AssertionError(
                    f"{path}: README new flag differs from immutable baseline inventory"
                )
            if lifecycle == "active":
                if path not in tracked_readmes or not (root / path).is_file():
                    raise AssertionError(f"README active path is absent: {path}")
                continue
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
            if row["retiredBy"] == "WERPC-008":
                expected_destination = PurePosixPath(
                    "docs/90.references/research/2026-08-08-wer/README.md"
                )
                expected_paths = {
                    PurePosixPath(
                        "docs/90.references/research/2026-07-04-wer/README.md"
                    ),
                    PurePosixPath(
                        "docs/90.references/research/2026-07-07-wer/README.md"
                    ),
                    PurePosixPath(
                        "docs/90.references/research/2026-08-07-wer/README.md"
                    ),
                }
                if path not in expected_paths or destination_path != expected_destination:
                    raise AssertionError(
                        f"{path}: WERPC README retirement destination is invalid"
                    )
                if path in tracked_readmes or (root / path).exists():
                    raise AssertionError(f"README retired path is still current: {path}")
                continue
            if row["retiredBy"] != "ADM-006":
                raise AssertionError(
                    f"{path}: README retirement owner must be ADM-006 or WERPC-008"
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

    active_baseline = active_paths & conceptual_baseline_readmes
    active_program_created = active_paths - conceptual_baseline_readmes
    if len(baseline_readmes) != 67:
        raise AssertionError("README immutable baseline must contain exact 67 paths")
    retired_baseline = retired_paths & conceptual_baseline_readmes
    retired_program_created = retired_paths - conceptual_baseline_readmes
    if (
        len(active_baseline) != 45
        or len(active_program_created) != 6
        or len(retired_baseline) != 22
        or len(retired_program_created) != 1
    ):
        raise AssertionError(
            "README handoff must contain active45+new6 and retired22+new1"
        )
    if active_baseline | retired_baseline != conceptual_baseline_readmes:
        raise AssertionError(
            "README active baseline plus retired paths must reconstruct baseline67"
        )
    current_rename_targets = set(work105_readme_renames.values()) & tracked_readmes
    if active_program_created != new_readmes - current_rename_targets:
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
    if len(declared_new_paths) != 6:
        raise AssertionError(
            "README fixture mutation proof requires exact six active program-created paths"
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


def _work105_generator_transition_control_lines(text: str) -> frozenset[int]:
    """Return the sole reviewed legacy-row assignment in the pinned overlay."""

    lines = tuple(text.splitlines())
    if any(
        lines.count(literal) != 1
        for literal in WORK105_WIKI_GENERATOR_REVIEWED_LITERALS
    ):
        return frozenset()

    def block_starts(block: tuple[str, ...]) -> tuple[int, ...]:
        width = len(block)
        return tuple(
            index
            for index in range(len(lines) - width + 1)
            if lines[index : index + width] == block
        )

    header_starts = block_starts(WORK105_WIKI_GENERATOR_HEADER_LINES)
    projection_starts = block_starts(WORK105_WIKI_GENERATOR_PROJECTION_LINES)
    if len(header_starts) != 1 or len(projection_starts) != 1:
        return frozenset()
    base_offset = WORK105_WIKI_GENERATOR_HEADER_LINES.index(
        WORK105_WIKI_GENERATOR_BASE_ROW_ASSIGNMENT
    )
    return frozenset({header_starts[0] + base_offset + 1})


def _work105_consumer_disposition(
    pattern_id: str,
    path: str,
    matched_line: str,
    *,
    historical_context: bool = False,
    line_context: str | None = None,
    generator_transition_control: bool = False,
) -> tuple[str, str, str, str]:
    """Classify one pinned WORK-105 consumer without an open fallback bucket."""

    pattern_ids = frozenset(pattern_id.split("+"))
    if not pattern_ids or not pattern_ids <= {"ard", "authored-api-spec"}:
        raise AssertionError(f"unknown WORK-105 consumer pattern: {pattern_id}")
    if historical_context or path.startswith(
        ("docs/90.references/", "docs/98.archive/")
    ):
        return (
            "immutable-history",
            "retain-history",
            path,
            "Preserve pinned observation, archive, progress, or completed-history evidence.",
        )
    lowered = matched_line.casefold()
    immutable_archive_namespace = (
        path == "docs/99.templates/support/document-profiles.json"
        and re.fullmatch(
            r'"?docs/98\.archive/02\.architecture/requirements/'
            r'000[1-3]-[^"/]+\.md"?,?',
            matched_line.strip(),
        )
        is not None
    )
    if immutable_archive_namespace:
        return (
            "immutable-history",
            "retain-history",
            path,
            "Preserve the exact immutable Stage 98 namespace inventory.",
        )
    strict_case_context = line_context.strip() if line_context is not None else ""
    validator_occurrence_control = (
        path == "scripts/validate-document-contract-registry.py"
        and r"ambiguous\s*=\s*" in strict_case_context
        and "historical " + "ARD" + " remains current" in strict_case_context
    )
    strict_occurrence_control = (
        path == "tests/test_document_strict_cutover.py"
        and (
            re.fullmatch(
                r'ambiguous\s*=\s*["\']?historical ARD remains current '
                r'sdlc/ard["\']?',
                strict_case_context,
            )
            is not None
            or re.fullmatch(
                r'\(?\s*["\']?ard["\']?\s*,\s*'
                r'["\']?consumer\.json["\']?\s*,\s*'
                r'["\']?no WORK-105 token is present["\']?\s*\)?',
                strict_case_context,
            )
            is not None
        )
    )
    if validator_occurrence_control or strict_occurrence_control:
        return (
            "retired-route-control",
            "retired-route-negative",
            "WORK-105 retired authored-route controls",
            "Retain an explicit retired-route assertion or negative fixture line.",
        )
    ria_transition_overlay_control = (
        path
        in {
            "scripts/reference_information_architecture.py",
            "tests/test_reference_information_architecture.py",
        }
        and line_context is not None
        and "Architecture requirements" in line_context
        and "ARD-style architecture requirement index" in line_context
    )
    if ria_transition_overlay_control:
        return (
            "retired-route-control",
            "retired-route-negative",
            "WORK-105 RIA generator transition overlay",
            "Retain only the exact base row in the reviewed Stage 90 generator overlay.",
        )
    wiki_generator_transition_control = (
        path == WORK105_WIKI_GENERATOR_PATH
        and generator_transition_control
        and line_context == WORK105_WIKI_GENERATOR_BASE_ROW_ASSIGNMENT
    )
    if wiki_generator_transition_control:
        return (
            "retired-route-control",
            "retired-route-negative",
            "WORK-105 LLM Wiki generator transition overlay",
            "Retain only the exact pinned old-to-new row assignment and OID guard.",
        )
    migration_contract_path = path in WORK105_MIGRATION_CONTRACT_PATHS
    contract_context = line_context if line_context is not None else matched_line
    retirement_wording = re.search(
        r"\b(?:legacy|retired|retirement|unconverted|source|migration|"
        r"convert(?:ed|s|ing)?|replace(?:d|ment)?|terminal|mapping|"
        r"classif(?:ier|ication)|evidence)\b",
        contract_context.casefold(),
    )
    replacement_evidence = re.search(
        r"\bAD(?:-[0-9]{4})?\b|sdlc/ad|descriptions/ad-|"
        r"\b(?:SRS|Interface Requirement)\b|migrate-current|retain-history",
        contract_context,
    )
    migration_contract_control = (
        migration_contract_path
        and retirement_wording is not None
        and replacement_evidence is not None
    )
    if migration_contract_control:
        return (
            "retired-route-control",
            "retired-route-negative",
            "WORK-105 retired authored-route controls",
            "Retain an explicit retired-route assertion or negative fixture line.",
        )
    history_signal = re.search(
        r"\b(?:historical|history|provenance|superseded|previously|former)\b|"
        r"\bsource ard\b|\bcompleted (?:the )?(?:ard|migration)|"
        r"retained historical ard evidence|"
        r"docs/(?:90\.references|98\.archive)/|"
        r"\|\s*ard-[0-9]{4}\s*\|.*\bad-[0-9]{4}\b.*descriptions/ad-",
        lowered,
    )
    if history_signal is not None and re.search(
        r"\b(?:current|live|active authoring|active route)\b", lowered
    ):
        raise AssertionError("WORK-105 consumer occurrence is semantically mixed")
    if history_signal is not None:
        return (
            "semantic-history",
            "retain-history",
            path,
            "Retain an explicitly historical, superseded, or provenance-only reference.",
        )
    authored_api_signal = re.search(
        r"sdlc/api-spec|template/sdlc/api-spec|api-spec\.template\.md|"
        r"(^|/)api-spec\.md",
        matched_line,
    )
    if "authored-api-spec" in pattern_ids and authored_api_signal is None:
        return (
            "native-contract-consumer",
            "retain-native",
            "OpenAPI/GraphQL/Protobuf native contract surfaces",
            "Retain the native contract identity, bytes, and consumer evidence.",
        )
    registry_fixture_control = (
        path == "tests/fixtures/document-contracts/registry-cases.json"
        and line_context is not None
        and re.match(r'^\s*"[^"\n]+"\s*:', line_context) is not None
    )
    validator_control = path == "scripts/validate-document-contract-registry.py"
    strict_test_control = (
        path == "tests/test_document_strict_cutover.py"
        and line_context is not None
        and re.search(
            r"assert|for value in|pattern\[\"id\"\]|patternId|"
            r"docs/98\.archive/|sdlc/ard|template/sdlc/ard|ard\.template|"
            r"api-spec|requirements/[^\s\"']*retired|"
            r"path\.startswith\([\"']docs/02\.architecture/requirements/|"
            r"\[\"ard\"|\"ard\"\s*:|^\s*\"ard\",?\s*$",
            line_context,
        )
        is not None
    )
    retired_field_assertion_control = (
        path == "tests/test_active_corpus_retention.py"
        and matched_line == "programArd"
        and line_context is not None
        and re.search(
            r"assertNotIn\(\s*[\"']programArd[\"']\s*,\s*row\s*\)",
            line_context,
        )
        is not None
    )
    retired_alias_control = (
        path
        in {
            "scripts/validate-document-lifecycle.py",
            "scripts/validate-links-and-owners.py",
            "scripts/validate-markdown-profiles.py",
            "scripts/archive_cutover.py",
            "tests/fixtures/document-lifecycle.json",
            "tests/fixtures/links-and-owners.json",
            "tests/fixtures/markdown-profiles.json",
            "tests/test_archive_cutover.py",
        }
        and re.search(
            r"02\.architecture/requirements/(?:README\.md|000[1-9]-|001[01]-)|"
            r"ard\.template\.md|api-spec\.template\.md|sdlc/api-spec|"
            r"original_type=[\"']ard[\"']|three immutable ARD rows",
            matched_line,
        )
        is not None
    )
    lifecycle_control = path == "scripts/validate-document-lifecycle.py"
    links_control = (
        path == "scripts/validate-links-and-owners.py"
        and line_context is not None
        and re.search(
            r"WORK105|work105|accepted_history|completed_history|"
            r"retired|negative|mutation",
            line_context,
        )
        is not None
    )
    active_corpus_test_control = (
        path == "tests/test_active_corpus_retention.py"
        and line_context is not None
        and re.search(
            r"wrong-|assertNotIn|\(\s*[\"']ard[\"']\s*,|"
            r"field in \{[^}]*[\"']ard[\"']",
            line_context,
        )
        is not None
    )
    links_fixture_control = (
        path == "tests/fixtures/links-and-owners.json"
        and line_context is not None
        and "docs/05.operations/guides/9997-history.md" in line_context
        and '"status": "done"' in line_context
    )
    fixture_or_code_control = (
        registry_fixture_control
        or validator_control
        or strict_test_control
        or retired_field_assertion_control
        or retired_alias_control
        or lifecycle_control
        or links_control
        or active_corpus_test_control
        or links_fixture_control
    )
    retired_route_control = re.search(
        r"\b(?:reject(?:ed|ion)?|forbid(?:den)?|negative|"
        r"zero (?:live|authored|instance)|no active|must not)\b",
        lowered,
    )
    if fixture_or_code_control or retired_route_control is not None:
        return (
            "retired-route-control",
            "retired-route-negative",
            "WORK-105 retired authored-route controls",
            "Retain an explicit retired-route assertion or negative fixture line.",
        )
    current_ard_signal = re.search(WORK105_CONSUMER_PATTERNS[0]["regex"], matched_line)
    if "ard" in pattern_ids and current_ard_signal is not None:
        return (
            "current-ard-consumer",
            "migrate-current",
            "sdlc/ad at docs/02.architecture/descriptions/ad-<id>-<slug>.md",
            "Migrate the current ARD profile, route, template, label, and relationship consumer.",
        )
    if "authored-api-spec" in pattern_ids and authored_api_signal is not None:
        return (
            "current-authored-api-spec-consumer",
            "migrate-current",
            "terminal SRS, Interface Requirement, Spec, or native contract surface",
            "Retire the authored API Spec route while preserving native machine contracts.",
        )
    raise AssertionError("WORK-105 consumer occurrence is unclassified")


def _work105_occurrence_dispositions(
    pattern: dict[str, str],
    path: str,
    matched_line: str,
    *,
    historical_context: bool = False,
    semantic_context: str | None = None,
    generator_transition_control: bool = False,
) -> tuple[tuple[str, str, str, str] | None, ...]:
    """Classify each semantic occurrence without line-wide category masking."""

    pattern_id = pattern.get("id")
    expression = pattern.get("regex")
    if not isinstance(pattern_id, str) or not isinstance(expression, str):
        raise AssertionError("WORK-105 consumer pattern is malformed")
    matches = tuple(re.finditer(expression, matched_line))
    boundaries = tuple(
        match.start() for match in WORK105_SEMANTIC_BOUNDARY.finditer(matched_line)
    )
    dispositions: list[tuple[str, str, str, str] | None] = []
    for occurrence in matches:
        left_index = bisect.bisect_left(boundaries, occurrence.start()) - 1
        right_index = bisect.bisect_left(boundaries, occurrence.end())
        left = boundaries[left_index] + 1 if left_index >= 0 else 0
        right = (
            boundaries[right_index]
            if right_index < len(boundaries)
            else len(matched_line)
        )
        segment = matched_line[left:right]
        try:
            disposition = _work105_consumer_disposition(
                pattern_id,
                path,
                segment,
                historical_context=historical_context,
                line_context=(
                    semantic_context if semantic_context is not None else matched_line
                ),
                generator_transition_control=generator_transition_control,
            )
        except AssertionError:
            disposition = None
        dispositions.append(disposition)
    return tuple(dispositions)


def _work105_markdown_contexts(lines: list[str]) -> tuple[str, ...]:
    """Project prose paragraphs and bind table rows to their exact header."""

    contexts = list(lines)
    cursor = 0
    while cursor < len(lines):
        if lines[cursor].lstrip().startswith("|"):
            end = cursor + 1
            while end < len(lines) and lines[end].lstrip().startswith("|"):
                end += 1
            header = lines[cursor].strip()
            for index in range(cursor, end):
                contexts[index] = f"{header} {lines[index].strip()}"
            cursor = end
            continue
        if (
            not lines[cursor].strip()
            or lines[cursor].lstrip().startswith(("#", "```"))
        ):
            cursor += 1
            continue
        end = cursor + 1
        while (
            end < len(lines)
            and lines[end].strip()
            and not lines[end].lstrip().startswith(("#", "|", "```"))
        ):
            end += 1
        context = " ".join(line.strip() for line in lines[cursor:end])
        for index in range(cursor, end):
            contexts[index] = context
        cursor = end
    return tuple(contexts)


def _work105_record_disposition(
    dispositions: tuple[tuple[str, str, str, str] | None, ...],
) -> tuple[str, str, str, str]:
    if not dispositions or any(item is None for item in dispositions):
        raise AssertionError("WORK-105 base consumer occurrence is unclassified")
    classified = tuple(item for item in dispositions if item is not None)
    for priority in (
        "migrate-current",
        "retired-route-negative",
        "retain-history",
        "retain-native",
    ):
        selected = next((item for item in classified if item[1] == priority), None)
        if selected is not None:
            return selected
    raise AssertionError("WORK-105 base consumer disposition is unknown")


def _work105_base_consumer_records(
    root: Path, patterns: tuple[dict[str, str], ...]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    semantic_context_by_path: dict[str, tuple[str, ...]] = {}
    prefix = (WORK105_CONSUMER_BASE_COMMIT + ":").encode("utf-8")
    combined_regex = "|".join(f"({pattern['regex']})" for pattern in patterns)
    result = subprocess.run(
        [
            "git",
            "grep",
            "--full-name",
            "-n",
            "-I",
            "-E",
            "-e",
            combined_regex,
            WORK105_CONSUMER_BASE_COMMIT,
            "--",
        ],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode not in {0, 1}:
        raise AssertionError("WORK-105 pinned consumer census git grep failed")
    for raw_row in result.stdout.splitlines():
        if not raw_row.startswith(prefix):
            raise AssertionError("WORK-105 pinned consumer census row is malformed")
        raw_path, raw_line, matched_line = raw_row[len(prefix) :].split(b":", 2)
        path = raw_path.decode("utf-8")
        line_number = int(raw_line)
        decoded_line = matched_line.decode("utf-8")
        matched_patterns = tuple(
            pattern
            for pattern in patterns
            if re.search(pattern["regex"], decoded_line) is not None
        )
        pattern_id = "+".join(pattern["id"] for pattern in matched_patterns)
        historical_context = (
            path == WORK105_PROGRESS_PATH
            or path in WORK105_COMPLETED_HISTORY_PATHS
            or path in WORK105_ACCEPTED_BASE_HISTORY_PATHS
            or path in WORK105_PINNED_LEGACY_HISTORY_PATHS
        )
        semantic_context = None
        if path in WORK105_MIGRATION_CONTRACT_PATHS:
            if path not in semantic_context_by_path:
                try:
                    pinned_lines = (
                        _work105_pinned_blob(root, path).decode("utf-8").splitlines()
                    )
                except UnicodeDecodeError as exc:
                    raise AssertionError(
                        f"WORK-105 pinned migration contract is not UTF-8: {path}"
                    ) from exc
                semantic_context_by_path[path] = _work105_markdown_contexts(
                    pinned_lines
                )
            semantic_context = semantic_context_by_path[path][line_number - 1]
        occurrence_dispositions = tuple(
            disposition
            for pattern in matched_patterns
            for disposition in _work105_occurrence_dispositions(
                pattern,
                path,
                decoded_line,
                historical_context=historical_context,
                semantic_context=semantic_context,
            )
        )
        occurrence_count = len(occurrence_dispositions)
        if occurrence_count < 1:
            raise AssertionError("WORK-105 pinned consumer occurrence count is empty")
        consumer_class, disposition, target, reason = _work105_record_disposition(
            occurrence_dispositions
        )
        records.append(
            {
                "patternId": pattern_id,
                "path": path,
                "line": line_number,
                "matchedLineSha256": hashlib.sha256(matched_line).hexdigest(),
                "occurrenceCount": occurrence_count,
                "consumerClass": consumer_class,
                "disposition": disposition,
                "target": target,
                "reason": reason,
            }
        )
    return records


def _work105_consumer_census_sha256(records: list[dict[str, Any]]) -> str:
    payload = json.dumps(
        records, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _work105_read_stream_bounded(stream: Any, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = stream.read(min(65_536, limit + 1 - total))
        if not isinstance(chunk, bytes):
            raise AssertionError("WORK-105 Git stream type is invalid")
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)
        total += len(chunk)
        if total > limit:
            raise AssertionError("WORK-105 Git output exceeds its resource budget")


def _work105_git_stdout_bounded(
    root: Path, arguments: tuple[str, ...], limit: int
) -> bytes:
    process = subprocess.Popen(
        ["git", *arguments],
        cwd=root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    assert process.stdout is not None
    try:
        output = _work105_read_stream_bounded(process.stdout, limit)
        returncode = process.wait()
        if returncode != 0:
            raise AssertionError("WORK-105 Git inventory command failed")
        return output
    except Exception:
        process.kill()
        process.wait()
        raise
    finally:
        process.stdout.close()


def _work105_parse_staged_inventory(
    raw: bytes,
    *,
    entry_limit: int = WORK105_STAGED_ENTRY_LIMIT,
    path_byte_limit: int = WORK105_STAGED_PATH_BYTES,
) -> tuple[tuple[str, bytes], ...]:
    """Parse one bounded stage-zero inventory without disclosing path payloads."""

    if not isinstance(raw, bytes) or not raw.endswith(b"\0"):
        raise AssertionError("WORK-105 staged consumer inventory is malformed")
    records = raw.split(b"\0")
    if len(records) - 1 > entry_limit:
        raise AssertionError("WORK-105 staged path count exceeds its resource budget")
    grouped: dict[str, list[tuple[bytes, bytes, bytes]]] = {}
    for record in records[:-1]:
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, object_id, stage = header.split(b" ", 2)
            if (
                len(raw_path) > path_byte_limit
                or WORK105_OBJECT_ID.fullmatch(object_id) is None
            ):
                raise ValueError
            path = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as exc:
            raise AssertionError(
                "WORK-105 staged consumer inventory is malformed"
            ) from exc
        grouped.setdefault(path, []).append((mode, object_id, stage))
    selected: list[tuple[str, bytes]] = []
    for path, entries in sorted(grouped.items()):
        if len(entries) != 1 or entries[0][2] != b"0":
            raise AssertionError("WORK-105 staged consumer inventory is unmerged")
        mode, object_id, _ = entries[0]
        if mode.startswith(b"100"):
            selected.append((path, object_id))
    return tuple(selected)


def _work105_read_bounded_line(stream: Any) -> bytes:
    line = bytearray()
    while len(line) <= WORK105_GIT_HEADER_BYTES:
        byte = stream.read(1)
        if not isinstance(byte, bytes) or not byte:
            raise AssertionError("WORK-105 staged blob response is truncated")
        line.extend(byte)
        if byte == b"\n":
            return bytes(line)
    raise AssertionError("WORK-105 staged blob header exceeds its resource budget")


def _work105_read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(min(65_536, remaining))
        if not isinstance(chunk, bytes) or not chunk or len(chunk) > remaining:
            raise AssertionError("WORK-105 staged blob payload is truncated")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _work105_read_blob_batch_protocol(
    stream: Any,
    object_ids: tuple[bytes, ...],
    *,
    per_blob_limit: int = WORK105_STAGED_BLOB_BYTES,
    aggregate_limit: int = WORK105_STAGED_AGGREGATE_BYTES,
    object_limit: int = WORK105_STAGED_OBJECT_LIMIT,
) -> dict[bytes, bytes]:
    """Read an exact ``cat-file --batch`` protocol within fixed budgets."""

    if len(object_ids) > object_limit:
        raise AssertionError("WORK-105 staged object count exceeds its resource budget")
    blobs_by_id: dict[bytes, bytes] = {}
    aggregate = 0
    for expected_id in object_ids:
        if WORK105_OBJECT_ID.fullmatch(expected_id) is None:
            raise AssertionError("WORK-105 staged object identity is malformed")
        header = _work105_read_bounded_line(stream).removesuffix(b"\n").split(b" ")
        if len(header) != 3 or header[0] != expected_id or header[1] != b"blob":
            raise AssertionError("WORK-105 staged blob response is malformed")
        try:
            size = int(header[2])
        except ValueError as exc:
            raise AssertionError("WORK-105 staged blob size is malformed") from exc
        if size < 0 or size > per_blob_limit or aggregate + size > aggregate_limit:
            raise AssertionError("WORK-105 staged blob bytes exceed their resource budget")
        blobs_by_id[expected_id] = _work105_read_exact(stream, size)
        if stream.read(1) != b"\n":
            raise AssertionError("WORK-105 staged blob response is malformed")
        aggregate += size
    if stream.read(1) != b"":
        raise AssertionError("WORK-105 staged blob response has trailing data")
    return blobs_by_id


def _work105_read_staged_blob_batch(
    root: Path, object_ids: tuple[bytes, ...]
) -> dict[bytes, bytes]:
    if not object_ids:
        return {}
    with tempfile.TemporaryFile() as request:
        for object_id in object_ids:
            request.write(object_id + b"\n")
        request.seek(0)
        process = subprocess.Popen(
            ["git", "cat-file", "--batch"],
            cwd=root,
            stdin=request,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        assert process.stdout is not None
        try:
            blobs = _work105_read_blob_batch_protocol(process.stdout, object_ids)
            returncode = process.wait()
            if returncode != 0:
                raise AssertionError("WORK-105 staged blob read failed")
            return blobs
        except Exception:
            process.kill()
            process.wait()
            raise
        finally:
            process.stdout.close()


def _work105_staged_blobs(root: Path) -> tuple[tuple[str, bytes], ...]:
    """Read candidate bytes only from a bounded stage-zero index stream."""

    inventory = _work105_git_stdout_bounded(
        root,
        ("ls-files", "--stage", "-z"),
        WORK105_STAGED_INVENTORY_BYTES,
    )
    selected = _work105_parse_staged_inventory(inventory)
    unique_ids = tuple(dict.fromkeys(object_id for _, object_id in selected))
    blobs_by_id = _work105_read_staged_blob_batch(root, unique_ids)
    return tuple((path, blobs_by_id[object_id]) for path, object_id in selected)


def _work105_pinned_blob(root: Path, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{WORK105_CONSUMER_BASE_COMMIT}:{path}"],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"WORK-105 pinned blob is unavailable: {path}")
    return result.stdout


def _work108_without_outer_artifact_id(path: str, raw: bytes) -> bytes | None:
    identity = _work106_derive_artifact_identity(path)
    if identity is None:
        return None
    expected = f'artifact_id: "{identity.artifact_id}"'.encode("ascii")
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
    if len(matches) != 1:
        return None
    index = matches[0]
    if index == 0 or not lines[index - 1].startswith(b"updated:"):
        return None
    return b"".join(lines[:index] + lines[index + 1 :])


def _work105_post_state(
    root: Path, patterns: tuple[dict[str, str], ...]
) -> dict[str, dict[str, int]]:
    live = {pattern["id"]: 0 for pattern in patterns}
    unclassified = {pattern["id"]: 0 for pattern in patterns}
    authored_api_instances = 0
    compiled = tuple((pattern, re.compile(pattern["regex"])) for pattern in patterns)
    for relative, raw in _work105_staged_blobs(root):
        if b"\0" in raw:
            continue
        projected_raw = _work108_without_outer_artifact_id(relative, raw) or raw
        try:
            text = projected_raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        historical_line_limit = 0
        completed_history = False
        pinned_history_lines: tuple[str, ...] = ()
        if relative == WORK105_PROGRESS_PATH:
            pinned = _work105_pinned_blob(root, relative)
            if not raw.startswith(pinned):
                raise AssertionError(
                    "WORK-105 progress evidence is not an append-only pinned-base prefix"
                )
            historical_line_limit = len(pinned.splitlines())
        elif relative in (
            WORK105_COMPLETED_HISTORY_PATHS | WORK105_ACCEPTED_BASE_HISTORY_PATHS
        ):
            pinned = _work105_pinned_blob(root, relative)
            completed_history = raw == pinned or (
                _work108_without_outer_artifact_id(relative, raw) == pinned
            )
            if not completed_history:
                raise AssertionError(
                    f"WORK-105 completed-history blob changed: {relative}"
                )
        elif relative in WORK105_PINNED_LEGACY_HISTORY_PATHS:
            try:
                pinned_history_lines = tuple(
                    _work105_pinned_blob(root, relative).decode("utf-8").splitlines()
                )
            except UnicodeDecodeError as exc:
                raise AssertionError(
                    f"WORK-105 pinned history is not UTF-8: {relative}"
                ) from exc
        lines = text.splitlines()
        semantic_contexts = (
            _work105_markdown_contexts(lines)
            if relative in WORK105_MIGRATION_CONTRACT_PATHS
            else tuple(lines)
        )
        generator_transition_lines = (
            _work105_generator_transition_control_lines(text)
            if relative == WORK105_WIKI_GENERATOR_PATH
            else frozenset()
        )
        authored_api_instances += len(
            re.findall(r"(?m)^type:\s*sdlc/api-spec\s*$", text)
        )
        for line_number, matched_line in enumerate(lines, start=1):
            for pattern, expression in compiled:
                if expression.search(matched_line) is None:
                    continue
                occurrence_dispositions = _work105_occurrence_dispositions(
                    pattern,
                    relative,
                    matched_line,
                    historical_context=(
                        completed_history
                        or line_number <= historical_line_limit
                        or (
                            line_number <= len(pinned_history_lines)
                            and pinned_history_lines[line_number - 1] == matched_line
                        )
                    ),
                    semantic_context=semantic_contexts[line_number - 1],
                    generator_transition_control=(
                        line_number in generator_transition_lines
                    ),
                )
                for classified in occurrence_dispositions:
                    if classified is None:
                        unclassified[pattern["id"]] += 1
                        continue
                    _, disposition, _, _ = classified
                    if disposition == "migrate-current":
                        live[pattern["id"]] += 1
    return {
        "ard": {"live": live["ard"], "unclassified": unclassified["ard"]},
        "authoredApiSpec": {
            "instances": authored_api_instances,
            "live": live["authored-api-spec"],
            "unclassified": unclassified["authored-api-spec"],
        },
    }


def _assert_work105_consumer_disposition(root: Path, fixture: dict[str, Any]) -> None:
    section = fixture.get(WORK105_CONSUMER_DISPOSITION_FIXTURE_FIELD)
    expected_keys = {"baseCommit", "patterns", "censusSha256", "records", "postState"}
    if not isinstance(section, dict) or set(section) != expected_keys:
        raise AssertionError("WORK-105 consumer-disposition fixture shape differs")
    if section["baseCommit"] != WORK105_CONSUMER_BASE_COMMIT:
        raise AssertionError("WORK-105 consumer-disposition base commit differs")
    expected_patterns = tuple(copy.deepcopy(WORK105_CONSUMER_PATTERNS))
    actual_patterns = section["patterns"]
    if not isinstance(actual_patterns, list) or tuple(actual_patterns) != expected_patterns:
        raise AssertionError("WORK-105 consumer-disposition patterns differ")
    records = section["records"]
    if (
        not isinstance(records, list)
        or not records
        or any(not isinstance(record, dict) or set(record) != WORK105_CONSUMER_RECORD_KEYS for record in records)
    ):
        raise AssertionError("WORK-105 consumer-disposition records differ")
    generated = _work105_base_consumer_records(root, expected_patterns)
    if records != generated:
        raise AssertionError("WORK-105 consumer-disposition exact base census differs")
    digest = _work105_consumer_census_sha256(generated)
    if section["censusSha256"] != digest:
        raise AssertionError("WORK-105 consumer-disposition census digest differs")
    expected_post_state = {
        "ard": {"live": 0, "unclassified": 0},
        "authoredApiSpec": {"instances": 0, "live": 0, "unclassified": 0},
    }
    if section["postState"] != expected_post_state:
        raise AssertionError("WORK-105 consumer-disposition declared post-state differs")
    actual_post_state = _work105_post_state(root, expected_patterns)
    if actual_post_state != expected_post_state:
        raise AssertionError(
            "WORK-105 consumer-disposition post-state is not closed: "
            f"{actual_post_state!r}"
        )


def _work106_derive_artifact_identity(
    raw_path: str,
) -> Work106ArtifactIdentity | None:
    """Derive one canonical outer identity from a terminal repository path."""

    slug = WORK106_SLUG
    simple_patterns = (
        (rf"^docs/01\.requirements/(?P<id>[0-9]{{3}})-{slug}\.md$", "PRD"),
        (rf"^docs/01\.requirements/srs-(?P<id>[0-9]{{3}})-{slug}\.md$", "SRS"),
        (
            rf"^docs/01\.requirements/ifc-(?P<id>[0-9]{{3}})-(?P<suffix>{slug})\.md$",
            "IFC",
        ),
        (
            rf"^docs/02\.architecture/descriptions/ad-(?P<id>[0-9]{{4}})-{slug}\.md$",
            "AD",
        ),
        (
            rf"^docs/02\.architecture/decisions/(?P<id>[0-9]{{4}})-{slug}\.md$",
            "ADR",
        ),
        (rf"^docs/05\.operations/guides/(?P<id>[0-9]{{4}})-{slug}\.md$", "GUIDE"),
        (rf"^docs/05\.operations/policies/(?P<id>[0-9]{{4}})-{slug}\.md$", "POLICY"),
        (rf"^docs/05\.operations/runbooks/(?P<id>[0-9]{{4}})-{slug}\.md$", "RUNBOOK"),
    )
    for pattern, prefix in simple_patterns:
        match = re.fullmatch(pattern, raw_path)
        if match is None:
            continue
        suffix = match.groupdict().get("suffix")
        artifact_id = f"{prefix}-{match.group('id')}"
        if suffix is not None:
            artifact_id += f"-{suffix.upper()}"
        return Work106ArtifactIdentity(artifact_id)

    stage03 = re.fullmatch(
        rf"docs/03\.specs/(?P<id>[0-9]{{3}})-{slug}/"
        r"(?P<leaf>spec|agent-design|data-model|tests|plan|tasks)\.md",
        raw_path,
    )
    if stage03 is not None:
        prefix = {
            "spec": "SPEC",
            "agent-design": "AGENT-DESIGN",
            "data-model": "DATA-MODEL",
            "tests": "TESTS",
            "plan": "PLAN",
            "tasks": "TASK",
        }[stage03.group("leaf")]
        return Work106ArtifactIdentity(f"{prefix}-{stage03.group('id')}")

    incident = re.fullmatch(
        rf"docs/05\.operations/incidents/(?P<year>[0-9]{{4}})/"
        rf"INC-(?P<id>[0-9]{{3}})-(?P<slug>{slug})/"
        rf"(?P<leaf>INC-(?P=id)-(?P=slug)\.md|postmortem\.md)",
        raw_path,
    )
    if incident is not None:
        prefix = "POSTMORTEM" if incident.group("leaf") == "postmortem.md" else "INC"
        return Work106ArtifactIdentity(
            f"{prefix}-{incident.group('year')}-{incident.group('id')}"
        )

    change = re.fullmatch(
        rf"docs/98\.archive/changes/chg-(?P<id>[0-9]{{4}})-{slug}/"
        r"(?P<leaf>plan|task)\.md",
        raw_path,
    )
    if change is not None:
        change_id = f"CHG-{change.group('id')}"
        kind = "change-plan" if change.group("leaf") == "plan" else "change-task"
        prefix = "PLAN" if kind == "change-plan" else "TASK"
        return Work106ArtifactIdentity(
            f"{prefix}-{change_id}", change_id=change_id, record_kind=kind
        )

    migration = re.fullmatch(
        rf"docs/98\.archive/migrations/mig-(?P<id>[0-9]{{4}})-{slug}\.md",
        raw_path,
    )
    if migration is not None:
        migration_id = f"MIG-{migration.group('id')}"
        return Work106ArtifactIdentity(
            migration_id, migration_id=migration_id, record_kind="migration"
        )

    tombstone = re.fullmatch(
        r"docs/98\.archive/tombstones/(?P<stage>[0-9]{2}\.[a-z]+)/"
        r"tmb-(?P<body>[a-z0-9]+(?:-[a-z0-9]+)*)\.md",
        raw_path,
    )
    if tombstone is not None:
        allowed_types = WORK106_TOMBSTONE_TYPES.get(tombstone.group("stage"), ())
        body = tombstone.group("body")
        for type_token in sorted(allowed_types, key=len, reverse=True):
            prefix = type_token.lower() + "-"
            if body.startswith(prefix) and re.fullmatch(slug, body.removeprefix(prefix)):
                return Work106ArtifactIdentity(
                    f"TMB-{type_token}-{body.removeprefix(prefix).upper()}",
                    record_kind="tombstone",
                )
        return None
    return None


def _work106_artifact_diagnostics(
    records: tuple[tuple[str, Mapping[str, Any]], ...], *, terminal: bool
) -> tuple[str, ...]:
    diagnostics: list[str] = []
    owners: dict[str, list[str]] = {}
    for path, metadata in records:
        identity = _work106_derive_artifact_identity(path)
        declared = metadata.get("artifact_id")
        if identity is None:
            if declared is not None:
                diagnostics.append(f"ARTIFACT-ID-PROHIBITED:{path}")
            continue
        if isinstance(declared, str):
            owners.setdefault(declared, []).append(path)
        if declared is None:
            if terminal:
                diagnostics.append(f"ARTIFACT-ID-MISSING:{path}")
        elif not isinstance(declared, str) or declared != identity.artifact_id:
            diagnostics.append(f"ARTIFACT-ID-PATH:{path}")
        if identity.change_id is not None and metadata.get("change_id") != identity.change_id:
            diagnostics.append(f"ARTIFACT-CHANGE-ID:{path}")
        if identity.migration_id is not None and metadata.get("migration_id") != identity.migration_id:
            diagnostics.append(f"ARTIFACT-MIGRATION-ID:{path}")
    for artifact_id, paths in owners.items():
        if len(paths) > 1:
            diagnostics.append(
                f"ARTIFACT-ID-DUPLICATE:{artifact_id}:{','.join(sorted(paths))}"
            )
    return tuple(sorted(diagnostics))


def _work106_canonical_legacy_path(raw_path: str) -> bool:
    if not raw_path or raw_path.startswith("/") or "//" in raw_path or "\\" in raw_path:
        return False
    path = PurePosixPath(raw_path)
    return (
        path.as_posix() == raw_path
        and all(part not in {"", ".", ".."} for part in path.parts)
        and raw_path.startswith("docs/")
    )


def _work106_legacy_tombstone_token(legacy_path: str, source_blob: str) -> str:
    if not _work106_canonical_legacy_path(legacy_path):
        raise ValueError("legacy path is not canonical")
    if WORK106_OBJECT_ID.fullmatch(source_blob) is None:
        raise ValueError("source blob is not a lowercase Git object ID")
    digest = hashlib.sha256(
        legacy_path.encode("utf-8") + b"\0" + source_blob.encode("ascii")
    ).hexdigest().upper()
    return f"LEGACY-{digest}"


def _work106_tombstone_artifact_id(
    stage: str,
    terminal_type: str,
    original_artifact_id: str | None,
    legacy_path: str,
    source_blob: str,
) -> str:
    allowed = WORK106_TOMBSTONE_TYPES.get(stage)
    if allowed is None or terminal_type not in allowed:
        raise ValueError("tombstone stage/type pair is outside the closed map")
    if original_artifact_id is None:
        token = _work106_legacy_tombstone_token(legacy_path, source_blob)
    else:
        historical_ad_type = "AR" + "D"
        source_type = (
            historical_ad_type
            if terminal_type == "AD"
            and original_artifact_id.startswith(historical_ad_type + "-")
            else terminal_type
        )
        prefix = f"{source_type}-"
        token = original_artifact_id.removeprefix(prefix)
        if (
            not original_artifact_id.startswith(prefix)
            or re.fullmatch(r"[A-Z0-9]+(?:-[A-Z0-9]+)*", token) is None
        ):
            raise ValueError("original artifact identity does not match tombstone type")
    return f"TMB-{terminal_type}-{token}"


def _work106_is_canonical_artifact_id(value: object) -> bool:
    if not isinstance(value, str):
        return False
    return re.fullmatch(
        r"(?:PRD|SRS|AD|ADR|SPEC|AGENT-DESIGN|DATA-MODEL|TESTS|PLAN|TASK)-[0-9]{3,4}"
        r"|IFC-[0-9]{3}-[A-Z0-9]+(?:-[A-Z0-9]+)*"
        r"|(?:GUIDE|POLICY|RUNBOOK)-[0-9]{4}"
        r"|(?:INC|POSTMORTEM)-[0-9]{4}-[0-9]{3}"
        r"|(?:PLAN|TASK)-CHG-[0-9]{4}"
        r"|MIG-[0-9]{4}"
        r"|TMB-[A-Z]+(?:-[A-Z]+)*-[A-Z0-9]+(?:-[A-Z0-9]+)*",
        value,
    ) is not None


def _work106_ledger_diagnostics(
    rows: tuple[Mapping[str, Any], ...], *, current: bool
) -> tuple[str, ...]:
    diagnostics: list[str] = []
    stable_owners: dict[str, list[int]] = {}
    artifact_owners: dict[str, list[int]] = {}
    legacy_owners: dict[str, list[int]] = {}
    change_leaves: dict[str, set[str]] = {}
    tombstone_stages: dict[str, int] = {}
    for index, row in enumerate(rows):
        label = f"row-{index + 1}"
        if not isinstance(row, Mapping) or set(row) != WORK106_LEDGER_FIELDS:
            diagnostics.append(f"LEDGER-FIELDS:{label}")
            continue
        migration_id = row["migration_id"]
        if row["schema_version"] != 1 or not isinstance(migration_id, str) or WORK106_MIGRATION_ID.fullmatch(migration_id) is None:
            diagnostics.append(f"LEDGER-SCHEMA:{label}")
        legacy_path = row["legacy_path"]
        if not isinstance(legacy_path, str) or not _work106_canonical_legacy_path(legacy_path):
            diagnostics.append(f"LEDGER-LEGACY-PATH:{label}")
        else:
            legacy_owners.setdefault(legacy_path, []).append(index)
        stable_path = row["stable_path"]
        identity = _work106_derive_artifact_identity(stable_path) if isinstance(stable_path, str) else None
        if identity is None:
            diagnostics.append(f"LEDGER-STABLE-PATH:{label}")
        elif row["artifact_id"] != identity.artifact_id:
            diagnostics.append(f"LEDGER-ARTIFACT-ID:{label}")
        elif row["record_kind"] != identity.record_kind:
            diagnostics.append(f"LEDGER-RECORD-KIND:{label}")
        if isinstance(stable_path, str):
            stable_owners.setdefault(stable_path, []).append(index)
        artifact_id = row["artifact_id"]
        if isinstance(artifact_id, str):
            artifact_owners.setdefault(artifact_id, []).append(index)
        for field in (
            "source_commit",
            "legacy_archive_commit",
            "legacy_envelope_blob",
            "source_blob",
        ):
            if not isinstance(row[field], str) or WORK106_OBJECT_ID.fullmatch(row[field]) is None:
                diagnostics.append(f"LEDGER-GIT-OBJECT:{label}:{field}")
        if not isinstance(row["content_sha256"], str) or WORK106_CONTENT_DIGEST.fullmatch(row["content_sha256"]) is None:
            diagnostics.append(f"LEDGER-CONTENT-DIGEST:{label}")
        if not isinstance(row["reason"], str) or not row["reason"].strip():
            diagnostics.append(f"LEDGER-REASON:{label}")
        action, replacement = row["action"], row["replacement"]
        if action == "moved":
            if replacement is not None:
                diagnostics.append(f"LEDGER-ACTION-REPLACEMENT:{label}")
        elif action in {"merged", "replaced"}:
            if (
                identity is None
                or identity.record_kind != "tombstone"
                or not _work106_is_canonical_artifact_id(replacement)
            ):
                diagnostics.append(f"LEDGER-ACTION-REPLACEMENT:{label}")
        elif action == "deleted":
            if identity is None or identity.record_kind != "tombstone" or replacement is not None:
                diagnostics.append(f"LEDGER-ACTION-REPLACEMENT:{label}")
        else:
            diagnostics.append(f"LEDGER-ACTION:{label}")
        if identity is not None and identity.change_id is not None:
            change_leaves.setdefault(identity.change_id, set()).add(identity.record_kind or "")
        if identity is not None and identity.record_kind == "tombstone":
            stage = stable_path.split("/", 4)[3]
            tombstone_stages[stage] = tombstone_stages.get(stage, 0) + 1
    for path, indices in stable_owners.items():
        if len(indices) > 1:
            diagnostics.append(f"LEDGER-STABLE-PATH-DUPLICATE:{path}")
    for path, indices in legacy_owners.items():
        if len(indices) > 1:
            diagnostics.append(f"LEDGER-LEGACY-PATH-DUPLICATE:{path}")
    for artifact_id, indices in artifact_owners.items():
        if len(indices) > 1:
            diagnostics.append(f"LEDGER-ARTIFACT-ID-DUPLICATE:{artifact_id}")
    if current:
        if len(rows) != 93 or any(
            not isinstance(row, Mapping) or row.get("action") != "moved"
            for row in rows
        ):
            diagnostics.append("LEDGER-CURRENT-CENSUS")
        pair_counts = {
            frozenset({"change-plan", "change-task"}): 0,
            frozenset({"change-plan"}): 0,
            frozenset({"change-task"}): 0,
        }
        for leaves in change_leaves.values():
            key = frozenset(leaves)
            if key not in pair_counts:
                diagnostics.append("LEDGER-CHANGE-GROUP")
            else:
                pair_counts[key] += 1
        if tuple(pair_counts.values()) != (35, 2, 4):
            diagnostics.append("LEDGER-CHANGE-CENSUS")
        if tombstone_stages != {
            "01.requirements": 3,
            "02.architecture": 8,
            "03.specs": 4,
            "05.operations": 2,
        }:
            diagnostics.append("LEDGER-TOMBSTONE-CENSUS")
    return tuple(sorted(set(diagnostics)))


def _work106_mutated_ledger_rows(
    source: Mapping[str, Any], mutation: str
) -> tuple[dict[str, Any], ...]:
    row = dict(source)
    if mutation == "missing-field":
        row.pop("reason")
        return (row,)
    if mutation == "extra-field":
        row["unexpected"] = True
        return (row,)
    if mutation == "bad-legacy-path":
        row["legacy_path"] = "docs/../escape.md"
    elif mutation == "bad-source-commit":
        row["source_commit"] = "A" * 40
    elif mutation == "bad-content-digest":
        row["content_sha256"] = "0" * 63
    elif mutation == "artifact-path-mismatch":
        row["artifact_id"] = "TASK-CHG-0001"
    elif mutation == "kind-path-mismatch":
        row["record_kind"] = "change-task"
    elif mutation == "moved-replacement":
        row["replacement"] = "SPEC-052"
    elif mutation == "bad-replacement-id":
        row["action"] = "replaced"
        row["stable_path"] = "docs/98.archive/tombstones/03.specs/tmb-plan-0001.md"
        row["artifact_id"] = "TMB-PLAN-0001"
        row["record_kind"] = "tombstone"
        row["replacement"] = "not-an-id"
    elif mutation == "duplicate-legacy-path":
        second = dict(row)
        second["stable_path"] = second["stable_path"].replace("chg-0001", "chg-0002")
        second["artifact_id"] = "PLAN-CHG-0002"
        return (row, second)
    elif mutation == "duplicate-stable-path":
        return (row, dict(row))
    elif mutation == "duplicate-artifact-id":
        second = dict(row)
        second["stable_path"] = second["stable_path"].replace("chg-0001", "chg-0002")
        return (row, second)
    else:
        raise AssertionError(f"unknown WORK-106 ledger mutation: {mutation}")
    return (row,)


def _work106_ledger_row(
    ordinal: int, stable_path: str, artifact_id: str, record_kind: str
) -> dict[str, Any]:
    object_id = f"{ordinal:040x}"[-40:]
    return {
        "schema_version": 1,
        "migration_id": "MIG-0001",
        "legacy_path": f"docs/04.execution/legacy/record-{ordinal:03d}.md",
        "stable_path": stable_path,
        "artifact_id": artifact_id,
        "action": "moved",
        "replacement": None,
        "source_commit": object_id,
        "legacy_archive_commit": f"{ordinal + 100:040x}"[-40:],
        "legacy_envelope_blob": f"{ordinal + 200:040x}"[-40:],
        "source_blob": f"{ordinal + 300:040x}"[-40:],
        "content_sha256": f"{ordinal:064x}"[-64:],
        "record_kind": record_kind,
        "reason": "Reviewed current-corpus stable rehome",
    }


def _work106_synthetic_current_ledger() -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    ordinal = 1
    for change in range(1, 42):
        leaves = (
            ("plan", "PLAN", "change-plan"),
            ("task", "TASK", "change-task"),
        )
        if change in {36, 37}:
            leaves = leaves[:1]
        elif change >= 38:
            leaves = leaves[1:]
        for leaf, prefix, kind in leaves:
            path = f"docs/98.archive/changes/chg-{change:04d}-record-{change:04d}/{leaf}.md"
            rows.append(_work106_ledger_row(ordinal, path, f"{prefix}-CHG-{change:04d}", kind))
            ordinal += 1
    tombstone_groups = (
        ("01.requirements", "prd", 3),
        ("02.architecture", "ad", 8),
        ("03.specs", "spec", 4),
        ("05.operations", "guide", 2),
    )
    for stage, kind, count in tombstone_groups:
        for number in range(1, count + 1):
            token = f"{number:04d}"
            path = f"docs/98.archive/tombstones/{stage}/tmb-{kind}-{token}.md"
            rows.append(
                _work106_ledger_row(
                    ordinal, path, f"TMB-{kind.upper()}-{token}", "tombstone"
                )
            )
            ordinal += 1
    return tuple(rows)


def _work106_frontmatter(raw: bytes) -> Mapping[str, Any]:
    if not raw.startswith(b"---\n"):
        return {}
    closing = raw.find(b"\n---\n", 4)
    if closing < 0:
        return {}
    metadata: dict[str, Any] = {}
    for line in raw[4:closing].decode("utf-8").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        metadata[key.strip()] = None if value == "null" else value.strip("'\"")
    return metadata


def _assert_work106_transition_contract(
    root: Path, fixture: Mapping[str, Any], *, terminal: bool
) -> None:
    artifact_cases = fixture.get(WORK106_ARTIFACT_FIXTURE_FIELD)
    ledger_fixture = fixture.get(WORK106_LEDGER_FIXTURE_FIELD)
    if not isinstance(artifact_cases, list) or len(artifact_cases) != 20:
        raise AssertionError("WORK-106 artifact identity fixture differs")
    for case in artifact_cases:
        if not isinstance(case, dict) or not isinstance(case.get("path"), str):
            raise AssertionError("WORK-106 artifact identity fixture differs")
        identity = _work106_derive_artifact_identity(case["path"])
        if identity is None or identity.artifact_id != case.get("artifactId"):
            raise AssertionError("WORK-106 artifact identity fixture differs")
        if identity.change_id != case.get("changeId") or identity.migration_id != case.get("migrationId"):
            raise AssertionError("WORK-106 artifact identity fixture differs")
    if not isinstance(ledger_fixture, dict) or set(ledger_fixture) != {"row", "negativeMutations"}:
        raise AssertionError("WORK-106 migration ledger fixture differs")
    row = ledger_fixture["row"]
    mutations = ledger_fixture["negativeMutations"]
    if _work106_ledger_diagnostics((row,), current=False):
        raise AssertionError("WORK-106 migration ledger positive fixture differs")
    if not isinstance(mutations, list) or any(
        not _work106_ledger_diagnostics(_work106_mutated_ledger_rows(row, mutation), current=False)
        for mutation in mutations
    ):
        raise AssertionError("WORK-106 migration ledger negative fixture differs")
    if _work106_ledger_diagnostics(_work106_synthetic_current_ledger(), current=True):
        raise AssertionError("WORK-106 current 93-row census fixture differs")
    records = tuple(
        (path, _work106_frontmatter(raw))
        for path, raw in _work105_staged_blobs(root)
        if path.endswith(".md")
    )
    diagnostics = _work106_artifact_diagnostics(records, terminal=terminal)
    if diagnostics:
        raise AssertionError("WORK-106 artifact identity: " + ", ".join(diagnostics))


def _fixture_prd_008_immutable_projection(
    fixture: dict[str, Any],
) -> tuple[Any, ...]:
    projection = fixture.get(PROGRAM_LINEAGE_PROJECTION_FIXTURE_FIELD)
    if not isinstance(projection, dict) or set(projection) != {
        "prd",
        "ad",
        "tranches",
        "followUps",
    }:
        raise AssertionError("production PRD-008 lineage fixture shape differs")
    tranches = projection["tranches"]
    follow_ups = projection["followUps"]
    if (
        not isinstance(projection["prd"], str)
        or not isinstance(projection["ad"], str)
        or not isinstance(tranches, list)
        or len(tranches) != 1
        or not isinstance(tranches[0], dict)
        or set(tranches[0]) != {"spec", "order", "decision"}
        or not isinstance(tranches[0]["spec"], str)
        or type(tranches[0]["order"]) is not int
        or not isinstance(tranches[0]["decision"], str)
        or follow_ups != []
    ):
        raise AssertionError("production PRD-008 lineage fixture shape differs")
    return (
        projection["prd"],
        projection["ad"],
        ((tranches[0]["spec"], tranches[0]["order"], tranches[0]["decision"]),),
        (),
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
    try:
        fixture_prd_008_projection = _fixture_prd_008_immutable_projection(fixture)
        _assert_work105_consumer_disposition(root, fixture)
        _assert_work106_transition_contract(root, fixture, terminal=False)
    except AssertionError as exc:
        print(f"FAIL document contract registry self-test: {exc}")
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
        _assert_gemini_native_current_surface_mutation_proofs(root)
        _assert_retired_cloud_sdlc_surface_mutation_proofs()
        _assert_parser_safety()
        _assert_inventory_safety(root)
        parity_case_count = _assert_template_source_mutation_proofs(root, raw_registry)
        _assert_role_inheritance_mutation_proof(root, raw_registry)
        profile_count, template_count = _assert_positive_coverage(
            root, raw_registry, fixture
        )
        registry = validate_registry(root, raw_registry)
        _assert_program_lineage_projection(registry, fixture_prd_008_projection)
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


def _load_migration_tool(root: Path) -> Any:
    path = root / "scripts/migrate-document-work-units.py"
    specification = importlib.util.spec_from_file_location(
        "document_taxonomy_migration_contract", path
    )
    if specification is None or specification.loader is None:
        raise AssertionError("migration tool is unavailable")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def _classify_retired_route_hit(
    raw_registry: Any, path: PurePosixPath
) -> str | None:
    """Return one explicit immutable evidence profile, or fail closed."""
    if not isinstance(raw_registry, dict):
        return None
    policy = raw_registry.get("retiredRouteEvidence")
    if not isinstance(policy, dict) or policy.get("routeSegment") != "04.execution":
        return None
    profiles = policy.get("profiles")
    if not isinstance(profiles, list):
        return None
    path_text = path.as_posix()
    matches: list[str] = []
    for profile in profiles:
        if not isinstance(profile, dict) or set(profile) != {"id", "paths", "routes"}:
            return None
        profile_id = profile.get("id")
        expected_prefix = {
            "stage90/immutable-retired-route-evidence": "docs/90.references/",
            "stage98/immutable-retired-route-evidence": "docs/98.archive/",
        }.get(profile_id)
        if expected_prefix is None or not isinstance(profile.get("paths"), list) or not isinstance(profile.get("routes"), list):
            return None
        selected = path_text in profile["paths"]
        for route in profile["routes"]:
            if not isinstance(route, dict) or set(route) != {"kind", "value"}:
                return None
            kind, value = route.get("kind"), route.get("value")
            if not isinstance(value, str):
                return None
            if kind == "exact":
                selected = selected or path_text == value
            elif kind == "regex" and value.startswith("^") and value.endswith("$"):
                selected = selected or re.fullmatch(value, path_text) is not None
            elif kind != "regex":
                return None
        if selected and path_text.startswith(expected_prefix):
            matches.append(profile_id)
    return matches[0] if len(matches) == 1 else None


def _terminal_route_contract_diagnostics(
    root: Path,
    raw_registry: Any,
    raw_schema: Any,
    retired_route_hits: tuple[PurePosixPath, ...],
) -> tuple[str, ...]:
    diagnostics: list[str] = []
    manifest_path = PurePosixPath("scripts/document-taxonomy-migration.json")
    if (root / manifest_path).exists():
        diagnostics.append("TERMINAL-MIGRATION-FILE")
    profiles = raw_registry.get("profiles", []) if isinstance(raw_registry, dict) else []
    if any(
        isinstance(profile, dict)
        and profile.get("id") == "native/document-migration-manifest"
        for profile in profiles
    ):
        diagnostics.append("TERMINAL-MIGRATION-PROFILE")
    if any(
        isinstance(profile, dict)
        and any(
            isinstance(route, dict)
            and route.get("kind") == "exact"
            and route.get("value") == manifest_path.as_posix()
            for route in profile.get("routes", [])
        )
        for profile in profiles
    ):
        diagnostics.append("TERMINAL-MIGRATION-ROUTE")
    definitions = raw_schema.get("$defs", {}) if isinstance(raw_schema, dict) else {}
    if any(name in definitions for name in ("documentMigrationManifest", "documentMigrationEntry")):
        diagnostics.append("TERMINAL-MIGRATION-SCHEMA")
    for path in retired_route_hits:
        if _classify_retired_route_hit(raw_registry, path) is None:
            diagnostics.append(f"TERMINAL-RETIRED-HIT:{path.as_posix()}")
    return tuple(sorted(set(diagnostics)))


def _assert_route_state(root: Path, registry: Any, requested: str | None) -> None:
    state = requested or registry.route_state
    if requested is not None and requested != registry.route_state:
        raise AssertionError(
            f"route state differs from registry: requested={requested} registry={registry.route_state}"
        )
    manifest_path = PurePosixPath("scripts/document-taxonomy-migration.json")
    if state == "transition":
        profile = classify_path(registry, manifest_path)
        if profile.profile_id != "native/document-migration-manifest":
            raise AssertionError("migration manifest selected the wrong native profile")
        tool = _load_migration_tool(root)
        document = tool.load_manifest_document(root / manifest_path)
        if document.source_commit != tool.EXPECTED_SOURCE_COMMIT:
            raise AssertionError("migration manifest source commit is not the reviewed base")
        entries = document.entries
        diagnostics = tool.validate_manifest(root, entries, document.source_commit)
        if diagnostics:
            raise AssertionError("migration manifest invalid: " + ", ".join(diagnostics))
        tool.validate_counts(
            move_count=sum(row["disposition"] == "move-current" for row in entries),
            archive_count=sum(row["disposition"] == "archive-unique" for row in entries),
            source_count=len(entries),
        )
    elif state == "terminal":
        raw_registry = load_json_file(root / REGISTRY_PATH)
        raw_schema = load_json_file(root / SCHEMA_PATH, diagnostic_path=SCHEMA_PATH)
        token = "docs/" + raw_registry["retiredRouteEvidence"]["routeSegment"]
        result = subprocess.run(
            ["git", "grep", "-Il", "-F", "--", token],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode not in {0, 1}:
            raise AssertionError("terminal retired-route scan failed")
        hits = tuple(PurePosixPath(path) for path in result.stdout.splitlines())
        diagnostics = _terminal_route_contract_diagnostics(
            root, raw_registry, raw_schema, hits
        )
        if diagnostics:
            raise AssertionError(
                "terminal route contract failed: " + ", ".join(diagnostics)
            )


def main() -> int:
    args = _parse_args()
    try:
        root = _assert_repository_root_directory(args.root)
    except AssertionError as exc:
        print(f"FAIL document contract registry: {exc}")
        return 1
    if args.self_test:
        return _self_test(root)

    try:
        registry = load_registry(root)
        fixture = _load_json(root / FIXTURE_PATH)
        _assert_work105_consumer_disposition(root, fixture)
        _assert_work106_transition_contract(
            root,
            fixture,
            terminal=(args.route_state or registry.route_state) == "terminal",
        )
        _assert_route_state(root, registry, args.route_state)
        _assert_template_source_parity(registry)
        _assert_gemini_native_current_surface(root)
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
