---
title: "Pinned Package Fixtures in Lifecycle Tests"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
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
| WORK-001 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | Pin the three package reads | platform | frontmatter | PASS | EVD-002 in commit `e806ac96`; EVD-003 review and UTF-8 repair |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Archive simulation, focused tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Archive simulation, focused tests and staged QA | Scratch clone at `918ed00f` with the SPEC-0105 and SPEC-0107 packages and SPEC-0106 `tsk-0016` moved out of `docs/03.specs/`: the SPEC-0105 rebind test, `ExactLegacyTaskBindingTests` and `OptionalMultiRowStatusTests` errored with `FileNotFoundError` (3 errors) before the change and 6 tests passed after it. In the repository both modules ran 47 tests OK, with no assertion removed. Package reads now come from `bceca1b7` and the legacy baseline from `TASK_LEGACY_BASELINE_COMMIT`. `qa.py staged` on the WORK-001 index passed all selected gates | PASS | This Task; WORK-001 commit | yes | EVD-001 |
| EVD-003 | [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent read-only review | A code-reviewer subagent reviewed `e806ac96`, ran the three affected test classes OK and confirmed every pinned path exists at its commit with byte-identical content. No HIGH or MEDIUM finding. LOW, repaired in this commit: `text=True` decoded with the locale encoding, so the three new reads and the SPEC-0111 pin now use `encoding="utf-8"`; 16 affected tests passed after the repair. LOW, accepted: no unit test now fails if the live `tsk-0016` is edited, because lifecycle validation still sends that file through `legacy_task_profile` and reports it; one archived SPEC-0080 plan is still read from the working tree, outside this scope | PASS | This Task | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PIN-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-002, EVD-003 | Accept the pinned package reads; the archive simulation fails before and passes after, and review LOW items are recorded | platform |

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

The work unit is complete and VAL-PIN-001 is accepted. With the three
packages moved out of `docs/03.specs/` in a scratch clone, the affected
tests failed before the change and passed after it; in the repository both
modules ran 47 tests OK, and every commit passed `qa.py staged` from the
documented validation environment. One scripting error put the Spec and
Plan approval and the Task start in commit `d3487935`; the approval record
followed in `918ed00f`.

Residual risk: an edit to the live SPEC-0106 `tsk-0016` no longer fails a
unit test and is caught by lifecycle validation instead; one archived
SPEC-0080 plan is still read from the working tree. Limitations: hosted
CI, push and pull request are not executed. Next owner: the operator for
push, pull request and merge.
