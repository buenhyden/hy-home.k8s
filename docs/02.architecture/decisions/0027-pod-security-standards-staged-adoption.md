---
title: 'ADR-0027: Pod Security Standards Staged Adoption'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: accepted
owner: platform
updated: 2026-08-18
artifact_id: "ADR-0027"
---

# ADR-0027: Pod Security Standards Staged Adoption

## Overview

The Spec 060 cycle established that this repository has a real workload hardening
convention and that nothing enforces it. No namespace declares a
`pod-security.kubernetes.io` label and no policy engine is installed, so a
workload escapes the convention by omission rather than by override — which is
exactly how `adminer` escaped it.

Pod Security Admission is the built-in mechanism that would close that. This
decision declines to apply it now, and records the prerequisite chain, the
ordering, and the ownership boundary that a future adoption must respect.

## Context

Three facts frame the decision, and the second one reorders the work.

**The convention is unenforced and the gap is invisible.** Both platform
workloads carry pod `runAsNonRoot: true`, `runAsUser: 65534`, `fsGroup: 65534`
and container `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`,
`readOnlyRootFilesystem: true`. `adminer` carried none of it until Spec 060, and
nothing reported that. A convention that produces no signal when violated is
indistinguishable from an accident.

**The binding prerequisite is Istio, not any workload.** The Baseline profile's
capabilities control restricts `spec.initContainers[*].securityContext.capabilities.add`
alongside the container and ephemeral-container paths, and its allowed list is
`AUDIT_WRITE`, `CHOWN`, `DAC_OVERRIDE`, `FOWNER`, `FSETID`, `KILL`, `MKNOD`,
`NET_BIND_SERVICE`, `SETFCAP`, `SETGID`, `SETPCAP`, `SETUID`, and `SYS_CHROOT`.
`NET_ADMIN` and `NET_RAW` are not on it.

This repository deploys Istio `1.25.2` as `base` and `istiod` only. There is no
`istio-cni` Application. Istio documents that default sidecar injection uses an
`istio-init` init container requiring "the `NET_ADMIN` and `NET_RAW`
capabilities", and that the CNI node agent "enables the same networking
functionality, but without requiring the use or deployment of privileged init
containers in every workload", "thereby removing the need for privileged init
containers, as well as the requirement for `NET_ADMIN` and `NET_RAW`
capabilities".

`apps` and `ingress-nginx` both carry `istio-injection: enabled`. Applying
Baseline to either would flag every injected pod. That flag would be correct
about the capability and wrong about the cause: it reports Istio's chosen
networking mechanism, not a workload defect.

**Most namespaces are not this repository's to fix.** GitOps declares nine
namespaces. This repository authors the pod specs in exactly two: `monitoring`,
holding `kube-state-metrics` and `alloy-k8s-logs`, and `apps`, holding `adminer`.
One, `platform`, holds no pods at all — nine Services, nine EndpointSlices, and
six NetworkPolicies — so a profile there admits nothing and changes nothing. The
remaining six hold Helm-chart-managed workloads whose pod specs are upstream:
`cert-manager`, `external-secrets`, `headlamp`, `ingress-nginx`, `istio-system`,
and `argo-rollouts`. Adopting a profile there means auditing charts this
repository does not own, and absorbing their upgrades as a compliance surface.

A seventh Helm-owned namespace, `argocd`, holds pods but is not GitOps-declared,
because bootstrap installs the `argo-cd` chart directly before GitOps ownership
exists. A label on it would have no GitOps home today, which is the same
pre-GitOps ownership boundary that left both bootstrap charts unpinned until
Spec 059.

One namespace is close to unambiguous, but not as close as it first appears.
`monitoring` declares `istio-injection: disabled`, and both its workloads satisfy
Baseline and three of Restricted's four added controls: `runAsNonRoot: true`,
`allowPrivilegeEscalation: false`, and `capabilities.drop: [ALL]`. Neither sets
`seccompProfile`, at pod or container level, so both fail Restricted on that one
control. Restricted requires `RuntimeDefault` or `Localhost`; Baseline does not
require it at all, which is why a workload that looks fully hardened can still be
Baseline-clean and Restricted-dirty.

## Decision

Do not apply `pod-security.kubernetes.io` labels to any namespace now, and do not
install a policy engine for this purpose.

Record the adoption ordering, so that a future cycle starts from the binding
constraint rather than from the most visible workload:

1. Install the Istio CNI node agent, which removes the `istio-init` privileged
   init container and with it the Baseline violation on `apps` and
   `ingress-nginx`.
2. Apply `warn` and `audit` at `baseline`, which report and never reject, and
   observe the actual signal before changing any admission outcome.
3. Apply `enforce` per namespace, starting with `monitoring`. Its workloads
   satisfy Baseline today, so `enforce=baseline` is admissible there immediately.
   Reaching `enforce=restricted` there additionally requires adding
   `seccompProfile.type: RuntimeDefault` to both workloads — a repository-static
   edit with no other prerequisite.

Treat step 1 as a prerequisite rather than a parallel option. Steps 2 and 3 read
as low-risk in isolation and are not, because their signal is meaningless while
the mesh's own init container is the dominant violation.

