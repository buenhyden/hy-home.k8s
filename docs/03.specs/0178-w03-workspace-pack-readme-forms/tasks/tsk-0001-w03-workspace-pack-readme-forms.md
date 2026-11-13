---
title: "W03 Workspace and Reference Pack README Forms"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0178-TSK-0001"
parent_ids: ["SPEC-0178-PLAN-0001"]
---

# Task: W03 Workspace and Reference Pack README Forms

## Overview

This Task records the last phase-2 package of W03, the Workspace and Reference Pack README forms, for [SPEC-0178](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to follow the requirements where a choice or correction is needed, to check existing work before the next task, and approved commit, push, PR and merge. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-workspace-pack-readme-form` from `ed91d165` (SPEC-0177 closure; PR #242 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D09 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** asked which single index title the Reference Pack form uses, given `Report Index` in research and audit packs and `Item Index` in data packs, the user answered on 2026-11-13 "follow the requirements"; DOC-01 requires one form per README role, so following the W03-D10 `Pack Contract` pattern the title is `Pack Index` (W03-D19).
- **Requirement basis:** DOC-01 (same-role READMEs share one form) and the TEMPLATE-DEFINITION-CONTRACT note that the role table is not a closed list; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | Role list and schema; forms, local H3s, TemplateDefinitions, bindings and navigation; tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | Pack renames; policy texts; regression and exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007; exact-index QA at the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `7a4d9d23…`, plan.md `146a3cea…`, with a scratch simulation of both forms, the role additions, the bindings and the renames; 2026-11-13 | FAIL | REJECT: BLOCK research pack 0001's link-list `Related Documents` fails the empty-section check unless the section is `link_only`; BLOCK three sentences name a renamed heading in prose; FIXes on review-only closure enforcement, the `DocumentRole` literal and its parity test, a missing schema-enum test, and the form-level fields and local-form marking. The reviewer confirmed the requirements support two local roles and the `Pack Index` choice. | no | none |
| EVD-002 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"a102d0add1b7293f416a38e1ed6fbf49fdceae0d507164f6f0aebe24c300b466","plan_sha256":"59412d600de7fdade38bb420e0b2f774b7b12f9783a19502a517d69bf8671810"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed in the simulation, including the author's narrowing of the text search to the pack folders because `Item Index` is also an unrelated `.agents/` collection heading; no other change in meaning; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0178 approval question naming spec.md a102d0ad and plan.md 59412d60 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0178","SPEC-0178-PLAN-0001"],"reviewed_spec_sha256":"a102d0add1b7293f416a38e1ed6fbf49fdceae0d507164f6f0aebe24c300b466","reviewed_plan_sha256":"59412d600de7fdade38bb420e0b2f774b7b12f9783a19502a517d69bf8671810","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Roles, schema, forms, local H3s, TemplateDefinitions, bindings, navigation and tests, red then green | Working tree over `3dcc5027`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): the four affected test modules gave 326 tests with 49 failures and 11 errors before the registry change; `test_typed_stage_and_document_role_match_the_schema` failed alone after the schema change and passed once the `DocumentRole` literal matched. Green: all OK. `DocumentRole` and both schema enums gain `workspace-readme` and `reference-pack-readme` in the same order; each form's `extension_policy` marks it a Stage 99 local role under W03-D09/D10, not a COMMON-DOC-FORM-1 role; only `Related Documents` is `link_only`; the pack form keeps the twelve Spec sections with `Method` optional and the three closure sections conditional; the two local H3s under `Pack Contract` carry owner, verification, review and removal; eight bindings; four TemplateDefinitions with empty `tables`; navigation reads `Pack Index`. The data pack positives and consumers point to `docs/90.references/data/README.md`, since no data pack README exists yet. The Workspace profile is a router, so an empty section raises no diagnostic, as the Spec edge case states; a test records it. | yes | none |
| EVD-005 | [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Pack renames and policy texts | Staged diff over `894d0835`, read line by line by the author | PASS | Removed lines are only `Audit Contract`, `Research Contract` and `Data Contract` headings (now `Pack Contract`), `Report Index` and `Item Index` headings (now `Pack Index`), the three named prose sentences, and version and updated values; template frontmatter unchanged. `git grep -n -E 'Report Index\|Item Index\|Research Contract\|Audit Contract\|Data Contract' -- docs/90.references docs/99.templates/templates/references` is empty (rc 1). The seven `_workspace/` READMEs are byte-identical to `HEAD`. Policy texts: `document-authoring.md` 3.16.0 and `docs/99.templates/README.md` 0.28.0 name both local roles and the two section names. | yes | none |
| EVD-006 | [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged index after `894d0835`, 2026-11-13 | PASS | Strict `markdown-profiles`, `links-and-owners` and `document-lifecycle` output equal to the before run at `3dcc5027`; `document-contract-registry` PASS with 294 paths against 291, the difference being this package's three files. Staged lifecycle PASS; `python3 scripts/qa.py staged` 12 gates PASS. Suites: `agent-governance` 105, `ci-metadata` 87, `cluster-gate` 72, `document` 573 (3 skipped), `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK. `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. `.secrets.baseline` registry line 7266 moved to 7407 in `894d0835`. | yes | none |
| EVD-007 | [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 15 files over `894d0835` | PASS | Risk class `medium` (role literal, schema, registry, tests and four Stage 90 READMEs). Checklist: scope matches the Spec; one writer per file; W03-D09, W03-D10 and W03-D19 applied; no new COMMON-DOC-FORM-1 role claimed; Workspace README bodies unchanged; template frontmatter unchanged; the ignored read-only contract input was read only; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow file changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCALREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-LOCALREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D19 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, the seven Workspace README bodies, `_workspace/workspace_execution_tasks/`, Stage 90 report documents, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's standing 2026-11-13 instruction
- **Static Validation**: strict document validators, fragment search, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); criterion acceptance pending. Risk class `medium`.
