---
title: "Pinned Package Fixtures in Lifecycle Tests"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0112-TSK-0001"
parent_ids: ["SPEC-0112-PLAN-0001"]
---

# Task: Pinned Package Fixtures in Lifecycle Tests

## Overview

Execute the single work unit of the [Plan](../plan.md) for
[SPEC-0112](../spec.md) and record its evidence here.

## Inputs

- [SPEC-0112](../spec.md) and its [Plan](../plan.md).
- Operator instruction on 2026-10-13 to continue with the SPEC-0111 review
  follow-up.
- Main `bceca1b7a495a4025291062e4b204f79ae2064c4`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | Pin the three package reads | platform | frontmatter | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Archive simulation, focused tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Archive simulation, focused tests and staged QA | Scratch clone at `918ed00f` with the SPEC-0105 and SPEC-0107 packages and SPEC-0106 `tsk-0016` moved out of `docs/03.specs/`: the SPEC-0105 rebind test, `ExactLegacyTaskBindingTests` and `OptionalMultiRowStatusTests` errored with `FileNotFoundError` (3 errors) before the change and 6 tests passed after it. In the repository both modules ran 47 tests OK, with no assertion removed. Package reads now come from `bceca1b7` and the legacy baseline from `TASK_LEGACY_BASELINE_COMMIT`. `qa.py staged` on the WORK-001 index passed all selected gates | PASS | This Task; WORK-001 commit | yes | EVD-001 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/README.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  (reciprocal link), `tests/test_task_acceptance_contract.py` and
  `tests/test_task_execution_contract.py`.
- **Forbidden Paths**: `scripts/`, `docs/99.templates/`, other Spec
  packages, frozen Archive payloads, live cluster, Vault and secret
  material.
- **Approval Required**: the operator approved SPEC-0112 and its Plan for
  implementation on 2026-10-13 after reviewing the draft at `33b19203`.
  A scripting error put the Spec and Plan approval and this Task's start in
  one commit, `d3487935`, whose message names only the start; each
  document still moved one edge. Push, pull request and merge await the
  operator.
- **Static Validation**: archive simulation in a scratch clone, focused
  tests and staged QA from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
