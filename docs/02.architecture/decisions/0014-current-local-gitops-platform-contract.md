---
title: "Current Local GitOps Platform Contract"
version: "1.0.5"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-10-05"
layer: "architecture"
artifact_id: "ADR-0014"
---

# ADR-0014: Current Local GitOps Platform Contract

## Overview

This ADR fixes the currently implemented local GitOps platform contract as one active architecture decision.
old topology, endpoint, and cluster UI decisions no longer serve as active implementation input.

## Context

The repository has current desired state under `gitops/`, bootstrap and validation assets under `infrastructure/`, and quality gates under `scripts/`.
Several older documents described replaced endpoints or removed UI resources. Active architecture must now describe only the repo-backed current state and leave replaced records to Git history.

## Decision

- The active platform contract is WSL2 + WSL-native Docker + k3d + ArgoCD App-of-Apps.
- Current external service contracts are the `Service` and `EndpointSlice` manifests under `gitops/platform/external-services`.
- Current network-policy egress contracts are under `gitops/platform/network-policies`.
- Headlamp is the current cluster UI surface under `gitops/apps/root/platform-headlamp-app.yaml` and `gitops/platform/headlamp`.
- Kiali, Istio, cert-manager, the Traefik ingress controller ([ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md)), Argo Rollouts, Argo Notifications, monitoring, and ESO/Vault integration remain in active scope.
- Old replaced decisions are removed from active input and removed from this log and recovered only from Git history.

### Agent decision application

- Agents must prefer this ADR and the active PRD/ARD/Spec chain for current platform work.
- Agents must not use deleted or archived documents as design input.

## Explicit Non-goals

- This ADR does not define live cluster repair or external service startup.
- This ADR does not store secret values or Vault runtime state.
- This ADR does not preserve old decision bodies in active docs.

## Consequences

- **Positive**:
  - Active docs point to one current platform decision.
  - Static checks can fail on stale implementation contracts instead of allowing them with old status markers.
  - Replaced docs stay out of current implementation context.
- **Trade-offs**:
  - Old decision body details are no longer available in active docs.
  - Readers must use Git history for full historical body reconstruction.

## Alternatives

### Keep Old Decisions Active With Current Notes

- Good: Preserves narrative context in place.
- Bad: Allows agents and readers to confuse stale contract text with current implementation.

### Delete Old Decisions Without Replacement Routing

- Good: Maximally reduces stale content.
- Bad: Loses in-tree routing; Git history is the only recovery path.

## Traceability

**Current-state clarification (2026-11-03).** Under
[ADR-0053](./0053-unvalidated-archive.md) there are no tombstones and no archive
index. The archive wording in this decision is superseded by that rule: deleted
documents are summarized in the Archived Lineage tables and recovered with
`git show <commit>:<path>`. The platform baseline is unchanged.

**Current-state clarification (2026-10-03).** The agent application clause's
current authority chain is [REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md)
→ [AD-0007](../descriptions/0007-current-local-gitops-platform.md) → executable
desired state and validators in [gitops](../../../gitops/),
[infrastructure](../../../infrastructure/) and [scripts](../../../scripts/).
AD-0007 names the current operating owners.
The earlier Spec package is
not ongoing execution authority. A later platform
change uses its own scoped work unit; this clarification preserves the accepted
platform decisions and does not declare remaining delivery-assurance gaps closed.

**Current-state clarification (2026-09-23).** The
`vault-external` identifier is retired under [ADR-0046](./0046-external-services-over-host-addresses.md): ESO
reaches OpenBao at `https://openbao.hy.home.arpa` with a pinned CA, and other
external services are reached through host-published ports. The
`vault-backend` identifier and the secret-value boundary are unchanged.

**Current-state clarification (2026-09-23).** The host named here as
WSL2 with WSL-native Docker is a single Linux server with the native Docker
Engine under [ADR-0042](./0042-linux-server-single-host-baseline.md). Every
other clause of this decision is unchanged.

**Current-state clarification (2026-09-23).** The secret backend named here as
Vault is now OpenBao under
[ADR-0041](./0041-openbao-secret-backend.md). The ESO integration, the
`vault-external` and `vault-backend` identifiers, and the secret-value boundary
stated above are unchanged.

**Current-state clarification (2026-09-14).** The archive clauses below predate ADR-0030 and ADR-0038. A superseded decision body
leaves the Stage 02 decision log for `docs/98.archive/superseded/` with its
reciprocal supersession links, and terminal documents are
retained in `docs/98.archive/` by retention class rather than represented only
by the archive index and Tombstones. The document chain is now named
Requirement, Architecture Description and Spec rather than PRD, ARD and Spec.
The platform baseline this decision records is unchanged.

- **PRD**: [../../01.requirements/0004-current-local-gitops-platform.md](../../01.requirements/0004-current-local-gitops-platform.md)
- **ARD**: [../descriptions/0007-current-local-gitops-platform.md](../descriptions/0007-current-local-gitops-platform.md)
- **Spec**: N/A — SPEC-0008 left the tree; Git history recovers it ([REQ-0004 Archived Lineage](../../01.requirements/0004-current-local-gitops-platform.md#archived-lineage))

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [Architecture owner](../descriptions/0007-current-local-gitops-platform.md) | N/A — no whole-document supersession; scoped current-state clarifications above remain preserved | N/A — SPEC-0008 left the tree; Git history recovers it |
