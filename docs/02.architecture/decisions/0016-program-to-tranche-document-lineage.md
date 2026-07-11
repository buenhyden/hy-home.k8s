---
title: 'ADR-0016: Program-to-Tranche Document Lineage'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-12
---

# ADR-0016: Program-to-Tranche Document Lineage

## Overview

This decision defines numeric and semantic lineage for one program PRD that is
implemented through multiple dependent Specs.

## Context

The current lifecycle contract recommends matching PRD and Spec numbers for one
feature lineage and allocating each routed family from its own highest number.
The approved modernization is one program with seven independently reviewable
technical tranches. The next PRD number is `005`; the next Spec range is
`026` through `032`. Reusing an existing Spec number or creating seven duplicate
program PRDs would weaken either family uniqueness or product ownership.

## Decision

- Allocate the program PRD as `005`, the next PRD-family number.
- Allocate the seven tranche Specs as `026` through `032`, the next Spec-family
  numbers, in dependency order.
- Treat PRD 005 as the single product and success-metric owner for all seven
  tranche Specs.
- Require each tranche Spec to link PRD 005, ARD 0008, this ADR, its predecessor
  and successor where applicable, and its own Plan/Task evidence after creation.
- Record this as the explicit program-to-many-tranche exception to numeric
  equality; semantic body links are authoritative for this program.
- Preserve the default matching-number recommendation for ordinary one-PRD,
  one-Spec feature lineages.
- Add this relationship to the document registry and lifecycle support contract
  during Spec 026; do not add a universal lineage frontmatter key.

## Explicit Non-goals

- Renumbering historical PRDs or Specs.
- Allowing arbitrary numeric mismatches without an accepted lineage decision.
- Creating a new metadata identifier with no consuming validator.
- Combining the seven implementation contracts into one unreviewable Spec.

## Consequences

- **Positive**: Both routed families remain monotonic and unique; product intent
  has one owner; each tranche has an independent review and rollback boundary.
- **Trade-offs**: Lineage cannot be inferred from numeric equality alone for this
  program, so reciprocal body links and registry fixtures are mandatory.

## Alternatives

### Number the PRD 026

- Good: Numeric equality with the first tranche Spec.
- Bad: Violates next-number allocation in the PRD family and suggests the other
  six Specs have no program relationship.

### Create seven PRDs

- Good: One numeric match for every Spec.
- Bad: Duplicates one program's goals, risks, and success metrics across seven
  current owners.

### Create one program Spec

- Good: One-to-one number mapping is simple.
- Bad: Removes the approved independent tranche, review, commit, and rollback
  boundaries.

## Related Documents

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../requirements/0008-workspace-document-assurance-operating-model.md)
- **Related ADR**: [Declarative Document Contract Registry](./0015-declarative-document-contract-registry.md)
- **Specs**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md) through [Protected Surface and Supply Chain Hardening](../../03.specs/032-protected-surface-supply-chain-hardening/spec.md)
