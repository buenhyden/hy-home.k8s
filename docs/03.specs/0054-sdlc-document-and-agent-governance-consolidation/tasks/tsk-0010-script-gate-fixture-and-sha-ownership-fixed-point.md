---
title: 'Task: Script, gate, fixture, and SHA ownership fixed point'
type: sdlc/task
status: done
owner: platform
updated: 2026-09-01
artifact_id: "TSK-0054-0010"
---

# Task: Script, gate, fixture, and SHA ownership fixed point

## Overview

This is the completed parent activation-owner record for WP-010. It owns only
the exact-index activation and delegated-state transfer; it does not execute or
claim the validation-tooling implementation delegated to Spec 0066.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-010 execution boundary](../plan.md#wp-010--script-gate-fixture-and-sha-ownership-fixed-point)
- [Accepted ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)

## Task Table

**Plan label:** WP-010

**Depends on:** WP-006 and WP-008

**Current state:** `done; activation transaction complete`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-010 | VAL-SDLC-010..VAL-SDLC-012 | Own the reviewed ADR/lifecycle activation index, establish package-local delegated-component validation, and transfer WP-010/WP-011 execution to Spec 0066 without executing the delegated tooling work. | platform | Done | Accepted ADR-0031, reconciled its predecessor and scoped-amendment relations, established delegated-component validation, and transferred execution to active Spec 0066 while preserving parent acceptance ownership. No delegated tooling implementation is claimed. | WP-006 cutover commit `b8d35ff`; WP-008 cutover commit `124ef61`; exact-index activation gates; eight focused delegated-ownership cases; legal state transitions; parent compatibility-pointer rotation; transfer relation to `TSK-0066-0001` |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. This Task's completed scope is limited to the activation
transaction defined by the linked Plan section. Spec 0066 owns the subsequent
machine-ownership audit, cleanup, reviews, rollback, and logical commits.

## Verification Summary

Direct human approval on 2026-08-31 selected Spec 0066 as the delegated
execution package. The reviewed activation transaction accepted ADR-0031,
superseded its five named predecessors with reciprocal relations, recorded the
ADR-0030 scoped amendment, aligned current Stage 02/03 labels and indexes, and
added a package-local delegated-ownership gate. Eight focused cases cover the
valid component, complementary accepted ADRs, and rejection of missing
reciprocity, proposed-only authority, multiple parents, foreign Plan/Task
links, state mismatch, and duplicate child authority.

The same index activated Spec/Plan/Task 0066, moved the parent compatibility
pointer to TSK-0054-0011, completed this Task, and activated TSK-0054-0011 as
the sole parent acceptance owner. It created no Spec 0066 standalone row and
did not change the Stage 99 lifecycle domain, schema, or projection. Spec 0066
now owns detailed implementation and evidence; this Task claims none of that
work. The retired `route_state` option was not reintroduced.

Repository-static activation evidence:

- `python3 tests/test_delegated_execution_ownership.py`: 8 tests, PASS.
- `python3 tests/test_document_strict_cutover.py`: 45 tests, PASS.
- strict cross-document validation: PASS.
- staged lifecycle validation: PASS.
- Archive/Recovery regression: 112 tests, PASS.
- aggregate repository quality gates: PASS.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-010](../plan.md#wp-010--script-gate-fixture-and-sha-ownership-fixed-point) | Done; activation transaction complete. | Completed WP-006/WP-008 evidence, eight focused delegated-ownership cases, active `TSK-0066-0001`, [Current Spec Index](../../README.md#current-spec-index), and accepted [ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md) |
