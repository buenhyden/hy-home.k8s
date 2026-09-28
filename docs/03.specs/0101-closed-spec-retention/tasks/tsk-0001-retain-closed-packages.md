---
title: "Retain Closed Spec Packages"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0101-TSK-0001"
---

# Task: Retain Closed Spec Packages

## Overview

Execute [SPEC-0101-PLAN-0001](../plan.md). On 2026-09-28 the request owner
asked for SPEC-0098, SPEC-0099, and SPEC-0100 to be closed and then retained.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-CSP-001, VAL-CSP-002 | Retain the three packages | platform | Queued | Pending | This Task |
| WORK-002 | VAL-CSP-001 | Record the evidence and close | platform | Queued | Pending | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: the three packages as whole units, `docs/98.archive/README.md`, `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`, and this package
- **Forbidden Paths**: the content of any retained body or frozen record; credentials and cluster state
- **Approval Required**: the request owner asked for the retention. Push and merge stay with the request owner.
- **Static Validation**: `python3 scripts/qa.py staged`, the archive contract tests, and the archive cutover gate
- **Live Validation**: not applicable; the change is repository-static
- **Secret / Vault Handling**: no credential is read or recorded
- **Rollback Plan**: revert the move commit; Git restores every original path
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-28)

| Unit | Members | Class | Current consumers |
| --- | --- | --- | --- |
| SPEC-0098 | Spec, Plan, and one Task `completed` | `completed` | REQ-0003, the Stage 03 index |
| SPEC-0099 | Spec, Plan, and one Task `completed` | `completed` | the Stage 03 index |
| SPEC-0100 | Spec, Plan, and one Task `completed` | `completed` | REQ-0003, the Stage 03 index |

`tests/test_document_lifecycle_cumulative_history.py` names a SPEC-0099 path
only as a synthetic fixture string, so it needs no change.

## Traceability

- Stable Task: `SPEC-0101-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Pending | This Task |
| [WORK-002](../plan.md#work-breakdown) | Pending | This Task |
