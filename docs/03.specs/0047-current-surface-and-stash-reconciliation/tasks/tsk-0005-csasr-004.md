---
title: "VAL-CSASR-005"
version: "1.0.0"
type: sdlc/task
layer: "specs"
status: queued
owner: platform
updated: 2026-08-07
artifact_id: "SPEC-0047-TSK-0005"
---

# SPEC-0047-TSK-0005: VAL-CSASR-005

## Overview

Append-only Task record for legacy work item `CSASR-004` from the package's
decomposed monolithic ledger. The exact row below preserves its criterion,
dependency, owner, result, and evidence.

## Inputs

- [Package router](../README.md)
- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-004 | VAL-CSASR-005 | Regenerate only validator-proven stale derived evidence with current producer | platform | Queued | Not executed | Current generator command/result and residue validator evidence, or evidence-backed no-change |

## Approval and Safety Boundaries

The shared approval, safety, and rollback contract is preserved once in the
[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This
record does not broaden that contract.

## Verification Summary

The row-specific validation/result/evidence is preserved verbatim above. The
shared verification context is in the
[owning Plan](../plan.md#legacy-task-verification-evidence).

## Traceability

- Stable Task: `SPEC-0047-TSK-0005`
- Legacy work item: `CSASR-004`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| N/A — legacy work item `CSASR-004` | Preserved legacy status; current Task is `queued`. | Row-specific result and evidence remain in the Task Table above. |

- Package inventory: [README](../README.md#task-records)
- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
