---
title: "W03 Policy Rule ID Contract"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0194-TSK-0001"
parent_ids: ["SPEC-0194-PLAN-0001"]
---

# Task: W03 Policy Rule ID Contract

## Overview

This Task records Policy package 2 of handoff W03-H29 (W03-D42 to W03-D44): the rule ID contract in the registry, its schema, the two Policy templates, the validators and the tests, with one registered code per policy and no rule ID in any document, for [SPEC-0194](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `de64c58d` (after PR #252, SPEC-0186) and on the SPEC-0187 package commit `362f59c4`, and are checked against `main` before delivery. The package merges after SPEC-0187 to SPEC-0193.
- **Decisions reused:** SPEC-0161 W03-D27, W03-D41, W03-D42, W03-D43, W03-D44, W03-D65 and W03-H29.
- **Decision to record with this package:** W03-D53 (the adoption gate, the home of the code record, the definition position of an inline ID, the coverage floor, the Status values and the fifteen codes); the user's exact words are copied at commit time and the number is re-read then.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | The registry section and its schema, the authority key, the loader, `REGISTRY_POLICY_RULE_CODE`, the fifteen records, the table's condition, the `Status` extension, the conditional table in both definitions and both templates, and the changed Policy table tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-RULEID-002](../spec.md#success-criteria--verification-plan) | The six document rules and the adoption gate; `tests/test_policy_rule_ids.py`, its suite membership and its surface route; the generator's recorded authoring set if a rule reaches it. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-RULEID-003](../spec.md#success-criteria--verification-plan) | Policy texts; W03-D53, the W03-H29 state cell and the ledger entry; the unit inventory; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"50518f9348b9532db5612d9aea36e86d225705b94c3e47b5c5b6fff994c0c6e5","plan_sha256":"dfc78c0bbd5387c21bcd55a657571ac7e24069a63204a29bfb237884ab07c752"} | PASS | Read-only reviewer that wrote none of the package, 2026-11-14: APPROVE with NITs and no BLOCK or FIX; the user deferred NIT 1 (enforcing that a code changes only while pending) to Policy package 5 with the history no-reuse check, and NIT 2 to NIT 4 (trace fit, estimate totals, sized coverage risk) need no change. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes; NIT to package 5 to the SPEC-0194 approval question naming spec.md 50518f93 and plan.md dfc78c0b dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0194","SPEC-0194-PLAN-0001"],"reviewed_spec_sha256":"50518f9348b9532db5612d9aea36e86d225705b94c3e47b5c5b6fff994c0c6e5","reviewed_plan_sha256":"dfc78c0bbd5387c21bcd55a657571ac7e24069a63204a29bfb237884ab07c752","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"35c8ef63c42dc7cc5a27b7933e338fef655398afbc78e52d2a376d3b7df1c060","plan_sha256":"19fa102081d9f11d74bec2139e88f854bdd07153a590514a50c3cab855aed20d"} | PASS | Independent review on 2026-11-14 of the W03-D65 revision (conditional Rules table with four common columns and a registered Status extension per REQ:37, 310, 486, 742; Q-07 bound on permanence per REQ:143): APPROVE, with the reviewers' FIX and NIT items applied and confirmed over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all six to the policy package re-approval question naming spec.md 35c8ef63 and plan.md 19fa1020 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0194","SPEC-0194-PLAN-0001"],"reviewed_spec_sha256":"35c8ef63c42dc7cc5a27b7933e338fef655398afbc78e52d2a376d3b7df1c060","reviewed_plan_sha256":"19fa102081d9f11d74bec2139e88f854bdd07153a590514a50c3cab855aed20d","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RULEID-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-RULEID-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-RULEID-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_authority.py`, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, the two Policy templates, `tests/test_policy_rule_ids.py`, `tests/test_common_form_tree.py`, `tests/test_document_generator.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, the Policy sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`), this package, `docs/03.specs/README.md`, the W03-D53 row, an evidence row, the W03-H29 state cell and the frontmatter `version` and `updated` of the SPEC-0161 Task, the W03-H29 entry of `docs/03.specs/work-residue-ledger.json`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: the body of any of the fifteen policies beyond the one named sentence, any section of the shared Policy form, any other form, profile, lifecycle domain or frontmatter key, the glossary, the generator's code, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `python3 scripts/validate-document-contract-registry.py --root .`, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed and first-recorded on the earlier bytes (EVD-001/002); revised under W03-D65; awaiting re-approval of the current bytes. Implementation not started.
