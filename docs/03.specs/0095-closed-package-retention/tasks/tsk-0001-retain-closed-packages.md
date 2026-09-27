---
title: "Retain Closed Packages"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0095-TSK-0001"
---

# Task: Retain Closed Packages

## Overview

Execute [SPEC-0095-PLAN-0001](../plan.md). The request owner approved
archiving the finished packages on 2026-09-27 (chooser: request owner; choice:
"move to the archive together"). SPEC-0094 deferred SPEC-0086 to this round.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- [Archive Index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-CPR-001 | Record the approval and survey each unit | platform | Done | Two units surveyed; see the survey below | This Task |
| WORK-002 | VAL-CPR-002, VAL-CPR-003 | Retain both packages in `completed/` | platform | Queued | Pending the move commit | Staged QA and archive gates |
| WORK-003 | VAL-CPR-003 | Record the results and close this package | platform | Queued | Pending | Staged QA |

## Approval and Safety Boundaries

- **Allowed Paths**: SPEC-0086 and SPEC-0094 as whole units, `docs/98.archive/README.md`, the current documents and provider notes that cite them, and this package
- **Forbidden Paths**: the content of any retained body, frozen record, or sealed ledger; the Stage 99 registry; live credentials and cluster state
- **Approval Required**: the request owner approved the dispositions. Push, pull request, and merge stay with the request owner.
- **Static Validation**: `python3 scripts/qa.py staged` per commit, plus the archive contract tests and the archive cutover gate on the move
- **Live Validation**: none; no live system is involved
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the move commit; Git restores every original path
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-27)

| Unit | Members | Class | Current consumers |
| --- | --- | --- | --- |
| SPEC-0086 | Spec, Plan, and one Task done | `completed` | REQ-0003, `.claude/provider.md`, `.codex/provider.md`, the Stage 03 index |
| SPEC-0094 | Spec, Plan, and one Task done | `completed` | REQ-0003, the Stage 03 index |

## Traceability

- Stable Task: `SPEC-0095-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Survey above |
| [WORK-002](../plan.md#work-breakdown) | Queued | Pending the move commit |
| [WORK-003](../plan.md#work-breakdown) | Queued | Pending |
