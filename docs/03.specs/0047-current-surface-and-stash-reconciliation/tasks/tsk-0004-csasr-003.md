---
title: "VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007"
version: "1.0.2"
type: "sdlc/task"
status: "cancelled"
owner: "platform"
updated: "2026-09-10"
layer: "specs"
artifact_id: "SPEC-0047-TSK-0004"
---

# SPEC-0047-TSK-0004: VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007

## Overview

Append-only Task record for legacy work item `CSASR-003` from the package's
decomposed monolithic ledger. The exact row below preserves its criterion,
dependency, owner, result, and evidence.

**Cancellation (2026-09-24).** This record is cancelled because its owning Spec is withdrawn, not on a finding of its own. The request owner approved withdrawing SPEC-0047 on 2026-09-24 (chooser: request owner; choice: "0047: Withdraw"), so this Task has no scope left to execute: `git stash list` is empty and stash object `6370311e020620cc2743005896cc88db97d15465` is unreachable, so the reconciliation obligation this Task existed to discharge no longer has a subject. The record was never executed, so nothing is discarded. It left `queued` only because the task domain routes every terminal disposition through `in-progress`; no work was started.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- Migration recovery ledger MIG-0004, through the [archive index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-003 | VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007 | Record tracked stash hunk categories without applying or dropping stash | platform | Cancelled | Not executed | Full stash object/parent metadata, tracked path list, hunk categories, destination owner, and review |

## Approval and Safety Boundaries

The shared approval, safety, and rollback contract is preserved once in the
[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This
record does not broaden that contract.

## Verification Summary

The row-specific validation/result/evidence is preserved verbatim above. The
shared verification context is in the
[owning Plan](../plan.md#legacy-task-verification-evidence).

## Traceability

- Stable Task: `SPEC-0047-TSK-0004`
- Legacy work item: `CSASR-003`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| N/A — legacy work item `CSASR-003` | Cancelled (2026-09-24): the owning Spec is withdrawn. | Row-specific result and evidence remain in the Task Table above. |

- Legacy bytes: MIG-0004, through the [archive index](../../../98.archive/README.md)
