---
title: "OpenBao as the Runtime Secret Backend"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0041"
supersedes: "ADR-0003"
---

# ADR-0041: OpenBao as the Runtime Secret Backend

## Overview

This ADR moves the external backend for runtime secrets from HashiCorp Vault
to OpenBao. The pattern of delivering secrets through the External Secrets
Operator (ESO) and Kubernetes Auth carries over unchanged from ADR-0003; only
the backend product and its access address change. This decision supersedes
ADR-0003.

## Context

The external services workspace (`hy-home.docker`) retired its Vault
container and runs OpenBao. That workspace's current facts are:

- containers `openbao` and `openbao-agent`, image `openbao/openbao:2.6.2`
- the fixed address `172.18.0.17` on the k3d network `k3d-hyhome`, listener `8200`
  (HTTP, local-only)
- the external Traefik route `https://openbao.hy.home.arpa`

This repository still kept the removed Vault address (`172.18.0.8`) and host
as its desired state and bootstrap defaults, so ESO pointed at an endpoint that
no longer exists. OpenBao is compatible with the Vault HTTP API, KV v2, and the
Kubernetes auth method, so ESO's `vault` provider and the existing
ClusterSecretStore work unchanged.

## Decision

- The single source of runtime secrets is the external OpenBao. Plaintext
  secrets are kept out of Git, manifests, documents, and logs.
- Secrets sync through the ESO `vault` provider, and authentication keeps the
  Kubernetes Auth role `eso-read-platform` (audience `vault`). Policy applies
  least privilege per namespace/path.
- The cluster-internal access path is the `vault-external` Service and
  EndpointSlice in the `platform` namespace; the EndpointSlice address is
  `172.18.0.17` and the port is `8200`. The ESO egress NetworkPolicy is limited
  to the same `/32`.
- Host-side administration and bootstrap access use
  `https://openbao.hy.home.arpa` with a verified CA. The cluster-internal HTTP
  path remains the same local-only exception as before.
- The Kubernetes identifiers `vault-external` and `vault-backend`, the ESO
  `vault` provider, and the KV paths (`secret/platform/*`,
  `secret/apps/<app>/config`) do not change. These names refer to the API
  contract, not the product.

## Explicit Non-goals

- Renaming the Kubernetes Service, ClusterSecretStore, or NetworkPolicy
- OpenBao operations such as migrating secret values, unsealing, and setting
  up auth mounts and roles; the external workspace operator owns them
- Switching the cluster-internal OpenBao path to TLS
- Forcing apps to call the OpenBao SDK directly

## Consequences

- **Positive**:
  - The desired state, bootstrap, and static validation match the actual
    external runtime again.
  - The ESO, ClusterSecretStore, and ExternalSecret configuration and the KV
    path contract do not change, so the change is limited to the endpoint
    address and host.
- **Trade-offs**:
  - The `vault-*` Kubernetes names now differ from the product name, so
    documents must state how the two relate.
  - If an upstream change breaks OpenBao's Vault API compatibility, the ESO
    provider choice must be reconsidered.
- **Operational**:
  - The external operator keeps OpenBao's Kubernetes auth `kubernetes_host`,
    reviewer JWT/CA, and role settings aligned with this contract. The
    repository's static PASS does not prove this.

## Alternatives

### Rename the Kubernetes identifiers to `openbao-*` too

- Good:
  - Product and resource names match.
- Bad:
  - It needs a live cutover that changes the ClusterSecretStore, every
    ExternalSecret, the NetworkPolicy, and the validators together, and secret
    sync can break in between.

### Keep Vault

- Good:
  - No repository change.
- Bad:
  - The external workspace retired Vault, so it points at a backend that does
    not exist.

## Traceability

**Current-state clarification (2026-09-23).** The cluster-internal
`vault-external` HTTP path at `172.18.0.17:8200` is replaced under
[ADR-0046](./0046-external-services-over-host-addresses.md): ESO reaches `https://openbao.hy.home.arpa`
through the external Traefik and pins the mkcert root CA. OpenBao as the
secret backend and the ESO integration are unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)
- **Operations Policy**: [`../../05.operations/policies/0001-k8s-gitops-operations-policy.md`](../../05.operations/policies/0001-k8s-gitops-operations-policy.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| ADR-0003 | Supersedes ADR-0003; the ESO and Kubernetes Auth pattern carries over | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
