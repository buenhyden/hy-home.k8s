---
title: "Agent Surface Deferred Conformance"
version: "0.1.0"
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
- Start: branch `docs/agents-deferred` from `main` at `18b76c17`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | Derived projection fields | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | Role-body shared sections | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | Collection-index README subsections | platform | draft | NOT_RUN | EVD-003 |
| WORK-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | `sdlc.md` invariant, CIS numbers, sibling pin | platform | draft | NOT_RUN | EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DEF-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression test and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DEF-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and agent-governance tests | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-DEF-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-DEF-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Source comparison and strict document checks | Pending | NOT_RUN | Pending | yes | none |

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
