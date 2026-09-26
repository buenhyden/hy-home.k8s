---
title: "In-Cluster Telemetry Collection with an External Backend"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0045"
---

# ADR-0045: In-Cluster Telemetry Collection with an External Backend

## Overview

This ADR records the review of where k8s observability belongs. Storage and
querying (Prometheus, Loki, Tempo, Grafana, Alertmanager) stay in the external
services workspace (`hy-home.docker`). Collecting k8s telemetry is the job of
Alloy inside this repository's cluster, which pushes to the external backend.

## Context

The state as of 2026-09-23:

- The external workspace's observability stack is running. Docker services'
  metrics, logs, and traces are already viewed in one Grafana, and Prometheus
  starts with `--web.enable-remote-write-receiver`.
- For k8s metrics, the external Prometheus scrapes the NodePorts
  `172.18.0.2:30082-30092` as static targets. But the external workspace's
  Traefik holds `172.18.0.2` on the `k3d-hyhome` network, so this target points
  at Traefik, not a k3d node.
- The sidecars' `istio_requests_total` (port `15090`) and the kubelet and
  cAdvisor metrics are not collected, so Kiali's traffic graph, which uses the
  external Prometheus, has no data.
- This repository's Alloy (`gitops/platform/monitoring/alloy-k8s-logs.yaml`)
  pushes pod logs and events to the external Loki and already has read access
  that includes `nodes/proxy`.
- This repository has no persistent storage
  ([ADR-0044](./0044-stateful-data-stores-stay-external.md)).

## Decision

- Prometheus, Loki, Tempo, Grafana, and Alertmanager stay in the external
  workspace. No second storage backend or Grafana runs inside k8s.
- Alloy inside the cluster owns collecting k8s telemetry. Through Kubernetes
  service discovery, Alloy scrapes:
  - pod annotations and the Istio sidecar `15090`
  - kube-state-metrics
  - kubelet and cAdvisor (`nodes/proxy`)
  - istiod, ArgoCD, and Argo Rollouts
- Alloy pushes the collected metrics to the remote write endpoint of
  `prometheus-external`, adding the label `cluster="k3d-hyhome"` to every series.
- The external Prometheus's k3d static scrape job and this repository's metrics
  NodePort Services (`30082-30092`) are retired once the new path is validated.
- Traces follow later, on a path where Istio sends them to the OTLP endpoint of
  `alloy-external`. This decision settles only metric and log collection.

## Explicit Non-goals

- Changing the external observability stack's configuration, retention, or alert rules
- Introducing kube-prometheus-stack, the Prometheus Operator, or an in-cluster Grafana
- Deleting the external Prometheus's static jobs; the external workspace owns that

## Consequences

- **Positive**:
  - Nothing depends on k3d node addresses or NodePorts, so the `172.18.0.2`
    conflict disappears.
  - Pod and sidecar metrics are collected, so the Kiali graph and Rollouts
    analysis use real data.
  - Observability data lifetime is decoupled from recreating the k3d cluster,
    and there is still one place to query.
- **Trade-offs**:
  - It depends on the external Prometheus accepting remote write and on
    egress to `prometheus-external`.
  - The Alloy configuration carries both log and metric collection, so the
    configuration file grows.
- **Operational**:
  - The external workspace retires the k3d static scrape job and keeps
    accepting remote write.

## Alternatives

### Move all observability into k8s (kube-prometheus-stack)

- Good:
  - Uses standard Kubernetes tooling and ServiceMonitors.
- Bad:
  - Storage backends and Grafana are duplicated, splitting where to query.
  - Without persistent storage, history is lost when the cluster is recreated.
  - It takes a large share of the single-host resource budget.

### Keep the external Prometheus scraping directly

- Good:
  - Few changes to this repository.
- Bad:
  - Service discovery by pod IP from the docker network needs extra cluster
    credentials and routing, and the static NodePort approach is already broken
    by the address conflict.

## Traceability

**Current-state clarification (2026-09-23).** Alloy remote-writes to
`https://prometheus.hy.home.arpa/api/v1/write` through the external Traefik with
Basic Auth instead of the retired `prometheus-external` Service, under
[ADR-0046](./0046-external-services-over-host-addresses.md). The rest of this decision is unchanged.

**Current-state clarification (2026-09-23).** The metrics NodePort
Services (`30082-30092`) are retired before live remote write evidence, because
the external workspace removed their static scrape jobs
(`hy-home.docker` PR #218) and no consumer remained. Remote write now reaches the host address under
[ADR-0046](./0046-external-services-over-host-addresses.md). The rest of this
decision is unchanged.

**Current-state clarification (2026-09-24).** The follow-up trace path is now
in place. Istio sidecars send traces over OTLP to `alloy-external`
(`192.168.0.13:4317`) through the mesh-wide `defaultProviders.tracing` setting
in the istiod `meshConfig`, at 10% sampling, and the `apps` egress policy
allows that port. The external Alloy's home configuration receives OTLP and
forwards it to Tempo (`hy-home.docker`). The rest of this decision is
unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0009](./0009-kiali-external-observability.md) | Keeps ADR-0009's external observability backend; moves k8s metric collection into the cluster | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
