---
title: "Local QA Rightsizing Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0117-TSK-0001"
parent_ids: ["SPEC-0117-PLAN-0001"]
---

# Task: Local QA Rightsizing Execution

## Overview

Execute [SPEC-0117](../spec.md) through [WORK-001–005](../plan.md#work-breakdown):
repair failing tests and remove over-applied, duplicated, conflicting and
stale local checks found by the 2026-10-16 audit.

## Inputs

- The operator's 2026-10-16 request to review the local full test surface for
  over-applied, duplicated, conflicting or stale checks and to fix them; the
  operator chose to start with phase one.
- Start: main `f062294c` (PR #155 merge), branch
  `qa/spec-0117-local-qa-rightsizing`.
- A per-module test timing run on `main` in the session scratch directory.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | Repair the three failing test modules | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-QR-002](../spec.md#success-criteria--verification-plan) | CI Python contract consistency checks | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-QR-003](../spec.md#success-criteria--verification-plan) | Ingress validator without chart versions | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-QR-004](../spec.md#success-criteria--verification-plan) | Quality and registry cleanup | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-005 | [VAL-QR-005](../spec.md#success-criteria--verification-plan) | Delivery procedure and README alignment | platform | in-progress | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Per-module test timing | Every `tests/test_*.py` module on main `f062294c`, run one module at a time with the pinned validation environment | FAIL | `test_completed_state_migration` (3 failures), `test_generic_migration_recovery` (1 error) and `test_document_lifecycle_cumulative_history` (5 failures) fail on `main` | yes | none |
| EVD-002 | [VAL-QR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Per-module test timing | Same run completed: 76 modules, 1,503 tests, 1,880.8 s serial on main `f062294c` | FAIL | A fourth module, `test_task_execution_contract` (3 failures, 9 errors), also fails. Slowest modules: `test_qa_runner` 492 s, `test_archive_validation` 481 s, `test_documentation_link_boundary` 297 s | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-QR-001](../spec.md#success-criteria--verification-plan) | pending | none | Root-cause repair of the failing modules remains | platform |
| [VAL-QR-002](../spec.md#success-criteria--verification-plan) | pending | none | Validator and test change remains | platform |
| [VAL-QR-003](../spec.md#success-criteria--verification-plan) | pending | none | Validator and test change remains | platform |
| [VAL-QR-004](../spec.md#success-criteria--verification-plan) | pending | none | Validator, registry and fixture change remains | platform |
| [VAL-QR-005](../spec.md#success-criteria--verification-plan) | pending | none | Document change and review remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0117-local-qa-rightsizing/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validate-ci-python-contract.py`, `scripts/validation/**`,
  `tests/**`, `.agents/governance/quality.md`, `.agents/governance/git.md`,
  `.github/repository-surface.md`, `.github/CODEOWNERS`, `README.md`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's request ("review, analyze, fix,
  supplement and improve") and the phase-one choice are recorded as approval
  of SPEC-0117 and its Plan as written on 2026-10-16; the operator may revoke
  or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
