# k8s Observability 복구 Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스 및 복구`

## Overview (KR)

이 런북은 k3d/k3s 클러스터의 메트릭/로그 수집 스택(kube-state-metrics, in-cluster Alloy, Prometheus alert_rules)에 장애가 발생했을 때 즉시 진단하고 복구하는 절차를 제공한다.

주된 장애 원인:

1. **kube-state-metrics 미배포**: NodePort 30091 미생성으로 Prometheus가 k8s 오브젝트 상태 메트릭 수집 불가
2. **alloy-k8s-logs CrashLoop**: `readOnlyRootFilesystem` + storage 경로 미설정, 또는 미지원 속성 사용
3. **alert_rules 미로드**: `prometheus.yml` rule_files 패턴이 고정 파일명을 커버하지 않아 0 rules 반환
4. **AppProject destinations 미포함**: `monitoring` 네임스페이스가 AppProject에 없어 Application 배포 실패
5. **k3d 재시작 후 NodePort 접근 실패**: 노드 IP 변경 또는 파드 재기동 지연

## When to Use

- Prometheus 타겟에서 `kube-state-metrics`, `istiod`, `argo-rollouts` job이 `down`으로 표시될 때
- Loki에서 `{cluster="k3d-hyhome"}` 쿼리 결과가 비어 있을 때
- `alloy-k8s-logs` 파드가 `CrashLoopBackOff` 상태일 때
- Grafana에서 `kube_pod_*`, `kube_deployment_*` 메트릭이 조회되지 않을 때
- alert_rules 로드 수가 0이거나 kubernetes_alerts 그룹이 없을 때

---

## 정상 상태 기준값

| 항목                          | 기준값                                                                  |
| ----------------------------- | ----------------------------------------------------------------------- |
| kube-state-metrics NodePort   | `172.18.0.2:30091/metrics` → HTTP 200                                   |
| istiod NodePort               | `172.18.0.2:30090/metrics` → HTTP 200                                   |
| argo-rollouts NodePort        | `172.18.0.2:30092/metrics` → HTTP 200                                   |
| alloy-k8s-logs 파드           | `1/1 Running`                                                           |
| Prometheus kube-state-metrics | `health: up`                                                            |
| Loki k8s 로그 스트림          | `{cluster="k3d-hyhome"}` → 스트림 수 > 0                                |
| Alert rules                   | kubernetes_alerts 13 + etcd_alerts 8 + istio_alerts 6 + argocd_alerts 4 |
| AppProject destinations       | `monitoring` 포함                                                       |

---

## Procedure 1: 전체 상태 진단

```bash
echo "=== NodePort 상태 ==="
for port in 30090 30091 30092; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  case $port in
    30090) label="istiod" ;;
    30091) label="kube-state-metrics" ;;
    30092) label="argo-rollouts" ;;
  esac
  echo "  $port ($label): HTTP $code"
done

echo "=== Prometheus k8s Targets ==="
curl -s http://172.18.0.10:9090/api/v1/targets | python3 -c "
import sys, json
d=json.load(sys.stdin)
jobs=['kube-state-metrics','istiod','argo-rollouts']
for t in d['data']['activeTargets']:
    if t['labels'].get('job') in jobs:
        print(' ', t['labels']['job'], '->', t['health'])
"

echo "=== alloy-k8s-logs 파드 상태 ==="
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs

echo "=== Alert Rules 로드 상태 ==="
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d=json.load(sys.stdin)
for g in d['data']['groups']:
    if g['name'] in ('kubernetes_alerts','etcd_alerts','istio_alerts','argocd_alerts'):
        print(f'  {g[\"name\"]}: {len(g[\"rules\"])} rules')
"

echo "=== Loki k8s 로그 ==="
curl -s -G "http://172.18.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('  스트림 수:', len(d['data']['result']))"
```

---

## Procedure 2: platform-monitoring ArgoCD App 배포 복구

> **Agent execution boundary**: AppProject 직접 적용은 human-approved bootstrap 또는 break-glass 전용이다. Agent는 기본적으로 Git 파일 수정, 리뷰, ArgoCD reconciliation 계획, 증적 정리까지만 수행한다.

