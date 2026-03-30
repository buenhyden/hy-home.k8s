# Observability Platform Operations Policy

## Overview (KR)

이 문서는 Prometheus/Grafana/Kiali 기반 관측성 플랫폼의 운영 통제 기준을 정의한다.
Istio 서비스 포트 네이밍 규칙, Grafana 인증 정책, ArgoCD 메트릭 수집 NodePort 할당을 포함한다.

## Policy Scope

- Istio 서비스 포트 네이밍 (`gitops/platform/external-services/`)
- Grafana anonymous access 정책 (`hy-home.docker/infra/06-observability/docker-compose.yml`)
- ArgoCD 메트릭 NodePort 할당 (`gitops/platform/argocd/argocd-metrics-nodeport.yaml`)
- Prometheus scrape 설정 (`hy-home.docker/infra/06-observability/prometheus/config/prometheus.yml`)

## Applies To

- **Systems**: `gitops/platform/external-services/`, `gitops/platform/argocd/`, `hy-home.docker/infra/06-observability/`
- **Agents**: 문서/운영 자동화 에이전트
- **Environments**: WSL2 local cluster

---

## Controls

### Istio 서비스 포트 네이밍 (KIA0601)

Kiali는 Service 포트 이름이 Istio 프로토콜 규칙을 따르는지 검사한다(KIA0601). 이름이 잘못되면 Kiali가 프로토콜을 인식하지 못해 트래픽 관리 및 메시 정책이 올바르게 적용되지 않는다.

**Required**:

- Service 및 EndpointSlice 포트 이름은 반드시 `<protocol>[-suffix]` 형식을 따른다.
- 프로토콜이 이름의 **앞**에 와야 한다. 유효 프로토콜: `grpc`, `http`, `https`, `tcp`, `udp`, `tls`, `mongo`, `mysql`, `redis`, `http2`, `grpc-web`

**현재 적용된 포트 이름 계약:**

| 서비스                  | 포트  | 포트 이름            | 프로토콜 근거  |
| ----------------------- | ----- | -------------------- | -------------- |
| alloy-external          | 4317  | `grpc-otlp`          | OTLP gRPC      |
| alloy-external          | 4318  | `http-otlp`          | OTLP HTTP/1.1  |
| valkey-external         | 6379  | `tcp-valkey`         | Redis 호환 TCP |
| postgres-write-external | 15432 | `tcp-postgres-write` | PostgreSQL TCP |
| postgres-read-external  | 15433 | `tcp-postgres-read`  | PostgreSQL TCP |

**Allowed**:

- `grpc-*`, `http-*`, `tcp-*` 접두사로 신규 포트 이름 추가
- Kiali 재확인: `kubectl get svc -n platform -o jsonpath='{.items[*].spec.ports[*].name}'`

**Disallowed**:

- 프로토콜 없이 서비스명만으로 포트 이름 설정 (예: `valkey`, `postgres-write`)
- 프로토콜을 suffix에 배치 (예: `otlp-grpc` → 위반)

**주의사항**: EndpointSlice는 ArgoCD `resource.exclusions`에 포함되어 자동 동기화되지 않는다. Service 포트 이름 변경 시 EndpointSlice도 반드시 `kubectl apply`로 수동 적용해야 한다.

```bash
# 포트 이름 규칙 검증
kubectl get svc -n platform -o custom-columns='NAME:.metadata.name,PORTS:.spec.ports[*].name'

# EndpointSlice 수동 적용 (포트 이름 변경 후)
kubectl apply -f gitops/platform/external-services/<service>.yaml
```

---

### Grafana Anonymous Access

Kiali 및 기타 내부 서비스는 Grafana API 엔드포인트(`/api/frontend/settings`, `/api/health`)를 헬스체크에 사용한다. Grafana가 OAuth 전용(`GF_AUTH_DISABLE_LOGIN_FORM=true`)으로 설정된 경우 인증 없는 API 호출이 401을 반환하여 Kiali가 Grafana를 Unreachable로 표시한다.

**Required**:

- Grafana에 Anonymous Viewer 접근 활성화:
  - `GF_AUTH_ANONYMOUS_ENABLED=true`
  - `GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer`
- 설정 파일: `hy-home.docker/infra/06-observability/docker-compose.yml` grafana 서비스 환경 변수

**Allowed**:

- Anonymous Org Role을 `Viewer`로 제한
- 브라우저 접근은 `GF_AUTH_OAUTH_AUTO_LOGIN=true`로 Keycloak OAuth 리다이렉트 유지

**Disallowed**:

