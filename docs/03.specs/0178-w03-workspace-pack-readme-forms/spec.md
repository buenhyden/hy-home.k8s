---
title: "W03 Workspace and Reference Pack README Forms"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0178"
---

# W03 Workspace and Reference Pack README Forms Technical Specification (Spec)

## Overview

This approved change contract is the tenth and last phase-2 package of the W03 stage of the external v14.7 execution package. W03-D09 and W03-D10 give two README kinds their own role, form and TemplateDefinition instead of a COMMON-DOC-FORM-1 role: the Workspace README (`common/readme-workspace-staging`, seven READMEs under `_workspace/` outside the read-only input folder, and one template) and the Reference Pack README (the research, audit and data pack profiles under `docs/90.references/`, three READMEs and three templates, one form). DOC-01 requires READMEs of one role to use one form; W03-D10 merges `Research Contract` and `Audit Contract` into `Pack Contract` and makes the succession and closure sections conditional. The index section is `Report Index` in research and audit packs and `Item Index` in data packs; on 2026-11-13 the user answered "follow the requirements" to that choice, so one form takes one title and, following the W03-D10 pattern, both become `Pack Index`; the data pack's `Refresh and Retention` becomes conditional like the two closure sections W03-D10 names (W03-D19). It reuses the model of SPEC-0169 to SPEC-0177 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D19 is added there by this package's first commit. The [Task](tasks/tsk-0001-w03-workspace-pack-readme-forms.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; `docs/99.templates/contracts/document-profile.schema.json` (role and form enums, and the descriptions that call every form a COMMON-DOC-FORM-1 form); `scripts/document_contracts.py` (the `DocumentRole` literal and the same description); the three pack READMEs and the three pack templates; in `docs/90.references/audits/0001-sdlc-governance/README.md` and `docs/90.references/research/README.md` only the sentences that name a renamed heading; the Workspace README template only if its TemplateDefinition needs it; `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py`, `tests/test_readme_navigation.py`, `tests/test_reference_pack_routes.py` and any test that pins these profiles' lists, navigation sections or the role list; the forms sentence of `.agents/governance/document-authoring.md` and the forms bullets of `docs/99.templates/README.md`; the W03-D19 row, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the seven Workspace READMEs' text, which already has the form; `_workspace/workspace_execution_tasks/` (read-only input); Stage 90 report documents; H06, H07 and phase 3.
- Form-only migration (W03-D01): no sentence changes meaning; the only heading changes are the decided renames to `Pack Contract` and `Pack Index`, and the only text changes are the three sentences that name a renamed heading literally (audit pack lines naming `Report Index` and `Audit Contract`, and the research collection README naming `## Report Index`). Korean prose that describes a section without naming its heading stays. No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Roles.** The `DocumentRole` literal in `scripts/document_contracts.py` and the role and form enums of `document-profile.schema.json` gain `workspace-readme` and `reference-pack-readme`, in the same order; the requirements state that the role table is not a closed list (W03-D09, W03-D10). `common_forms.contract_id` stays `COMMON-DOC-FORM-1` for the list; each local form says in its `extension_policy` that it is a Stage 99 local role under W03-D09 and W03-D10, not a COMMON-DOC-FORM-1 role, and the schema and code descriptions that call every form a COMMON-DOC-FORM-1 form say the list also holds such local forms.
- **Workspace README form.** `common_forms.forms` gains `workspace-readme` (`title` `Workspace README`), the current shared form of the seven READMEs and their template: Overview; Scope (Permitted Artifacts, Forbidden Local State); Structure; Usage (Promotion and Cleanup, Tracking Rules); Related Documents; every section required, `link_only` false except `Related Documents`, which is `link_only` true because it is a link list, no extension. Each form carries `h1` `{{document_title}}`, the README `language_rule` that the Stage README form uses, and its `extension_policy`; each section carries `content`, `required_content`, `prohibited_content`, `empty_policy` and `validation_ids` written for its present use, as the other forms do. `common/readme-workspace-staging` and its twin get `document_role` `workspace-readme` and empty H2 lists; no document text changes.
- **Reference Pack README form.** `common_forms.forms` gains `reference-pack-readme` (`title` `Reference Pack README`): Overview, Scope, Pack Contract, Method (optional), Structure, Pack Index, Usage, Refresh and Succession (conditional: research pack), Review and Closure (conditional: audit pack), Refresh and Retention (conditional: data pack), Evidence Boundary and Related Documents, in that order, `link_only` false except `Related Documents`, which is `link_only` true because research pack 0001 holds only a link list there and the pack profiles are authored. `Method` exists today only in the profiles' optional lists, in no document or template; its position after `Pack Contract` is a decision of this package, not a carry-over. Two registered conditional local H3s under Pack Contract keep the research-pack sections that research pack 0001 holds today: `External Finding Vocabulary` and `Separate Evidence Axes`, each with owner, verification (the form tree check), review (when the form changes) and removal (when the form gains a matching section). `reference/research-pack`, `reference/audit-pack`, `reference/data-pack` and their three twins get `document_role` `reference-pack-readme` and empty H2 lists.
- **Renames (W03-D10, W03-D19).** In the three pack READMEs and three templates, `Research Contract`, `Audit Contract` and `Data Contract` become `Pack Contract`, and `Report Index` and `Item Index` become `Pack Index`; section bodies do not change except the named sentences above. No link in the tree names the old anchors, and after the change a text search for the old titles in the pack READMEs, the Stage 90 collection READMEs and the pack templates finds none; the unrelated `Item Index` H4 headings of `.agents/` collection READMEs and their test fixture are another section and stay.
- **Navigation.** `readme_navigation` for the three pack profiles reads `Pack Index`, `complete` stays `true`.
- **Tables.** The requirements define no conditional table for these two local roles, and the current index contents differ (a list in the audit pack, tables with different headers in the research packs), so both TemplateDefinitions carry `tables` as an empty list.
- **TemplateDefinitions.** One on the Workspace twin and one on each pack twin, each with purpose, responsibility, non-goals, policy references (`document-authoring.md`, `document-lifecycle.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (registry, schema, its template, its documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-links-and-owners.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Policy text.** `document-authoring.md` adds the two local README roles to the roles that use their registry forms; `docs/99.templates/README.md` says in its forms bullets that Workspace READMEs and reference pack READMEs use their own forms, naming `Pack Contract` and `Pack Index`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and README navigation ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data: two forms, two local extensions, four TemplateDefinitions with empty tables, eight profiles' lists and bindings, three navigation sections. Code and schema: two role identifiers.

## Interfaces & Data Structures

- `scripts/document_contracts.py` and the schema: the two role identifiers; `test_typed_stage_and_document_role_match_the_schema` in `tests/test_document_terminal_contract.py` compares them and fails first when only one side changes.
- `tests/test_common_form_tree.py`: `ROLE_IDS` and `test_schema_role_and_form_enums_are_the_sixteen_common_roles` become eighteen roles in schema order; the ten-form constant and the tests named for it become twelve forms; the per-form `link_only` assertions expect `Related Documents` true in the two new forms; `ROLE_BINDINGS`, `FORM_PROFILES` and `FORM_TEMPLATES` gain the eight profiles; the per-form loop and role tuple gain the two roles with their extensions and no tables; synthetic cases cover both trees, the two local H3s and the conditional sections.
- `tests/test_readme_navigation.py` and `tests/test_reference_pack_routes.py`: the pack navigation section and any pinned pack heading become `Pack Index` and `Pack Contract`.

## Edge Cases & Error Handling

- A pack of one kind should carry only its own conditional closure section; the tree check enforces none of the three, so this is enforced by review, which loses the per-kind requirement that each pack profile has today.
- A Workspace README is a router profile, so its empty sections are enforced by review.

## Failure Modes & Fallback / Human Escalation

If any document outside the three pack READMEs and four templates gains a diagnostic, or a Workspace README changes, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators; after must equal before.
- Before and after, the fragment search `git grep -n -E '#(report-index|item-index|research-contract|audit-contract|data-contract)' -- ':!docs/98.archive'`; it stays empty.
- Before and after, the text search `git grep -n -E 'Report Index|Item Index|Research Contract|Audit Contract|Data Contract' -- docs/90.references docs/99.templates/templates/references`; after the change it finds none.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-LOCALREADME-001 | The registry, schema and role list hold the two local roles, their forms, the two local H3s, the four TemplateDefinitions, the eight bindings with empty lists and the `Pack Index` navigation; tests fail first and then pass. |
| VAL-LOCALREADME-002 | The seven Workspace READMEs pass unchanged; the three pack READMEs and four templates pass the tree, navigation, link, quality and markdownlint checks with only the decided renames; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCALREADME-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, schema and form tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-LOCALREADME-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
