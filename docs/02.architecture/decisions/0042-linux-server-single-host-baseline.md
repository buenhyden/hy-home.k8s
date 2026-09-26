---
title: "Linux Server Single-Host Baseline"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0042"
---

# ADR-0042: Linux Server Single-Host Baseline

## Overview

This ADR records the local GitOps platform's host as a Linux server, not WSL2.
This decision takes over only the host clause "WSL2 + WSL-native Docker" of
[ADR-0014](./0014-current-local-gitops-platform-contract.md); the other clauses,
including k3d, ArgoCD App-of-Apps, and the external service contract, stay in
ADR-0014 unchanged.

## Context

The platform runs on a single Linux server, not on WSL2 over Windows. The
host is Ubuntu 24.04 LTS, runs Docker Engine as a native daemon, and its Docker
context is `default`. The k3d cluster `k3d-hyhome` and the containers of the
external services workspace (`hy-home.docker`) share the host's Docker network
`k3d-hyhome`.

Yet ADR-0014, the Architecture Description, the Stage 05 documents, the
infrastructure README, and the static validators still assume a WSL2 shell,
WSL-native Docker, and a Windows portproxy. That assumption misdirects the
runtime prerequisites an operator must confirm and turns a nonexistent Windows
boundary into a failure boundary.

## Decision

- The platform host is a single Linux server. Docker is the host's native
  Docker Engine, and the Docker context is confirmed on the host.
- Local UI and external service host names use the `hy.home.arpa` domain. The
  operator owns the DNS, host firewall, and external Traefik gateway that
  resolve these names; they are outside repository static validation.
- The k3d cluster shape, the `k3d-hyhome` network and context, the
  ingress-nginx LoadBalancer `172.18.0.240`, and the external service
  EndpointSlice contract do not change.
- A constraint an earlier decision wrote as the "WSL2 resource budget" reads
  as the single-host resource budget. This decision changes neither the size
  of the constraint nor any resource request/limit value.
- The infrastructure runtime prerequisite table and its static validation are
  based on the Linux server host, not WSL2.

## Explicit Non-goals

- Extending to multiple hosts or a remote cluster
- Owning the `hy.home.arpa` DNS server, the host firewall, or the TLS
  certificate issuance procedure
- Changing the k3d cluster settings, node count, or resource requests/limits
- Editing archive records or accepted ADR bodies written under the WSL2
  assumption at the time of their decision

## Consequences

- **Positive**:
  - The runtime prerequisites and failure boundaries match the actual host.
  - Nonexistent boundaries such as the Windows portproxy and the WSL gateway
    disappear from the operations documents.
- **Trade-offs**:
  - Accepted ADR bodies written under the WSL2 assumption stay as they are,
    so readers must read this decision alongside them.
- **Operational**:
  - The operator maintains `*.hy.home.arpa` resolution in host DNS, and a
    repository static PASS does not prove it.

## Alternatives

### Supersede all of ADR-0014

- Good:
  - The current platform contract gathers in one document.
- Bad:
  - Changing one host clause would mean rewriting every unchanged clause as a
    new decision and moving every document that cites ADR-0014.

### Edit the ADR-0014 body directly

- Good:
  - The smallest diff.
- Bad:
  - Changing an accepted decision's body erases the record of the decision as
    it was made.

## Traceability

**Current-state clarification (2026-09-23).** The host names k8s serves are
`hy-k8s.home.arpa`, not `hy.home.arpa`, and use a dedicated entry point
([ADR-0043](./0043-dedicated-k8s-ingress-router.md)). `hy.home.arpa` remains
only for the external services workspace's host names. The rest of the host
clause is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
- **Infrastructure**: [`../../../infrastructure/README.md`](../../../infrastructure/README.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0014](./0014-current-local-gitops-platform-contract.md) | Carries ADR-0014's host clause only; ADR-0014 stays accepted for every other clause | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
