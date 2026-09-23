---
title: "Argo Rollouts, Notifications & Headlamp Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0004"
---

# Argo Rollouts, Notifications & Headlamp Runbook

## Overview

이 런북은 Argo Rollouts, Argo Notifications(Slack), Headlamp의 초기 부트스트랩, 복구, 검증 절차를 제공한다.

### Purpose

Rollouts, Notifications, Headlamp 운영 상태를 빠르게 확인하고, 초기 부트스트랩 또는 장애 복구 시 필요한 순서를 제공한다.

## Runbook Type

`bootstrap`

## When to Use

- Rollouts Controller가 기동하지 않거나 CRD가 없을 때
- Notifications Slack 알림이 전달되지 않을 때
- Headlamp에 접근 불가 (401/404/502) 또는 `headlamp-tls` 미발급 상황
- 초기 플랫폼 부트스트랩 후 신규 컴포넌트 검증 시

---

## Procedure or Checklist

아래 절차는 Notifications secret 준비, controller 상태 확인, Rollouts 상태 확인, Headlamp 및 Rollouts Dashboard 접근 검증 순서로 수행한다.
[RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)의 CLI 전제에 더해
`kubectl argo rollouts` plugin이 필요하다.

### Procedure 1: Vault Notifications Secret 준비 (최초 1회)

Notifications token provisioning은 이 저장소의 실행 transcript 밖에서 승인된
Vault operator가 수행하는 external secret operation이다. token 값, login
명령, Vault write 명령은 문서·shell history·검증 로그에 남기지 않는다.
이 런북은 ESO가 생성한 리소스의 상태를 읽는 지점에서 시작한다.

```bash
kubectl -n argocd get externalsecret
kubectl -n argocd get secret argocd-notifications-secret
```

> **주의**: secret value를 출력하는 `kubectl get secret -o yaml/json` 형태는
> 증적 수집에 사용하지 않는다.

---

### Procedure 2: ArgoCD Notifications 활성화 확인

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

아래 annotation과 이 런북의 restart·promote·undo 명령은 live
state를 바꾸므로 [POL-0004](../policies/0004-rollouts-notifications-headlamp-policy.md)와
[POL-0001](../policies/0001-k8s-gitops-operations-policy.md#exceptions)에 따른
operator-approved 실행에서만 사용한다.

```bash
kubectl -n argocd annotate externalsecret argocd-notifications-secret \
  force-sync=$(date +%s) --overwrite
```

---

### Procedure 3: Argo Rollouts 상태 확인

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

### Procedure 4: Headlamp 접근 검증

```bash
# Pod 및 Ingress 상태 확인
kubectl -n headlamp get pods,ingress,svc

# TLS Secret 확인 (cert-manager 발급)
kubectl -n headlamp get certificate headlamp-tls 2>/dev/null || \
kubectl -n headlamp get secret headlamp-tls 2>/dev/null

# HTTP 응답 확인 (mkcert rootCA로 TLS 검증)
curl --fail --silent --show-error --cacert secrets/certs/rootCA.pem \
  -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
```

### 복구: Headlamp TLS NotReady

`headlamp-tls`가 `READY=False`이면 먼저 ClusterIssuer 복구를
[RUN-0003](./0003-platform-expansion-bootstrap-runbook.md)으로 확인한다.

```bash
kubectl -n headlamp describe certificate headlamp-tls
kubectl -n cert-manager logs deploy/cert-manager | grep -i "headlamp" | tail -20
argocd app get platform-headlamp-config --hard-refresh
```

### 복구: Headlamp Token Unauthorized

브라우저 접근이 401이면 chart가 만든 ClusterRoleBinding을 확인하고 단기
ServiceAccount token을 발급한다. token은 문서, 로그, 채팅에 남기지 않는다.

```bash
kubectl get clusterrolebinding headlamp-admin
kubectl -n headlamp create token headlamp --duration=1h
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

### Procedure 5: Rollouts Dashboard 접근 검증

```bash
# Pod 및 Ingress 상태
kubectl -n argo-rollouts get pods
kubectl -n argo-rollouts get ingress

# HTTP 응답 확인
curl --fail --silent --show-error --cacert secrets/certs/rootCA.pem \
  -o /dev/null -w '%{http_code}' https://rollouts.127.0.0.1.nip.io/
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

### Troubleshooting Signatures

- `Error syncing application: slack token is empty` → Vault secret 미등록 또는 ESO 미동기화
- Headlamp 404 → ingress-nginx 미시작 또는 TLS secret 미발급
- Rollouts `CRD not found` → `installCRDs: true` 확인 또는 ArgoCD sync wave 순서 문제
- Rollouts Dashboard 502 → dashboard Pod 미기동, service port 3100 확인

## Traceability

- **Operations**: [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **ADR-0011**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Rollouts Spec**: `SPEC-0004` (retained; reach it through the Archive index)
- **Notifications Spec**: `SPEC-0005` (retained; reach it through the Archive index)
- **Rollouts Task records**: Spec 0004 Plan
- **Notifications Task records**: Spec 0005 Plan

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| N/A — SPEC-0004 is retained under ADR-0039 and reached through the Archive index, so no eligible upstream document carries a reciprocal link | Rollouts controller, CRDs, dashboard, promotion, analysis, or workload rollback needs bootstrap, diagnosis, or verification. | Platform operator records controller/CRD/Rollout/dashboard evidence and owns approved promotion or workload rollback. |
| N/A — SPEC-0005 is retained under ADR-0039 and reached through the Archive index, so no eligible upstream document carries a reciprocal link | Notifications delivery or the ESO-backed Slack secret is missing or degraded without exposing credential values. | Platform operator records controller, ConfigMap, ExternalSecret, and redacted send/error evidence; secret owner restores the Vault input. |
