---
title: "External Data Service Contract Alignment"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-10-09"
layer: "architecture"
artifact_id: "ADR-0049"
---

# ADR-0049: External Data Service Contract Alignment

## Overview

The request owner chose to retire this Kubernetes repository's former HA
PostgreSQL route, keep Valkey-cluster consumption outside its current scope,
and align its data-service
interface with the tracked `hy-home.docker` management and development
services. This proposed record identifies the narrow replacement clauses of
[ADR-0044](./0044-stateful-data-stores-stay-external.md) and
[ADR-0046](./0046-external-services-over-host-addresses.md). Their external
runtime ownership and host-transport decisions remain accepted for the
unaffected services. The proposed state is initial authoring, not an accepted
decision or observed cluster reconciliation.

## Context

At the reviewed local source, Kubernetes required `mng-valkey` for Argo CD
at host `192.168.0.13:26379`, but also declared optional PostgreSQL
`postgres-write-external:15432` and `postgres-read-external:15433` through
`postgres-ha`/`pg-router`. Adminer set that old write route as its default
database server, while its actual UI could return HTTP 200 without a working
database connection. The earlier read-only sample found both HA host ports
refused and did not show `pg-router` in selected Docker metadata. That sample
does not test the independent management or development PostgreSQL.

The tracked external Compose contracts at
`77a80bc1478c3dfb46cfe8b8de97aa971817c494` distinguish four services:

| Role | External source and default publication | Current Kubernetes consumer |
| --- | --- | --- |
| Management Valkey | `hy-home.docker/infra/04-data/mng-db/docker-compose.yml`: `mng-valkey` container `6379` published at `192.168.0.13:26379` | Argo CD through `platform/valkey-external:6379` and its EndpointSlice |
| Development Valkey | `hy-home.docker/infra/04-data/dev-db/docker-compose.yml`: `dev-valkey` exposes `6379` only on `dev_data_net`; no host port | None |
| Management PostgreSQL | management Compose: `mng-pg` container `5432` published at `127.0.0.1:25432` | None |
| Development PostgreSQL | development Compose: `dev-pg` container `5432` published at `127.0.0.1:25433` | None |

The external workspace's separate LAB PostgreSQL loopback ports
`127.0.0.1:35432/35433` map to LAB container `15432/15433`; LAB Valkey ports
`127.0.0.1:17379–17384` are also separate. Neither LAB role is a current
Kubernetes consumer or a replacement for the removed HA routes. This decision
does not delete or reconfigure foreign LAB services.

[REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)
requires reproducible desired state (FR-0001), explicit external data
interfaces (FR-0003), currently supported UI claims (FR-0004), validation
depth and truthful live evidence (FR-0008), fail-closed source references
(FR-0010), and no secret values in Git or logs (NFR-0002). The existing
observation and local change are owned by
[SPEC-0106](../../03.specs/0106-stage99-lifecycle-normalization/spec.md),
WORK-019 and its Task. External Docker runtime and credentials remain outside
this repository.

## Decision

1. Keep the data services outside k3d. Argo CD retains one required
   management Valkey interface: `valkey-external.platform.svc.cluster.local`
   service port `6379` targets host `192.168.0.13:26379`. Its approved
   OpenBao/ESO secret flow remains unchanged. Do not replace it with
   development Valkey or LAB Valkey cluster ports.
2. Remove `postgres-write-external` and `postgres-read-external` from current
   K8s desired state and direct network-policy, bootstrap, verifier, test,
   operating and workload consumers. The former `postgres-ha`/`pg-router`
   `15432/15433` pair is retired from this repository's current local
   contract. Valkey cluster already had no current K8s consumer and remains
   excluded. Preserve earlier source and live
   observations as dated evidence; do not treat their refusal as failure of
   `mng-pg` or `dev-pg`.
3. Treat `mng-pg` and `dev-pg` as optional external host-loopback services,
   not Kubernetes endpoints. Their default `127.0.0.1:25432/25433` publishes
   permit a bounded host-side TCP observation; they do not imply LAN, k3d,
   authenticated SQL or application reachability. Development Valkey remains
   Docker-network-only. No Docker bind address, environment or credential is
   changed by this decision.
4. Remove Adminer's obsolete HA default database server without silently
   substituting either PostgreSQL instance. The current UI may be healthy
   without a supported DB login. If an app later requires PostgreSQL from
   Kubernetes, propose and review its purpose, endpoint transport, network
   policy, authentication/Secret flow, TLS and operator evidence before
   adding a K8s route. A localhost publish alone is insufficient.
