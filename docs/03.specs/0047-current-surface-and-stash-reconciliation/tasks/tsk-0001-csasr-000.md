---
title: "VAL-CSASR-001, VAL-CSASR-009"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-08-07"
layer: "specs"
artifact_id: "SPEC-0047-TSK-0001"
---

# SPEC-0047-TSK-0001: VAL-CSASR-001, VAL-CSASR-009

## Overview

Append-only Task record for legacy work item `CSASR-000` from the package's
decomposed monolithic ledger. The exact row below preserves its criterion,
dependency, owner, result, and evidence.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-000 | VAL-CSASR-001, VAL-CSASR-009 | Activate PRD-0007 lineage and reciprocal Spec/Plan/Task path | platform | In Progress | Exact activation set is under validation; activation SHA is not preclaimed | Program registry, projection validator, indexes, staged lifecycle, and activation commit |

## Approval and Safety Boundaries

The shared approval, safety, and rollback contract is preserved once in the
[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This
record does not broaden that contract.

## Verification Summary

The row-specific validation/result/evidence is preserved verbatim above. The
shared verification context is in the
[owning Plan](../plan.md#legacy-task-verification-evidence).

## Traceability

- Stable Task: `SPEC-0047-TSK-0001`
- Legacy work item: `CSASR-000`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| N/A — legacy work item `CSASR-000` | Preserved legacy status; current Task is `in-progress`. | Row-specific result and evidence remain in the Task Table above. |

- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
