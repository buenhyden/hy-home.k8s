---
title: "W03 Work Ledger Contract"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0185-TSK-0001"
parent_ids: ["SPEC-0185-PLAN-0001"]
---

# Task: W03 Work Ledger Contract

## Overview

This Task records the first half of handoff W03-H30 (W03-D25): requirement, architecture and governance text, `ADR-0060` and the work residue ledger clarifications, for [SPEC-0185](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-work-ledger-contract` from `c54eed50` (`main` after PR #249, SPEC-0184); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D25 and W03-H30.
- **Decision recorded with this package:** W03-D37 to W03-D40 (residue-only JSON ledger; on-demand view with pruning; seed now with exempt history; new ADR plus REQ and AD edits); user answers of 2026-11-13 to the GOV-06 ledger questions.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | Write `ADR-0060` as `proposed` with its README entry and the four dated clarifications; amend REQ-0003 and AD-0006. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | Governance and knowledge-map sentences; the superseding EVD row and refreshed state cells; regression and exact-index QA; then the Task Evidence row with the user's ADR-0060 acceptance answer and the `proposed` to `accepted` flip alone. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | FAIL | REJECT over spec.md `cd019398…` and plan.md `320267ca…`: BLOCK B1 (ADR creation and acceptance in one commit) and FIXes F1 to F9, applied to the drafts. | no | none |
| EVD-002 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"6a7a72e3fa3ea31195e5e6c00256e5c5c2d0b2e66dabc5ba83d9be8854bcf19a","plan_sha256":"5b36ab60875afbb91c12a52fcf6fe9773e1f13a0c1220e2115c3d7380e86fe2d"} | PASS | Same reviewer: round 2 APPROVE over the revised bytes with NIT-A (the `rg` criterion scope) and NIT-B (the route wording), both left to implementation and this Task. The approved bytes are the bytes named here; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 approval question naming spec.md 6a7a72e3 and plan.md 5b36ab60 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0185","SPEC-0185-PLAN-0001"],"reviewed_spec_sha256":"6a7a72e3fa3ea31195e5e6c00256e5c5c2d0b2e66dabc5ba83d9be8854bcf19a","reviewed_plan_sha256":"5b36ab60875afbb91c12a52fcf6fe9773e1f13a0c1220e2115c3d7380e86fe2d","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"90163654d94d30f15561eea10c65e3dff6cd1bf573c7759a193aa3189dc85019","plan_sha256":"90d0066eb5073abdea51ef31ea8b18e2a62502fb205340dd0674b3746d775dca"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the only difference from the bytes approved in EVD-003 is the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22) and announced by the open-package layer rule these bytes already named; facts re-checked on `main` `c54eed50` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 90163654 and plan.md 90d0066e dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0185","SPEC-0185-PLAN-0001"],"reviewed_spec_sha256":"90163654d94d30f15561eea10c65e3dff6cd1bf573c7759a193aa3189dc85019","reviewed_plan_sha256":"90d0066eb5073abdea51ef31ea8b18e2a62502fb205340dd0674b3746d775dca","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LEDGER-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LEDGER-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`ADR-0060` and its README entry, REQ-0003, AD-0006, the four dated ADR clarifications, five governance or skill sentences), this package, `docs/03.specs/README.md`, the W03-D37 to W03-D40 rows, evidence rows, the state cells of the `LEDGER` conflict row and the W03-H30 row, and the frontmatter `version` and `updated` of the SPEC-0161 Task, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: the ledger file, its schema, script and validator (package 2), any Stage 90 document, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; the acceptance of `ADR-0060` (a separate user answer recorded as Task Evidence before the `proposed` to `accepted` flip); push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, the `rg` checks of the Spec, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit (set `ADR-0060` back to `proposed` if only the flip is wrong); before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key, the bytes without that line were reviewed (EVD-004) and approved by the user again (EVD-005); these are the committed bytes. Implementation not started.
