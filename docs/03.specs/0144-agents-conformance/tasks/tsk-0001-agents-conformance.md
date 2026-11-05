---
title: "Agent Surface Conformance"
version: "0.1.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0144-TSK-0001"
parent_ids: ["SPEC-0144-PLAN-0001"]
---

# Task: Agent Surface Conformance

## Overview

Correct the `.agents/` files against their governance, forms and the current
workspace. It executes [SPEC-0144](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): check every `.agents/` file against its governance,
  form and the current workspace, and remove conflicts, contradictions and
  duplication.
- Operator choices (2026-11-06): the correctness-and-code scope; bind
  `ops-runbook` to `doc-writer`; remove only the unread schema field.
- Approval (2026-11-06): the operator approved SPEC-0144 and its Plan after
  review of the draft in `d541fb8a`, and asked for a pull request and merge;
  that choice also accepts the criteria once their evidence passes.
- Start: branch `docs/agents-conformance` from `main` at `75ba7b04`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | Code, registry and schema changes | platform | ready | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | Governance files | platform | ready | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | Roles and skills | platform | ready | NOT_RUN | EVD-003 |
| WORK-004 | [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | README, knowledge, prompts, workflows, evaluations | platform | ready | NOT_RUN | EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Regression tests and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict document checks and agent-governance validator | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | WORK-004 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AGC-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |
| [VAL-AGC-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-003 | platform |
| [VAL-AGC-003](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-004 | platform |
| [VAL-AGC-004](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/`, `.claude/agents/doc-writer.md`,
  `.codex/agents/doc-writer.toml`, `scripts/prompt-input.py`,
  `scripts/validate-agent-governance.py`, `tests/`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` registry and schemas, provider
  settings and hooks, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: regression tests, agent-governance validator,
  document contract suite, strict document checks, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

Not run yet.