```bash
# AppProject에 monitoring namespace 포함 확인
kubectl get appproject platform -n argocd \
  -o jsonpath='{.spec.destinations[*].namespace}' | tr ' ' '\n' | grep monitoring

# 없으면 human-approved bootstrap/break-glass로 직접 적용
kubectl apply -f gitops/clusters/local/appproject-platform.yaml

# namespace 먼저 배포
argocd app sync platform-namespaces

# monitoring 리소스 배포
argocd app sync platform-monitoring

# 배포 확인
kubectl get all -n monitoring
```

예상 출력:

```text
NAME                                  READY   STATUS    RESTARTS
pod/alloy-k8s-logs-xxxx              1/1     Running   0
pod/kube-state-metrics-xxxx          1/1     Running   0

NAME                          TYPE        CLUSTER-IP    PORT(S)
service/kube-state-metrics    ClusterIP   10.x.x.x      8080/TCP
service/kube-state-metrics-np NodePort    10.x.x.x      8080:30091/TCP
```

---

## Procedure 3: alloy-k8s-logs CrashLoop 복구

### 3-1. 원인 파악

```bash
# 최근 로그 확인
kubectl logs -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --tail=30

# 이벤트 확인
kubectl describe pod -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs
```

### 3-2. 오류 시그니처별 조치

| 오류 시그니처                                | 원인                             | 조치                                          |
| -------------------------------------------- | -------------------------------- | --------------------------------------------- |
| `mkdir data-alloy: read-only file system`    | `--storage.path` 미설정          | args에 `--storage.path=/var/lib/alloy` 추가   |
| `unrecognized attribute name 'extra_labels'` | Alloy v1.13.1 미지원 속성        | `loki.process` + `stage.static_labels`로 대체 |
| `failed to list pods: Forbidden`             | ClusterRole 권한 미할당          | ClusterRoleBinding 재적용                     |
| `connection refused` to `loki-external`      | ExternalService/Endpoints 미설정 | `platform` 네임스페이스 loki-external 확인    |

### 3-3. storage path 수정 후 재배포

`gitops/platform/monitoring/alloy-k8s-logs.yaml`의 Deployment args 확인:

```yaml
args:
  - run
  - --server.http.listen-addr=0.0.0.0:12345
  - --storage.path=/var/lib/alloy # 필수
  - /etc/alloy/config.alloy
```

```bash
# 기본 경로: ArgoCD sync
argocd app sync platform-monitoring
# human-approved break-glass only
kubectl apply -f gitops/platform/monitoring/alloy-k8s-logs.yaml
```

### 3-4. Loki 전송 확인

```bash
# Loki ExternalService 상태
kubectl get svc,endpoints -n platform loki-external

# alloy 로그에서 수집 확인
kubectl logs -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --tail=20 \
  | grep -E "tailer|loki.source.kubernetes|level=error"
```

---

## Procedure 4: Prometheus alert_rules 미로드 복구

```bash
# 현재 로드된 rule groups 확인
curl -s http://172.18.0.10:9090/api/v1/rules \
  | python3 -c "
import sys, json
d=json.load(sys.stdin)
for g in d['data']['groups']:
    print(g['name'])
"

# kubernetes_alerts/etcd_alerts/istio_alerts/argocd_alerts가 없으면
# hy-home.docker prometheus.yml rule_files 확인
cat /path/to/hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml | grep rule_files -A 10
```

`rule_files` 정상 설정:

```yaml
rule_files:
  - '/etc/prometheus/alert_rules/alert_rules.local.*.yml'
  - '/etc/prometheus/alert_rules/alert_rules.k8s.yml'
  - '/etc/prometheus/alert_rules/alert_rules.keycloak.yml'
  - '/etc/prometheus/alert_rules/alert_rules.vault.yml'
  - '/etc/prometheus/alert_rules/recording_rules.yml'
```

```bash
# Prometheus reload (설정 변경 후)
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"

# reload 후 확인
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d=json.load(sys.stdin)
total=sum(len(g['rules']) for g in d['data']['groups']
          if g['name'] in ('kubernetes_alerts','etcd_alerts','istio_alerts','argocd_alerts'))
print(f'k8s 관련 rules: {total}건 (기대: 31건)')
"
```

---

## Procedure 5: k3d 재시작 후 NodePort 복구

k3d 재시작 시 파드가 재기동되므로 NodePort 응답이 일시적으로 실패할 수 있다.

