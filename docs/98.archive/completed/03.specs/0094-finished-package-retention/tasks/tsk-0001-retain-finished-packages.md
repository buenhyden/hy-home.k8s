---
title: "Retain Finished Packages"
version: "0.2.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0094-TSK-0001"
---

# Task: Retain Finished Packages

## Overview

Execute [SPEC-0094-PLAN-0001](../plan.md). The request owner approved the
disposition of all eight units on 2026-09-27 (chooser: request owner; choice:
"move to the archive together").

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- [Archive Index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-FPR-001 | Record the approval and survey each unit | platform | Done | Eight units surveyed; see the survey below | This Task |
| WORK-002 | VAL-FPR-002, VAL-FPR-003 | Retain the eight packages in `completed/` | platform | Done | Eight units retained with catalog rows naming `fbcafca1`; commit `febf70f5` | [Retention](#retention-2026-09-27) |
| WORK-003 | VAL-FPR-004 | Record the results and close this package | platform | Done | Staged QA and the archive gates passed; hosted `qa` is handed to the request owner | [Retention](#retention-2026-09-27) |

## Approval and Safety Boundaries

- **Allowed Paths**: the eight packages as whole units, `docs/98.archive/README.md`, the current documents that cite them, the archive report budget test, and this package
- **Forbidden Paths**: the content of any retained body, frozen record, or sealed ledger; the Stage 99 registry; live credentials and cluster state
- **Approval Required**: the request owner approved the dispositions. Push, pull request, and merge stay with the request owner.
- **Static Validation**: the lifecycle, link, and archive gates and `python3 scripts/qa.py staged` per commit
- **Live Validation**: none; no live system is involved
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the move commit; Git restores every original path
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-27)

Every unit's anchor, Plan, and Tasks are `done`, so every unit's class is
`completed`.

| Unit | Members | Current consumers |
| --- | --- | --- |
| SPEC-0072 | Plan and five Tasks done | REQ-0003, AD-0006, SPEC-0086, the Stage 03 index |
| SPEC-0085 | Plan and two Tasks done | REQ-0003, ADR-0039, ADR-0040, the Stage 03 index |
| SPEC-0087 | Plan and one Task done | REQ-0003, REQ-0004, AD-0007, the Stage 03 index |
| SPEC-0088 | Plan and one Task done | REQ-0003, REQ-0004, the Stage 03 index |
| SPEC-0089 | Plan and one Task done | REQ-0003, REQ-0004, AD-0007, the Stage 03 index |
| SPEC-0090 | Plan and one Task done | REQ-0003, REQ-0004, AD-0007, the Stage 03 index |
| SPEC-0091 | Plan and one Task done | REQ-0003, SPEC-0008, the Stage 03 index |
| SPEC-0093 | Plan and one Task done | REQ-0003, the Stage 03 index |

Links between these packages stay inside bodies that freeze together. Links
from already retained or retired bodies are read at their envelope commits.

### Retention (2026-09-27)

- **Envelope**: `fbcafca1`, the default-branch tip this branch starts from.
  All eight package trees are byte-identical there.
- **Move**: commit `febf70f5`, 29 pure renames into `completed/03.specs/`, with the
  catalog rows and the repointed citations in the same commit.
- **Validation**: every commit passed `python3 scripts/qa.py staged`.
  `python3 scripts/run-archive-contract-tests.py --root .` passed 136 tests.
  `python3 scripts/archive_cutover.py --root .` passed
  (`records=25 historical_links=198 secret_clean=25`) with a local Gitleaks
  build on the path. The archive report's Git budget test passed unchanged on
  a branch checkout.
- **Full profile**: `python3 scripts/qa.py full` passed every gate except three.
  `archive-cutover` and two `unit-tests` cases failed only because Gitleaks is
  off the trusted path. `pre-commit` is also off that path. Two process and IO
  race cases (`test_escaped_descendant_is_failed_without_post_reap_group_signal`
  and `test_file_reader_rejects_changes_during_read`) also fail on the
  unchanged base tree, so they are environment findings, not results of this
  round.
- **Deferral**: SPEC-0086 closed in this branch, so its tree has no
  default-branch envelope yet. It is retained in a later round after merge.
  Next owner: the request owner.

## Traceability

- Stable Task: `SPEC-0094-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Survey above |
| [WORK-002](../plan.md#work-breakdown) | Done | Commit `febf70f5` |
| [WORK-003](../plan.md#work-breakdown) | Done | Local results below; hosted `qa` pending the pull request |
