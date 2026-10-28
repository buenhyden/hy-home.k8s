---
title: "Release Body Limit"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0137-TSK-0001"
parent_ids: ["SPEC-0137-PLAN-0001"]
---

# Task: Release Body Limit

## Overview

Keep the Release body within GitHub's limit without shortening the changelog.
It executes [SPEC-0137](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose to add length handling to
  `scripts/release.py` after the PR #191 review found the `0.1.0` notes
  exceed GitHub's 125,000-character Release body limit.
- Start: `26b0543b`, branch `fix/release-body-limit`.
- Scope change: the first commit attempt failed `repository-quality` with
  `EXECUTABLE-CURRENT` for `scripts/validate-repo-quality-gates.sh` named in
  `CHANGELOG.md`. On 2026-10-28 the operator approved classifying
  `CHANGELOG.md` as historical in the same Spec (0.1.1).

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RB-001](../spec.md#success-criteria--verification-plan) | Derive a bounded Release body | platform | in-progress | PASS | EVD-004 closes EVD-001 |
| WORK-002 | [VAL-RB-002](../spec.md#success-criteria--verification-plan) | Use the body in publish and describe it in RUN-0012 | platform | in-progress | PASS | EVD-005 closes EVD-002 |
| WORK-003 | [VAL-RB-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-then-passing test | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RB-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Release tests and runbook | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RB-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-RB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Failing-then-passing test | `python3 -m unittest tests.test_release.ReleaseBodyTest` on `c640d1e2` with the new tests and the unchanged tool, then after the change | PASS | Before: 2 tests, 2 errors, because no body function existed. After: 2 tests OK. An over-limit section yields a summary within 125,000 characters with each group's count and the tagged `CHANGELOG.md` link; a section at the limit, and a short one, are unchanged | yes | EVD-001 |
| EVD-005 | [VAL-RB-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Release tests and runbook | `python3 -m unittest tests.test_release`; `_release_body` on the committed `0.1.0` section; RUN-0012 Verification | PASS | 21 tests OK. `publish` builds the draft, its verification and the preview from one derived body, and the preview reports `body_chars` and `body=section` or `summary`. The 143,352-character `0.1.0` section yields a 391-character summary over eleven groups. RUN-0012 1.2.1 states the rule. The CHANGELOG reference test fails with `EXECUTABLE-CURRENT` on the previous classifier and passes after it; `tests.test_current_executable_references` runs 13 tests OK and `scripts/validation/repository/quality.py` passes with the `0.1.0` changelog | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RB-001](../spec.md#success-criteria--verification-plan) | pending | none | Test and change remain | platform |
| [VAL-RB-002](../spec.md#success-criteria--verification-plan) | pending | none | Publish wiring remains | platform |
| [VAL-RB-003](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index, REQ-0003,
  `scripts/release.py`, `tests/test_release.py`,
  `scripts/validation/current_executable_references.py`,
  `tests/test_current_executable_references.py` and
  `docs/05.operations/runbooks/0012-main-release-preparation-runbook.md`.
- **Forbidden Paths**: `CHANGELOG.md`, `cliff.toml`, tags, Releases, other
  validators and workflows.
- **Approval Required**: the operator decided on 2026-10-28 (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: none; no release is published.
- **Secret / Vault Handling**: no secret is read.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