```bash
# 파드 Ready 확인
kubectl get pods -n monitoring
kubectl get pods -n istio-system -l app=istiod
kubectl get pods -n argo-rollouts

# 모두 Ready가 되면 NodePort 재테스트
for port in 30090 30091 30092; do
  code=$(curl -s --max-time 5 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: HTTP $code"
done

# Prometheus target 재확인
curl -s "http://172.18.0.10:9090/api/v1/targets" | python3 -c "
import sys, json
d=json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if t['labels'].get('job') in ('kube-state-metrics','istiod','argo-rollouts'):
        print(t['labels']['job'], '->', t['health'], '|', t.get('lastError',''))
"
```

k3d-hyhome-server-0 IP가 변경된 경우:

```bash
# 현재 IP 확인
docker inspect k3d-hyhome-server-0 | python3 -c "
import sys,json; d=json.load(sys.stdin)
ip=d[0]['NetworkSettings']['Networks']
for net,info in ip.items(): print(net, info['IPAddress'])
"

# prometheus.yml scrape target IP 업데이트 후 reload
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"
```

---

## Verification

```bash
echo "=== 전체 검증 ==="

echo "[1] NodePorts"
for port in 30090 30091 30092; do
  echo -n "  $port: "
  curl -s --max-time 3 -o /dev/null -w "%{http_code}\n" http://172.18.0.2:${port}/metrics
done

echo "[2] Prometheus Targets"
curl -s http://172.18.0.10:9090/api/v1/targets | python3 -c "
import sys, json
d=json.load(sys.stdin)
jobs=['kube-state-metrics','istiod','argo-rollouts']
for t in d['data']['activeTargets']:
    if t['labels'].get('job') in jobs:
        print(f\"  {t['labels']['job']}: {t['health']}\")
"

echo "[3] kube_node_info count"
curl -s 'http://172.18.0.10:9090/api/v1/query?query=kube_node_info' | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f\"  nodes: {len(d['data']['result'])} (기대: 4)\")
"

echo "[4] Alert Rules"
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d=json.load(sys.stdin)
for g in d['data']['groups']:
    if g['name'] in ('kubernetes_alerts','etcd_alerts','istio_alerts','argocd_alerts'):
        print(f\"  {g['name']}: {len(g['rules'])} rules\")
"

echo "[5] alloy-k8s-logs"
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --no-headers \
  | awk '{print "  "$1": "$3}'

echo "[6] Loki k8s log streams"
curl -s -G "http://172.18.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('  스트림:', len(d['data']['result']))"
```

---

## Troubleshooting

| 증상                                       | 원인                                               | 조치                                              |
| ------------------------------------------ | -------------------------------------------------- | ------------------------------------------------- |
| platform-monitoring InvalidSpecError       | AppProject에 monitoring namespace 미포함           | Git 파일 확인 후 human-approved bootstrap/break-glass로 AppProject 반영 |
| alloy CrashLoop: read-only file system     | `--storage.path` 미설정                            | args에 `--storage.path=/var/lib/alloy` + emptyDir |
| alloy CrashLoop: unrecognized extra_labels | `loki.source.kubernetes_events` 미지원 속성        | `loki.process` + `stage.static_labels` 파이프라인 |
| kube-state-metrics target down             | NodePort 30091 미배포                              | `argocd app sync platform-monitoring`             |
| alert rules 0건                            | rule_files 패턴이 고정 파일명 미포함               | prometheus.yml rule_files 항목 추가 후 reload     |
| Loki에 k8s 로그 없음                       | alloy-k8s-logs 미실행 또는 loki-external 연결 실패 | Procedure 3 참고                                  |
| NodePort HTTP 000 (timeout)                | 파드 미기동 또는 k3d 재시작 중                     | 파드 Ready 대기 후 재시도                         |

---

## Related Documents

- [k8s 관측성 부트스트랩 가이드](../07.guides/0007-k8s-observability-bootstrap-guide.md)
- [k8s Observability 운영 정책](../08.operations/0006-k8s-observability-operations-policy.md)
- [Observability Platform Policy](../08.operations/0005-observability-platform-operations-policy.md)
- [ArgoCD 메트릭 런북](./0008-argocd-metrics-prometheus-runbook.md)
