---
title: "External Services Reached Through Host-Published Addresses"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0046"
---

# ADR-0046: External Services Reached Through Host-Published Addresses

## Overview

This ADR changes the path by which the cluster reaches the services of the
external services workspace (`hy-home.docker`). The decisions to use external
backends ([ADR-0041](./0041-openbao-secret-backend.md),
[ADR-0044](./0044-stateful-data-stores-stay-external.md),
[ADR-0045](./0045-in-cluster-telemetry-collection.md)) stay as they are; the
cluster uses host-published addresses and ports instead of container addresses
on the shared docker network `k3d-hyhome`.

## Context

The state as of 2026-09-23:

- At its owner's direction, the external workspace detached every Compose
  service from `k3d-hyhome` (`hy-home.docker` commit `f6d481e74`, PR #218). The
  fixed addresses, the Traefik k3d routes, the Prometheus NodePort job, and the
  k8s dashboards and alert rules are gone. Containers already running keep
  their old addresses until they are recreated.
- Every external service contract in this repository used a `172.18.0.x`
  container address. When the containers are recreated, ESO, the ArgoCD
  Valkey, log collection, and Kiali all break together.
- The host's primary address is `192.168.0.13`, and the external Traefik binds
  `80/443` on it. The ports reachable at that address from `k3d-hyhome` are:
  - open: `443` (Traefik), `3100` (Loki), `3200` (Tempo), `26379` (`mng-valkey`),
    `25432` (`mng-pg`), `6550` (k3d API)
  - closed: `9090` (Prometheus, not published on the host), `3000` (Grafana, not
    published on the host), `4317` (Alloy OTLP, published but refusing
    connections), `15432/15433` (`pg-router`, profile `postgres-ha` stopped)
- Traefik's Prometheus route sits behind an SSO middleware, so machine clients
  cannot use it. The OpenBao and Grafana routes have no SSO.
- The k3d API certificate's SAN lacks `192.168.0.13`. Once OpenBao leaves
  `k3d-hyhome`, it cannot reach the API by the name `k3d-hyhome-server-0`.

## Decision

- The cluster reaches external services at the host address `192.168.0.13`
  and host-published ports. The `*-external` Service names in the `platform`
  namespace stay; only the EndpointSlice addresses and ports change. When a
  Service port differs from the host port, the Service `targetPort` points at
  the host port.
  - Valkey (`mng-valkey`): `192.168.0.13:26379`
  - PostgreSQL (`pg-router`): `192.168.0.13:15432` (write), `15433` (read)
  - Loki `3100`, Tempo `3200`, Alloy OTLP `4317/4318`
  - Prometheus `9090`, Grafana `3000`: these work only once the external
    workspace publishes them on the host
- ESO reaches OpenBao at `https://openbao.hy.home.arpa` (the external Traefik)
  and verifies the certificate with the mkcert root CA. Inside the cluster, a
  CoreDNS custom zone resolves that name to `192.168.0.13`. The `vault-external`
  Service and EndpointSlice, and the cluster-internal HTTP local-only exception,
  are retired.
- The k3d API binds only `192.168.0.13:6550` and puts that address in its
  certificate SAN. The OpenBao Kubernetes auth `kubernetes_host` is
  `https://192.168.0.13:6550`.
- NetworkPolicy egress allows only `192.168.0.13/32` and the ports needed.
- PostgreSQL is not a required bootstrap dependency. `postgresql-cluster` is
  the service database and its profile may be off, so bootstrap only warns.
  `mng-pg` is the external workspace's administration database and not a
  contract of this repository.

## Explicit Non-goals

- Changing the external workspace's port publishing, bind addresses, or
  Traefik routes; publishing Prometheus and Grafana on the host is a request to
  the external workspace
- Fixing the cause of the Alloy OTLP `4317` connection refusal
- Moving the external backends into the cluster

## Consequences

- **Positive**:
  - The two workspaces no longer share a docker network or container
    addresses, so recreating a container does not break a cluster contract.
  - The cluster-internal HTTP exception between ESO and OpenBao disappears,
    and TLS is verified.
- **Trade-offs**:
  - The contract depends on the external workspace publishing host ports. If
    a port is narrowed to loopback, the cluster cannot reach it.
  - Bootstrap must manage the CoreDNS custom zone and the root CA ConfigMap.
  - Changing the k3d API bind requires recreating the cluster.
- **Operational**:
  - The operator changes the OpenBao `kubernetes_host` to the new address.
  - Until Prometheus and Grafana are published on the host, remote write and
    Kiali's metric queries do not work.

## Alternatives

### Make the cluster self-sufficient

- Good:
  - Changes in the external workspace have no effect.
- Bad:
  - It reverses ADR-0041, ADR-0044, and ADR-0045, and the cluster would have
    to own new storage and secret backends.

### Restore the external workspace's `k3d-hyhome` attachment

- Good:
  - No change to this repository.
- Bad:
  - It conflicts with the external workspace owner's decision.

## Traceability

**Current-state clarification (2026-09-23).** The external workspace chose
not to publish Prometheus `9090` or Grafana `3000` on the host. Prometheus
exposes only its HTTP API through the external Traefik at
`https://prometheus.hy.home.arpa/api/v1/`, with Basic Auth
(`hy-home.docker` PR #222). Grafana is reached at `https://grafana.hy.home.arpa`. So the
`prometheus-external` and `grafana-external` Services are retired, and Alloy,
Kiali and the Rollouts controller call those names directly:

- The CoreDNS custom zone resolves the names to the host address.
- The Basic Auth credentials come from OpenBao `platform/prometheus-api`
  through ESO.
- Grafana allows no anonymous API access, so Kiali sends a Viewer service
  account token from OpenBao `platform/grafana-api` through ESO.
- The gateway CA comes from bootstrap-created ConfigMaps (`hy-home-root-ca`,
  `kiali-cabundle`).
- Egress uses `192.168.0.13:443`.

Every other clause of this decision is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0041](./0041-openbao-secret-backend.md) | Keeps OpenBao as the secret backend; replaces the cluster-internal `vault-external` HTTP path with HTTPS through the external Traefik | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [ADR-0044](./0044-stateful-data-stores-stay-external.md) | Keeps PostgreSQL and Valkey external; moves their endpoints from container addresses to host-published ports | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
| [ADR-0045](./0045-in-cluster-telemetry-collection.md) | Keeps in-cluster collection with an external backend; moves the backend endpoints to host-published ports | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
