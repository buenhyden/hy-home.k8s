---
title: "Retain Closed Packages"
version: "0.2.0"
type: "sdlc/task"
status: "done"
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
| WORK-002 | VAL-CPR-002, VAL-CPR-003 | Retain both packages in `completed/` | platform | Done | Two units retained with catalog rows naming `576a8927`; commit `a6809725` | [Retention](#retention-2026-09-27) |
| WORK-003 | VAL-CPR-003 | Record the results and close this package | platform | Done | Staged QA and the archive gates passed; hosted `qa` pending the pull request | [Retention](#retention-2026-09-27) |

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

### Retention (2026-09-27)

- **Envelope**: `576a8927`, the PR #102 merge on the default branch.
- **Move**: commit `a6809725`, 6 pure renames into `completed/03.specs/`, with the
  catalog rows, the repointed REQ-0003 links, and the provider-note path spans
  in the same commit.
- **Validation**: every commit passed `python3 scripts/qa.py staged`.
  `python3 scripts/run-archive-contract-tests.py --root .` passed 136 tests, and
  `python3 scripts/archive_cutover.py --root .` passed
  (`records=25 historical_links=198 secret_clean=25`) with a local Gitleaks
  build on the path. The archive report's Git budget test passed on a branch
  checkout.
- **Residual**: SPEC-0008 is the only package left in Stage 03 apart from this
  one, and it stays `active` by design. The two SPEC-0086 findings, the Claude
  projections that declare `Grep` and `Glob` and the undiscovered Codex role
  projections, keep the owners that the retained SPEC-0086 Task names.

## Traceability

- Stable Task: `SPEC-0095-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Survey above |
| [WORK-002](../plan.md#work-breakdown) | Done | Commit `a6809725` |
| [WORK-003](../plan.md#work-breakdown) | Done | Local results below |
