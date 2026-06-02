---
title: 'Argo Rollouts, Notifications & Headlamp Operations Policy'
type: policy
status: active
owner: platform
updated: 2026-05-21
---

# Argo Rollouts, Notifications & Headlamp Operations Policy

## Overview (KR)

이 문서는 Argo Rollouts(점진적 배포), Argo Notifications(Slack 알림), Headlamp(클러스터 UI) 운영 통제 기준을 정의한다.

## Policy Scope

- Argo Rollouts v1.9.0 (chart 2.40.9) — `argo-rollouts` namespace
- Argo Notifications (ArgoCD 내장 컨트롤러) — `argocd` namespace
- Headlamp v0.41.0 — `headlamp` namespace
- Traefik 외부 artifact — `traefik/` (별도 Traefik 레포 적용)

## Applies To

- **Systems**: `gitops/apps/root/platform-rollouts-app.yaml`, `gitops/apps/root/platform-headlamp-app.yaml`, `gitops/platform/argocd/argocd-notifications-*`, `traefik/`
- **Agents**: 운영 자동화 에이전트
- **Environments**: WSL2 local cluster

## Controls

### Argo Rollouts

- **Required**:
  - Rollouts Controller namespace: `argo-rollouts` 고정
  - Rollouts Dashboard 항상 활성화 (`dashboard.enabled: true`)
  - 기본 promotion 전략: 수동 (`pause: {}`) — 자동 프로모션 승인 없이 활성화 금지
  - Analysis 결과 무시(`skipAnalysis: true`)는 플랫폼 오너 승인 필요
  - CRD 설치: `installCRDs: true` 유지
  - Rollouts Dashboard는 `rollouts.127.0.0.1.nip.io` + ingress-nginx + TLS 유지
- **Allowed**:
  - 수동 Rollout promotion은 [Rollouts/Notifications/Headlamp 런북](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)의 승인/증적 절차로 실행
  - canary/blue-green 전략 선택
  - Prometheus AnalysisTemplate 정의 (외부 Prometheus `172.18.0.10:9090` 활용)
- **Disallowed**:
  - `argo-rollouts` namespace에 Rollouts 외 워크로드 배치
  - `skipAnalysis: true` 임의 사용

### Argo Notifications

- **Required**:
  - Slack token: Vault `secret/platform/notifications.slack_token` → ESO → `argocd-notifications-secret`
  - templates/triggers: `argocd-notifications-cm` (GitOps 관리)
  - Default subscriptions: `on-health-degraded`, `on-sync-failed`
  - 앱별 opt-in: annotation `notifications.argoproj.io/subscribe.<trigger>.slack: <channel>`
- **Allowed**:
  - 앱 annotation으로 개별 채널 지정
  - template 추가 (GitOps PR 통해)
- **Disallowed**:
  - `argocd-notifications-secret`에 webhook URL 평문 커밋
  - notifications controller 비활성화(`notifications.enabled: false`) 임의 적용

### Headlamp

- **Required**:
  - Headlamp namespace: `headlamp` 고정
  - Ingress hostname: `headlamp.127.0.0.1.nip.io`
  - TLS Secret: `headlamp-tls` (cert-manager `mkcert-ca-issuer` 자동 발급) # pragma: allowlist secret
  - Traefik artifact `headlamp-k3d.yaml` 별도 Traefik 레포에 적용 유지
- **Allowed**:
  - ServiceAccount Token 방식 인증 (로컬 플랫폼 기본)
  - Headlamp 플러그인 설치 (검토 후)
- **Disallowed**:
  - 대체된 클러스터 UI 재설치 (ADR-0014의 Headlamp 계약과 충돌)

## Exceptions

- Rollouts analysis skip, notifications disablement, or Headlamp authentication changes require platform owner approval and a linked PR.
- Direct cluster changes are allowed only for human-approved bootstrap or break-glass recovery and must be followed by GitOps state reconciliation.
- Traefik external artifact changes must be reviewed with the matching k8s ingress and TLS contract.

## Traefik 외부 Artifact 관리

- `traefik/kiali-k3d.yaml` — Kiali Traefik 라우터
- `traefik/headlamp-k3d.yaml` — Headlamp Traefik 라우터
- `traefik/rollouts-k3d.yaml` — Rollouts Dashboard Traefik 라우터
- 이 파일들은 별도 Traefik 레포에 수동 적용한다. 자동화 금지.

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Argo Rollouts | Controller/dashboard pods are running and Rollout CRDs/list output is available | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Argo Notifications | Controller is running, ESO-backed secret exists, and Slack send/error logs are reviewed without committing token values | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |
| Headlamp and Traefik | Headlamp pods/ingress/TLS are healthy and `headlamp`/`rollouts` hostnames return expected HTTP status through Traefik | [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md) |

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## AI Agent Policy Section (If Applicable)

이 정책은 인프라 리소스를 직접 관리하며 AI Agent 모델/프롬프트/평가 정책이 별도 적용되지 않는다.
단, Agent가 이 정책 범위의 리소스를 조작할 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Related Documents

- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Rollouts Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Notifications Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **Rollouts Plan**: [`../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Notifications Plan**: [`../../04.execution/plans/2026-05-18-argo-notifications-slack.md`](../../04.execution/plans/2026-05-18-argo-notifications-slack.md)
- **Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)
