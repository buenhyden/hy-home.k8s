---
title: "Platform Expansion Bootstrap Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-11-20"
artifact_id: "RUN-0003"
---

# Platform Expansion Bootstrap Runbook

## 문서 개요

### 목적과 독자

이 런북은 Platform Expansion Bootstrap Runbook 작업이나 장애를 수행·복구할 운영자와 검토자에게 실제 절차를 제공한다. 시작 조건은 [Trigger](#trigger)에 기록한다.

### 책임과 적용 범위

platform은 이 절차의 운영 범위를 유지한다. 대상은 [Targets](#targets), 사전 조건과 권한은 [Preflight](#preflight), 실행·복구는 [Procedure](#procedure)에서 확인한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

이 런북은 기본 플랫폼 위에 추가된 cert-manager, Istio(현재 1.25.2), Kiali를 부트스트랩하거나 복구하기 위한 즉시 실행 가능한 체크리스트와 증상별 복구 절차를 제공한다.

- 신규 플랫폼 확장 컴포넌트 설치
- host 재시작 또는 k3d 클러스터 재생성 후 복구
- cert-manager ClusterIssuer NotReady 복구
- Istio/Kiali 배포 실패 복구

##### Targets

Ingress controller는 Traefik이며 Istio 업그레이드(ADR-0051)는 아직 실행되지 않았다.

기본 플랫폼 부트스트랩(`infrastructure/bootstrap-local.sh`, ArgoCD, ESO/OpenBao,
외부 서비스 endpoint)은 [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md),
Headlamp 검증·복구는 [RUN-0004](./0004-rollouts-notifications-headlamp-runbook.md),
Kiali와 외부 observability 연결 복구는
[RUN-0007](./0007-kiali-observability-connectivity-runbook.md)이 소유한다.

관련 문서: **Architecture**: [AD-0007](../../02.architecture/01.descriptions/0007-current-local-gitops-platform.md)

#### Preflight

##### Authority

플랫폼 운영자는 대상 클러스터와 승인 범위를 확인한다. CA Secret 재주입과
컨트롤러 재시작은 아래 Escalation의 bootstrap 또는 승인된 복구 조건을 따른다.

관련 문서: **Operations**: [`../policies/0003-service-mesh-cert-manager-policy.md`](../02.policies/0003-service-mesh-cert-manager-policy.md); **ADR-0014**: [`../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md`](../../02.architecture/02.decisions/0014-current-local-gitops-platform-contract.md); [`../../02.architecture/decisions/0006-cert-manager-mkcert-ca-issuer.md`](../../02.architecture/02.decisions/0006-cert-manager-mkcert-ca-issuer.md)

##### Environment

Steps의 Checklist에서 CA 입력과 외부 의존성을 확인한다. CA 개인 키는
승인된 Secret 입력에만 사용하고 명령 출력이나 운영 증적에 남기지 않는다.

#### Procedure

##### Steps

###### Checklist

- [ ] [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md) checklist와 bootstrap 완료
- [ ] `secrets/certs/rootCA.pem` 존재 (cert-manager용)
- [ ] `secrets/certs/rootCA-key.pem` 존재 (ClusterIssuer CA key)
- [ ] `rootCA.pem`이 로컬 신뢰 저장소에 등록됨
- [ ] Prometheus API (Kiali): `https://prometheus.hy.home.arpa/api/v1/status/buildinfo`가 인증 없이 `401`(Basic Auth, ADR-0046)
- [ ] Tempo 연결 (트레이싱): `nc -z 192.168.0.13 3200`
- [ ] Istio trace용 Alloy OTLP 연결: `nc -z 192.168.0.13 4317`
- [ ] Grafana (Kiali용): `https://grafana.hy.home.arpa/api/health`가 `200`

0. k8s router 이름 해석 확인

   Kiali 호스트명 `kiali.hy-k8s.home.arpa`는 k8s 전용 router(`192.168.0.14`)가
   받는다. 이름 해석이 그 주소를 가리키는지 확인한다. host 주소와 이름
   해석은 operator-approved 작업이며 통제는
   [POL-0001](../02.policies/0001-k8s-gitops-operations-policy.md)이 소유한다.

1. 기본 플랫폼 부트스트랩을 [RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)
   절차로 완료한다. `infrastructure/bootstrap-local.sh`가 cert-manager
   namespace와 `mkcert-root-ca` Secret을 함께 준비한다.

2. cert-manager ClusterIssuer 상태 확인

   ```bash
   kubectl -n cert-manager get deployment cert-manager
   test "$(kubectl get clusterissuer mkcert-ca-issuer \
     -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')" = True
   ```

3. Istio 가용성 확인

   ```bash
   kubectl get crd | grep istio.io | wc -l   # 10개 이상
   kubectl -n istio-system get deployment istiod
   ```

4. Kiali 가용성 + Prometheus 연결 확인

   ```bash
   kubectl -n istio-system get deployment kiali
   kubectl -n istio-system logs deploy/kiali | grep -i prometheus | tail -5
   ```

5. 아래 Verification의 정적 계약과 런타임 검사를 실행한다.

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 0 | k8s router 이름 해석 확인 | 이름 해석이 k8s router 192.168.0.14를 가리킨다 | 중단하고 Escalation의 Next Owner(서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자)와 Recovery or Forward Repair를 따른다 |
| 1 | 기본 플랫폼 부트스트랩을 RUN-0001 절차로 완료한다 | cert-manager namespace와 mkcert-root-ca Secret이 준비된다 | 중단하고 Escalation의 Next Owner(서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자)와 Recovery or Forward Repair를 따른다 |
| 2 | cert-manager ClusterIssuer 상태 확인 | ClusterIssuer mkcert-ca-issuer Ready=True | READY=False이면 cert-manager ClusterIssuer NotReady 복구 절차를 따른다; CA 입력을 복구할 수 없거나 승인된 조치 뒤에도 준비되지 않으면 서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자에게 넘긴다 |
| 3 | Istio 가용성 확인 | istio.io CRD 10개 이상, istiod deployment 가용 | CRD 없이 istiod 설치 오류이면 Istio CRD 복구 절차를 따르고, istiod CrashLoop/OOMKilled이면 해당 복구 절차를 따른다; 그 밖에는 중단하고 Escalation의 Next Owner(서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자)와 Recovery or Forward Repair를 따른다 |
| 4 | Kiali 가용성 + Prometheus 연결 확인 | kiali deployment 가용 | Kiali Prometheus 연결 오류는 RUN-0007을 따른다; 그 밖에는 중단하고 Escalation의 Next Owner(서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자)와 Recovery or Forward Repair를 따른다 |
| 5 | 아래 Verification의 정적 계약과 런타임 검사를 실행한다 | 정적 계약, ClusterIssuer, istiod·kiali deployment, TLS 접근 검사를 수행한다(기대 HTTP 코드는 이 문서에 명시 없음) | 중단하고 Escalation의 Next Owner(서비스 메시·cert-manager 운영 정책을 담당하는 플랫폼 운영자)와 Recovery or Forward Repair를 따른다 |

##### Stop Conditions

중단 조건: 별도 목록 없음 — 이 런북은 중단 조건을 한곳에 모으지 않으며, 단계 안의 확인 조건은 Steps에 두고 실패 시 Escalation의 Next Owner와 Recovery or Forward Repair를 따른다.

#### Verification

##### Expected Results

```bash
# 정적 계약
./scripts/validate-infrastructure-contracts.sh

# 런타임
kubectl get clusterissuer mkcert-ca-issuer
kubectl -n istio-system get deploy istiod kiali

# TLS 접근
curl --fail --silent --show-error --cacert secrets/certs/rootCA.pem \
  https://kiali.hy-k8s.home.arpa -o /dev/null -w '%{http_code}\n'
```

- **Signals**: ClusterIssuer readiness, Istiod/Kiali deployment availability, ArgoCD Application health.

##### Unverified Conditions

- **Evidence to Capture**: static contract output, relevant Kubernetes events, cert-manager logs, Kiali Prometheus connection logs.

##### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Service Mesh and cert-manager Operations Policy](../02.policies/0003-service-mesh-cert-manager-policy.md) | Initial expansion or recovery of cert-manager, Istio, or Kiali must preserve CA-secret, namespace-injection, and sync-wave controls. | Platform operator captures ClusterIssuer, ingress/TLS, deployment, and static-contract evidence; approved break-glass operator owns bounded recovery actions. |

#### Escalation

##### Next Owner

CA 입력을 복구할 수 없거나 승인된 조치 뒤에도 ClusterIssuer가 준비되지 않으면
[서비스 메시·cert-manager 운영 정책](../02.policies/0003-service-mesh-cert-manager-policy.md)을 담당하는 플랫폼 운영자에게 넘긴다.

##### Recovery or Forward Repair

확장 변경을 되돌릴 때는 operator-approved 범위와 적용 전 Git 리비전을 확인한다.
기본 플랫폼 변경은 [RUN-0001의 롤백 절차](./0001-argocd-platform-bootstrap-runbook.md#recovery-or-forward-repair)를
따른다. 확장 Application 설정을 되돌린 뒤 이 런북의 Expected Results로 영향받은
컴포넌트와 Git·ArgoCD 상태를 다시 대조한다.

##### Recovery Procedures

###### cert-manager ClusterIssuer NotReady

**증상**: `kubectl get clusterissuer mkcert-ca-issuer` → `READY=False`

> **Execution boundary**: Secret 재주입과 controller 재시작은 bootstrap 또는 human-approved break-glass 전용이다.

```bash
# 1. rootCA Secret 존재 확인
kubectl -n cert-manager get secret mkcert-root-ca

# 2. Secret 없으면 재주입 (bootstrap/break-glass only)
kubectl -n cert-manager create secret tls mkcert-root-ca \
  --cert=secrets/certs/rootCA.pem \
  --key=secrets/certs/rootCA-key.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. cert-manager controller 재시작
kubectl -n cert-manager rollout restart deploy/cert-manager

# 4. ClusterIssuer Ready=True 대기 (최대 60초)
kubectl wait clusterissuer mkcert-ca-issuer \
  --for=condition=Ready --timeout=60s
```

###### Istiod CrashLoop / OOMKilled

**증상**: `kubectl -n istio-system get pods -l app=istiod` → CrashLoopBackOff 또는 OOMKilled

```bash
# 1. 자원 사용량 확인
kubectl -n istio-system top pod -l app=istiod

# 2. istiod 자원 값은 gitops/apps/root/platform-istiod-app.yaml의 inline Helm values가 소유한다.
#    POL-0003은 requests를 cpu 100m, memory 128Mi 아래로 낮추지 않는다.
#    값 조정이 필요하면 해당 Application을 수정·커밋한 뒤 ArgoCD sync로 반영한다.

# 3. 재시작 (operator-approved restart only)
kubectl -n istio-system rollout restart deploy/istiod
```

###### Kiali "No Prometheus" 오류

Kiali의 Prometheus·Grafana·Tempo 연결 복구는
[RUN-0007](./0007-kiali-observability-connectivity-runbook.md)을 따른다.

###### Istio CRD 없이 istiod 설치 오류

**증상**: `platform-istiod` ArgoCD app sync 실패 — CRD not found

```bash
# 1. istio-base sync 상태 확인
argocd app get platform-istio-base

# 2. operator-triggered reconciliation only (sync-wave 강제). --prune은 리소스를 삭제하므로 operator 승인이 필요하다
argocd app sync platform-istio-base --prune

# 3. CRD 설치 확인 후 istiod sync
kubectl get crd | grep istio.io | wc -l
# operator-triggered reconciliation only
argocd app sync platform-istiod
```

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
