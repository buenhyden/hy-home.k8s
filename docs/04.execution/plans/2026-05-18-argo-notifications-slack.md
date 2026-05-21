---
title: 'Argo Notifications Slack Backfill Plan'
type: plan
status: complete
owner: platform-team
updated: 2026-05-21
---

# Argo Notifications Slack Backfill Plan

## Overview (KR)

이 문서는 이미 저장소에 존재하는 ArgoCD Notifications Slack 실행계약을 PRD/ARD/ADR/Spec/Task 체인에 연결하기 위한 backfill 실행 계획서다.
런타임 변경 없이 문서 추적성, Secret 경계, 검증 기준을 보완한다.

## Context

ArgoCD Notifications는 `infrastructure/argocd/values-local.yaml`에서 활성화되어 있고, ConfigMap과 ExternalSecret은 `gitops/platform/argocd/`에서 GitOps로 관리된다.
하지만 Notifications PRD와 ADR을 잇는 ARD/Spec/Plan/Task 문서가 없어 credential boundary와 검증 경로가 `03.specs`에서 추적되지 않는다.

## Goals & In-Scope

- **Goals**:
  - Notifications current contract를 ARD/Spec/Plan/Task 체인으로 보강한다.
  - Slack token의 Vault/ESO 보안 경계를 명확히 한다.
  - ArgoCD Notifications와 Rollouts chart notifications를 분리한다.
- **In Scope**:
  - 문서 backfill과 README index 갱신
  - Notifications ConfigMap/ExternalSecret current contract 설명
  - 정적 검증과 live Slack validation boundary 명시

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Slack token 발급 또는 Vault write
  - 새 알림 채널 추가
  - Rollouts chart notifications 활성화
- **Out of Scope**:
  - live Slack notification test
  - Slack workspace/channel 운영
  - Alertmanager/PagerDuty/Email integration

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Notifications ARD 작성 | `docs/02.architecture/requirements/0005-argo-notifications-slack.md` | REQ-PRD-FUN-01..06 | ARD가 PRD/ADR/Spec/Plan 링크를 포함 |
| PLN-002 | Notifications Spec 작성 | `docs/03.specs/005-argo-notifications-slack/spec.md` | REQ-PRD-FUN-01..06 | Spec heading/template gate 통과 |
| PLN-003 | Notifications Task 작성 | `docs/04.execution/tasks/2026-05-18-argo-notifications-slack.md` | REQ-PRD-MET-01..05 | Task가 validation evidence를 정의 |
| PLN-004 | 역링크와 README index 갱신 | PRD, ADR, README, operations docs | REQ-PRD-FUN-02 | stale gap text 없음 |
| PLN-005 | 검증 실행 | validation scripts | REQ-PRD-MET-02 | secret scan과 static contract PASS |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Secret | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-003 | Contract | static notification contract | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|이번 PRD 정비에서 생성하지 않음" docs/01.requirements` | no matches |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Slack token 노출 | High | docs/manifests only reference Vault/ESO keys; run secret scan |
| Rollouts chart notifications와 혼동 | High | Spec에서 `rolloutsChartNotifications.enabled: false`를 명시 |
| Live Slack test를 자동 검증으로 오해 | Medium | live validation은 human-approved secret 준비 후 runbook에서만 수행 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo quality, secret scan, manifest syntax, static contract checks pass.
- **Sandbox / Canary Rollout**: Not applicable for docs-only backfill.
- **Human Approval Gate**: Vault write, Slack token read, live Slack send test require explicit human approval.
- **Rollback Trigger**: validation failure or credential boundary contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] ARD, Spec, Plan, Task chain exists for Notifications.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Notifications.
- [x] Verification commands are documented for execution.

## Related Documents

- **PRD**: [`../../01.requirements/2026-05-17-argo-notifications-slack.md`](../../01.requirements/2026-05-17-argo-notifications-slack.md)
- **ARD**: [`../../02.architecture/requirements/0005-argo-notifications-slack.md`](../../02.architecture/requirements/0005-argo-notifications-slack.md)
- **Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **ADR**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Tasks**: [`../tasks/2026-05-18-argo-notifications-slack.md`](../tasks/2026-05-18-argo-notifications-slack.md)
