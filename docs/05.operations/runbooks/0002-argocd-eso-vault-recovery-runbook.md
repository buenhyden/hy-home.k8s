---
title: 'ArgoCD ESO Vault Recovery Runbook'
type: sdlc/runbook
status: active
owner: platform
updated: 2026-06-02
---

# ArgoCD ESO Vault Recovery Runbook

## Overview

이 런북은 `ClusterSecretStore/vault-backend Ready=False` 상황에서 Vault sealed 상태, EndpointSlice drift, Kubernetes auth drift를 구분하고, ArgoCD/ESO 상태를 정상화한 뒤 TLS/CI 계약 회귀를 점검하는 절차를 제공한다.

> **현재 실행계약 메모 (2026-06-02)**: 현재 `gitops/platform/external-services/`와 정적 검증 스크립트는 외부 서비스 EndpointSlice/CIDR을 `172.18.x` 기준으로 고정한다. 이 런북은 old endpoint 값을 보존하지 않고 현재 repo-backed 계약만 사용한다.
>
> **Agent execution boundary**: EndpointSlice hotfix와 Docker network mutation은 human-approved break-glass 전용이다. Agent는 기본적으로 사전 스냅샷, Git 파일 보정안, 검증 계획, 후속 증적 정리까지만 수행한다.

### Purpose

`vault-external` endpoint 부재, 연결 거부, Vault sealed 상태, 또는 Kubernetes auth drift로 발생하는 ESO/Vault 연동 장애를 빠르게 분류하고, operator-bound 복구 절차와 계약 회귀 검증을 연결한다.

## Runbook Type

`recovery`

## When to Use

- `vault-backend`가 `Ready=False`
- ESO 로그에 `connection refused`, `InvalidProviderConfig`, 또는 `context deadline exceeded` 반복
- ESO 로그에 `Vault is sealed`가 반복
- `argocd-external-valkey`가 `SecretSyncedError`
- 복구 후 ArgoCD HTTPS 진입점(`argocd.127.0.0.1.nip.io`) 회귀가 의심될 때
- Docker 재시작 후 vault 컨테이너가 k3d 네트워크에서 분리된 경우

## Procedure or Checklist

### Checklist

- [ ] `kubectl` 컨텍스트 확인
- [ ] 평문 시크릿/토큰 출력 금지
- [ ] 복구 전 상태 스냅샷 수집
- [ ] 외부 Vault의 `eso-read-platform` role에 `bound_audiences=vault` 설정 확인

`vault-external`과 `vault-backend`의 HTTP 연결은 현재 로컬 k3d 네트워크
내부 전용 예외이며 production TLS 구성을 의미하지 않는다. 외부 Vault
관리 요청은 HTTPS와 검증된 CA를 사용해야 한다.

### Procedure

1. 사전 스냅샷을 저장한다.

```bash
kubectl -n external-secrets get clustersecretstore vault-backend -o yaml
kubectl -n argocd get externalsecret argocd-external-valkey -o yaml
kubectl -n argocd get app platform-eso-config platform-argocd-config -o wide
kubectl -n external-secrets logs deploy/external-secrets --tail=200 | \
  rg -i 'vault|clustersecretstore|error|connection refused|sealed'
```

1. Vault sealed 상태와 endpoint drift를 먼저 분류한다.

```bash
kubectl -n platform get svc vault-external -o yaml
kubectl -n platform get endpointslice vault-external-1 -o yaml
curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health
kubectl -n external-secrets logs deploy/external-secrets --since=2h --tail=80 | \
  rg -i 'Vault is sealed|connection refused|context deadline|permission denied|invalid'
```

판정 기준:

- `sys/health`가 `sealed:true`이고 ESO 로그가 `Vault is sealed`를 보이면 EndpointSlice를 수정하지 않는다. Vault unseal이 먼저다.
- `sys/health`가 응답하지 않거나 `connection refused`가 반복되면 endpoint/network 절차로 이동한다.
- `sys/health`가 `sealed:false`인데 Kubernetes auth login이 실패하면 Vault auth mount, role, TokenReview reviewer 설정을 operator-bound로 재검토한다.

1. Vault가 sealed 상태면 operator-bound unseal 절차를 수행한다. Agent는
   unseal key, root token, Vault token, secret value를 요청하거나 출력하지
   않는다. Vault 운영자는 승인된 비밀 입력 채널을 사용하고 credential을
   명령 인자, 셸 환경, 채팅, Git, 로그, PR 본문에 넣지 않는다.

unseal 후에는 secret 값을 조회하지 말고 readiness metadata만 확인한다.

```bash
curl -sS --max-time 5 http://172.18.0.8:8200/v1/sys/health
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
```

1. Vault endpoint/network drift가 확인된 경우에만 Vault 컨테이너를 k3d 네트워크에 연결하고 `EndpointSlice` 핫픽스를 적용한다. 이 단계는 human-approved break-glass 전용이다.

```bash
# Vault가 k3d-hyhome 네트워크에 연결되어 있는지 확인
VAULT_K3D_IP=$(docker inspect vault --format '{{(index .NetworkSettings.Networks "k3d-hyhome").IPAddress}}' 2>/dev/null)

# 연결되지 않은 경우 연결
if [ -z "$VAULT_K3D_IP" ]; then
  docker network connect k3d-hyhome vault
  VAULT_K3D_IP=$(docker inspect vault --format '{{(index .NetworkSettings.Networks "k3d-hyhome").IPAddress}}')
  echo "vault connected to k3d-hyhome: $VAULT_K3D_IP"
fi

# vault-external EndpointSlice를 k3d-hyhome IP로 업데이트
# human-approved break-glass only
cat <<YAML | kubectl apply -f -
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: vault-external-1
  namespace: platform
  annotations:
    platform.hyhome.io/environment-scope: local-only
    platform.hyhome.io/transport-boundary: local-only-http
  labels:
    kubernetes.io/service-name: vault-external
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 8200
endpoints:
  - addresses:
      - ${VAULT_K3D_IP}
YAML
```

