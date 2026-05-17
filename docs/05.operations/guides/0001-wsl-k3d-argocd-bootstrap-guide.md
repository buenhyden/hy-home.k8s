---
title: 'WSL k3d ArgoCD Bootstrap Guide'
type: guide
status: active
owner: platform
updated: 2026-03-27
---

# WSL k3d ArgoCD Bootstrap Guide

## Overview (KR)

이 문서는 WSL2 환경에서 k3d(k3s) + ArgoCD GitOps 플랫폼을 부트스트랩할 때 필요한 사전 조건, 실행 순서, 검증 포인트를 정리한다.
외부 서비스(Vault/Valkey/PostgreSQL)는 이 저장소가 아닌 별도 워크스페이스(repo)에서 운영하며, 이 저장소는 Kubernetes 연동 계약만 관리한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer
- GitOps Operator

## Purpose

로컬 플랫폼을 표준 계약으로 반복 재현하고, 부트스트랩 직후 GitOps/Secret/외부 엔드포인트 상태를 일관되게 검증한다.

## Prerequisites

- Windows 11 + WSL2 Ubuntu
- Docker Desktop (WSL backend)
- `k3d`, `kubectl`, `helm`, `argocd`, `jq`, `curl`, `mkcert`
- `VAULT_TOKEN` 환경 변수
- 외부 서비스 런타임(별도 repo) 사전 기동 및 계약 충족:
  - Vault: `https://vault.127.0.0.1.nip.io` (unseal 완료)
  - Valkey: `172.18.0.9:6379`
  - PostgreSQL HAProxy: `172.18.0.15:15432/15433`
- Vault 시크릿 계약:
  - `secret/platform/argocd` 의 `valkey_password`
  - `secret/platform/postgres-app` 의 `db_name`, `username`, `password`

## Step-by-step Instructions

1. 외부 서비스 런타임 및 포트 계약을 확인한다.

   ```bash
   docker network inspect infra_net >/dev/null
   nc -z 172.18.0.9 6379
   nc -z 172.18.0.15 15432
   nc -z 172.18.0.15 15433
   curl -ksS -o /dev/null -w '%{http_code}\n' \
     https://vault.127.0.0.1.nip.io/v1/sys/health
   ```

2. Vault 시크릿 키 존재 여부(값 비노출)를 검증한다.

   ```bash
   export VAULT_TOKEN='replace-with-vault-admin-token'

   curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
     https://vault.127.0.0.1.nip.io/v1/secret/data/platform/argocd \
     | jq -e '.data.data.valkey_password != null' >/dev/null

   curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
     https://vault.127.0.0.1.nip.io/v1/secret/data/platform/postgres-app \
     | jq -e '.data.data.db_name != null and .data.data.username != null and .data.data.password != null' >/dev/null
   ```

3. ArgoCD TLS 인증서 입력을 확인한다.

   ```bash
   test -f secrets/certs/cert.pem
   test -f secrets/certs/key.pem
   openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
     rg 'argocd\.127\.0\.0\.1\.nip\.io|\*\.127\.0\.0\.1\.nip\.io'
   ```

4. 부트스트랩 스크립트를 실행한다.

   ```bash
   ./infrastructure/bootstrap-local.sh
   ```

5. Bootstrap 결과로 생성되는 ArgoCD ingress TLS secret을 확인한다.

   ```bash
   kubectl -n argocd get secret argocd-local-tls -o jsonpath='{.type}'
   ```

6. ArgoCD 루트 앱 경로와 동기화 상태를 확인한다.

   ```bash
   kubectl -n argocd get application root-platform -o yaml | \
     rg 'path: gitops/apps/root|targetRevision: main'
   kubectl -n argocd get applications,applicationsets
   ```

7. ESO와 외부 서비스 Kubernetes 인터페이스를 검증한다.

   ```bash
   kubectl -n external-secrets get pods
   kubectl -n argocd get externalsecret,secret argocd-external-valkey
   kubectl -n platform get svc,endpointslice | \
     rg 'postgres-(write|read)-external|15432|15433'
   kubectl -n platform get svc,endpointslice | rg 'valkey-external|172.18.0.9|6379'
   ```

## Common Pitfalls

- `vault is sealed (status=503)`
  - 원인: Vault unseal 미완료
  - 조치: Vault를 unseal 후 `/v1/sys/health`가 `200/429/472/473`인지 확인
- `could not read secret key valkey_password from Vault path secret/platform/argocd`
  - 원인: Vault 경로/키 누락 또는 토큰 권한 부족
  - 조치: `secret/platform/argocd`에 `valkey_password` 생성 및 권한 재검증
- `WRONGPASS invalid username-password pair`
  - 원인: Valkey 비밀번호 불일치(bootstrap 시크릿/ESO 동기화 불일치)
  - 조치: Vault 값을 기준으로 `argocd-external-valkey` 재동기화
- `root-platform` Sync `Unknown` + `app path does not exist`
  - 원인: `spec.source.path`와 원격 브랜치 실제 경로 불일치
  - 조치: `gitops/apps/root` 경로 존재 확인 후 Application 재동기화

## Related Documents

- **Spec**: [`../../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Operation**: [`../policies/0001-k8s-gitops-operations-policy.md`](../policies/0001-k8s-gitops-operations-policy.md)
- **Runbook**: [`../runbooks/0001-argocd-platform-bootstrap-runbook.md`](../runbooks/0001-argocd-platform-bootstrap-runbook.md)
- **Plan**: [`../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
