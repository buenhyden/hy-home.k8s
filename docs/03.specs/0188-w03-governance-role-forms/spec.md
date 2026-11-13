---
title: "W03 Governance Role Forms"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0188"
---

# W03 Governance Role Forms Technical Specification (Spec)

## Overview

This approved change contract is the second of three packages that close handoff W03-H28 and decision W03-D26 of the W03 stage of the external v14.7 execution package. SPEC-0186 (closed; frozen source `31d527d0:docs/03.specs/0186-w03-small-local-forms/spec.md`) gave six of the nine Stage 99 local roles of W03-D20 their forms and left `reference-report`, `governance-document` and `provider-native`. On 2026-11-13 the user decided in W03-D34 that the 17 `.agents/roles/*.md` role files become a separate Stage 99 local role `governance-role` whose form requires eight H3 titles under `Current Contract`, while the two provider files (`.claude/provider.md` and `.codex/provider.md`) stay `governance-document` documents with an H2-only form. This package builds both forms. It depends on SPEC-0186 (the six small forms) and on SPEC-0187 (closed; frozen source `067c18e0:docs/03.specs/0187-w03-sdlc-policy-form/spec.md`) (`.agents/governance/sdlc.md` leaves `governance/contract` for `governance/rule`), and both land first: with SPEC-0187 landed, `governance-document` binds only `governance/provider` and its twin, so the role has one document kind and one form.

The role files' H3 titles are `Role`, `When to Use`, `Inputs`, `Outputs`, `Guardrails`, `Capability and Evidence`, `Handoff / Escalation` and `Postflight`, in that order, under the H2 `Current Contract`; a read-only inventory of 2026-11-13 found them in all 17 files with no H4 and no other H3. The package reuses the model of SPEC-0169 to SPEC-0186 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The [Task](tasks/tsk-0001-w03-governance-role-forms.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json` (two forms, the four profiles' H2 lists, the `governance/role` and `common/template-governance-role` role binding, the two twins' TemplateDefinition texts); `docs/99.templates/templates/governance/role.template.md` (the eight H3 with author prompts; the only template edit of this package); `docs/99.templates/contracts/document-profile.schema.json` (the role enum and the form enum); `scripts/document_contracts.py` (the `DocumentRole` and `FormId` literals and the comment above `DocumentRole`); `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py` and any test that pins the counts, the roles or the form list; the forms sentence of `.agents/governance/document-authoring.md` and the sentence of `docs/99.templates/README.md` that lists the local roles; the evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the 17 role files, the two provider files and `.agents/roles/README.md`, which move form-only and change no text; the six roles of SPEC-0186; `reference-report` and the research H3 titles (W03-D35 and W03-D36, package 3); `provider-native` (W03-D33); the binding of `sdlc.md` (SPEC-0187); the full TemplateDefinition record (W03-H15); `_workspace/workspace_execution_tasks/` (read-only input); phase 3.
- Form-only migration (W03-D01): no role file, provider file or other document changes a heading, sentence or table. The role template is a Stage 99 form source, not a governed document: its eight H3 are the form's own shape, as the skill template carries its H3. If SPEC-0187 or SPEC-0186 has not landed, this package waits; it does not absorb their changes. No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none. This package's own three files (`spec.md`, `plan.md` and the Task) fall under the open-package layer rule of SPEC-0184.

## Contracts

