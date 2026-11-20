---
title: "ArgoCD ESO OpenBao Recovery Runbook"
version: "2.0.1"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-11-20"
artifact_id: "RUN-0002"
---

# ArgoCD ESO OpenBao Recovery Runbook

## 문서 개요

### 목적과 독자

이 런북은 ArgoCD ESO OpenBao Recovery Runbook 작업이나 장애를 수행·복구할 운영자와 검토자에게 실제 절차를 제공한다. 시작 조건은 [Trigger](#trigger)에 기록한다.

### 책임과 적용 범위

platform은 이 절차의 운영 범위를 유지한다. 대상은 [Targets](#targets), 사전 조건과 권한은 [Preflight](#preflight), 실행·복구는 [Procedure](#procedure)에서 확인한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

이 런북은 `ClusterSecretStore/vault-backend Ready=False` 상황에서 OpenBao
sealed 상태, 이름 해석 또는 CA drift, Kubernetes auth drift를 구분하고,
ArgoCD/ESO 상태를 정상화한 뒤 TLS/CI 계약 회귀를 점검하는 절차를 제공한다.

- `vault-backend`가 `Ready=False`
- ESO 로그에 `connection refused`, `no such host`, `x509`, `InvalidProviderConfig`, 또는 `context deadline exceeded` 반복
- ESO 로그에 `Vault is sealed`가 반복
- `argocd-external-valkey`가 `SecretSyncedError`
- 복구 후 ArgoCD HTTPS 진입점(`argo.hy-k8s.home.arpa`) 회귀가 의심될 때
- k3d cluster 재생성 뒤 OpenBao Kubernetes auth가 실패할 때

##### Targets

외부 secret backend는 OpenBao(ADR-0041)이며 Vault API 호환이다. 파일명과
`vault-*` 식별자는 호환성 때문에 유지한다. ESO는 외부 Traefik 뒤의
`https://openbao.hy.home.arpa`(host `192.168.0.13:443`)로 닿는다. cluster
안에서 그 이름은 CoreDNS custom zone(`kube-system/coredns-custom`)이 host
주소로 풀고, ESO는 `external-secrets/openbao-ca` ConfigMap의 mkcert root CA로
인증서를 검증한다(ADR-0046). `ClusterSecretStore/vault-backend`와 ESO `vault` provider는 기존
Kubernetes 식별자로 유지한다.

bootstrap `[7.3/11]` 단계가 만드는 CoreDNS custom zone과 gateway CA
ConfigMap(`openbao-ca`, `hy-home-root-ca`, `kiali-cabundle`)의 재적용은 이
런북의 Steps 4단계가 단일 owner다. Kiali, Alloy, Rollouts 런북은 이름
해석이나 `x509` 오류를 이 단계로 보낸다.

관련 문서: [`../../02.architecture/descriptions/0007-current-local-gitops-platform.md`](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)

#### Preflight

##### Authority

> **Agent execution boundary**: CoreDNS custom zone과 `openbao-ca` ConfigMap 재적용, OpenBao auth 설정 변경은 human-approved break-glass 전용이다. Agent는 기본적으로 사전 스냅샷, Git 파일 보정안, 검증 계획, 후속 증적 정리까지만 수행한다.

관련 문서: **Operations Policy**: [`../policies/0001-k8s-gitops-operations-policy.md`](../02.policies/0001-k8s-gitops-operations-policy.md); [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/02.decisions/0014-current-local-gitops-platform-contract.md); [`../../02.architecture/decisions/0046-external-services-over-host-addresses.md`](../../02.architecture/02.decisions/0046-external-services-over-host-addresses.md)

##### Environment

Steps의 Checklist를 확인하고, 변경할 각 ConfigMap의 적용 전 상태를 승인된 로컬 위치에 보관한다. 인증정보는 스냅샷·명령 출력·증적에 남기지 않는다.

#### Procedure

##### Steps

###### Checklist

- [ ] `kubectl` 컨텍스트 확인
- [ ] 평문 시크릿/토큰 출력 금지
- [ ] 복구 전 상태 스냅샷 수집
- [ ] 외부 OpenBao의 `eso-read-platform` role에 `bound_audiences=vault` 설정 확인(ESO token은 `vault`와 API server audience를 함께 요청한다)
- [ ] OpenBao Kubernetes auth `kubernetes_host`가 `https://192.168.0.13:6550`
- [ ] OpenBao policy가 `infrastructure/vault/policies/eso-read.hcl`의 경로만 읽기 허용

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
   증상이 난 소비자의 ConfigMap만 적용한다. CA ConfigMap을 바꿀 때는 먼저
   현재 CA bundle을 복구할 수 있는 승인된 입력과 대상·키를 확인한다.

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

   > **참고**: k3d API는 `kubernetes_host` 주소에만 bind하고 인증서 SAN에 그 주소를 둔다(`infrastructure/k3d/k3d-cluster.yaml`). cluster를 재생성하면 CA가 바뀌므로 OpenBao 운영자는 `kubernetes_ca_cert`를 새 CA로 갱신한다.

5. Store/ExternalSecret/ArgoCD 상태를 재평가한다.

   ```bash
   kubectl -n external-secrets get clustersecretstore vault-backend
   kubectl -n argocd get externalsecret argocd-external-valkey
   kubectl -n argocd get app platform-eso-config platform-argocd-config
   ```

6. 필요 시 ArgoCD 재평가/동기화를 수행한다.

   ```bash
   argocd app get platform-eso-config --hard-refresh   # operator-triggered refresh: 읽기 전용 점검이 아니라 Application 상태를 바꾼다
   argocd app get platform-argocd-config --hard-refresh
   # operator-triggered reconciliation only
   argocd app sync platform-eso-config
   argocd app sync platform-argocd-config
   ```

7. 복구한 경로에 해당하는 라이브 계약을 운영자가 선택해 검증한다. ESO
   readiness는 아래 `Verification`의 metadata 조회로 확인하고,
   NetworkPolicy와 ingress/TLS를 수정한 경우에만 각 검증 스크립트를
   실행한다. 모든 live 전제가 충족된 별도 전체 플랫폼 수용 작업에서만
   `infrastructure/verify/run-all.sh`를 사용한다.

   NetworkPolicy를 수정했다면:

   ```bash
   ./infrastructure/verify/verify-network-policies.sh
   ```

   ingress/TLS를 수정했다면:

   ```bash
   ./infrastructure/verify/verify-ingress-tls.sh
   ```

   k8s router 주소가 host에 할당되어 있고 그 경로도 변경했다면
   `CHECK_K8S_ROUTER=true ./infrastructure/verify/verify-ingress-tls.sh`로
   추가 확인한다. 각 호출의 실제 입력과 결과를 Task 또는 사건 기록에 남긴다.

8. 저장소 정적 계약 회귀를 검증한다.

   ```bash
   ./scripts/validate-infrastructure-contracts.sh
   python3 scripts/validate-vault-eso-contracts.py --root .
   for f in infrastructure/bootstrap-local.sh infrastructure/verify/*.sh; do bash -n "$f"; done
   ```

9. GitOps source gate를 확인한다(로컬 파일 수정만으로 반영되지 않음).
   [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md) 절차 6의 루트 앱
   `source.path`·`targetRevision` 검사 두 줄을 그대로 다시 실행하고, 둘 다
   통과해야 Verification으로 넘어간다.

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 사전 스냅샷을 저장한다 | 변경 전 `coredns-custom` 구성이 승인된 로컬 위치에 저장되고 Store·ExternalSecret·App 상태와 ESO 오류 신호를 비밀값 없이 기록한다 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 2 | sealed 상태, 경로, 인증서를 먼저 분류한다 | health·CoreDNS·CA·ESO 오류 결과로 sealed, 외부 runtime, DNS, TLS 또는 auth 실패 경로가 구분된다. 조회 실패는 정상으로 판정하지 않는다 | sealed:true이면 cluster 설정을 수정하지 않고 OpenBao unseal이 먼저다; host에서 sys/health가 응답하지 않으면 외부 workspace 운영자에게 넘긴다; 그 밖에는 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 3 | OpenBao가 sealed 상태면 operator-bound unseal 절차를 수행한다 | 승인된 OpenBao 운영자가 unseal한 경우 health가 `sealed:false`를 보이고 Store·ExternalSecret의 readiness metadata를 다시 확인한다 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 4 | 이름 해석이나 CA drift가 확인된 경우에만 bootstrap [7.3/11]과 같은 입력으로 다시 적용한다 | 승인된 대상 ConfigMap만 재적용되고 재조회에서 해당 DNS 또는 CA 오류가 사라진다. 재조회 전에는 복구 성공으로 판정하지 않는다 | CoreDNS custom zone 재적용이 상황을 악화시키면 Steps 1단계의 스냅샷으로 되돌린다; CA bundle 이전 입력이 없거나 신뢰를 확인할 수 없으면 CA 소유자에게 넘긴다 |
| 5 | Store/ExternalSecret/ArgoCD 상태를 재평가한다 | vault-backend Ready=True, argocd-external-valkey Ready=True | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 6 | 필요 시 ArgoCD 재평가/동기화를 수행한다 | platform-eso-config, platform-argocd-config Degraded 해소 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 7 | 복구한 경로에 해당하는 라이브 계약을 운영자가 선택해 검증한다 | 포트/서비스 계약 회귀 없음, argocd·external-secrets egress 통과, ingress/TLS 계약 유지 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 8 | 저장소 정적 계약 회귀를 검증한다 | 선택한 저장소 정적 계약 통과 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |
| 9 | GitOps source gate를 확인한다 | RUN-0001 절차 6의 source.path·targetRevision 검사 두 줄이 모두 통과한다 | 중단하고 Escalation의 Next Owner(동일 증상이 반복되면 Operations 예외 승인 절차)와 Recovery or Forward Repair를 따른다 |

##### Stop Conditions

중단 조건: 별도 목록 없음 — 이 런북은 중단 조건을 한곳에 모으지 않으며, 단계 안의 확인 조건은 Steps에 두고 실패 시 Escalation의 Next Owner와 Recovery or Forward Repair를 따른다.

#### Verification

##### Expected Results

- [ ] `vault-backend Ready=True`
- [ ] `argocd-external-valkey Ready=True`
- [ ] `platform-eso-config`, `platform-argocd-config` Degraded 해소
- [ ] 포트/서비스 계약 회귀 없음
- [ ] `argocd` egress(Valkey `192.168.0.13:26379` + DNS + HTTPS) 통과
- [ ] `external-secrets` egress(`192.168.0.13:443` + DNS) 통과
- [ ] ingress/TLS 계약(host=`argo.hy-k8s.home.arpa`, secret=`argocd-local-tls`) 유지 # pragma: allowlist secret
- [ ] Traefik LoadBalancer IP(Service `traefik/traefik`) 기반 HTTPS 응답 확인; k8s router
      (`192.168.0.14:443`) 확인은 host 주소가 할당된 경우에만 별도 수행
- [ ] 선택한 저장소 정적 계약(`./scripts/validate-infrastructure-contracts.sh`) 통과

- **Signals**: ArgoCD Application health, ExternalSecret Ready status, ESO controller logs, CoreDNS logs, repo-server logs.

##### Unverified Conditions

- **Evidence to Capture**: failed sync output, ExternalSecret condition, OpenBao auth role read result, recovery command output.

##### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [K8s GitOps Platform Operations Policy](../02.policies/0001-k8s-gitops-operations-policy.md) | `vault-backend` or dependent ExternalSecrets are not Ready because sealed state, name resolution or CA drift, or Kubernetes-auth drift must be distinguished. | Platform operator records secret-safe snapshots and readiness metadata; external OpenBao operator owns unseal/auth changes, and approved break-glass owners reconcile CoreDNS and CA changes back to Git. |

#### Escalation

##### Next Owner

이 저장소의 운영 비상 연락·승인 담당자는 [Stage 05 Owners](../README.md#owners)를 따른다. 담당자 지정은 이 절차의 개별 실행 승인이 아니다.

- 동일 증상이 반복되면 Operations 예외 승인 절차를 따른다.

##### Recovery or Forward Repair

CoreDNS custom zone 재적용이 상황을 악화시키면 Steps 1단계의 스냅샷으로
되돌린다. zone을 삭제하면 cluster 안에서 `openbao`, `prometheus`,
`grafana` 이름 해석이 모두 끊기므로 기존 zone을 복구한다. CA ConfigMap의
변경을 되돌릴 때는 변경 전과 일치하는 승인된 CA bundle을 같은 대상과 키에
적용한다. 이전 입력이 없거나 신뢰를 확인할 수 없으면 CA 소유자에게 넘긴다.

```bash
# human-approved break-glass only
kubectl apply -f "${TMPDIR:-/tmp}/coredns-custom.before.yaml"
kubectl -n kube-system rollout restart deployment/coredns
```

- 롤백 후 변경한 입력에 해당하는 정적 계약과 위 선택 live 검사를 다시
  확인한다. 전체 플랫폼 수용 검사가 필요한 별도 작업만 `run-all.sh`를 수행한다.

##### Recovery Procedures

###### Troubleshooting Signatures

- `openbao.hy.home.arpa`에 대한 `no such host`: CoreDNS custom zone이 없거나 로드되지 않았다.
- `x509: certificate signed by unknown authority`: `openbao-ca` ConfigMap이 없거나 오래되었다.
- `192.168.0.13:443`에 대한 `connection refused`: 외부 Traefik이 host 주소에 bind되지 않았다.
- ESO controller 로그의 `InvalidProviderConfig`
- `kubernetes_host`와 CA가 최신인데도 `auth/kubernetes/login`이 `403 permission denied`: ESO token에 API server audience가 없다. OpenBao에는 reviewer JWT가 없어 그 token을 자기 credential로 TokenReview에 보내고, API server는 `vault`만 가진 token에 `401`을 돌려준다. `vault-backend`는 `gitops/platform/eso/vault-secret-store.yaml`에서 두 audience(`vault`, `https://kubernetes.default.svc.cluster.local`)를 모두 유지한다.
- `argocd-external-valkey SecretSyncedError`
- `cert.pem` SAN 불일치로 인한 TLS handshake 오류

###### SAN mismatch remediation

```bash
openssl x509 -in secrets/certs/cert.pem -noout -ext subjectAltName | \
  rg 'argo\.hy-k8s\.home\.arpa|\*\.hy-k8s\.home\.arpa'
```

SAN이 없으면 인증서를 재발급한 뒤
[RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)의 bootstrap 절차를 다시 실행한다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
