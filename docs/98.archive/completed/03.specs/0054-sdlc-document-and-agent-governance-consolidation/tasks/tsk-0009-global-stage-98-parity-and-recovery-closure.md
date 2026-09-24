---
title: "Task: Isolated Stage 98 archive minimization"
version: "1.0.1"
type: "sdlc/task"
status: "cancelled"
owner: "platform"
updated: "2026-09-03"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0009"
---

# Task: Isolated Stage 98 archive minimization

## Overview

This is the terminal queued Task record for WP-009.

Archive retention and archive removal answer different questions, and the
2026-09-03 measurement separates them. Whether a Migration stays is an
archive-internal value judgement; when it can leave is decided by the executable
references that still name it. `scripts/` and `tests/` name MIG-0010 and
MIG-0011 zero times and MIG-0012 once, so those are judged on value alone, while
MIG-0004 at thirty-five references, MIG-0002 at eighteen, and MIG-0005 at
sixteen cannot leave until their pins do. 172 distinct forty-hex pins remain in
`scripts/`.

**Cancellation (2026-09-16).** This record was written against the ADR-0032 and ADR-0038 record forms that ADR-0039 has since frozen, and its concrete instructions name a `docs/98.archive/tombstones/` directory that does not exist in this tree. Its one surviving invariant, that no current authority cites a sealed record, is now decided by the registry's ordered citation table rather than by this work item. Nothing executable remains, so it is cancelled. It was moved out of `queued` only because the task domain routes every terminal disposition through `in-progress`; no work was started.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-009 execution boundary](../plan.md#wp-009--global-stage-98-parity-and-recovery-closure)

## Task Table

**Plan label:** WP-009

**Depends on:** WP-013

**Current state:** `queued`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-009 | VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Minimize the isolated historical Archive after active citations and cross-links are zero, without count, current-consumer, branch, or current-state SHA gates. | platform | Cancelled | Not executed. | Zero inbound active links, minimal safety/readability checks, Git recovery, and logical commit |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
without exception. WP-009's sealed-history and recovery boundaries, reviews,
rollback, and logical commit are owned by its linked Plan section.

## Verification Summary

WP-009 is queued and has no accepted execution evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-009](../plan.md#wp-009--global-stage-98-parity-and-recovery-closure) | Queued. | No accepted execution evidence yet. |
