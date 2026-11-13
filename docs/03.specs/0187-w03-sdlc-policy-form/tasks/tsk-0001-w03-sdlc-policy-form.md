---
title: "W03 SDLC Policy Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0187-TSK-0001"
parent_ids: ["SPEC-0187-PLAN-0001"]
---

# Task: W03 SDLC Policy Form

## Overview

This Task records the move of `.agents/governance/sdlc.md` to the Policy form (handoff W03-H29, W03-D27), for [SPEC-0187](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-sdlc-policy-form` from `de64c58d` (`main` after PR #252, SPEC-0186); checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D06 and W03-H29.
- **Decision recorded with this package:** W03-D41 to W03-D44 (sdlc.md joins governance/rule; `<CODE>-R<NNN>` rule IDs; inline ID plus required Rules table; Status column for retirement); user answers of 2026-11-13 to the Policy role questions. The Spec writes out the D41 supersede wording.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | Move `sdlc.md` to the Policy form; write the explained-none texts; make the one edit; check the anchor. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-SDLCPOL-002](../spec.md#success-criteria--verification-plan) | Registry consolidation; remove the template; retarget the tests; record W03-D41 to W03-D44. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | FAIL | Rounds 1 and 2 REJECT. Round 1 over spec.md `e985ffdb…` and plan.md `53e297d0…`: BLOCK dead SPEC-0182 links, BLOCK a missed consumer at `docs/99.templates/templates/README.md` line 46, FIX-3 to FIX-10. Round 2 over spec.md `abfe3f53…`: the quoted sentences were code spans, not real links, and NITs. Applied to the drafts. | no | none |
| EVD-002 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"5258bd2928f54a84a04eacf5e17b659a4510918aa83fd0db295c7e903652dcab","plan_sha256":"99149487d799b207608bdf095ebd45ec27e5c4a769c528fb525a6c0d070287b6"} | PASS | Same reviewer: round 3 APPROVE over the final bytes named here. The trial repository `scratchpad/pkgPOLICY1/repo3` carries the quoted sentences of `sdlc.md` lines 56 and 202 as links. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0187 approval question naming spec.md 5258bd29 and plan.md 99149487 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0187","SPEC-0187-PLAN-0001"],"reviewed_spec_sha256":"5258bd2928f54a84a04eacf5e17b659a4510918aa83fd0db295c7e903652dcab","reviewed_plan_sha256":"99149487d799b207608bdf095ebd45ec27e5c4a769c528fb525a6c0d070287b6","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"5e0efa513cd1f3374d12f464a4c244414f727087163c13087bb91d67a2363084","plan_sha256":"5f14aa2de1a4bd5b17633401306f773f3835971b5a602b3a8f54218b10cf78ad"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-13: the only difference from the bytes approved in EVD-003 is the deleted frontmatter `layer` line in each file, required by SPEC-0184 (W03-D22) and announced by the open-package layer rule these bytes already named; facts re-checked on `main` with line drift only. APPROVE. | yes | none |
| EVD-005 | [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 5e0efa51 and plan.md 5f14aa2d dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0187","SPEC-0187-PLAN-0001"],"reviewed_spec_sha256":"5e0efa513cd1f3374d12f464a4c244414f727087163c13087bb91d67a2363084","reviewed_plan_sha256":"5f14aa2de1a4bd5b17633401306f773f3835971b5a602b3a8f54218b10cf78ad","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SDLCPOL-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SDLCPOL-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`.agents/governance/sdlc.md`; the `governance/contract` profile, its twin, its family entry and the `governance/rule` pattern and consumers in `docs/99.templates/registry.json`; the removed `contract.template.md`; `docs/99.templates/templates/README.md`; the 21 named test lines), this package, `docs/03.specs/README.md`, the W03-D41 to W03-D44 rows, the refreshed state cell of the W03-H29 row, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: rule IDs, the Rules table and its checks (packages 2 to 5), any rule text of `sdlc.md` other than the one named edit, the Policy form and template, the glossary, `docs/90.references/`, `docs/98.archive/`, `sessions/`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key, the bytes without that line were reviewed (EVD-004) and approved by the user again (EVD-005); these are the committed bytes. Implementation not started.
