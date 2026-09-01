---
title: 'Mutable Target Revision Retention'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: accepted
owner: platform
updated: 2026-08-18
artifact_id: "ADR-0029"
---

# ADR-0029: Mutable Target Revision Retention

## Overview

[ADR-0026](0026-argo-cd-source-integrity-non-adoption.md) declined Argo CD Source
Integrity and recorded commit-SHA pinning of `targetRevision` as the preferred
control for the same gap, explicitly without authorizing it. This decision takes
that recommendation up and declines it, for a reason ADR-0026 did not examine:
pinning is not a hardening measure in this repository, it is a different
deployment model.

## Context

Twelve declarations track `targetRevision: main`. All twelve point at **this
repository**, not at an upstream chart:

- ten `gitops/apps/root/*-app.yaml` Applications whose source is a path in this
  repository
- `gitops/clusters/local/root-application.yaml`, the app-of-apps root
- `gitops/clusters/local/applicationset-apps.yaml`

Every Application that consumes an external Helm chart already pins an exact
chart version. The mutable reference is confined to self-reference.

Three facts decide this.

**Pinning changes when a change deploys, not only what.** Every one of these
Applications runs `automated` sync with `selfHeal`. Under a mutable `main`, a
merged commit reconciles on its own. Under a pinned SHA, it reconciles when a
second commit updates the pin. That is manual promotion, and it is a deployment
model rather than a control.

**The pin cannot reference the commit that sets it.** A commit updating twelve
`targetRevision` values necessarily names its own parent, so the deployed
revision always trails the authored one by at least one commit. Closing that gap
requires either a follow-up commit per change or automation that writes commits
back to the repository.

**Half of the identity gap is already observable.** Argo CD records the revision
it synced and reports drift against it. What a pin adds is immutability of the
reference, which matters when a branch can be rewritten under a running
controller. This repository has a single operator, no force-push workflow, and
Git-revert-first recovery.

## Decision

Keep `targetRevision: main` on all twelve self-referencing declarations. Do not
adopt commit-SHA pinning, a promotion branch, or automated pin-bumping.

Record that continuous reconciliation from `main` is the **intended** deployment
model for this lab, not an unclosed gap. The repository is authored and deployed
by one operator against one cluster, and the delay a promotion step would
introduce buys nothing that operator does not already have by reading the commit
they just merged.

Record equally that this is a property of the current operating model, not a
judgement that pinning is wrong. It becomes the right answer the moment the
model changes, and the reversal conditions below name when.

## Explicit Non-goals

- This decision does not claim commit-SHA pinning is unnecessary in general; for
  multi-environment or multi-operator repositories it is standard practice.
- It does not reopen ADR-0026's Source Integrity decision, which remains declined
  on independent grounds.
- It does not close the Git, chart, and image identity gap recorded in the
  research pack. That gap stays open and stays recorded.
- It does not change any Application's sync policy, and asserts no live
  reconciliation behavior.

## Consequences

The identity gap stays open, unchanged, and now has a recorded reason for staying
open rather than an unexecuted recommendation pointing at it. That is the
substantive difference from ADR-0026's position: a reader no longer finds a
preferred control that nobody adopted and cannot tell why.

A force-push to `main` would be reconciled. Nothing prevents that, and the
mitigation remains the same as for any accidental merge — revert and let
reconciliation converge. For a single-operator lab this is the same recovery path
already used for every other mistake.

Reconciliation stays immediate, which is what makes the lab useful for iterating
on manifests. Twelve promotion steps per change would have been the main cost of
the alternative, and it is not incurred.

Reversal stays cheap. Pinning is a value change in twelve files with no
structural work, so adopting it later costs no more than adopting it now.

## Alternatives

**Commit-SHA pinning — recommended by ADR-0026, declined here.** Gives exact
reproducibility and immunity to branch rewrites. Rejected because it converts
automated reconciliation into manual promotion across twelve declarations, and
because the pin can never reference its own commit, so a trailing gap remains by
construction. The threat it addresses — a rewritten branch under a running
controller — has no vector in a single-operator repository with no force-push
workflow.

**A `release` branch that `main` is fast-forwarded into.** Separates authored
from deployed at one merge instead of twelve pin updates, and is the cheapest way
to get a promotion gate. Rejected on the same ground as pinning: it buys a
promotion gate this lab has no use for, and `release` is itself mutable, so it
does not deliver the immutability that motivated the recommendation.

**Automated pin-bumping.** A job that rewrites `targetRevision` after each merge
would keep both reproducibility and immediacy. Rejected as machinery that writes
commits back to the repository, in a lab where the human-visible benefit is a
reference already available in Argo CD's synced-revision field.

**Pin the root Application only.** Superficially cheap. Rejected because it does
not work: each child Application re-resolves its own `targetRevision`
independently, so pinning the root changes nothing about what the children
deploy.

## Traceability

Reversal condition: reopen this decision when a second operator or a second
environment is added, when any workflow that can rewrite `main` is introduced,
when an incident is traced to a reconciliation the operator did not intend, or
when Argo CD's synced-revision reporting stops being sufficient to answer what is
deployed.

### Lifecycle Traceability

| Decision lineage                                                          | Replacement relation                                                                                          | Affected Spec                                            |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [ADR-0026](0026-argo-cd-source-integrity-non-adoption.md) preferred control | Resolves ADR-0026's unexecuted recommendation by declining it; supersedes no decision and reverses no adoption | N/A — standalone decision record with no execution scope |

### Related Documents

- [ADR-0026 — Argo CD source integrity non-adoption](0026-argo-cd-source-integrity-non-adoption.md)
- [Current local GitOps platform](../descriptions/0007-current-local-gitops-platform.md)
