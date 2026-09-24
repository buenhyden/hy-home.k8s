---
title: "Argo Rollouts, Notifications & Headlamp Operations Policy"
version: "1.0.7"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "operations"
artifact_id: "POL-0004"
---

# Argo Rollouts, Notifications & Headlamp Operations Policy

## Overview

이 문서는 Argo Rollouts(점진적 배포), Argo Notifications(Slack 알림), Headlamp(클러스터 UI) 운영 통제 기준을 정의한다.

## Policy Scope

- Argo Rollouts — `argo-rollouts` namespace
- Argo Notifications (ArgoCD 내장 컨트롤러) — `argocd` namespace
- Headlamp — `headlamp` namespace

chart 버전은 각 Application manifest의 `targetRevision`이 소유하며 이 정책은
버전을 복제하지 않는다.

## Applies To

- **Systems**: `gitops/apps/root/platform-rollouts-app.yaml`, `gitops/apps/root/platform-headlamp-app.yaml`, `gitops/platform/argocd/argocd-notifications-*`
- **Agents**: 운영 자동화 에이전트
- **Environments**: Linux server local cluster

## Controls

### Argo Rollouts

- **Required**:
  - Rollouts Controller namespace: `argo-rollouts` 고정
  - Rollouts Dashboard 항상 활성화 (`dashboard.enabled: true`)
  - canary 단계는 AnalysisTemplate으로 gate한다. 단계 사이 pause는 앱별로 timed pause(`pause: {duration: ...}`) 또는 수동 pause(`pause: {}`)를 선택하며, 플랫폼이 자동 promotion을 강제하지 않는다 (ADR-0011)
  - Analysis 결과 무시(`skipAnalysis: true`)는 플랫폼 오너 승인 필요
  - CRD 설치: `installCRDs: true` 유지
  - Rollouts Dashboard는 `rollouts.hy-k8s.home.arpa` + ingress-nginx + TLS 유지
- **Allowed**:
  - 수동 Rollout promotion은 [Rollouts/Notifications/Headlamp 런북](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)의 승인/증적 절차로 실행
  - canary/blue-green 전략 선택
  - Prometheus AnalysisTemplate 정의 (`https://prometheus.hy.home.arpa`, `apps/prometheus-api-auth`의 Basic Auth header, controller의 `hy-home-root-ca` 신뢰; ADR-0046)
- **Disallowed**:
  - `argo-rollouts` namespace에 Rollouts 외 워크로드 배치
  - `skipAnalysis: true` 임의 사용

### Argo Notifications

- **Required**:
  - Slack token: Vault `secret/platform/notifications.slack_token` → ESO → `argocd-notifications-secret`
  - templates/triggers: `argocd-notifications-cm` (GitOps 관리)
  - `defaultTriggers`: `on-health-degraded`, `on-sync-failed`; 기본 수신자
    `slack:hy-home-alerts` 구독은 `argocd-notifications-cm`이 소유한다
  - 앱별 opt-in: annotation `notifications.argoproj.io/subscribe.<trigger>.slack: <channel>`
- **Allowed**:
  - 앱 annotation으로 개별 채널 지정
  - template 추가 (GitOps PR 통해)
- **Disallowed**:
  - `argocd-notifications-secret`에 webhook URL 평문 커밋
  - ArgoCD chart의 notifications controller 비활성화(`notifications.enabled: false`) 임의 적용 (Rollouts chart의 별도 값과 무관)

### Headlamp

- **Required**:
  - Headlamp namespace: `headlamp` 고정
  - Ingress hostname: `headlamp.hy-k8s.home.arpa`
  - TLS Secret: `headlamp-tls` (cert-manager `mkcert-ca-issuer` 자동 발급) # pragma: allowlist secret
  - k8s router 경로는 [POL-0001](./0001-k8s-gitops-operations-policy.md)의 ingress 통제를 따른다
- **Allowed**:
  - ServiceAccount Token 방식 인증 (로컬 플랫폼 기본)
  - Headlamp 플러그인 설치 (검토 후)
- **Disallowed**:
  - 대체된 클러스터 UI 재설치 (ADR-0014의 Headlamp 계약과 충돌)

## Exceptions

- Rollouts analysis skip, notifications disablement, or Headlamp authentication changes require platform owner approval and a linked PR.
- Live cluster changes follow the shared exception in [POL-0001](./0001-k8s-gitops-operations-policy.md#exceptions).

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Argo Rollouts | Controller/dashboard pods are running and Rollout CRDs/list output is available | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Argo Notifications | Controller is running, ESO-backed secret exists, and Slack send/error logs are reviewed without committing token values | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Headlamp and k8s router | Headlamp pods/ingress/TLS are healthy and `headlamp`/`rollouts` hostnames return expected HTTP status through the k8s router | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## Traceability

- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Rollouts Spec**: `SPEC-0004` (retained; reach it through the Archive index)
- **Notifications Spec**: `SPEC-0005` (retained; reach it through the Archive index)
- **Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — SPEC-0004 is retained in `completed/` under ADR-0040 and reached through the Archive index, so no eligible upstream document carries a reciprocal link | Platform Owner for promotion approval, analysis exceptions, CRDs, dashboard, and rollback evidence | Argo Rollouts chart values, Rollout resources, AnalysisTemplate review, dashboard ingress/TLS, and runbook evidence |
| N/A — SPEC-0005 is retained in `completed/` under ADR-0040 and reached through the Archive index, so no eligible upstream document carries a reciprocal link | Platform Owner for subscription policy; secret owner for the Slack credential path | Vault-to-ESO secret contract, notifications ConfigMap and annotations, controller logs, and plaintext-secret gates |
