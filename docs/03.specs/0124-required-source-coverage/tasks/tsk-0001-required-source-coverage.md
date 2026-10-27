---
title: "Required Source Coverage"
version: "0.4.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0124-TSK-0001"
parent_ids: ["SPEC-0124-PLAN-0001"]
---

# Task: Required Source Coverage

## Overview

Read the ten required sources and record their per-perspective support in
the research register. It executes [SPEC-0124](../spec.md) through
[WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request: the operator's repository survey specification, CR-02.04 and
  CR-02.06, and the 2026-10-27 instruction to continue with the next slice.
- Start: main `d308fd56`, branch `docs/required-source-coverage`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RS-001](../spec.md#success-criteria--verification-plan) | Read the ten sources and add the dated block to m0012 | platform | completed | PASS | EVD-003 closes EVD-001 |
| WORK-002 | [VAL-RS-002](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | completed | PASS | EVD-004 closes EVD-002 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Source block and independent re-read | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Source block and independent re-read | Branch `docs/required-source-coverage`: a delegated read-only researcher read the ten sources on 2026-10-27; a second, independent researcher re-read the live pages of the four new sources and spot-checked the other six | PASS | m0012 gains the 2026-10-27 block: 16 source rows (SRC-WERPC-267 to 275 new, five IDs reused) and a ten-by-six matrix whose 60 cells each hold one valid value, none `NOT_RETRIEVED`. The re-read confirmed every commit, release and date claim and every `EXPLICIT` cell of the four new sources, and approved. Its one medium finding (an unstated Validate-to-converge mapping) and five low findings (attribution, two cells moved to `DERIVED_PROPOSAL`, absence notes) were applied. Diátaxis first returned HTTP 429 to one tool and was read with a second | yes | EVD-001 |
| EVD-004 | [VAL-RS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Staged QA and hosted checks | PR #179 head `2af87818`, CI run `40481689611`; pre-commit staged QA on commits `5756a030`, `f8bb00d1`, `2319af7b` and `2af87818` | PASS | `ci-summary`, `style-pr`, `label` and GitGuardian passed (5 passed, 0 failed). Staged QA passed on all four commits. The first attempt to commit the block failed `detect-secrets` because the block moves four baselined m0012 hashes by 42 lines; the baseline line numbers moved first in `2319af7b`, as `8c4f3088` did | yes | EVD-002 |
| EVD-005 | [VAL-RS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Evidence count correction | PR #179 final review of head `41def872` | PASS | EVD-003 says five IDs were reused; the block reuses seven (`SRC-WERPC-014`, 020, 071, 116, 117, 127 and 184), so its 16 rows are nine new and seven reused. The final review approved the whole pull request; CI on head `41def872` (run `40483298697`) passed | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RS-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-003 | Accepted by the operator on 2026-10-27: the ten sources are recorded with a value for every perspective and the independent re-read approved | platform |
| [VAL-RS-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the operator on 2026-10-27: staged QA passed on every commit and the hosted checks passed | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index and
  `docs/90.references/research/0001-workspace-engineering/m0012-source-coverage.md`,
  and the m0012 line numbers in `.secrets.baseline`, which shift when the
  block is inserted.
- **Forbidden Paths**: governance, templates, validators, other research
  members, provider settings and credentials.
- **Approval Required**: the operator asked on 2026-10-27 to continue with
  the next slice. Push, pull request and merge follow RUN-0013.
- **Acceptance**: on 2026-10-27 the operator accepted VAL-RS-001 and
  VAL-RS-002.
- **Static Validation**: `qa.py staged` on the exact index.
- **Live Validation**: none; the hosted checks on the pull request.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request; the block is removed.
- **Evidence Location**: this Task.

## Verification Summary

WORK-001 passed (EVD-003): m0012 records the ten required sources with a
support value for each of the six perspectives, none `NOT_RETRIEVED`, and an
independent re-read approved. WORK-002 passed (EVD-004): staged QA and the
hosted checks passed. The operator accepted both criteria. Adoption of any
source content stays with the canonical owners (CR-02.07).
