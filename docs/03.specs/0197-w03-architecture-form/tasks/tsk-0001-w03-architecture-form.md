---
title: "W03 Architecture Form"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0197-TSK-0001"
parent_ids: ["SPEC-0197-PLAN-0001"]
---

# Task: W03 Architecture Form

## Overview

This Task records the Architecture part of handoffs W03-H02 and W03-H13 and the second step of W03-D55: the COMMON-DOC-FORM-1 Architecture form with its two local H3 extensions, the description TemplateDefinition and tables, the move of the description template and the four active architecture descriptions, the completed citing rows, the `REQUIREMENT-COVERAGE` check and the removal of the Requirement `Downstream owner` column, for [SPEC-0197](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to continue W03 phase 3 in the order of W03-D49. The request approves no Spec bytes or criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `de64c58d` (after PR #252, SPEC-0186) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-H02, W03-H13, W03-D01, W03-D03, W03-D08, W03-D30, W03-D31, W03-D49, W03-D51, W03-D52, W03-D55 and W03-D56.
- **Decision recorded with this package:** W03-D57 (the `Constraints` table with the columns `Architecture ID`, `Constraint` and `Affected Components` is registered with `minimum_rows` 0 and no existing table is renamed; an `N/A —` line with a reason under a Requirement's Downstream Links is the explained exclusion that `REQUIREMENT-COVERAGE` reads); user answers of 2026-11-14.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ADFORM-001](../spec.md#success-criteria--verification-plan) | The form, the two local extensions, the description profiles' lists, the TemplateDefinition and its tables, and the form tree tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-ADFORM-002](../spec.md#success-criteria--verification-plan) | The description template and the four descriptions by the heading map, with the `arc42 coverage` links and any false positional word corrected. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-ADFORM-003](../spec.md#success-criteria--verification-plan) | The reviewed citing rows; `REQUIREMENT-COVERAGE` and its tests; the column removal; the `relationship_contract` entry; the texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ADFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `2d5ba811…` and plan.md `b647f5af…`; 2026-11-14 | FAIL | APPROVE-WITH-FIX: FIX 1, removing `Downstream owner` would drop the 20 description links on acceptance-only `N/A —` rows, which the disposition table did not cover. NITs on the registry source of the Downstream Links section, a failing test for a Requirement without that section, and the resulting Requirement versions. | no | none |
| EVD-002 | [VAL-ADFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"bc244aa2bf11b5e2b9a0820f886986f5510d7296fd29576d00099e2c3fecc762","plan_sha256":"742e4b520a7ae8aff1f72e2efee3198dc6ac9af0ccb5360fdfd565090730320e"} | PASS | Same reviewer, round 2 on 2026-11-14: FIX 1 resolved (the disposition table covers 36 cells and all 20 acceptance criteria are named by description rows) and the NITs are applied; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-ADFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0197 approval question naming spec.md bc244aa2 and plan.md 742e4b52 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0197","SPEC-0197-PLAN-0001"],"reviewed_spec_sha256":"bc244aa2bf11b5e2b9a0820f886986f5510d7296fd29576d00099e2c3fecc762","reviewed_plan_sha256":"742e4b520a7ae8aff1f72e2efee3198dc6ac9af0ccb5360fdfd565090730320e","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ADFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-ADFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-ADFORM-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, the description and requirement templates under `docs/99.templates/templates/`, the four descriptions under `docs/02.architecture/descriptions/`, the `Lifecycle Traceability` table and Downstream Links pointer line of the four Requirements under `docs/01.requirements/`, `scripts/validate-links-and-owners.py`, `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py`, `tests/test_documentation_link_boundary.py`, the forms sentence of `.agents/governance/document-authoring.md`, the SDLC forms bullet of `docs/99.templates/README.md` and the linking rules of `docs/01.requirements/README.md` and `docs/02.architecture/README.md`), this package, `docs/03.specs/README.md`, the W03-D57 row, the handoff closure, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of the work residue ledger, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any ADR, the `Archived Lineage` section of any document, any requirement ID, statement, rationale, priority or acceptance cell, any other part of a Requirement, any Spec, Plan or other Task, any other script, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; the citing-row table and the removed-cell table before any document changes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan drafted; not yet reviewed or approved. Implementation not started.
