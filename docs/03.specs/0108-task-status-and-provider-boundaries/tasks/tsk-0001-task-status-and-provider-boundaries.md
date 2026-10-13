---
title: "Task Status Derivation and Provider Boundaries"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0108-TSK-0001"
parent_ids: ["SPEC-0108-PLAN-0001"]
---

# Task: Task Status Derivation and Provider Boundaries

## Overview

Execute the three work units of the [Plan](../plan.md) for
[SPEC-0108](../spec.md) as separate logical commits and record their
focused, staged and review evidence here.

## Inputs

- [SPEC-0108](../spec.md) and its [Plan](../plan.md).
- Operator selections on 2026-10-13: implement K-P1 and K-P2 first; move
  push and pull-request commands to `ask`; write only a design Spec for the
  shared memory store.
- Base main `57f44c4446e9ad0e9c8ae87e81c1d208aa7f3c8b`, equal to
  `origin/main` at intake.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | README language exception and Korean roles router | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | Claude ask list and exact permission validation | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | Shared Task status reader and writer retirement | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Language tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Governance tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Task contract tests and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-003 checks | platform |
| [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/0109-shared-workspace-memory/`,
  `docs/03.specs/README.md`, `docs/99.templates/`, `scripts/document_*.py`,
  `scripts/validate-{markdown-profiles,links-and-owners,agent-governance}.py`,
  `scripts/validation/registry.json`, `scripts/sync-task-status.py`
  (removal), `.agents/governance/document-authoring.md`,
  `.agents/roles/README.md`, `.claude/settings.json` and the named tests.
- **Forbidden Paths**: frozen Archive payloads, other Spec packages, live
  cluster, Vault and secret material.
- **Approval Required**: the operator selected the scope and the `ask`
  conversion in this session; push, pull request and merge await the
  operator.
- **Static Validation**: focused unit tests, the four validators named in
  the Spec and `python3 scripts/qa.py staged` per commit.
- **Live Validation**: DEFER — no live surface is touched; native Claude
  prompting for `ask` entries is not observed.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
