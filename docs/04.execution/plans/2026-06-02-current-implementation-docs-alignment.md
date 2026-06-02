---
title: 'Current Implementation Docs Alignment Plan'
type: plan
status: done
owner: platform
updated: 2026-06-02
---

# Current Implementation Docs Alignment Plan

## Overview (KR)

이 문서는 `docs/01-04`를 현재 repo-backed 구현과 맞추고, old 문서를 `98.archive` Tombstone으로 이동한 초기 실행 계획서다.
`docs/05.operations`까지 확장한 후속 currentness pass는 [Docs 01-05 Current Implementation Alignment Plan](./2026-06-02-docs-01-05-current-implementation-alignment.md)이 소유한다.

## Context

Current implementation is represented by `gitops/`, `infrastructure/`, `scripts/`, README indexes, and static contract evidence.
Old active-stage documents contained conflicting implementation contracts, so the docs model now uses current replacement docs plus archive Tombstones.

## Goals & In-Scope

- **Goals**:
  - Active `docs/01-04` describe current implementation only.
  - Old conflicting documents move to `docs/98.archive` with Tombstone bodies.
  - Governance and quality gates enforce the new archive policy.
- **In Scope**:
  - Current PRD/ARD/ADR/Spec chain.
  - Current cleanup Plan/Task evidence.
  - Archive index, Tombstone template, stage README updates.
  - Repo quality and static GitOps checks.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Live cluster mutation.
  - External service runtime changes.
  - Secret value inspection.
- **Out of Scope**:
  - Cloud example redesign.
  - Full rewrite of operations runbooks unrelated to archived links.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Add current baseline PRD/ARD/ADR/Spec chain | `docs/01-03` | REQ-PRD-FUN-01..07 | Template and link validation pass |
| PLN-002 | Add `98.archive` Tombstone stage | `docs/98.archive`, `docs/99.templates` | REQ-PRD-FUN-07 | Archive template coverage pass |
| PLN-003 | Move old conflicting docs to Tombstones | `docs/01-04`, `docs/98.archive` | REQ-PRD-FUN-07 | Active stale-contract scan pass |
| PLN-004 | Update README indexes and related links | `README.md`, `docs/**/README.md`, related docs | REQ-PRD-MET-04 | Link validation pass |
| PLN-005 | Harden quality gate and QA surfaces | `scripts/validate-repo-quality-gates.sh`, governance hooks, PR checklist | REQ-PRD-MET-04 | Repo quality gate pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Repo quality gate | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Static | Current implementation contract | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-003 | Static | GitOps hierarchy | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-004 | Static | Kubernetes manifest syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-005 | CI fallback | Secret and policy gates | `bash scripts/check-secret-handling.sh .`; `bash scripts/validate-policy-gates.sh .` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Scope shrinks when old docs are archived | High | Add current baseline PRD/ARD/ADR/Spec before removing old docs |
| Active docs link directly to Tombstones | Medium | Use archive README as Index Only link |
| Old body text survives in archive | Medium | Enforce Tombstone heading and stale-body checks |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo quality and static GitOps checks must pass.
- **Sandbox / Canary Rollout**: not applicable; docs/static-only change.
- **Human Approval Gate**: required for any live cluster or external service action.
- **Rollback Trigger**: failing quality gate or broken replacement chain.
- **Prompt / Model Promotion Criteria**: not applicable.

## Completion Criteria

- [x] Current baseline docs are active.
- [x] Old conflicting docs are Tombstones.
- [x] README indexes and related links are updated.
- [x] Verification passed.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-02-current-local-gitops-platform.md](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- **ARD**: [../../02.architecture/requirements/0007-current-local-gitops-platform.md](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- **Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **ADR**: [../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Tasks**: [../tasks/2026-06-02-current-implementation-docs-alignment.md](../tasks/2026-06-02-current-implementation-docs-alignment.md)
- **Follow-up Plan**: [./2026-06-02-docs-01-05-current-implementation-alignment.md](./2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
