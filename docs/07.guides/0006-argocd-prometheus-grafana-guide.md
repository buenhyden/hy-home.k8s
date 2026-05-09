# ArgoCD Prometheus 메트릭 수집 및 Grafana 대시보드 가이드

## Overview (KR)

이 문서는 k3d 클러스터 외부에서 실행 중인 Prometheus(Docker)가 클러스터 내부 ArgoCD 메트릭을 수집하도록 설정하는 방법을 설명한다.

Prometheus는 k8s ServiceMonitor/PodMonitor를 사용할 수 없어(Docker 컨테이너, k8s 외부) NodePort 방식으로 각 ArgoCD 컴포넌트의 메트릭 포트를 클러스터 외부에 노출한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- DevOps Engineer

## Purpose

ArgoCD 앱 동기화 상태, 헬스 체크 결과, Git fetch 지연, repo-server 부하 등 GitOps 운영 지표를 Prometheus로 수집하고 Grafana 대시보드에서 시각화한다.

## Prerequisites

### 아키텍처 전제

| 컴포넌트            | 위치                            | IP / 포트        |
| ------------------- | ------------------------------- | ---------------- |
| Prometheus          | Docker (infra_net + k3d-hyhome) | 172.18.0.10:9090 |
| Grafana             | Docker (k3d-hyhome)             | 172.18.0.14:3000 |
| k3d-hyhome-server-0 | k3d 노드                        | 172.18.0.2       |
| ArgoCD              | k8s namespace `argocd`          | ClusterIP 내부   |

### 사전 확인

```bash
# k3d 노드 IP 확인 (server-0 기준)
docker network inspect k3d-hyhome \
  --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}' \
  | grep server-0
# → k3d-hyhome-server-0 172.18.0.2/16

# 기존 NodePort 충돌 확인
kubectl get svc -A -o jsonpath='{.items[*].spec.ports[*].nodePort}' \
  | tr ' ' '\n' | sort -n | grep -E "^3008[2-6]$"
# → 출력 없어야 함 (30082-30086 미사용)

# ArgoCD 파드 메트릭 포트 확인
kubectl get pod -n argocd -l app.kubernetes.io/name=argocd-server \
  -o jsonpath='{.items[0].spec.containers[0].ports[*].name}'
# → server metrics
```

---

## Procedure 1: NodePort 서비스 배포

`gitops/platform/argocd/argocd-metrics-nodeport.yaml`에 5개 NodePort 서비스를 정의하고 배포한다.

| 서비스                                      | Pod Port      | NodePort | 대상 컴포넌트             |
| ------------------------------------------- | ------------- | -------- | ------------------------- |
| argocd-application-controller-metrics-np    | 8082          | 30082    | application-controller    |
| argocd-server-metrics-np                    | 8083          | 30083    | argocd-server             |
| argocd-repo-server-metrics-np               | 8084          | 30084    | repo-server               |
| argocd-applicationset-controller-metrics-np | 8080(metrics) | 30085    | applicationset-controller |
| argocd-notifications-controller-metrics-np  | 9001(metrics) | 30086    | notifications-controller  |

```bash
# ArgoCD는 platform-argocd-config app이 관리하므로 ArgoCD sync로 배포됨
# operator-triggered reconciliation only
argocd app sync platform-argocd-config

# human-approved break-glass only
kubectl apply -f gitops/platform/argocd/argocd-metrics-nodeport.yaml

# 서비스 생성 확인
kubectl get svc -n argocd | grep metrics-np
```

**NodePort 접근 테스트:**

```bash
for port in 30082 30083 30084 30085 30086; do
  status=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" \
    http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: HTTP ${status}"
done
# 모두 200이어야 함

# application-controller 메트릭 샘플 확인
curl -s http://172.18.0.2:30082/metrics | grep "^argocd_app_info" | head -3
```

---

## Procedure 2: Prometheus Scrape 설정 추가

`hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml`의 `KUBERNETES / GITOPS` 섹션에 아래 5개 job을 추가한다.

```yaml
# ============================================================================
# KUBERNETES / GITOPS
# ============================================================================
# ArgoCD metrics via NodePort (k3d-hyhome-server-0: 172.18.0.2)
- job_name: 'argocd-application-controller'
  static_configs:
    - targets: ['172.18.0.2:30082']
      labels:
        component: 'application-controller'
        domain: 'gitops'

- job_name: 'argocd-server'
  static_configs:
    - targets: ['172.18.0.2:30083']
      labels:
        component: 'server'
        domain: 'gitops'

- job_name: 'argocd-repo-server'
  static_configs:
    - targets: ['172.18.0.2:30084']
      labels:
        component: 'repo-server'
        domain: 'gitops'

- job_name: 'argocd-applicationset-controller'
  static_configs:
    - targets: ['172.18.0.2:30085']
      labels:
        component: 'applicationset-controller'
        domain: 'gitops'

- job_name: 'argocd-notifications-controller'
  static_configs:
    - targets: ['172.18.0.2:30086']
      labels:
        component: 'notifications-controller'
        domain: 'gitops'
```

**Prometheus config reload:**

```bash
# lifecycle API로 무중단 reload (--web.enable-lifecycle 필요, 기존 설정에 포함됨)
curl -s -X POST http://172.18.0.10:9090/-/reload && echo "Reloaded"
```

---

## Procedure 3: Grafana 대시보드 확인

대시보드 파일이 이미 provisioning 디렉토리에 존재한다.

```bash
ls hy-home.docker/infra/06-observability/grafana/dashboards/ | grep ArgoCD
# → ArgoCD-1774772992626.json  (title: "ArgoCD", 16 panels)
```

브라우저에서 `https://grafana.127.0.0.1.nip.io` → Dashboards → "ArgoCD"로 이동한다.

대시보드가 없다면 Grafana에 직접 import한다:

```bash
# 커뮤니티 대시보드 (ID: 14584 - ArgoCD Operational Overview)
# Grafana UI → Dashboards → Import → 14584 입력
```

---

## Verification

```bash
# 1. NodePort 직접 확인
curl -s http://172.18.0.2:30082/metrics | head -5
# → # HELP argocd_app_info Information about application.

# 2. Prometheus target 상태 확인
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

# 3. 앱 수집 수 확인
curl -s "http://172.18.0.10:9090/api/v1/query?query=argocd_app_info" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('수집된 앱 수:', len(d['data']['result']))
"
# → 수집된 앱 수: 18 (이상)
```

---

## Common Pitfalls

| 증상                                 | 원인                                                             | 해결                                       |
| ------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------ |
| NodePort curl timeout                | ArgoCD 파드 미실행 또는 selector 불일치                          | `kubectl get pod -n argocd` 확인           |
| Prometheus target `down`             | prometheus.yml 미reload                                          | `curl -X POST .../9090/-/reload`           |
| port 30085/30086 200이나 메트릭 없음 | applicationset/notifications의 targetPort가 이름(`metrics`) 참조 | `kubectl describe svc -n argocd ...-np`    |
| k3d 재시작 후 NodePort 불통          | 노드 IP 변경 가능성                                              | `docker network inspect k3d-hyhome` 재확인 |
| Grafana 대시보드 데이터 없음         | datasource 이름 불일치                                           | 대시보드 datasource를 `Prometheus`로 변경  |

---

## Related Documents

- [Operations Policy](../08.operations/0005-observability-platform-operations-policy.md)
- [Runbook](../09.runbooks/0008-argocd-metrics-prometheus-runbook.md)
- [Kiali Connectivity Runbook](../09.runbooks/0007-kiali-observability-connectivity-runbook.md)
