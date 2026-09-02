---
title: "VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007"
version: "1.0.0"
type: sdlc/task
layer: "specs"
status: queued
owner: platform
updated: 2026-08-07
artifact_id: "SPEC-0047-TSK-0004"
---

# SPEC-0047-TSK-0004: VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007

## Overview

Append-only Task record for legacy work item `CSASR-003` from the package's
decomposed monolithic ledger. The exact row below preserves its criterion,
dependency, owner, result, and evidence.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-003 | VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007 | Record tracked stash hunk categories without applying or dropping stash | platform | Queued | Not executed | Full stash object/parent metadata, tracked path list, hunk categories, destination owner, and review |

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
| N/A — legacy work item `CSASR-003` | Preserved legacy status; current Task is `queued`. | Row-specific result and evidence remain in the Task Table above. |

- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
