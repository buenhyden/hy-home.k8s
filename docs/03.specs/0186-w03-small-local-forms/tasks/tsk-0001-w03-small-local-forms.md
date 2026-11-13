---
title: "W03 Small Local Forms"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0186-TSK-0001"
parent_ids: ["SPEC-0186-PLAN-0001"]
---

# Task: W03 Small Local Forms

## Overview

This Task records the six small local forms of handoff W03-H28 (W03-D26), for [SPEC-0186](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-small-local-forms` from `cd174848` (`main` after PR #251, SPEC-0190; SPEC-0182 to SPEC-0185 and SPEC-0190 merged); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D26, W03-D01 and W03-H28.
- **Decision recorded with this package:** W03-D33 to W03-D36 (provider-native stays form-less; governance-role split; research H3 registered as is; one reference-report form with link-only Sources); user answers of 2026-11-13 to the local-forms questions.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | Form literal and schema; six forms; profile lists; table sections and definition texts; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document proof; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | PASS | Conditional APPROVE over spec.md `d233c8d4…` and plan.md `d3c5fa20…` with FIX-1 (nine-role wording), FIX-2 (nine tables and table diagnostics), FIX-3 (four-step commit order) and NITs, applied to the drafts. | no | none |
| EVD-002 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"ec14697e2e313b1c2e5a32ba016f1c7196e5386583deedac394fdfa0dfbebf38","plan_sha256":"5eebb58dec8cf58545bd802af1fe3c6c2c4181568d01480b736dcd22ad6592d6"} | PASS | Same reviewer: round 2 APPROVE confirming the fixes over the final bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0186 approval question naming spec.md ec14697e and plan.md 5eebb58d dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0186","SPEC-0186-PLAN-0001"],"reviewed_spec_sha256":"ec14697e2e313b1c2e5a32ba016f1c7196e5386583deedac394fdfa0dfbebf38","reviewed_plan_sha256":"5eebb58dec8cf58545bd802af1fe3c6c2c4181568d01480b736dcd22ad6592d6","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b5e1a28f624adfbf5d2f74b0e7d16ff163e6518b0603bd2ae38e95582d5ae6ac","plan_sha256":"1bd6b6068c05dab8dac3fe1bdaa0bcde5ecd763f6e1c3e706ca6ac6d708d5703"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the only difference from the bytes approved in EVD-003 is the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22) and announced by the open-package layer rule these bytes already named; facts re-checked on `main` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md b5e1a28f and plan.md 1bd6b606 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0186","SPEC-0186-PLAN-0001"],"reviewed_spec_sha256":"b5e1a28f624adfbf5d2f74b0e7d16ff163e6518b0603bd2ae38e95582d5ae6ac","reviewed_plan_sha256":"1bd6b6068c05dab8dac3fe1bdaa0bcde5ecd763f6e1c3e706ca6ac6d708d5703","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SMALLFORMS-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SMALLFORMS-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, the profile schema form enum, `scripts/document_contracts.py` literals and comments, the named tests, the forms sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, the W03-D33 to W03-D36 rows, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: the documents and templates of the six roles (form-only, no text change), `reference-report`, `governance-document` and `governance-role`, `provider-native`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, knowledge-surface and prompt-input tests, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key, the bytes without that line were reviewed (EVD-004) and approved by the user again (EVD-005); these are the committed bytes. Implementation not started.
