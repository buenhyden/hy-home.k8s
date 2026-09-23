---
title: "In-Cluster Telemetry Collection with an External Backend"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
artifact_id: "ADR-0045"
---

# ADR-0045: In-Cluster Telemetry Collection with an External Backend

## Overview

이 ADR은 k8s 관측을 어디에 둘지 검토한 결과를 기록한다. 저장과 조회
(Prometheus, Loki, Tempo, Grafana, Alertmanager)는 외부 서비스
workspace(`hy-home.docker`)에 남긴다. k8s telemetry의 수집은 이 저장소의
cluster 안 Alloy가 맡고, 외부 backend로 push한다.

## Context

2026-09-23 기준 상태는 다음과 같다.

- 외부 workspace의 관측 stack은 실행 중이다. docker 서비스의 메트릭, 로그,
  trace를 이미 한 Grafana에서 보고 있고, Prometheus는
  `--web.enable-remote-write-receiver`로 기동한다.
- k8s 메트릭은 외부 Prometheus가 `172.18.0.2:30082-30092` NodePort를 static
  target으로 scrape한다. 그런데 외부 workspace의 Traefik이 `k3d-hyhome`
  network에서 `172.18.0.2`를 고정으로 쓰므로, 이 target은 k3d node가 아니라
  Traefik을 가리킨다.
- sidecar의 `istio_requests_total`(port `15090`), kubelet과 cAdvisor
  메트릭은 수집되지 않는다. 그래서 외부 Prometheus를 쓰는 Kiali의 트래픽
  graph에 데이터가 없다.
- 이 저장소의 Alloy(`gitops/platform/monitoring/alloy-k8s-logs.yaml`)는 pod
  로그와 event를 외부 Loki로 push하며, `nodes/proxy`를 포함한 조회 권한을
  이미 가진다.
- 이 저장소에는 persistent storage가 없다
  ([ADR-0044](./0044-stateful-data-stores-stay-external.md)).

## Decision

- Prometheus, Loki, Tempo, Grafana, Alertmanager는 외부 workspace에 남는다.
  k8s 안에 두 번째 저장 backend나 Grafana를 두지 않는다.
- k8s telemetry의 수집은 cluster 안 Alloy가 소유한다. Alloy는 Kubernetes
  service discovery로 다음을 scrape한다.
  - pod annotation과 Istio sidecar `15090`
  - kube-state-metrics
  - kubelet과 cAdvisor(`nodes/proxy`)
  - istiod, ArgoCD, Argo Rollouts
- Alloy는 수집한 메트릭을 `prometheus-external`의 remote write endpoint로
  push한다. 모든 series에 `cluster="k3d-hyhome"` label을 붙인다.
- 외부 Prometheus의 k3d static scrape job과 이 저장소의 metrics NodePort
  Service(`30082-30092`)는 새 경로가 검증된 뒤 폐지한다.
- trace는 Istio가 `alloy-external`의 OTLP endpoint로 보내는 경로를 후속으로
  둔다. 이 결정은 메트릭과 로그 수집만 확정한다.

## Explicit Non-goals

- 외부 관측 stack의 구성, 보존 기간, alert rule 변경
- kube-prometheus-stack, Prometheus Operator, cluster 안 Grafana 도입
- 외부 Prometheus의 static job 삭제 작업. 외부 workspace가 소유한다

## Consequences

- **Positive**:
  - k3d node 주소나 NodePort에 의존하지 않으므로 `172.18.0.2` 충돌이
    사라진다.
  - pod와 sidecar 메트릭이 수집되어 Kiali graph와 Rollouts analysis가 실제
    데이터를 쓴다.
  - 관측 데이터의 수명이 k3d cluster 재생성과 분리되고, 조회 창은 하나로
    남는다.
- **Trade-offs**:
  - 외부 Prometheus의 remote write 수신과 `prometheus-external` egress에
    의존한다.
  - Alloy 설정이 로그와 메트릭 수집을 함께 가지므로 설정 파일이 커진다.
- **Operational**:
  - 외부 workspace는 k3d static scrape job을 폐지하고 remote write 수신을
    유지한다.

## Alternatives

### 관측 전체를 k8s로 이전(kube-prometheus-stack)

- Good:
  - Kubernetes 표준 도구와 ServiceMonitor를 쓴다.
- Bad:
  - 저장 backend와 Grafana가 두 벌이 되고 조회 창이 갈린다.
  - persistent storage가 없어 cluster 재생성 때 이력을 잃는다.
  - single host 자원 예산을 크게 쓴다.

### 외부 Prometheus가 계속 직접 scrape

- Good:
  - 이 저장소의 변경이 적다.
- Bad:
  - docker network에서 pod IP로 service discovery를 하려면 cluster
    credential과 routing이 추가로 필요하다. static NodePort 방식은 이미
    주소 충돌로 깨져 있다.

## Traceability

**Current-state clarification (2026-09-23).** The metrics NodePort
Services (`30082-30092`) are retired before live remote write evidence, because
the external workspace removed their static scrape jobs (`hy-home.docker` PR
#218) and no consumer remained. Remote write now reaches the host address under
[ADR-0046](./0046-external-services-over-host-addresses.md). The rest of this
decision is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0009](./0009-kiali-external-observability.md) | Keeps ADR-0009's external observability backend; moves k8s metric collection into the cluster | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
