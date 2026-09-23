---
title: "Platform Expansion Bootstrap Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0003"
---

# Platform Expansion Bootstrap Runbook

## Overview

이 런북은 기본 플랫폼 위에 추가된 cert-manager, Istio, Kiali를 부트스트랩하거나 복구하기 위한 즉시 실행 가능한 체크리스트와 증상별 복구 절차를 제공한다.

기본 플랫폼 부트스트랩(`infrastructure/bootstrap-local.sh`, ArgoCD, ESO/Vault,
외부 서비스 endpoint)은 [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md),
Headlamp 검증·복구는 [RUN-0004](./0004-rollouts-notifications-headlamp-runbook.md),
Kiali와 외부 observability 연결 복구는
[RUN-0007](./0007-kiali-observability-connectivity-runbook.md)이 소유한다.

### Purpose

플랫폼 확장 컴포넌트의 부트스트랩 단계를 재현 가능하게 수행하고, 장애 발생 시 원인별 복구 명령을 제공한다.

## Runbook Type

`bootstrap`

## When to Use

- 신규 플랫폼 확장 컴포넌트 설치
- host 재시작 또는 k3d 클러스터 재생성 후 복구
- cert-manager ClusterIssuer NotReady 복구
- Istio/Kiali 배포 실패 복구

## Procedure or Checklist

### Checklist

- [ ] [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md) checklist와 bootstrap 완료
- [ ] `secrets/certs/rootCA.pem` 존재 (cert-manager용)
- [ ] `secrets/certs/rootCA-key.pem` 존재 (ClusterIssuer CA key)
- [ ] `rootCA.pem`이 로컬 신뢰 저장소에 등록됨
- [ ] Prometheus 연결 (Kiali용): `nc -z 192.168.0.13 9090`
- [ ] Loki 연결 (로그 수집): `nc -z 192.168.0.13 3100`
- [ ] Tempo 연결 (트레이싱): `nc -z 192.168.0.13 3200`
- [ ] Alloy OTLP 연결: `nc -z 192.168.0.13 4317`
- [ ] Grafana 연결 (Kiali용): `nc -z 192.168.0.13 3000`

### Procedure

0. k8s router 이름 해석 확인

   Kiali 호스트명 `kiali.hy-k8s.home.arpa`는 k8s 전용 router(`192.168.0.14`)가
   받는다. 이름 해석이 그 주소를 가리키는지 확인한다. host 주소와 이름
   해석은 operator-approved 작업이며 통제는
   [POL-0001](../policies/0001-k8s-gitops-operations-policy.md)이 소유한다.

1. 기본 플랫폼 부트스트랩을 [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)
   절차로 완료한다. `infrastructure/bootstrap-local.sh`가 cert-manager
   namespace와 `mkcert-root-ca` Secret을 함께 준비한다.

2. cert-manager ClusterIssuer 상태 확인

   ```bash
   kubectl -n cert-manager get deployment cert-manager
   kubectl get clusterissuer mkcert-ca-issuer \
     -o jsonpath='{.status.conditions[0].type}'
   # 출력: Ready
   ```

3. Istio 가용성 확인

   ```bash
   kubectl get crd | grep istio.io | wc -l   # 10개 이상
   kubectl -n istio-system get deployment istiod
   ```

4. Kiali 가용성 + Prometheus 연결 확인

   ```bash
   kubectl -n istio-system get deployment kiali
   kubectl -n istio-system logs deploy/kiali | grep -i prometheus | tail -5
   ```

5. 전체 정적 계약 검증

   ```bash
   ./scripts/validate-infrastructure-contracts.sh
   ```

## Verification Steps

```bash
# 정적 계약
./scripts/validate-infrastructure-contracts.sh

# 런타임
kubectl get clusterissuer mkcert-ca-issuer
kubectl -n istio-system get deploy istiod kiali

# TLS 접근
curl --fail --silent --show-error --cacert secrets/certs/rootCA.pem \
  https://kiali.hy-k8s.home.arpa -o /dev/null -w '%{http_code}\n'
```

## Observability and Evidence Sources

- **Signals**: ClusterIssuer readiness, Istiod/Kiali deployment availability, ArgoCD Application health.
- **Evidence to Capture**: static contract output, relevant Kubernetes events, cert-manager logs, Kiali Prometheus connection logs.

## Safe Rollback or Recovery Procedure

### cert-manager ClusterIssuer NotReady

**증상**: `kubectl get clusterissuer mkcert-ca-issuer` → `READY=False`

> **Execution boundary**: Secret 재주입과 controller 재시작은 bootstrap 또는 human-approved break-glass 전용이다.

```bash
# 1. rootCA Secret 존재 확인
kubectl -n cert-manager get secret mkcert-root-ca

# 2. Secret 없으면 재주입 (bootstrap/break-glass only)
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert=secrets/certs/rootCA.pem \
  --key=secrets/certs/rootCA-key.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. cert-manager controller 재시작
kubectl -n cert-manager rollout restart deploy/cert-manager

# 4. ClusterIssuer 상태 재확인 (30초 대기)
kubectl wait clusterissuer mkcert-ca-issuer \
  --for=condition=Ready --timeout=60s
```

### Istiod CrashLoop / OOMKilled

**증상**: `kubectl -n istio-system get pods -l app=istiod` → CrashLoopBackOff 또는 OOMKilled

```bash
# 1. 자원 사용량 확인
kubectl -n istio-system top pod -l app=istiod

# 2. istiod 자원 값은 gitops/apps/root/platform-istiod-app.yaml의 inline Helm values가 소유한다.
#    POL-0003은 requests를 cpu 100m, memory 128Mi 아래로 낮추지 않는다.
#    값 조정이 필요하면 해당 Application을 수정·커밋한 뒤 ArgoCD sync로 반영한다.

# 3. 재시작
kubectl -n istio-system rollout restart deploy/istiod
```

### Kiali "No Prometheus" 오류

Kiali의 Prometheus·Grafana·Tempo 연결 복구는
[RUN-0007](./0007-kiali-observability-connectivity-runbook.md)을 따른다.

### Istio CRD 없이 istiod 설치 오류

**증상**: `platform-istiod` ArgoCD app sync 실패 — CRD not found

```bash
# 1. istio-base sync 상태 확인
argocd app get platform-istio-base

# 2. operator-triggered reconciliation only (sync-wave 강제)
argocd app sync platform-istio-base --prune

# 3. CRD 설치 확인 후 istiod sync
kubectl get crd | grep istio.io | wc -l
# operator-triggered reconciliation only
argocd app sync platform-istiod
```

## Traceability

- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Operations**: [`../policies/0003-service-mesh-cert-manager-policy.md`](../policies/0003-service-mesh-cert-manager-policy.md)
- **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- **Previous Runbook**: [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)
- [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Service Mesh and cert-manager Operations Policy](../policies/0003-service-mesh-cert-manager-policy.md) | Initial expansion or recovery of cert-manager, Istio, or Kiali must preserve CA-secret, namespace-injection, and sync-wave controls. | Platform operator captures ClusterIssuer, ingress/TLS, deployment, and static-contract evidence; approved break-glass operator owns bounded recovery actions. |
