---
title: "Kiali Observability 연결 복구 Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0007"
---

# Kiali Observability 연결 복구 Runbook

## Overview

이 런북은 Kiali에서 Grafana, Prometheus, Tempo 등 외부 관측성 서비스가 Unreachable로 표시되는 장애를 진단하고 복구하는 절차를 제공한다.

주된 원인은 세 가지다:

1. **외부 경로 drift**: Kiali는 Prometheus API(`https://prometheus.hy.home.arpa`, Basic Auth)와 Grafana(`https://grafana.hy.home.arpa`)를 외부 Traefik으로, Tempo는 host port `192.168.0.13:3200`으로 호출한다(ADR-0046). 이름 해석(CoreDNS custom zone), gateway CA(`istio-system/kiali-cabundle`), Basic Auth Secret(`istio-system/kiali-prometheus-auth`) 중 하나가 어긋나거나 외부 workspace가 route나 port를 바꾸면 연결이 끊긴다.
2. **ArgoCD EndpointSlice 제외**: ArgoCD는 `discovery.k8s.io/EndpointSlice` 리소스를 기본 resource.exclusions에 포함하여 직접 관리하지 않을 수 있다. 따라서 YAML을 수정하고 커밋해도 EndpointSlice가 자동으로 클러스터에 동기화되지 않을 수 있다. 직접 `kubectl apply`/`kubectl patch`는 운영자가 승인한 break-glass 복구에서만 사용한다.
3. **Grafana 인증 실패**: 외부 Grafana는 익명 API 접근을 허용하지 않는다. Kiali는 Grafana Viewer service account token(`istio-system/kiali-grafana-auth`, OpenBao `platform/grafana-api`)을 bearer로 보낸다. token이 없거나 만료·폐기되면 `/api/frontend/settings`가 401을 반환하고 Kiali는 Grafana를 Unreachable로 표시한다.

### Purpose

Kiali에서 외부 observability service가 unreachable로 표시될 때 EndpointSlice, NetworkPolicy, Kiali configuration, Grafana auth 상태를 순서대로 진단하고 복구한다.

## Runbook Type

`troubleshooting`

## When to Use

- Kiali에서 Grafana/Prometheus/Tempo가 unreachable로 표시될 때
- 외부 workspace가 관측 서비스의 host port 공개나 bind 주소를 바꾼 뒤
- `kubectl get endpointslice -n platform`에서 alloy, loki, grafana의 주소가 비어있거나 없을 때

---

## Procedure or Checklist

아래 절차는 host port 공개 확인, Kiali 파드 연결 테스트, EndpointSlice/NetworkPolicy 점검, Grafana auth 확인 순서로 수행한다.

### host 공개 port 계약표 (ADR-0046)

| 대상 | 경로 | 인증 |
| --- | --- | --- |
| Prometheus API | `https://prometheus.hy.home.arpa/api/v1/` (외부 Traefik `192.168.0.13:443`) | Basic Auth |
| Grafana | `https://grafana.hy.home.arpa` (외부 Traefik `192.168.0.13:443`) | Viewer service account token (bearer) |
| Tempo | `tempo-external` → host `192.168.0.13:3200` | 없음 |
| Loki | `loki-external` → host `192.168.0.13:3100` | 없음 |
| Alloy OTLP | `alloy-external` → host `192.168.0.13:4317/4318` | 없음 |

> 닫혀 있거나 route가 응답하지 않으면 이 저장소가 아니라 외부 workspace의 route와 port 공개를 먼저 확인한다.

---

### Procedure 1: 연결 상태 진단

### 1-1. 현재 EndpointSlice IP 확인

```bash
kubectl get endpointslice -n platform
```

출력 예시에서 `ENDPOINTS` 컬럼이 비어있거나 `192.168.0.13`이 아니면 문제 있음.

### 1-2. 외부 route와 host port 확인 (Linux server host에서)

```bash
# 인증 없이 401이면 Prometheus API route가 살아 있다
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://prometheus.hy.home.arpa/api/v1/status/buildinfo
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://grafana.hy.home.arpa/api/health
docker ps --format '{{.Names}}\t{{.Ports}}' | rg 'infra-(tempo|loki|alloy)'
```

### 1-3. Kiali 파드에서 직접 연결 테스트

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

### 1-4. ArgoCD resource.exclusions 확인

```bash
kubectl get configmap argocd-cm -n argocd \
  -o jsonpath='{.data.resource\.exclusions}'
```

출력에 `EndpointSlice`가 포함되어 있으면 ArgoCD가 해당 리소스를 동기화하지 않음을 확인한다.

---

### Procedure 2: EndpointSlice 주소 복구

> **Agent execution boundary**: 아래 `kubectl patch`/`kubectl apply` 절차는 human-approved break-glass 전용이다. Agent는 기본적으로 Git 파일 수정, 리뷰, ArgoCD reconciliation 계획, 증적 정리까지만 수행한다.

