# k8s Observability Operations Policy

## Overview (KR)

이 문서는 k3d/k3s 클러스터(k3d-hyhome)의 메트릭/로그 수집 관련 운영 통제 기준을 정의한다.
kube-state-metrics NodePort 예약, in-cluster Alloy 로그 수집, Prometheus alert_rules 로드 패턴, k8s NodePort 예약 범위를 포함한다.

## Policy Scope

- kube-state-metrics / istiod / argo-rollouts NodePort 할당 (`gitops/platform/monitoring/`)
- in-cluster Alloy 로그 수집 정책 (`gitops/platform/monitoring/alloy-k8s-logs.yaml`)
- Prometheus alert_rules 로드 패턴 (`hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml`)
- AppProject destinations 관리 (`gitops/clusters/local/appproject-platform.yaml`)

## Applies To

- **Systems**: `gitops/platform/monitoring/`, `hy-home.docker/infra/06-observability/`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster (k3d-hyhome)

---

## Controls

### k8s 메트릭 NodePort 예약

Prometheus(Docker)가 k8s 클러스터 내부 메트릭을 수집하기 위해 NodePort 서비스를 사용한다.
NodePort 번호는 고정값으로 예약하며, 다른 서비스에 재사용하지 않는다.

**Required**:

- 아래 NodePort 번호는 클러스터 메트릭 수집 전용으로 예약
- NodePort 서비스는 각 컴포넌트 네임스페이스에 생성

**NodePort 예약표:**

| 서비스 이름              | 네임스페이스  | Pod Port | NodePort  | 컴포넌트           |
| ------------------------ | ------------- | -------- | --------- | ------------------ |
| kube-state-metrics-np    | monitoring    | 8080     | **30091** | kube-state-metrics |
| istiod-metrics-np        | istio-system  | 15014    | **30090** | istiod             |
| argo-rollouts-metrics-np | argo-rollouts | 8090     | **30092** | argo-rollouts      |

- Prometheus scrape 대상: `172.18.0.2:30090~30092` (k3d-hyhome-server-0)
- GitOps 파일:
  - `gitops/platform/monitoring/kube-state-metrics.yaml`
  - `gitops/platform/monitoring/metrics-nodeports.yaml`

**Allowed**:

- k3d 노드 IP 변경 시 Prometheus scrape target IP만 업데이트 (NodePort 번호 유지)
- `curl -X POST http://172.18.0.10:9090/-/reload`로 Prometheus 무중단 재설정

**Disallowed**:

- 30090-30092 NodePort를 다른 서비스에 재사용
- kube-state-metrics를 NodePort 없이 ClusterIP만으로 운영 (Prometheus에서 접근 불가)

```bash
# NodePort 할당 현황 확인
kubectl get svc -n monitoring -o custom-columns='NAME:.metadata.name,NODEPORT:.spec.ports[*].nodePort'
kubectl get svc -n istio-system -l app=istiod -o custom-columns='NAME:.metadata.name,NODEPORT:.spec.ports[*].nodePort'
kubectl get svc -n argo-rollouts -o custom-columns='NAME:.metadata.name,NODEPORT:.spec.ports[*].nodePort'

# NodePort 접근 검증
for port in 30090 30091 30092; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: ${code}"
done
# → 모두 200
```

---

### in-cluster Alloy k8s 로그 수집

k3d는 containerd를 사용하므로 외부 Docker 소켓 기반 Alloy는 k3d 파드 로그를 수집할 수 없다.
클러스터 내부에 Alloy Deployment를 배포하여 k8s API 기반으로 파드 로그와 이벤트를 수집한다.

**Required**:

- in-cluster Alloy는 `monitoring` 네임스페이스에 `alloy-k8s-logs` Deployment로 배포
- `loki.source.kubernetes` 컴포넌트로 파드 로그 수집 (파일 마운트 불필요)
- `loki.source.kubernetes_events` + `loki.process` 파이프라인으로 이벤트 수집
- `--storage.path=/var/lib/alloy` 인자 + `emptyDir` 볼륨 마운트 필수 (`readOnlyRootFilesystem: true` 환경)
- Loki 전송 대상: `loki-external.platform.svc.cluster.local:3100` (ExternalService)

**Required Labels**:

| 레이블      | 값                  | 소스                                                 |
| ----------- | ------------------- | ---------------------------------------------------- |
| `cluster`   | `k3d-hyhome`        | static (discovery.relabel)                           |
| `env`       | `dev`               | static (discovery.relabel)                           |
| `namespace` | pod 네임스페이스    | `__meta_kubernetes_namespace`                        |
| `pod`       | 파드 이름           | `__meta_kubernetes_pod_name`                         |
| `container` | 컨테이너 이름       | `__meta_kubernetes_pod_container_name`               |
| `app`       | app label 값        | `__meta_kubernetes_pod_label_app_kubernetes_io_name` |
| `job`       | `kubernetes-events` | static (events only, loki.process)                   |

**Allowed**:

- 수집 제외: `observability.logs/disabled: "true"` 애노테이션 설정
- 자동 제외: `Succeeded`, `Failed` 상태 파드

**Disallowed**:

- `loki.source.kubernetes_events`의 `extra_labels` 속성 사용 (Alloy v1.13.1 미지원)
  → 반드시 `loki.process` + `stage.static_labels`로 대체
- `readOnlyRootFilesystem: true` 없이 Alloy 배포 (보안 미준수)
- Alloy를 DaemonSet으로 배포 (파일 마운트 기반 방식 — k3d containerd에서 불가)

