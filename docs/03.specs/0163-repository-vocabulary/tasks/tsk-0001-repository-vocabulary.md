---
title: "Repository Vocabulary"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0163-TSK-0001"
parent_ids: ["SPEC-0163-PLAN-0001"]
---

# Task: Repository Vocabulary

## Overview

This Task records the Repository Vocabulary change for [SPEC-0163](../spec.md) under its [Plan](../plan.md). The user approved the Spec and Plan on 2026-11-12 (EVD-002, EVD-003).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user repeated the instruction to continue every open item, with current v14.7 requirements prevailing over conflicting rules ([SPEC-0161](../../0161-w00-v14-7-delta-intake/spec.md) Task, EVD-018). The user answered "Approve these bytes" to the round-2 Spec and Plan. That answer neither accepts ADR-0058 nor a criterion, and authorizes no push, PR or merge.
- **Base:** branch `claude/w00-v14-7-intake` after `4956440a`.
- **Package contract:** `REPOSITORY-VOCABULARY.json` (`repository-vocabulary` v14.5), SHA-256 `b03ae3c00a4228de90d90b48c9a7af4b716492651d83b6deab128d9e3bc92fce`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | Failing vocabulary and Hangul tests, then the validator change. | platform | completed | PASS | EVD-006 resolves EVD-004. |
| WORK-002 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | ADR-0058, FR-0032, registry and template, glossary, SDLC table and the knowledge owners. | platform | ready | NOT_RUN | Pending ADR-0058 acceptance. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `6f8ac0dd…`, plan.md `e9da3a98…`; round 2 over spec.md `10137683…`, plan.md `192f97ec…`; 2026-11-12 | PASS | Round 1 REJECT: one BLOCK (ADR-0036 and four other owners declare the knowledge surface pointer-only) and seven FIXes (owner role text, contract version, Korean column, RFC declaration, Hangul matching, dispatch, template path, README and skill wording, traceability). Round 2 APPROVE, no BLOCK or FIX; notes applied in execution. | no | none |
| EVD-002 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent semantic review | {"spec_sha256":"8fa68d19802d5c9d52ae269b518f0520fa00afa4ac046f75d604f5346cb235d5","plan_sha256":"5999a7381fdc248dbd9d01c2a5613cbf6c68fbb74719ad7e4c72a07cf271f712"} | PASS | Same reviewer, round 3, 2026-11-12: both hashes matched; reversing only the version, status and two approved-wording edits reproduces the user-approved round-2 bytes `10137683…` and `192f97ec…`; verdict APPROVE. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0163 question dated 2026-11-12 Asia/Seoul; recorded bytes differ only by the approved status edits verified in EVD-002","review_ref":"EVD-002","scope":["SPEC-0163","SPEC-0163-PLAN-0001"],"reviewed_spec_sha256":"8fa68d19802d5c9d52ae269b518f0520fa00afa4ac046f75d604f5346cb235d5","reviewed_plan_sha256":"5999a7381fdc248dbd9d01c2a5613cbf6c68fbb74719ad7e4c72a07cf271f712","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion or ADR and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Vocabulary validator tests | `tests/test_validate_knowledge_surface.py` with the new tests on the unchanged validator, then with the validator change | NOT_RUN | Pending the implementation commit. | yes | none |
| EVD-005 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Glossary, registry and owner checks with exact-index QA | Knowledge validator, inline ID check, strict document checks and commit hooks | NOT_RUN | Pending ADR-0058 acceptance. | yes | none |
| EVD-006 | [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Vocabulary validator tests | `python3 -m unittest tests.test_validate_knowledge_surface` with the seven new tests on the validator at `5a8ba3dc`, then with the validator change; `python3 scripts/run-contract-tests.py --root . --suite tooling`; `python3 scripts/validate-knowledge-surface.py --root .`; `ruff check` and `ruff format --check` on both files; 2026-11-12 | PASS | RED: 15 run, 7 failed (valid vocabulary, empty table, bad ID, duplicate ID, missing owner, copied Latin span, copied Hangul span); the 8 existing tests passed. GREEN: 15 OK. Suite `tooling`: 7 modules, 162 tests OK. Tree: 2 pointer documents, 0 violations under Hangul matching. Ruff clean. | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan) | pending | none | Glossary and inline ID check | platform |
| [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | pending | none | Tests before and after the validator change | platform |
| [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | pending | none | ADR-0058 acceptance and owner updates | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec names by writer, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: ADR-0036's body; any policy rule's meaning
- **Approval Required**: ADR-0058 acceptance before the glossary is committed; criterion acceptance; any push, PR or merge
- **Static Validation**: contract suite, knowledge validator, strict document validators, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commits; the package commit can be reverted separately
- **Evidence Location**: this Task

## Verification Summary

Approval recorded; WORK-001 and WORK-002 are pending. Risk class `medium` (registry, validator, test and ADR change).
