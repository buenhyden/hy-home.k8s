---
title: 'Task: Responsibility topology and compatibility cutover'
type: sdlc/task
status: in-progress
owner: platform
updated: 2026-09-01
artifact_id: "SPEC-0054-TSK-0011"
---

# Task: Responsibility topology and compatibility cutover

## Overview

This is the sole active parent acceptance-owner record for delegated WP-011.
It reviews integrated results and never executes or claims Spec 0066's
delegated implementation.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-011 execution boundary](../plan.md#wp-011--responsibility-topology-and-compatibility-cutover)
- [Accepted ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)

## Task Table

**Plan label:** WP-011

**Depends on:** the SPEC-0054-TSK-0010 activation transaction

**Current state:** `in-progress; delegated implementation accepted, awaiting the later parent handoff`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-011 | VAL-SDLC-010..VAL-SDLC-012 | Review the delegated responsibility-topology and compatibility evidence, then record Spec 0054 integrated acceptance without executing the delegated changes. | platform | Done | Spec 0054 integrated acceptance is recorded. The delegated result establishes one routing owner, one owner per semantic rule, a dispatch-only aggregate, and consumer-zero retirement, with every review finding remediated before commit. | Committed `fa3d5a9d` and the isolated `913f284b`; SPEC-0066-TSK-0001 review, disposition, and ordered lane evidence; accepted ADR-0031 |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. Spec 0066 owns WP-011's responsibility graph,
consumer-zero retirement, reviews, rollback, and ordered implementation
commits. This Task owns only the parent acceptance checklist and record.
Activating this acceptance owner does not satisfy or bypass the delegated Spec
0066 WP-011 dependency on its own WP-010.

## Verification Summary

Direct human approval on 2026-08-31 selected Spec 0066 as the delegated
execution package. SPEC-0054-TSK-0010 completed the parent activation transaction:
Spec 0066 Spec/Plan are `active`, SPEC-0066-TSK-0001 is `in-progress`, this Task is
the sole `in-progress` parent acceptance owner, and the existing Spec 0054
compatibility pointer names this Task. Spec 0066 has no standalone row.

The delegated evidence is committed and reviewed, and the parent checklist
passes, so Spec 0054 integrated acceptance is recorded here. Acceptance rests
on the delegated Task's own record: the validation registry has one owner under
`scripts/validation/`, each semantic rule and residual repository contract names
a single production owner, the aggregate shell dispatches without embedding a
rule, transitional wrappers and current-state digests are retired with consumer
and recovery proof, and the required external `agent-governance-static` check
name is unchanged. Independent review and complete execution raised five
defects, including a hosted-CI discovery failure and a provider post-validate
fixture gap, and all were remediated before the implementation commit. This
Task remains `in-progress` while Spec 0066 performs its state-only closure. A later parent handoff moves this Task to `done` and the compatibility
pointer to queued SPEC-0054-TSK-0013 atomically; SPEC-0054-TSK-0013 activates only in a
subsequent legal transition. Rejected evidence returns to Spec 0066 without
changing ownership or claiming implementation here. The retired `route_state`
option is not reintroduced.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-011](../plan.md#wp-011--responsibility-topology-and-compatibility-cutover) | Done; parent acceptance recorded for the committed delegated result. | Committed `fa3d5a9d`, `SPEC-0066-TSK-0001` review and lane evidence, [Current Spec Index](../../README.md#current-spec-index), and accepted [ADR-0031](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md) |
