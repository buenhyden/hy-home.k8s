---
title: "W03 Full TemplateDefinition Record"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0196-TSK-0001"
parent_ids: ["SPEC-0196-PLAN-0001"]
---

# Task: W03 Full TemplateDefinition Record

## Overview

This Task records handoff W03-H15 and the rest of W03-H28: the function that derives the 19-field TemplateDefinition record, its schema, the stored `contract_version`, the registry rule and tests over every template, and the retirement of the heading-line table path, for [SPEC-0196](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes or criterion; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `de64c58d` (after PR #252, SPEC-0186) and are checked against `main` after SPEC-0188 to SPEC-0195 land.
- **Decisions reused:** SPEC-0161 W03-H15, W03-H28, W03-H13, W03-D01, W03-D09, W03-D20, W03-D26, W03-D33 to W03-D36, W03-D45, W03-D47, W03-D49, W03-D51 and W03-D65 (recorded by SPEC-0193; its third resolution is applied here).
- **Decision recorded with this package:** W03-D56 (a tracked byte copy of the package schema with a pinned SHA-256; `contract_version` stored on each definition; a full record with empty `headings` for `provider-native`, that one finding tolerated; the heading-line path retired here after its replacement refusal; the function, check and tests only, with no print command and no tracked output); user answer of 2026-11-14.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | The schema copy and its digest pin, `contract_version` in the profile schema and the definitions, the function, `REGISTRY_TEMPLATE_RECORD` and the record and negative tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-TDREC-002](../spec.md#success-criteria--verification-plan) | The consumer-zero list, the replacement refusal and the removal of the heading-line rule, branch, helpers, tests and wording. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-TDREC-003](../spec.md#success-criteria--verification-plan) | Policy texts; the W03-D56 row of the SPEC-0161 Task, the closure of W03-H15 and W03-H28 and their ledger entries; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"3011638a39c48ba3ea7fd41b08d5b3cac042da84afc5769fc0d675b1cb9cda1d","plan_sha256":"79c8432a65c132cda0aaed5e1af64160cdcd41f3517196f9a4582230580216c5"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-14: APPROVE with NITs and no BLOCK or FIX; the NITs (Spec merge-order wording, provenance of the copied schema whose title is Korean and names v14.5, purity of scripts/document_language.py) are handled at implementation and recorded in this Task. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0196 approval question naming spec.md 3011638a and plan.md 79c8432a dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0196","SPEC-0196-PLAN-0001"],"reviewed_spec_sha256":"3011638a39c48ba3ea7fd41b08d5b3cac042da84afc5769fc0d675b1cb9cda1d","reviewed_plan_sha256":"79c8432a65c132cda0aaed5e1af64160cdcd41f3517196f9a4582230580216c5","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"69f6462ee4415ecef6d2c83970c121abd7360865c74dc3766a986e205820f424","plan_sha256":"aba1606e876f2b81e3ac3c174916b5f429e4d04d6e4acba86954af2ab98384cb"} | PASS | Independent review, three rounds on 2026-11-14 (W03-D65, W03-D66 and W03-D69 revisions): every FIX and NIT item applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all four to the SPEC-0193, SPEC-0196, SPEC-0198 and SPEC-0207 approval question naming spec.md 69f6462e and plan.md aba1606e dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0196","SPEC-0196-PLAN-0001"],"reviewed_spec_sha256":"69f6462ee4415ecef6d2c83970c121abd7360865c74dc3766a986e205820f424","reviewed_plan_sha256":"aba1606e876f2b81e3ac3c174916b5f429e4d04d6e4acba86954af2ab98384cb","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-005 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"6e13a77cbf1a6ec5e8144a121f4039580cef1cf51d2348185da44bb9bddc1000","plan_sha256":"aba1606e876f2b81e3ac3c174916b5f429e4d04d6e4acba86954af2ab98384cb"} | PASS | Read-only audit of the pending packages against main 035143d1 and decisions W03-D70 to W03-D76, 2026-11-14: stale statements corrected (fixed registry version value, stale baseline or merge order); every other byte unchanged (checked by diff). | yes | none |
| EVD-006 | [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Re-approve all three (Recommended) to the re-approval question naming the new bytes of SPEC-0196, SPEC-0205 and SPEC-0209, here spec.md 6e13a77c and plan.md aba1606e, 2026-11-14","review_ref":"EVD-005","scope":["SPEC-0196","SPEC-0196-PLAN-0001"],"reviewed_spec_sha256":"6e13a77cbf1a6ec5e8144a121f4039580cef1cf51d2348185da44bb9bddc1000","reviewed_plan_sha256":"aba1606e876f2b81e3ac3c174916b5f429e4d04d6e4acba86954af2ab98384cb","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TDREC-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-TDREC-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-TDREC-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `docs/99.templates/contracts/template-definition.schema.json`, `docs/99.templates/contracts/document-profile.schema.json`, the `template_definition` entries of `docs/99.templates/registry.json`, `tests/test_common_form_tree.py` and any test that pins the definition key set, the TemplateDefinition sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, the W03-D56 row, evidence rows, the closure of W03-H15 and W03-H28 and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of `docs/03.specs/work-residue-ledger.json`, `scripts/document_authority.py`, `scripts/provider_write_guard.py` and `scripts/validate-document-lifecycle.py` (the MAJOR constant, the guard constant and the readable set of the expected bump), `.secrets.baseline` (this Task's reviewed digests and shifted registry lines only)
- **Forbidden Paths**: any form, section, extension, profile heading list or lifecycle domain of the registry, any template file, any governed document body beyond the named sentences, the H2-list model and its checks, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `python3 scripts/validate-work-residue-ledger.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan revised to 1.1.0 (the `provider-native` extension record, `REGISTRY_TEMPLATE_EXTENSION`, the MAJOR bump and W03-D65) and awaiting re-approval; the EVD-001 and EVD-002 rows bind the earlier 1.0.0 bytes and are unchanged. Implementation not started.