```bash
# Alloy 파드 상태 확인
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs

# Loki에서 k8s 파드 로그 수신 확인
curl -s -G "http://172.18.0.13:3100/loki/api/v1/query" \
  --data-urlencode 'query={cluster="k3d-hyhome"}' \
  --data-urlencode "limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('스트림:', len(d['data']['result']))"
```

---

### Prometheus alert_rules 로드 패턴

Prometheus `rule_files`는 glob 패턴을 지원하지만, 패턴이 맞지 않으면 파일이 로드되지 않아도 오류 없이 0개의 rule을 반환한다.

**Required**:

- `rule_files`에 각 alert_rules 파일을 **명시적**으로 나열
- glob 패턴(`alert_rules.local.*.yml`)에만 의존 금지 — 고정 파일명은 별도 항목으로 추가

**현재 설정 (정상):**

```yaml
rule_files:
  - '/etc/prometheus/alert_rules/alert_rules.local.*.yml'
  - '/etc/prometheus/alert_rules/alert_rules.k8s.yml'
  - '/etc/prometheus/alert_rules/alert_rules.keycloak.yml'
  - '/etc/prometheus/alert_rules/alert_rules.vault.yml'
  - '/etc/prometheus/alert_rules/recording_rules.yml'
```

**Disallowed**:

- glob 패턴 하나(`alert_rules.local.*.yml`)로 모든 rule 파일 커버 시도
- 신규 alert_rules 파일 추가 시 `rule_files` 항목 미추가

```bash
# alert_rules 로드 상태 확인
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d = json.load(sys.stdin)
for g in d['data']['groups']:
    if g['name'] in ('kubernetes_alerts', 'etcd_alerts', 'istio_alerts', 'argocd_alerts'):
        print(f\"{g['name']}: {len(g['rules'])} rules\")
"
# 기대값: kubernetes_alerts: 13, etcd_alerts: 8, istio_alerts: 6, argocd_alerts: 4
```

---

### AppProject destinations 관리

ArgoCD Application이 새 네임스페이스에 리소스를 배포하려면 AppProject destinations에 해당 네임스페이스가 포함되어야 한다.

**Required**:

- 새 네임스페이스 추가 시 `gitops/clusters/local/appproject-platform.yaml` destinations에 명시
- AppProject 변경 후 live 반영은 운영자 승인 하의 bootstrap 또는 break-glass 절차로만 수행

**현재 destinations 목록:**

```text
argocd, ingress-nginx, external-secrets, platform, cert-manager,
istio-system, headlamp, argo-rollouts, metallb-system, monitoring
```

**Disallowed**:

- AppProject destinations 미추가 상태에서 Application 배포 시도 (→ InvalidSpecError)
- Agent가 AppProject 변경을 직접 `kubectl apply`로 반영
- AppProject 변경을 ArgoCD UI/CLI sync에만 의존하고 승인된 bootstrap/break-glass 증적을 남기지 않는 것

```bash
# AppProject destinations 확인
kubectl get appproject platform -n argocd -o jsonpath='{.spec.destinations[*].namespace}'

# monitoring 포함 여부 확인
kubectl get appproject platform -n argocd \
  -o jsonpath='{.spec.destinations[*].namespace}' | tr ' ' '\n' | grep monitoring
```

---

## Exceptions

- AppProject live 반영은 운영자가 명시 승인한 bootstrap 또는 break-glass 상황에서만 허용한다.
- NodePort 번호 변경은 Prometheus scrape target, manifest, runbook을 같은 변경에서 갱신할 때만 허용한다.

## Verification

아래 Audit / Verification 명령으로 NodePort 예약 상태, Prometheus target, alert rules, Alloy 로그 수집, AppProject destinations를 확인한다.

## Audit / Verification

```bash
echo "=== NodePort 예약 상태 ==="
for port in 30090 30091 30092; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "  NodePort ${port}: ${code}"
done

echo "=== Prometheus k8s Targets ==="
curl -s http://172.18.0.10:9090/api/v1/targets | python3 -c "
import sys, json
d=json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if t['labels'].get('job') in ('kube-state-metrics','istiod','argo-rollouts'):
        print(' ', t['labels']['job'], '->', t['health'])
"

echo "=== Alert Rules ==="
curl -s http://172.18.0.10:9090/api/v1/rules | python3 -c "
import sys, json
d=json.load(sys.stdin)
for g in d['data']['groups']:
    if g['name'] in ('kubernetes_alerts','etcd_alerts','istio_alerts','argocd_alerts'):
        print(f\"  {g['name']}: {len(g['rules'])} rules\")
"

echo "=== Alloy k8s Logs ==="
kubectl get pods -n monitoring -l app.kubernetes.io/name=alloy-k8s-logs --no-headers \
  | awk '{print "  "$1": "$3}'

echo "=== AppProject Destinations ==="
kubectl get appproject platform -n argocd \
  -o jsonpath='{.spec.destinations[*].namespace}' | tr ' ' '\n' | sort
```

---

## Review Cadence

- monitoring namespace, NodePort, alert_rules, Alloy 설정 변경 시마다 검토한다.
- k3d/k3s 버전 또는 observability backend 주소가 바뀌면 관련 Spec/Runbook과 함께 검토한다.

## Related Documents

- [k8s 관측성 부트스트랩 가이드](../guides/0007-k8s-observability-bootstrap-guide.md)
- [k8s 관측성 런북](../runbooks/0009-k8s-observability-runbook.md)
- [Observability Platform Policy](./0005-observability-platform-operations-policy.md)
- [ArgoCD 메트릭 가이드](../guides/0006-argocd-prometheus-grafana-guide.md)
