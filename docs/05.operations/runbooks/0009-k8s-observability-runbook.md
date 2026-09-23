---
title: "k8s Observability 복구 Runbook"
version: "2.1.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0009"
---

# k8s Observability 복구 Runbook

## Overview

이 런북은 cluster 안 Alloy(`monitoring/alloy-k8s-logs`)의 k8s 메트릭·로그 수집에
장애가 났을 때 진단하고 복구하는 절차를 제공한다. ArgoCD component별 확인은
[RUN-0008](./0008-argocd-metrics-prometheus-runbook.md)이 다룬다.

수집 경로([ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md),
[ADR-0046](../../02.architecture/decisions/0046-external-services-over-host-addresses.md)):

- **로그와 event**: Kubernetes API → Alloy → `loki-external`(host `192.168.0.13:3100`)
- **메트릭**: Alloy가 pod IP와 API server proxy로 scrape한 뒤 외부 Traefik의
  Prometheus API `https://prometheus.hy.home.arpa/api/v1/write`로 remote write한다.
  Basic Auth는 `monitoring/prometheus-api-auth`(OpenBao `platform/prometheus-api`),
  CA는 `monitoring/hy-home-root-ca`다. 모든 series에 `cluster="k3d-hyhome"`가 붙는다.

| job | 대상 |
| --- | --- |
| `kubernetes-pods` | `prometheus.io/scrape` annotation pod(istiod, Istio sidecar), ArgoCD component(`8082`, `8083`, `8084`, `8080`, `9001`), argo-rollouts `8090`, kube-state-metrics `8080` |
| `kubelet` | 각 node의 `/api/v1/nodes/<node>/proxy/metrics` |
| `cadvisor` | 각 node의 `/api/v1/nodes/<node>/proxy/metrics/cadvisor` |

저장, 조회, dashboard, alert rule은 외부 observability workspace가 소유한다. 외부
Prometheus의 NodePort static scrape는 폐지되었다.

주된 장애 원인:

1. **remote write 실패**: 자격 증명이 외부 Traefik의 Basic Auth(`INFRA-007`)와
   맞지 않거나(401), 이름 해석·CA가 어긋나거나(`no such host`, `x509`), remote
   write receiver가 꺼져 있다(404).
2. **alloy-k8s-logs CrashLoop**: `readOnlyRootFilesystem` + storage 경로
   미설정, 또는 미지원 속성 사용
3. **egress 차단**: `monitoring` NetworkPolicy가 `192.168.0.13`의 `3100`/`443`이나
   API server `6443`을 허용하지 않는다.
4. **target 누락**: component의 label, container port, annotation이 바뀌어
   relabel 규칙에서 빠진다.
5. **AppProject destinations 미포함**: `monitoring` 네임스페이스가 AppProject에 없어
   Application 배포 실패

### Purpose

in-cluster 메트릭·로그 수집과 remote write 장애를 진단하고, GitOps 상태와 외부
observability endpoint 연결을 복구한다.

## Runbook Type

`bootstrap`

## When to Use

- 외부 Prometheus에서 `up{cluster="k3d-hyhome"}` 결과가 비었거나 job이 빠졌을 때
- `argocd_app_info`, `kube_pod_*`, `istio_requests_total`이 조회되지 않을 때
- Loki에서 `{cluster="k3d-hyhome"}` 쿼리 결과가 비어 있을 때
- `alloy-k8s-logs` 파드가 `CrashLoopBackOff` 상태일 때
- Alloy 로그에 remote write 오류가 반복될 때

---

## Procedure or Checklist

아래 절차는 전체 상태 진단, platform-monitoring App 복구, Alloy CrashLoop 복구,
remote write 복구, target 누락 복구 순서로 수행한다.

### 정상 상태 기준값

| 항목 | 기준값 |
| --- | --- |
| alloy-k8s-logs 파드 | `1/1 Running` |
| 외부 Prometheus job | `kubernetes-pods`, `kubelet`, `cadvisor`가 `cluster="k3d-hyhome"`로 존재 |
| ArgoCD 메트릭 | `argocd_app_info{cluster="k3d-hyhome"}` 결과 수 ≥ `gitops/apps/root` Application 수 |
| node 메트릭 | `kube_node_info{cluster="k3d-hyhome"}` 결과 4건 |
| Loki k8s 로그 스트림 | `{cluster="k3d-hyhome"}` → 스트림 수 > 0 |
| AppProject destinations | `monitoring` 포함 |

---

### Procedure 1: 전체 상태 진단

### 조회 helper

host에서 외부 Prometheus를 조회할 때 쓴다. 비밀번호는 외부 workspace의 secret
파일에서 읽어 curl의 stdin 설정(`-K -`)으로 넘긴다. 명령 인자나 shell history에
남지 않는다.

