---
title: "W03 Service README Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0174-TSK-0001"
parent_ids: ["SPEC-0174-PLAN-0001"]
---

# Task: W03 Service README Form

## Overview

This Task records the sixth phase-2 package of W03, the Service README form, for [SPEC-0174](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-service-readme-form` from `0f60ce3b` (SPEC-0173 closure, contained in `main` after PR #238 merged as `bfbb1bdf`); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08, W03-D10, W03-D11 and W03-D16; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** on 2026-11-13 the user answered "Service README (Recommended)" to the W03-D16 question of which form the four agent and provider READMEs use; they move with the implementation READMEs to the Service README form, amending W03-D10 for them (W03-D17).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Service README (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[13]); conditional content from `COMMON-ROLE-FORMS`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinitions, tables, bindings and navigation; tests. | platform | in-progress | PASS | EVD-006 |
| WORK-002 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | 21 documents and two templates moved with the map; policy texts; regression and exact-index QA. | platform | in-progress | PASS | EVD-004, EVD-005, EVD-007, EVD-008, EVD-009; exact-index QA at the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `224d5334…`, plan.md `5fc062ab…`; 2026-11-13 | FAIL | REJECT: BLOCK `tests/test_repository_quality_rules.py` mutates the `Example Role Matrix` heading by an H2-to-H3 pattern and would fail once the matrix is H4, and was not in scope; FIXes on the matrix count (fourteen, including `infrastructure/verify/`), PR #238 being merged, inventories placed by two rules, the old H2 disposition and unplaced headings, the named test changes, and the child-link wording. The reviewer confirmed the form equals roles[13], the navigation rule accepts `Service Role`, and no current table starts with `Command`. | no | none |
| EVD-002 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"7223bfca11e5b4c103871a5e48e15482a3e2f6a7a205dee8096e40792680b9d4","plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: round 2 confirmed every round-1 fix against the repository and every heading of the 21 documents and two templates placed by one rule, and asked one fix (the level of `Working Procedure` under Local Workflow); the author applied it; round 3 confirmed both hashes and that only that sentence changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0174 approval question naming spec.md 7223bfca and plan.md f6aba035 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0174","SPEC-0174-PLAN-0001"],"reviewed_spec_sha256":"7223bfca11e5b4c103871a5e48e15482a3e2f6a7a205dee8096e40792680b9d4","reviewed_plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec amendment review | {"spec_sha256":"fa31cfb2f81bd39d429ae7b0c04df1fe03111f4aceaa1466ef9d60c3013f3764","plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb"} | PASS | During WORK-002, `gitops/README.md` failed `README-NAV-ENUMERATION` (12, then 2 deep targets in `platform/`): the approved map put `Namespace Ownership Matrix` and the Overview paragraph on `platform/external-services` into the navigation section. The user chose to place the matrix under Supported Environment with a Spec fix; spec.md 1.1.0 removes the matrix from the Service Role list and sends content that would exceed the navigation limit to the H3 its content matches, naming both placements. Same reviewer, round 4, 2026-11-13: only those changes versus `7223bfca`, no check weakened, the paragraph fits Inputs and Outputs, and all 20 READMEs return no navigation finding; verdict APPROVE. | yes | none |
| EVD-005 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Spec amendment approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the amended SPEC-0174 approval question naming spec.md fa31cfb2 and plan.md f6aba035 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0174","SPEC-0174-PLAN-0001"],"reviewed_spec_sha256":"fa31cfb2f81bd39d429ae7b0c04df1fe03111f4aceaa1466ef9d60c3013f3764","reviewed_plan_sha256":"f6aba0350835c5fd19312448b9b22a9b03a83882401d8cb9a9db00c14383c6bb","validity":"confirmed","revocation":"none"} | PASS | Approves the amended Spec bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-006 | [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, bindings, table, navigation and tests, red then green | Working tree over `abfc636f`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_common_form_tree` and `tests.test_readme_navigation` 170 tests with 17 failures before the registry change; the `Example Role Matrix` mutation failed on the moved `examples/README.md` with the old `#{2,3}` pattern. Green: the three modules 184 tests OK (one skipped base). The registry Service README form is built from COMMON-DOC-FORM-1 1.0.0 roles[13] by the same mapping that reproduces the root and stage forms, `link_only` false, `extensions` empty; the four profiles bind `service-readme` with empty H2 lists; navigation reads `Service Role` (complete false); both template TemplateDefinitions carry `Commands` (Command and Output required, minimum 0 rows, identity Command) and consumer paths that are regular files. No validator code changed. | yes | none |
| EVD-007 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | 21 documents and two templates meaning map | Implementer maps (three doc-writer subagents; `secrets/README.md` moved by the author from the user-printed source and copied in by the user, because the `secrets/` read deny covers it) and a line comparison of every document against `HEAD`, read by the author | PASS | Every source line is kept; old H2 headings are removed, old H3 and H4 shift one level under the form H3 of the map; plain text precedes the H4s inside each form H3. Added lines are Korean none-with-reason lines or pointers to existing text only; each reason was checked against a sentence already in its document. Placement calls for owner review: Related links of aws and azure now precede `Current authority transfer`; the sample-app Policy link went to Inputs and Outputs and its Runbook link to Runbook Links; the azure/gitops runbook line points to Reference Links; Security Boundary pointer lines where a Scope paragraph forbids committing credentials; in `tests/README.md` the `Operations` H4 is left without body because its `Working Procedure` moved to Local Workflow, which its none line states; the gitops matrix and external-services paragraph as amended (EVD-004). | yes | none |
| EVD-008 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged working tree after `abfc636f`, 2026-11-13 | PASS | The four strict document validators exit 0; output equals the before run at `abfc636f` except the registry path count, which grows by this package's three files. `quality.py` PASS; markdownlint over the edited Markdown 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 468, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` 37 with the known default-branch error (SPEC-0161 W03-H11). `.secrets.baseline` registry `source_revision` line 6602 moves to 6753 in its own commit. | yes | none |
| EVD-009 | [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 30 files over `abfc636f` | PASS | Risk class `medium` (registry, tests, 21 router documents including `.github/repository-surface.md`). Checklist: scope matches the amended Spec; one writer per file; the form equals the external contract; W03-D17 applied; the matrix titles read by `document_content.py` stay unique at H4; navigation passes with no rule change; the owner references of `.github/repository-surface.md` remain; policy text `document-authoring.md` 3.12.0 and `docs/99.templates/README.md` 0.24.0; templates keep their frontmatter placeholder as in SPEC-0173; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SERVICEREADME-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SERVICEREADME-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D17 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/` other than `repository-surface.md`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed; `secrets/README.md` is a tracked router document and holds no secret value
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved by the user at their exact bytes (EVD-003); the Spec amended, reviewed and re-approved at 1.1.0 (EVD-004, EVD-005). WORK-001 and WORK-002 implemented with PASS evidence (EVD-006 to EVD-009); criterion acceptance pending. Risk class `medium`.
