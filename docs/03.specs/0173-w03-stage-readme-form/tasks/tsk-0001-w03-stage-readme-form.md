---
title: "W03 Stage README Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0173-TSK-0001"
parent_ids: ["SPEC-0173-PLAN-0001"]
---

# Task: W03 Stage README Form

## Overview

This Task records the fifth phase-2 package of W03, the Stage README form, for [SPEC-0173](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-stage-readme-form` from `a34539c2` (SPEC-0172 closure; PR #237 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** on 2026-11-13 the user answered "Split them out" to the question of the four agent and provider READMEs, three of which name children only in code spans and would fail the collection complete-listing check (W03-D16).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Stage README (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[12]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinitions, tables, binding and navigation; the H4 table reader; tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-STAGEREADME-002](../spec.md#success-criteria--verification-plan) | 22 documents and two templates moved with the map; policy texts; regression and exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007; exact-index QA at the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `16c11916…`, plan.md `97ff8f74…`; 2026-11-13 | FAIL | REJECT: BLOCK three of the four agent and provider READMEs name children only in code spans and would fail the collection complete-listing check (ten diagnostics, reproduced in-process); BLOCK `link_only` was justified by a mechanism that never runs for router profiles; FIXes on a count, the D11 attribution, the classification rule for matrices outside Structure, three tests to rewrite and the Stage 03 README entry at the package commit. | no | none |
| EVD-002 | [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"deb199374da15bbc5e446bfccbb6e2c809d3ae6033334a0a4b57ae60d0537e22","plan_sha256":"a728dd549074d6f88fc62dd59fcb742a1fed5db83dc52262c9be68a34d6b2c5f"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: round 2 confirmed the user's W03-D16 split (the 22 stage and collection READMEs pass complete listing as they stand) and every round-1 fix, and asked three wording fixes (the Common forms bullet, a stale path-pattern phrase, the SPEC-0161 Task edits in scope); the author applied them; round 3 confirmed both hashes and that only those edits changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0173 approval question naming spec.md deb19937 and plan.md a728dd54 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0173","SPEC-0173-PLAN-0001"],"reviewed_spec_sha256":"deb199374da15bbc5e446bfccbb6e2c809d3ae6033334a0a4b57ae60d0537e22","reviewed_plan_sha256":"a728dd549074d6f88fc62dd59fcb742a1fed5db83dc52262c9be68a34d6b2c5f","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, bindings, tables, H4 reader and tests, red then green | Working tree over `f777b9a4`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_readme_navigation` 37 tests with 3 failures, `tests.test_repository_quality_rules` 14 with 3, `tests.test_common_form_tree` 126 with 20. Green: all three modules OK (one skipped base). The author compared the registry Stage README form with COMMON-DOC-FORM-1 1.0.0 roles[12]: sections equal apart from the added `link_only` false, `extensions` empty. Both template twins name the Stage README form, carry empty H2 lists, `Current Items` navigation with complete listing and a TemplateDefinition whose `Index` table has Path and Purpose required, Owner optional, minimum 0 rows, identity Path; every consumer path is a regular file. `_document_content_table` also reads `#### title` and still refuses an ambiguous title. | yes | none |
| EVD-005 | [VAL-STAGEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | 22 READMEs and two templates meaning map | Seven stage READMEs (`docs/README.md`, 01, 02, 03, 05, 90, 99) and 15 collection READMEs; implementer maps and word-multiset comparison, read by the author | PASS | Every source sentence is kept, moved under the form's H2 and H3 headings; old H3 headings became H4. Word comparison shows no removal; additions are Korean none-with-reason lines under form H3 headings without source text only. Placement calls for owner review: split Usage lists renumbered under Create and Review; Add and Find kept whole under Create and Review; the Stage 90 `In Scope` table moved under Classification; the Stage 99 scope sub-headings under Classification with Inputs and Outputs left as a none-with-reason line; the headingless need tables of the guides, policies and runbooks READMEs under Classification. `docs/05.operations/README.md` line 152 now points at the Operations Mutation Boundary that moved above it. The templates each carry 4 H2 and 8 H3 headings and an optional Index table. | yes | none |
| EVD-006 | [VAL-STAGEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged working tree after `f777b9a4`, 2026-11-13 | PASS | The four strict document validators exit 0 with output byte-identical to the before run at `f777b9a4`. `quality.py` PASS; markdownlint over the 25 edited Markdown files 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 461, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` 37 with the known default-branch error (SPEC-0161 W03-H11). `REFERENCE_PACK_INDEX_DRIFT` fails while the reference READMEs are unstaged and clears once staged. `.secrets.baseline` registry `source_revision` line 6437 moves to 6602 in its own commit. | yes | none |
| EVD-007 | [VAL-STAGEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 31 files over `f777b9a4` | PASS | Risk class `medium` (registry, validator code, tests and 22 router READMEs). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; the four agent and provider READMEs stay on their current binding (W03-D16); the H4 reader still requires one match; no check weakened; policy text `document-authoring.md` 3.11.0 and the `docs/99.templates/README.md` Common forms bullet; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-STAGEREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-STAGEREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md` (also one of the 22 documents), the W03-D16 and EVD-034 rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); criterion acceptance pending. Risk class `medium`.
