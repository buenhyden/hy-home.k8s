---
title: "Shared Edition Consistency"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0157-TSK-0001"
parent_ids: ["SPEC-0157-PLAN-0001"]
---

# Task: Shared Edition Consistency

## Overview

This in-progress Task records the W01 edition gap and the execution of [SPEC-0157](../spec.md) under its [Plan](../plan.md). EVD-001 was observed before approval and is marked not required; The user approved the Spec and Plan on 2026-11-11 (EVD-006, EVD-007).

## Inputs

- **Request:** on 2026-11-11 (Asia/Seoul) the user asked to finish W00 first and then W01, and chose a new branch from the W00 closure commit for the W01 edition check. These answers do not approve this Spec or Plan, accept a criterion, or authorize a push or merge.
- **Upstream:** completed SPEC-0156 and SPEC-0158 at `18ef5024`, the base of branch `claude/w01-edition-check`.
- **Registry binding:** `docs/99.templates/registry.json` `shared_contract` with `contract_id` `WGOV-CORE`, `version` `3.0.0`, `stage` `adopted`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EDITION-001](../spec.md#success-criteria--verification-plan) | Focused tests RED, implementation, tests GREEN; the lifecycle policy sentence, which names no edition other than the adopted one. | platform | in-progress | PASS | EVD-008 passed RED then GREEN; EVD-010 retested after the review fix. |
| WORK-002 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan), [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | Negative copies, independent review, commit checks. | platform | in-progress | NOT_RUN | EVD-009 and EVD-010 passed; EVD-005 exact-index QA is pending. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Pre-approval edition gap demonstration | Disposable copy of HEAD `18ef5024` outside the repository; `docs/99.templates/README.md` changed to `WGOV-CORE / 3.1.0` and `.agents/governance/document-lifecycle.md` to `WGOV-CORE 3.1.0`, both staged; 2026-11-11 | PASS | Gap confirmed: on the unchanged copy the registry validator exits 0, and with both changes the registry, markdown-profile and links-and-owners validators in strict mode and `validate-agent-governance.py` all still exit 0. No current validator compares prose editions with the registry. | no | none |
| EVD-002 | [VAL-EDITION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests RED then GREEN | `python3 -m unittest tests.test_shared_contract_binding` before and after the implementation | NOT_RUN | Pending Spec and Plan approval. | yes | none |
| EVD-003 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Validator on current tree and negative copies | Current tree; disposable copies with a wrong edition and with the earlier projection and adoption faults | NOT_RUN | Pending implementation. | yes | none |
| EVD-004 | [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent read-only code review | Code, tests and scope | NOT_RUN | Pending; a reviewer that wrote none of the change. | yes | none |
| EVD-005 | [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and exact-index QA | Strict document validators, the staged lifecycle check and the active commit hooks on the exact index | NOT_RUN | Pending an authorized commit. | yes | none |
| EVD-006 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan), [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent semantic review | {"spec_sha256":"0f367bac227c123d2aa62027764359756a4fe66f8a019fa1ee54dba161439765","plan_sha256":"17289a5af19f3d47c87c274f69009dd191cca53f3c6a34dbca41925e1accc0d1"} | PASS | Read-only reviewer that produced no SPEC-0157 content, 2026-11-11: both exact hashes matched, verdict APPROVE, no BLOCK. One FIX: `enumerate_tracked_regular_paths` fails closed on the 17 tracked symlinks under `.claude/skills/`, so a bare `.claude` pathspec would fail; the implementation lists only `:(glob)<root>**/*.md`, which never selects those symlinks (EVD-008). NOTEs: pin the edition boundary in a test (done, EVD-008); history exclusions hold by construction because history lies outside the four scanned roots; the Spec scope omits `.secrets.baseline`, which the Plan allows; `shared_edition_surface_texts` is an extra public helper the Spec describes only as the tracked rule-surface reading. | yes | none |
| EVD-007 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan), [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-chat user message approve the SPEC-0157 Spec and Plan dated 2026-11-11 Asia/Seoul","review_ref":"EVD-006","scope":["SPEC-0157","SPEC-0157-PLAN-0001"],"reviewed_spec_sha256":"0f367bac227c123d2aa62027764359756a4fe66f8a019fa1ee54dba161439765","reviewed_plan_sha256":"17289a5af19f3d47c87c274f69009dd191cca53f3c6a34dbca41925e1accc0d1","validity":"confirmed","revocation":"none"} | PASS | Trusted direct user message in this chat on 2026-11-11 Asia/Seoul; EVD-006 is the separate exact-byte review. No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push or merge. | yes | none |
| EVD-008 | [VAL-EDITION-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused tests RED then GREEN | `python3 -m unittest tests.test_shared_contract_binding`; RED log SHA-256 `5fa4c81a94dda871e7c69e69727aeb0d3bf27eff114edd3685c28d4b1922077c`; then `scripts/document_contracts.py` `a649647b04a180bf33c7e8530aa094e0c0761b75b3075716a0cd99f92f61de96`, `scripts/validate-document-contract-registry.py` `c12960a26f39f035cf165dd3fec14f7fe3f573d1753e9cb259a68440acf591f6`, `tests/test_shared_contract_binding.py` `cccd90aa1473c7f8aba15c161f1ec687d0dd29ef24f33653488aa95c9cff4eea`; 2026-11-11 | PASS | RED: exit 1, `ImportError: cannot import name shared_edition_mismatches`. GREEN: 9 tests OK: both forms refused with path and line, matching, history, non-Markdown and edition-less mentions pass, an absent shared contract disables the check, the current rule surfaces pass, and the boundary test pins trailing punctuation, a Korean particle and a wrapped mention as refused, and `3.1` and `v3.1.0` as not editions. The 19 test modules that import the touched code ran 313 tests OK; ruff check and format passed. | yes | EVD-002 |
| EVD-009 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Validator on current tree and negative copies | Four disposable copies of HEAD `18ef5024` plus the working-tree changes, outside the repository; 2026-11-11 | PASS | Current tree and unchanged copy: registry validator `PASS ... 293 paths`, agent governance exit 0. Edition copy (`docs/99.templates/README.md` names `WGOV-CORE / 3.1.0`): exit 1, `FAIL REGISTRY_SHARED_EDITION_MISMATCH docs/99.templates/README.md: expected WGOV-CORE 3.0.0; actual line 23: WGOV-CORE 3.1.0`. Adoption without approval (`approval_ref` null): exit 1, `REGISTRY_SCHEMA`. Projection drift (code-reviewer model changed): agent governance exit 1, `AGENT-NATIVE-METADATA`. | yes | EVD-003 |
| EVD-010 | [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent read-only code review | Read-only reviewer that wrote none of the change, over the three code files at the EVD-008 hashes, the approved Spec and Plan and `git status`; 2026-11-11 | PASS | No BLOCK. The reviewer reran the 9 tests and the validator (exit 0, PASS line unchanged), saw a mismatch appended to `.agents/README.md` refused at line 100, confirmed `:(glob)<root>**/*.md` selects 132 regular tracked files and no symlink, and that a tracked `.md` symlink fails closed through `main()` with exit 1. One optional FIX, applied after the review: a hyphenated word such as `3.0.0-compatible` was read as a pre-release edition; a pre-release suffix must now contain a digit, and the boundary test covers it. NOTEs kept as designed: a mention wrapped across lines counts; only the first version after the ID is read, so `v3.1.0` and table cells are not editions; the path re-filter in the pure function serves the history tests; the inline test import was hoisted. After the fix: `scripts/document_contracts.py` `b5f8454af4882d1169046386b652495d06c4f6b4b52d514c07f8c9c8c34b04ce`, `tests/test_shared_contract_binding.py` `694a1d4c35d3394590ff8dba5b1008236134ee288a3667c5b3fff31e1332fd3b`, validator file unchanged; 9 focused tests OK, the 19 related test modules OK, ruff clean, the edition copy still exits 1 with the new rule. | yes | EVD-004 |
| EVD-011 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan), [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent semantic review | {"spec_sha256":"f338a0d26891fc26104eaf55603bb4a1ef4e13e6c197b0fddafdeed7233d68e4","plan_sha256":"e980e16a07a8685204f3c0d1a4d2833357e2396b31bb7b8c7767d9e6cdccfede"} | PASS | The first package commit was refused by `PLAN-PROMOTION`: the Plan promoted the rule to `scripts/`, which is not a current owner. The user chose to promote it to `.agents/governance/document-lifecycle.md`, so the Spec and Plan were amended and the EVD-006 and EVD-007 bytes are superseded. The same reviewer found round 2 BLOCK on the Task, whose path boundary still forbade the policy sentence, and a FIX to name the policy file's version bump; both were corrected. Round 3 matched these exact hashes and found no BLOCK or FIX. | yes | none |
| EVD-012 | [VAL-EDITION-002](../spec.md#success-criteria--verification-plan), [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-chat user message approving the amended SPEC-0157 Spec and Plan dated 2026-11-11 Asia/Seoul","review_ref":"EVD-011","scope":["SPEC-0157","SPEC-0157-PLAN-0001"],"reviewed_spec_sha256":"f338a0d26891fc26104eaf55603bb4a1ef4e13e6c197b0fddafdeed7233d68e4","reviewed_plan_sha256":"e980e16a07a8685204f3c0d1a4d2833357e2396b31bb7b8c7767d9e6cdccfede","validity":"confirmed","revocation":"none"} | PASS | Trusted direct user message in this chat on 2026-11-11 Asia/Seoul approving the amended bytes reviewed in EVD-011; it supersedes the EVD-007 receipt, whose bytes changed. No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-EDITION-001](../spec.md#success-criteria--verification-plan) | pending | none | EVD-008 passed; waits for EVD-005 and operator acceptance. | platform |
| [VAL-EDITION-002](../spec.md#success-criteria--verification-plan) | pending | none | EVD-009 passed; waits for EVD-005 and operator acceptance. | platform |
| [VAL-EDITION-003](../spec.md#success-criteria--verification-plan) | pending | none | EVD-010 passed; waits for EVD-005 and operator acceptance. | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0157-shared-edition-consistency/`, `docs/03.specs/README.md`, one back-link sentence in the Traceability section of `docs/01.requirements/0003-workspace-agent-governance-platform.md`, `scripts/document_contracts.py`, `scripts/validate-document-contract-registry.py`, `tests/test_shared_contract_binding.py`, one sentence in `.agents/governance/document-lifecycle.md` with its patch `version` bump (2.5.0 to 2.5.1) and `updated` date, and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret
- **Forbidden Paths**: every other repository path, including `docs/99.templates/registry.json`, any other governance policy text, provider settings, `.github/`, completed Spec packages, the archive, `CHANGELOG.md` and the package under `_workspace/`
- **Approval Required**: Spec and Plan approval of the amended bytes is recorded (EVD-012). Criterion acceptance and any commit, push, PR or merge are pending.
- **Static Validation**: focused unit tests, the strict document checks in `docs/AGENTS.md`, `validate-document-lifecycle.py --mode staged` and the active commit hooks
- **Live Validation**: N/A; no runtime behaviour is claimed.
- **Secret / Vault Handling**: no secret, token or private memory body was read or printed
- **Rollback Plan**: revert the commits of this package; the check, its tests and the documents leave together
- **Evidence Location**: this Task

## Verification Summary

The W01 edition gap is confirmed on a disposable copy (EVD-001). The user approved the Spec and Plan (EVD-007). The focused tests went RED then GREEN (EVD-008), and the validator refuses a wrong edition while the earlier refusals still fail (EVD-009). The independent code review passed, and its one optional fix was applied and retested (EVD-010). Exact-index QA (EVD-005) is NOT_RUN until the commit.
