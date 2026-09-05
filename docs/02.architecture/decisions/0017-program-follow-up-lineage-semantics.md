---
title: "Program Follow-up Lineage Semantics"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "superseded"
owner: "platform"
updated: "2026-09-01"
layer: "architecture"
artifact_id: "ADR-0017"
superseded_by: "ADR-0031"
---

# ADR-0017: Program Follow-up Lineage Semantics

## Overview

### Historical source citations after authority transfer

References marked Historical below identify the exact original source in a sealed
superseded record; they do not change which Requirement or AD this document originally
served. Current semantic authority is held by [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) /
[REQ-0004](../../01.requirements/0004-current-local-gitops-platform.md) and [AD-0006](../descriptions/0006-workspace-agent-governance-platform.md) /
[AD-0007](../descriptions/0007-current-local-gitops-platform.md). This reference maintenance changes no lifecycle
status, decision supersession, package location, or execution completion claim.

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
- **Original program**: [Historical PRD-005](../../98.archive/superseded/01.requirements/0005-workspace-document-assurance-modernization.md)
- **Original architecture**: [Historical ARD-0008](../../98.archive/superseded/02.architecture/descriptions/0008-workspace-document-assurance-operating-model.md)
- **Follow-up**: [Spec 033](../../98.archive/completed/03.specs/0033-template-lifecycle-contract-normalization/spec.md)
- **New program**: [Historical PRD-006](../../98.archive/superseded/01.requirements/0006-workspace-document-lifecycle-and-evidence-consolidation.md)

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| ADR-0016 original program lineage | Complementary successor; original decision remains accepted | [Spec 034](../../98.archive/completed/03.specs/0034-authority-and-lineage-foundation/spec.md) |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Supersedes the permanent follow-up instance roster and validation-routing ownership; preserves this record's historical lineage context. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
