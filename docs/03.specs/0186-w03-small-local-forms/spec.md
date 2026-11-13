---
title: "W03 Small Local Forms"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0186"
---

# W03 Small Local Forms Technical Specification (Spec)

## Overview

This approved change contract is the first of three packages that close handoff W03-H28 and decision W03-D26 of the W03 stage of the external v14.7 execution package. The nine roles of W03-D20 (`reference-report`, `governance-document`, `knowledge-map`, `vocabulary`, `prompt`, `evaluation-task`, `evaluation-score`, `evaluation-results` and `provider-native`) have a role and a TemplateDefinition but no form; SPEC-0177 and SPEC-0178 gave forms to other roles (`skill`, a COMMON-DOC-FORM-1 role, and the two README roles of W03-D09 and W03-D10). This package gives six of the nine roles forms and three remain. W03-D26 and DOC-01 ask for local forms with H2 and H3 titles, order and content for these roles, and for the documents to move form-only. This package covers the six simple roles, whose documents hold no H3: `knowledge-map` (`.agents/knowledge/domains.md`, `.agents/knowledge/project-map.md`), `vocabulary` (`.agents/knowledge/glossary.md`), `prompt` (`.agents/prompts/*.md` other than the README), and `evaluation-task`, `evaluation-score` and `evaluation-results` (the templates under `docs/99.templates/templates/evaluations/` and `.agents/evaluations/results.md`), each with its template twin. It reuses the model of SPEC-0169 to SPEC-0181 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). On 2026-11-13 the user decided the rest of W03-H28: the provider-native role stays without a form because its documents use native formats (DOC-02, W03-D33); the 17 `.agents/roles/*.md` become a separate `governance-role` role with the eight H3 titles required while the provider files stay H2-only `governance-document` documents (W03-D34, the second package); the research H3 titles are registered as they stand (W03-D35, the third package); and the three reference reports share one form whose Sources section is link-only (W03-D36, the third package). The user's decisions are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D33 to W03-D36 are added there by this package's commit. The [Task](tasks/tsk-0001-w03-small-local-forms.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json` (six forms, the 12 profiles' H2 lists, the six twins' TemplateDefinition texts and table sections); `docs/99.templates/contracts/document-profile.schema.json` (the form enum); `scripts/document_contracts.py` (the `FormId` literal and its comment at line 681, and the comment above `DocumentRole`); `tests/test_common_form_tree.py` (including the stale comments at lines 56, 457 and 3715), `tests/test_document_terminal_contract.py` (including the stale comment at lines 233 and 234), `tests/test_evaluation_document_profiles.py` and any test that pins these profiles' H2 lists, form counts or the form list; the forms sentences of `.agents/governance/document-authoring.md` and of `docs/99.templates/README.md`; the W03-D33 to W03-D36 rows, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the documents and templates of the six roles, which move form-only and change no text; `reference-report`, `governance-document` and the new `governance-role` role (W03-D34, package 2); the research H3 titles and the reference-report form (W03-D35 and W03-D36, package 3); `provider-native`, which stays without a form (W03-D33); the full TemplateDefinition record (W03-H15); `_workspace/workspace_execution_tasks/` (read-only input); phase 3.
- Form-only migration (W03-D01): no document or template heading, sentence or table changes. The H2 titles `Pointer Index`, `Repository Vocabulary`, `Local Extensions` and `Inputs` keep their literal text because `scripts/validate-knowledge-surface.py` (lines 29 to 32) and `scripts/prompt-input.py` (line 22) read them by name. No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none. This package's own three files (`spec.md`, `plan.md` and the Task) fall under the open-package layer rule of SPEC-0184, and SPEC-0182 lands first.


## Contracts

- **Form identifiers.** The `FormId` literal in `scripts/document_contracts.py` and the `form_id` enum of `document-profile.schema.json` gain `knowledge-map`, `vocabulary`, `prompt`, `evaluation-task`, `evaluation-score` and `evaluation-results` after `reference-pack-readme`, in the same order, which is the role order; the enum goes from 18 to 24 identifiers and `registry.common_forms.forms` from 12 to 18 forms. `DocumentRole` and its schema enum already hold all six roles and do not change; the comment above the `DocumentRole` literal that calls the nine local roles "a role with no form" is corrected to name the three that stay without one (`reference-report`, `governance-document` and `provider-native` until package 2 and package 3). `common_forms.contract_id` stays `COMMON-DOC-FORM-1` for the list; each form says in its `extension_policy` that it is a Stage 99 local role under W03-D09, W03-D20 and W03-D26, not a COMMON-DOC-FORM-1 role.
- **Forms.** Every form carries `h1` `{{document_title}}`, the same `language_rule` string the other local forms carry, its `extension_policy`, and for each section `content`, `required_content`, `prohibited_content`, `empty_policy` `explain_none_or_not_applicable`, `validation_ids` (`FORM-STRUCTURE` and `FORM-CONTENT-REVIEW`) and `link_only`. A section id is the form id and the slug of the H2 title (for example `vocabulary-repository-vocabulary`). Every section is required, there is no H3 and no extension, because no document of these roles has an H3 (read-only inventory of 2026-11-13). The H2 sets and order are those of the profiles' `sections.required` today:

| Form | Title | H2 sections in order | `link_only` |
| --- | --- | --- | --- |
| `knowledge-map` | Knowledge Map | Overview; Authority Boundary; Pointer Index; Validation and Refresh; Related Documents | `Related Documents` |
| `vocabulary` | Vocabulary | Purpose; Scope; Normative Language; Repository Vocabulary; Local Extensions; Maintenance; References | `References` |
| `prompt` | Prompt | Overview; Authority Boundary; Inputs; Output; Validation; Refusal Conditions; Related Documents | `Related Documents` |
| `evaluation-task` | Evaluation Task | Overview; Declared Trials; Signals and Criteria; Human Calibration; Related Documents | `Related Documents` |
| `evaluation-score` | Evaluation Score | Overview; Trial Evidence; Criterion Scores; Human Calibration; Related Documents | `Related Documents` |
| `evaluation-results` | Evaluation Results | Overview; Pair Coverage; Aggregate; Limitations; Related Documents | `Related Documents` |

- **Link-only sections.** `Related Documents` and `References` are link lists, so they are `link_only` true and every other section false, as the other local forms do. The `Overview` of the task and score forms holds a `Field` table and the vocabulary sections hold `Term ID` tables, so none of them is link-only.
- **Profiles.** The 12 profiles that bind the six roles (`governance/knowledge`, `governance/vocabulary`, `governance/prompt`, `evaluation/task`, `evaluation/score`, `evaluation/results` and their six `common/template-*` twins) get empty `sections.required`, `optional` and `forbidden` lists, because `REGISTRY_FORM_LEGACY_LISTS` refuses H2 lists on a profile whose role has a form; the headings then come from the form. The `ordered` flag of the vocabulary profile is not carried over: a form fixes its section order, which the form tree check enforces. `evaluation/raw-output` has no role and keeps its empty lists.
- **Tables.** The six twins' TemplateDefinitions record their tables under form section ids instead of heading lines (SPEC-0179), with columns, minimum rows and row identity unchanged: `Term ID` under `vocabulary-repository-vocabulary`; for the task `Field` under `evaluation-task-overview`, `Trial ID` under `evaluation-task-declared-trials` and `Criterion ID` under `evaluation-task-signals-and-criteria`; for the score `Field` under `evaluation-score-overview`, `Trial ID` under `evaluation-score-trial-evidence` and `Trial ID` under `evaluation-score-criterion-scores`; for the results `Cycle ID` under `evaluation-results-pair-coverage` and `Scope` under `evaluation-results-aggregate`. The knowledge-map and prompt twins keep no table, because the requirements define no conditional table for them and the documents' tables differ.
- **TemplateDefinitions.** Each of the six twins keeps its definition and changes its texts: the non-goal that calls the role "a Stage 99 local role under W03-D09 and W03-D20 and has no form" says that the role has its own local form under W03-D09, W03-D20 and W03-D26 and is not a COMMON-DOC-FORM-1 role; the non-goal about leaving the H2 lists as the profile records them says that the template's headings stay and are now owned by the form; `consumer_paths` add `scripts/validate-document-contract-registry.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests that pin the role; the validation cases name the form tree check and the section ids instead of the H2 list and the heading line, so the `validation.negative` texts drop `BODY-TABLE-SECTION` (which cannot fire for a role with a form, `scripts/validate-markdown-profiles.py` lines 918 to 921) and the heading-line wording, and name `REGISTRY_TABLE_SECTION` for an unknown section id, with `BODY-TABLE-COLUMNS` and `BODY-TABLE-ROWS` for the table body (the section-id table case that the other form roles carry); `migration.meaning_map` names this package.
- **Policy text.** `document-authoring.md` lists the six roles among those that use their registry forms and keeps the sentence that a template whose role has no form keeps its H2 lists for the three that remain; `docs/99.templates/README.md` (lines 132 to 136, one sentence that now covers all nine roles) is rewritten to say that six roles (`knowledge-map`, `vocabulary`, `prompt` and the three evaluation roles) use their own local forms and that `reference-report`, `governance-document` and `provider-native` have none yet. The documents under `.agents/` and the templates stay English-only under `document_language`; only that README sentence is Korean.
- **Recorded decisions.** W03-D33 (provider-native stays form-less, native formats, DOC-02), W03-D34 (the 17 role files become the `governance-role` role with the eight H3 titles required, provider files stay `governance-document` H2-only; package 2), W03-D35 (research H3 titles registered as they stand; package 3) and W03-D36 (one reference-report form, Sources link-only; package 3) are added to the SPEC-0161 Task with this package's commit (step 2 of the commit order); W03-H28 is updated to name the three packages.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and template definition ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes. A role with a form reads its H2 lists from the form, so the six roles stop using the H2-list model that W03-H13 keeps only for roles without a form.

## Data Modeling & Storage Strategy

Registry data: six forms with 34 sections and no extension, 12 profiles with empty lists, six TemplateDefinitions with changed texts and nine table sections. Code and schema: six form identifiers.

## Interfaces & Data Structures

- `scripts/document_contracts.py` and the schema: the six form identifiers; `test_typed_form_identifier_matches_the_schema_form_enum` in `tests/test_document_terminal_contract.py` compares them and fails first when only one side changes; its count of 18 and its set of roles without a form change to 24 and `reference-report`, `governance-document` and `provider-native`.
- `tests/test_common_form_tree.py`: `FORM_IDS` gains the six identifiers and `LOCAL_ROLE_IDS` keeps the three that have no form, with `ROLE_IDS` built in the schema role order (it is no longer `FORM_IDS + LOCAL_ROLE_IDS`); `test_schema_role_enum_is_twenty_seven_and_form_enum_stays_eighteen` becomes a 24-form test; the twelve-form constants and the tests named for it (`TWELVE_FORMS`, the exact-forms and only-form-profiles tests) become eighteen forms; `FORM_PROFILES` and `FORM_TEMPLATES` gain the 12 profiles and the six twins while `LOCAL_TABLES` keeps only the templates of the three remaining roles and the reference and governance ones; the table expectations of the six twins use section ids; every assertion that a profile of these roles has `form is None` flips; synthetic cases cover each of the six trees, a missing and a reordered required H2, a stray H3 and a bare empty section.
- `tests/test_evaluation_document_profiles.py`: `test_forms_keep_six_key_envelope_and_required_headings` reads `profile.headings.required[1]`, which now comes from the form and is the same H2, so it is expected to pass unchanged; any assertion on the profile's own `sections` lists changes.
- `tests/test_validate_knowledge_surface.py` and `tests/test_prompt_input.py` keep passing, because the literal H2 titles they read do not change.

## Edge Cases & Error Handling

- The H2 titles read by name by `scripts/validate-knowledge-surface.py` and `scripts/prompt-input.py` must not be renamed; a form that renamed one would break those scripts while the profile check still passed.
- The evaluation task and score instances do not exist in the tree today (only `.agents/evaluations/results.md` and the three templates), so the task and score forms are exercised by their templates and by synthetic tests.
- A form fixes section order, while the vocabulary profile alone had `ordered` true; the other five profiles accept any order today and the form tree check will now enforce their order. The documents already follow it (read-only inventory), and the Task confirms it with the strict validators.
- The `Overview` of the evaluation task and score templates holds a table, so `prohibited_content` states that the table is not replaced by prose and the form does not make `Overview` link-only.

## Failure Modes & Fallback / Human Escalation

Documents are expected to pass unchanged, so this package edits none of them. If any document or template of the six roles gains a diagnostic from the strict validators, the form is wrong and is fixed before commit, never the document; the author does not edit a governed document to satisfy a form. If a form cannot be written without a heading, sentence or table change in a document, the author stops and asks the user. If `scripts/validate-knowledge-surface.py`, `scripts/prompt-input.py` or a script outside this list stops passing, the change is wrong and is reverted to the last passing step.

## Verification Commands

- Before and after, record the output of the four strict document validators; after must equal before (no new diagnostic and no removed one).
- `git diff --stat` over `.agents/knowledge/`, `.agents/prompts/`, `.agents/evaluations/` and `docs/99.templates/templates/` is empty.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`; the tests of `scripts/validate-knowledge-surface.py` and `scripts/prompt-input.py`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SMALLFORMS-001 | The registry, schema and form literal hold the six forms with their 34 sections, `link_only` Related Documents and References, the 12 profiles with empty lists, the six TemplateDefinitions with section-id tables and changed texts, and no extension; the form-identifier parity test and the form tree tests fail first and then pass. |
| VAL-SMALLFORMS-002 | The two knowledge documents, the glossary, the four prompts, `results.md` and the six templates pass unchanged; the policy texts are updated; validator output over the tree is unchanged; the knowledge-surface and prompt-input tests pass; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SMALLFORMS-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, schema and form tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SMALLFORMS-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
