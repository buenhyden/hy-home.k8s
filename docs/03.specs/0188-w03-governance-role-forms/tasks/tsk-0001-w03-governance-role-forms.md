---
title: "W03 Governance Role Forms"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0188-TSK-0001"
parent_ids: ["SPEC-0188-PLAN-0001"]
---

# Task: W03 Governance Role Forms

## Overview

This Task records the `governance-role` role and the two governance forms of handoff W03-H28 (W03-D34), for [SPEC-0188](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-governance-role-forms` from `8daf643f` (`main` after PR #253; SPEC-0186 and SPEC-0187 merged); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D34, W03-D01 and W03-H28; W03-D33 to W03-D36 are recorded by SPEC-0186.
- **Decision recorded with this package:** no new decision row; the packages reuse W03-D34.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | Role and form literals and schema; two forms; profile lists and role rebind; role template H3; definition texts; tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-GOVROLE-002](../spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document proof; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | PASS | Round 1 APPROVE over spec.md `1f117aaf…` and plan.md `fdc09ff9…` with FIX-1 (two contract profiles), FIX-2 (the local-role sentence) and NITs, applied to the drafts. | no | none |
| EVD-002 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"2b1d4b4b1c876008fec62be048ac7b69573558bbf3674a413a15175dfe5a278c","plan_sha256":"c804c867b9997f24f2a81ecf103194609335ede46cd682836e41cdd37cb2bd4c"} | PASS | Same reviewer: round 2 APPROVE confirming the fixes over the final bytes named here (strict profile check, 0 diagnostics on the drafts). This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0188 approval question naming spec.md 2b1d4b4b and plan.md c804c867 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0188","SPEC-0188-PLAN-0001"],"reviewed_spec_sha256":"2b1d4b4b1c876008fec62be048ac7b69573558bbf3674a413a15175dfe5a278c","reviewed_plan_sha256":"c804c867b9997f24f2a81ecf103194609335ede46cd682836e41cdd37cb2bd4c","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"719d9fcfaefb575db6c1d13c1dc704790ba374abfeab4c8cdedb998c82223d82","plan_sha256":"7cd2d8ccc0b04f95de06cd6c2d2c7a490b54a452a9c691dbeede6b2820aeda8f"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the differences from the bytes approved in EVD-003 are the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22), and one Overview link path corrected from the nonexistent `0187-w03-governance-contract-to-rule` to `0187-w03-sdlc-policy-form`; facts re-checked on `main` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 719d9fcf and plan.md 7cd2d8cc dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0188","SPEC-0188-PLAN-0001"],"reviewed_spec_sha256":"719d9fcfaefb575db6c1d13c1dc704790ba374abfeab4c8cdedb998c82223d82","reviewed_plan_sha256":"7cd2d8ccc0b04f95de06cd6c2d2c7a490b54a452a9c691dbeede6b2820aeda8f","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"d844f3193c9cbfb278868998dc2155af12a20020c747742ff2aeb3e2b0074ac0","plan_sha256":"7cd2d8ccc0b04f95de06cd6c2d2c7a490b54a452a9c691dbeede6b2820aeda8f"} | PASS | Same reviewer, 2026-11-14: the package commit over the EVD-005 bytes was refused by `LINK-BROKEN` because SPEC-0186 and SPEC-0187 left the tree; the fix replaces the two links with plain-text frozen-source citations (`31d527d0`, `067c18e0`), confirmed as the only change and as existing paths. APPROVE over the bytes named here; this row records a review, not an approval. | yes | none |
| EVD-007 | [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0188 re-approval question naming spec.md d844f319 and plan.md 7cd2d8cc dated 2026-11-14 Asia/Seoul","review_ref":"EVD-006","scope":["SPEC-0188","SPEC-0188-PLAN-0001"],"reviewed_spec_sha256":"d844f3193c9cbfb278868998dc2155af12a20020c747742ff2aeb3e2b0074ac0","reviewed_plan_sha256":"7cd2d8ccc0b04f95de06cd6c2d2c7a490b54a452a9c691dbeede6b2820aeda8f","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GOVROLE-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-GOVROLE-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`; `docs/99.templates/templates/governance/role.template.md`; the profile schema role and form enums; `scripts/document_contracts.py` literals and comment; the named tests; the forms sentence of `.agents/governance/document-authoring.md` and the local-role sentence of `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: the 17 role files, the two provider files and `.agents/roles/README.md` (form-only, no text change), the SPEC-0186 roles, `reference-report`, `provider-native`, `sdlc.md`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key and a broken link was corrected, the new bytes were reviewed (EVD-004) and approved by the user again (EVD-005); the package commit then replaced two links to closed packages with frozen-source citations, reviewed (EVD-006) and approved again (EVD-007); these are the committed bytes. Implementation not started.
