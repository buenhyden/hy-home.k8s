---
title: "Kiali Observability 연결 복구 Runbook"
version: "2.0.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "operations"
artifact_id: "RUN-0007"
---

# Kiali Observability 연결 복구 Runbook

## Overview

이 런북은 Kiali에서 Grafana, Prometheus, Tempo 등 외부 관측성 서비스가 Unreachable로 표시되는 장애를 진단하고 복구하는 절차를 제공한다.

주된 원인은 세 가지다:

1. **외부 경로 drift**: Kiali는 Prometheus API(`https://prometheus.hy.home.arpa`, Basic Auth)와 Grafana(`https://grafana.hy.home.arpa`)를 외부 Traefik으로 호출한다(ADR-0046). 이름 해석(CoreDNS custom zone), gateway CA(`istio-system/kiali-cabundle`), Basic Auth Secret(`istio-system/kiali-prometheus-auth`) 중 하나가 어긋나거나 외부 workspace가 route를 바꾸면 연결이 끊긴다.
2. **Tempo endpoint drift**: Tempo는 `tempo-external` Service와 EndpointSlice를 거쳐 host port `192.168.0.13:3200`으로 닿는다. EndpointSlice는 ArgoCD Application `platform-external-services`가 Git에서 관리한다.
3. **Grafana 인증 실패**: 외부 Grafana는 익명 API 접근을 허용하지 않는다. Kiali는 Grafana Viewer service account token(`istio-system/kiali-grafana-auth`, OpenBao `platform/grafana-api`)을 bearer로 보낸다. token이 없거나 만료·폐기되면 `/api/frontend/settings`가 401을 반환하고 Kiali는 Grafana를 Unreachable로 표시한다.

### Purpose

Kiali에서 외부 observability service가 unreachable로 표시될 때 외부 route, 이름 해석과 CA, Tempo endpoint, NetworkPolicy, Kiali configuration, Grafana auth 상태를 순서대로 진단하고 복구 owner로 보낸다.

## Runbook Type

`troubleshooting`

## When to Use

- Kiali에서 Grafana/Prometheus/Tempo가 unreachable로 표시될 때
- 외부 workspace가 관측 서비스의 route, host port 공개나 bind 주소를 바꾼 뒤
- `kubectl get endpointslice -n platform`에서 `tempo-external-1`의 주소가 비어있거나 없을 때

---

## Procedure or Checklist

아래 절차는 외부 route와 host port 확인, Kiali 파드 연결 테스트, NetworkPolicy 점검, Kiali 설정 확인, Grafana auth 확인 순서로 수행한다.

### Kiali 외부 의존 계약표 (ADR-0046)

| 대상 | 경로 | 인증 |
| --- | --- | --- |
| Prometheus API | `https://prometheus.hy.home.arpa/api/v1/` (외부 Traefik `192.168.0.13:443`) | Basic Auth |
| Grafana | `https://grafana.hy.home.arpa` (외부 Traefik `192.168.0.13:443`) | Viewer service account token (bearer) |
| Tempo | `tempo-external` → host `192.168.0.13:3200` | 없음 |

> 닫혀 있거나 route가 응답하지 않으면 이 저장소가 아니라 외부 workspace의 route와 port 공개를 먼저 확인한다.

---

### Procedure 1: 연결 상태 진단

### 1-1. 외부 route와 host port 확인 (Linux server host에서)

```bash
# 인증 없이 401이면 Prometheus API route가 살아 있다
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://grafana.hy.home.arpa/api/health
docker ps --format '{{.Names}}\t{{.Ports}}' | rg 'infra-tempo'
```

### 1-2. Kiali 파드에서 직접 연결 테스트

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
Procedure 4단계로 재적용한다.

### 1-3. Tempo EndpointSlice 확인

```bash
kubectl -n platform get endpointslice tempo-external-1
```

주소가 `192.168.0.13`이 아니거나 port가 `3200`이 아니면
[RUN-0001](./0001-argocd-platform-bootstrap-runbook.md)의 External Endpoint
Recovery 절차로 복구한다.

---

### Procedure 2: NetworkPolicy egress 규칙 점검

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

---

### Procedure 3: Kiali 외부 서비스 설정 확인

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

---

### Troubleshooting

### `nc` 명령이 Kiali 파드 내에서 항상 OK를 반환한다

Kiali 기본 이미지의 `nc`(BusyBox)는 특정 옵션에서 오동작할 수 있다. Procedure 1-2의 `bash /dev/tcp` 방식을 사용한다.

### 경로·endpoint·egress가 맞는데도 연결이 안 된다

1. cluster DNS가 외부 이름을 host 주소로 해석하는지 확인한다.

   ```bash
   kubectl run -it --rm debug --image=busybox:1.36 --restart=Never -- \
     nslookup grafana.hy.home.arpa
   ```

2. Kiali 파드를 재시작하여 캐시를 초기화한다.

   ```bash
   # operator-approved restart only
   kubectl rollout restart deployment/kiali -n istio-system
   ```

### Kiali 로그에 `grafana version check failed: code=[401]`가 반복된다

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

---

## Verification Steps

- [ ] Kiali pod에서 `192.168.0.13:443`과 `192.168.0.13:3200` TCP 연결이 성공한다.
- [ ] `tempo-external-1` 주소가 host 주소 `192.168.0.13`이고 port가 `3200`이다.
- [ ] `allow-kiali-egress-to-observability`가 `192.168.0.13/32`의 `443`, `3200`을 허용한다.
- [ ] Kiali 로그에 Grafana `401`이나 Prometheus 연결 오류가 없다.

## Observability and Evidence Sources

- **Signals**: Kiali external service status, Kiali logs, `tempo-external` EndpointSlice, Kiali NetworkPolicy egress rules, Grafana API response code.
- **Evidence to Capture**: Kiali log excerpts, route response codes, `/api/frontend/settings` HTTP result, applied PR link for GitOps corrections.

## Safe Rollback or Recovery Procedure

- NetworkPolicy and Kiali configuration changes are reverted through GitOps if the new address or port mapping is wrong.
- Tempo EndpointSlice recovery follows RUN-0001 External Endpoint Recovery; name resolution and CA recovery follow RUN-0002 Procedure step 4.
- Grafana auth changes belong to the external observability workspace; this repository only verifies their result.

## Traceability

- **Operations Policy**: [`../policies/0005-observability-platform-operations-policy.md`](../policies/0005-observability-platform-operations-policy.md)
- **k8s Observability Runbook**: [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)
- **Endpoint Recovery**: [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)
- **Name Resolution and CA Recovery**: [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)
- **External Services**: [`../../../gitops/platform/external-services`](../../../gitops/platform/external-services)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Observability Platform Operations Policy](../policies/0005-observability-platform-operations-policy.md) | Kiali reports Prometheus, Grafana, or Tempo unreachable because the external route, name resolution or CA, Tempo endpoint, NetworkPolicy, URL, or Viewer-only API access may have drifted. | Platform operator captures Kiali logs, route, endpoint, and egress evidence; RUN-0001 and RUN-0002 own endpoint and CA repair, and the observability owner persists Grafana changes in its repository. |
