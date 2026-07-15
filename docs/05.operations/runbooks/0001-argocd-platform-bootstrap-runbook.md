---
title: 'ArgoCD Platform Bootstrap Runbook'
type: sdlc/runbook
status: active
owner: platform
updated: 2026-05-22
---

# ArgoCD Platform Bootstrap Runbook

## Overview

이 런북은 WSL2 기반 GitOps 플랫폼을 즉시 실행 가능한 체크리스트 순서로 부트스트랩하고, 오류 시그니처별 복구 절차를 제공한다.

### Purpose

클러스터 구성, ArgoCD 설치, ESO/Vault 연동, 외부 endpoint 연결(Valkey `6379`, PostgreSQL `15432/15433`)을 재현 가능하게 수행한다.

## Runbook Type

`bootstrap`

## When to Use

- 신규 로컬 플랫폼 초기 구축
- 환경 재구축/복구
- 정책 검증 전 사전 점검

## Procedure or Checklist

### Checklist

- [ ] WSL2/WSL-native Docker 정상 상태
- [ ] CLI 도구(k3d/kubectl/helm/argocd) 설치
- [ ] 외부 서비스 런타임은 별도 워크스페이스(repo)에서 기동됨 (`vault`, `vault-agent`, `mng-valkey`)
- [ ] Valkey `172.18.0.9:6379` 접근 가능
- [ ] PostgreSQL HAProxy `172.18.0.15:15432/15433` 접근 가능
- [ ] Vault(`https://vault.127.0.0.1.nip.io`) 접근 가능 및 unseal 상태
- [ ] 읽기 가능한 `VAULT_CA_FILE`과 대화형 `/dev/tty` 준비
- [ ] 외부 Vault의 `eso-read-platform` role에 `bound_audiences=vault` 설정
- [ ] `secrets/certs/cert.pem`, `secrets/certs/key.pem` 존재 및 ArgoCD host SAN 포함
- [ ] `secret/platform/argocd.valkey_password` 존재
- [ ] `secret/platform/postgres-app.{db_name,username,password}` 존재

### Procedure

1. 외부 런타임 연결성 및 Vault 상태를 점검한다.

   ```bash
   docker network inspect infra_net >/dev/null
   nc -z 172.18.0.9 6379
   nc -z 172.18.0.15 15432
   nc -z 172.18.0.15 15433
   VAULT_CA_FILE=secrets/certs/rootCA.pem
   curl --fail --silent --show-error --cacert "$VAULT_CA_FILE" \
     -o /dev/null -w '%{http_code}\n' \
     https://vault.127.0.0.1.nip.io/v1/sys/health
   ```

2. 저장소의 Vault/ESO 계약을 값 조회 없이 정적으로 검증한다.

   ```bash
   python3 scripts/validate-vault-eso-contracts.py --root .
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
   export VAULT_CA_FILE="$PWD/secrets/certs/rootCA.pem"
   ./infrastructure/bootstrap-local.sh
   ```

   스크립트는 토큰을 환경 변수나 명령 인자로 받지 않고 `/dev/tty`에서
   표시 없이 직접 입력받는다. `VAULT_ADDR`는 HTTPS여야 하고 CA 파일은
   읽을 수 있어야 하며, 비대화형 또는 인증서 검증 생략 fallback은 없다.
   `vault-backend`의 클러스터 내부 HTTP 연결은 로컬 k3d 전용 예외이며
   production TLS 구성을 의미하지 않는다.

5. Bootstrap 결과로 생성되는 ingress TLS secret을 확인한다.

   ```bash
   kubectl -n argocd get secret argocd-local-tls -o jsonpath='{.type}'
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
argocd login argocd.127.0.0.1.nip.io --grpc-web
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

### Troubleshooting Matrix

| 에러 시그니처                                                                      | 진단 포인트                                  | 즉시 조치                                                      | 재검증                                                                                    |
| ---------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `vault is sealed (status=503)`                                                     | Vault health code가 503                      | Vault unseal 수행 후 health 재확인                             | CA 검증을 사용하는 HTTPS health 요청                                                        |
| `could not read secret key valkey_password from Vault path secret/platform/argocd` | 경로/키 누락 또는 토큰 권한 부족             | `secret/platform/argocd`에 `valkey_password` 확인, 권한 재설정 | Vault API + `jq -e '.data.data.valkey_password != null'`                                  |
| `WRONGPASS invalid username-password pair`                                         | ArgoCD secret과 Vault 값 불일치              | Vault 기준으로 `argocd-external-valkey` 재동기화               | `kubectl -n argocd get secret argocd-external-valkey -o yaml` + ArgoCD 로그               |
| `app path does not exist` (`root-platform`)                                        | `spec.source.path`와 원격 브랜치 구조 불일치 | `gitops/apps/root` 경로 확인 후 앱 재동기화                    | `kubectl -n argocd get application root-platform -o yaml \| rg 'path:'`                   |

## Safe Rollback or Recovery Procedure

- [ ] ArgoCD app을 이전 리비전으로 rollback

  ```bash
  argocd app history root-platform
  argocd app rollback root-platform <history-id>
  ```

- [ ] Vault 값을 명령 인자나 환경 변수로 브리지하지 않는다. 외부 Vault의
      경로/정책과 ESO readiness를 복구한 뒤 ExternalSecret 재조정을 기다리고,
      필요하면 위의 대화형 CA 검증 부트스트랩을 다시 실행한다.

- [ ] ArgoCD hard refresh로 캐시/상태 재평가

  ```bash
  argocd app get root-platform --hard-refresh
  # operator-triggered reconciliation only
  argocd app sync root-platform
  ```

- [ ] 외부 endpoint mapping/IP 및 ESO auth 설정 재적용 후 재검증

### Agent Operations

- **Prompt Rollback**: 최근 문서/설정 변경 롤백
- **Model Fallback**: 검증 실패 시 보수적 절차 우선
- **Tool Disable / Revoke**: 위험 자동화 중지
- **Eval Re-run**: T-001~T-011 검증 재실행
- **Trace Capture**: task 문서에 증적 추가

## Traceability

- **Incident and Postmortem Index**: [`../incidents/README.md`](../incidents/README.md)
- [`../../02.architecture/requirements/0007-current-local-gitops-platform.md`](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Current Local GitOps Platform Spec](../../03.specs/008-current-local-gitops-platform/spec.md) | A new or rebuilt local cluster needs the current ArgoCD, ESO/Vault, TLS, and external-service contracts established and checked. | Platform operator captures bootstrap, ArgoCD/ESO, endpoint, and connectivity evidence and owns bounded ArgoCD rollback or configuration recovery. |
