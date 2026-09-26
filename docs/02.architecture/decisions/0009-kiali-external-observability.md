---
title: "Kiali with External Observability Stack"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0009"
---

# ADR-0009: Kiali with External Observability Stack

## Overview

This ADR records the decision to install Kiali from the `kiali-server` Helm chart and connect it to the external Docker-hosted observability stack (Prometheus/Grafana/Tempo).

## Context

Kiali is needed to visualize the Istio service mesh's traffic topology and metrics.
Prometheus, Grafana, and Tempo run as an external Docker-hosted observability stack and are connected through GitOps Service/EndpointSlice objects without a separate install inside K8s.
Docker Traefik proxies `kiali.hy-k8s.home.arpa` to the k3d ingress.

## Decision

- The Kiali `kiali-server` Helm chart (`https://kiali.org/helm-charts`) is installed in the `istio-system` namespace.
  - It runs as a single instance without a separate Kiali Operator.
- Kiali version: v2.6.x
- External observability integration:
  - Prometheus: `http://172.18.0.10:9090`
  - Grafana: `http://172.18.0.14:3000`
  - Tracing (Tempo): `http://172.18.0.12:3200`
- Ingress: `ingress-nginx`, hostname `kiali.hy-k8s.home.arpa`.
- TLS: issued by the cert-manager `ClusterIssuer` (mkcert CA).
- Authentication: anonymous (local environment only).
- External exposure: a Docker Traefik router `kiali-k3d` is added (managed in the separate Traefik repo).
- Kiali egress NetworkPolicy: allows only the Prometheus/Grafana/Tempo EndpointSlice addresses and the required Kubernetes/DNS/Istio control-plane egress.

## Explicit Non-goals

- An operator-based Kiali install
- Production-grade authentication hardening (this is local only)
- Installing Prometheus/Grafana inside K8s
- Jaeger integration (Tempo is used instead)

## Consequences

- **Positive**:
  - Service mesh traffic topology, metrics, and tracing are visible in one UI.
  - Reusing the existing external observability stack saves resources inside K8s.
  - cert-manager TLS automates HTTPS.
- **Trade-offs**:
  - The network path to the external Prometheus/Grafana/Tempo must be kept.
  - The Kiali egress NetworkPolicy must state the observability scope.
  - Istio must be installed first.

## Alternatives

### Kiali Operator

- Good: operational automation and better lifecycle management
- Bad: excessive complexity for a single local instance

### Install Prometheus inside K8s

- Good: the cluster is self-contained
- Bad: an external stack already runs, so resources would be duplicated

### Use Grafana alone

- Good: reuses the existing Grafana
- Bad: cannot visualize the Istio service mesh topology

## Traceability

**Current-state clarification (2026-09-23).** The `172.18.0.x`
container addresses above are replaced by host-published ports on
`192.168.0.13` under [ADR-0046](./0046-external-services-over-host-addresses.md), and the Grafana browser link is
`https://grafana.hy.home.arpa`. Kiali still calls the backends through the
`*-external` services; the rest of this decision is unchanged.

**Current-state clarification (2026-09-23).** The browser route this decision
assigns to the external Docker Traefik is retired. The host is served by the
dedicated k8s router under
[ADR-0043](./0043-dedicated-k8s-ingress-router.md); the rest of this decision
is unchanged.

**Current-state clarification (2026-09-14).** The install-mode clauses of this
decision no longer describe the implementation. Since commit `b54655ad`
(2026-03-30) `gitops/apps/root/platform-kiali-app.yaml` installs the
`kiali-operator` chart `2.10.0` with an operator-created Kiali CR
(`cr.create: true`), and Kiali reaches Prometheus, Grafana and Tempo through
`platform` service DNS names rather than the IP URLs listed above. The
external-observability boundary itself is unchanged.
[ADR-0037](0037-kiali-operator-installation.md) proposes the successor decision.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **ARD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