```bash
prom() {
  printf 'user = "k8s-prometheus:%s"\n' \
    "$(cat ~/data/hy-home.docker/secrets/observability/prometheus_api_password.txt)" |
    curl -s -K - --cacert secrets/certs/rootCA.pem \
      https://prometheus.hy.home.arpa/api/v1/query --data-urlencode "query=$1"
}
```

```bash
LOKI=http://192.168.0.13:3100

echo "=== alloy-k8s-logs 파드 ==="
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs

echo "=== remote write 오류 ==="
kubectl logs -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --since=10m \
  | rg -i 'remote_write|prometheus.remote_write|level=error' | tail -5

echo "=== job별 target ==="
prom 'count by (job) (up{cluster="k3d-hyhome"})'

echo "=== ArgoCD 메트릭 ==="
prom 'count(argocd_app_info{cluster="k3d-hyhome"})'

echo "=== Loki k8s 로그 ==="
curl -s -G "$LOKI/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('  스트림 수:', len(d['data']['result']))"
```

`prom`이 401, `x509` 오류를 내거나 응답하지 않으면 Procedure 4로 이동한다.

---

### Procedure 2: platform-monitoring ArgoCD App 배포 복구

> **Agent execution boundary**: AppProject 직접 적용은 human-approved bootstrap 또는 break-glass 전용이다. Agent는 기본적으로 Git 파일 수정, 리뷰, ArgoCD reconciliation 계획, 증적 정리까지만 수행한다.

```bash
# AppProject에 monitoring namespace 포함 확인
kubectl get appproject platform -n argocd \
  -o jsonpath='{.spec.destinations[*].namespace}' | tr ' ' '\n' | grep monitoring

# 없으면 human-approved bootstrap/break-glass로 직접 적용
kubectl apply -f gitops/clusters/local/appproject-platform.yaml

# namespace 먼저 배포 (operator-triggered reconciliation only)
argocd app sync platform-namespaces

# monitoring 리소스 배포 (operator-triggered reconciliation only)
argocd app sync platform-monitoring

# 배포 확인
kubectl get deploy,svc -n monitoring
```

---

### Procedure 3: alloy-k8s-logs CrashLoop 복구

### 3-1. 원인 파악

```bash
kubectl logs -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --tail=30
kubectl describe pod -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs
```

### 3-2. 오류 시그니처별 조치

| 오류 시그니처 | 원인 | 조치 |
| --- | --- | --- |
| `mkdir data-alloy: read-only file system` | `--storage.path` 미설정 | args에 `--storage.path=/var/lib/alloy` 추가 |
| `unrecognized attribute name 'extra_labels'` | 당시 Alloy v1.13.1 미지원 속성 | `loki.process` + `stage.static_labels`로 대체 |
| `failed to list pods: Forbidden` | ClusterRole 권한 미할당 | ClusterRoleBinding 재적용 |
| `nodes/proxy` `Forbidden` | kubelet/cAdvisor proxy 권한 누락 | ClusterRole의 `nodes/proxy` get 확인 |
| `connection refused` to `loki-external` | host `3100` 미공개 또는 egress 차단 | Procedure 4 |

### 3-3. 수정 후 재배포

`gitops/platform/monitoring/alloy-k8s-logs.yaml`을 고치고 커밋한 뒤 동기화한다.

```bash
# 기본 경로: ArgoCD sync (operator-triggered reconciliation only)
argocd app sync platform-monitoring
# human-approved break-glass only
kubectl apply -f gitops/platform/monitoring/alloy-k8s-logs.yaml
```

---

### Procedure 4: remote write와 로그 전송 경로 복구

```bash
# 1. 외부 route: 인증 없이 401이면 route가 살아 있다 (Linux server host에서)
curl -s -o /dev/null -w '%{http_code}\n' --cacert secrets/certs/rootCA.pem \
  https://prometheus.hy.home.arpa/api/v1/status/buildinfo
docker ps --format '{{.Names}}\t{{.Ports}}' | rg 'infra-loki'

# 2. cluster 쪽 이름 해석, CA, 자격 증명
kubectl -n kube-system get configmap coredns-custom -o yaml | rg prometheus
kubectl -n monitoring get configmap hy-home-root-ca
kubectl -n monitoring get externalsecret prometheus-api-auth

# 3. Loki EndpointSlice와 monitoring egress(443, 3100)
kubectl -n platform get endpointslice loki-external-1
kubectl -n monitoring get networkpolicy allow-egress-monitoring -o yaml | rg -A8 ipBlock
```

판정 기준:

- route가 응답하지 않으면 외부 workspace의 Traefik `prometheus-api` router 문제다.
  이 저장소에서 고칠 수 없다.
- Alloy 로그의 remote write가 `401`이면 OpenBao `platform/prometheus-api`와 외부
  workspace의 Basic Auth(`INFRA-007`)가 어긋난 것이다. 외부 workspace가 값을 맞춘다.
