---
title: "Kiali Operator Installation"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-10-03"
layer: "architecture"
artifact_id: "ADR-0037"
---

# ADR-0037: Kiali Operator Installation

## Overview

This decision accepts the Kiali Operator installation already declared in GitOps.
It replaces only ADR-0009's `kiali-server` installation, fixed Kiali version and
operator non-goal clauses. ADR-0009 remains accepted for its external backend,
local authentication, certificate and network isolation boundaries; ADR-0043 and
ADR-0046 own the later router and endpoint changes.

## Context

ADR-0009 chose the `kiali-server` Helm chart, pinned Kiali 2.6.x, and listed the
Kiali Operator as a non-goal. Commit `b54655ad` (2026-03-30) migrated the
installation to the operator. The repository has declared that install since,
so ADR-0009's install-mode clauses describe a state the tree no longer has.

## Decision

- Install Kiali through the `kiali-operator` Helm chart declared by
  `gitops/apps/root/platform-kiali-app.yaml`. The Application owns the chart
  version (currently `2.10.0`).
- Let the operator create the Kiali custom resource (`cr.create: true`) in
  `istio-system`, with anonymous authentication for the local-only platform.
- Keep the external observability paths selected by ADR-0046: Prometheus at
  `https://prometheus.hy.home.arpa` with Basic Auth and Grafana at
  `https://grafana.hy.home.arpa` with a Viewer service account token. Both clients
  verify the gateway CA supplied by bootstrap; ESO supplies credentials from
  OpenBao references. The Grafana browser link uses the same HTTPS name.
  Tempo remains `http://tempo-external.platform.svc.cluster.local:3200`.
- Keep ADR-0009's ingress host, cert-manager TLS and egress NetworkPolicy
  boundary unchanged.

## Explicit Non-goals

- Changing the external observability stack or its addresses.
- Production-grade authentication.
- Installing Prometheus, Grafana or Tempo inside the cluster.

## Consequences

- **Positive**: the decision log matches the reconciled desired state, and the
  operator owns the Kiali resource lifecycle.
- **Trade-offs**: the operator adds a controller and a CRD to a local
  single-instance install, which is the complexity ADR-0009 had avoided.
- **Operational**: an operator chart upgrade can change the Kiali resource
  schema, so upgrades are reviewed as chart changes.

## Alternatives

### Return to the `kiali-server` chart

- Good: fewer moving parts for one local instance.
- Bad: reverses a migration that has been in force since 2026-03-30, with no
  current requirement driving it.

### Leave ADR-0009 unchanged

- Good: no decision-log change.
- Bad: an accepted decision would keep contradicting the implementation it
  governs.

## Traceability

The request owner authorized reviewing SPEC-0008 against implementation and
selecting the standards-aligned contract on 2026-10-03. This accepts the bounded
installation amendment with its documented controller/CRD trade-off. It does not
supersede ADR-0009 as a whole or claim a new deployment or live verification.
The endpoint and browser-route decisions remain with
[ADR-0046](./0046-external-services-over-host-addresses.md) and
[ADR-0043](./0043-dedicated-k8s-ingress-router.md).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0009](0009-kiali-external-observability.md) | Replaces only the install-mode/version clauses and operator non-goal; ADR-0009 stays accepted for its remaining boundaries, with no whole-document supersession | [SPEC-0008](../../98.archive/completed/03.specs/0008-current-local-gitops-platform/spec.md) |

- **Requirement**: [REQ-0004-FR-0004 and REQ-0004-NFR-0001](../../01.requirements/0004-current-local-gitops-platform.md)
- **Current architecture**: [AD-0007](../descriptions/0007-current-local-gitops-platform.md)
- **Implementation source**: [Kiali Application](../../../gitops/apps/root/platform-kiali-app.yaml)