- **Role and form identifiers.** `DocumentRole` in `scripts/document_contracts.py` and the `document_role` enum of the schema gain `governance-role` after `governance-document` (27 to 28 roles). The `FormId` literal and the `form_id` enum gain `governance-document` and `governance-role` after `evaluation-results`, in that order (24 to 26 identifiers after SPEC-0186), and `registry.common_forms.forms` goes from 18 to 20 forms, the two new forms appended in `FormId` order (`governance-document`, then `governance-role`) after `evaluation-results`. The comment above `DocumentRole` that names the roles without a form is corrected to the one that remains, `provider-native`, plus `reference-report` until package 3. `common_forms.contract_id` stays `COMMON-DOC-FORM-1` for the list; each form says in its `extension_policy` that it is a Stage 99 local role under W03-D09, W03-D20, W03-D26 and W03-D34, not a COMMON-DOC-FORM-1 role.
- **Forms.** Each form carries `h1` `{{document_title}}`, the same `language_rule` string the other local forms carry, its `extension_policy`, and for each section `content`, `required_content`, `prohibited_content`, `empty_policy` `explain_none_or_not_applicable`, `validation_ids` (`FORM-STRUCTURE` and `FORM-CONTENT-REVIEW`) and `link_only`. A section id is the form id, the parent slug for an H3, and the slug of the title (for example `governance-role-current-contract-when-to-use`); ids are free text that the registry check requires to be unique, so `Handoff / Escalation` takes `governance-role-current-contract-handoff-escalation`. Every section is required and no extension is registered, because no document of these roles has another H3.

| Form | Title | Sections in order | `link_only` |
| --- | --- | --- | --- |
| `governance-role` | Governance Role | H2 Overview; Authority Boundary; Governance Context; Current Contract (H3 Role; When to Use; Inputs; Outputs; Guardrails; Capability and Evidence; Handoff / Escalation; Postflight); Validation and Refresh; Related Documents | `Related Documents` |
| `governance-document` | Governance Document | H2 Overview; Authority Boundary; Governance Context; Current Contract; Validation and Refresh; Related Documents (no H3) | `Related Documents` |

  That is 14 sections for `governance-role` (six H2, eight H3) and six for `governance-document`, 20 in all. `Related Documents` is a link list in all 17 role files and in both provider files (read-only inventory), so it is `link_only` true and every other section false. The `governance-document` form has no H3, and its `prohibited_content` for `Current Contract` states that a provider note does not take the role's eight H3, which `governance-role` owns.
