---
title: "Dead Profile Mode Cleanup"
version: "0.2.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0143-TSK-0001"
parent_ids: ["SPEC-0143-PLAN-0001"]
---

# Task: Dead Profile Mode Cleanup

## Overview

Remove the profile and frontmatter modes that no registry value produces, and
the validator branches that only they reach. It executes
[SPEC-0143](../spec.md) through [WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): clean up the dead modes, the follow-up SPEC-0142
  left.
- Approval (2026-11-06): the operator approved SPEC-0143 and its Plan after
  review of the draft in `efba0179`, and asked for a pull request and merge.
- Start: branch `refactor/dead-profile-modes` from `main` at `0b00f3a3`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | Type regression test and narrowed `Literal` types | platform | completed | PASS | EVD-003, EVD-004 |
| WORK-002 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | Unreachable branches and helper code | platform | completed | PASS | EVD-005, EVD-006 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Type regression test | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Code search, document suite, strict document checks and repository quality check | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Type regression test | New test copied onto a detached worktree of `5af1f081` with the old scripts | FAIL | Local run, 2026-11-05T17:14Z: `test_typed_modes_match_the_schema_and_loader` fails with `'frontmatter-free'` and `'classification-only'` outside the schema enum, as expected | no | none |
| EVD-004 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Type regression test | Working tree on `5af1f081` with the change | PASS | Local run, 2026-11-05T17:15Z: the test passes; after the review the frontmatter half derives its expected set from the schema enum and the loader mapping, and the module's 35 tests pass | yes | EVD-001 |
| EVD-005 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent review of the implementing change | Working tree on `5af1f081` | PASS | code-reviewer report: no removed branch was reachable (only `scripts/document_contracts.py` builds `DocumentProfile` and `FrontmatterContract`, the schema and loader admit none of the removed values); the GitHub-native `FM-FORBIDDEN` diagnostic keeps its rule, text and owner; one advisory on the test's frontmatter half was applied | yes | none |
| EVD-006 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Code search, document suite, strict document checks and repository quality check | Working tree on `5af1f081` with the change | PASS | Local run, 2026-11-05T17:15Z: `git grep` finds no `frontmatter-free` or `classification-only` mode and no frontmatter `not-applicable` in the three scripts (one unrelated message wording remains in `quality.py`); `run-contract-tests.py --suite document` 282 tests PASS; strict registry, profile, link and lifecycle checks PASS; `quality.py` PASS; `ruff` clean | yes | EVD-002 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-003, EVD-004 | Operator accepted on 2026-11-06 | platform |
| [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006 | Operator accepted on 2026-11-06 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/document_contracts.py`,
  `scripts/validate-markdown-profiles.py`,
  `scripts/validation/repository/quality.py`,
  `tests/test_document_terminal_contract.py`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` schemas and registry, current
  document bodies outside the Allowed Paths
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: document contract suite, strict document checks,
  repository quality check, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

- The type regression failed on the old scripts (EVD-003) and passes with
  the change (EVD-004).
- The code search, document suite, strict document checks and repository
  quality check pass (EVD-006); the independent review found no reachable
  removed branch (EVD-005).
- Live lane: not applicable.
- Rollback: revert the implementing commit.
