---
title: 'Pod Security Admission Per-namespace Adoption'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: accepted
owner: platform
updated: 2026-08-18
artifact_id: "ADR-0028"
---

# ADR-0028: Pod Security Admission Per-namespace Adoption

## Overview

[ADR-0027](0027-pod-security-standards-staged-adoption.md) declined to apply Pod
Security Admission labels and recorded an ordering: install the Istio CNI node
agent, then apply non-rejecting `warn` and `audit`, then apply `enforce` per
namespace. Its reversal condition fired when the CNI agent was adopted.

This decision takes the question again with evidence ADR-0027 did not have, and
adopts labels — but not uniformly. Each namespace gets the strongest mode its own
evidence supports, and three namespaces are deliberately held back.

## Context

Four facts decide this, and two of them are constraints ADR-0027 could not see.

**Every workload now satisfies Restricted, except where Istio injects.** The
compliance survey found six Restricted shortfalls; all six were closed. Every
workload this repository deploys or configures passes both profiles as rendered
with this repository's own values.

**Istio's injected containers carry no `seccompProfile`.** The sidecar injection
template sets it only for gateways, never for `istio-proxy` or
`istio-validation`. Restricted's seccomp rule is satisfied by a pod-level value
or by every container setting one, so an injected pod reaches Restricted only if
its **pod** securityContext sets `seccompProfile`. Neither `adminer` nor the
`ingress-nginx` controller does — the latter renders no pod securityContext at
all. Restricted is therefore currently unreachable in `apps` and
`ingress-nginx`, though only two small edits away.

**The CNI adoption is not live-verified.** It is repository-static and
render-verified only. Nothing yet proves the agent installs on all four k3d
nodes, that redirection works, or that injected pods start. If it did not take
effect, injected pods still carry `istio-init` with `NET_ADMIN` and `NET_RAW`,
and `enforce: baseline` on those namespaces would reject every one of them.
Enforcing there now would convert an unverified change into an outage.

**Helm-owned compliance is version-bound.** The four non-injected Helm namespaces
pass Restricted at their current chart versions. That is a fact about those
versions, not a property of the charts. `enforce` there would turn a future chart
upgrade that regresses into a failed sync rather than a warning.

One namespace was unavailable when this decision was taken: `argocd` holds pods
but was not GitOps-declared, because bootstrap installs that chart before GitOps
ownership exists, so a label there would have had no home in this repository.
That gap has since been closed — see the amendment under `Decision`.

And one is permanently exempt: `istio-cni-node` requires `NET_ADMIN`, `NET_RAW`,
`SYS_PTRACE`, `SYS_ADMIN`, `DAC_OVERRIDE` and a `/proc` hostPath on every node,
so `istio-system` can never satisfy Baseline. That is the recorded cost of the
CNI trade, not a defect.

## Decision

Apply `pod-security.kubernetes.io` labels to the GitOps-declared namespaces, at a
level chosen per namespace from its own evidence.

| Namespace                                                       | `enforce`    | `audit` / `warn` |
| --------------------------------------------------------------- | ------------ | ---------------- |
| `istio-system`                                                  | `privileged` | `privileged`     |
| `monitoring`, `platform`                                        | `restricted` | `restricted`     |
| `cert-manager`, `external-secrets`, `headlamp`, `argo-rollouts` | none         | `restricted`     |
| `apps`, `ingress-nginx`                                         | none         | `baseline`       |

Pin `enforce-version` to the cluster's current minor and leave `audit` and `warn`
unpinned. An unpinned `enforce` can begin rejecting workloads after a Kubernetes
upgrade with no change to this repository; an unpinned `audit`/`warn` reports
what a future version would reject without acting on it. The pair gives stable
enforcement plus forward warning.

`argocd` was excluded when this decision was taken because it was not
GitOps-declared. **That has since been amended.** The namespace is now declared
in `gitops/platform/namespaces/namespace-argocd.yaml` and carries `audit` and
`warn` at `restricted`, with no `enforce`.

Two constraints shape that amendment. The namespace is adopted with
`argocd.argoproj.io/sync-options: Prune=false`, because the owning Application
prunes and a pruned `argocd` namespace would delete every Application in it along
with Argo CD itself. And `enforce` is withheld for a stronger version of the
chart-version argument above: all ten `argo-cd` workloads pass Restricted at the
pinned version, but enforcing there would mean a regressing chart upgrade locks
Argo CD out of its own namespace.

Enforce only where compliance is a property of manifests this repository controls
and does not depend on the unverified CNI change. `monitoring` holds two
repository-authored workloads with no injection; `platform` holds no pods at all,
so the label costs nothing and guards future additions.

