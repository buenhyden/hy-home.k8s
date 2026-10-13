---
title: "Historical Fixture Drift in Lifecycle Tests"
version: "0.1.0"
type: "sdlc/spec"
status: "in-review"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0111"
---

# Historical Fixture Drift in Lifecycle Tests Technical Specification (Spec)

## Overview

Five lifecycle tests fail on main `07ef6b7e` and on every commit since
their fixtures drifted. `git bisect` places the breaks on two
documentation-only commits, so the validators are correct and the tests
read inputs that later Tasks legitimately changed. Consumers are the
lifecycle and acceptance test suites and any operator who runs them. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-historical-fixture-drift.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `tests/test_task_acceptance_contract.py`
  `ApprovedPackageRetentionTests` (two failures) and
  `tests/test_task_execution_contract.py` `GenerationAdmissionTests` (three
  failures); the stale SPEC-0109 sentence in the Stage 03 index.
- Non-goals: any change to `scripts/`, the Registry, templates or a
  recorded Task; weakening an assertion to make a test pass.

## Contracts

- A test that names a historical commit reads every document input from a
  pinned Git object, never from the working tree.
- Where the current contract has retired a historical form, the fixture
  projects that one input into the current form and a separate assertion
  keeps the retired transition rejected.

## Core Design

`ApprovedPackageRetentionTests` read the SPEC-0107 package from the
working tree; commit `2a9daeb7` added a second Task and changed the Plan,
so the synthetic successor scenario now meets `COMPLETION-ALLOCATION` and
`COMPLETION-ACCEPTANCE`. The fix reads those three files from
`2a27d98f`, the parent of that commit.

`GenerationAdmissionTests` replay the generation 9 to 10 boundary with the
current Registry. The SPEC-0106 Task at `MIGRATION_COMMIT` has an
eight-column table that the current contract accepts only as exact
completed baseline bytes (`legacy_task_profile`), so the replay reports
`TASK-ITEM-HIDE` and the cumulative history cannot prove creation
(`LIFECYCLE-CREATE`). The test's later step also moves the Spec
`in-progress` to `completed`, an edge the current Spec lifecycle no longer
declares. Pinning an older Registry was tried and fails, because the
current code depends on current Registry semantics. The fix projects that
one Task into the current seven- and nine-column tables in the fixture,
replaces the later step with the declared `in-progress` to `cancelled`
edge for the history and budget assertions, and adds an assertion that
`in-progress` to `completed` reports `LIFECYCLE-EDGE`.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

- `current_task_form(text: str) -> str` in the execution test module:
  drops the Task table `Acceptance` column and maps the evidence
  `Acceptance` column to `Required` (`no` for `not-required`, otherwise
  `yes`) and `Resolves` (`none`).
- `PACKAGE_SNAPSHOT` in the acceptance test module: the pinned commit.

## Edge Cases & Error Handling

A projection that leaves a malformed table makes the replay fail with
`TASK-ITEM-HIDE`, so a bad projection cannot pass silently.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert of the test commits.

## Verification Commands

- `python3 -m unittest tests.test_task_acceptance_contract tests.test_task_execution_contract`
  from the documented validation environment.
- `"$VALIDATION_VENV/bin/python" scripts/qa.py staged` per logical commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-FIXTURE-001 | `ApprovedPackageRetentionTests` fails before the pin and all 12 acceptance tests pass after it, with no assertion removed. |
| VAL-FIXTURE-002 | `GenerationAdmissionTests` fails before the projection and all six pass after it, and a new assertion shows the retired Spec `in-progress` to `completed` edge reports `LIFECYCLE-EDGE`. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FIXTURE-001 | Deterministic tests independent of later document edits; focused tests. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FIXTURE-002 | Deterministic negative test for the retired edge; focused tests. |
