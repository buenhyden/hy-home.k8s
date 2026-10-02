---
title: "Retain Closed Spec Packages"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
| WORK-001 | VAL-CSP-001, VAL-CSP-002 | Retain the three packages | platform | Done | Three units retained with catalog rows naming `4046bb71`; commit `4062c8b8` | [Retention](#retention-2026-09-28) |
| WORK-002 | VAL-CSP-001 | Record the evidence and close | platform | Done | Evidence recorded; package `completed` | [Retention](#retention-2026-09-28) |

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

### Retention (2026-09-28)

- **Envelope**: `4046bb7168e7f093bbfa34137e71dff4eb52adeb`, the PR #111 head.
  The default branch reaches it through merge `26aa38b9`, and this branch
  descends from it. The merge commit itself was not usable as the envelope,
  because the comparison base of this branch does not reach it; the lifecycle
  gate rejected it with `Retention Envelope names no object the comparison base
  reaches`. Each package tree at `4046bb71` equals its tree at `26aa38b9`.
- **Move**: commit `4062c8b8`, 9 pure renames into `completed/03.specs/`, with
  the three catalog rows, the Stage 03 index entries removed, and the two
  REQ-0003 links repointed in the same commit. Each moved tree has the same
  object ID as its envelope tree.
- **Validation**: `python3 scripts/qa.py staged` passed all six gates on every
  commit. `python3 scripts/run-archive-contract-tests.py --root .` passed 144
  tests, and `python3 scripts/archive_cutover.py --root .` passed
  (`records=25 historical_links=198 secret_clean=25`) with a local Gitleaks
  build on the path.
- **Residual**: SPEC-0008 stays `active` by design. This package is the only
  other one left in Stage 03, and a later round retains it.

## Traceability

- Stable Task: `SPEC-0101-TSK-0001`

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done | Commit `4062c8b8` |
| [WORK-002](../plan.md#work-breakdown) | Done | [Retention](#retention-2026-09-28) |