- Anonymous Role을 `Editor` 또는 `Admin`으로 설정
- Anonymous 접근 비활성화 상태에서 Kiali Grafana URL 설정 (Unreachable 유발)

**보안 근거**: Grafana는 k3d-hyhome 내부 Docker 네트워크(172.18.0.0/16)에서만 접근 가능하다. Anonymous Viewer는 대시보드 조회만 허용하며 편집 권한이 없다. 브라우저에서의 Grafana 접근은 여전히 Keycloak OAuth 인증을 거친다.

```bash
# 검증
curl -s -o /dev/null -w "%{http_code}" \
  http://172.18.0.14:3000/api/frontend/settings
# → 200

# 컨테이너 내 설정 확인
docker exec infra-grafana bash -c "grep 'enabled = true' /etc/grafana/grafana.ini"
```

---

### ArgoCD 메트릭 NodePort 할당

Prometheus(Docker)가 k8s 내부 ArgoCD 메트릭을 수집하기 위해 NodePort 서비스를 사용한다. NodePort 번호는 고정값으로 재사용하지 않는다.

**Required**:

- NodePort 서비스는 `argocd` namespace에만 생성
- 아래 NodePort 번호 예약, 다른 서비스에 사용 금지

**NodePort 예약표:**

| 서비스 이름                                 | Pod Port      | NodePort  | 컴포넌트                  |
| ------------------------------------------- | ------------- | --------- | ------------------------- |
| argocd-application-controller-metrics-np    | 8082          | **30082** | application-controller    |
| argocd-server-metrics-np                    | 8083          | **30083** | server                    |
| argocd-repo-server-metrics-np               | 8084          | **30084** | repo-server               |
| argocd-applicationset-controller-metrics-np | 8080(metrics) | **30085** | applicationset-controller |
| argocd-notifications-controller-metrics-np  | 9001(metrics) | **30086** | notifications-controller  |

- Prometheus scrape 대상: `172.18.0.2:30082` ~ `172.18.0.2:30086` (k3d-hyhome-server-0)
- GitOps 파일: `gitops/platform/argocd/argocd-metrics-nodeport.yaml` (ArgoCD 관리)
- Prometheus job 이름 prefix: `argocd-`, label `domain: gitops`

**Allowed**:

- k3d 노드 IP 변경 시 Prometheus scrape target IP만 업데이트 (NodePort 번호 유지)
- `curl -X POST http://172.18.0.10:9090/-/reload`로 Prometheus 무중단 재설정

**Disallowed**:

- 30082-30086 NodePort를 다른 서비스에 재사용
- Prometheus 컨테이너에 kubeconfig 마운트 (불필요한 k8s 권한 확대)
- ArgoCD metrics 수집을 위해 kube-prometheus-stack 별도 배포 (중복 구성)

```bash
# NodePort 할당 현황 확인
kubectl get svc -n argocd -o custom-columns='NAME:.metadata.name,NODEPORT:.spec.ports[*].nodePort' \
  | grep metrics-np

# Prometheus에서 ArgoCD 메트릭 수집 확인
curl -s "http://172.18.0.10:9090/api/v1/query?query=argocd_app_info" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print('앱 수:', len(d['data']['result']))"
```

---

## Audit / Verification

```bash
# 1. Istio 포트 이름 전체 검증
kubectl get svc -n platform \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.ports[*]}{.name}{" "}{end}{"\n"}{end}'

# 2. Kiali 헬스체크 URL 검증
curl -s -o /dev/null -w "%{http_code}" http://172.18.0.14:3000/api/frontend/settings
# → 200

# 3. ArgoCD NodePort 전체 상태
for port in 30082 30083 30084 30085 30086; do
  code=$(curl -s --max-time 3 -o /dev/null -w "%{http_code}" http://172.18.0.2:${port}/metrics)
  echo "NodePort ${port}: ${code}"
done

# 4. Prometheus ArgoCD 타깃 상태
curl -s http://172.18.0.10:9090/api/v1/targets \
  | python3 -c "
import sys, json
d=json.load(sys.stdin)
for t in d['data']['activeTargets']:
    if 'argocd' in t['labels'].get('job',''):
        print(t['labels']['job'], t['health'])
"
```

---

## Related Documents

- [ArgoCD 메트릭 가이드](../07.guides/0006-argocd-prometheus-grafana-guide.md)
- [ArgoCD 메트릭 런북](../09.runbooks/0008-argocd-metrics-prometheus-runbook.md)
- [Kiali 연결 런북](../09.runbooks/0007-kiali-observability-connectivity-runbook.md)
- [Service Mesh Policy](./0003-service-mesh-cert-manager-policy.md)
