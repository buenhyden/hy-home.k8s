---
title: "Kiali Operator Installation"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-09-14"
layer: "architecture"
artifact_id: "ADR-0037"
---

# ADR-0037: Kiali Operator Installation

## Overview

This proposed decision records how Kiali is installed today so that the decision
log matches the GitOps implementation. It would replace the install-mode clauses
of ADR-0009 once accepted, and it keeps ADR-0009's external observability
boundary.

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
- Point Kiali at the external observability stack through `platform` service DNS
  names: `prometheus-external`, `grafana-external` and `tempo-external`. Keep the
  Grafana browser link on the external IP, because that link opens in the
  operator's browser, not inside the cluster.
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

**Current-state clarification (2026-09-23).** Kiali reaches Prometheus and
Grafana through the external Traefik by name (`https://prometheus.hy.home.arpa`
with Basic Auth, `https://grafana.hy.home.arpa`) under [ADR-0046](./0046-external-services-over-host-addresses.md);
`prometheus-external` and `grafana-external` are retired and only
`tempo-external` remains. The operator installation decision is unchanged.

Acceptance of this record should move ADR-0009 to `superseded` with reciprocal
links, in one reviewed change.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0009](0009-kiali-external-observability.md) | Proposed successor for ADR-0009's install-mode clauses; ADR-0009 stays accepted until this record is accepted | N/A — standalone decision record with no execution scope |
