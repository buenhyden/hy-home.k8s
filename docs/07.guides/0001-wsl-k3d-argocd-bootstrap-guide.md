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
- `VAULT_TOKEN` 환경변수
- 외부 서비스 런타임은 별도 워크스페이스(repo)에서 사전 기동
  - Vault: `https://vault.127.0.0.1.nip.io`
  - PostgreSQL: `172.30.0.11:5432`
  - Valkey: `mng-valkey:6379` (`infra_net`)

## Step-by-step Instructions

1. 외부 서비스 런타임(별도 repo) 상태를 먼저 확인한다.

   ```bash
   docker network inspect infra_net >/dev/null
   docker ps --format '{{.Names}}' | rg '^(vault|vault-agent|mng-valkey)$'
   curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health
   ```

2. Vault 토큰과 호스트 매핑을 설정한다.

   ```bash
   export VAULT_TOKEN='replace-with-vault-admin-token'
   echo "127.0.0.1 argocd.local" | sudo tee -a /etc/hosts
   ```

3. 저장소 루트에서 부트스트랩 스크립트를 실행한다.

   ```bash
   ./infrastructure/bootstrap-local.sh
   ```

4. `argocd.local` TLS 시크릿을 생성한다.

   ```bash
   mkcert -install
   mkcert argocd.local
   kubectl -n argocd create secret tls argocd-local-tls \
     --cert=argocd.local.pem \
     --key=argocd.local-key.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

5. ArgoCD 루트 앱 및 ApplicationSet 상태를 확인한다.

   ```bash
   kubectl -n argocd get applications,applicationsets
   ```

6. ESO가 Vault 값을 읽어 `argocd-external-valkey` 비밀을 유지하는지 확인한다.

   ```bash
   kubectl -n argocd get externalsecret,secret argocd-external-valkey
   ```

7. 외부 서비스 매핑(PostgreSQL EndpointSlice, Valkey ExternalName)과 네트워크 정책을 검증한다.

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
