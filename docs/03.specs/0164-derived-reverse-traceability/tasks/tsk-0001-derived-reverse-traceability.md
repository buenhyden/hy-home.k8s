---
title: "Derived Reverse Traceability"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0164-TSK-0001"
parent_ids: ["SPEC-0164-PLAN-0001"]
---

# Task: Derived Reverse Traceability

## Overview

This Task records the DOC-09 change for [SPEC-0164](../spec.md) under its [Plan](../plan.md). The user approved the Spec and Plan on 2026-11-12 (EVD-002, EVD-003).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user repeated the instruction to continue every open item, with current v14.7 requirements prevailing over conflicting rules ([SPEC-0161](../../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018). The user answered "Approve these bytes" to the SPEC-0164 question. That answer accepts no criterion and authorizes no push, PR or merge.
- **Base:** branch `claude/w00-v14-7-intake` after `e6157654`.
- **Requirement source:** package `REQUIREMENTS.json` DOC-09 (file SHA-256 `4c9da241ba185310048f3231815c04ed42dc7ce54c44e201f97e469f5945084b`).

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REVERSE-002](../spec.md#success-criteria--verification-plan) | Backlinks tool, test-first. | platform | completed | PASS | EVD-006 resolves EVD-004. |
| WORK-002 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | Remove the reciprocal rule everywhere; reword the traceability owners. | platform | in-progress | PASS | EVD-007 to EVD-010 pass; completion waits for the operator's criterion acceptance. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `f6f07036…`, plan.md `abf804af…`; round 2 over spec.md `dc93ba57…`, plan.md `c2c01840…`; 2026-11-12 | PASS | Round 1 REJECT: two BLOCKs (the skill, AD-0006 and Stage 05 cells were missing from scope; no stated search) and six FIXes (supersession evidence, parent-side columns, self-containedness, sentences to remove, tool details, named tests and schema `required`). Round 2 APPROVE with one FIX (search pattern), applied. | no | none |
| EVD-002 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent semantic review | {"spec_sha256":"71f17b06e6b7c11d69fe8b7879e2a50b2fc5989980fc6f1f97d9b2605e2b358a","plan_sha256":"ce6ebdbb3992483a99a1ad1779d61745237141ad7e96d041e12dcd5485e40338"} | PASS | Same reviewer, round 3, 2026-11-12: both hashes matched; reversing the listed edits reproduces the round-2 bytes; verdict APPROVE. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0164 question naming spec.md 71f17b06 and plan.md ce6ebdbb dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0164","SPEC-0164-PLAN-0001"],"reviewed_spec_sha256":"71f17b06e6b7c11d69fe8b7879e2a50b2fc5989980fc6f1f97d9b2605e2b358a","reviewed_plan_sha256":"ce6ebdbb3992483a99a1ad1779d61745237141ad7e96d041e12dcd5485e40338","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-REVERSE-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Backlinks tool tests | `tests/test_document_backlinks.py` before and after `scripts/document-backlinks.py` exists | NOT_RUN | Pending the implementation commit. | yes | none |
| EVD-005 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Reciprocal rule removal checks with exact-index QA | Repository search, `document` suite, strict document checks and commit hooks | NOT_RUN | Pending WORK-002. | yes | none |
| EVD-006 | [VAL-REVERSE-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Backlinks tool tests | `python3 -m unittest tests.test_document_backlinks` before and after adding `scripts/document-backlinks.py` at `f4fc3000`; `python3 scripts/run-contract-tests.py --root . --suite tooling` with the module registered; `ruff check` and `ruff format`; the tool on REQ-0003 in the tree; 2026-11-12 | PASS | RED: 4 tests, 4 errors (tool absent). GREEN: 4 OK. Suite `tooling`: 8 modules, 166 tests OK. Ruff clean after formatting. On the tree the tool lists the SPEC-0161 to SPEC-0164 documents that cite REQ-0003. | yes | EVD-004 |
| EVD-007 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Reciprocal rule removal | Worktree after `9c9fd469`: the `leftover-reciprocal-evidence` case in `tests/test_document_terminal_contract.py` before and after the removal; suites `document` and `tooling`; the four strict document validators; the Spec's `git grep` over `.agents`, `docs/AGENTS.md`, `docs/*/AGENTS.md`, Stage 01, 02 (descriptions), 05 and 99; 2026-11-12 | PASS | RED: the leftover key was accepted (`DocumentContractError not raised`). After removing 22 registry keys, the schema `required` entry and property, the loader field, `REGISTRY_BODY_RECIPROCAL`, the `BODY-LINK-RECIPROCAL` branch and `_links_back_to`, the leftover key is refused by `REGISTRY_BODY_FIELD`, the loader's exact-field check that runs before the schema (the Spec said the schema; the refusal is earlier, the outcome the same). Suites: document 312, tooling 166 PASS. Strict validators PASS with the four REQ-0003 back-link sentences removed. Search: only `document-lifecycle.md` Validation and Refresh and `sdlc.md` rule 5 (supersession, kept) and the REQ-0003 rejected-clause history sentence remain. | yes | none |
| EVD-008 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Reciprocal rule removal checks with exact-index QA | Commit `09293928` (tree `c9455a1fafd381adb0a952da43790556e319f0ed`); `python3 scripts/qa.py staged` and the commit hooks with the scratch venv; 2026-11-12 | PASS | 13 gates PASS, including document-contract-tests and document-lifecycle-tests; the Staged QA Snapshot, commitizen and commit-message-exception hooks passed. With EVD-007 this closes EVD-005. | yes | EVD-005 |
| EVD-009 | [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Forward relationship link regression | New `test_forward_relationship_link_still_fails_broken_or_wrong_profile` in `tests/test_documentation_link_boundary.py` over this package's `spec.md`: unchanged, a missing Requirement target, an AD-0006 target; a mutation copy with the profile branch disabled; suites `document` and `tooling`; `ruff check` and `ruff format --check`; 2026-11-12 | PASS | No test asserted `BODY-LINK-BROKEN` or `BODY-LINK-SOURCE-PROFILE` before; the removed back-link test was the only one near them. Unchanged: no finding; missing target: `BODY-LINK-BROKEN`; AD target: `BODY-LINK-SOURCE-PROFILE`. Mutation: fails with `'BODY-LINK-SOURCE-PROFILE' not found in []`; restored: passes. Suites document 313, tooling 166 OK; ruff clean. The test class name and the validator docstring no longer mention reciprocal evidence. | yes | none |
| EVD-010 | [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan), [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Core-diff checklist | Diff `f4fc3000..09293928` outside `docs/03.specs` (21 files, 221 insertions, 133 deletions) plus the EVD-009 change; risk class `medium`; 2026-11-12 | PASS | Acceptance matches VAL-REVERSE-001 to 003 (EVD-006 to EVD-009). One writer per file, as the Spec assigns. Checks removed: only `BODY-LINK-RECIPROCAL`, `REGISTRY_BODY_RECIPROCAL` and their test, as the Spec requires; forward link, profile and stage-boundary checks kept and now tested (EVD-009); supersession reciprocity untouched. No secret; `.secrets.baseline` moved one line only. No permission, trigger or protected action changed. Recovery: revert `09293928`, then `b784e418`. Findings: NOTE, `scripts/validation/registry.json` gained one exact path, `tests/test_document_backlinks.py`, under the existing knowledge-surface test surface, and `scripts/run-contract-tests.py` lists the module in `tooling`; the Spec said the registry stays unchanged. The entry maps a test file to a surface (`SURFACE-PATH-UNMATCHED` otherwise) and adds no gate, so the tool is still not a gate. NOTE, the leftover-key refusal comes from the loader (EVD-007). No BLOCK or FIX open. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REVERSE-001](../spec.md#success-criteria--verification-plan) | pending | none | Search and strict checks after WORK-002 | platform |
| [VAL-REVERSE-002](../spec.md#success-criteria--verification-plan) | pending | none | Backlinks tests before and after | platform |
| [VAL-REVERSE-003](../spec.md#success-criteria--verification-plan) | pending | none | Forward and schema negative cases and suites | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec names by writer, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: supersession code and its policy sentences; accepted ADR bodies
- **Approval Required**: criterion acceptance; any push, PR or merge
- **Static Validation**: `tooling` and `document` suites, strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commits; the package commit can be reverted separately
- **Evidence Location**: this Task

## Verification Summary

WORK-001 is complete (EVD-006); WORK-002 passes (EVD-007 to EVD-010, with the core-diff checklist in EVD-010) and waits for criterion acceptance. Parent-side link columns remain forward links until the common-forms work replaces them. Risk class `medium` (registry, validator and test change).
