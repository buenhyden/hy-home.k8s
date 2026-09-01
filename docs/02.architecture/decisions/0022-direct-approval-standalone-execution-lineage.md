---
title: 'ADR-0022: Direct-Approval Standalone Execution Lineage'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: superseded
owner: platform
updated: 2026-09-01
artifact_id: "ADR-0022"
superseded_by: ADR-0031
---

# ADR-0022: Direct-Approval Standalone Execution Lineage

## Overview

This accepted decision adds one closed, optional standalone-execution relation
to document profile registry schema v8. It records a directly human-approved
Spec, its exact Plan and Task, and their shared lifecycle without inventing a
PRD or ARD owner.

## Context

Spec 053 was approved directly by the human on 2026-08-08, while Spec 054 and
Spec 055 were approved directly on 2026-08-09, each with an explicit
no-separate-PRD/ARD boundary. The existing `programLineage` contract correctly requires
PRD/ARD-backed program membership and must remain unchanged, while the
unowned-active-component gate correctly rejects either active Plan/Task pair
without a separate typed owner.

## Decision

- Keep production registry schema version 8 and every existing
  `programLineage` invariant and diagnostic unchanged.
- Add the optional closed `standaloneExecutions` array. Absence declares no
  standalone relationship and does not relax the unowned component gate.
- Require exact Spec, Plan, Task, state, reason, accepted ADR, and
  `spec-body-record` approval-mode fields for each relation.
- Require unique, numerically sorted Spec identities; unique Plan and Task
  identities; and disjoint standalone and program Spec membership.
- Require tracked regular owners with the expected profiles, shared state,
  reciprocal Spec/ADR and Plan/Task links, direct Plan/Task links to only the
  owning Spec, and the exact declared active execution component.
- Preserve terminal standalone relations as valid archival eligibility
  lineage for their done Plan/Task pair without synthesizing PRD/ARD values.

## Explicit Non-goals

- Changing or weakening `programLineage` readiness, follow-up, historical,
  reciprocal, chronology, or execution-component semantics.
- Treating a prose conflict link as execution ownership.
- Allowing implicit approval, inferred Plan/Task paths, multiple approval
  modes, or unregistered active execution components.
- Creating a PRD or ARD solely to satisfy a machine relationship shape.

## Consequences

Spec 053, Spec 054, Spec 055, Spec 056, Spec 057, Spec 058, Spec 059, and Spec 060, with each exact Plan/Task pair, gain
deterministic registry ownership without a fabricated program component. Validators accept
an exact ISO-date direct-approval statement, reject invalid calendar dates,
missing approval fields, identity overlap, wrong owners or states, incomplete
reciprocal evidence, foreign-Spec links, and extra active component nodes.
Terminal standalone relations can support later archival eligibility without
false upstream authority.

## Alternatives

- **Add Spec 053 to PRD-0008/ARD-0011 `programLineage`**: rejected because the
  approved Spec explicitly treats those documents as conflicting inputs, not
  execution authority.
- **Create a new PRD and ARD**: rejected because it contradicts the approved
  no-separate-PRD/ARD lifecycle and adds documents only for schema compliance.
- **Exempt the WERPC paths from the unowned gate**: rejected because an
  untyped path exception would not preserve ownership, state, reciprocity, or
  terminal eligibility evidence.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| Direct human approval recorded in the Spec body | N/A — first typed standalone-execution relation; preserves ADR-0016/0017 program lineage semantics | [Spec 053](../../03.specs/0053-workspace-engineering-research-pack-consolidation/spec.md) |
| Direct human approval recorded in the Spec body | B-scope SDLC and AI-agent governance consolidation including Stage 90 | [Spec 054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |
| Direct human approval recorded in the Spec body | N/A — tenth typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 0062](../../03.specs/0062-workspace-research-full-corpus-reverification/spec.md) |
| Direct human approval recorded in the Spec body | N/A — eleventh typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 0063](../../03.specs/0063-governance-invariant-consolidation/spec.md) |
| Direct human approval recorded in the Spec body | N/A — twelfth typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 0064](../../03.specs/0064-agent-governance-surface-consolidation/spec.md) |
| Direct human approval recorded in the Spec body | N/A — thirteenth typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 0065](../../03.specs/0065-transition-residue-retirement/spec.md) |
| [ADR-0031](./0031-current-corpus-retention-and-validation-ownership.md) | Supersedes permanent standalone instance-roster authority with package-local execution ownership; preserves direct human approval as historical context. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

Specs 0055 through 0061 were executed under this same direct-approval semantics,
each with the approval recorded in its own Spec body, and are named here without
links because the registry does not declare them as relations. Their Plans route
Tasks through a README index rather than linking them, which the reciprocity half
of the relation contract requires, and Plan, Task and Spec are all terminal, so
the shape cannot be corrected. A linked Spec above is a declared relation, which
`STANDALONE-DECISION-ROSTER` holds equal to the registry; naming these seven
without links records the execution without asserting a relation the registry
cannot hold.
