# ArgoCD Platform Bootstrap Runbook

: WSL k3d/k3s GitOps Bootstrap

## Overview (KR)

이 런북은 WSL2 기반 GitOps 플랫폼을 즉시 실행 가능한 체크리스트 순서로 부트스트랩하고, 오류 시그니처별 복구 절차를 제공한다.

## Purpose

클러스터 구성, ArgoCD 설치, ESO/Vault 연동, 외부 endpoint 연결(Valkey `6379`, PostgreSQL `15432/15433`)을 재현 가능하게 수행한다.

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
- [ ] `secret/platform/argocd.valkey_password` 존재
- [ ] `secret/platform/postgres-app.{db_name,username,password}` 존재

### Procedure

1. 외부 런타임 연결성 및 Vault 상태를 점검한다.

   ```bash
   docker network inspect infra_net >/dev/null
   ss -ltn '( sport = :26379 or sport = :15432 or sport = :15433 )'
   curl -ksS -o /dev/null -w '%{http_code}\n' \
     https://vault.127.0.0.1.nip.io/v1/sys/health
   ```

2. Vault 경로/키 존재를 검증한다(비밀 값 출력 금지).

   ```bash
   export VAULT_TOKEN='replace-with-vault-admin-token'

   curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
     https://vault.127.0.0.1.nip.io/v1/secret/data/platform/argocd \
     | jq -e '.data.data.valkey_password != null' >/dev/null

   curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
     https://vault.127.0.0.1.nip.io/v1/secret/data/platform/postgres-app \
     | jq -e '.data.data.db_name != null and .data.data.username != null and .data.data.password != null' >/dev/null
   ```

3. `argocd.local` 매핑을 확인하고 없으면 추가한다.

   ```bash
   grep -q 'argocd.local' /etc/hosts || \
     echo "127.0.0.1 argocd.local" | sudo tee -a /etc/hosts
   ```

4. 부트스트랩 스크립트를 실행한다.

   ```bash
   ./infrastructure/bootstrap-local.sh
   ```

5. ingress TLS를 적용한다.

   ```bash
   mkcert -install
   mkcert argocd.local
   # human-approved bootstrap only
   kubectl -n argocd create secret tls argocd-local-tls \
     --cert=argocd.local.pem \
     --key=argocd.local-key.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

6. ArgoCD 루트 앱 및 GitOps 경로 계약을 확인한다.

   ```bash
   kubectl -n argocd get application root-platform -o yaml | \
     rg 'path: gitops/apps/root|targetRevision: main'
   kubectl -n argocd get applications,applicationsets
   ```

7. ESO 및 Vault 기반 비밀 동기화를 확인한다.

   ```bash
   kubectl -n external-secrets get pods
   kubectl -n argocd get externalsecret,secret argocd-external-valkey
   ```

8. 외부 서비스 Kubernetes 인터페이스를 확인한다.

   ```bash
   kubectl -n platform get svc,endpointslice
   kubectl -n platform get svc,endpointslice | rg 'postgres-(write|read)-external'
   kubectl -n platform get svc valkey-external -o yaml
   ```

9. 클러스터 내부에서 write/read/Postgres와 Valkey 포트 연결성을 점검한다.

   ```bash
   kubectl -n platform run svc-probe --rm -it --restart=Never \
     --image=busybox:1.36 -- sh -c \
     "nc -zvw3 postgres-write-external 15432 && \
      nc -zvw3 postgres-read-external 15433 && \
      nc -zvw3 valkey-external 6379"
   ```

10. ArgoCD 접속 후 프로젝트 경계와 앱 상태를 확인한다.

```bash
argocd login argocd.local --grpc-web
argocd proj list
argocd app list
```

## Verification Steps

- [ ] `kubectl get nodes`에서 4개 노드 Ready 확인
- [ ] `kubectl -n argocd get pods` 정상
- [ ] `kubectl get svc,endpointslice -A | rg 'postgres-(write|read)-external|valkey-external'`
- [ ] `kubectl -n external-secrets get externalsecret,secretstore,clustersecretstore`
- [ ] `argocd app list` 및 sync 상태 확인
- [ ] `svc-probe`에서 `postgres-write-external:15432`, `postgres-read-external:15433`, `valkey-external:6379` 연결 성공

## Observability and Evidence Sources

- **Signals**: ArgoCD health/sync, ESO sync status, pod readiness
- **Evidence to Capture**: 명령 출력, 이벤트 로그, 실패/복구 타임스탬프

## Troubleshooting Matrix

| 에러 시그니처                                                                      | 진단 포인트                                  | 즉시 조치                                                      | 재검증                                                                                    |
| ---------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `vault is sealed (status=503)`                                                     | Vault health code가 503                      | Vault unseal 수행 후 health 재확인                             | `curl -ksS -o /dev/null -w '%{http_code}\n' https://vault.127.0.0.1.nip.io/v1/sys/health` |
| `could not read secret key valkey_password from Vault path secret/platform/argocd` | 경로/키 누락 또는 토큰 권한 부족             | `secret/platform/argocd`에 `valkey_password` 확인, 권한 재설정 | Vault API + `jq -e '.data.data.valkey_password != null'`                                  |
| `WRONGPASS invalid username-password pair`                                         | ArgoCD secret과 Vault 값 불일치              | Vault 기준으로 `argocd-external-valkey` 재동기화               | `kubectl -n argocd get secret argocd-external-valkey -o yaml` + ArgoCD 로그               |
| `app path does not exist` (`root-platform`)                                        | `spec.source.path`와 원격 브랜치 구조 불일치 | `gitops/apps/root` 경로 확인 후 앱 재동기화                    | `kubectl -n argocd get application root-platform -o yaml \| rg 'path:'`                   |

## Safe Rollback or Recovery Procedure

- [ ] ArgoCD app을 이전 리비전으로 rollback

  ```bash
  argocd app history root-platform
  argocd app rollback root-platform <history-id>
  ```

- [ ] Vault 키 브릿지(응급 복구): Vault 값을 읽어 ArgoCD secret 재생성

  ```bash
  VALKEY_PASSWORD="$(curl -ksS -H "X-Vault-Token: $VAULT_TOKEN" \
    https://vault.127.0.0.1.nip.io/v1/secret/data/platform/argocd \
    | jq -r '.data.data.valkey_password')"

  # human-approved break-glass only
  kubectl -n argocd create secret generic argocd-external-valkey \
    --from-literal=redis-password="$VALKEY_PASSWORD" \
    --dry-run=client -o yaml | kubectl apply -f -
  ```

- [ ] ArgoCD hard refresh로 캐시/상태 재평가

  ```bash
  argocd app get root-platform --hard-refresh
  # operator-triggered reconciliation only
  argocd app sync root-platform
  ```

- [ ] 외부 endpoint mapping/IP 및 ESO auth 설정 재적용 후 재검증

## Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 문서/설정 변경 롤백
- **Model Fallback**: 검증 실패 시 보수적 절차 우선
- **Tool Disable / Revoke**: 위험 자동화 중지
- **Eval Re-run**: T-001~T-011 검증 재실행
- **Trace Capture**: task 문서에 증적 추가

## Related Documents

- **Incident Index**: [`../10.incidents/README.md`](../10.incidents/README.md)
- **Postmortem Index**: [`../10.incidents/README.md`](../10.incidents/README.md)
