---
title: "Hosted CI Lock Check"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0123-TSK-0001"
parent_ids: ["SPEC-0123-PLAN-0001"]
---

# Task: Hosted CI Lock Check

## Overview

Run the reviewed base's CI Python lock check on pull requests that change
`.github/requirements/`. It executes [SPEC-0123](../spec.md) through
[WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-27, after reviewing the Dependabot alerts, the operator
  chose "Hosted lock check" to close the gap where a Dependabot lock pull
  request skips local staged QA and shows green checks.
- Precedent: PR #164 (virtualenv) and PR #172 (filelock) both dropped
  `--only-binary :all:`; commits `7195e74e` and `26b85e56` restored it.
- Start: main `a5b430c0`, branch `ci/hosted-lock-check`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HL-001](../spec.md#success-criteria--verification-plan) | Add the step, the reviewed topology and its tests, and the hosted lane wording | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-HL-002](../spec.md#success-criteria--verification-plan) | Observe the hosted run and staged QA | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-HL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Reviewed topology and failing lock | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-HL-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Hosted run and staged QA | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-HL-001](../spec.md#success-criteria--verification-plan) | pending | none | Step, topology and tests remain | platform |
| [VAL-HL-002](../spec.md#success-criteria--verification-plan) | pending | none | Hosted run and staged QA remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `.github/workflows/ci.yml`, `scripts/validate-ci-python-contract.py`,
  `tests/test_validate_ci_python_contract.py` and
  `.agents/governance/quality.md`.
- **Forbidden Paths**: branch protection, `.github/dependabot.yml`, the lock,
  provider settings and credentials.
- **Approval Required**: the operator chose this change on 2026-10-27. Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: focused tests and `qa.py staged` on the exact index.
- **Live Validation**: the hosted `style-pr` run on the pull request.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request; `style-pr` returns to six steps.
- **Evidence Location**: this Task.

## Verification Summary

Nothing has run yet.
