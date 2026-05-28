---
title: 'k3d/k3s 클러스터 관측성 부트스트랩 가이드'
type: guide
status: active
owner: platform
updated: 2026-05-09
---

# k3d/k3s 클러스터 관측성 부트스트랩 가이드

## Overview (KR)

이 문서는 k3d 클러스터(k3d-hyhome)의 메트릭과 로그를 외부 관측성 스택(Prometheus/Loki/Grafana)에서 수집하도록 설정하는 방법을 설명한다.

k3d는 containerd 기반으로 파드를 실행하므로, 외부 Docker 소켓 기반 Alloy로는 파드 로그를 수집할 수 없다. 이를 해결하기 위해 클러스터 내부에 인프라 컴포넌트를 배포한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer

## Purpose

k3d 클러스터의 Kubernetes 오브젝트 상태 메트릭, 파드 로그, 이벤트, Istio 제어 평면 메트릭, Argo Rollouts 메트릭을 외부 관측성 스택과 연결한다.

## Prerequisites

### 아키텍처 개요

```text
k3d-hyhome (Docker network: 172.18.0.0/16)
├── server-0 (172.18.0.2)         ← NodePort gateway
│   ├── monitoring/kube-state-metrics (NodePort 30091)
│   ├── monitoring/alloy-k8s-logs    → Loki (172.18.0.13:3100)
│   ├── istio-system/istiod-metrics-np (NodePort 30090)
│   └── argo-rollouts/argo-rollouts-metrics-np (NodePort 30092)
├── agent-0 (172.18.0.3)
├── agent-1 (172.18.0.4)
└── agent-2 (172.18.0.5)

Docker (k3d-hyhome network)
├── Prometheus (172.18.0.10:9090) ← scrapes NodePorts
├── Loki       (172.18.0.13:3100) ← receives k8s pod logs from in-cluster Alloy
└── Grafana    (172.18.0.14:3000)
```

```bash
# k3d 클러스터 정상 동작 확인
kubectl get nodes

# 관측성 스택 정상 동작 확인
curl -s http://172.18.0.10:9090/-/healthy  # → Prometheus Server is Healthy.
curl -s http://172.18.0.13:3100/ready      # → ready
```

---

## Step-by-step Instructions

아래 절차는 monitoring 리소스 배포, NodePort 접근 확인, Prometheus 수집 확인, Loki 로그 확인, Grafana 대시보드 임포트 순서로 진행한다.

### Procedure 1: monitoring namespace + 리소스 배포

ArgoCD가 자동으로 배포하지만, 최초 부트스트랩 시 순서가 필요하다.

> **Agent execution boundary**: AppProject 직접 적용은 최초 bootstrap 또는 human-approved break-glass 전용이다. Agent는 기본적으로 Git 파일 수정, 리뷰, ArgoCD reconciliation 계획, 증적 정리까지만 수행한다.

```bash
# 1. AppProject에 monitoring namespace destination 추가 (operator-approved bootstrap only)
kubectl apply -f gitops/clusters/local/appproject-platform.yaml

# 2. namespace 배포 (operator-triggered reconciliation only)
argocd app sync platform-namespaces

# 3. monitoring 리소스 배포 (operator-triggered reconciliation only)
argocd app sync platform-monitoring

# 4. 배포 확인
kubectl get all -n monitoring
```

예상 출력:

```text
NAME                                       READY   STATUS    RESTARTS
pod/alloy-k8s-logs-xxxx-xxxx              1/1     Running   0
pod/kube-state-metrics-xxxx-xxxx          1/1     Running   0

NAME                            TYPE        CLUSTER-IP    PORT(S)
service/kube-state-metrics      ClusterIP   10.x.x.x      8080/TCP
service/kube-state-metrics-np   NodePort    10.x.x.x      8080:30091/TCP
```

---

### Procedure 2: NodePort 접근 확인

```bash
for port in 30090 30091 30092; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  case $port in
    30090) label="istiod" ;;
    30091) label="kube-state-metrics" ;;
    30092) label="argo-rollouts" ;;
  esac
  echo "NodePort $port ($label): HTTP $code"
done
# → 모두 200
```

---

### Procedure 3: Prometheus 수집 확인

```bash
# Prometheus reload (설정 변경 시)
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"

# target 상태 확인
curl -s "http://172.18.0.10:9090/api/v1/targets" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if t['labels'].get('domain') in ('kubernetes', 'mesh') or t['labels'].get('job') in ('argo-rollouts',):
        print(t['labels']['job'], '->', t['health'])
"
# → kube-state-metrics -> up
# → istiod -> up
# → argo-rollouts -> up

# kube-state-metrics 메트릭 확인 (4개 노드)
curl -s "http://172.18.0.10:9090/api/v1/query?query=kube_node_info" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('nodes:', len(d['data']['result']))"

# alert rules 로드 확인
curl -s "http://172.18.0.10:9090/api/v1/rules" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for g in d['data']['groups']:
    if g['name'] in ('kubernetes_alerts', 'etcd_alerts', 'istio_alerts', 'argocd_alerts'):
        print(f\"{g['name']}: {len(g['rules'])} rules\")
"
```

