---
title: "Spec Architecture Column"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0147-TSK-0001"
parent_ids: ["SPEC-0147-PLAN-0001"]
---

# Task: Spec Architecture Column

## Overview

Make a Spec's architecture statement machine-checked (audit D-1). It
executes [SPEC-0147](../spec.md) through
[WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review D-1 and proceed.
- Review (2026-11-06): option B, a required column without link-target or
  reciprocal checks, chosen over a target link column.
- Approval (2026-11-06): the operator's request to review D-1 and proceed approves SPEC-0147 and its Plan, drafted in `b3e663fc`; merge is separate and criterion acceptance stays the operator's.
- Start: branch `docs/sdlc-cross-artifact-conformance` at `d4338908`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | Focused test and registry column | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | Template and fixtures | platform | completed | PASS | EVD-005, EVD-006 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and unit tests | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Working tree on `4fe16be7` with the new test and the old registry | FAIL | Local run, 2026-11-06T06:10Z: `SpecArchitectureColumnTests` fails, the four-column header is refused with `BODY-CONTRACT-COLUMNS` | no | none |
| EVD-004 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Working tree on `4fe16be7` with the registry column | PASS | Local run, 2026-11-06T06:10Z: `SpecArchitectureColumnTests` OK: new header accepted, old header `BODY-CONTRACT-COLUMNS`, empty cell `BODY-CONTRACT-CELL` | yes | EVD-001 |
| EVD-005 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and unit tests | Working tree on `4fe16be7` with template, fixtures and this Spec updated | PASS | Local run, 2026-11-06T06:10Z to 06:13Z: strict registry, profile, link and lifecycle PASS; `test_document*` OK; form, task-execution, task-acceptance and agent-route tests OK after one fixture consumer (`test_one_plan_work_unit_can_assign_multiple_required_criteria`) was updated to the new row | yes | EVD-002 |
| EVD-006 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and unit tests | Staged index on `85cfdfd4` after the review fixes | PASS | Local run, 2026-11-06: `python3 scripts/qa.py staged` 12 gates PASS; code-reviewer report found no BLOCK, its advisories (template-profile coverage in the test, presence-only wording in `sdlc.md`) applied | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006 | Operator accepted on 2026-11-06 after review | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/templates/specs/spec.template.md`,
  `tests/test_task_execution_contract.py`, `tests/fixtures/`, `.secrets.baseline`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.agents/governance/sdlc.md`
- **Forbidden Paths**: `scripts/`, product manifests, `secrets/`, provider
  settings
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

- Red then green: the focused test failed on the old registry (EVD-003) and
  passes with the column (EVD-004).
- Strict document checks and the affected unit tests PASS; one fixture
  consumer was updated to the new row (EVD-005); the moved secret-scan baseline line was committed first in `85cfdfd4`.
- `sdlc.md` 3.2.0 names the column, so the Plan's Promotion row is real.
- Not run: hosted, provider-runtime and live lanes (not applicable).
- Residual risk: the cell is checked for presence, not for the right AD or
  ADR; reviewers still judge the content.
- Acceptance: the operator accepted VAL-ARCH-001 and 002 on 2026-11-06.
- Next owner: operator, for merge. Rollback: revert
  the implementing commit.