Use `warn` and `audit` at `baseline` on the injected namespaces deliberately, not
as a placeholder. That channel is the live verification signal for the CNI
adoption: if the agent took effect, injected pods produce no warning; if it did
not, the `istio-init` capabilities warning appears on every one. This converts an
outstanding verification into an observable rather than an inspection.

## Explicit Non-goals

- This decision does not enforce on any injected namespace, and does not claim the
  CNI adoption succeeded.
- It did not add the pod-level `seccompProfile` that `adminer` and the
  `ingress-nginx` controller need for Restricted; that was named as a separate
  change and has since been made. With it, both namespaces satisfy Restricted on
  the manifest, and the remaining barrier to raising them is the live CNI
  verification alone rather than two barriers.
- It did not label `argocd` or resolve that namespace's pre-GitOps ownership
  gap; both were done afterwards and are recorded as an amendment above. The
  broader pre-GitOps boundary — bootstrap installing charts before GitOps
  ownership exists — remains open and is the same boundary that left both
  bootstrap charts unpinned until Spec 059.
- It does not assess the Kiali operand, cert-manager ACME solver pods, or any
  other runtime-created pod spec.
- It asserts no admission outcome. No cluster was contacted.

## Consequences

The convention becomes enforced where it is safe and observed everywhere else. A
workload can no longer silently omit the hardening pattern in `monitoring` or
`platform`, which is the failure mode that let `adminer` escape it.

Two namespaces gain a live verification signal they did not have. The CNI
adoption's outstanding question is answered by whether Baseline warnings appear
in `apps` and `ingress-nginx`, without any risk of rejection.

`istio-system` is now explicitly and permanently `privileged`. Making that visible
in the namespace manifest is preferable to leaving it as an unstated default,
because a reader can see that the exemption is deliberate and why.

A chart upgrade that regresses compliance in the four `audit`-only namespaces will
warn rather than fail. That is the intended trade for this stage; promoting them
to `enforce` is a later decision with its own evidence.

Reversal is per-namespace and additive. Removing a label restores prior behavior
immediately, and no label here rejects a workload that runs today, with the single
exception of `monitoring` and `platform` — both verified Restricted-clean, one of
which has no pods.

## Alternatives

**Enforce Baseline everywhere now.** The evidence nearly supports it: every
workload passes Baseline post-CNI. Rejected because "post-CNI" is exactly the
unverified part. If the agent is not working on k3d, this rejects every injected
pod in the two namespaces that serve traffic. The gap between render-verified and
live-verified is precisely where this would fail.

**Enforce Restricted everywhere reachable, including the Helm namespaces.**
Tempting and currently true. Rejected because their compliance is a property of
pinned chart versions rather than of anything this repository authors, so the
first upgrade that regresses becomes a failed sync during an unrelated change.
`audit` surfaces the same regression without coupling it to an upgrade window.

**Keep `warn`/`audit` only, enforce nothing.** The conservative reading of
ADR-0027. Rejected because it declines free safety: `monitoring` and `platform`
are provably clean, independent of the CNI question and of any chart, and
enforcement there cannot reject anything that exists.

**Add the pod-level `seccompProfile` first and enforce Restricted on the injected
namespaces too.** Rejected for sequencing, not merit. Restricted on those
namespaces is worth having, but stacking it on top of an unverified CNI change
compounds two unknowns into one failure. Raise them after the Baseline warning
channel comes back clean.

**Pin nothing, or pin everything.** Pinning nothing lets a Kubernetes upgrade
start rejecting workloads with no repository change. Pinning everything hides the
fact that a future version would tighten. Splitting them is what makes the warning
channel useful.

## Traceability

Reversal condition: reopen this decision when the Baseline warning channel on
`apps` and `ingress-nginx` is observed clean, which unblocks `enforce: baseline`
there; when the pod-level `seccompProfile` is added to those workloads, which
unblocks Restricted; or when a chart upgrade regresses one of the `audit`-only
namespaces, which is the event those labels exist to surface.

### Lifecycle Traceability

| Decision lineage                                                                    | Replacement relation                                                                                  | Affected Spec                                            |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [ADR-0027](0027-pod-security-standards-staged-adoption.md) after its reversal fired | Supersedes ADR-0027's steps 2 and 3; ADR-0027 is retained as the reasoning that produced the ordering | N/A — standalone decision record with no execution scope |

### Related Documents

- [ADR-0027 — Pod Security Standards staged adoption](0027-pod-security-standards-staged-adoption.md)
- [Kubernetes infrastructure and security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)
- [Istio CNI application](../../../gitops/apps/root/platform-istio-cni-app.yaml)
