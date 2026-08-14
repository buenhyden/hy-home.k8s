---
title: 'ADR-0022: Direct-Approval Standalone Execution Lineage'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-08-12
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

Spec 053, Spec 054, Spec 055, Spec 056, and Spec 057, with each exact Plan/Task pair, gain
deterministic registry ownership without a fabricated program component. Validators accept
an exact ISO-date direct-approval statement, reject invalid calendar dates,
missing approval fields, identity overlap, wrong owners or states, incomplete
reciprocal evidence, foreign-Spec links, and extra active component nodes.
Terminal standalone relations can support later archival eligibility without
false upstream authority.

## Alternatives

- **Add Spec 053 to PRD-008/ARD-0011 `programLineage`**: rejected because the
  approved Spec explicitly treats those documents as conflicting inputs, not
  execution authority.
- **Create a new PRD and ARD**: rejected because it contradicts the approved
  no-separate-PRD/ARD lifecycle and adds documents only for schema compliance.
- **Exempt the WERPC paths from the unowned gate**: rejected because an
  untyped path exception would not preserve ownership, state, reciprocity, or
  terminal eligibility evidence.

## Traceability

### Lifecycle Traceability

| Decision lineage                                | Replacement relation                                                                                      | Affected Spec                                                                                  |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Direct human approval recorded in the Spec body | N/A — first typed standalone-execution relation; preserves ADR-0016/0017 program lineage semantics        | [Spec 053](../../03.specs/053-workspace-engineering-research-pack-consolidation/spec.md)       |
| Direct human approval recorded in the Spec body | N/A — second typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 054](../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)              |
| Direct human approval recorded in the Spec body | N/A — third typed standalone-execution relation; reuses the same closed approval and ownership semantics  | [Spec 055](../../03.specs/055-workspace-engineering-gap-only-refresh/spec.md)                  |
| Direct human approval recorded in the Spec body | N/A — fourth typed standalone-execution relation; reuses the same closed approval and ownership semantics | [Spec 056](../../03.specs/056-workspace-engineering-partial-defer-incremental-refresh/spec.md) |
| Direct human approval recorded in the Spec body | N/A — fifth typed standalone-execution relation; reuses the same closed approval and ownership semantics  | [Spec 057](../../03.specs/057-workspace-research-consistency-and-partial-refresh/spec.md)      |
