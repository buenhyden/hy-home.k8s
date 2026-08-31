---
title: 'Task: Script, gate, fixture, and SHA ownership fixed point'
type: sdlc/task
status: queued
owner: platform
updated: 2026-08-31
artifact_id: "TSK-0054-0010"
---

# Task: Script, gate, fixture, and SHA ownership fixed point

## Overview

This is the queued parent activation-owner record for WP-010. After WP-006 and
WP-008 complete, the active owner hands off to this Task as the sole
`in-progress` Task in a separate lifecycle-valid change. This Task then owns
only the exact-index activation and delegated-state transfer; it does not
execute the validation-tooling implementation delegated to Spec 0066.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-010 execution boundary](../plan.md#wp-010--script-gate-fixture-and-sha-ownership-fixed-point)
- [Proposed ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)

## Task Table

**Plan label:** WP-010

**Depends on:** WP-006 and WP-008

**Current state:** `queued; transfer to Spec 0066 designed but not activated`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-010 | VAL-SDLC-010..VAL-SDLC-012 | Own the reviewed ADR/lifecycle activation index, establish package-local delegated-component validation, and transfer WP-010/WP-011 execution to Spec 0066 without executing the delegated tooling work. | platform | Queued | Delegation transfer designed; no execution accepted. | Exact-index activation gates, focused delegated-ownership tests, legal state transitions, parent compatibility-pointer rotations, and transfer relation to `TSK-0066-0001` |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. This Task's future active scope is limited to the activation
transaction defined by the linked Plan section. Spec 0066 owns the later
machine-ownership audit, cleanup, reviews, rollback, and logical commits.

## Verification Summary

Direct human approval on 2026-08-31 selected Spec 0066 at
`../../0066-validation-tooling-ownership/spec.md` as the delegated execution
package, with `TSK-0066-0001` as its queued execution record. Cross-package
navigation remains in the [Current Spec Index](../../README.md#current-spec-index).
Spec 0054 retains integration acceptance; Spec 0066 owns the detailed execution
and evidence after activation. This record remains `queued` during the design
checkpoint and has no accepted execution evidence.

After the written design and implementation plan are reviewed and WP-006 and
WP-008 are complete, this Task first becomes the sole `in-progress`
parent Task through a separate lifecycle-valid handoff. The same handoff moves
the existing Spec 0054 `standaloneExecutions` task pointer to this Task. It then
owns the activation transaction that accepts ADR-0031, moves all five named
predecessors to `superseded` with reciprocal relations, updates the Decisions
README and current `Proposed ADR-0031` labels, updates the Spec 0066 router and
Current Spec Index to active execution, adds the narrow package-local delegated
ownership rule and focused positive/negative tests, changes Spec 0066 Spec/Plan
to `active`, changes its first Task to `in-progress`, moves the parent
compatibility pointer to TSK-0054-0011, changes this Task from `in-progress` to
`done`, and changes TSK-0054-0011 from `queued` to `in-progress` as the sole
parent acceptance owner. The index verifies that child Plan/Task execution
links remain inside Spec 0066 and creates no child standalone row. All Task
transitions already exist in the Stage 99 lifecycle domain. The retired
`route_state` option is not reintroduced.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-010](../plan.md#wp-010--script-gate-fixture-and-sha-ownership-fixed-point) | Queued; transfer pending activation. | `TSK-0066-0001`, [Current Spec Index](../../README.md#current-spec-index), and proposed [ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md) |
