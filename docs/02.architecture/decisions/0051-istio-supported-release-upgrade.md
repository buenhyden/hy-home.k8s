---
title: "Istio Supported Release Upgrade"
version: "1.0.1"
type: "sdlc/architecture-decision"
status: "accepted"
owner: "platform"
updated: "2026-10-20"
layer: "architecture"
artifact_id: "ADR-0051"
---

# ADR-0051: Istio Supported Release Upgrade

## Overview

This decision moves Istio `base`, `cni` and `istiod` from 1.25.2 to the
supported 1.31 line (1.31.2 or later). The local cluster is rebuilt at the
target version instead of being upgraded in place.

## Context

- The three Istio Applications under `gitops/apps/root/` pin 1.25.2.
- Istio 1.25 reached end of life on 2025-09-30. The Istio supported-releases
  page (read 2026-10-16) lists Kubernetes 1.29 to 1.32 for it, while the
  cluster runs Kubernetes 1.35
  (`rancher/k3s:v1.35.0-k3s1`).
- ISTIO-SECURITY-2025-001 lists 1.25.0 to 1.25.4 as affected.
- On 2026-10-16 the supported releases are 1.31 (end of life about February
  2027) and 1.30 (about December 2026). 1.29 is at its expected end of life.
- ISTIO-SECURITY-2026-007 (2026-10-15) is fixed in 1.31.2.
- Istio does not test or recommend upgrading across more than two minor
  versions in one step. The canary revision method is recommended for Helm.
- The cluster is a disposable local k3d cluster, rebuilt from the repository
  by `infrastructure/bootstrap-local.sh`.
- Gateway API, which [ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md)
  defers, is Stable in current Istio.

## Decision

- Target Istio 1.31.2 or later for `base`, `cni` and `istiod`, with the k3s
  CNI profile and the current values otherwise preserved.
- Method: rebuild the local cluster at the target version with
  `infrastructure/bootstrap-local.sh`, because the cluster is disposable and a
  rebuild avoids three canary hops. The operator chose this method on
  2026-10-20.
- Verify STRICT mTLS, the adminer canary and the Kiali, telemetry and tracing
  providers after the rebuild.

## Explicit Non-goals

- Adopting Gateway API or the Istio ingress gateway; that is a later decision.
- Changing the ingress controller (ADR-0050).
- Ambient mode.

## Consequences

- Positive: the mesh returns to a supported release with security fixes, and
  it is within the cluster's Kubernetes range. Gateway API becomes available as
  a later option.
- Negative: the rebuild discards cluster state that the repository does not
  declare. Values or CRD changes across six minor versions may need
  repository edits. The rebuild is planned after the SPEC-0121 ingress
  cutover, so that the cutover is verified once, on the current cluster.
- Operational: the rebuild is a live change and needs operator approval
  when it runs. Keep the version pinned and track Istio's support window.

## Alternatives

- **Stay on 1.25.2:** rejected. It is out of support and has known advisories.
- **Stop at 1.30:** rejected. Its end of life is about December 2026.
- **Single jump 1.25 to 1.31 on a running cluster:** rejected. Istio does not
  support it.
- **Canary revisions in two-minor-version hops (1.25 to 1.27, 1.29 and 1.31)
  on the running cluster:** rejected. It keeps cluster state but takes three
  upgrades, each needing its own notes and verification, while the cluster
  can be rebuilt from the repository.

## Traceability

The research for this decision was read on 2026-10-16 from the Istio supported
releases, upgrade and security pages. The operator chose the rebuild method on
2026-10-20.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0008](./0008-istio-install-and-ingress-coexist.md) | Not replaced. It keeps the Istio ingress gateway disabled; only the version changes | N/A — the upgrade Spec follows the method decision |
| [ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md) | Not replaced. It defers Gateway API until after this upgrade | N/A — no Spec implements the deferral |