5. Static source/consumer checks can establish this repository's local
   contract after review. Argo CD's automatic reconciliation and prune can
   remove old live resources after authorized publication to remote `main`
   and reconciliation; a local merge or source edit does not establish that
   outcome. The operator owns target/revision, deployment
   authorization, actual reconciliation observation and rollback evidence.

## Explicit Non-goals

- Moving PostgreSQL or Valkey into k3d, creating a new PG LAN proxy, or
  binding the existing PostgreSQL instances on the LAN.
- Deleting external LAB PostgreSQL or LAB Valkey services, changing their
  profiles, data, backups, secrets or host ports.
- Granting remote merge, live cluster mutation, release publication or
  secret-value access through this ADR.
- Claiming Adminer database login, authenticated SQL, post-change Argo CD
  reconciliation or service availability from a manifest or old UI response.

## Consequences

- **Positive:** The repository's K8s data contract names its actual required
  `mng-valkey` consumer and stops advertising the former HA PostgreSQL route and
  Valkey-cluster routes. Management/development Docker roles remain distinct.
- **Trade-off:** Adminer loses its obsolete default DB target. A supported
  Kubernetes-to-PostgreSQL path requires a future reviewed interface and
  likely additional policy, secret and transport work. Host-loopback checks
  cannot substitute for that path.
- **Operational:** Authorized publication to remote `main` can trigger
  automatic Argo CD prune/reconciliation. Operators must assess that effect
  before publication and
  confirm old-resource removal and current Valkey health afterward. Until
  then the local static result and live outcome are separate.

## Alternatives

- **Keep the opt-in HA PostgreSQL route.** This preserves the old Adminer
  default and desired EndpointSlices, but the old K8s LAN `15432/15433`
  interface does not match the tracked current LAB loopback
  `35432/35433` publication. No current K8s database need justifies
  maintaining that route and its manifests, policies and checks. The earlier
  port refusal does not establish the LAB runtime's current state. Rejected
  by the user's retirement choice.
- **Redirect Adminer/K8s to management or development PostgreSQL.** This may
  avoid a separate HA cluster, but the existing host-loopback binds cannot be
  reached by the declared K8s LAN interface. Widening exposure also requires
  a security, credential and workload-isolation design. Deferred until an
  actual application need and separate approval.
- **Move data stores into k3d.** This changes persistence, backup and runtime
  ownership, and is unnecessary for the current single-host interface.
  Rejected for this scope.

## Traceability

The amendment applies only to the data-service consumer/transport clauses.
ADR-0044's external placement, separation from cluster persistence and
external backup ownership remain. ADR-0046's host-address transport for
OpenBao, telemetry and management Valkey, and its API/CA/router decisions
remain. Their original dated context and bytes stay as historical decisions;
neither whole document is superseded or archived by this proposed ADR.

- **Requirement:** [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md),
  FR-0001/0003/0004/0008/0010 and NFR-0002.
- **Architecture:** [AD-0007](../descriptions/0007-current-local-gitops-platform.md).
- **Specification and execution:** [SPEC-0106](../../03.specs/0106-stage99-lifecycle-normalization/spec.md),
  [Plan WORK-019](../../03.specs/0106-stage99-lifecycle-normalization/plan.md#work-breakdown),
  [Task0019](../../03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0019-live-quality-observation.md).
- **Operations:** [POL-0001](../../05.operations/policies/0001-k8s-gitops-operations-policy.md),
  [POL-0007](../../05.operations/policies/0007-app-gitops-onboarding-policy.md),
  [RUN-0001](../../05.operations/runbooks/0001-argocd-platform-bootstrap-runbook.md).

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0044](./0044-stateful-data-stores-stay-external.md) | Replaces only its `pg-router` K8s PostgreSQL consumer clause; confirms its existing exclusion of Valkey cluster from this repository, while preserving external placement, backup and data-lifetime ownership | [SPEC-0106](../../03.specs/0106-stage99-lifecycle-normalization/spec.md) |
| [ADR-0046](./0046-external-services-over-host-addresses.md) | Replaces only host `15432/15433` PostgreSQL route and PG bootstrap warning clauses; preserves host transport for OpenBao, telemetry, management Valkey and k3d API/TLS | [SPEC-0106](../../03.specs/0106-stage99-lifecycle-normalization/spec.md) |
