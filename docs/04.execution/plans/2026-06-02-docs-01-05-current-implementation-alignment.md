---
title: 'Docs 01-05 Current Implementation Alignment Plan'
type: plan
status: done
owner: platform
updated: 2026-06-02
---

# Docs 01-05 Current Implementation Alignment Plan

## Overview (KR)

이 문서는 `docs/01.requirements`부터 `docs/05.operations`까지 active 문서를 현재 repo-backed 구현과 대조해 정리하는 실행 계획서다.
판정 기준은 링크 검증 통과 여부가 아니라 `gitops/`, `infrastructure/`, `scripts/`, `.github/`, provider/agent governance, validation scripts의 현재 SSoT다.

## Context

기존 current implementation alignment는 `docs/01-04` 중심으로 old contract를 `docs/98.archive` Tombstone으로 이동했다.
이번 작업은 범위를 축소하지 않고 `docs/05.operations`까지 포함해 Headlamp OIDC 미구현 계약, stale hook path, stale CI job wording, completed-but-draft Phase evidence를 현재 구현 기준으로 정리한다.

## Goals & In-Scope

- **Goals**:
  - Active `docs/01-05`가 현재 repo-backed 구현과 상충하지 않게 한다.
  - 미구현 Headlamp OIDC/Keycloak 문서는 `docs/98.archive` metadata-only Tombstone으로 이동한다.
  - Completed Phase 1-4 evidence와 README indexes를 `done` 상태로 정리한다.
  - `repo-quality-static`이 active stale currentness drift를 잡도록 validator와 QA 문서를 보강한다.
- **In Scope**:
  - `docs/03.specs`, `docs/04.execution`, `docs/05.operations` active 문서 보정.
  - `docs/98.archive` 05.operations mirror와 stage별 Archive Index 확장.
  - Plans/Tasks README, progress ledger, governance routing, QA/CI guide, scripts README, GitHub ABOUT 보정.
  - Local static validation and targeted semantic scans.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - New Headlamp OIDC, Keycloak, Vault, ESO, ArgoCD, Kubernetes, provider, model, or CI topology implementation.
  - Live runtime state를 archive 판정 기준으로 사용.
  - `docs/99.templates/reference.template.md`에 archive policy 추가.
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

## Agent Rollout & Evaluation Gates (If Applicable)

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

## Related Documents

- **Current Platform Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Harness Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Current Implementation Alignment Plan**: [./2026-06-02-current-implementation-docs-alignment.md](./2026-06-02-current-implementation-docs-alignment.md)
- **Tasks**: [../tasks/2026-06-02-docs-01-05-current-implementation-alignment.md](../tasks/2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Plan Template**: [../../99.templates/plan.template.md](../../99.templates/plan.template.md)
