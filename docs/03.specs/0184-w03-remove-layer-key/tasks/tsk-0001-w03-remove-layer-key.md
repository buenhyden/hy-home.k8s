---
title: "W03 Remove the Layer Frontmatter Key"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0184-TSK-0001"
parent_ids: ["SPEC-0184-PLAN-0001"]
---

# Task: W03 Remove the Layer Frontmatter Key

## Overview

This Task records handoff W03-H25, the removal of the frontmatter `layer` key from documents other than accepted ADRs, for [SPEC-0184](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-remove-layer-key` from `8e23dc1f` (the SPEC-0183 closure; PR #248 open), stacked on that PR and checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D22 and W03-H25.
- **Decision recorded with this package:** W03-D32, a one-use exemption in the package-exit check and the published Stage 90 rewrite check for the `layer` line only; user answer "One-use exemption (Recommended)" on 2026-11-13 to the freeze-gate question.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | Gate exemptions, `FM-LAYER-ADR`, registry, documents, templates, tests and fixtures. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | Policy texts; open-package evidence rows; regression and exact-index QA; exemption retirement in the final source commit. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `3a8bcf66…` and plan.md `b8246699…`; 2026-11-13 | FAIL | REJECT: BLOCK R4 of the package-exit check refuses the `layer` edit on SPEC-0161; BLOCK the registry refuses rewriting published Stage 90 members; BLOCK `TEMPLATE_OMITTED_KEYS` must keep `layer`; FIXes F1 to F5 on the drafts. The decision W03-D32 (a one-use exemption) followed. | no | none |
| EVD-002 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"9d029adc9cb773357d5e1a99fe61163c37b4ceb980d9150d0ca9aa5c81b27185","plan_sha256":"a82ae68957145fe85e7dbdb962acb4fd79973401e9f744757da04b6e435e7f20"} | PASS | Same reviewer: round 2 APPROVE with FIX-1 to FIX-3 over spec.md `76eda90e…` and plan.md `03e4492d…`; round 3 APPROVE over spec.md `d6152191…` and plan.md `6fefd7cc…`. The author then applied the three wording NITs of round 3 (closure changed to final source commit; the SPEC-0161 version and updated exception added to the scope; a duplicate anchor clause removed), giving the bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0184 approval question naming spec.md 9d029adc and plan.md a82ae689 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0184","SPEC-0184-PLAN-0001"],"reviewed_spec_sha256":"9d029adc9cb773357d5e1a99fe61163c37b4ceb980d9150d0ca9aa5c81b27185","reviewed_plan_sha256":"a82ae68957145fe85e7dbdb962acb4fd79973401e9f744757da04b6e435e7f20","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LAYER-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LAYER-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D32 row, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: the 34 accepted ADRs, `.github/workflows/`, document body text other than the named policy sentences, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance`, `ci-metadata`, `validation-routing` and `tooling` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
