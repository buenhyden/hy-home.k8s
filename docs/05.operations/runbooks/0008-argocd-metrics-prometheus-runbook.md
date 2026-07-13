---
title: 'ArgoCD 메트릭 Prometheus 수집 복구 Runbook'
type: sdlc/runbook
status: active
owner: platform
updated: 2026-05-09
---

# ArgoCD 메트릭 Prometheus 수집 복구 Runbook

## Runbook Type

`maintenance`

## Overview

이 런북은 Prometheus(Docker)가 ArgoCD 메트릭을 정상적으로 수집하지 못할 때 진단하고 복구하는 절차를 제공한다.

ArgoCD는 k3d 클러스터 내부에서 실행되며, Prometheus는 Docker 컨테이너(k3d 외부)에서 실행된다. ServiceMonitor를 사용할 수 없으므로 NodePort(30082-30086)를 통해 메트릭 포트를 클러스터 외부에 노출한다.

주된 원인은 세 가지다:

1. **k3d 재시작 후 노드 IP 변경**: k3d-hyhome-server-0의 IP가 바뀌면 Prometheus scrape target(`172.18.0.2:30082~30086`)이 실패한다.
2. **NodePort 서비스 미배포**: `argocd-metrics-nodeport.yaml`이 아직 ArgoCD에 의해 동기화되지 않았거나, ArgoCD app이 OutOfSync 상태이다.
3. **Prometheus config 미reload**: `prometheus.yml`을 수정했으나 Prometheus 프로세스에 반영되지 않았다.

### Purpose

ArgoCD metrics NodePort와 Prometheus scrape 상태를 진단하고, k3d 재시작 또는 config drift 이후 메트릭 수집을 복구한다.

## Canonical References

- [Operations Policy](../policies/0005-observability-platform-operations-policy.md)
- [Guide](../guides/0006-argocd-prometheus-grafana-guide.md)
- [NodePort YAML](../../../gitops/platform/argocd/argocd-metrics-nodeport.yaml)
- External sibling workspace path: `hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml`

## When to Use

- Prometheus 타겟에서 `argocd-*` job이 `down`으로 표시될 때
- k3d 재시작 후 ArgoCD 메트릭이 수집되지 않을 때
- `argocd_app_info` 메트릭이 Grafana에서 조회되지 않을 때
- NodePort curl이 timeout 또는 connection refused가 날 때

---

## Procedure or Checklist

아래 절차는 연결 상태 진단, NodePort 서비스 재배포, k3d 노드 IP 변경 대응, Prometheus config reload 순서로 수행한다.

### NodePort 정상 상태 기준값

| 서비스                                      | Pod Port | NodePort  | 컴포넌트                  |
| ------------------------------------------- | -------- | --------- | ------------------------- |
| argocd-application-controller-metrics-np    | 8082     | **30082** | application-controller    |
| argocd-server-metrics-np                    | 8083     | **30083** | argocd-server             |
| argocd-repo-server-metrics-np               | 8084     | **30084** | repo-server               |
| argocd-applicationset-controller-metrics-np | 8080     | **30085** | applicationset-controller |
| argocd-notifications-controller-metrics-np  | 9001     | **30086** | notifications-controller  |

- k3d-hyhome-server-0 정상 IP: `172.18.0.2`
- Prometheus scrape target: `172.18.0.2:30082` ~ `172.18.0.2:30086`
- GitOps 파일: `gitops/platform/argocd/argocd-metrics-nodeport.yaml`

---

### Procedure 1: 연결 상태 진단

### 1-1. NodePort 직접 curl 테스트

```bash
for port in 30082 30083 30084 30085 30086; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: HTTP ${code}"
done
# 모두 200이어야 함
```

### 1-2. Prometheus target 상태 확인

```bash
curl -s "http://172.18.0.10:9090/api/v1/targets" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if 'argocd' in t['labels'].get('job', ''):
        print(t['labels']['job'], '->', t['health'], t.get('lastError', ''))
"
```

### 1-3. ArgoCD NodePort 서비스 존재 여부 확인

```bash
kubectl get svc -n argocd -o custom-columns='NAME:.metadata.name,NODEPORT:.spec.ports[*].nodePort' \
  | grep metrics-np
```

출력이 없으면 NodePort 서비스가 미배포 상태 → Procedure 2로 이동.

### 1-4. k3d 노드 IP 확인 (IP 변경 여부)

```bash
docker network inspect k3d-hyhome \
  --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}' \
  | grep server-0
# → k3d-hyhome-server-0 172.18.0.2/16 (정상)
```

IP가 다르면 Procedure 3으로 이동.

---

### Procedure 2: NodePort 서비스 재배포

NodePort 서비스가 없거나 ArgoCD가 OutOfSync인 경우:

```bash
# ArgoCD 동기화로 배포 (권장)
# operator-triggered reconciliation only
argocd app sync platform-argocd-config

# 동기화 후 서비스 확인
kubectl get svc -n argocd | grep metrics-np
```

ArgoCD가 접근 불가능한 경우에도 직접 배포는 human-approved break-glass로만 수행한다.

```bash
# human-approved break-glass only
kubectl apply -f gitops/platform/argocd/argocd-metrics-nodeport.yaml

# 배포 확인
kubectl get svc -n argocd | grep metrics-np
```

