---
title: "Agent Surface Deferred Conformance"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0145-TSK-0001"
parent_ids: ["SPEC-0145-PLAN-0001"]
---

# Task: Agent Surface Deferred Conformance

## Overview

Handle the six items SPEC-0144 deferred. It executes [SPEC-0145](../spec.md)
through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): handle the deferred items and finish.
- Approval (2026-11-06): the operator's instruction to handle the deferred
  items and finish approves SPEC-0145 and its Plan, drafted in `87e32afd`, and the
  delivery through a pull request and merge; it also accepts the criteria once
  their evidence passes.
- Start: branch `docs/agents-deferred` from `main` at `18b76c17`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | Derived projection fields | platform | in-progress | PASS | EVD-005, EVD-006 |
| WORK-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | Role-body shared sections | platform | ready | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | Collection-index README subsections | platform | ready | NOT_RUN | EVD-003 |
| WORK-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | `sdlc.md` invariant, CIS numbers, sibling pin | platform | ready | NOT_RUN | EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and agent-governance tests | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Source comparison and strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Working tree on `40b97e1e` with the new test and the old registry | FAIL | Local run, 2026-11-06T00:44Z: `test_role_projections_are_derived_not_declared` fails because every role still carries `projections` and `supported_providers` | no | none |
| EVD-006 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Working tree on `40b97e1e` with the change | PASS | Local run, 2026-11-06T00:54Z: `tests.test_validate_agent_registry`, `tests.test_agent_governance` and `tests.test_prompt_input` 111 tests OK; `validate-agent-governance.py` PASS with projections=51; `role_projections` derives each path and the stale-or-extra projection comparison is unchanged; the role-level provider checks it replaced were unreachable | yes | EVD-001 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |
| [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-003 | platform |
| [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-004 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/`, `scripts/validate-agent-governance.py`,
  `tests/test_agent_governance.py`, `tests/test_validate_agent_registry.py`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` registry and schemas, provider
  settings, hooks and projections, `secrets/`, the sibling repository
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: regression test, agent-governance validator and
  tests, strict document checks, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

Not run yet.
