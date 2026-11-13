---
title: "W03 Reference Report Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0189-TSK-0001"
parent_ids: ["SPEC-0189-PLAN-0001"]
---

# Task: W03 Reference Report Form

## Overview

This Task records the `reference-report` form of handoff W03-H28 (W03-D35, W03-D36), for [SPEC-0189](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch from from `main` (set at commit time), after SPEC-0186 and SPEC-0188 land; checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D35, W03-D36, W03-D01 and W03-H28; the rows are recorded by SPEC-0186.
- **Decision recorded with this package:** no new decision row; the packages reuse W03-D35 and W03-D36.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | Form literal and schema; the form and its extensions; profile lists; table sections and definition texts; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document and published-member proof; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | PASS | Round 1 APPROVE over spec.md `6dbff37e…` and plan.md `a6158650…` with FIX-1 (validator code stays, tests move to a synthetic profile) and FIX-2 (`Sources` required content), applied to the drafts. | no | none |
| EVD-002 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"4c12f089355501d8f3ef48e1187079311dc920e7cf76d339d96529a056e5bc74","plan_sha256":"0ae492fef4b3c29564aab4cc61666ea6a8dcd8b60511346f7fc0c1dbde9a1e4a"} | PASS | Same reviewer: round 2 APPROVE over the final bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0189 approval question naming spec.md 4c12f089 and plan.md 0ae492fe dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0189","SPEC-0189-PLAN-0001"],"reviewed_spec_sha256":"4c12f089355501d8f3ef48e1187079311dc920e7cf76d339d96529a056e5bc74","reviewed_plan_sha256":"0ae492fef4b3c29564aab4cc61666ea6a8dcd8b60511346f7fc0c1dbde9a1e4a","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"873116156b967590d62db619377bc6169f0518c05821fe52e85814f26cf3ca7a","plan_sha256":"70c2426ec5a6a5330d97c76c7f613f873910b4efed921af31e4da4973033c310"} | PASS | Same reviewer, 2026-11-14: after SPEC-0184 refused the layer frontmatter key, the only change from the EVD-003 bytes is the deleted layer line in spec.md and plan.md, confirmed as the only difference. APPROVE over the bytes named here; this row records a review, not an approval. | yes | none |
| EVD-005 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 87311615 and plan.md 70c2426e dated 2026-11-14 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0189","SPEC-0189-PLAN-0001"],"reviewed_spec_sha256":"873116156b967590d62db619377bc6169f0518c05821fe52e85814f26cf3ca7a","reviewed_plan_sha256":"70c2426ec5a6a5330d97c76c7f613f873910b4efed921af31e4da4973033c310","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`; the profile schema form enum; `scripts/document_contracts.py` literal and comments; the named tests; the forms sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`; `scripts/validate-markdown-profiles.py` and the heading-line path of `REGISTRY_TABLE_SECTION`, unchanged), this package, `docs/03.specs/README.md`, the W03-H28 row, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: any document under `docs/90.references/` (the 13 published members byte for byte; the four others unchanged), the three templates' text, the SPEC-0186 and SPEC-0188 roles, `provider-native`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
