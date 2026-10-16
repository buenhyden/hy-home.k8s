---
title: "Independent Review Merge Gate Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0116-TSK-0001"
parent_ids: ["SPEC-0116-PLAN-0001"]
---

# Task: Independent Review Merge Gate Execution

## Overview

Execute [SPEC-0116](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
a local publisher, its runbook, the operator-created review App and the
required `independent-review` check on `main`. Completion closes the PR-edited
workflow forgery path behind SPEC-0115 Task 0005 EVD-012.

## Inputs

- The operator's 2026-10-16 request: research a resolution for EVD-012, write
  its Spec and proceed. A follow-up instruction excluded any AI model API. The
  operator then chose the review App and check-run route over a second
  machine-user account.
- Start: main `26508fe2fd5ba6fc4daaaec2fe7a883a2d8d102d` (PR #151 merge),
  branch `codex/evd-012-independent-review`.
- Research (EVD-001) and the retired SPEC-0107 `qa-provenance` design, which
  bound a check to verifier App `5156553` and was retired with hosted QA, not
  for a defect.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | Publisher script and focused tests | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-IR-002](../spec.md#success-criteria--verification-plan) | RUN-0013 and README routes | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | Review App creation, installation and first check run | operator | draft | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | Main protection requirement and EVD-012 disposition | operator and platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Mitigation research | GitHub documentation read on 2026-10-16 by a `docs-researcher` agent, plus read-only `gh api` GETs of rulesets, main protection and environments | NOT_RUN | Pending | no | none |
| EVD-002 | [VAL-IR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Publisher focused tests | `scripts/independent_review.py`, `tests/test_independent_review.py` on branch `codex/evd-012-independent-review` | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-IR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review App check run | Operator-created App, single-repository installation, this package's PR head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-IR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Main protection read-back | Before/after `branches/main/protection` and PR merge state | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-IR-001](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and independent review of the script remain | platform |
| [VAL-IR-002](../spec.md#success-criteria--verification-plan) | pending | none | Run document checks and independent review | platform |
| [VAL-IR-003](../spec.md#success-criteria--verification-plan) | pending | none | Operator creates and installs the review App | operator |
| [VAL-IR-004](../spec.md#success-criteria--verification-plan) | pending | none | Protection change after a successful observed check run | operator and platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0116-independent-review-gate/**`,
  `docs/03.specs/README.md`, `docs/05.operations/runbooks/0013-independent-review-check-runbook.md`,
  `docs/05.operations/runbooks/README.md`, `scripts/independent_review.py`,
  `scripts/README.md`, `tests/test_independent_review.py`,
  `.github/rulesets/main-protection.md`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other
  Spec packages, credentials and any file holding the review App key.
- **Approval Required**: The operator's request covers repository work and
  research. App creation and installation are operator UI actions. The
  `main` protection update needs the operator's exact approval of the target
  field set after WORK-003, with before/after read-back. No model API key is
  requested or stored.
- **Static Validation**: Focused tests, Ruff, `qa.py staged` on the exact
  index and selected document checks.
- **Live Validation**: Remote observation only: check-run App ID and protection
  read-back. No cluster access.
- **Secret / Vault Handling**: The App private key stays in the operator's
  local file with mode `0600`; agents neither read nor print it. Installation
  tokens are never logged.
- **Rollback Plan**: Revert the repository commits through Git. Remove the
  required check by a reviewed operator decision with read-back; uninstall or
  delete the App if abandoned.
- **Evidence Location**: This Task.

## Verification Summary

The publisher and its tests pass locally. Repository QA, independent review,
the operator-created App, its first observed check run and the protection
change remain pending. Until WORK-004 completes, EVD-012 stays HIGH. After
it, PR-edited workflows can no longer satisfy every required check; the
operator's own access to the key and the procedural independence of the
local reviewer remain residual risks.
