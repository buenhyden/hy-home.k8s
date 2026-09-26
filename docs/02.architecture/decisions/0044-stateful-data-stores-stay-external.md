---
title: "Stateful Data Stores Stay Outside the Cluster"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-09-26"
layer: "architecture"
artifact_id: "ADR-0044"
---

# ADR-0044: Stateful Data Stores Stay Outside the Cluster

## Overview

This ADR records the review of whether to move the `postgresql-cluster` and
`valkey-cluster` of the external services workspace (`hy-home.docker`) into the
k3d cluster. Both clusters stay in the external workspace, and this repository
connects to them only through Service and EndpointSlice contracts, as before.

## Context

The state of the two workspaces as of 2026-09-23:

- `postgresql-cluster` consists of three Spilo (Patroni) nodes, three etcd
  nodes, and the HAProxy `pg-router`. It starts only with the opt-in profile
  `postgres-ha` and was stopped at the time of the decision. Only `pg-router`
  joins the k3d network, at `172.18.0.15`.
- The external workspace's apps (keycloak, dbt, mlflow) use the standalone
  `mng-pg`. The only consumers of `postgresql-cluster` are this repository's
  `postgres-app-secret` and the adminer workload.
- `valkey-cluster` runs in six-node cluster mode and joins only `lab_net`. It
  has no consumer in either workspace. The Valkey this repository's ArgoCD uses
  (`172.18.0.9`) is the standalone `mng-valkey`.
- Both clusters store their data in host bind directories. This repository has
  no PVC, StorageClass, or k3d host volume mapping. The k3d default local-path
  volumes live inside the node containers and vanish when the cluster is
  recreated.

## Decision

- `postgresql-cluster`, `valkey-cluster`, `mng-pg`, and `mng-valkey` stay in
  the external workspace. This repository does not own their runtime.
- The PostgreSQL contract is `pg-router` (`172.18.0.15:15432/15433`); for it to
  work, the external workspace's profile `postgres-ha` must be running.
- The Valkey contract is `mng-valkey` (`172.18.0.9:6379`). `valkey-cluster` is
  not a contract of this repository.

## Explicit Non-goals

- Changing the external workspace's cluster configuration, backups, or profiles
- Introducing a PostgreSQL operator, StorageClass, or backup system in this repository
- Deciding whether to keep or retire `valkey-cluster`; the external workspace owns that

## Consequences

- **Positive**:
  - Data lifetime is decoupled from recreating the k3d cluster.
  - This repository takes on no stateful operator or backups.
- **Trade-offs**:
  - The PostgreSQL contract depends on the external workspace's opt-in
    profile; if that profile is off, the live connection fails despite a
    static PASS.
- **Operational**:
  - Before bootstrap and live validation, the operator confirms that
    `pg-router` and `mng-valkey` are running.

## Alternatives

### Move both clusters into k8s

- Good:
  - The IP-based cross-repository contract disappears, and the lifecycle is
    managed through GitOps.
- Bad:
  - k3d nodes are containers on the same host, so the triple redundancy of
    Patroni and etcd brings no availability benefit.
  - Persistent storage, an operator, and backups would have to be introduced,
    with a risk of losing data when the cluster is recreated.
  - `valkey-cluster` has no consumer.

### Change the PostgreSQL contract to `mng-pg`

- Good:
  - Uses a database that is always running.
- Bad:
  - Mixes the external workspace's operations database and k8s app data in one
    instance.

## Traceability

**Current-state clarification (2026-09-23).** The endpoints
above move from container addresses to host-published ports on
`192.168.0.13` under [ADR-0046](./0046-external-services-over-host-addresses.md): `mng-valkey` at `26379`
and `pg-router` at `15432/15433`. The bootstrap no longer requires
`pg-router`. The placement decision is unchanged.

- **PRD**: [`../../01.requirements/0004-current-local-gitops-platform.md`](../../01.requirements/0004-current-local-gitops-platform.md)
- **AD**: [`../descriptions/0007-current-local-gitops-platform.md`](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: [`../../03.specs/0008-current-local-gitops-platform/spec.md`](../../03.specs/0008-current-local-gitops-platform/spec.md)
- **Related ADR**: [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0014](./0014-current-local-gitops-platform-contract.md) | Confirms ADR-0014's external service contract for PostgreSQL and Valkey; replaces nothing | [SPEC-0008](../../03.specs/0008-current-local-gitops-platform/spec.md) |
