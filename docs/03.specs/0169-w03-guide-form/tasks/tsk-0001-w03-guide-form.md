---
title: "W03 Guide Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0169-TSK-0001"
parent_ids: ["SPEC-0169-PLAN-0001"]
---

# Task: W03 Guide Form

## Overview

This Task records the first phase-2 package of W03, the Guide form, for [SPEC-0169](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user asked, after the SPEC-0168 closure, to investigate every remaining, unverified, unreviewed, unconfirmed and unprogressed W03 item, continue each, and fix any existing rule that conflicts with current requirements to match them. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-phase2-forms` at `4d5dc5e7` (from `de5c31b0`, the SPEC-0168 closure on PR #233, plus SPEC-0161 decision and missing-item commits); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11 (EVD-025 to EVD-030); EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Guide (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[6]) and the package TemplateDefinition `tables` schema; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | Schema, registry form, extension, TemplateDefinition and table registry checks. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-GUIDEFORM-002](../spec.md#success-criteria--verification-plan) | Document table check. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | Template and GDE-0010 moved form-only with the meaning map; policy text; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `e672f75f…`, plan.md `1bd60337…`; 2026-11-12 | FAIL | REJECT: BLOCK `REGISTRY_BODY_SECTION` (`scripts/document_contracts.py:1593`) refuses a form profile whose body-contract section is not in its empty H2 list, reproduced in memory; FIXes: three no-form tests in `tests/test_common_form_tree.py`, operations tests, the route of tables to authored profiles, an all-tables iterator, an ADR-0059 claim not in its text, the decision link, the second Promotion row's substance, the extension condition and removal, the `.secrets.baseline` commit order, and heading-list consumers (`form_contracts.py`, `quality.py`, `validate-links-and-owners.py`). | no | none |
| EVD-002 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b1447f677232c8e032b9509aaec2d992692643801411fe2f9aa3e9ff62f52732","plan_sha256":"a6cec5aee38256cd5746d2b8d110cb0c5957057d33e307eedb9d91ff041b62d1"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-12: round 2 confirmed every round-1 finding closed (heading lists derived from the form for form profiles, tables copied from the template to its source profiles, body-contract table not checked twice) and APPROVE with four NOTEs; the author applied NOTEs 1, 2 and 4 to the files and recorded NOTE 3 and the multi-template rule as SPEC-0161 W03-H10 (`4d5dc5e7`); round 3 confirmed both hashes and that only those edits changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0169 approval question naming spec.md b1447f67 and plan.md a6cec5ae dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0169","SPEC-0169-PLAN-0001"],"reviewed_spec_sha256":"b1447f677232c8e032b9509aaec2d992692643801411fe2f9aa3e9ff62f52732","reviewed_plan_sha256":"a6cec5aee38256cd5746d2b8d110cb0c5957057d33e307eedb9d91ff041b62d1","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-GUIDEFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document` and `agent-governance` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). Implementation not started.
