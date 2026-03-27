# ArgoCD Platform Bootstrap Runbook

: WSL k3d/k3s GitOps Bootstrap

## Overview (KR)

이 런북은 WSL2 기반 GitOps 플랫폼을 실제로 부트스트랩하고 검증하는 실행 절차를 제공한다.

## Purpose

클러스터 구성, ArgoCD 설치, ESO/Vault 연동, 외부 endpoint 연결을 재현 가능하게 수행한다.

## Canonical References

- [`../02.ard/0001-wsl-k3d-argocd-platform.md`](../02.ard/0001-wsl-k3d-argocd-platform.md)
- [`../03.adr/0001-k3d-topology-and-network.md`](../03.adr/0001-k3d-topology-and-network.md)
- [`../03.adr/0002-argocd-helm-and-gitops-model.md`](../03.adr/0002-argocd-helm-and-gitops-model.md)
- [`../03.adr/0003-eso-vault-k8s-auth.md`](../03.adr/0003-eso-vault-k8s-auth.md)
- [`../03.adr/0004-external-services-endpoints-and-valkey-backend.md`](../03.adr/0004-external-services-endpoints-and-valkey-backend.md)
- [`../04.specs/001-wsl-k3d-argocd-platform/spec.md`](../04.specs/001-wsl-k3d-argocd-platform/spec.md)
- [`../05.plans/2026-03-27-wsl-k3d-argocd-platform.md`](../05.plans/2026-03-27-wsl-k3d-argocd-platform.md)

## When to Use

- 신규 로컬 플랫폼 초기 구축
- 환경 재구축/복구
- 정책 검증 전 사전 점검

## Procedure or Checklist

### Checklist

- [ ] WSL2/Docker Desktop 정상 상태
- [ ] CLI 도구(k3d/kubectl/helm/argocd) 설치
- [ ] 외부 서비스 런타임은 별도 워크스페이스(repo)에서 기동됨 (`vault`, `vault-agent`, `mng-valkey`)
- [ ] `mng-valkey:6379`가 host `26379`으로 publish됨
- [ ] PostgreSQL HAProxy write/read 포트(`15432`, `15433`)가 열려 있음
- [ ] Vault(`https://vault.127.0.0.1.nip.io`) 접근 가능 및 unseal 상태
- [ ] `VAULT_TOKEN` 환경변수 설정
- [ ] `/etc/hosts`에 `argocd.local` 매핑

### Procedure

1. 사전 변수 설정 및 호스트 매핑.

   ```bash
   export VAULT_TOKEN='replace-with-vault-admin-token'
   echo "127.0.0.1 argocd.local" | sudo tee -a /etc/hosts
   ```

2. 외부 서비스 런타임 계약 확인(별도 repo 운영 범위).

   ```bash
   docker network inspect infra_net >/dev/null
   docker ps --format '{{.Names}}' | rg '^(vault|vault-agent|mng-valkey)$'
   curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health
   ```

3. 부트스트랩 스크립트 실행.

   ```bash
   ./infrastructure/bootstrap-local.sh
   ```

4. ingress-nginx 로드 및 TLS 인증서 적용.

   ```bash
   mkcert -install
   mkcert argocd.local
   kubectl -n argocd create secret tls argocd-local-tls \
     --cert=argocd.local.pem \
     --key=argocd.local-key.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

5. ArgoCD 루트 앱 동기화 상태 확인.

   ```bash
   kubectl -n argocd get applications
   kubectl -n argocd get applicationsets
   ```

6. ESO 및 Vault 기반 비밀 동기화 확인.

   ```bash
   kubectl -n external-secrets get pods
   kubectl -n argocd get externalsecret,secret argocd-external-valkey
   ```

7. 외부 서비스 매핑(PostgreSQL EndpointSlice, Valkey ExternalName) 연결성 확인.

   ```bash
   kubectl -n platform get svc,endpointslice
   kubectl -n platform get svc,endpointslice | rg 'postgres-(write|read)-external'
   kubectl -n platform get svc valkey-external -o yaml
   ```

8. ArgoCD UI 접속 및 프로젝트 경계 검증.

   ```bash
   argocd login argocd.local --grpc-web
   argocd proj list
   ```

## Verification Steps

- [ ] `kubectl get nodes`에서 4개 노드 Ready 확인
- [ ] `kubectl -n argocd get pods` 정상
- [ ] `kubectl get svc,endpointslice -A | rg 'postgres-(write|read)-external|valkey-external'`
- [ ] `kubectl -n external-secrets get externalsecret,secretstore,clustersecretstore`
- [ ] `argocd app list` 및 sync 상태 확인

## Observability and Evidence Sources

- **Signals**: ArgoCD health/sync, ESO sync status, pod readiness
- **Evidence to Capture**: 명령 출력, 이벤트 로그, 실패/복구 타임스탬프

## Safe Rollback or Recovery Procedure

- [ ] ArgoCD app을 이전 리비전으로 rollback
- [ ] external endpoint mapping/IP 재검증
- [ ] Vault role/policy 및 ESO auth 설정 재적용

## Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 문서/설정 변경 롤백
- **Model Fallback**: 검증 실패 시 보수적 절차 우선
- **Tool Disable / Revoke**: 위험 자동화 중지
- **Eval Re-run**: T-001~T-011 검증 재실행
- **Trace Capture**: task 문서에 증적 추가

## Related Operational Documents

- **Incident examples**: `[../10.incidents/YYYY/YYYY-MM-DD-<incident-title>.md]`
- **Postmortem examples**: `[../11.postmortems/YYYY/YYYY-MM-DD-<incident-title>.md]`
