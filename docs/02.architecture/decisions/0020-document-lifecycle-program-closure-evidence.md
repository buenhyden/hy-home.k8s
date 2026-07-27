---
title: 'ADR-0020: Document Lifecycle Program Closure Evidence'
type: sdlc/adr
status: draft
owner: platform
updated: 2026-07-27
---

# ADR-0020: Document Lifecycle Program Closure Evidence

## Overview

This draft decision records the closure-evidence architecture for the PRD-006
and ARD-0009 document lifecycle program. It exists so the final ARD-0009
`active` to `accepted` transition has a dedicated role-decision evidence owner
that can later move through the lifecycle validator's same-diff
`active` to `accepted` predicate.

## Context

PRD-006 and ARD-0009 define the document lifecycle, full-body archive,
reference-currentness, execution-retention, strict validation, and repository
QA program. Specs 034 through 039 already provide most tranche evidence, and
Spec 040 owns the final strict cutover and program closure.

The architecture lifecycle contract requires an ARD acceptance proposal to link
to at least one accepted ADR that also changes status and body in the same diff.
ADR-0017 and ADR-0018 are already accepted historical decisions, so they cannot
provide that same-diff evidence for the ARD-0009 terminal transition. A separate
closure decision is needed to preserve accepted history while giving Spec 040 a
bounded, current role-decision evidence path.

## Decision

- Introduce this ADR as the dedicated closure-evidence decision for PRD-006,
  ARD-0009, and Spec 040.
- Keep the decision in `draft` until the closure matrix and repository-static
  evidence are complete enough to justify activation.
- Require this ADR to remain reciprocally linked with ARD-0009 while it is
  `draft` or `active`.
- Use this ADR, after a later `active` to `accepted` transition, as the
  same-diff role-decision evidence for ARD-0009 acceptance.
- Preserve ADR-0017 and ADR-0018 as historical accepted decisions rather than
  reopening or rewriting them to manufacture closure evidence.
- Keep hosted, provider, remote, and live evidence classifications separate from
  repository-static closure results.

## Explicit Non-goals

- Accepting ARD-0009 in this draft commit.
- Accepting this ADR before Spec 040 final review and QA evidence exists.
- Superseding ADR-0017 or ADR-0018.
- Rewriting accepted decisions or completed tranche bodies for cosmetic
  reciprocity.
- Claiming current hosted, provider, remote, or live readiness from local static
  validation.

## Consequences

- ARD-0009 can later close through the registry's `accept-architecture`
  predicate without reusing already accepted ADRs as synthetic same-diff
  evidence.
- Spec 040 gains an explicit decision evidence path for the final atomic closure
  proposal.
- One additional ADR must be activated before the terminal closure commit and
  accepted in that same terminal proposal.
- Closure remains honest about repository-static PASS versus deferred external
  lanes.

## Alternatives

- **Reuse ADR-0017 or ADR-0018**: rejected because both are already accepted and
  cannot satisfy the same-diff status and body evidence required for ARD
  acceptance.
- **Use draft ADR-0019**: rejected because ADR-0019 belongs to the later
  PRD-003 / ARD-0006 agent-governance program and is gated on Specs 041 through
  046.
- **Accept ARD-0009 without a new decision evidence path**: rejected because it
  would conflict with the registry-owned lifecycle predicate.

## Traceability

- **Architecture**:
  [ARD-0009](../requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Program PRD**:
  [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **Final tranche**:
  [Spec 040](../../03.specs/040-contract-cutover-and-program-closure/spec.md)
- **Historical decisions**:
  [ADR-0017](./0017-program-follow-up-lineage-semantics.md) and
  [ADR-0018](./0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ARD-0009](../requirements/0009-document-lifecycle-evidence-operating-model.md) | Adds a dedicated closure-evidence decision for final PRD-006 / ARD-0009 acceptance; existing ADR-0017 and ADR-0018 remain accepted history. | N/A — Spec 040 already owns the final closure plan and will link this ADR during the terminal proposal. |