> **참고**: vault-external EndpointSlice는 `gitops/platform/external-services/vault-external.yaml`의 현재 k3d-reachable Vault 주소와 일치해야 한다.
> k3d 노드는 k3d-hyhome 네트워크에서 접근 가능한 Vault 주소만 안정적으로 사용할 수 있다.
> Vault Kubernetes auth `kubernetes_host`는 `https://172.18.0.2:6443`으로 설정되어야 한다(k3d-hyhome 경유).

1. Store/ExternalSecret/ArgoCD 상태를 재평가한다.

```bash
kubectl -n platform get endpointslice vault-external-1 -o yaml
kubectl -n external-secrets get clustersecretstore vault-backend
kubectl -n argocd get externalsecret argocd-external-valkey
kubectl -n argocd get app platform-eso-config platform-argocd-config
```

1. 필요 시 ArgoCD 재평가/동기화를 수행한다.

```bash
argocd app get platform-eso-config --hard-refresh
argocd app get platform-argocd-config --hard-refresh
# operator-triggered reconciliation only
argocd app sync platform-eso-config
argocd app sync platform-argocd-config
```

1. 런타임 계약 회귀를 검증한다.

```bash
./infrastructure/tests/verify-network-policies.sh
./infrastructure/tests/verify-ingress-tls.sh
CHECK_TRAEFIK_443=true ./infrastructure/tests/verify-ingress-tls.sh
./infrastructure/tests/run-all.sh
```

1. CI 정적 계약 회귀를 검증한다.

```bash
./infrastructure/tests/verify-contracts-static.sh
bash -n infrastructure/bootstrap-local.sh infrastructure/tests/*.sh
```

1. GitOps source gate를 확인한다(로컬 파일 수정만으로 반영되지 않음).

```bash
kubectl -n argocd get app root-platform -o yaml | \
  rg 'path: gitops/apps/root|targetRevision: main'
```

## Verification Steps

- [ ] `vault-backend Ready=True`
- [ ] `argocd-external-valkey Ready=True`
- [ ] `platform-eso-config`, `platform-argocd-config` Degraded 해소
- [ ] 포트/서비스 계약 회귀 없음
- [ ] `argocd` egress(Valkey + DNS + HTTPS) 통과
- [ ] ingress/TLS 계약(host=`argocd.127.0.0.1.nip.io`, secret=`argocd-local-tls`) 유지 # pragma: allowlist secret
- [ ] ingress-nginx LoadBalancer IP 기반 HTTPS 응답 확인; 외부 Traefik 443
      확인은 gateway 런타임이 준비된 경우에만 별도 수행
- [ ] CI 정적 계약(`verify-contracts-static.sh`) 통과

## Observability and Evidence Sources

- **Signals**: ArgoCD Application health, ExternalSecret Ready status, ESO controller logs, repo-server logs.
- **Evidence to Capture**: failed sync output, ExternalSecret condition, Vault auth role read result, recovery command output.

### Troubleshooting Signatures

- `connection refused` on `vault-external.platform.svc.cluster.local:8200`
- `InvalidProviderConfig` in ESO controller logs
- `argocd-external-valkey SecretSyncedError`
- TLS handshake error due to SAN mismatch (`cert.pem`)

### SAN mismatch remediation

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg '127\.0\.0\.1\.nip\.io|\*\.127\.0\.0\.1\.nip\.io'
# 미포함 시 인증서 재발급 후 bootstrap 재실행
export VAULT_CA_FILE="$PWD/secrets/certs/rootCA.pem"
./infrastructure/bootstrap-local.sh
```

부트스트랩은 HTTPS와 읽기 가능한 `VAULT_CA_FILE`을 강제하고 토큰을
`/dev/tty`에서 표시 없이 입력받는다. 비대화형 또는 insecure fallback은 없다.

### Vault sealed remediation

`curl http://172.18.0.8:8200/v1/sys/health`가 `sealed:true`를 반환하거나 ESO 로그에 `Vault is sealed`가 반복되면 GitOps manifest를 변경하지 않는다.

- Vault operator가 unseal key shares를 사용해 Vault를 unseal한다.
- Agent는 unseal key, root token, Vault token, secret value를 조회하거나 기록하지 않는다.
- Unseal 후 `ClusterSecretStore/vault-backend`와 dependent `ExternalSecret` readiness metadata만 재검증한다.
- Unseal 후에도 `InvalidProviderConfig`가 지속되면 Kubernetes auth mount/role configuration drift를 별도 operator-bound task로 분리한다.

## Safe Rollback or Recovery Procedure

```bash
kubectl -n platform delete endpointslice vault-external-1
```

- 롤백 후 `verify-contracts-static.sh`와 `run-all.sh`를 재실행한다.
- 동일 증상이 반복되면 Operations 예외 승인 절차를 따른다.

### Agent Operations

이 런북은 인프라 절차를 다루며 AI Agent 모델/프롬프트 롤백이 직접 적용되지 않는다.
단, Agent가 이 런북을 자동화하는 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Traceability

- **Guide**: [`../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md`](../guides/0002-wsl2-k3d-argocd-ha-setup-guide.md)
- **Operations Policy**: [`../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md`](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- [`../../02.architecture/requirements/0007-current-local-gitops-platform.md`](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md)
- [`../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md`](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