### 2-1. 기존 EndpointSlice 패치 (human-approved break-glass)

```bash
# Alloy (EndpointSlice가 없으면 2-2 참고)
# human-approved break-glass only
kubectl patch endpointslice alloy-external-1 -n platform --type=json \
  -p='[{"op":"replace","path":"/endpoints/0/addresses/0","value":"192.168.0.13"}]'

# Loki (EndpointSlice가 없으면 2-2 참고)
# human-approved break-glass only
kubectl patch endpointslice loki-external-1 -n platform --type=json \
  -p='[{"op":"replace","path":"/endpoints/0/addresses/0","value":"192.168.0.13"}]'
```

### 2-2. 누락된 EndpointSlice 생성 (human-approved break-glass)

ArgoCD가 동기화하지 않는 경우에도 직접 apply는 운영자가 승인한 break-glass 상황에서만 수행한다.

```bash
kubectl apply -f gitops/platform/external-services/alloy-external.yaml
kubectl apply -f gitops/platform/external-services/loki-external.yaml
```

### 2-3. git 파일도 같은 주소로 수정 후 커밋

```bash
# gitops/platform/external-services/ 아래 EndpointSlice 주소 수정 후
git add gitops/platform/external-services/
git commit -m "fix(platform): restore external service endpoints to the host address"
```

> **주의**: git 커밋만으로는 EndpointSlice가 클러스터에 반영되지 않을 수 있다. 직접 `kubectl apply` 또는 `kubectl patch`는 human-approved break-glass 절차로만 실행하고, 실행 전후 증적을 남긴다.

### 2-4. 적용 결과 확인

```bash
kubectl get endpointslice -n platform
kubectl describe endpointslice loki-external-1 -n platform
```

---

### Procedure 3: NetworkPolicy egress 규칙 점검

NetworkPolicy의 egress `ipBlock` 규칙은 **post-DNAT 기준 IP**로 작성해야 한다. 외부 서비스는 host 주소 `192.168.0.13/32`와 공개 port로 허용한다(ADR-0046).

### 3-1. 현재 egress ipBlock 확인

```bash
kubectl get networkpolicy -n istio-system -o yaml | grep -A5 ipBlock
```

### 3-2. ArgoCD egress NetworkPolicy 확인

```bash
kubectl get networkpolicy -n argocd argocd-egress-to-external-valkey -o yaml
```

### 3-3. 수정이 필요한 경우

`gitops/platform/network-policies/` 하위 NetworkPolicy YAML의 `ipBlock.cidr`를 실제 IP로 수정하고 git 커밋한다. NetworkPolicy는 ArgoCD가 정상 동기화하므로 커밋 후 ArgoCD Sync로 적용 가능하다.

```bash
# ArgoCD Sync 강제 실행
# operator-triggered reconciliation only
argocd app sync platform-network-policies --force
```

---

### Procedure 4: Kiali Grafana URL 설정 확인

Kiali의 Grafana 연동 URL은 ArgoCD App의 Helm values 또는 ConfigMap에서 관리된다.

### 4-1. 현재 설정된 URL 확인

```bash
# platform-kiali Application의 Grafana URL 확인
kubectl get app platform-kiali -n argocd -o jsonpath='{.spec.source.helm.values}'
```

또는 직접 파일에서 확인:

```bash
grep -i grafana gitops/apps/root/platform-kiali-app.yaml
```

### 4-2. URL이 계약과 다른 경우

`gitops/apps/root/platform-kiali-app.yaml`의 브라우저용 Grafana 링크(`url`)는 외부 Traefik의
`https://grafana.hy.home.arpa`다. Kiali의 cluster 내부 연결은 service DNS(`in_cluster_url`)를
사용하므로 주소 변경은 `platform` 네임스페이스의 external service endpoint가 소유한다.

```yaml
# 예시: 현재 GitOps 계약 (cr.spec.external_services)
grafana:
  in_cluster_url: "https://grafana.hy.home.arpa"
  url: "https://grafana.hy.home.arpa"
```

수정 후 커밋하고 ArgoCD Sync를 실행한다:

```bash
git add gitops/apps/root/platform-kiali-app.yaml
git commit -m "fix(platform): restore the Kiali Grafana link"
# operator-triggered reconciliation only
argocd app sync platform-kiali
```

### 4-3. Kiali ConfigMap 직접 확인 (선택)

```bash
kubectl get configmap kiali -n istio-system -o yaml | grep -A3 grafana
```

---

### Troubleshooting

### `nc` 명령이 Kiali 파드 내에서 항상 OK를 반환한다

Kiali 기본 이미지의 `nc`(BusyBox)는 특정 옵션에서 오동작할 수 있다. 반드시 아래 방식을 사용한다:

```bash
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/<IP>/<PORT>" && echo OK || echo FAIL'
```

