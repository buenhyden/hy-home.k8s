---
title: "W03 Guide Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0169-TSK-0001"
parent_ids: ["SPEC-0169-PLAN-0001"]
---

# Task: W03 Guide Form

## Overview

This Task records the first phase-2 package of W03, the Guide form, for [SPEC-0169](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user asked, after the SPEC-0168 closure, to investigate every remaining, unverified, unreviewed, unconfirmed and unprogressed W03 item, continue each, and fix any existing rule that conflicts with current requirements to match them. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-phase2-forms` at `4d5dc5e7` (from `de5c31b0`, the SPEC-0168 closure on PR #233, plus SPEC-0161 decision and missing-item commits); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11 (EVD-025 to EVD-030); EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Guide (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[6]) and the package TemplateDefinition `tables` schema; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | Schema, registry form, extension, TemplateDefinition and table registry checks. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-GUIDEFORM-002](../spec.md#success-criteria--verification-plan) | Document table check. | platform | in-progress | PASS | EVD-005 |
| WORK-003 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | Template and GDE-0010 moved form-only with the meaning map; policy text; regression and exact-index QA. | platform | in-progress | PASS | EVD-006, EVD-007, EVD-008, EVD-009, EVD-010 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `e672f75f…`, plan.md `1bd60337…`; 2026-11-12 | FAIL | REJECT: BLOCK `REGISTRY_BODY_SECTION` (`scripts/document_contracts.py:1593`) refuses a form profile whose body-contract section is not in its empty H2 list, reproduced in memory; FIXes: three no-form tests in `tests/test_common_form_tree.py`, operations tests, the route of tables to authored profiles, an all-tables iterator, an ADR-0059 claim not in its text, the decision link, the second Promotion row's substance, the extension condition and removal, the `.secrets.baseline` commit order, and heading-list consumers (`form_contracts.py`, `quality.py`, `validate-links-and-owners.py`). | no | none |
| EVD-002 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"b1447f677232c8e032b9509aaec2d992692643801411fe2f9aa3e9ff62f52732","plan_sha256":"a6cec5aee38256cd5746d2b8d110cb0c5957057d33e307eedb9d91ff041b62d1"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-12: round 2 confirmed every round-1 finding closed (heading lists derived from the form for form profiles, tables copied from the template to its source profiles, body-contract table not checked twice) and APPROVE with four NOTEs; the author applied NOTEs 1, 2 and 4 to the files and recorded NOTE 3 and the multi-template rule as SPEC-0161 W03-H10 (`4d5dc5e7`); round 3 confirmed both hashes and that only those edits changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0169 approval question naming spec.md b1447f67 and plan.md a6cec5ae dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0169","SPEC-0169-PLAN-0001"],"reviewed_spec_sha256":"b1447f677232c8e032b9509aaec2d992692643801411fe2f9aa3e9ff62f52732","reviewed_plan_sha256":"a6cec5aee38256cd5746d2b8d110cb0c5957057d33e307eedb9d91ff041b62d1","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, derived heading lists and table registry checks, red then green | Working tree over `adba07c6`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-12 | PASS | Red (implementer log): `python3 -m unittest tests.test_common_form_tree` ran 40 tests with 27 failures and 22 errors before the code. Green: 75 tests OK. Covers the Guide form copied from COMMON-DOC-FORM-1 1.0.0 roles[6] (author compared sections, `h1`, `language_rule` and `extension_policy`: equal), the `guide-lifecycle-traceability` extension, the TemplateDefinition with `Steps` and `Lifecycle Traceability` tables, guide heading lists derived from the form, and the negatives table section outside the form, duplicate column key, `row_identity` not a column, Lifecycle keys differing from the body contract, guide profile with H2 lists, body-contract section not a required H2 of the form, and a definition without `tables`. The three no-form repository tests are rewritten to assert exactly the Guide form and definition. | yes | none |
| EVD-005 | [VAL-GUIDEFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Document table check, red then green | Same run | PASS | Inside EVD-004's red and green runs: reordered, missing and extra columns fail `BODY-TABLE-COLUMNS`; fewer rows than `minimum_rows` fail `BODY-TABLE-ROWS`; other tables in the section are ignored; H4 tables count; the body-contract table is skipped; only authored profiles are checked. | yes | none |
| EVD-006 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | User decision on consumer paths | Implementer first limited `consumer_paths` to the four Stage 99 files because `tests/test_task_execution_contract.py` `CompletionIndexTests.setUp` copies only `docs/99.templates` and its 8 tests then failed `REGISTRY_TEMPLATE_DEFINITION`; question naming the TemplateDefinition contract (every real Registry, Schema, Parser, Validator, Tests and guidance consumer) and the out-of-scope test file; 2026-11-12 Asia/Seoul | PASS | Direct current-session user answer "Full list + fixture fix (Recommended)". `consumer_paths` now lists the four Stage 99 files plus GDE-0010, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validation/repository/form_contracts.py` and `tests/test_common_form_tree.py`; the fixture copies every consumer path the registry names. This adds one test file to the Spec's scope by the user's decision; no assertion is weakened. | yes | none |
| EVD-007 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Regression over the tree and suites | Author run over the working tree after `414989ae`, 2026-11-12 | PASS | The four strict document validators exit 0 with output byte-identical to the before run at `adba07c6` (0 FAIL lines). `python3 -m unittest tests.test_task_execution_contract tests.test_common_form_tree` OK; operations section and lineage tests OK (84 with the form tree module). Suites: `document` 401 tests OK (22 modules), `agent-governance` 104 OK. `python3 scripts/validation/repository/quality.py --root .` PASS (form contracts, template parity, residue). `ruff check scripts tests` clean. `graphify update .` rc 0. `.secrets.baseline` registry `source_revision` line 6016 moved to 6100 in `414989ae` (detect-secrets reports the `grep -n` line). | yes | none |
| EVD-008 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | GDE-0010 meaning map | Diff of GDE-0010 1.6.0 to 1.7.0; implementer word-multiset comparison and author read | PASS | Outcome: Overview sentence 1, Audience and Goal sentences 1 and 2, the three reader bullets. Boundaries: Overview sentences 2 and 3 (no duplicated procedure; ADR-0048 owns the decision) and Audience sentence 3 (owners of commands, CI jobs and recovery). Environment: Prerequisites items 1 and 3. Permissions: items 2 and 4. Actions: Guidance sections 1 to 5 unchanged, headings now H4. Exceptions: the retired full/ci `NOT_RUN` bullet and the live-check bullet. Expected Result: the local PASS, fixed-count and aggregate-gate bullets. Troubleshooting: the retired-path bullet. Lifecycle Traceability under Verification unchanged. Related Documents removed; six links already inline. Added sentences (3, Korean in the guide): Outcome, a related-document line linking the Reference Maintenance Runbook; Environment, a none-with-reason line saying tool versions are not applicable because `scripts/README.md` owns the command implementation; Permissions, a related-document line linking the Agent Execution Policy. No other word added or changed. | yes | none |
| EVD-009 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Semantic review: risk class and core-diff checklist | Diff of 10 files over `414989ae` (about 1,330 lines added, 120 removed) | PASS | Risk class `medium` (registry, validator, test and governed document change). Checklist: scope matches the Spec plus the user-approved fixture (EVD-006); one writer per file; the form equals the external contract; ADR-0033 and ADR-0059 unchanged; no check weakened (heading lists derived so `REGISTRY_BODY_SECTION`, template author prompts, residue scope and link heading validity keep running; `REGISTRY_FORM_LEGACY_LISTS` stays on raw lists); policy text in `document-authoring.md` 3.7.0 and `docs/99.templates/README.md` 0.19.0; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |
| EVD-010 | [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Every contract suite and the remaining consumer-path fixtures | Author run over the working tree after `414989ae`, 2026-11-12; first implementation commit attempt refused by staged QA (`document-lifecycle` suite: 3 failures, `REGISTRY_TEMPLATE_DEFINITION` in fixtures that copy only part of the registry) | PASS | Under the user's EVD-006 decision, the same consumer-path copy is added to `tests/test_document_lifecycle_package_exit.py` (its template-source copy set) and `tests/test_document_artifact_identity.py` (one temporary root); no assertion changed. All suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 401, `document-lifecycle` 18 (after the fix), `release` 29, `tooling` 166, `validation-routing` 173 OK. `qa-runner` 37 tests, 1 error in `test_snapshot_keeps_a_default_branch_that_exists_only_as_remote_tracking`: `git branch -D master` fails because the fixture repository's initial branch name follows the local Git default; the test and `scripts/qa.py` are untouched by this change and staged QA does not select that suite here. Next owner for that environment dependency: W05. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-GUIDEFORM-001](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting the operator's acceptance | platform |
| [VAL-GUIDEFORM-002](../spec.md#success-criteria--verification-plan) | pending | EVD-005 | Awaiting the operator's acceptance | platform |
| [VAL-GUIDEFORM-003](../spec.md#success-criteria--verification-plan) | pending | EVD-006, EVD-007, EVD-008, EVD-009, EVD-010 | Awaiting the operator's acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, `tests/test_task_execution_contract.py`, `tests/test_document_lifecycle_package_exit.py` and `tests/test_document_artifact_identity.py` (consumer-path fixtures only, EVD-006, EVD-010), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document` and `agent-governance` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved at their exact bytes (EVD-003). WORK-001 to WORK-003 implemented with PASS evidence (EVD-004 to EVD-010); every criterion awaits the operator's acceptance. Risk class `medium`. Residual risk: a mistyped first header exempts a Steps table (stated in the Spec). Next owner: the operator for acceptance, then W03 for package exit and the next phase-2 role.
