---
title: "ArgoCD ESO Vault Recovery Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "operations"
artifact_id: "RUN-0002"
---

# ArgoCD ESO Vault Recovery Runbook

## Overview

외부 secret backend는 Vault API 호환 OpenBao다. ESO는 외부 Traefik 뒤의
`https://openbao.hy.home.arpa`(host `192.168.0.13:443`)로 닿는다. cluster
안에서 그 이름은 CoreDNS custom zone(`kube-system/coredns-custom`)이 host
주소로 풀고, ESO는 `external-secrets/openbao-ca` ConfigMap의 mkcert root CA로
인증서를 검증한다(ADR-0046). `vault-backend`와 ESO `vault` provider는 기존
Kubernetes 식별자로 유지한다.

이 런북은 `ClusterSecretStore/vault-backend Ready=False` 상황에서 OpenBao
sealed 상태, 이름 해석 또는 CA drift, Kubernetes auth drift를 구분하고,
ArgoCD/ESO 상태를 정상화한 뒤 TLS/CI 계약 회귀를 점검하는 절차를 제공한다.

bootstrap `[7.3/11]` 단계가 만드는 CoreDNS custom zone과 gateway CA
ConfigMap(`openbao-ca`, `hy-home-root-ca`, `kiali-cabundle`)의 재적용은 이
런북의 Procedure 4단계가 단일 owner다. Kiali, Alloy, Rollouts 런북은 이름
해석이나 `x509` 오류를 이 단계로 보낸다.

> **Agent execution boundary**: CoreDNS custom zone과 `openbao-ca` ConfigMap 재적용, OpenBao auth 설정 변경은 human-approved break-glass 전용이다. Agent는 기본적으로 사전 스냅샷, Git 파일 보정안, 검증 계획, 후속 증적 정리까지만 수행한다.

### Purpose

OpenBao 연결 거부, 이름 해석 실패, 인증서 검증 실패, sealed 상태, 또는
Kubernetes auth drift로 발생하는 ESO/OpenBao 연동 장애를 빠르게 분류하고,
operator-bound 복구 절차와 계약 회귀 검증을 연결한다.

## Runbook Type

`recovery`

## When to Use

- `vault-backend`가 `Ready=False`
- ESO 로그에 `connection refused`, `no such host`, `x509`, `InvalidProviderConfig`, 또는 `context deadline exceeded` 반복
- ESO 로그에 `Vault is sealed`가 반복
- `argocd-external-valkey`가 `SecretSyncedError`
- 복구 후 ArgoCD HTTPS 진입점(`argo.hy-k8s.home.arpa`) 회귀가 의심될 때
- k3d cluster 재생성 뒤 OpenBao Kubernetes auth가 실패할 때

## Procedure or Checklist

### Checklist

- [ ] `kubectl` 컨텍스트 확인
- [ ] 평문 시크릿/토큰 출력 금지
- [ ] 복구 전 상태 스냅샷 수집
- [ ] 외부 OpenBao의 `eso-read-platform` role에 `bound_audiences=vault` 설정 확인
- [ ] OpenBao Kubernetes auth `kubernetes_host`가 `https://192.168.0.13:6550`

### Procedure

1. 사전 스냅샷을 저장한다.

   ```bash
   kubectl get clustersecretstore vault-backend -o yaml
   kubectl -n kube-system get configmap coredns-custom -o yaml > "${TMPDIR:-/tmp}/coredns-custom.before.yaml"
   kubectl -n argocd get externalsecret argocd-external-valkey -o yaml
   kubectl -n argocd get app platform-eso-config platform-argocd-config -o wide
   kubectl -n external-secrets logs deploy/external-secrets --tail=200 | \
     rg -i 'vault|clustersecretstore|error|connection refused|no such host|x509|sealed'
   ```