NodePort 접근 재확인:

```bash
for port in 30082 30083 30084 30085 30086; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: HTTP ${code}"
done
```

---

### Procedure 3: k3d 노드 IP 변경 대응

k3d 재시작 후 노드 IP가 변경된 경우:

```bash
# 1. 신규 서버 노드 IP 확인
NEW_IP=$(docker network inspect k3d-hyhome \
  --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}' \
  | grep server-0 | awk '{print $2}' | cut -d'/' -f1)
echo "New server IP: ${NEW_IP}"
```

`hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml` 에서 기존 IP를 새 IP로 교체한다:

```bash
# 변경 전 (기존 IP 확인)
grep "172.18.0." hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml \
  | grep "3008[2-6]"

# 변경 후 Prometheus reload
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"
```

> **주의**: NodePort 번호(30082-30086)는 변경하지 않는다. IP만 갱신한다.

---

### Procedure 4: Prometheus config reload

`prometheus.yml`을 수정했으나 Prometheus에 반영되지 않은 경우:

```bash
# lifecycle API로 무중단 reload
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"

# reload 후 target 상태 확인 (30초 대기)
sleep 5
curl -s "http://172.18.0.10:9090/api/v1/targets" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if 'argocd' in t['labels'].get('job', ''):
        print(t['labels']['job'], '->', t['health'])
"
```

---

## Verification Steps

복구 완료 후 최종 검증:

```bash
# 1. NodePort 전체 200 확인
for port in 30082 30083 30084 30085 30086; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: HTTP ${code}"
done
# → 모두 200

# 2. Prometheus target 전체 up 확인
curl -s "http://172.18.0.10:9090/api/v1/targets" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if 'argocd' in t['labels'].get('job', ''):
        print(t['labels']['job'], '->', t['health'])
"
# → argocd-application-controller -> up
# → argocd-server -> up
# → argocd-repo-server -> up
# → argocd-applicationset-controller -> up
# → argocd-notifications-controller -> up

# 3. argocd_app_info 메트릭 수집 수 확인
curl -s "http://172.18.0.10:9090/api/v1/query?query=argocd_app_info" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('수집된 앱 수:', len(d['data']['result']))
"
# → 수집된 앱 수: 10 이상 (ArgoCD 관리 앱 수 기준)
```

---

## Observability and Evidence Sources

- **Signals**: NodePort HTTP status, Prometheus target health, `argocd_app_info` query result, ArgoCD component pod readiness.
- **Evidence to Capture**: target health output, NodePort curl results, Prometheus reload result, changed scrape target diff.

## Safe Rollback or Recovery Procedure

- Incorrect Prometheus scrape target changes should be reverted in the owning Prometheus config.
- Incorrect NodePort service changes should be reverted through GitOps rather than ad hoc cluster edits.
- If k3d node IP drift is temporary, wait for pod readiness before changing persistent scrape targets.

### Troubleshooting

### ArgoCD 파드 미실행으로 NodePort timeout

```bash
# ArgoCD 파드 상태 확인
kubectl get pod -n argocd

# 특정 컴포넌트 파드 로그 확인
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller --tail=20
```

### port 30085/30086: 200 응답이나 메트릭 없음

applicationset-controller와 notifications-controller는 `targetPort: metrics`(이름 참조) 방식이다.

```bash
# selector 확인
kubectl describe svc -n argocd argocd-applicationset-controller-metrics-np
kubectl describe svc -n argocd argocd-notifications-controller-metrics-np

# 실제 엔드포인트 확인
kubectl get endpoints -n argocd argocd-applicationset-controller-metrics-np
```

### Prometheus container 접근 불가

```bash
# Prometheus container 상태 확인
docker ps | grep prometheus

# Prometheus 헬스체크
curl -s http://172.18.0.10:9090/-/healthy
# → Prometheus Server is Healthy.
```

### Prometheus config 문법 오류

```bash
# 컨테이너 내에서 config 검증
docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
# → SUCCESS
```

---

### 오류 시그니처 요약

| 오류 증상                                            | 원인                                          | 해결 절차                    |
| ---------------------------------------------------- | --------------------------------------------- | ---------------------------- |
| `curl: (28) Connection timed out`                    | k3d 노드 IP 변경 또는 파드 미실행             | Procedure 3                  |
| `curl: (7) Failed to connect`                        | NodePort 서비스 미배포                        | Procedure 2                  |
| Prometheus target `down`                             | prometheus.yml 미reload 또는 IP 불일치        | Procedure 4                  |
| 메트릭 수집 0건 (target up이나 argocd_app_info 없음) | scrape_interval 아직 미경과 또는 job명 불일치 | 30초 대기 후 재확인          |
| `YAML syntax error` in prometheus.yml                | config 문법 오류                              | `promtool check config` 실행 |

---

### Agent Operations

이 런북은 인프라 절차를 다루며 AI Agent 모델/프롬프트 롤백이 직접 적용되지 않는다.
단, Agent가 이 런북을 자동화하는 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Traceability

- **Kiali Connectivity Runbook**: [`./0007-kiali-observability-connectivity-runbook.md`](./0007-kiali-observability-connectivity-runbook.md)
- **k8s Observability Runbook**: [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)
