---
title: 'ADR-0026: Argo CD Source Integrity Non-adoption'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-08-18
artifact_id: "ADR-0026"
---

# ADR-0026: Argo CD Source Integrity Non-adoption

## Overview

Argo CD `3.5.0`, released 2026-08-04, shipped a Source Integrity subsystem that
generalizes and replaces the legacy GPG-only signature verification mechanism.
`3.5.1`, released 2026-08-12, is a patch with no change to the feature. Its
arrival satisfied a refresh trigger the research pack had recorded against
`REQ-WERPC-008` and `REQ-WERPC-025`, which described the facility as
forward-looking and labeled version 3.5.

This decision declines to adopt it now, and records the stronger control that
would address the same gap.

## Context

The research pack records a Git, chart, and image identity gap for this
repository. Three facts frame the decision.

First, the gap's root cause is a mutable reference. Ten `gitops/apps/root/*.yaml`
declarations plus `gitops/clusters/local/root-application.yaml` and
`applicationset-apps.yaml` track `targetRevision: main`. Argo CD re-resolves that
branch to its current tip on every reconciliation.

Second, Source Integrity verifies a commit, not a reference. As implemented in
`3.5.0` and `3.5.1` it performs GPG-based Git commit signature verification,
configured through `AppProject.spec.sourceIntegrity.git.policies[].gpg` with
`mode` and `keys`. It authenticates whichever commit is currently at tip. It does
not pin a revision, does not prevent a force-push from being accepted provided
the new tip is also signed by a trusted key, and does not make a run reproducible.
A mutable branch under signature verification is an authenticated moving target,
not a pinned one.

Third, the facility's current scope is narrower than the recorded gap. Helm chart
provenance and OCI image digest or signature verification are not covered.
Extension to Sigstore, cosign, Helm, and OCI is named as a future direction on
the implementing pull request but is not built.

Two operational facts also bear on it. The repository installs Argo CD through an
operator-approved bootstrap step that runs
`helm upgrade --install argo/argo-cd`, which this cycle has now pinned to chart
`10.4.0`, application version `v3.5.1` — so the capability is present in the
pinned control plane. That install is operator-approved bootstrap execution, not
an agent action, and this decision triggers none of it.

And no commit in this repository is GPG-signed; the pack independently records
that no Git signature enforcement was observed.

## Decision

Do not adopt Argo CD Source Integrity.

Keep `AppProject.spec.sourceIntegrity` unset in
`gitops/clusters/local/appproject-apps.yaml` and
`appproject-platform.yaml`. Do not establish a GPG signing workflow, a key store,
or a trust policy for this purpose.

Record commit-SHA pinning of `targetRevision` as the preferred control for the
identity gap. It addresses the gap's actual cause, requires no key management, no
signing discipline, and no fail-closed gate, and delivers reproducibility that
signature verification cannot. It is not executed by this decision.

## Explicit Non-goals

- This decision does not reject signature verification in principle, and does not
  claim the facility is defective.
- It does not close the Git, chart, and image identity gap. The gap remains open
  and is unchanged by this decision.
- It does not authorize or schedule `targetRevision` SHA pinning; that is a
  separate design change over twelve declarations.
- It does not evaluate Argo CD's own release-artifact signing, which is about
  Argo CD's binaries rather than this repository's sources.
- It does not assess whether Source Integrity is enforced anywhere at runtime. No
  cluster was contacted.

## Consequences

The identity gap stays open and stays recorded. `REQ-WERPC-008` and
`REQ-WERPC-025` keep `Partial`; declining a capability changes no status.

Reconciliation keeps its current failure surface. Adopting the facility with
`mode: strict` would have added a fail-closed gate on every synced commit, and no
warn-only or audit mode could be confirmed in the current documentation. For a
single-operator lab whose recovery model is Git-revert-first, an unsigned
fix-up commit or a merge produced by the Git host's default merge button would
have stopped reconciliation for real workloads until the signing problem was
resolved. That failure mode is not introduced.

The legacy GPG surface is on a removal path. `AppProject.spec.signatureKeys`,
`argocd proj add-signature-key`, `remove-signature-key`, and the `verifyResult`
API field are deprecated in favor of Source Integrity, with removal targeted for
Argo CD 4.0. This repository uses none of them, so the deprecation costs nothing
here, but a future adoption decision must target Source Integrity rather than the
legacy mechanism.

Reversal is cheap. The facility is opt-in per `AppProject`, so adopting it later
is additive and breaks nothing until configured.

## Alternatives

**Commit-SHA pinning of `targetRevision` — preferred, not executed.** Replaces
the mutable branch with an immutable content identity, giving both verifiability
and reproducibility. Costs a deliberate update step per change and affects twelve
declarations. This addresses the gap's cause rather than authenticating its
symptom, and is the control this decision recommends instead.

**Adopt Source Integrity with `mode: strict`.** The strongest case for adoption is
real and worth stating: it is free to configure, needs no new infrastructure or
controller, is already present in the pinned control plane, and directly answers
"was this commit authored by someone I trust" — a genuine answer to GitHub account
or token compromise, which is the one threat a solo operator cannot rule out.
Rejected because it does not address the mutable-reference cause, covers only one
of the gap's three concerns, requires signing discipline the repository does not
have, adds a fail-closed gate with no confirmed soft-rollout mode, and was GA for
fourteen days at decision time with the hydrator-integrated form documented as
Alpha.

**Adopt Source Integrity in a non-strict mode first.** Rejected because no
warn-only or audit mode could be confirmed against primary documentation. Adopting
on the assumption that one exists would be resting a fail-closed control on an
unverified premise.

**Adopt the legacy `signatureKeys` mechanism.** Rejected outright: deprecated in
`3.5.0` with removal targeted for 4.0.

**Defer without recording anything.** Rejected. The trigger fired and would fire
again every cycle. Recording the decision and its reversal condition is what stops
the question from being re-litigated, in the same way the blocking-class closure
of the prior cycle stops structurally unreachable rows from being re-tested.

## Traceability

Reversal condition: reopen this decision when Source Integrity covers Helm chart
provenance or OCI image signatures, when a warn-only or audit mode is documented,
or when this repository adopts commit signing for an independent reason. Adopting
`targetRevision` SHA pinning does not reopen it, because the two controls are
orthogonal.

### Lifecycle Traceability

| Decision lineage                                | Replacement relation                                                                             | Affected Spec                                                           |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| Direct human approval recorded in the Spec body | N/A — first non-adoption decision over a fired research refresh trigger; supersedes no prior ADR | [Spec 0060](../../03.specs/0060-platform-currency-defect-closure/spec.md) |

### Related Documents

- [ADR 0022 — direct-approval standalone execution lineage](0022-direct-approval-standalone-execution-lineage.md)
- [Kubernetes, infrastructure, and security research](../../90.references/research/0001-workspace-engineering/kubernetes-infrastructure-and-security.md)
