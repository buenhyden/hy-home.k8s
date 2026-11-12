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
| WORK-002 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | ADR-0058, FR-0032, registry and template, glossary, SDLC table and the knowledge owners. | platform | in-progress | PASS | EVD-007, EVD-008, EVD-010, EVD-011 and EVD-012 pass; completion waits for the operator's criterion acceptance. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Pre-approval review rounds | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `6f8ac0dd…`, plan.md `e9da3a98…`; round 2 over spec.md `10137683…`, plan.md `192f97ec…`; 2026-11-12 | PASS | Round 1 REJECT: one BLOCK (ADR-0036 and four other owners declare the knowledge surface pointer-only) and seven FIXes (owner role text, contract version, Korean column, RFC declaration, Hangul matching, dispatch, template path, README and skill wording, traceability). Round 2 APPROVE, no BLOCK or FIX; notes applied in execution. | no | none |
| EVD-002 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent semantic review | {"spec_sha256":"8fa68d19802d5c9d52ae269b518f0520fa00afa4ac046f75d604f5346cb235d5","plan_sha256":"5999a7381fdc248dbd9d01c2a5613cbf6c68fbb74719ad7e4c72a07cf271f712"} | PASS | Same reviewer, round 3, 2026-11-12: both hashes matched; reversing only the version, status and two approved-wording edits reproduces the user-approved round-2 bytes `10137683…` and `192f97ec…`; verdict APPROVE. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0163 question dated 2026-11-12 Asia/Seoul; recorded bytes differ only by the approved status edits verified in EVD-002","review_ref":"EVD-002","scope":["SPEC-0163","SPEC-0163-PLAN-0001"],"reviewed_spec_sha256":"8fa68d19802d5c9d52ae269b518f0520fa00afa4ac046f75d604f5346cb235d5","reviewed_plan_sha256":"5999a7381fdc248dbd9d01c2a5613cbf6c68fbb74719ad7e4c72a07cf271f712","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion or ADR and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Vocabulary validator tests | `tests/test_validate_knowledge_surface.py` with the new tests on the unchanged validator, then with the validator change | NOT_RUN | Pending the implementation commit. | yes | none |
| EVD-005 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Glossary, registry and owner checks with exact-index QA | Knowledge validator, inline ID check, strict document checks and commit hooks | NOT_RUN | Pending ADR-0058 acceptance. | yes | none |
| EVD-006 | [VAL-VOCAB-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Vocabulary validator tests | `python3 -m unittest tests.test_validate_knowledge_surface` with the seven new tests on the validator at `5a8ba3dc`, then with the validator change; `python3 scripts/run-contract-tests.py --root . --suite tooling`; `python3 scripts/validate-knowledge-surface.py --root .`; `ruff check` and `ruff format --check` on both files; 2026-11-12 | PASS | RED: 15 run, 7 failed (valid vocabulary, empty table, bad ID, duplicate ID, missing owner, copied Latin span, copied Hangul span); the 8 existing tests passed. GREEN: 15 OK. Suite `tooling`: 7 modules, 162 tests OK. Tree: 2 pointer documents, 0 violations under Hangul matching. Ruff clean. | yes | EVD-004 |
| EVD-007 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | ADR-0058 acceptance | Direct current-session user answer "Accept ADR-0058" to the acceptance question, 2026-11-12 Asia/Seoul; ADR-0058 first recorded `proposed` in `5ec2a995` | PASS | ADR-0058 moves to `accepted` 1.0.0 in the WORK-002 commit; it accepts no SPEC-0163 criterion. | yes | none |
| EVD-008 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Glossary, registry and owner checks | Worktree after `63afa49b` with WORK-002 staged: `python3 scripts/validate-knowledge-surface.py --root .`; inline set comparison of the glossary's common Term IDs with `REPOSITORY-VOCABULARY.json`; the four strict document validators; `validate-document-lifecycle.py --mode staged`; suites `document`, `tooling`, `agent-governance`; `validate-agent-governance.py`; 2026-11-12 | PASS | Knowledge surface: 3 documents, 0 violations. Common IDs: 33 of 33, equal to the contract set. First run found 10 `LINK-STAGE-BOUNDARY` hits (glossary pointed into numbered stages) and `LIFECYCLE-CREATE` (glossary created `active`); owners rerouted to stage READMEs and indexes, glossary first recorded `draft`. After that all four validators PASS. Suites: tooling 162, agent-governance 104 PASS; document first FAIL (3, see EVD-009), then 313 PASS. | yes | none |
| EVD-009 | [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Document contract suite | `python3 scripts/run-contract-tests.py --root . --suite document` on the WORK-002 worktree; 2026-11-12 | FAIL | `tests/test_document_frontmatter_negatives.py` pinned `TODAY = 2026-11-11` while using the live `.agents/governance/document-lifecycle.md` as its valid control; SPEC-0162 commit `f0aa80cf` set that file's `updated` to 2026-11-12, so `FM-FUTURE-DATE` failed 3 tests. Fixed in WORK-002 by judging the control on its own `updated` day; the 2999 future-date case keeps its strength. | yes | none |
| EVD-010 | [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Document contract suite | Same command after the test change; `ruff check` and `ruff format --check` on the test | PASS | 21 modules, 313 tests OK; ruff clean. | yes | EVD-009 |
| EVD-011 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Glossary, registry and owner checks with exact-index QA | Commit `a84381dd` (tree `56828abaaeb4771a47425e2e5f6c12614f89b799`); `python3 scripts/qa.py staged` and the commit hooks with the scratch venv; 2026-11-12 | PASS | 13 gates PASS: affected-surface-contract, agent-governance, document-contract-registry, document-contract-tests, document-lifecycle, document-lifecycle-tests, external-service-contracts, knowledge-surface, links-and-owners, markdown-profiles, repository-quality, selected-nonstyle, selected-style; the Staged QA Snapshot, commitizen and commit-message-exception hooks passed. With EVD-008 and EVD-010 this closes EVD-005. | yes | EVD-005 |
| EVD-012 | [VAL-VOCAB-001](../spec.md#success-criteria--verification-plan), [VAL-VOCAB-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Core-diff checklist | Diff `5c9b381f..a84381dd` outside `docs/03.specs` (18 files, 561 insertions, 53 deletions); risk class `medium`; 2026-11-12 | PASS | Acceptance matches VAL-VOCAB-001 to 003 (EVD-006, EVD-010, EVD-011). One writer per file, as SPEC-0161 Primary Writers assigns. Checks removed or weakened: none; `KNOWLEDGE-POINTER-EMPTY` kept after the table-reader refactor, the word pattern now also matches Hangul (stricter matching, tested in EVD-006), and the frontmatter negative test keeps its 2999 future-date case (EVD-009). No secret; `.secrets.baseline` moved one line only. No permission, trigger or protected action changed. Recovery: revert `a84381dd`, `5ec2a995` and `55467184`. Findings: NOTE, the glossary stays `draft` like the other `.agents/knowledge` maps (`domains.md`, `project-map.md`); no transition is needed for this criterion. No BLOCK or FIX open. | yes | none |

### SDLC Table Mapping

| Old row | Kept in `sdlc.md` (rule) | Moved to the glossary (meaning) |
| --- | --- | --- |
| Requirement | Stage 01 | TERM-REQUIREMENT |
| Architecture Description / ADR | Stage 02 | TERM-ARCHITECTURE-DESCRIPTION, TERM-ARCHITECTURE-DECISION |
| Spec / Plan / Task | One Stage 03 package; approval is not execution completion | TERM-SPEC, TERM-PLAN, TERM-TASK |
| GitHub Issue / Project | Link by ID or URL, no full copy, no two-way status sync, remote state needs observation | TERM-ISSUE |
| Policy / rule / contract / control | Placement in `.agents/governance/`, scripts and Stage 99; no parallel policy directories; `governance/rule` identity | TERM-POLICY, TERM-RULE, TERM-CONTRACT, TERM-CONTROL |
| Provider / Role / Agent | Native configuration is not runtime evidence | TERM-PROVIDER, TERM-ROLE, TERM-AGENT |
| Skill | Lives under `.agents/skills/`; discovery depends on the provider; a reference is not a registration | TERM-SKILL |
| Hook / Gate / validator / Fixture | A hook need not run QA; a fixture is never production policy input | TERM-HOOK, TERM-GATE, TERM-VALIDATOR, TERM-FIXTURE |
| QA / CI / CD | Local repository-static QA; hosted jobs' scope; Argo CD boundary | TERM-QA, TERM-CI, TERM-CD |
| Deployment / release | Neither follows from local validation or a commit | TERM-DEPLOYMENT, TERM-RELEASE-OPERATION |
| Guide / Runbook | Stage 05 | TERM-GUIDE, TERM-RUNBOOK |
| Evidence / archive | Task and Git own change evidence; Git owns recovery; Stage 98 is unvalidated history | TERM-EVIDENCE, TERM-ARCHIVE |

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

WORK-001 is complete (EVD-006). WORK-002 checks pass (EVD-007, EVD-008, EVD-010); a document-suite regression from SPEC-0162 was found and fixed (EVD-009, EVD-010). The core-diff checklist is EVD-012. The glossary stays `draft`, like the other knowledge maps. Risk class `medium` (registry, validator, test and ADR change).
