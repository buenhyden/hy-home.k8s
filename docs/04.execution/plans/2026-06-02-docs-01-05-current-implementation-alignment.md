---
title: 'Docs 01-05 Current Implementation Alignment Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Docs 01-05 Current Implementation Alignment Plan

## Overview

This document is the implementation plan for comparing and cleaning up active
documents from `docs/01.requirements` through `docs/05.operations` against the
current repo-backed implementation. The decision basis is the current SSoT in
`gitops/`, `infrastructure/`, `scripts/`, `.github/`, provider/agent
governance, and validation scripts, not merely whether link validation passes.

## Context

The prior current implementation alignment focused on `docs/01-04` and moved
old contracts to `docs/98.archive` Tombstones. This work does not narrow the
scope; it includes `docs/05.operations` and cleans up unimplemented Headlamp
OIDC contracts, stale hook paths, stale CI job wording, and completed-but-draft
Phase evidence against the current implementation.

## Goals & In-Scope

- **Goals**:
  - Ensure active `docs/01-05` does not conflict with the current repo-backed implementation.
  - Move unimplemented Headlamp OIDC/Keycloak documents to `docs/98.archive` metadata-only Tombstones.
  - Set completed Phase 1-4 evidence and README indexes to `done`.
  - Harden the validator and QA docs so `repo-quality-static` catches active stale currentness drift.
- **In Scope**:
  - Adjust active documents in `docs/03.specs`, `docs/04.execution`, and `docs/05.operations`.
  - Extend the `docs/98.archive` 05.operations mirror and stage-level Archive Indexes.
  - Adjust Plans/Tasks READMEs, the progress ledger, governance routing, the QA/CI guide, scripts README, and GitHub ABOUT.
  - Local static validation and targeted semantic scans.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - New Headlamp OIDC, Keycloak, Vault, ESO, ArgoCD, Kubernetes, provider, model, or CI topology implementation.
  - Using live runtime state as the archive decision basis.
  - Adding archive policy to `docs/99.templates/templates/common/reference.template.md`.
- **Out of Scope**:
  - live k3d mutation, ArgoCD sync, Vault unseal/write, ESO secret sync repair, deployment action, external network operation, or secret-value inspection.
  - Private RTK DB, credentials, tokens, private keys, or shell history inspection.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Seal currentness evidence and archive Headlamp OIDC docs | `docs/05.operations/**`, `docs/98.archive/05.operations/**` | REQ-DOC-CUR-001 | Active docs have no Headlamp OIDC desired-state claims for missing repo artifacts. |
| PLN-002 | Archive superseded governance cleanup snapshot | superseded Spec/Plan/Task, `docs/98.archive/**` | REQ-DOC-CUR-002 | Active indexes remove superseded-only docs and archive index lists Tombstones. |
| PLN-003 | Normalize active current contracts | `docs/03.specs/006-*`, old Plan/Task command evidence, HA guide/policy, QA/CI docs | REQ-DOC-CUR-003 | Active docs use shared hook path, current CI job names, and local multi-node baseline wording. |
| PLN-004 | Harden governance and QA/static gates | `scripts/validate-repo-quality-gates.sh`, `scripts/README.md`, `.github/ABOUT.md`, operations QA guide | REQ-DOC-CUR-004 | Repo quality gate rejects direct Tombstone links, stale OIDC contract, stale hook path, and stale CI job wording. |
| PLN-005 | Sync Plan/Task indexes and progress | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, `progress.md` | REQ-DOC-CUR-005 | README rows match moved/added documents and progress records evidence. |
| PLN-006 | Run local static verification | repo validators | REQ-DOC-CUR-006 | Required static commands pass or limitations are recorded without live-readiness claims. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DOC-001 | Diff hygiene | Check whitespace and conflict markers | `git diff --check` | Exit 0. |
| VAL-DOC-002 | Generated reference | Confirm LLM Wiki index freshness | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-DOC-003 | Repository currentness | Run governance/template/currentness gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-DOC-004 | GitOps structure | Confirm GitOps repo shape remains valid | `bash scripts/validate-gitops-structure.sh` | PASS. |
| VAL-DOC-005 | Manifest syntax | Validate Kubernetes YAML syntax and optional lint | `bash scripts/validate-k8s-manifests.sh .` | PASS or optional tool skip recorded. |
| VAL-DOC-006 | Secret handling | Scan plaintext secret patterns | `bash scripts/check-secret-handling.sh .` | PASS. |
| VAL-DOC-007 | Policy gates | Run policy validation fallback or Conftest | `bash scripts/validate-policy-gates.sh .` | PASS. |
| VAL-DOC-008 | Semantic stale scan | Scan active docs for archived Headlamp OIDC, stale hook path, stale CI job, and moved doc links | targeted `rg` commands | No active hits outside validator sentinels. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Active docs lose scope when old docs are archived | High | Keep current replacement links and archive only missing/superseded contracts. |
| Historical execution docs are treated as current commands | Medium | Rewrite active command surfaces to current shared hook and CI topology wording. |
| Tombstone body preserves old implementation details | Medium | Keep Tombstones metadata-only and validate line count/required phrases. |
| Repo-static pass is mistaken for runtime readiness | High | State live k3d/ArgoCD/Vault/ESO/deployment checks as out of scope unless separately approved and run. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: local static verification commands and targeted semantic scans.
- **Sandbox / Canary Rollout**: not applicable; docs and static validator changes only.
- **Human Approval Gate**: already granted for docs/governance/QA/CI script hardening; required again for live runtime mutation, secret inspection, deployment, or CI topology changes.
- **Rollback Trigger**: failing repo quality gate, broken README indexes, or active docs losing current replacement coverage.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Headlamp OIDC/Keycloak docs moved to metadata-only Tombstones.
- [x] Superseded 007 governance consistency snapshot moved to archive.
- [x] Active README indexes and related docs point to current replacements, not individual Tombstones.
- [x] Active docs use current shared hook path and current CI topology wording.
- [x] Phase 1-4 completed evidence is marked `done`.
- [x] Validator and QA docs enforce stale currentness gates.
- [x] Local static verification is executed and results are recorded.

## Traceability

- **Current Platform Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Harness Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Current Implementation Alignment Plan**: [./2026-06-02-current-implementation-docs-alignment.md](./2026-06-02-current-implementation-docs-alignment.md)
- **Tasks**: [../tasks/2026-06-02-docs-01-05-current-implementation-alignment.md](../tasks/2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Plan Template**: [../../99.templates/templates/sdlc/execution/plan.template.md](../../99.templates/templates/sdlc/execution/plan.template.md)
