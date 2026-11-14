---
title: "W03 Requirement Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0195-TSK-0001"
parent_ids: ["SPEC-0195-PLAN-0001"]
---

# Task: W03 Requirement Form

## Overview

This Task records the Requirement part of handoffs W03-H02 and W03-H13: the COMMON-DOC-FORM-1 Requirement form with its two local H3 extensions, the requirement TemplateDefinition and tables, and the move of the requirement template and the four approved Requirements with the table column change of W03-D55, for [SPEC-0195](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to continue W03 phase 3 in the order of W03-D49. The request approves no Spec bytes or criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `de64c58d` (after PR #252, SPEC-0186) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-H02, W03-H13, W03-D01, W03-D03, W03-D08, W03-D30, W03-D31, W03-D48, W03-D49, W03-D51 and W03-D52.
- **Decision recorded with this package:** W03-D55 (the `Downstream owner` column stays unchanged here and the Architecture form package retires it with a derived coverage check; the 8 NFR rows and the seven quality H3 of REQ-0004 move under Quality Requirements; the requirement tables take the columns `Requirement ID`, `Statement`, `Rationale` and `Acceptance`, with every requirement ID and statement unchanged and each rationale a sourced sentence or an explained none); user answers of 2026-11-14. The handoff row for the `Downstream owner` column is recorded with it.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REQFORM-001](../spec.md#success-criteria--verification-plan) | The form, the two local extensions, the profile lists, the TemplateDefinition and its three tables, the `relationship_contract` note and the tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-REQFORM-002](../spec.md#success-criteria--verification-plan) | The rationale table and its review; the template and the four Requirements by the heading map with the new columns; the three texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REQFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `60bca469…` and plan.md `e8e070e0…`; 2026-11-14 | FAIL | APPROVE-WITH-FIX: FIX 1, the byte-preservation hash compared cells in reading order, which the NFR move reorders, so the comparison must key by requirement ID. NITs on the version level, the base commit and the SPEC-0193 dependency. | no | none |
| EVD-002 | [VAL-REQFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"69ec0cdbb32422cb6d271469a7444b3c717564e5f6a5ab00a5e7466e617a4356","plan_sha256":"b0d265a1c0a85e3f52debeed9b59c3d535c3dafe5c62a61a7859b00626e9d204"} | PASS | Same reviewer, round 2 on 2026-11-14: FIX 1 resolved (comparison keyed by requirement ID), the four Requirements take a major raise and the template stays 0.1.0 per document-authoring.md line 233, the uncited-member count is exactly 10; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-REQFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0195 approval question naming spec.md 69ec0cdb and plan.md b0d265a1 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0195","SPEC-0195-PLAN-0001"],"reviewed_spec_sha256":"69ec0cdbb32422cb6d271469a7444b3c717564e5f6a5ab00a5e7466e617a4356","reviewed_plan_sha256":"b0d265a1c0a85e3f52debeed9b59c3d535c3dafe5c62a61a7859b00626e9d204","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REQFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-REQFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, `docs/99.templates/templates/requirements/requirement-package.template.md`, the four documents under `docs/01.requirements/`, `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py`, the forms sentence of `.agents/governance/document-authoring.md`, the SDLC forms bullet of `docs/99.templates/README.md` and the linking rules of `docs/01.requirements/README.md`), this package, `docs/03.specs/README.md`, the W03-D55 row, the `Downstream owner` handoff row, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of the work residue ledger, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: the `Archived Lineage` section of any Requirement, any requirement ID, statement, priority or acceptance cell, the `Downstream owner` column and the body contract, any architecture description, ADR, Spec, Plan or other Task, any script, the Requirement lifecycle domain, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; the rationale table before any document changes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan drafted; not yet reviewed or approved. Implementation not started.
