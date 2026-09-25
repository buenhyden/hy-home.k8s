---
title: "Retire SPEC-0049"
version: "0.3.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0090-TSK-0001"
---

# Task: Retire SPEC-0049

## Overview

Execute [SPEC-0090-PLAN-0001](../plan.md). The request owner approved the move
of SPEC-0049 and the push of the resulting commits on 2026-09-25.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- [Archive Index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SRT-001 | Record the approval and survey the unit | platform | Done | Survey below | This Task |
| WORK-002 | VAL-SRT-002, VAL-SRT-003 | Retain SPEC-0049 in `retired/` | platform | Done | Unit retained in `retired/03.specs/` with a catalog row naming `62ed8f05`; current links rewritten in the same commit | Lifecycle, link, and archive gates |
| WORK-003 | VAL-SRT-004 | Record the results and close | platform | Done | Results below | Staged QA |

## Approval and Safety Boundaries

- **Allowed Paths**: the SPEC-0049 package as a whole unit, `docs/98.archive/README.md`, the current documents that link to it, and this package
- **Forbidden Paths**: the content of any retained body, frozen record, or sealed ledger; the Stage 99 registry; live credentials and cluster state
- **Approval Required**: the request owner approved the move and the push; any other external action needs its own approval
- **Static Validation**: the lifecycle, link, and archive gates and `python3 scripts/qa.py staged` per commit
- **Live Validation**: none; no live system is involved
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the move commit; Git restores the original path
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-25)

| Unit | Anchor state | Members | Class | Current consumers |
| --- | --- | --- | --- | --- |
| SPEC-0049 | `withdrawn` | Plan withdrawn; seven Tasks cancelled | `retired` | REQ-0003, REQ-0004, AD-0007, the AD index, the Stage 03 index |

The envelope is `62ed8f05`, the commit in which every member reached its
terminal state.

### Results

| Commit | Scope |
| --- | --- |
| `7ddecc1b` | Propose this package; pushed with the envelope `62ed8f05` by the request owner |
| `8e405331` | Retain SPEC-0049 in `retired/03.specs/`, add its catalog row, and rewrite its current links |
| Closing commit | Record these results and close |

- **Staged QA**: every selected gate passed for each commit.
- **Archive gate**: the Retention Catalog envelope check returned no
  diagnostic, so every row, including `62ed8f05`, equals its object and is
  reachable from `origin/main`. `archive_cutover.py` as a whole still fails
  on this host because Gitleaks is absent, with the same output as before the
  move. The archive contract suite passed 136 tests.
- **Hosted `ci-summary`**: DEFER; not observed.
- **Rollback**: revert `8e405331`; Git restores the original path.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Survey recorded | This Task |
| [WORK-002](../plan.md#work-breakdown) | Unit retained | Lifecycle, link, and archive gates |
| [WORK-003](../plan.md#work-breakdown) | Package closed | Results above |
