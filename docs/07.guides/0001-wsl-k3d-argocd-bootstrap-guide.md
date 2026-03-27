# WSL k3d ArgoCD Bootstrap Guide

## Overview (KR)

이 문서는 WSL2 환경에서 k3d(k3s)와 ArgoCD GitOps 플랫폼을 초기 부트스트랩하는 방법을 설명한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer

## Purpose

로컬 환경에서 표준 토폴로지와 GitOps 흐름을 재현해 개발/검증 기반을 일관되게 맞춘다.

## Prerequisites

- Windows 11 + WSL2 Ubuntu
- Docker Desktop (WSL backend)
- `kubectl`, `helm`, `k3d`, `argocd` CLI
- `mkcert` (로컬 TLS 인증서 생성)
- `VALKEY_PASSWORD` 환경변수

## Step-by-step Instructions

1. 비밀번호와 호스트 매핑을 먼저 설정한다.

   ```bash
   export VALKEY_PASSWORD='replace-with-strong-password'
   echo "127.0.0.1 argocd.local" | sudo tee -a /etc/hosts
   ```

2. 저장소 루트에서 부트스트랩 스크립트를 실행한다.

   ```bash
   ./infrastructure/bootstrap-local.sh
   ```

3. `argocd.local` TLS 시크릿을 생성한다.

   ```bash
   mkcert -install
   mkcert argocd.local
   kubectl -n argocd create secret tls argocd-local-tls \
     --cert=argocd.local.pem \
     --key=argocd.local-key.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

4. ArgoCD 루트 앱 및 ApplicationSet 상태를 확인한다.

   ```bash
   kubectl -n argocd get applications,applicationsets
   ```

5. ESO가 Vault 값을 읽어 `argocd-external-valkey` 비밀을 유지하는지 확인한다.

   ```bash
   kubectl -n argocd get externalsecret,secret argocd-external-valkey
   ```

6. 외부 서비스 래핑(Service/EndpointSlice)과 네트워크 정책을 검증한다.

   ```bash
   kubectl get svc,endpointslice,networkpolicy -n platform
   ```

## Common Pitfalls

- `172.30.0.0/24` 대역 중복으로 endpoint 연결 실패
- ArgoCD 프로젝트 권한 누락으로 sync 실패
- Vault role/path 매핑 불일치로 secret sync 실패

## Related Documents

- **Spec**: [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Operation**: [`../08.operations/0001-k8s-gitops-operations-policy.md`](../08.operations/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [`../09.runbooks/0001-argocd-platform-bootstrap-runbook.md`](../09.runbooks/0001-argocd-platform-bootstrap-runbook.md)
