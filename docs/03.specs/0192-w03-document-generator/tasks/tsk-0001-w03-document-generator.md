---
title: "W03 Document Generator"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0192-TSK-0001"
parent_ids: ["SPEC-0192-PLAN-0001"]
---

# Task: W03 Document Generator

## Overview

This Task records handoff W03-H27 (W03-D24): the document generator `scripts/document-generator.py`, its round-trip and negative tests and their registration, for [SPEC-0192](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 and 2026-11-14 (Asia/Seoul) the user asked to continue the remaining W03 items and approved commit, push, PR and merge in those requests. The requests approve no Spec bytes or criterion.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `8231f782` (after PR #250, SPEC-0185) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D24, W03-H27 and W03-D30.
- **Decision recorded with this package:** W03-D48 (the recommended answer to each of the ten design choices: the generable-profile rule; the pack anchor identity in `expected_artifact_id`; a Requirement refused until its creation state is repaired; no status input; no number allocation; `0.1.0` kept and the key table sentence corrected; the starter H1 kept; an absent parent refused; the `document` suite; the generator documented with a hand copy still valid); user answer of 2026-11-13. The new repair handoff row for the missing `sdlc/requirement` creation state is recorded with it.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GEN-001](../spec.md#success-criteria--verification-plan) | The command, the fill, the output check, the creation-state extraction, the round-trip tests, suite membership, surface routes and the `scripts` route carve-out. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-GEN-002](../spec.md#success-criteria--verification-plan) | Identity, parent, occupied-path and status refusals; the pack anchor identity in the profile check. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-GEN-003](../spec.md#success-criteria--verification-plan) | Remaining negative tests; policy texts and the key table sentence; SPEC-0161 Task rows and, once the ledger exists, its entries; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GEN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | FAIL | APPROVE-WITH-FIX over spec.md `24daff11…` and plan.md `2a809b10…`: FIX 1 (`scripts/document_lifecycle.py` and its tests in scope, because exposing the creation rule refactors a protected reader), FIX 2 (the merge order with SPEC-0191 for the W03-H27 closure and the repair handoff), FIX 3 (the carve-out from the generic `scripts` surface route) and one NIT (the `importlib` load of the hyphenated profile check), applied to the drafts. | no | none |
| EVD-002 | [VAL-GEN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"9115fd9a14acaeee90fcf3d10851d260ed397bde76deac6086b3f9304c0ed2a7","plan_sha256":"b711f42860f56bc5d8fb9d1c418c48e0fe89d02378efbfc9ee13272ce5585680"} | PASS | Same review: the round 1 verdict was approval with fixes, and FIX 1 to FIX 3 and the NIT are applied in the bytes named here; round 2 on 2026-11-14 confirmed every FIX resolved and gave APPROVE over these bytes. The approved bytes are the bytes named here; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-GEN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0192 approval question naming spec.md 9115fd9a and plan.md b711f428 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0192","SPEC-0192-PLAN-0001"],"reviewed_spec_sha256":"9115fd9a14acaeee90fcf3d10851d260ed397bde76deac6086b3f9304c0ed2a7","reviewed_plan_sha256":"b711f42860f56bc5d8fb9d1c418c48e0fe89d02378efbfc9ee13272ce5585680","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GEN-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-GEN-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |
| [VAL-GEN-003](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`scripts/document-generator.py`, `tests/test_document_generator.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, `scripts/validate-markdown-profiles.py` and `scripts/document_lifecycle.py` with their tests, the `version` entry of `frontmatter_keys` in `docs/99.templates/registry.json`, the generator sentences in `.agents/governance/document-authoring.md`, `docs/99.templates/README.md` and `scripts/README.md`), this package, `docs/03.specs/README.md`, the W03-D48 row, evidence rows, the W03-H27 closure, the new repair handoff row and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of `docs/03.specs/work-residue-ledger.json` once SPEC-0191 has merged, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any template, profile, lifecycle domain or the frontmatter schema, any existing document's content beyond the named sentences, the design, schema, script and checks of the work residue ledger, any recorded Task row, EVD row, decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge are approved by the user's requests in Inputs
- **Static Validation**: strict document validators, the `document`, `document-lifecycle` and `validation-routing` suites, `python3 scripts/validate-affected-surfaces.py --root .`, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