## Explicit Non-goals

- This decision does not reject Pod Security Admission, and does not claim the
  mechanism is unsuitable.
- It does not authorize, schedule, or design the Istio CNI installation. That is a
  node-networking change with its own risk and its own approval.
- It did not assess whether any Helm-managed workload satisfies Baseline or
  Restricted; none was inspected at the time this decision was taken. That
  assessment has since been carried out against the repository manifests and is
  summarized in
  [the Kubernetes security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md),
  which amends the `warn`/`audit` alternative below without changing this
  decision.
- It does not close the `adminer` deferred controls, which remain blocked on
  reading the image filesystem.
- It does not assert any admission, scheduling, or rejection behavior. No cluster
  was contacted.

## Consequences

The hardening convention stays conventional. A future workload can omit it and
nothing will report the omission, exactly as happened with `adminer`. The
mitigation until adoption is the corrected sample template, which now carries the
complete pattern, and review.

No admission behavior changes, so no workload that runs today can stop running
because of this decision.

The ordering above is now recorded, which is the decision's main product. Without
it, a future cycle would predictably start by labeling the namespace holding the
workload it just hardened — `apps` — and would hit the Istio violation
immediately, learning the constraint by failed reconciliation rather than by
reading.

The Istio CNI prerequisite acquires a second justification beyond PSS. Removing a
privileged init container from every injected pod is a defensible posture
improvement whether or not Pod Security Admission is ever enabled.

Adoption stays cheap to begin. `warn` and `audit` reject nothing by definition, so
step 2 is reversible by deleting two labels, and step 3 is per-namespace and
additive.

## Alternatives

**Install Istio CNI first, then adopt — preferred, not executed.** This is the
ordering recorded in the Decision. It is preferred because it removes the
dominant violation at its source rather than exempting it, and it improves posture
independently. Not executed here because node-level networking changes in a k3d
cluster carry their own failure mode and warrant their own evaluation and
approval.

**Apply `warn` and `audit` at `baseline` to every namespace now.** Genuinely
tempting: neither mode can reject a pod, so the change is risk-free in the
admission sense, and it would make the gap visible immediately.

This decision originally rejected it on the grounds that the Helm-owned
namespaces would contribute warnings this repository cannot act on. **A
subsequent survey disproved that.** Every deployed workload passes Baseline, so
those namespaces would contribute no warnings at all, and the entire signal
would be the Istio init container in two namespaces — precise, singular, and
already understood. See
[the Kubernetes security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md).

The rejection therefore rests on a narrower and weaker argument than recorded:
the one signal Baseline would produce is a fact this decision already documents,
so enabling it buys regression detection rather than discovery. That is real but
modest value, and it is still ordered after the Istio prerequisite, because
turning it on first would establish a warning channel whose only content is a
violation the prerequisite exists to remove.

**Apply PSS to `monitoring` only.** The safest possible pilot: injection is
disabled and both workloads satisfy Baseline, so `enforce=baseline` would change
nothing there. Rejected as a standalone move for that same reason — it exercises
the mechanism only where there is no problem, and produces no evidence about the
namespaces that have one. It is retained as step 3's starting point rather than as
a cycle of its own. Note that the same property does not hold at Restricted, where
both workloads currently fail on `seccompProfile`.

**Label `apps` and `ingress-nginx` as `privileged` explicitly.** Would let the
other namespaces adopt Baseline immediately. Rejected because it encodes the
current gap as a permanent exemption at exactly the two namespaces that serve
traffic, and removes the pressure to install CNI.

**Install Kyverno or Gatekeeper instead.** More expressive than the three built-in
profiles, and able to express the coupling rule that Spec 060 recorded. Rejected
for now: it adds a controller, its own CRDs, and its own upgrade surface to a
single-operator lab, to solve a problem the built-in admission plugin already
covers at this scale.

## Traceability

**This decision's reversal condition has since fired.** The Istio CNI node agent
was adopted as `platform-istio-cni` with `pilot.cni.enabled: true` on istiod,
which removes the `istio-init` violation from `apps` and `ingress-nginx` and
completes step 1 of the ordering above. Steps 2 and 3 are therefore unblocked and
require a fresh decision; this record is retained as the reasoning that produced
the ordering, not as a current instruction to withhold labels.

Reversal condition: reopen this decision when the Istio CNI node agent is
installed, when Istio's default injection no longer requires a privileged init
container, or when a policy requirement arrives that the built-in profiles cannot
express. Hardening an individual workload does not reopen it, because the binding
constraint is the mesh's networking mechanism rather than any workload's spec.

### Lifecycle Traceability

| Decision lineage                                | Replacement relation                                                                                        | Affected Spec                                            |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Direct human approval recorded in this decision | N/A — first Pod Security Admission adoption decision; supersedes no prior ADR and replaces no prior control | N/A — standalone decision record with no execution scope |

### Related Documents

- [ADR-0026 — Argo CD source integrity non-adoption](0026-argo-cd-source-integrity-non-adoption.md)
- [Spec 060 — workload security context baseline](../../03.specs/0061-workload-security-context-baseline/spec.md)
- [Kubernetes, infrastructure, and security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)
