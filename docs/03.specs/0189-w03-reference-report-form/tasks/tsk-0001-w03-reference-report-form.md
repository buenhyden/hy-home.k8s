---
title: "W03 Reference Report Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0189-TSK-0001"
parent_ids: ["SPEC-0189-PLAN-0001"]
---

# Task: W03 Reference Report Form

## Overview

This Task records the `reference-report` form of handoff W03-H28 (W03-D35, W03-D36), for [SPEC-0189](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch from from `main` (set at commit time), after SPEC-0186 and SPEC-0188 land; checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D35, W03-D36, W03-D01 and W03-H28; the rows are recorded by SPEC-0186.
- **Decision recorded with this package:** no new decision row; the packages reuse W03-D35 and W03-D36.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | Form literal and schema; the form and its extensions; profile lists; table sections and definition texts; tests. | platform | in-progress | PASS | EVD-008 |
| WORK-002 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document and published-member proof; regression and exact-index QA. | platform | in-progress | DEFER | EVD-009, EVD-010, EVD-011, EVD-012, EVD-013, EVD-014 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only reviewer that wrote none of the package, over the drafts of the Spec and Plan; 2026-11-13 | PASS | Round 1 APPROVE over spec.md `6dbff37e…` and plan.md `a6158650…` with FIX-1 (validator code stays, tests move to a synthetic profile) and FIX-2 (`Sources` required content), applied to the drafts. | no | none |
| EVD-002 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"4c12f089355501d8f3ef48e1187079311dc920e7cf76d339d96529a056e5bc74","plan_sha256":"0ae492fef4b3c29564aab4cc61666ea6a8dcd8b60511346f7fc0c1dbde9a1e4a"} | PASS | Same reviewer: round 2 APPROVE over the final bytes named here. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0189 approval question naming spec.md 4c12f089 and plan.md 0ae492fe dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0189","SPEC-0189-PLAN-0001"],"reviewed_spec_sha256":"4c12f089355501d8f3ef48e1187079311dc920e7cf76d339d96529a056e5bc74","reviewed_plan_sha256":"0ae492fef4b3c29564aab4cc61666ea6a8dcd8b60511346f7fc0c1dbde9a1e4a","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"873116156b967590d62db619377bc6169f0518c05821fe52e85814f26cf3ca7a","plan_sha256":"70c2426ec5a6a5330d97c76c7f613f873910b4efed921af31e4da4973033c310"} | PASS | Same reviewer, 2026-11-14: after SPEC-0184 refused the layer frontmatter key, the only change from the EVD-003 bytes is the deleted layer line in spec.md and plan.md, confirmed as the only difference. APPROVE over the bytes named here; this row records a review, not an approval. | yes | none |
| EVD-005 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0185 to SPEC-0189 re-approval question naming spec.md 87311615 and plan.md 70c2426e dated 2026-11-14 Asia/Seoul","review_ref":"EVD-004","scope":["SPEC-0189","SPEC-0189-PLAN-0001"],"reviewed_spec_sha256":"873116156b967590d62db619377bc6169f0518c05821fe52e85814f26cf3ca7a","reviewed_plan_sha256":"70c2426ec5a6a5330d97c76c7f613f873910b4efed921af31e4da4973033c310","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-006 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | H3 title re-scan before the form is written | Script scan of the 17 authored files and three templates (fenced code and comments excluded) on `c0bbf371`, 2026-11-14 | PASS | Counts as the Plan fixes them: research 60 distinct (H2, H3) pairs, 18 shared by two or more documents and 42 in one; audit 5; data template 5; the six research template titles; 31 conditional H3 (Overview 1, Reference Type 1, Authority Boundary 1, Scope 4, Definitions / Facts 11, Sources 4, Review and Freshness 9) and 39 `local_h3` titles (33, 3 and 3); the three `Sources` titles of the 0002 m0001 report are `Findings`, `Limitations` and `Recommendations`; an order satisfying every document and template exists. | yes | none |
| EVD-007 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Reference-report form, form-identifier parity and form tree tests | `python3 -m unittest tests.test_common_form_tree tests.test_document_terminal_contract tests.test_reference_pack_routes` over the new and updated tests with the literal, schema, registry and policy texts unchanged, on `c0bbf371`, 2026-11-14 | FAIL | Red: 332 tests, 6 failures and 1 error (3 skipped): `test_typed_form_identifier_matches_the_schema_form_enum`, `test_schema_role_enum_is_twenty_eight_and_form_enum_is_twenty_seven`, `test_repository_registry_binds_clear_roles_and_carries_exactly_the_twenty_one_forms`, `test_repository_registry_loads_with_exactly_the_twenty_one_forms`, `test_valid_form_binds_to_every_profile_of_its_role`, `test_only_the_twenty_one_form_profiles_use_the_tree`, and the `setUpClass` error of `ReferenceReportFormTests` (no form in the registry). Expected failure before the change. | yes | none |
| EVD-008 | [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Reference-report form, form-identifier parity and form tree tests | Same command over the working tree with `reference-report` in the `FormId` literal and the schema form enum, the form (8 H2, 31 conditional H3, 39 `local_h3`), the six profiles with empty H2 lists, the nine tables on section ids and the three changed TemplateDefinition texts | PASS | Green: 355 tests OK (3 skipped, as at base); `ReferenceReportFormTests` 23 of 23 OK; role literal and enum 28, form literal and enum 27, `registry.common_forms.forms` 21 with `reference-report` last; `LocalRoleTableTests` and the heading-line template test run over a synthetic no-form registry. | yes | EVD-007 |
| EVD-009 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document validators before and after | The four strict validators (`validate-document-contract-registry.py`, `validate-markdown-profiles.py`, `validate-links-and-owners.py`, `validate-document-lifecycle.py`, each `--root . --mode strict`) run before any change and after the implementation | PASS | Output equal before and after for all four (diff empty): registry `baseline=0 new=294 uncovered=0 ambiguous=0` and 294 paths, markdown profiles 0 violations, links and owners valid, lifecycle strict PASS; the 17 authored files and three templates gain no diagnostic. | yes | none |
| EVD-010 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Published members and templates unchanged | SHA-256 of the 17 authored Stage 90 members and the three templates before any change and after the implementation; `git diff --stat -- docs/90.references docs/99.templates/templates`; `python3 scripts/validate-document-contract-registry.py --root .` | PASS | The hash lists are identical (20 files, 13 published members among the 17); the diff stat is empty; no `REFERENCE_PUBLISHED_REWRITE` is reported. The policy texts changed: `document-authoring.md` 3.23.0 to 3.24.0 and `docs/99.templates/README.md` 0.30.3 to 0.30.4. | yes | none |
| EVD-011 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Contract suites, affected surfaces, ruff and markdownlint | `python3 scripts/run-contract-tests.py --root . --suite document`, `document-lifecycle`, `agent-governance`, `validation-routing`; `python3 scripts/validate-affected-surfaces.py --root .`; `ruff check scripts tests`; `ruff format --check scripts tests`; `npx --no-install markdownlint-cli2` over `.agents/governance/document-authoring.md`, `docs/99.templates/README.md`, this Task and the SPEC-0161 Task; `graphify update .` | PASS | document 723 tests OK (3 skipped); document-lifecycle 24 OK; agent-governance 105 OK (17 roles, 51 projections); validation-routing 173 OK; affected surfaces paths=668 uncovered=0 ambiguous=0; ruff check clean and format clean (113 files); markdownlint 0 issues; graph updated. Repository-static evidence only. | yes | none |
| EVD-012 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Repository quality gate | `python3 scripts/validation/repository/quality.py --root .` in the author checkout | DEFER | Its only diagnostic is `.claude/worktrees/agent-a260fbbd5fe4b5005/graphify-out/graph.json is not a bounded strict UTF-8 regular file`, a file under a locally excluded (`.git/info/exclude`) agent worktree that no tracked path references; the change itself produced no quality diagnostic. Next owner: the operator or the staged QA on the exact index. | no | none |
| EVD-013 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Staged lifecycle check and strict validators on the index | `python3 scripts/validate-document-lifecycle.py --root . --mode staged` and the four strict validators over the index holding the implementation files (`.secrets.baseline` left unstaged), 2026-11-14 | PASS | Staged lifecycle PASS (`mode=staged`) over the index holding the nine implementation files and this Task; the four strict validators PASS with the same output as EVD-009 on the final tree. Not run here: `python3 scripts/qa.py staged`, commit hooks (EVD-014). | yes | none |
| EVD-014 | [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Exact-index QA and commit hooks | `python3 scripts/qa.py staged` and the commit hooks on the exact index | DEFER | Pending: not run by the implementing agent, which may not run `scripts/qa.py staged` or commit. The `.secrets.baseline` registry line moves from 8462 to 8417 and is left as an unstaged change for its own commit (step 3 of the commit order). Next owner: the main session, which commits through the hooks. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-REFFORM-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-REFFORM-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`; the profile schema form enum; `scripts/document_contracts.py` literal and comments; the named tests; the forms sentences of `.agents/governance/document-authoring.md` and `docs/99.templates/README.md`; `scripts/validate-markdown-profiles.py` and the heading-line path of `REGISTRY_TABLE_SECTION`, unchanged), this package, `docs/03.specs/README.md`, the W03-H28 row, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only), each edited document's `version` and `updated`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: any document under `docs/90.references/` (the 13 published members byte for byte; the four others unchanged), the three templates' text, the SPEC-0186 and SPEC-0188 roles, `provider-native`, `.github/workflows/`, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, the registry check, the `document`, `document-lifecycle`, `agent-governance` and `tooling` suites, `ruff check scripts tests`, markdownlint, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). After SPEC-0184 removed the `layer` key the new bytes were reviewed (EVD-004) and approved again (EVD-005). Implemented in the working tree (EVD-006 to EVD-013): the H3 re-scan matched the Plan, red tests (EVD-007), green tests (EVD-008), equal strict validators, unchanged members and templates, and the suites pass; the quality gate is DEFER in the author checkout because of an excluded local worktree file (EVD-012). Not committed; exact-index QA and the commit hooks (EVD-014) and criterion acceptance are pending.