- `404`면 `--web.enable-remote-write-receiver`가 꺼져 있다. 외부 workspace가 소유한다.
- `no such host`, `x509`면 `coredns-custom`이나 `hy-home-root-ca`를 bootstrap 파일로
  다시 적용한다(human-approved break-glass).
- Loki EndpointSlice나 NetworkPolicy가 `192.168.0.13`이 아니면 Git의
  `gitops/platform/`을 고치고 reconciliation으로 반영한다.

---

### Procedure 5: target 누락 복구

`kubernetes-pods` job에서 특정 component가 빠지면 label과 port를 relabel 규칙과
비교한다.

```bash
kubectl get pods -n argocd -L app.kubernetes.io/name
kubectl get pods -n argo-rollouts -L app.kubernetes.io/name
kubectl get pods -n istio-system -l app=istiod \
  -o jsonpath='{.items[*].metadata.annotations.prometheus\.io/scrape}'
```

- ArgoCD, argo-rollouts, kube-state-metrics는 `discovery.relabel "platform_pods"`의
  `namespace;app.kubernetes.io/name;container port` 규칙에 맞아야 한다. chart
  업그레이드로 이름이나 port가 바뀌면 그 규칙을 고친다.
- istiod와 Istio sidecar는 `prometheus.io/scrape` annotation으로 잡힌다.
- 외부 Prometheus 쪽에서 job 이름은 `kubernetes-pods`이고 component는 `app`
  label로 구분한다.

---

## Verification Steps

```bash
# prom helper: 위 "조회 helper"
echo "[1] alloy-k8s-logs"
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --no-headers \
  | awk '{print "  "$1": "$3}'

echo "[2] jobs"
prom 'count by (job) (up{cluster="k3d-hyhome"})'
# → kubernetes-pods, kubelet, cadvisor

echo "[3] components"
prom 'count by (app) (up{cluster="k3d-hyhome",job="kubernetes-pods"})'

echo "[4] ArgoCD and node metrics"
prom 'count(argocd_app_info{cluster="k3d-hyhome"})'
prom 'count(kube_node_info{cluster="k3d-hyhome"})'

echo "[5] Loki k8s log streams"
curl -s -G "http://192.168.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('  스트림:', len(d['data']['result']))"
```

## Observability and Evidence Sources

- **Signals**: Alloy pod readiness, Alloy remote write errors, `up{cluster="k3d-hyhome"}` by job and app, Loki stream count.
- **Evidence to Capture**: verification command output, ArgoCD Application status, Alloy logs, host port table.

## Safe Rollback or Recovery Procedure

- Monitoring manifest changes should be reverted through GitOps if relabel, remote write, or egress changes regress collection.
- External Prometheus, Loki, dashboard, and alert rule changes are reverted in the owning external workspace.
- AppProject destination changes require reviewed GitOps updates; direct cluster edits remain bootstrap/break-glass only.

### Troubleshooting

| 증상 | 원인 | 조치 |
| --- | --- | --- |
| platform-monitoring InvalidSpecError | AppProject에 monitoring namespace 미포함 | Git 파일 확인 후 human-approved bootstrap/break-glass로 AppProject 반영 |
| Alloy 로그에 remote write `401` | Basic Auth 자격 증명 불일치 | OpenBao `platform/prometheus-api`와 외부 `INFRA-007` 대조 (Procedure 4) |
| `no such host` / `x509` | CoreDNS custom zone 또는 CA ConfigMap 누락 | Procedure 4 |
| remote write `404` | remote write receiver 꺼짐 | 외부 workspace가 flag 복구 |
| `kubelet`/`cadvisor` job 없음 | `nodes/proxy` 권한 또는 API egress 누락 | Procedure 3-2, egress `6443` 확인 |
| ArgoCD component만 빠짐 | chart 변경으로 label/port 불일치 | Procedure 5 |
| Loki에 k8s 로그 없음 | alloy 미실행 또는 loki-external 연결 실패 | Procedure 3, 4 |

---

## Traceability

- [Observability Platform Policy](../policies/0005-observability-platform-operations-policy.md)
- [Kiali Connectivity Runbook](./0007-kiali-observability-connectivity-runbook.md)
- [ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md)
- [ADR-0046](../../02.architecture/decisions/0046-external-services-over-host-addresses.md)
- [`../../../gitops/platform/monitoring`](../../../gitops/platform/monitoring)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Observability Platform Operations Policy](../policies/0005-observability-platform-operations-policy.md) | In-cluster metric collection, remote write, ArgoCD metrics, Alloy log/event collection, or monitoring AppProject admission is degraded. | Platform operator captures pod, remote write, job, Loki, and ArgoCD evidence; GitOps owner restores cluster resources and the observability owner restores external Prometheus/Loki publication and settings. |
