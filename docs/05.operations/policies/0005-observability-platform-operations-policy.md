---
title: "Observability Platform Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0005"
---

# Observability Platform Operations Policy

## Overview

이 문서는 local cluster와 외부 observability backend 사이의 메트릭·로그
수집 통제를 하나의 정책으로 정의한다. 서비스 포트, in-cluster Alloy 수집과 remote write,
Prometheus rule loading, Grafana 접근, AppProject destination을 다룬다.

## Policy Scope

- `gitops/platform/external-services/`의 Istio 포트 명명
- `gitops/platform/argocd/`와 `gitops/platform/monitoring/`의 metrics endpoint
- in-cluster Alloy에서 외부 Loki로 이어지는 로그 경계
- 외부 Prometheus/Grafana 설정과 `monitoring` AppProject destination

## Applies To

- **Systems**: `gitops/platform/`, `gitops/clusters/local/`, external observability workspace
- **Roles**: Platform Owner, Observability Owner, approved operator
- **Environment**: Linux server local cluster와 연결된 external observability services

## Controls

### Responsibilities

| Role | Responsibility | Escalation owner |
| --- | --- | --- |
| Platform Owner | Service, AppProject GitOps 계약을 승인한다. | Workspace Owner |
| Observability Owner | Prometheus, Grafana, Loki, Alloy 수집 계약을 유지한다. | Platform Owner |
| Approved operator | Runbook에 따라 runtime 증적과 복구 결과를 기록한다. | Platform Owner |

### Control Register

| Control | Accountable role | Enforcement surface | Evidence |
| --- | --- | --- | --- |
| OBS-001 port naming | Platform Owner | Service and EndpointSlice manifests | protocol-prefixed port names |
| OBS-002 ArgoCD metrics | Observability Owner | in-cluster Alloy `platform_pods` relabel for ArgoCD components | `argocd_app_info{cluster="k3d-hyhome"}` in the external Prometheus |
| OBS-003 cluster metrics | Observability Owner | in-cluster Alloy scrape of istiod, argo-rollouts, kube-state-metrics, kubelet, cAdvisor | `up{cluster="k3d-hyhome"}` by job and `app` |
| OBS-004 logs and rules | Observability Owner | Alloy deployment; external Prometheus rule config | Ready `{cluster="k3d-hyhome"}` streams; external rule groups when the external workspace defines them |
| OBS-006 in-cluster metric collection | Observability Owner | in-cluster Alloy `prometheus.remote_write` to `https://prometheus.hy.home.arpa/api/v1/write` through the external Traefik with Basic Auth (`monitoring/prometheus-api-auth`) and the `hy-home-root-ca` gateway CA, and `monitoring` egress to host `192.168.0.13:443` (ADR-0046) | `cluster="k3d-hyhome"` series for jobs `kubernetes-pods`, `kubelet`, `cadvisor` in the external Prometheus |
| OBS-005 access | Platform Owner | Grafana service account role and AppProject destinations | Viewer-only token and monitoring destination |

### Service Port Naming

`gitops/platform/external-services/`의 Service와 EndpointSlice 포트 이름은 `<protocol>[-suffix]` 형식이어야 한다.
현재 외부 계약은 Alloy `grpc-otlp`/`http-otlp`, Valkey `tcp-valkey`,
PostgreSQL `tcp-postgres-write`/`tcp-postgres-read`를 사용한다. suffix-only
이름이나 프로토콜이 없는 이름은 금지한다.

### In-Cluster Metric Collection

k8s 메트릭의 기준 수집 경로는 cluster 안 Alloy다
([ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md)).
Alloy는 pod IP와 API server proxy로 scrape하고 외부 Prometheus에 remote
write한다. 저장, 조회, alert rule은 외부 workspace가 소유한다. 외부
Prometheus의 NodePort static scrape와 metrics NodePort Service(`30082-30092`)는
폐지되었다. 그 target 주소 `172.18.0.2`는 외부 Traefik이었다.
`scripts/validate-infrastructure-contracts.sh`는 `gitops/platform`에 NodePort
Service가 다시 생기면 실패한다. 수집을 위해 과도한 kubeconfig 권한을 외부에
부여하지 않는다.

### Logs, Rules, and Access

- in-cluster `alloy-k8s-logs`는 `monitoring` namespace에서 Kubernetes API를
  통해 pod logs/events를 수집하고 `loki-external.platform.svc.cluster.local:3100`으로 전송한다.
- Alloy는 read-only root filesystem과 전용 storage path를 유지하며, k3d
  containerd 로그를 Docker socket 또는 host file mount로 수집하지 않는다.
- Prometheus `rule_files`는 필요한 고정 파일을 명시적으로 나열한다. glob이
  고정 파일의 존재를 암묵적으로 보장한다고 간주하지 않는다.
- 외부 Grafana는 익명 API 접근을 허용하지 않는다. Kiali는 Viewer role의 Grafana
  service account token(OpenBao `platform/grafana-api`, ESO `istio-system/kiali-grafana-auth`)으로
  호출한다. Editor/Admin token이나 익명 접근은 쓰지 않는다.
- `gitops/clusters/local/appproject-platform.yaml`은 `monitoring` destination을
  명시하며 wildcard destination으로 대체하지 않는다.

## Exceptions

AppProject live 변경은 [POL-0001](./0001-k8s-gitops-operations-policy.md#exceptions)의
공통 live 변경 예외를 따른다. 이 정책이 추가하는 조건은 manifest와 관련
Runbook을 같은 변경으로 동기화하는 것이다. 외부
Prometheus·Grafana·Loki 설정 변경은 외부 observability workspace가 소유하며
이 저장소의 Runbook은 그 결과를 검증만 한다.

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Istio and Grafana connectivity | protocol port names, Viewer-only token and Grafana health | [RUN-0007](../runbooks/0007-kiali-observability-connectivity-runbook.md) |
| ArgoCD metrics | ArgoCD components under `kubernetes-pods`, `argocd_app_info` presence | [RUN-0008](../runbooks/0008-argocd-metrics-prometheus-runbook.md) |
| Cluster metrics | `kubernetes-pods`, `kubelet`, `cadvisor` jobs with `cluster="k3d-hyhome"` | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| Alloy and Loki | deployment Ready and cluster-labelled streams received | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| Rules and AppProject | required rule groups load; monitoring destination present | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |

## Review Cadence

Service/EndpointSlice port, Alloy relabel rule, remote write endpoint, Alloy version,
rule file, Grafana role, Loki endpoint, AppProject destination 변경 시 검토한다.

## Traceability

- [Service Mesh and cert-manager Policy](./0003-service-mesh-cert-manager-policy.md)
- [Kiali Connectivity Runbook](../runbooks/0007-kiali-observability-connectivity-runbook.md)
- [ArgoCD Metrics Runbook](../runbooks/0008-argocd-metrics-prometheus-runbook.md)
- [K8s Observability Runbook](../runbooks/0009-k8s-observability-runbook.md)

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — current GitOps and external observability contracts have no reciprocal Spec or Task policy link | Platform Owner and Observability Owner | service naming, Alloy relabel and remote write, Prometheus/Grafana/Loki config, AppProject destination, owning Runbooks |
