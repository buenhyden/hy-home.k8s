---
title: "W03 TemplateDefinitions for Templates Without a Common Role"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0179"
---

# W03 TemplateDefinitions for Templates Without a Common Role Technical Specification (Spec)

## Overview

This approved change contract closes handoff W03-H06, for the templates without a role, of the W03 stage of the external v14.7 execution package. DOC-11 and R45-10 require a TemplateDefinition for every real template, and the registry accepts a TemplateDefinition only on a template profile that has a `document_role`. Fourteen template profiles have neither: three reference report templates (audit, research, data), six governance templates (contract, knowledge, vocabulary, prompt, provider, role), three evaluation templates (task, score, results) and two provider-native templates (metadata, command). W03-D09 says a profile that matches no common role keeps its current form as its own role and gains a TemplateDefinition, and that the per-profile analysis goes to the user before any binding. On 2026-11-13 the user chose to group templates whose headings are identical into one local role, as W03-D10 did for the three pack READMEs (W03-D20), and chose to migrate the one current document whose table conflicts with its template table to the template columns (W03-D21). The six SDLC templates (requirement, architecture description, architecture decision, Spec, Plan, Task) have a role and no TemplateDefinition either; they are not phase-2 roles, so this package records them for phase 3 as W03-H13 with the H2-list question below, and DOC-11 is not complete until phase 3 adds theirs. It reuses the model of SPEC-0169 to SPEC-0178 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D20, W03-D21 and W03-H13 are added there by this package's first commit. The [Task](tasks/tsk-0001-w03-template-definitions.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; `docs/99.templates/contracts/document-profile.schema.json` (the role enum and the `template_table.section` description); `scripts/document_contracts.py` (the `DocumentRole` literal, a separate form-identifier literal and the registry table check); `scripts/validate-markdown-profiles.py` (the document table check and a template table-heading check); in `docs/90.references/research/0002-archive-retention-and-provenance/m0001-git-provenance-and-superseded-record-citation.md` only the table directly under `## Sources`; `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py` and any test that pins the role list or the table checks; the forms sentence of `.agents/governance/document-authoring.md` and one added sentence in `docs/99.templates/README.md`; the W03-D20, W03-D21 and W03-H13 rows, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document's frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: any template body; any other document body; a common form for these roles; TemplateDefinitions for the six SDLC templates (W03-H13, phase 3); W03-H07 (frontmatter key meaning), which follows as its own package; phase 3.
- No heading changes anywhere. The only document text change is the m0001 `Sources` table (W03-D21). No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Roles (W03-D20).** The `DocumentRole` literal and the schema role enum gain nine Stage 99 local roles, in this order: `reference-report` (`reference/audit`, `reference/research`, `reference/data` and their three twins, which share the same eight H2s), `governance-document` (`governance/contract`, `governance/provider`, `governance/role` and their twins, which share the same six H2s), `knowledge-map` (`governance/knowledge`), `vocabulary` (`governance/vocabulary`), `prompt` (`governance/prompt`), `evaluation-task`, `evaluation-score`, `evaluation-results` (the three evaluation profiles) and `provider-native` (`common/provider-native-metadata`, `common/provider-native-command` and their twins, whose bodies have no headings). The schema form enum stays at its eighteen identifiers and the registry keeps its twelve forms: none of these roles gets a form, and each profile keeps its H2 lists unchanged (W03-D09). Because `CommonForm.form_id` is typed by `DocumentRole` today, it gets its own literal of the eighteen form identifiers, compared with the schema form enum by a parity test, so the typed form identifier still refuses the nine new roles. The heading obligation of these roles is their H2 lists only: no H3 contract and no order beyond the existing `ordered` flag. Twenty-eight profiles gain a `document_role`: the fourteen templates and their fourteen source profiles.
- **Tables on a role without a form.** For a template whose role has no form, a table's `section` is the exact heading line that holds the table in the template, `## <title>` or `### <title>`, for example `## Sources` or `### Claim-Source Matrix`. The registry check reads no template body: it refuses a `section` that is not an H2 or H3 heading line, and an H2 line whose title is not in the profile's required list (these profiles have empty optional lists). The Markdown profile check, which already reads each template with its fence- and comment-aware helpers, refuses in the template itself a recorded heading line that is not exactly once outside fences and comments, or whose H2 (the line itself or the nearest H2 above it) is not in the required list (new rule `BODY-TABLE-SECTION`). The registry's caller-supplied mode is unchanged because the registry check reads no file. The document check reads that exact heading in each document of the template's source profiles, as it reads a form section today, and applies `BODY-TABLE-COLUMNS` and `BODY-TABLE-ROWS` there; a document without the heading is not checked, as today, and a heading that occurs more than once in a document is skipped there, since these roles have no tree check. For a role with a form, `section` stays a section or local H3 ID and nothing changes.
- **Tables recorded.** Each TemplateDefinition records every table its template holds, under the heading that holds it, with the template's column order, a `meaning` and `data_type` for each column, `minimum_rows` 0 and a `row_identity`. Every column is `required`: the read at the base found every current document's matching table using all of its template's columns. The eighteen tables are: audit four (`### Criteria and Inspected Surface`, `### Observed Evidence`, `### Findings and Gaps`, `### Remediation`), research two (`### Claim-Source Matrix`, `## Sources`), data three (`### Schema`, `### Provenance`, `### Generation and Refresh`), vocabulary one (`## Repository Vocabulary`), evaluation task three, evaluation score three and evaluation results two, each under the heading the template gives it; the evaluation task and score tables include each template's key-value `Field` table under `## Overview`. Two score tables share the name `Trial ID` (`## Trial Evidence` and `## Criterion Scores`); their heading lines tell them apart, as the document check reads each table only under its own heading. The governance-document, knowledge-map, prompt and provider-native templates hold no table and record `tables` as an empty list.
- **Table name.** A table's `name` is its first header cell, which the document check uses to find it. Current audit `Findings` tables start with `Finding or gap`, not the template's `ID`, so they are not read, and the data, evaluation task and evaluation score profiles have no current document; synthetic cases cover those tables.
- **Migration (W03-D21).** The m0001 research report's table under `## Sources` moves from `Source | URL | Checked | Result` to `Source | Grade | Retrieved | Relevance`, row for row: `Source` becomes `[<source>](<URL>)`, `Checked` becomes `Retrieved`, `Result` becomes `Relevance` as the recorded retrieval result, the PREMIS row's code-span URL staying in that cell, and the padded table style kept, and `Grade` is `Not graded` because no grade is on record; no row is added, removed or reordered and no other cell text changes. Its second table under `## Review and Freshness` is not under `## Sources` and stays. The research TemplateDefinition records that m0001's `Relevance` holds the recorded retrieval result, not a statement of direct support.
- **TemplateDefinitions.** One on each of the fourteen templates, with purpose, responsibility, non-goals (each states that the role is a Stage 99 local role under W03-D09 and W03-D20, not a COMMON-DOC-FORM-1 role, and that it has no form), policy references (`document-authoring.md` and the policy that owns the surface), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, consumer paths that exist, validation cases, migration and `tables`.
- **Policy text.** `document-authoring.md` says that a template whose role has no form keeps its H2 lists and records its tables under the template's own headings; `docs/99.templates/README.md` gains one Korean sentence beside its Governance and Evaluation form bullets saying these templates have local roles and TemplateDefinitions without a common form, naming the nine roles, and that the six SDLC templates gain theirs in phase 3.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and template definition ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)). No ADR body changes here. ADR-0059 says H2 lists stay only for a role without a form until the last role moves; the nine local roles keep their lists by W03-D09 and W03-D20, so that coexistence does not end with phase 3 as it stands. W03-H13 hands that to phase 3, which owns removing the H2-list model (W03-H02) and decides there whether ADR-0059 needs a successor.

