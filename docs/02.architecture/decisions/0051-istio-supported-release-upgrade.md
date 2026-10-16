---
title: "Istio Supported Release Upgrade"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "platform"
updated: "2026-10-16"
layer: "architecture"
artifact_id: "ADR-0051"
---

# ADR-0051: Istio Supported Release Upgrade

## Overview

This proposal moves Istio `base`, `cni` and `istiod` from 1.25.2 to the
supported 1.31 line (1.31.2 or later). It is proposed, not accepted. The
operator has not yet chosen the upgrade method.

## Context

- The three Istio Applications under `gitops/apps/root/` pin 1.25.2.
- Istio 1.25 reached end of life on 2025-09-30. Its supported Kubernetes range
  is 1.29 to 1.32, while the cluster runs Kubernetes 1.35
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

Proposed:
- Target Istio 1.31.2 or later for `base`, `cni` and `istiod`, with the k3s
  CNI profile and the current values otherwise preserved.
- Preferred method: rebuild the local cluster at the target version, because
  the cluster is disposable and a rebuild avoids three unsupported-era hops.
- Fallback when the running cluster must be kept: canary revisions in
  two-minor-version hops, 1.25 to 1.27, 1.29 and 1.31, reading each hop's
  upgrade notes.
- Verify STRICT mTLS, the adminer canary and the Kiali, telemetry and tracing
  providers after the change.

## Explicit Non-goals

- Adopting Gateway API or the Istio ingress gateway; that is a later decision.
- Changing the ingress controller (ADR-0050).
- Ambient mode.

## Consequences

- Positive: the mesh returns to a supported release with security fixes, and
  it is within the cluster's Kubernetes range. Gateway API becomes available as
  a later option.
- Negative: a rebuild discards cluster state, and a hop upgrade is slow and
  needs per-hop verification. Values or CRD changes across six minor versions
  may need repository edits.
- Operational: the chosen method needs operator approval before any live
  change. Keep the version pinned and track Istio's support window.

## Alternatives

- **Stay on 1.25.2:** rejected. It is out of support and has known advisories.
- **Stop at 1.30:** rejected. Its end of life is about December 2026.
- **Single jump 1.25 to 1.31 on a running cluster:** rejected. Istio does not
  support it.

## Traceability

The research for this proposal was read on 2026-10-16 from the Istio supported
releases, upgrade and security pages.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0008](./0008-istio-install-and-ingress-coexist.md) | Not replaced. It keeps the Istio ingress gateway disabled; only the version changes | N/A — the upgrade Spec follows the method decision |
| [ADR-0050](./0050-ingress-nginx-replacement-with-traefik.md) | Not replaced. It defers Gateway API until after this upgrade | N/A — no Spec implements the deferral |