### EndpointSlice patch 후에도 연결이 안 된다

1. NetworkPolicy가 해당 IP를 차단하고 있는지 확인한다 (Procedure 3 참고).
2. 클러스터 DNS가 Service를 제대로 해석하는지 확인한다.

```bash
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup grafana.hy.home.arpa
```

1. Kiali 파드를 재시작하여 캐시를 초기화한다.

```bash
kubectl rollout restart deployment/kiali -n istio-system
```

### Kiali 로그에 `grafana version check failed: code=[401]`가 반복된다

**원인**: Kiali가 보내는 Grafana service account token이 없거나 만료·폐기되었다. 외부 Grafana는 익명 API 접근을 허용하지 않는다.

Kiali는 내부 URL로 `/api/frontend/settings`를 호출해 Grafana 버전을 확인한다. 이 엔드포인트가 401을 반환하면 Kiali는 Grafana를 Unreachable로 표시한다.

**확인:**

```bash
kubectl -n istio-system logs deploy/kiali --since=5m | grep -i "grafana\|401"
# 예: grafana version check failed: url=[.../api/frontend/settings], code=[401]
```

**해결**: token은 외부 observability workspace가 Grafana Viewer service account로
발급하고 OpenBao `platform/grafana-api.token`에 둔다. 이 저장소는 ESO로 받아 쓰기만 한다.

1. `kubectl -n istio-system get externalsecret kiali-grafana-auth`가 Ready인지 확인한다.
2. Ready가 아니면 외부 workspace에 KV 값이나 policy 경로를 확인하도록 요청한다.
3. 401이 계속되면 token이 폐기되었거나 role이 Viewer 미만이다. 외부 workspace가
   token을 재발급하고 KV를 갱신한다. ESO가 1시간 안에 따라간다.

**검증:**

```bash
# 익명 호출은 401이 정상이다 (Grafana가 익명 접근을 허용하지 않는다)
curl -s -o /dev/null -w "%{http_code}" --cacert secrets/certs/rootCA.pem \
  https://grafana.hy.home.arpa/api/frontend/settings
kubectl -n istio-system get externalsecret kiali-grafana-auth

# Kiali 로그에서 Grafana 버전 확인 성공 여부
kubectl -n istio-system logs deploy/kiali --since=5m | rg -i 'grafana'

# Kiali 로그에서 401 오류 사라짐 확인
kubectl -n istio-system logs deploy/kiali --since=2m | grep -i "grafana\|401"
# → 출력 없음
```

### ArgoCD App이 OutOfSync로 표시된다

break-glass로 EndpointSlice를 직접 생성·수정하면 ArgoCD가 live 상태와 Git
desired state의 차이를 OutOfSync로 표시할 수 있다. ArgoCD Application에
live `ignoreDifferences`를 추가하지 말고, Procedure 2-3처럼 Git의
`gitops/platform/external-services/`를 같은 값으로 고친 뒤 리뷰와
reconciliation으로 차이를 없앤다.

---

## Verification Steps

- [ ] Kiali pod에서 Prometheus, Grafana, Tempo endpoint TCP 연결이 성공한다.
- [ ] EndpointSlice 주소가 host 주소 `192.168.0.13`이고 해당 port가 host에 공개되어 있다.
- [ ] NetworkPolicy egress ipBlock이 `192.168.0.13/32`와 필요한 port를 허용한다.
- [ ] Grafana `/api/frontend/settings`가 Kiali에서 200 응답을 반환한다.

## Observability and Evidence Sources

- **Signals**: Kiali external service status, Kiali logs, EndpointSlice endpoints, NetworkPolicy egress rules, Grafana API response code.
- **Evidence to Capture**: Kiali log excerpts, host port table, `/api/frontend/settings` HTTP result, applied PR link for GitOps corrections.

## Safe Rollback or Recovery Procedure

- EndpointSlice or NetworkPolicy changes should be reverted through GitOps if the new address or port mapping is wrong.
- Grafana auth changes belong to the external observability workspace; this repository only verifies their result.
- Direct EndpointSlice apply/patch remains human-approved break-glass only and must be reconciled back into Git.

## Traceability

- **Operations Policy**: [`../policies/0005-observability-platform-operations-policy.md`](../policies/0005-observability-platform-operations-policy.md)
- **k8s Observability Runbook**: [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)
- **External Services**: [`../../../gitops/platform/external-services`](../../../gitops/platform/external-services)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Observability Platform Operations Policy](../policies/0005-observability-platform-operations-policy.md) | Kiali reports Prometheus, Grafana, or Tempo unreachable because endpoint, NetworkPolicy, URL, or Viewer-only API access may have drifted. | Platform operator captures Kiali logs, endpoint/IP and egress evidence; approved break-glass operator owns live EndpointSlice repair, and the observability owner persists Grafana changes in its repository. |
