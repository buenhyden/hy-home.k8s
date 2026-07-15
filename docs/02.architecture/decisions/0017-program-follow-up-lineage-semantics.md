---
title: 'ADR-0017: Program Follow-up Lineage Semantics'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-15
---

# ADR-0017: Program Follow-up Lineage Semantics

## Overview

This decision preserves ADR-0016's seven original modernization tranches while
modeling completed Spec 033 as a follow-up within the same broader program.

## Context

ADR-0016, PRD-005, and ARD-0008 consistently define Specs 026-032 as seven
dependent tranches. Registry v5 lists Spec 033 in the same specs array even
though Spec 033 was approved after those tranches as template lifecycle
normalization. Rewriting accepted documents would erase the original decision;
leaving the registry unchanged makes machine lineage contradict it.

## Decision

- Keep Specs 026-032 as the immutable original tranche set for PRD-005 and
  ARD-0008.
- Record Spec 033 as a completed follow-up relation, not an eighth tranche.
- Extend the registry lineage model with separate tranches and followUps
  collections.
- Require a mutable or future follow-up to name its program PRD, ARD,
  governing decision, reason, status, and predecessor evidence through registry
  facts and reciprocal body links.
- For Spec 033, which was completed before this decision, use this ADR,
  registry facts, and the mutable remediation overlay as successor-side
  evidence; do not rewrite its completed body to manufacture reciprocity.
- Preserve historical numbering and prohibit inference that every later Spec
  sharing an upstream program is an original tranche.
- Use this same relation model for PRD-006 and Specs 034-040.

## Explicit Non-goals

- Superseding ADR-0016's original seven-tranche decision.
- Editing completed Spec 033 to simulate an original-tranche approval.
- Renumbering Specs, PRDs, or ARDs.
- Adding a universal lineage frontmatter key.
- Allowing unbounded follow-ups without an accepted decision and current owner.

## Consequences

- Machine lineage and accepted narrative become consistent.
- Program completion can distinguish original scope from later corrective work.
- Validators gain one additional relation type and reciprocal consistency rule.
- Future follow-ups require explicit admission evidence instead of array
  append-only behavior.

## Alternatives

- **Expand the program to eight original tranches**: rejected because it changes
  the meaning of the accepted seven-tranche decision after completion.
- **Remove Spec 033 from all program lineage**: rejected because it loses its
  genuine upstream product and architecture relationship.
- **Rewrite ADR-0016, PRD-005, and ARD-0008**: rejected because accepted and
  completed records are historical evidence.

## Traceability

- **Original decision**: [ADR-0016](./0016-program-to-tranche-document-lineage.md)
- **Original program**: [PRD-005](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **Original architecture**: [ARD-0008](../requirements/0008-workspace-document-assurance-operating-model.md)
- **Follow-up**: [Spec 033](../../03.specs/033-template-lifecycle-contract-normalization/spec.md)
- **New program**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| ADR-0016 original program lineage | Complementary successor; original decision remains accepted | [Spec 034](../../03.specs/034-authority-and-lineage-foundation/spec.md) |
