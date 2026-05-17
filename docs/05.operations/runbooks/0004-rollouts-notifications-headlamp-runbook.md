---
title: 'Argo Rollouts, Notifications & Headlamp Runbook'
type: runbook
status: active
owner: platform
updated: 2026-05-09
---

# Argo Rollouts, Notifications & Headlamp Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스 및 부트스트랩`

## Overview (KR)

이 런북은 Argo Rollouts, Argo Notifications(Slack), Headlamp의 초기 부트스트랩, 복구, 검증 절차를 제공한다.

## Purpose

Rollouts, Notifications, Headlamp 운영 상태를 빠르게 확인하고, 초기 부트스트랩 또는 장애 복구 시 필요한 순서를 제공한다.

## Canonical References

- [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)

## When to Use

- Rollouts Controller가 기동하지 않거나 CRD가 없을 때
- Notifications Slack 알림이 전달되지 않을 때
- Headlamp에 접근 불가 (404/502) 상황
- 초기 플랫폼 부트스트랩 후 신규 컴포넌트 검증 시

---

## Procedure or Checklist

아래 절차는 Notifications secret 준비, controller 상태 확인, Rollouts 상태 확인, Headlamp 및 Rollouts Dashboard 접근 검증 순서로 수행한다.

## Procedure 1: Vault Notifications Secret 준비 (최초 1회)

```bash
# Slack Bot Token 준비 후 Vault에 저장
export VAULT_TOKEN='<redacted>'
# external secret operation; human-approved bootstrap only
vault kv put secret/platform/notifications \
  slack_token="xoxb-your-slack-bot-token"

# 확인
vault kv get secret/platform/notifications
```

> **주의**: token은 반드시 Vault에 저장. 평문 커밋 금지.

---

## Procedure 2: ArgoCD Notifications 활성화 확인

```bash
# notifications controller pod 확인
kubectl -n argocd get pods | grep notification

# notifications-cm 확인
kubectl -n argocd get cm argocd-notifications-cm -o yaml | head -20

# notifications-secret (ESO 동기화 확인)
kubectl -n argocd get secret argocd-notifications-secret 2>/dev/null && echo "OK" || echo "Missing"

# notifications controller 로그 (Slack 전송 확인)
kubectl -n argocd logs deploy/argocd-notifications-controller --tail=100 | grep -i 'slack\|sent\|error'
```

### 복구: ESO 재동기화

```bash
kubectl -n argocd annotate externalsecret argocd-notifications-secret \
  force-sync=$(date +%s) --overwrite
```

---

## Procedure 3: Argo Rollouts 상태 확인

```bash
# Rollouts controller 및 dashboard pod 확인
kubectl -n argo-rollouts get pods

# CRD 확인
kubectl get crd | grep argoproj.io

# 전체 Rollout 목록
kubectl argo rollouts list rollouts --all-namespaces

# Rollout 상세 상태
kubectl argo rollouts get rollout <name> -n <namespace> --watch
```

### Rollout 수동 프로모션

```bash
# canary 다음 단계로 진행
kubectl argo rollouts promote <rollout-name> -n <namespace>

# 전체 즉시 프로모션
kubectl argo rollouts promote <rollout-name> -n <namespace> --full

# 롤백 (이전 버전으로)
kubectl argo rollouts undo <rollout-name> -n <namespace>
```

---

## Procedure 4: Headlamp 접근 검증

```bash
# Pod 및 Ingress 상태 확인
kubectl -n headlamp get pods,ingress,svc

# TLS Secret 확인 (cert-manager 발급)
kubectl -n headlamp get certificate headlamp-tls 2>/dev/null || \
kubectl -n headlamp get secret headlamp-tls 2>/dev/null

# HTTP 응답 확인
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
```

### 복구: Headlamp 재시작

```bash
kubectl -n headlamp rollout restart deployment headlamp
```

### Traefik artifact 적용 확인

```bash
# Traefik 컨테이너에서 headlamp-k3d 라우터 상태 확인
# (Traefik 관리 UI 또는 API에서 확인)
# Kubernetes 사이드에서는 ingress 상태만 확인 가능
kubectl -n headlamp get ingress headlamp -o yaml
```

---

## Procedure 5: Rollouts Dashboard 접근 검증

```bash
# Pod 및 Ingress 상태
kubectl -n argo-rollouts get pods
kubectl -n argo-rollouts get ingress

# HTTP 응답 확인
curl -ksS -o /dev/null -w '%{http_code}' https://rollouts.127.0.0.1.nip.io/
```

---

## Verification Steps

- [ ] `argo-rollouts` namespace에 controller + dashboard Pod Running
- [ ] `argo-rollouts` Rollout CRD 존재
- [ ] `argocd-notifications-controller` Pod Running
- [ ] `argocd-notifications-secret` ESO 동기화 완료
- [ ] `argocd-notifications-cm` ConfigMap 존재
- [ ] `headlamp` namespace에 Pod Running, Ingress Ready
- [ ] `https://headlamp.127.0.0.1.nip.io/` → 200 응답
- [ ] `https://rollouts.127.0.0.1.nip.io/` → 200 응답
- [ ] Traefik artifact (`headlamp-k3d.yaml`, `rollouts-k3d.yaml`) 외부 Traefik 레포에 적용됨

## Observability and Evidence Sources

- **Signals**: Rollouts controller readiness, notification controller logs, Headlamp ingress/TLS status, Traefik HTTP response codes.
- **Evidence to Capture**: pod status output, Slack send/error log snippets, HTTP response codes, ArgoCD Application health.

## Safe Rollback or Recovery Procedure

- Rollout 문제가 발생하면 `kubectl argo rollouts undo`로 workload 단위 rollback을 수행한다.
- Notifications 문제가 발생하면 Vault secret과 ExternalSecret 동기화 상태를 먼저 복구하고 controller 재시작은 마지막 수단으로 둔다.
- Headlamp 접근 실패 시 Ingress/TLS/Traefik artifact를 확인하고, Dashboard 재도입이 아니라 Headlamp 경로를 복구한다.

## Troubleshooting Signatures

- `Error syncing application: slack token is empty` → Vault secret 미등록 또는 ESO 미동기화
- Headlamp 404 → ingress-nginx 미시작 또는 TLS secret 미발급
- Rollouts `CRD not found` → `installCRDs: true` 확인 또는 ArgoCD sync wave 순서 문제
- Rollouts Dashboard 502 → dashboard Pod 미기동, service port 3100 확인

## Related Documents

- **Operations**: [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Rollouts Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Notifications Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **Rollouts Task**: [`../../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](../../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Notifications Task**: [`../../04.execution/tasks/2026-05-18-argo-notifications-slack.md`](../../04.execution/tasks/2026-05-18-argo-notifications-slack.md)