2. sealed 상태, 경로, 인증서를 먼저 분류한다.

   ```bash
   curl -sS --max-time 5 --cacert secrets/certs/rootCA.pem \
     https://openbao.hy.home.arpa/v1/sys/health
   kubectl -n kube-system get configmap coredns-custom -o yaml
   kubectl -n external-secrets get configmap openbao-ca
   kubectl -n external-secrets logs deploy/external-secrets --since=2h --tail=80 | \
     rg -i 'Vault is sealed|connection refused|no such host|x509|context deadline|permission denied|invalid'
   ```

   판정 기준:

   - `sys/health`가 `sealed:true`이고 ESO 로그가 `Vault is sealed`를 보이면 cluster 설정을 수정하지 않는다. OpenBao unseal이 먼저다.
   - host에서 `sys/health`가 응답하지 않으면 외부 Traefik이나 OpenBao runtime 문제다. 외부 workspace 운영자에게 넘긴다.
   - host에서는 응답하는데 ESO가 `no such host`를 보이면 CoreDNS custom zone을, `x509`를 보이면 `openbao-ca` ConfigMap을 확인한다.
   - `sys/health`가 `sealed:false`인데 Kubernetes auth login이 실패하면 OpenBao auth mount, role, `kubernetes_host`, TokenReview reviewer 설정을 operator-bound로 재검토한다.

3. OpenBao가 sealed 상태면 operator-bound unseal 절차를 수행한다. Agent는
   unseal key, root token, OpenBao token, secret value를 요청하거나 출력하지
   않는다. OpenBao 운영자는 승인된 비밀 입력 채널을 사용하고 credential을
   명령 인자, 셸 환경, 채팅, Git, 로그, PR 본문에 넣지 않는다.

   unseal 후에는 secret 값을 조회하지 말고 readiness metadata만 확인한다.

   ```bash
   curl -sS --max-time 5 --cacert secrets/certs/rootCA.pem \
     https://openbao.hy.home.arpa/v1/sys/health
   kubectl -n external-secrets get clustersecretstore vault-backend
   kubectl -n argocd get externalsecret argocd-external-valkey
   ```

4. 이름 해석이나 CA drift가 확인된 경우에만 bootstrap `[7.3/11]`과 같은
   입력으로 다시 적용한다. 이 단계는 human-approved break-glass 전용이다.
   증상이 난 소비자의 ConfigMap만 적용해도 된다.

   ```bash
   # human-approved break-glass only
   kubectl apply -f infrastructure/coredns-custom.yaml
   kubectl -n kube-system rollout restart deployment/coredns
   kubectl -n external-secrets create configmap openbao-ca \
     --from-file=ca.crt=secrets/certs/rootCA.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   for ns in monitoring argo-rollouts; do
     kubectl -n "$ns" create configmap hy-home-root-ca \
       --from-file=ca.crt=secrets/certs/rootCA.pem \
       --dry-run=client -o yaml | kubectl apply -f -
   done
   kubectl -n istio-system create configmap kiali-cabundle \
     --from-file=additional-ca-bundle.pem=secrets/certs/rootCA.pem \
     --dry-run=client -o yaml | kubectl apply -f -
   ```

   > **참고**: OpenBao Kubernetes auth `kubernetes_host`는 `https://192.168.0.13:6550`이다. k3d API는 그 주소에만 bind하고 인증서 SAN에 그 주소를 둔다(`infrastructure/k3d/k3d-cluster.yaml`). cluster를 재생성하면 CA가 바뀌므로 OpenBao 운영자는 `kubernetes_ca_cert`를 새 CA로 갱신한다.

5. Store/ExternalSecret/ArgoCD 상태를 재평가한다.

   ```bash
   kubectl -n external-secrets get clustersecretstore vault-backend
   kubectl -n argocd get externalsecret argocd-external-valkey
   kubectl -n argocd get app platform-eso-config platform-argocd-config
   ```

6. 필요 시 ArgoCD 재평가/동기화를 수행한다.

   ```bash
   argocd app get platform-eso-config --hard-refresh
   argocd app get platform-argocd-config --hard-refresh
   # operator-triggered reconciliation only
   argocd app sync platform-eso-config
   argocd app sync platform-argocd-config
   ```

7. 런타임 계약 회귀를 검증한다.

   ```bash
   ./infrastructure/verify/verify-network-policies.sh
   ./infrastructure/verify/verify-ingress-tls.sh
   CHECK_K8S_ROUTER=true ./infrastructure/verify/verify-ingress-tls.sh
   ./infrastructure/verify/run-all.sh
   ```

8. CI 정적 계약 회귀를 검증한다.

   ```bash
   ./scripts/validate-infrastructure-contracts.sh
   python3 scripts/validate-vault-eso-contracts.py --root .
   for f in infrastructure/bootstrap-local.sh infrastructure/verify/*.sh; do bash -n "$f"; done
   ```

