---
title: "Observability Platform Operations Policy"
version: "1.0"
type: sdlc/policy
layer: "05.operations"
status: active
owner: platform
updated: 2026-09-01
artifact_id: "POL-0005"
---

# Observability Platform Operations Policy

## Overview

이 문서는 local cluster와 외부 observability backend 사이의 메트릭·로그
수집 통제를 하나의 정책으로 정의한다. 서비스 포트, 고정 NodePort, Alloy,
Prometheus rule loading, Grafana 접근, AppProject destination을 다룬다.

## Policy Scope

- `gitops/platform/external-services/`의 Istio 포트 명명
- `gitops/platform/argocd/`와 `gitops/platform/monitoring/`의 metrics endpoint
- in-cluster Alloy에서 외부 Loki로 이어지는 로그 경계
- 외부 Prometheus/Grafana 설정과 `monitoring` AppProject destination

## Applies To

- **Systems**: `gitops/platform/`, `gitops/clusters/local/`, external observability workspace
- **Roles**: Platform Owner, Observability Owner, approved operator
- **Environment**: WSL2 local cluster와 연결된 external observability services

## Controls

### Responsibilities

| Role | Responsibility | Escalation owner |
| --- | --- | --- |
| Platform Owner | Service, NodePort, AppProject GitOps 계약을 승인한다. | Workspace Owner |
| Observability Owner | Prometheus, Grafana, Loki, Alloy 수집 계약을 유지한다. | Platform Owner |
| Approved operator | Runbook에 따라 runtime 증적과 복구 결과를 기록한다. | Platform Owner |

### Control Register

| Control | Accountable role | Enforcement surface | Evidence |
| --- | --- | --- | --- |
| OBS-001 port naming | Platform Owner | Service and EndpointSlice manifests | protocol-prefixed port names |
| OBS-002 ArgoCD metrics | Observability Owner | NodePorts 30082-30086 | Prometheus target evidence |
| OBS-003 cluster metrics | Observability Owner | NodePorts 30090-30092 | expected services and targets |
| OBS-004 logs and rules | Observability Owner | Alloy deployment and Prometheus config | Ready streams and loaded rule groups |
| OBS-005 access | Platform Owner | Grafana role and AppProject destinations | Viewer-only API and monitoring destination |

### Service Port Naming

Service와 EndpointSlice 포트 이름은 `<protocol>[-suffix]` 형식이어야 한다.
현재 외부 계약은 Alloy `grpc-otlp`/`http-otlp`, Valkey `tcp-valkey`,
PostgreSQL `tcp-postgres-write`/`tcp-postgres-read`를 사용한다. suffix-only
이름이나 프로토콜이 없는 이름은 금지한다.

### Metrics NodePort Reservations

| Range | Reserved services | Owner |
| --- | --- | --- |
| 30082-30086 | ArgoCD application-controller, server, repo-server, ApplicationSet, notifications metrics | [RUN-0008](../runbooks/0008-argocd-metrics-prometheus-runbook.md) |
| 30090 | istiod metrics | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| 30091 | kube-state-metrics | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| 30092 | argo-rollouts metrics | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |

예약 번호를 다른 서비스에 재사용하거나 Prometheus 접근을 위해 과도한
kubeconfig 권한을 부여하지 않는다.

### Logs, Rules, and Access

- in-cluster `alloy-k8s-logs`는 `monitoring` namespace에서 Kubernetes API를
  통해 pod logs/events를 수집하고 `loki-external.platform.svc.cluster.local:3100`으로 전송한다.
- Alloy는 read-only root filesystem과 전용 storage path를 유지하며, k3d
  containerd 로그를 Docker socket 또는 host file mount로 수집하지 않는다.
- Prometheus `rule_files`는 필요한 고정 파일을 명시적으로 나열한다. glob이
  고정 파일의 존재를 암묵적으로 보장한다고 간주하지 않는다.
- Grafana 내부 health/settings API의 anonymous role은 Viewer로 제한한다.
  Editor/Admin anonymous access는 금지한다.
- `gitops/clusters/local/appproject-platform.yaml`은 `monitoring` destination을
  명시하며 wildcard destination으로 대체하지 않는다.

## Exceptions

NodePort 또는 AppProject live 변경은 Platform Owner가 승인한 bootstrap 또는
break-glass 상황에서만 허용한다. 변경 시 manifest, external scrape target,
관련 Runbook을 같은 변경으로 동기화하고 GitOps reconciliation 증적을 남긴다.

## Verification

| Control Area | Required Evidence | Runbook Owner |
| --- | --- | --- |
| Istio and Grafana connectivity | protocol port names, Viewer-only API health | [RUN-0007](../runbooks/0007-kiali-observability-connectivity-runbook.md) |
| ArgoCD metrics | reserved 30082-30086 services, `argocd-*` targets, metric presence | [RUN-0008](../runbooks/0008-argocd-metrics-prometheus-runbook.md) |
| Cluster metrics | reserved 30090-30092 services and expected targets | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| Alloy and Loki | deployment Ready and cluster-labelled streams received | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |
| Rules and AppProject | required rule groups load; monitoring destination present | [RUN-0009](../runbooks/0009-k8s-observability-runbook.md) |

## Review Cadence

Service/EndpointSlice port, NodePort reservation, scrape target, Alloy version,
rule file, Grafana role, Loki endpoint, AppProject destination 변경 시 검토한다.

## Traceability

- [Service Mesh and cert-manager Policy](./0003-service-mesh-cert-manager-policy.md)
- [Kiali Connectivity Runbook](../runbooks/0007-kiali-observability-connectivity-runbook.md)
- [ArgoCD Metrics Runbook](../runbooks/0008-argocd-metrics-prometheus-runbook.md)
- [K8s Observability Runbook](../runbooks/0009-k8s-observability-runbook.md)

### Lifecycle Traceability

| Promoted owner | Control owner | Enforcement surface |
| --- | --- | --- |
| N/A — current GitOps and external observability contracts have no reciprocal Spec or Task policy link | Platform Owner and Observability Owner | service naming, NodePort manifests, Alloy, Prometheus/Grafana/Loki config, AppProject destination, owning Runbooks |
