# WSL2 k3d/k3s ArgoCD HA Setup Guide

## Overview (KR)

이 문서는 WSL2 환경에서 멀티노드 k3d 클러스터와 ArgoCD/ESO/Vault/외부 서비스 계약을 설정하고 검증하는 방법을 설명한다.

## Guide Type

`how-to`

## Target Audience

- Developer
- Operator

## Purpose

운영 계약(TLS/외부 서비스/최소권한)을 유지하면서, 로컬 런타임 검증과 CI 정적 검증을 분리해 재현성을 높인다.

## Prerequisites

- Windows + WSL2(Ubuntu)
- Docker Desktop WSL integration enabled
- `kubectl`, `k3d`, `helm`, `argocd`, `rg` 설치
- 외부 런타임(Vault/PostgreSQL/Valkey) 기동 상태
- 인증서 파일 준비: `secrets/certs/cert.pem`, `secrets/certs/key.pem`, `secrets/certs/rootCA.pem`

## Step-by-step Instructions

1. 클러스터 baseline을 생성/확인한다.

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
kubectl get nodes -o wide
```

1. 인증서 SAN과 ArgoCD 호스트 계약을 점검한다.

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg '127\.0\.0\.1\.nip\.io|\*\.127\.0\.0\.1\.nip\.io'
```

1. SAN이 미포함이면 재발급 후 동일 경로에 교체한다.

- 재발급 절차: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md#troubleshooting-signatures)

1. 부트스트랩 스크립트로 TLS Secret까지 포함해 초기화를 실행한다.

```bash
export VAULT_TOKEN='<redacted>'
./infrastructure/bootstrap-local.sh
```

1. ArgoCD 및 GitOps root app 상태를 확인한다.

```bash
kubectl -n argocd get application root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
kubectl -n argocd get applications
```

1. 외부 서비스 인터페이스 계약을 검증한다.

```bash
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|vault-external|8200|valkey-external|172.19.0.12|6379'
```

## Local Runtime Validation vs CI Static Validation

### Local Runtime Validation (cluster required)

```bash
./infrastructure/tests/run-all.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
```

### CI Static Validation (cluster not required)

```bash
./infrastructure/tests/verify-contracts-static.sh
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
```

### Workflow Security Validation

`.github/workflows/**` 변경 시 CI에서 자동 수행:

- `actionlint`
- `zizmor`

## Common Pitfalls

- `vault-external` EndpointSlice 누락으로 `connection refused` 발생
- AppProject wildcard 복원으로 과권한 상태 재발
- `cert.pem` SAN 누락으로 TLS handshake 실패
- 로컬 파일만 수정하고 원격 `main`에 반영하지 않아 ArgoCD 미동기화

## Related Documents

- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Operation**: [`../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- **Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
