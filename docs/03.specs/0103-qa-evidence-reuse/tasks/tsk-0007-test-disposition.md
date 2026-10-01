---
title: "Active QA test disposition"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-01"
layer: "specs"
artifact_id: "SPEC-0103-TSK-0007"
---

# Task: Active QA test disposition

## Overview

Execute [Plan WP-007](../plan.md) against [SPEC-0103](../spec.md). The later user request extends the active CI/QA/validation cleanup to invoked and discovered tests. No test retirement is claimed yet.

## Inputs

- [Plan](../plan.md), [Spec](../spec.md), and the [quality policy](../../../../.agents/governance/quality.md).
- Criterion: VAL-QER-012. The registry's `unit-tests` command discovers the active test suite.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-007 | VAL-QER-012 | Trace active test callers and distinct failure meanings; retire proven redundant or obsolete tests | platform | Queued | Not executed | This record; fill inventory, commits, counts, and reviewer. |

## Approval and Safety Boundaries

- **Allowed Paths**: directly affected `tests/` modules and fixtures, their CI/QA callers when behavior transfer or obsolete-contract proof is recorded, `.agents/governance/quality.md` for the retirement rule, and this Task record.
- **Forbidden Paths**: private credentials, global hooks, live Kubernetes/Vault mutation, archived Spec bodies.
- **Approval Required**: no external setting mutation in this Task; delivery actions follow the Plan's existing boundary.
- **Static Validation**: baseline and final `unittest` discovery counts, retained negative checks or obsolete-contract evidence for retirements, `python3 scripts/qa.py quick`, exact-index `staged` when required, and one full unit-test aggregate for final changed inputs.
- **Live Validation**: hosted CI remains separate evidence in Task 0006.
- **Secret / Vault Handling**: no secret values in evidence.
- **Rollback Plan**: restore a retired test and its caller if the retained negative check or aggregate coverage regresses.
- **Evidence Location**: this Task record with the one-time disposition table and exact commands/results; no permanent duplicate registry.

## Verification Summary

Queued. Inspect active test modules, direct standalone tests, fixtures, and imports before changing code. Record each candidate's distinct failure meaning and a keep/consolidate/retire decision. No test is deleted merely because it is old, large, or labelled one-off. A retired still-required behavior needs a retained negative check; a genuinely obsolete test needs evidence that its caller and requirement no longer exist.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-007](../plan.md#work-breakdown) | Queued | Plan Task 7; actual audit and validation pending. |
