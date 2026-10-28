---
title: "Archive Final Units"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0134-TSK-0001"
parent_ids: ["SPEC-0134-PLAN-0001"]
---

# Task: Archive Final Units

## Overview

Move SPEC-0080 to Git history after its test readers move, and record a
`usable` assessment with a reason for the eight units that stay.
It executes [SPEC-0134](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown). This Task is the Decision document
that the nine Retention Assessment rows name.

## Inputs

- Request: on 2026-10-28 the operator chose to move SPEC-0080 and SPEC-0103
  and to record `usable` for the other seven remaining units.
- Change during implementation: staged QA failed when the SPEC-0105 Task 0003
  Inputs link to SPEC-0103 was edited, because that Task uses an older form that
  the current validators reject on any change. SPEC-0103 therefore stays, with
  a `usable` row, and Spec 0.1.1 records the narrower scope.
- Start: main `480ec7eb`, branch `docs/archive-final-units`.

### Kept Units

| Unit | Assessment | Reason it stays |
| --- | --- | --- |
| ADR-0032 | usable | Three frozen migration ledgers resolve a link through its retained body; frozen records are not rewritten |
| SPEC-0004 | usable | REQ-0001, ADR-0011 and AD-0004 cite it as Argo Rollouts delivery evidence |
| SPEC-0005 | usable | REQ-0002, ADR-0012, AD-0005 and RUN-0004 cite it as Argo Notifications delivery evidence |
| SPEC-0008 | usable | REQ-0004, AD-0007 and the platform ADRs cite it as local GitOps platform delivery evidence |
| SPEC-0054 | usable | 48 Markdown links outside Stage 98 cite it as the governance convergence record |
| SPEC-0072 | usable | REQ-0003 names it as the trace owner of FR-0011 and acceptance criterion 09 |
| SPEC-0103 | usable | The SPEC-0105 Task 0003 Inputs link to its Task 0006, and that older-form Task cannot be edited |
| SPEC-0104 | usable | REQ-0004 FR-0008 and FR-0010 and AD-0007 cite its Tasks as acceptance evidence |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AF-001](../spec.md#success-criteria--verification-plan) | Move the test reads and link of SPEC-0080 | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-AF-002](../spec.md#success-criteria--verification-plan) | Isolated recovery of SPEC-0080 | platform | in-progress | PASS | EVD-005 closes EVD-002 |
| WORK-003 | [VAL-AF-003](../spec.md#success-criteria--verification-plan) | Remove SPEC-0080 and record the nine assessment rows | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-AF-004](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AF-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Test runs and link search | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AF-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AF-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Validators and staged QA | Exact disposition index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AF-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-AF-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Isolated recovery | Base `cfe3fdb6`: `git rev-parse` of the SPEC-0080 tree against its envelope tree, then `git archive` of the envelope into a scratch directory | PASS | Equal tree; restored 3 files, matching the current tree | yes | EVD-002 |
| EVD-006 | [VAL-AF-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Test runs and link search | PR #189 independent review of `7142c6a8` | FAIL | The pinned read in `test_task_acceptance_contract` decoded with the locale encoding instead of UTF-8, and the SPEC-0054 reason cited 78 links where 48 Markdown links exist outside Stage 98 | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AF-001](../spec.md#success-criteria--verification-plan) | pending | none | Test and link moves remain | platform |
| [VAL-AF-002](../spec.md#success-criteria--verification-plan) | pending | none | Recovery remains | platform |
| [VAL-AF-003](../spec.md#success-criteria--verification-plan) | pending | none | Removal and rows remain | platform |
| [VAL-AF-004](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index, REQ-0003, the
  `tests/test_archive_disposition_lifecycle.py`,
  `tests/test_task_acceptance_contract.py`, the SPEC-0080 directory and the
  Retention Assessment table in `docs/98.archive/README.md`.
- **Forbidden Paths**: the eight kept units, the SPEC-0105 Tasks, frozen Archive records, catalog
  rows and envelopes, validators, the registry and Task evidence rows.
- **Approval Required**: the operator decided on 2026-10-28 (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each exact index.
- **Live Validation**: not applicable.
- **Secret / Vault Handling**: no secret-bearing content is read or printed.
- **Rollback Plan**: availability never returns to `retained` (ADR-0040);
  content is recovered with `git archive <envelope commit> <original path>`.
  The test, link and row changes revert with the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
