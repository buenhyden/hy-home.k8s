---
title: 'Argo Rollouts Progressive Delivery Backfill Plan'
type: plan
status: done
owner: platform
updated: 2026-05-21
---

# Argo Rollouts Progressive Delivery Backfill Plan

## Overview (KR)

이 문서는 이미 저장소에 존재하는 Argo Rollouts 실행계약을 PRD/ARD/ADR/Spec/Task 체인에 연결하기 위한 backfill 실행 계획서다.
런타임 변경 없이 문서 추적성과 정적 검증 기준을 보완한다.

## Context

`platform-rollouts` Application, AppProject 권한, Rollouts Dashboard route, metrics NodePort, reference workload는 이미 GitOps 문서와 manifest에 존재한다.
하지만 Rollouts PRD와 ADR을 잇는 ARD/Spec/Plan/Task 문서가 없어서 `03.specs` 단계에서 구현 계약을 찾기 어렵다.

## Goals & In-Scope

- **Goals**:
  - Rollouts current contract를 ARD/Spec/Plan/Task 체인으로 보강한다.
  - Rollouts chart notifications와 ArgoCD Notifications의 소유권을 분리한다.
  - 검증 명령과 운영 문서 링크를 한 경로에서 추적 가능하게 만든다.
- **In Scope**:
  - 문서 backfill과 README index 갱신
  - `platform-rollouts` current contract 설명
  - 정적 검증과 live validation boundary 명시

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 신규 Rollouts 기능 추가
  - 자동 promotion 정책 변경
  - Rollouts chart notifications 활성화
- **Out of Scope**:
  - live cluster mutation
  - workload별 Rollout migration
  - Slack credential bootstrap

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Rollouts ARD 작성 | `docs/02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md` | REQ-PRD-FUN-01 | ARD가 PRD/ADR/Spec/Plan 링크를 포함 |
| PLN-002 | Rollouts Spec 작성 | `docs/03.specs/004-argo-rollouts-progressive-delivery/spec.md` | REQ-PRD-FUN-01..06 | Spec heading/template gate 통과 |
| PLN-003 | Rollouts Task 작성 | `docs/04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md` | REQ-PRD-MET-01..04 | Task가 validation evidence를 정의 |
| PLN-004 | 역링크와 README index 갱신 | PRD, ADR, README, operations docs | REQ-PRD-FUN-04 | stale gap text 없음 |
| PLN-005 | 검증 실행 | validation scripts | REQ-PRD-MET-04 | 모든 정적 검증 PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | GitOps | Rollouts Application and kustomization structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-003 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-004 | Contract | platform static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|이번 PRD 정비에서 생성하지 않음" docs/01.requirements` | no matches |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Backfill 문서가 future implementation으로 오해됨 | High | status를 active로 두고 current-contract backfill 문구를 상단에 명시 |
| Rollouts chart notifications를 잘못 활성화 | High | Spec에서 chart notifications disabled와 ArgoCD Notifications ownership을 분리 |
| Live validation이 정적 검증처럼 실행됨 | Medium | live `kubectl`/`curl`은 runbook evidence로 분리 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo quality, GitOps structure, manifest syntax, static contract checks pass.
- **Sandbox / Canary Rollout**: Not applicable for docs-only backfill.
- **Human Approval Gate**: Live promotion, abort, undo, or cluster mutation requires explicit human approval.
- **Rollback Trigger**: validation failure or stale current/historical contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] ARD, Spec, Plan, Task chain exists for Rollouts.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Rollouts.
- [x] Verification commands are documented for execution.

## Related Documents

- **PRD**: [`../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md`](../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md)
- **ARD**: [`../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md`](../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **ADR**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **Tasks**: [`../tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](../tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
