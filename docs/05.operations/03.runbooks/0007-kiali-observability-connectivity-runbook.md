---
title: "Kiali Observability 연결 복구 Runbook"
version: "3.0.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-11-20"
artifact_id: "RUN-0007"
---

# Kiali Observability 연결 복구 Runbook

## 문서 개요

### 목적과 독자

이 런북은 Kiali Observability 연결 복구 Runbook 작업이나 장애를 수행·복구할 운영자와 검토자에게 실제 절차를 제공한다. 시작 조건은 [Trigger](#trigger)에 기록한다.

### 책임과 적용 범위

platform은 이 절차의 운영 범위를 유지한다. 대상은 [Targets](#targets), 사전 조건과 권한은 [Preflight](#preflight), 실행·복구는 [Procedure](#procedure)에서 확인한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Trigger and Scope

##### Trigger

이 런북은 Kiali에서 Grafana, Prometheus, Tempo 등 외부 관측성 서비스가 Unreachable로 표시되는 장애를 진단하고 복구하는 절차를 제공한다.

주된 원인은 세 가지다:

1. **외부 경로 drift**: Kiali는 Prometheus API(`https://prometheus.hy.home.arpa`, Basic Auth)와 Grafana(`https://grafana.hy.home.arpa`)를 외부 Traefik으로 호출한다(ADR-0046). 이름 해석(CoreDNS custom zone), gateway CA(`istio-system/kiali-cabundle`), Basic Auth Secret(`istio-system/kiali-prometheus-auth`) 중 하나가 어긋나거나 외부 workspace가 route를 바꾸면 연결이 끊긴다.
2. **Tempo endpoint drift**: Tempo는 `tempo-external` Service와 EndpointSlice를 거쳐 host port `192.168.0.13:3200`으로 닿는다. EndpointSlice는 ArgoCD Application `platform-external-services`가 Git에서 관리한다.
3. **Grafana 인증 실패**: 외부 Grafana는 익명 API 접근을 허용하지 않는다. Kiali는 Grafana Viewer service account token(`istio-system/kiali-grafana-auth`, OpenBao `platform/grafana-api`)을 bearer로 보낸다. token이 없거나 만료·폐기되면 `/api/frontend/settings`가 401을 반환하고 Kiali는 Grafana를 Unreachable로 표시한다.

- Kiali에서 Grafana/Prometheus/Tempo가 unreachable로 표시될 때
- 외부 workspace가 관측 서비스의 route, host port 공개나 bind 주소를 바꾼 뒤
- `kubectl get endpointslice -n platform`에서 `tempo-external-1`의 주소가 비어있거나 없을 때

##### Targets

로컬 `k3d-hyhome`의 `istio-system` Kiali에서 외부 Prometheus, Grafana 및
Tempo로 이어지는 경로를 점검한다. 외부 서비스 설정 변경은 해당 운영자가 담당한다.

관련 문서: **k8s Observability Runbook**: [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md); **External Services**: [`../../../gitops/platform/external-services`](../../../gitops/platform/external-services)

#### Preflight

##### Authority

플랫폼 운영자는 대상 kube context와 Kiali 접근 권한을 확인한다. 재조정,
일회성 DNS 진단 Pod 생성·삭제, Kiali 재시작은 해당 작업의 별도 승인 범위에서 수행한다.

관련 문서: **Operations Policy**: [`../policies/0005-observability-platform-operations-policy.md`](../02.policies/0005-observability-platform-operations-policy.md)

##### Environment

DNS 진단 Pod는 승인된 `istio-system` namespace와 사용 가능한 Pod 이름을
확인한 뒤 사용한다. 인증정보 대신 Secret 동기화 상태와 필요한 연결 결과를 남긴다.

#### Procedure

##### Steps

아래 절차는 외부 route와 host port 확인, Kiali 파드 연결 테스트, NetworkPolicy 점검, Kiali 설정 확인, Grafana auth 확인 순서로 수행한다.

###### Kiali 외부 의존 계약표 (ADR-0046)

| 대상 | 경로 | 인증 |
| --- | --- | --- |
| Prometheus API | `https://prometheus.hy.home.arpa/api/v1/` (외부 Traefik `192.168.0.13:443`) | Basic Auth |
| Grafana | `https://grafana.hy.home.arpa` (외부 Traefik `192.168.0.13:443`) | Viewer service account token (bearer) |
| Tempo | `tempo-external` → host `192.168.0.13:3200` | 없음 |

> 닫혀 있거나 route가 응답하지 않으면 이 저장소가 아니라 외부 workspace의 route와 port 공개를 먼저 확인한다.

###### Procedure 1: 연결 상태 진단

<a id="1-1-외부-route와-host-port-확인-linux-server-host에서"></a>

**1-1. 외부 route와 host port 확인 (Linux server host에서)**

```bash
# 인증 없이 401이면 Prometheus API route가 살아 있다
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://grafana.hy.home.arpa/api/health
docker ps --format '{{.Names}}\t{{.Ports}}' | rg 'infra-tempo'
```

<a id="1-2-kiali-파드에서-직접-연결-테스트"></a>

**1-2. Kiali 파드에서 직접 연결 테스트**

`nc`는 Kiali 컨테이너 내에서 오동작할 수 있으므로 반드시 `bash /dev/tcp`를 사용한다.

```bash
KIALI_POD=$(kubectl get pod -n istio-system -l app=kiali -o jsonpath='{.items[0].metadata.name}')

# 외부 Traefik(Prometheus API, Grafana) 연결 테스트
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/192.168.0.13/443" && echo OK || echo FAIL'

# Tempo 연결 테스트
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/192.168.0.13/3200" && echo OK || echo FAIL'

# 이름 해석과 CA·자격 증명 준비
kubectl -n kube-system get configmap coredns-custom -o yaml | rg 'prometheus|grafana'
kubectl -n istio-system get configmap kiali-cabundle
kubectl -n istio-system get externalsecret kiali-prometheus-auth
```

`coredns-custom`이나 `kiali-cabundle`이 없거나 Kiali 로그에 `no such host`,
`x509`가 보이면 [RUN-0002](./0002-argocd-eso-vault-recovery-runbook.md)의
Steps 4단계로 재적용한다.

<a id="1-3-tempo-endpointslice-확인"></a>

**1-3. Tempo EndpointSlice 확인**

```bash
kubectl -n platform get endpointslice tempo-external-1
```

주소가 `192.168.0.13`이 아니거나 port가 `3200`이 아니면
[RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)의 External Endpoint
Recovery 절차로 복구한다.

###### Procedure 2: NetworkPolicy egress 규칙 점검

NetworkPolicy의 egress `ipBlock` 규칙은 **post-DNAT 기준 IP**로 작성해야 한다. Kiali egress는 host 주소 `192.168.0.13/32`의 `443`, `3200`을 허용한다(ADR-0046).

```bash
kubectl -n istio-system get networkpolicy allow-kiali-egress-to-observability -o yaml | \
  rg -A8 ipBlock
```

수정이 필요하면 `gitops/platform/network-policies/` 하위 YAML을 고쳐 PR로 반영한 뒤 reconciliation한다.

```bash
# operator-triggered reconciliation only
argocd app sync platform-network-policies
```

###### Procedure 3: Kiali 외부 서비스 설정 확인

Kiali의 외부 서비스 설정은 `gitops/apps/root/platform-kiali-app.yaml`의 `cr.spec.external_services`가 소유한다.

```bash
kubectl get app platform-kiali -n argocd -o jsonpath='{.spec.source.helm.values}'
rg -n 'url|in_cluster_url' gitops/apps/root/platform-kiali-app.yaml
kubectl get configmap kiali -n istio-system -o yaml | rg -A3 'grafana|prometheus|tracing'
```

현재 계약은 Grafana의 `in_cluster_url`과 브라우저 링크 `url` 모두 외부 Traefik의 `https://grafana.hy.home.arpa`, Prometheus `url`은 `https://prometheus.hy.home.arpa`, Tempo `in_cluster_url`은 `http://tempo-external.platform.svc.cluster.local:3200`이다. 값이 다르면 그 Application 파일을 고쳐 PR로 반영한 뒤 reconciliation한다.

```bash
# operator-triggered reconciliation only
argocd app sync platform-kiali
```

###### Troubleshooting

<a id="nc-명령이-kiali-파드-내에서-항상-ok를-반환한다"></a>

**`nc` 명령이 Kiali 파드 내에서 항상 OK를 반환한다**

Kiali 기본 이미지의 `nc`(BusyBox)는 특정 옵션에서 오동작할 수 있다. Procedure 1-2의 `bash /dev/tcp` 방식을 사용한다.

<a id="경로endpointegress가-맞는데도-연결이-안-된다"></a>

**경로·endpoint·egress가 맞는데도 연결이 안 된다**

1. cluster DNS가 외부 이름을 host 주소로 해석하는지 확인한다.

   클러스터 내부 DNS 검사가 필요하고 진단 Pod 생성과 삭제가 승인된 경우에만
   아래를 실행한다. 명령이 중단되면 같은 context와 namespace에서 Pod 정리를 확인한다.

   ```bash
   # operator-approved temporary DNS probe Pod only
   kubectl --context=k3d-hyhome -n istio-system run -it --rm kiali-dns-check \
     --image=busybox:1.36 --restart=Never -- \
     nslookup grafana.hy.home.arpa
   ```

2. Kiali 파드를 재시작하여 캐시를 초기화한다.

   ```bash
   # operator-approved restart only
   kubectl rollout restart deployment/kiali -n istio-system
   ```

<a id="kiali-로그에-grafana-version-check-failed-code401가-반복된다"></a>

**Kiali 로그에 `grafana version check failed: code=[401]`가 반복된다**

**원인**: Kiali가 보내는 Grafana service account token이 없거나 만료·폐기되었다. 외부 Grafana는 익명 API 접근을 허용하지 않는다.

Kiali는 내부 URL로 `/api/frontend/settings`를 호출해 Grafana 버전을 확인한다. 이 엔드포인트가 401을 반환하면 Kiali는 Grafana를 Unreachable로 표시한다.

**확인:**

```bash
kubectl -n istio-system logs deploy/kiali --since=5m | rg -i 'grafana|401'
# 예: grafana version check failed: url=[.../api/frontend/settings], code=[401]
```

**해결**: token은 외부 observability workspace가 Grafana Viewer service account로
발급하고 OpenBao `platform/grafana-api.token`에 둔다. 이 저장소는 ESO로 받아 쓰기만 한다.

1. `kubectl -n istio-system get externalsecret kiali-grafana-auth`가 Ready인지 확인한다.
2. Ready가 아니면 외부 workspace에 KV 값이나 policy 경로를 확인하도록 요청한다.
3. 401이 계속되면 token이 폐기되었거나 role이 Viewer 미만이다. 외부 workspace가
   token을 재발급하고 KV를 갱신한다. ESO는 `refreshInterval: 1h` 안에 따라간다.

**검증:**

```bash
# 익명 호출은 401이 정상이다 (Grafana가 익명 접근을 허용하지 않는다)
curl -s -o /dev/null -w "%{http_code}" --cacert secrets/certs/rootCA.pem \
  https://grafana.hy.home.arpa/api/frontend/settings
kubectl -n istio-system get externalsecret kiali-grafana-auth

# Kiali 로그에서 401 오류 사라짐 확인
kubectl -n istio-system logs deploy/kiali --since=2m | rg -i 'grafana|401'
```

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | 연결 상태 진단(1-1 외부 route와 host port, 1-2 Kiali 파드 연결, 1-3 Tempo EndpointSlice 확인) | Kiali pod에서 192.168.0.13:443과 192.168.0.13:3200 TCP 연결 성공, tempo-external-1 주소 192.168.0.13과 port 3200 | 1-2에서 coredns-custom이나 kiali-cabundle이 없거나 no such host, x509가 보이면 RUN-0002 Steps 4단계로 재적용한다; 1-3에서 주소나 port가 다르면 RUN-0001 External Endpoint Recovery로 복구한다; 닫혀 있거나 route가 응답하지 않으면 외부 workspace의 route와 port 공개를 먼저 확인한다 |
| 2 | NetworkPolicy egress 규칙 점검 | allow-kiali-egress-to-observability가 192.168.0.13/32의 443, 3200을 허용한다 | gitops/platform/network-policies 하위 YAML을 고쳐 PR로 반영한 뒤 reconciliation한다; 새 주소나 port 매핑이 틀리면 GitOps로 되돌린다 |
| 3 | Kiali 외부 서비스 설정 확인 | Kiali 로그에 Grafana 401이나 Prometheus 연결 오류가 없다 | 값이 다르면 Application 파일을 고쳐 PR로 반영한 뒤 reconciliation한다; Grafana auth 변경은 외부 observability workspace 소관이며 이 저장소는 결과만 확인한다 |

##### Stop Conditions

중단 조건: 별도 목록 없음 — 이 런북은 중단 조건을 한곳에 모으지 않으며, 단계 안의 확인 조건은 Steps에 두고 실패 시 Escalation의 Next Owner와 Recovery or Forward Repair를 따른다.

#### Verification

##### Expected Results

- [ ] Kiali pod에서 `192.168.0.13:443`과 `192.168.0.13:3200` TCP 연결이 성공한다.
- [ ] `tempo-external-1` 주소가 host 주소 `192.168.0.13`이고 port가 `3200`이다.
- [ ] `allow-kiali-egress-to-observability`가 `192.168.0.13/32`의 `443`, `3200`을 허용한다.
- [ ] Kiali 로그에 Grafana `401`이나 Prometheus 연결 오류가 없다.

- **Signals**: Kiali external service status, Kiali logs, `tempo-external` EndpointSlice, Kiali NetworkPolicy egress rules, Grafana API response code.

##### Unverified Conditions

- **Evidence to Capture**: Kiali log excerpts, route response codes, `/api/frontend/settings` HTTP result, applied PR link for GitOps corrections.

##### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Observability Platform Operations Policy](../02.policies/0005-observability-platform-operations-policy.md) | Kiali reports Prometheus, Grafana, or Tempo unreachable because the external route, name resolution or CA, Tempo endpoint, NetworkPolicy, URL, or Viewer-only API access may have drifted. | Platform operator captures Kiali logs, route, endpoint, and egress evidence; RUN-0001 and RUN-0002 own endpoint and CA repair, and the observability owner persists Grafana changes in its repository. |

#### Escalation

##### Next Owner

- Grafana auth changes belong to the external observability workspace; this repository only verifies their result.

##### Recovery or Forward Repair

- NetworkPolicy and Kiali configuration changes are reverted through GitOps if the new address or port mapping is wrong.

##### Recovery Procedures

- Tempo EndpointSlice recovery follows RUN-0001 External Endpoint Recovery; name resolution and CA recovery follow RUN-0002 Steps step 4.

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
