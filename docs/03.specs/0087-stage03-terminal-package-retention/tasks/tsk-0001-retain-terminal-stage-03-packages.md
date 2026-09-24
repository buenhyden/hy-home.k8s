---
title: "Retain Terminal Stage 03 Packages"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0087-TSK-0001"
---

# Task: Retain Terminal Stage 03 Packages

## Overview

Execute [SPEC-0087-PLAN-0001](../plan.md). The request owner approved the
disposition of all seven units on 2026-09-24 (chooser: request owner; choice:
"Approve archive, separate package"), after approving the withdrawals of
SPEC-0047 and SPEC-0050 the same day.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- [Archive Index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-STR-001 | Record the approval and survey each unit | platform | Done | Seven units surveyed; see the survey below | This Task |
| WORK-002 | VAL-STR-002, VAL-STR-003 | Retain the four withdrawn packages in `retired/` | platform | In progress | Not yet merged | Lifecycle, link, and archive gates |
| WORK-003 | VAL-STR-005 | Rewrite the SPEC-0054 test pin and move the SPEC-0062 allowlist entry | platform | Queued | Not executed | Unit tests and the secret-scan gate |
| WORK-004 | VAL-STR-004 | Retain SPEC-0054, SPEC-0062, and SPEC-0084 in `completed/` | platform | Queued | Not executed | Lifecycle, link, and archive gates |
| WORK-005 | VAL-STR-006 | Record the results and close this package | platform | Queued | Not executed | Staged QA and hosted CI |

## Approval and Safety Boundaries

- **Allowed Paths**: the seven packages as whole units, `docs/98.archive/`, the current documents that cite them, the SPEC-0054 test pin, the SPEC-0062 allowlist entry and its test, and this package
- **Forbidden Paths**: the content of any retained body, frozen record, or sealed ledger; the Stage 99 registry; live credentials and cluster state
- **Approval Required**: the request owner approved the dispositions, and the push-and-merge route for pull requests whose hosted `qa` passes; any other external action needs its own approval
- **Static Validation**: the lifecycle, link, and archive gates and `python3 scripts/qa.py staged` per commit; hosted `qa` per pull request
- **Live Validation**: none; no live system is involved
- **Secret / Vault Handling**: the allowlist entry keeps its exact anchored form; no secret value is read
- **Rollback Plan**: revert the move commit; Git restores every original path
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-24)

| Unit | Anchor state | Members | Class | Current consumers |
| --- | --- | --- | --- | --- |
| SPEC-0047 | `withdrawn` | Plan withdrawn; TSK-0001 done; TSK-0002 to TSK-0006 cancelled | `retired` | REQ-0003, REQ-0004, AD-0007, the AD index, the Stage 03 index |
| SPEC-0048 | `withdrawn` | Plan withdrawn; six Tasks cancelled | `retired` | REQ-0003, REQ-0004, AD-0007, SPEC-0049, the Stage 03 index |
| SPEC-0050 | `withdrawn` | Plan withdrawn; seven Tasks cancelled | `retired` | REQ-0003, REQ-0004, AD-0007, SPEC-0049, the Stage 03 index |
| SPEC-0051 | `withdrawn` | Plan withdrawn; six Tasks cancelled | `retired` | REQ-0003, REQ-0004, AD-0007, the Stage 03 index |
| SPEC-0054 | `done` | Plan done; thirteen Tasks done, one cancelled | `completed` | ADR-0030, ADR-0031, ADR-0033, AD-0006, REQ-0003, two Stage 05 documents, the test pin |
| SPEC-0062 | `done` | Plan done; eight Tasks done, three cancelled | `completed` | The secret-scan allowlist and its test, one research memo |
| SPEC-0084 | `done` | Plan done; one Task done | `completed` | REQ-0003, the current bodies of SPEC-0008, SPEC-0049 and SPEC-0072 |

The four withdrawn packages link to one another and to SPEC-0084 only inside
their own bodies, which freeze with them.

## Traceability

- Stable Task: `SPEC-0087-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Survey above |
| [WORK-002](../plan.md#work-breakdown) | In progress | Pending merge |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Queued |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Queued |
| [WORK-005](../plan.md#work-breakdown) | Not executed | Queued |
