---
title: "Istio Default Profile with ingress-nginx Coexistence"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0008"
---

# ADR-0008: Istio Default Profile with ingress-nginx Coexistence

## Overview

This ADR settles on installing Istio through Helm with the `default` profile, coexisting with the existing ingress-nginx.

## Context

A service mesh (mTLS, traffic management, observability) is needed, and the existing ingress-nginx-based external exposure must stay.
The WSL2 local environment has a limited resource budget, so install complexity must be minimal.
The Istio IngressGateway must coexist with ingress-nginx without port conflicts.

## Decision

- Istio is installed from the `istio-base` + `istiod` Helm charts (`https://istio-release.storage.googleapis.com/charts`).
- Profile: `default` (no ambient mesh; the sidecar model).
- `istiod` resource limits apply (WSL2 resource budget):
  - `pilot.resources.requests.cpu: 100m`
  - `pilot.resources.requests.memory: 128Mi`
- **The Istio IngressGateway is disabled** (`gateways.istio-ingressgateway.enabled: false`).
  - ingress-nginx handles external exposure; the Istio Gateway CR is not used.
- Sidecar injection is **namespace opt-in**: it applies only to namespaces labeled `istio-injection=enabled`.
- Namespaces without default sidecar injection: `argocd`, `cert-manager`, `headlamp`, `ingress-nginx`, `external-secrets`, `platform`.
- Istio version: v1.25.x

## Explicit Non-goals

- Using the Istio IngressGateway in place of ingress-nginx
- Adopting ambient mesh
- An istioctl-based install (not possible through GitOps)
- Multi-cluster Istio federation

## Consequences

- **Positive**:
  - Service mesh capabilities (mTLS, traffic policy) are gained.
  - The Istio lifecycle is managed through GitOps.
  - The ingress-nginx-based external exposure does not change.
  - Sidecar opt-in leaves system namespaces unaffected.
- **Trade-offs**:
  - Registering the Istio CRDs requires updating the AppProject clusterResourceWhitelist.
  - Pods with an injected sidecar run more containers and use more resources.
  - Istio must be installed before Kiali.

## Alternatives

### Enable the Istio IngressGateway

- Good: full use of Istio features
- Bad: port conflicts with ingress-nginx and contention for k3d LoadBalancer ports

### Linkerd

- Good: lighter than Istio and simpler to install
- Bad: rejected because the user requirement is Istio/Kiali

### istioctl install

- Good: convenient profile-based install
- Bad: cannot be managed declaratively through GitOps

## Traceability

**Current-state clarification (2026-09-14).** Two parts of the Decision no
longer match the tree. `ingress-nginx` is injected, not excluded:
`gitops/platform/namespaces/namespace-ingress-nginx.yaml` carries
`istio-injection: enabled`, and ADR-0028 relies on that. The install set also
includes the Istio CNI node agent (`gitops/apps/root/platform-istio-cni-app.yaml`,
sync wave 1 beside `istio-base`, with `pilot.cni.enabled: true` on istiod). The
IngressGateway stays disabled because no gateway is declared; the
`gateways.istio-ingressgateway.enabled: false` value is not set explicitly in the
Application values.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **ARD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md)
