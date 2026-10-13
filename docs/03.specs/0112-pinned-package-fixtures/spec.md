---
title: "Pinned Package Fixtures in Lifecycle Tests"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0112"
---

# Pinned Package Fixtures in Lifecycle Tests Technical Specification (Spec)

## Overview

[SPEC-0111](../0111-historical-fixture-drift/spec.md) fixed five tests that
broke when later Tasks edited documents those tests read from the working
tree. Its review found three more tests that still read completed package
documents from the working tree. They pass today, but an ordinary edit or
the archiving of SPEC-0105, SPEC-0106 or SPEC-0107 would break them
without any code defect. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-pinned-package-fixtures.md) records it.

## Strategic Boundaries & Non-goals

- In scope: the SPEC-0105 Task, Spec and Plan read in
  `tests/test_task_acceptance_contract.py` (task-item edge test); the
  SPEC-0106 `tsk-0016` read in `ExactLegacyTaskBindingTests`; the SPEC-0107
  `tsk-0004` read in `OptionalMultiRowStatusTests` in
  `tests/test_task_execution_contract.py`.
- Non-goals: reads of the live Registry, schema and templates, which follow
  the current contract by design; any validator or document change.

## Contracts

- These three tests read package documents from a pinned Git object.
- `ExactLegacyTaskBindingTests` reads `tsk-0016` from
  `TASK_LEGACY_BASELINE_COMMIT`, so it still proves that only the exact
  baseline bytes keep the previous form.
- No assertion is removed or loosened.

## Core Design

The two package snapshots are read from main `bceca1b7`, where SPEC-0105
and SPEC-0107 are complete. The legacy test imports the baseline commit
constant from `document_contracts` instead of repeating it.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

- `FIXTURE_SNAPSHOT` in each test module: the pinned commit.

## Edge Cases & Error Handling

A pinned path that does not exist at the commit makes `git show` fail, so
a wrong pin fails loudly.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert of the test commit.

## Verification Commands

- In a scratch clone, move the three packages as an archive would and run
  the affected tests before and after the change.
- `python3 -m unittest tests.test_task_acceptance_contract tests.test_task_execution_contract`
  from the documented validation environment.
- `"$VALIDATION_VENV/bin/python" scripts/qa.py staged` per logical commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-PIN-001 | With the three packages moved in a scratch clone, the affected tests fail before the change and pass after it; in the repository both modules pass with no assertion removed. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PIN-001 | Deterministic tests independent of later document edits; focused tests. |