- **Profiles.** The four profiles that bind the two roles (`governance/role` and `governance/provider` with their twins `common/template-governance-role` and `common/template-governance-provider`) get empty `sections.required`, `optional` and `forbidden` lists, because `REGISTRY_FORM_LEGACY_LISTS` refuses H2 lists on a profile whose role has a form; the headings then come from the form. The `governance/role` profile and its twin change `document_role` from `governance-document` to `governance-role`; the provider pair keeps `governance-document`. After SPEC-0187 no other profile binds `governance-document`: at HEAD the contract pair also does, and a stale binding left by SPEC-0187 stops this package.
- **Template.** `role.template.md` replaces the single `Current Contract` author prompt by the eight H3 titles, each with one `<!-- Author prompt: ... -->` comment, so the template-mode author-prompt check of `scripts/validation/repository/form_contracts.py` (the `canonical_form_content_errors` function) finds a useful prompt in the H2 section body, which holds the H3 text; its other five H2 sections, its frontmatter and its H1 do not change. `provider.template.md` does not change.
- **TemplateDefinitions.** The role twin says in its non-goal that `governance-role` has its own local form under W03-D09, W03-D20, W03-D26 and W03-D34 and is not a COMMON-DOC-FORM-1 role, and the provider twin says the same for `governance-document` under W03-D26; the non-goal about leaving the H2 lists as the profile records them says that the headings stay and the form now owns them (the role twin adds the eight H3); `consumer_paths` add `scripts/validate-document-contract-registry.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests that pin the role; the validation cases name the form tree check and the section ids instead of the H2 list and `BODY-HEADING-REQUIRED`; `tables` stay empty for both; `migration.meaning_map` names this package and records that the role template gains its eight H3.
- **Policy text.** `document-authoring.md` adds `governance-role` and `governance-document` to its Stage 99 local-role sentence (the one SPEC-0186 extends with the six small roles), not to the COMMON-DOC-FORM-1 list, and keeps the sentence that a template whose role has no form keeps its H2 lists for the roles that remain; the `docs/99.templates/README.md` sentence that lists the local roles is rewritten to say that `governance-role` and `governance-document` now have their own local forms and that `reference-report` and `provider-native` have none yet. Documents under `.agents/` and the templates stay English-only under `document_language`; only that README sentence is Korean.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and template definition ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes. Splitting the role from the provider note follows the one-role-one-form rule: the role files share an H3 shape the provider files do not, so one form cannot hold both without making the H3 optional.

## Data Modeling & Storage Strategy

Registry data: two forms with 20 sections (14 and 6) and no extension, four profiles with empty lists, two profiles rebound to the new role, two TemplateDefinitions with changed texts and no table. Code and schema: one role and two form identifiers. Template: one file with eight added H3.

## Interfaces & Data Structures

- `scripts/document_contracts.py` and the schema: `governance-role` in the role literal and enum, and the two form identifiers; `test_typed_stage_and_document_role_match_the_schema` and `test_typed_form_identifier_matches_the_schema_form_enum` in `tests/test_document_terminal_contract.py` compare them and fail first when only one side changes; their counts of 27 roles and 24 form identifiers (after SPEC-0186) become 28 and 26, and the set of roles without a form becomes `reference-report` and `provider-native`.
- `tests/test_common_form_tree.py`: `FORM_IDS` gains `governance-document` and `governance-role`; `LOCAL_ROLE_IDS` keeps the roles without a form and `ROLE_IDS` stays in schema role order; `test_schema_role_enum_is_twenty_seven_and_form_enum_stays_eighteen` (renamed by SPEC-0186 for 24 forms) becomes a 28-role and 26-form test; the eighteen-form constant and the tests named for it become twenty forms; the profile-to-role map binds `governance/role` to `governance-role`; the assertions that name `governance/role` and its twin move to the new role and every assertion that a profile of these roles has `form is None` flips; synthetic cases cover the `governance-role` tree, a missing, extra and reordered H3, a stray H3 in a `governance-document` tree, and a bare empty section.
- `tests/test_agent_governance.py`, `tests/test_validate_agent_registry.py` and the registry validators keep passing, because the role files and `.agents/roles/registry.json` are not edited.

## Edge Cases & Error Handling

- A form fixes H3 order, while the role profile had H2 lists only; the 17 role files already follow the eight-title order (read-only inventory), and the Task confirms it with the strict validators.
- The role template's H3 prompts must keep the template-mode author-prompt check passing; if the check required a prompt per H3, the template carries one for each of the eight.
- `.agents/roles/README.md` is a Stage README, not a `governance/role` document: the profile path pattern excludes it, and it does not change.
- If SPEC-0187 left `governance/contract` bound to `governance-document`, the provider form would still pass but the role would have two document kinds; the author stops and reports the dependency, not a form change.

## Failure Modes & Fallback / Human Escalation

Documents are expected to pass unchanged, so this package edits none of them. If any role file, provider file or template of these roles gains a diagnostic from the strict validators, the form is wrong and is fixed before commit, never the document; the author does not edit a governed document to satisfy a form. If a form cannot be written without a heading, sentence or table change in a document, the author stops and asks the user. If a script outside this list stops passing, the change is wrong and is reverted to the last passing step. After two failed attempts with no new information the author stops and reports a repository defect.

## Verification Commands

- Before and after, record the output of the four strict document validators; after must equal before (no new diagnostic and no removed one).
- `git diff --stat` over `.agents/roles/`, `.claude/provider.md` and `.codex/provider.md` is empty; over `docs/99.templates/templates/` it shows only `governance/role.template.md`.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-GOVROLE-001 | The registry, schema and literals hold the `governance-role` role, the two forms with their 20 sections, `link_only` Related Documents, no extension, the four profiles with empty lists, the role pair rebound, the two TemplateDefinitions with changed texts, and the role template with its eight H3 and author prompts; the role-parity, form-identifier parity and form tree tests fail first and then pass. |
| VAL-GOVROLE-002 | The 17 role files and the two provider files pass unchanged; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVROLE-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, schema, form and role-parity tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GOVROLE-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
