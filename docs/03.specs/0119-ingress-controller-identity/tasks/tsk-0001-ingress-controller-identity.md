---
title: "Ingress Controller Identity Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0119-TSK-0001"
parent_ids: ["SPEC-0119-PLAN-0001"]
---

# Task: Ingress Controller Identity Execution

## Overview

Execute [SPEC-0119](../spec.md) through [WORK-001–002](../plan.md#work-breakdown):
one declared ingress controller identity in the validator and no duplicated
shell assertions.

## Inputs

- The operator's 2026-10-16 instruction to proceed as recommended: phase two
  of the local QA review and item 18 (nginx hard-wiring) before the ingress
  replacement ADR.
- Start: main `ad3e187f` (PR #157 merge), branch
  `refactor/spec-0119-ingress-controller-identity`.
- A read-only `network-reviewer` scoping report of the same date.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | Declared controller identity in `ingress.py` | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | Remove duplicated shell assertions | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Ingress focused tests | `scripts/validation/platform/ingress.py`, `tests/test_platform_ingress.py` on this branch | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator change and tests remain | platform |
| [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | pending | none | Mutation proof and removal remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0119-ingress-controller-identity/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `scripts/validation/platform/ingress.py`,
  `scripts/validate-infrastructure-contracts.sh`, `tests/test_platform_ingress.py`.
- **Forbidden Paths**: `gitops/**`, `infrastructure/**`, `policy/**`,
  `.github/workflows/**`, credentials.
- **Approval Required**: The operator's "proceed as recommended" is recorded
  as approval of SPEC-0119 and its Plan as written on 2026-10-16; the operator
  may revoke or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, assurance, the shell validator, Ruff
  and `qa.py staged` on the exact index.
- **Live Validation**: None; no cluster access.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
