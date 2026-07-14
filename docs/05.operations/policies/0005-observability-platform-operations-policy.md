---
title: 'Observability Platform Operations Policy'
type: sdlc/policy
status: active
owner: platform
updated: 2026-05-22
---

# Observability Platform Operations Policy

## Overview

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
- Kiali 재확인은 [Kiali 연결 런북](../runbooks/0007-kiali-observability-connectivity-runbook.md)의 절차를 따른다.

**Disallowed**:

- 프로토콜 없이 서비스명만으로 포트 이름 설정 (예: `valkey`, `postgres-write`)
- 프로토콜을 suffix에 배치 (예: `otlp-grpc` → 위반)

**주의사항**: EndpointSlice는 ArgoCD `resource.exclusions`에 포함되어 자동 동기화되지 않을 수 있다. 기본 경로는 Git 파일 수정, 리뷰, 증적 기록이다. EndpointSlice 적용/패치 같은 실행 절차는 운영자가 명시 승인한 bootstrap 또는 break-glass 상황에서만 [Kiali 연결 런북](../runbooks/0007-kiali-observability-connectivity-runbook.md)을 따라 수행한다.

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

**Verification evidence**:

- `/api/frontend/settings`와 `/api/health`가 내부 네트워크에서 인증 없는 Viewer 수준 응답을 반환한다.
- Grafana 설정이 Anonymous Viewer로 제한되어 있고 Editor/Admin 권한이 노출되지 않는다.
- 상세 진단 명령은 [Kiali 연결 런북](../runbooks/0007-kiali-observability-connectivity-runbook.md)을 따른다.

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
- Prometheus 무중단 reload는 [ArgoCD 메트릭 런북](../runbooks/0008-argocd-metrics-prometheus-runbook.md)의 절차를 따른다.

**Disallowed**:

- 30082-30086 NodePort를 다른 서비스에 재사용
- Prometheus 컨테이너에 kubeconfig 마운트 (불필요한 k8s 권한 확대)
- ArgoCD metrics 수집을 위해 kube-prometheus-stack 별도 배포 (중복 구성)

**Verification evidence**:

- `argocd` namespace의 metrics NodePort 서비스가 예약 번호 30082-30086을 사용한다.
- Prometheus target에서 `argocd-*` jobs가 `up`이고 `argocd_app_info` 결과가 수집된다.
- 상세 진단/복구 명령은 [ArgoCD 메트릭 런북](../runbooks/0008-argocd-metrics-prometheus-runbook.md)을 따른다.

---

## Exceptions

- EndpointSlice 또는 AppProject live 반영은 운영자가 명시 승인한 bootstrap 또는 break-glass 상황에서만 허용한다.
- NodePort 번호 변경은 관련 Prometheus scrape config, README, runbook을 같은 변경에서 갱신할 때만 허용한다.

## Verification

정책 준수 여부는 아래 증적으로 확인한다. 실행 가능한 명령 순서, break-glass 적용, Prometheus reload 절차는 소유 런북으로 이동한다.

### Evidence Matrix

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Istio port naming | `platform` Service/EndpointSlice port names use valid protocol prefixes and avoid suffix-only protocol naming | [`../runbooks/0007-kiali-observability-connectivity-runbook.md`](../runbooks/0007-kiali-observability-connectivity-runbook.md) |
| Grafana anonymous viewer | Grafana internal API health/settings endpoints are reachable while anonymous role remains Viewer-only | [`../runbooks/0007-kiali-observability-connectivity-runbook.md`](../runbooks/0007-kiali-observability-connectivity-runbook.md) |
| ArgoCD metrics NodePort | Reserved NodePorts 30082-30086 are present only for ArgoCD metrics services | [`../runbooks/0008-argocd-metrics-prometheus-runbook.md`](../runbooks/0008-argocd-metrics-prometheus-runbook.md) |
| Prometheus ArgoCD targets | `argocd-*` Prometheus targets are `up` and `argocd_app_info` is populated | [`../runbooks/0008-argocd-metrics-prometheus-runbook.md`](../runbooks/0008-argocd-metrics-prometheus-runbook.md) |

---

## Review Cadence

- 관측성 포트, external service, Prometheus scrape target 변경 시마다 검토한다.
- Ingress/Grafana/Kiali 인증 경계 변경 시 관련 policy/runbook과 함께 검토한다.

### AI Agent Policy Section

이 정책은 인프라 리소스를 직접 관리하며 AI Agent 모델/프롬프트/평가 정책이 별도 적용되지 않는다.
단, Agent가 이 정책 범위의 리소스를 조작할 경우 [운영 거버넌스](../../00.agent-governance/README.md)에 따른다.

## Traceability

- [ArgoCD 메트릭 가이드](../guides/0006-argocd-prometheus-grafana-guide.md)
- [ArgoCD 메트릭 런북](../runbooks/0008-argocd-metrics-prometheus-runbook.md)
- [Kiali 연결 런북](../runbooks/0007-kiali-observability-connectivity-runbook.md)
- [Service Mesh Policy](./0003-service-mesh-cert-manager-policy.md)
