---
title: 'ADR-0014: Current Local GitOps Platform Contract'
type: adr
status: accepted
owner: platform
updated: 2026-06-02
---

# ADR-0014: Current Local GitOps Platform Contract

## Overview (KR)

이 ADR은 현재 구현된 local GitOps platform contract를 하나의 active architecture decision으로 고정한다.
old topology, endpoint, and cluster UI decisions are archived as Tombstones and no longer serve as active implementation input.

## Context

The repository has current desired state under `gitops/`, bootstrap and validation assets under `infrastructure/`, and quality gates under `scripts/`.
Several older documents described replaced endpoints or removed UI resources. Active architecture must now describe only the repo-backed current state and link old records through the archive index.

## Decision

- The active platform contract is WSL2 + WSL-native Docker + k3d + ArgoCD App-of-Apps.
- Current external service contracts are the `Service` and `EndpointSlice` manifests under `gitops/platform/external-services`.
- Current network-policy egress contracts are under `gitops/platform/network-policies`.
- Headlamp is the current cluster UI surface under `gitops/apps/root/platform-headlamp-app.yaml` and `gitops/platform/headlamp`.
- Kiali, Istio, cert-manager, ingress-nginx, Argo Rollouts, Argo Notifications, monitoring, and ESO/Vault integration remain in active scope.
- Old replaced decisions are removed from active input and represented only by `docs/98.archive/README.md` and Tombstones.

## Explicit Non-goals

- This ADR does not define live cluster repair or external service startup.
- This ADR does not store secret values or Vault runtime state.
- This ADR does not preserve old decision bodies in active docs.

## Consequences

- **Positive**:
  - Active docs point to one current platform decision.
  - Static checks can fail on stale implementation contracts instead of allowing them with old status markers.
  - Archived docs remain discoverable without polluting current implementation context.
- **Trade-offs**:
  - Old decision body details are no longer available in active docs.
  - Readers must use Git history for full historical body reconstruction.

## Alternatives

### Keep Old Decisions Active With Current Notes

- Good: Preserves narrative context in place.
- Bad: Allows agents and readers to confuse stale contract text with current implementation.

### Delete Old Decisions Without Tombstones

- Good: Maximally reduces stale content.
- Bad: Loses reviewable routing and replacement evidence.

## Agent-related Example Decisions (If Applicable)

- Agents must prefer this ADR and the active PRD/ARD/Spec chain for current platform work.
- Agents may use the archive index to understand why a path disappeared, but must not use Tombstones as design input.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-02-current-local-gitops-platform.md](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- **ARD**: [../requirements/0007-current-local-gitops-platform.md](../requirements/0007-current-local-gitops-platform.md)
- **Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md](../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
