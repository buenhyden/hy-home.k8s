"""Pure finite manifest shared by ARWB-003 archive and lifecycle gates."""

from __future__ import annotations


CUTOVER_BASE_COMMIT = (
    "f8a54ddab23e8301fca3caa9f43d54fa4064b27a"  # pragma: allowlist secret
)
BASE_REGISTRY_BLOB_OID = (
    "0d9347c8ffa84ba313d0d70b42efb331d6e468c1"  # pragma: allowlist secret
)
PROPOSED_REGISTRY_BLOB_OID = (
    "ed62f1792ba60e9be95d0d93b75d43654df3456f"  # pragma: allowlist secret
)
CUTOVER_PROPOSED_COMMIT = (
    "787b28fe1f2b1fff16d59936ed2a411e04d25db5"  # pragma: allowlist secret
)
BASE_REGISTRY_VERSION = 7
PROPOSED_REGISTRY_VERSION = 8
BASE_REGISTRY_ID = "https://hy-home.k8s/schemas/document-profiles-7.schema.json"
PROPOSED_REGISTRY_ID = "https://hy-home.k8s/schemas/document-profiles-8.schema.json"
LEGACY_ARCHIVE_PROFILE = "content/archive-tombstone"
ARCHIVE_PROFILE = "content/archive"
LEGACY_ARCHIVE_TEMPLATE_PROFILE = "template/content/archive-tombstone"
ARCHIVE_TEMPLATE_PROFILE = "template/content/archive"
LEGACY_ARCHIVE_TEMPLATE = (
    "docs/99.templates/templates/common/archive-tombstone.template.md"
)
ARCHIVE_TEMPLATE = "docs/99.templates/templates/common/archive-record.template.md"

EXPECTED_ARCHIVE_PATHS = (
    "docs/98.archive/01.requirements/2026-03-27-wsl-k3d-argocd-platform.md",
    "docs/98.archive/01.requirements/2026-03-28-wsl2-k3d-argocd-ha-platform.md",
    "docs/98.archive/01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md",
    "docs/98.archive/02.architecture/decisions/0001-k3d-topology-and-network.md",
    "docs/98.archive/02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md",
    "docs/98.archive/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md",
    "docs/98.archive/02.architecture/decisions/0007-kubernetes-dashboard-v3.md",
    "docs/98.archive/02.architecture/decisions/0010-headlamp-replaces-dashboard.md",
    "docs/98.archive/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md",
    "docs/98.archive/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md",
    "docs/98.archive/02.architecture/requirements/0003-platform-expansion-mesh-dashboard.md",
    "docs/98.archive/03.specs/001-wsl-k3d-argocd-platform/spec.md",
    "docs/98.archive/03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md",
    "docs/98.archive/03.specs/003-platform-expansion/spec.md",
    "docs/98.archive/03.specs/007-docs-governance-consistency/spec.md",
    "docs/98.archive/04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md",
    "docs/98.archive/04.execution/plans/2026-03-28-wsl2-k3d-argocd-ha-platform.md",
    "docs/98.archive/04.execution/plans/2026-03-29-platform-expansion.md",
    "docs/98.archive/04.execution/plans/2026-05-09-k3d-agent-first-remediation.md",
    "docs/98.archive/04.execution/plans/2026-05-22-spec-execution-implementation-audit.md",
    "docs/98.archive/04.execution/plans/2026-05-28-docs-governance-consistency.md",
    "docs/98.archive/04.execution/plans/2026-05-30-common-agent-governance-refactoring.md",
    "docs/98.archive/04.execution/tasks/2026-03-27-wsl-k3d-argocd-platform.md",
    "docs/98.archive/04.execution/tasks/2026-03-28-wsl2-k3d-argocd-ha-platform.md",
    "docs/98.archive/04.execution/tasks/2026-03-29-platform-expansion.md",
    "docs/98.archive/04.execution/tasks/2026-05-09-k3d-agent-first-remediation.md",
    "docs/98.archive/04.execution/tasks/2026-05-22-spec-execution-implementation-audit.md",
    "docs/98.archive/04.execution/tasks/2026-05-28-docs-governance-consistency.md",
    "docs/98.archive/04.execution/tasks/2026-05-30-governance-refactoring.md",
    "docs/98.archive/05.operations/guides/0004-headlamp-auth-oidc-guide.md",
    "docs/98.archive/05.operations/runbooks/0005-headlamp-keycloak-runbook.md",
)

EXPECTED_ARCHIVE_RECORDS = len(EXPECTED_ARCHIVE_PATHS)
