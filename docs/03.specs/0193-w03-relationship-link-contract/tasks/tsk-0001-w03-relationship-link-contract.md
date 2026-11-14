---
title: "W03 Relationship and Link Contract"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0193-TSK-0001"
parent_ids: ["SPEC-0193-PLAN-0001"]
---

# Task: W03 Relationship and Link Contract

## Overview

This Task records handoffs W03-H08 and W03-H16 (W03-D51): the registry `relationship_contract` section with its eight relations, seven relation kinds and four link types, its strict registry rules including the cycle rule, the supersession cycle observation, the `LINK-FRAGMENT` check and its fragment repairs, for [SPEC-0193](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to plan W03 phase 3 and answered its design questions. The request approves no Spec bytes or criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `de64c58d` (after PR #252, SPEC-0186) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-H08, W03-H16, W03-H02, W03-D03, W03-D11 and W03-D30.
- **Decisions recorded with this package:** W03-D49 (the phase-3 order of seven packages, Spec and Plan together and Task apart, TemplateDefinitions with each role's package), W03-D50 (a one-use form-only exemption for the SPEC-0161 Spec and Plan, retired at close; the SPEC-0161 Task moves form-only with a heading map), W03-D51 (the `relationship_contract` registry section, only `LINK-FRAGMENT` added now, the reciprocal carriers kept) and W03-D52 (the closed accepted-ADR list, an amending ADR for ADR-0059 Decision 5, Global Constraints under Overview, the promotion table unchanged under Promotion Map, other H3 demoted to H4) and W03-D65 (the requirement text governs a conflict with a current rule; four resolutions, text in the Spec); user answers of 2026-11-14. This package applies W03-D51 and the cycle clause of REQ only.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | The registry section with its 19 entries, the schema, the authority guard key, the loader, the four strict registry rules and their tests with suite and surface registration. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RELATION-002](../spec.md#success-criteria--verification-plan) | `LINK-FRAGMENT` and the supersession cycle observation with their tests; the fragment repairs; the two policy texts; the SPEC-0161 Task rows and, once the ledger exists, its entries; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over spec.md `c2e9c246…` and plan.md `66c057e5…`; 2026-11-14 | FAIL | APPROVE-WITH-FIX: FIX 1, the Plan dependency claimed no other open package edits the registry or the SPEC-0161 Task while SPEC-0187 to SPEC-0192 do, so the merge order and rebase rule must be stated; FIX 2, SPEC-0191 also adds an optional top-level registry key and must be named in the overlap note. NITs on the stale base commit, the owner of the 57 Spec-anchor links and a test for a lifecycle domain without `superseded`. | no | none |
| EVD-002 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"49f8d75879528108e7fdbbb72f1d174d9c0d3735a2d8446a1da1969cc62d0079","plan_sha256":"502c39527c858f672ddfac7e7bec44ddc5dca7e6a82e303f7daaa6c11748a2bb"} | PASS | Same reviewer, round 2 on 2026-11-14: FIX 1, FIX 2 and the NITs of EVD-001 are resolved and nothing new is false; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-003 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0193 approval question naming spec.md 49f8d758 and plan.md 502c3952 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0193","SPEC-0193-PLAN-0001"],"reviewed_spec_sha256":"49f8d75879528108e7fdbbb72f1d174d9c0d3735a2d8446a1da1969cc62d0079","reviewed_plan_sha256":"502c39527c858f672ddfac7e7bec44ddc5dca7e6a82e303f7daaa6c11748a2bb","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b460afe65c8dfd4f3341f88df3ab924f01f53469ea5583ff168b8a0eba5fba57","plan_sha256":"240be11460ec14fb626890ffd89acab14eaf438b01cf61d6211e8282735ba566"} | PASS | Independent review, three rounds on 2026-11-14 (W03-D65, W03-D66 and W03-D69 revisions): every FIX and NIT item applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-005 | [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all four to the SPEC-0193, SPEC-0196, SPEC-0198 and SPEC-0207 approval question naming spec.md b460afe6 and plan.md 240be114 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0193","SPEC-0193-PLAN-0001"],"reviewed_spec_sha256":"b460afe65c8dfd4f3341f88df3ab924f01f53469ea5583ff168b8a0eba5fba57","reviewed_plan_sha256":"240be11460ec14fb626890ffd89acab14eaf438b01cf61d6211e8282735ba566","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RELATION-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RELATION-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_authority.py`, `scripts/document_contracts.py`, `scripts/validate-links-and-owners.py`, `scripts/document_lifecycle.py`, `scripts/provider_write_guard.py`, `scripts/validate-document-lifecycle.py`, `tests/test_relationship_contract.py`, `tests/test_documentation_link_boundary.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, the link and relationship sentences of `.agents/governance/document-authoring.md`, the registry section list of `docs/99.templates/README.md`, and the link destinations of the documents whose fragments the new check reports), this package, `docs/03.specs/README.md`, the W03-D49 to W03-D52 and W03-D65 rows, evidence rows, the W03-H08 and W03-H16 closures and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of the work residue ledger once SPEC-0191 has merged, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any form, template, profile body contract, frontmatter key or lifecycle domain, any reciprocal field or column, any document content beyond the named sentences and fragment repairs, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan revised to 1.1.0 (eight relations, the cycle rules, the MAJOR bump and W03-D65) and awaiting re-approval; the EVD-001 to EVD-003 rows bind the earlier 1.0.0 bytes and are unchanged. Implementation not started.
