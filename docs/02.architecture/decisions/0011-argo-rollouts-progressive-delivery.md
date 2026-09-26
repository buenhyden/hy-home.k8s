---
title: "Argo Rollouts for Progressive Delivery"
version: "1.0.2"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0011"
---

# ADR-0011: Argo Rollouts for Progressive Delivery

## Overview

Argo Rollouts is introduced to the platform to support canary/blue-green delivery strategies.
The Rollouts Dashboard UI is installed alongside it to provide visual rollout state management.

## Context

With only ArgoCD's default Deployment-based delivery, the platform cannot express progressive delivery safety well enough.
Progressive delivery (canary, blue-green), Prometheus metric-based AnalysisRuns, and an automatic abort/rollback boundary on failure are needed.
Argo Rollouts comes from the same ecosystem as ArgoCD (argoproj) and integrates with it natively.

## Decision

- Argo Rollouts v1.9.0 (chart 2.40.9) is installed in the `argo-rollouts` namespace.
- Chart: `argoproj.github.io/argo-helm`, chart name: `argo-rollouts`
- The Rollouts Dashboard is enabled with it and exposed at `rollouts.hy-k8s.home.arpa`.
- Controller metrics are enabled (collected by the external Prometheus at `172.18.0.10`).
- The default promotion policy does not force automatic promotion. A per-app Rollout may use an approved Prometheus AnalysisTemplate.
- The Prometheus analysis provider uses the external Prometheus endpoint.

### Decision status

Accepted — 2026-03-30

## Explicit Non-goals

- Forcing automatic promotion (manual promotion is the default)
- Multi-cluster Rollouts
- Standardizing custom Analysis metrics platform-wide

## Consequences

- The `argo-rollouts` namespace is added
- The `argoproj.github.io/argo-helm` repo and the `argo-rollouts` namespace are added to the AppProject
- AppProject `platform` allows the Rollouts chart repo and the `argo-rollouts` namespace, and the AppProject `apps` namespaceResourceWhitelist allows `Rollout` and `AnalysisTemplate` for workload consumption
- The external Traefik artifact `rollouts-k3d.yaml` is required
- App teams must convert `Deployment` manifests to `Rollout` (in the apps namespaces)

## Alternatives

| Option | Assessment |
| ------------- | ------------------------------------------------------------ |
| Argo Rollouts | Native ArgoCD integration, Prometheus analysis, Rollouts Dashboard UI |
| Flagger | Flagger depends heavily on the Istio/Nginx controllers, which adds complexity |
| Manual deployment | Safe but not automated |

## Traceability

**Current-state clarification (2026-09-23).** The external
Prometheus is reached through the host address `192.168.0.13` under
[ADR-0046](./0046-external-services-over-host-addresses.md), not `172.18.0.10`. The rest of this decision is
unchanged.

**Current-state clarification (2026-09-23).** The browser route this decision
assigns to the external Docker Traefik is retired. The host is served by the
dedicated k8s router under
[ADR-0043](./0043-dedicated-k8s-ingress-router.md); the rest of this decision
is unchanged.

- [ADR-0002](./0002-argocd-helm-and-gitops-model.md) — ArgoCD GitOps model
- [ADR-0012](./0012-argo-notifications-slack.md) — Rollouts event notifications
- [PRD](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)
- [ARD](../descriptions/0004-argo-rollouts-progressive-delivery.md)
- [Spec](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md)
- [Plan](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md)
- [Task](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/plan.md)