9. GitOps source gate를 확인한다(로컬 파일 수정만으로 반영되지 않음).

   ```bash
   kubectl -n argocd get app root-platform -o yaml | \
     rg 'path: gitops/apps/root|targetRevision: main'
   ```

## Verification Steps

- [ ] `vault-backend Ready=True`
- [ ] `argocd-external-valkey Ready=True`
- [ ] `platform-eso-config`, `platform-argocd-config` Degraded 해소
- [ ] 포트/서비스 계약 회귀 없음
- [ ] `argocd` egress(Valkey `192.168.0.13:26379` + DNS + HTTPS) 통과
- [ ] `external-secrets` egress(`192.168.0.13:443` + DNS) 통과
- [ ] ingress/TLS 계약(host=`argo.hy-k8s.home.arpa`, secret=`argocd-local-tls`) 유지 # pragma: allowlist secret
- [ ] ingress-nginx LoadBalancer IP 기반 HTTPS 응답 확인; k8s router
      (`192.168.0.14:443`) 확인은 host 주소가 할당된 경우에만 별도 수행
- [ ] CI 정적 계약(`./scripts/validate-infrastructure-contracts.sh`) 통과

## Observability and Evidence Sources

- **Signals**: ArgoCD Application health, ExternalSecret Ready status, ESO controller logs, CoreDNS logs, repo-server logs.
- **Evidence to Capture**: failed sync output, ExternalSecret condition, OpenBao auth role read result, recovery command output.

### Troubleshooting Signatures

- `no such host` for `openbao.hy.home.arpa`: CoreDNS custom zone missing or not loaded
- `x509: certificate signed by unknown authority`: `openbao-ca` ConfigMap missing or stale
- `connection refused` on `192.168.0.13:443`: external Traefik not bound to the host address
- `InvalidProviderConfig` in ESO controller logs
- `403 permission denied` on `auth/kubernetes/login` although `kubernetes_host` and the CA are current: the ESO token lacks the API server audience. OpenBao has no reviewer JWT, so it sends that token to TokenReview as its own credential, and the API server answers `401` to a token scoped only to `vault`. `vault-backend` keeps both audiences (`vault`, `https://kubernetes.default.svc.cluster.local`).
- `argocd-external-valkey SecretSyncedError`
- TLS handshake error due to SAN mismatch (`cert.pem`)

### SAN mismatch remediation

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg 'argo\.hy-k8s\.home\.arpa|\*\.hy-k8s\.home\.arpa'
```

SAN이 없으면 인증서를 재발급한 뒤
[RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)의 bootstrap 절차를 다시 실행한다.

## Safe Rollback or Recovery Procedure

CoreDNS custom zone 재적용이 상황을 악화시키면 Procedure 1단계의 스냅샷으로
되돌린다. zone을 삭제하면 cluster 안에서 `openbao`, `prometheus`,
`grafana` 이름 해석이 모두 끊기므로 삭제로 롤백하지 않는다. CA
ConfigMap은 같은 `rootCA.pem`으로 다시 적용하는 것이 롤백이다.

```bash
# human-approved break-glass only
kubectl apply -f "${TMPDIR:-/tmp}/coredns-custom.before.yaml"
kubectl -n kube-system rollout restart deployment/coredns
```

- 롤백 후 `./scripts/validate-infrastructure-contracts.sh`와 `run-all.sh`를 재실행한다.
- 동일 증상이 반복되면 Operations 예외 승인 절차를 따른다.

## Traceability

- **Operations Policy**: [`../policies/0001-k8s-gitops-operations-policy.md`](../policies/0001-k8s-gitops-operations-policy.md)
- [`../../02.architecture/descriptions/0007-current-local-gitops-platform.md`](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- [`../../02.architecture/decisions/0046-external-services-over-host-addresses.md`](../../02.architecture/decisions/0046-external-services-over-host-addresses.md)
- [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [K8s GitOps Platform Operations Policy](../policies/0001-k8s-gitops-operations-policy.md) | `vault-backend` or dependent ExternalSecrets are not Ready because sealed state, name resolution or CA drift, or Kubernetes-auth drift must be distinguished. | Platform operator records secret-safe snapshots and readiness metadata; external OpenBao operator owns unseal/auth changes, and approved break-glass owners reconcile CoreDNS and CA changes back to Git. |
