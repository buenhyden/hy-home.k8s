# WSL2 k3d/k3s ArgoCD HA Setup Guide

## Overview (KR)

이 문서는 WSL2 환경에서 멀티노드 k3d 클러스터와 ArgoCD/ESO/Vault/외부 서비스 계약을 설정하고 검증하는 방법을 설명한다.

## Guide Type

`how-to`

## Target Audience

- Developer
- Operator

## Purpose

운영 핫픽스와 구조 개선을 함께 고려하여, 재현 가능한 로컬 HA 플랫폼을 구축한다.

## Prerequisites

- Windows + WSL2(Ubuntu)
- Docker Desktop WSL integration enabled
- `kubectl`, `k3d`, `helm`, `argocd`, `rg` 설치
- 외부 런타임(Vault/PostgreSQL/Valkey) 기동 상태

## Step-by-step Instructions

1. 클러스터 baseline을 생성/확인한다.

```bash
k3d cluster create --config infrastructure/k3d/k3d-cluster.yaml
kubectl get nodes -o wide
```

2. ArgoCD 및 GitOps root app 상태를 확인한다.

```bash
kubectl -n argocd get application root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
kubectl -n argocd get applications
```

3. 외부 서비스 인터페이스 계약을 검증한다.

```bash
kubectl -n platform get svc,endpointslice | \
  rg 'postgres-(write|read)-external|15432|15433|vault-external|8200'
kubectl -n platform get svc,endpointslice | \
  rg 'valkey-external|valkey-external-1|172.30.0.12|26379'
```

4. Secret plane을 검증한다.

```bash
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
```

5. 컴포넌트별 검증 스크립트를 실행한다.

```bash
./infrastructure/tests/run-all.sh
```

6. 최소권한 정책이 적용되었는지 확인한다.

```bash
kubectl -n argocd get appproject platform -o yaml | \
  rg 'clusterResourceWhitelist|namespaceResourceWhitelist'
cat infrastructure/vault/policies/eso-read.hcl
```

## Common Pitfalls

- `vault-external` EndpointSlice 누락으로 `connection refused` 발생
- Valkey를 ExternalName으로 유지한 상태에서 ipBlock 기반 네트워크 정책을 적용하면 연결 실패 가능
- WSL2 메모리 부족으로 control plane pod 재시작 반복
- `argocd` CLI 미설치/미로그인 상태에서 상태 재평가 누락

## Related Documents

- **Spec**: [`../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md`](../04.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- **Operation**: [`../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../08.operations/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- **Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