## Data Modeling & Storage Strategy

Registry data: twenty-eight bindings, fourteen TemplateDefinitions, eighteen tables. Code and schema: nine role identifiers; a form-identifier literal; the table checks resolve a heading line for a role without a form.

## Interfaces & Data Structures

- `scripts/document_contracts.py` and the schema: the nine role identifiers; `test_typed_stage_and_document_role_match_the_schema` in `tests/test_document_terminal_contract.py` compares them and fails first when only one side changes; a parity test of the new form-identifier literal against the schema form enum is added. The registry table check checks the heading-line syntax and the H2 title for a role without a form.
- `scripts/validate-markdown-profiles.py`: the document table check stops returning nothing for a profile without a form and resolves the heading line instead; the template check gains `BODY-TABLE-SECTION`.
- `tests/test_common_form_tree.py`: `ROLE_IDS` and the schema role-enum test become twenty-seven roles in schema order, and the form-enum test keeps eighteen with twelve forms. Tests that change: lines 991-998 (role-less profiles carry no tables and no definition), line 1001 (`governance/role` has no role), lines 1222-1226 (removing `document_role` from every non-form profile yields no diagnostic), lines 1274-1286 (`common/template-governance-role` as the role-less template with a definition, which becomes a synthetic removal of `document_role`), and `ROLE_BINDINGS` with its comment; `test_a_table_needs_a_form_to_name_a_section` (line 1405) keeps passing for a form role. Synthetic cases cover a table under an H2 and under an H3 of a role without a form, a heading line missing from the template, an H2 outside the profile's lists, a heading line repeated in the template, a reordered column and a missing required column.

## Edge Cases & Error Handling

- A document that holds a different table whose first header cell equals a recorded table's name, under the same heading, fails `BODY-TABLE-COLUMNS`; the read at the base found only the m0001 `Sources` table, which W03-D21 migrates. A different table under another heading is not read, which is why the research Claim table is recorded under `### Claim-Source Matrix`.
- The two provider-native templates have no body headings, so their roles carry no table and the document checks are unchanged.

## Failure Modes & Fallback / Human Escalation

If any document other than m0001 gains a diagnostic, the change is wrong and is fixed before commit; no other document is edited to pass. If a recorded column cannot be given a meaning from the template's author prompt, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators; the diagnostics after must equal those before, the only other difference being path counts that this package's own files change.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-TPLDEF-001 | The role list and schema hold the nine local roles; the twenty-eight profiles are bound with their H2 lists unchanged; the fourteen TemplateDefinitions and eighteen tables are recorded; both table checks resolve a heading line for a role without a form; tests fail first and then pass. |
| VAL-TPLDEF-002 | The m0001 `Sources` table is migrated row for row; every other document passes unchanged; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TPLDEF-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, schema and table tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-TPLDEF-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
