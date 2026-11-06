---
title: "Stage 90 Published Member Freeze"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0150-TSK-0001"
parent_ids: ["SPEC-0150-PLAN-0001"]
---

# Task: Stage 90 Published Member Freeze

## Overview

Refuse a rewrite of a published Stage 90 member (AUD-0001 F-10). It executes
[SPEC-0150](../spec.md) through [WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): resolve the remaining item of the same kind.
- Review (2026-11-06): the check belongs to the Stage 90 topology owner, not
  the lifecycle validator (REQ-0003-FR-0027); link destinations stay
  changeable for consumer succession.
- Approval (2026-11-06): the operator's request to resolve the remaining item approves SPEC-0150 and its Plan, drafted in `1b7f70aa`; merge is separate and criterion acceptance stays the operator's.
- Start: branch `fix/stage90-published-freeze` from `main` at `397e0c26`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | Focused tests and freeze check | platform | completed | PASS | EVD-004, EVD-006 |
| WORK-002 | [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | Strict checks and observed refusal | platform | completed | PASS | EVD-005 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and observed refusal | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `cc7804cf` with the new tests and the old validator | FAIL | Local run, 2026-11-06T08:32Z: `PublishedMemberFreezeTest` errors; `published_rewrite_errors` does not exist | no | none |
| EVD-004 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `cc7804cf` with the freeze check | PASS | Local run, 2026-11-06T08:33Z: `tests.test_reference_pack_routes` OK, including body and link-text rewrites refused, lifecycle values and link destinations allowed, draft, new and pack files not frozen; ruff clean | yes | EVD-001 |
| EVD-005 | [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict checks and observed refusal | Working tree on `cc7804cf`; the published `AUD-0001-m0001` staged with a one-word body change, then with a destination-only link change | PASS | Local run, 2026-11-06T08:34Z: the rewrite exits 1 with `REFERENCE_PUBLISHED_REWRITE`; the link change passes; m0001 restored to its HEAD bytes (SHA-256 prefix `5393780c2410897b` before and after) | yes | EVD-002 |
| EVD-006 | [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests red then green | Working tree on `cc7804cf` after the review fixes | PASS | Local run, 2026-11-06T08:39Z: the independent review found no BLOCK and ADVISORY bypasses; fixed: a renamed or moved member is compared with its HEAD original (`git diff --cached -M`), only a single link destination token is normalized so a title or prose is content, only an unborn HEAD skips the check, and the staged text is decoded after the published check; `tests.test_reference_pack_routes` OK with two new link cases; staging a `git mv` of m0001 with a one-word change is refused, m0001 restored identical to HEAD | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FRZ-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-006 | Operator accepted on 2026-11-06 after review | platform |
| [VAL-FRZ-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005 | Operator accepted on 2026-11-06 after review | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-document-contract-registry.py`,
  `tests/test_reference_pack_routes.py`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `scripts/validate-document-lifecycle.py`, the
  registry, published Stage 90 members, `secrets/`
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

- Red then green: the focused tests failed on the old validator (EVD-003)
  and pass with the freeze check (EVD-004).
- Observed: a staged rewrite of the published m0001 is refused and a
  destination-only link change passes; m0001 is unchanged (EVD-005).
- Not run: hosted, provider-runtime and live lanes (not applicable).
- Review: no BLOCK; the rename and link-destination bypasses were fixed
  (EVD-006).
- Scope: the freeze runs in local staged QA, where HEAD and the index
  differ; a plain strict run on a clean tree compares nothing, and hosted CI
  does not run it, so `--no-verify` bypasses it.
- Residual risk: reference-style link definitions (`[x]: target`) are not
  normalized, so changing one is refused; a link-shaped text inside a code
  fence is normalized like a link; one `git cat-file` runs per changed blob.
- Acceptance: the operator accepted VAL-FRZ-001 and 002 on 2026-11-06.
- Next owner: operator, for merge. Rollback: revert
  the implementing commit.
