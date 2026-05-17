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
  - 수동 `kubectl argo rollouts promote <rollout>` 실행
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
  - K8s Dashboard 재설치 (ADR-0010에 의해 교체됨)

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

```bash
# Rollouts 상태
kubectl -n argo-rollouts get pods
kubectl argo rollouts list rollouts --all-namespaces

# Notifications 상태
kubectl -n argocd get pods | grep notification
kubectl -n argocd logs deploy/argocd-notifications-controller --tail=50 | grep -i 'slack\|error\|sent'

# Headlamp 상태
kubectl -n headlamp get pods,ingress

# Traefik 라우팅 확인
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
curl -ksS -o /dev/null -w '%{http_code}' https://rollouts.127.0.0.1.nip.io/
```

## Review Cadence

- 운영 변경 시 즉시
- 정기 분기 검토

## Related Documents

- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)