---

### Procedure 4: Loki k8s 로그 수집 확인

alloy-k8s-logs가 k3d 파드 로그를 Loki로 전송하는지 확인한다.

```bash
# alloy-k8s-logs 상태 확인
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs

# alloy 로그에서 파드 수집 확인
kubectl logs -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --tail=20 \
  | grep -E "tailer|loki.source.kubernetes"

# Loki에서 k8s 로그 쿼리 확인
curl -s -G "http://172.18.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=5" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
streams = d.get('data', {}).get('result', [])
print(f'k8s 로그 스트림 수: {len(streams)}')
for s in streams[:3]:
    print(' -', s['stream'].get('namespace', '?'), '/', s['stream'].get('pod', '?'))
"

# k8s 이벤트 로그 확인
curl -s -G "http://172.18.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={job="kubernetes-events"}' \
  --data-urlencode "limit=3" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
streams = d.get('data', {}).get('result', [])
print(f'k8s 이벤트 스트림 수: {len(streams)}')
"
```

---

### Procedure 5: Grafana 대시보드 임포트

Grafana UI에서 아래 커뮤니티 대시보드를 임포트한다:

| 대시보드                       | Grafana ID | 필요 데이터소스 |
| ------------------------------ | ---------- | --------------- |
| Kubernetes / Compute Resources | 17375      | Prometheus      |
| Kube State Metrics v2          | 13332      | Prometheus      |
| Istio Control Plane Dashboard  | 7645       | Prometheus      |
| Argo Rollouts Dashboard        | 21177      | Prometheus      |

```text
Grafana UI → Dashboards → Import → ID 입력 → Prometheus datasource 선택
```

---

## Verification

```bash
# 전체 검증
echo "=== NodePorts ==="
for port in 30090 30091 30092; do
  echo -n "  $port: "
  curl -s --max-time 3 -o /dev/null -w "%{http_code}\n" http://172.18.0.2:${port}/metrics
done

echo "=== Prometheus Targets ==="
curl -s http://172.18.0.10:9090/api/v1/targets | python3 -c "
import sys, json
d = json.load(sys.stdin)
jobs = ['kube-state-metrics', 'istiod', 'argo-rollouts']
for t in d['data']['activeTargets']:
    if t['labels'].get('job') in jobs:
        print(f\"  {t['labels']['job']}: {t['health']}\")
"

echo "=== k8s Nodes ==="
curl -s 'http://172.18.0.10:9090/api/v1/query?query=kube_node_info' | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f\"  {len(d['data']['result'])} nodes\")
"

echo "=== Alert Rules ==="
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d = json.load(sys.stdin)
total = sum(len(g['rules']) for g in d['data']['groups'] if g['name'] in ('kubernetes_alerts','etcd_alerts','istio_alerts','argocd_alerts'))
print(f'  k8s/etcd/istio/argocd rules: {total}')
"

echo "=== Alloy k8s Logs ==="
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --no-headers | awk '{print "  "$1": "$3}'
```

---

## Common Pitfalls

| 증상                                 | 원인                                            | 해결                                                 |
| ------------------------------------ | ----------------------------------------------- | ---------------------------------------------------- |
| alloy-k8s-logs CrashLoopBackOff      | readOnlyRootFilesystem + storage 경로 미설정    | `--storage.path=/var/lib/alloy` + emptyDir 볼륨 확인 |
| platform-monitoring InvalidSpecError | AppProject에 monitoring namespace 미포함        | human-approved bootstrap/break-glass로 AppProject 반영 |
| kube-state-metrics target down       | NodePort 30091 미배포                           | operator-triggered reconciliation: `argocd app sync platform-monitoring` |
| alert rules 로드 안 됨 (0 rules)     | rule_files 패턴에 alert_rules.k8s.yml 미포함    | prometheus.yml rule_files 확인                       |
| k8s 로그가 Loki에 없음               | alloy-k8s-logs 미실행 또는 loki-external 미연결 | alloy 파드 로그 + loki-external 서비스 확인          |

---

## Related Documents

- [Operations Policy](../policies/0006-k8s-observability-operations-policy.md)
- [Runbook](../runbooks/0009-k8s-observability-runbook.md)
- [ArgoCD 메트릭 가이드](./0006-argocd-prometheus-grafana-guide.md)
- [GitOps 리소스](../../../gitops/platform/monitoring)
