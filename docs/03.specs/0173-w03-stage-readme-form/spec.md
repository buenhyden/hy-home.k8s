---
title: "W03 Stage README Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0173"
---

# W03 Stage README Form Technical Specification (Spec)

## Overview

This approved change contract is the fifth phase-2 package of the W03 stage of the external v14.7 execution package and the second of three README packages. It gives the Stage README role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry and moves 22 documents and two templates to the form without changing meaning: the seven stage READMEs (`common/readme-stage-index`) and the fifteen collection READMEs (`common/readme-collection-index`). The four agent and provider READMEs (`.agents/`, `.claude/`, `.codex/`, `.agents/evaluations/`), which W03-D10 binds to this role, stay on `common/readme-implementation` with their current form; the user deferred their binding (W03-D16), because three of them name children only in code spans and would fail the complete-listing check of a collection profile. It reuses the model of SPEC-0169 to SPEC-0172 (derived heading lists, TemplateDefinition `tables`, table checks, navigation in a form H3, optional trailing columns; recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions W03-D01, W03-D08 and W03-D10 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D16, the user's answer of 2026-11-13 in this package's review, is recorded in this package's Task and added to that table by this package's first commit. The [Task](tasks/tsk-0001-w03-stage-readme-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; the two templates `docs/99.templates/templates/common/readme-stage-index.template.md` and `readme-collection-index.template.md`; the 22 documents named above; `scripts/validate-markdown-profiles.py` (the document-content table reader); `tests/test_common_form_tree.py`, `tests/test_readme_navigation.py`, `tests/test_repository_quality_rules.py` and any test that pins these profiles' H2 lists or navigation section; the forms sentence of `.agents/governance/document-authoring.md` and the Common forms bullet of `docs/99.templates/README.md` (itself one of the 22); the W03-D16 row, the EVD-034 row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document with its frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the four agent and provider READMEs (W03-D16); the Service README role (the sixteen other `common/readme-implementation` READMEs and `.github/repository-surface.md`), Workspace README and Reference Pack README, which keep their H2 lists; the retirement of the list-mode `README_H2_*` rule IDs, which stay for those profiles; phase 3.
- Form-only migration (W03-D01): no sentence changes meaning, no fact is added, every command and link target stays; where an H3 has no source text, one Korean none-with-reason line states that none exists, listed in the Task for the user. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Stage README form.** `common_forms.forms` gains the Stage README form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[12]`): `form_id` `stage-readme`, `title` `Stage README`, Stage Responsibility (Purpose and Readers, Inputs and Outputs), Contents (Current Items, Classification), Workflow (Create and Review, Transition and Exit), Related Documents (Upstream and Downstream, Policy and Templates), every section required, `link_only` false everywhere as in the other forms. No extension. All 22 documents are `router` profiles, for which the tree check reports no `BODY-SECTION-EMPTY`; none-with-reason lines in them are therefore enforced by review and the Task list, not by the validator. Templates keep their H1.
- **Profiles and binding (W03-D10).** `common/readme-collection-index` and its template twin gain `document_role` `stage-readme` (the stage index already has it). No path pattern changes. The four profiles (two authored, two templates) carry empty H2 lists; heading lists are derived from the form.
- **Navigation.** `readme_navigation` sections for `common/readme-stage-index` and `common/readme-collection-index` become `Current Items`; `complete` stays `true` for both.
- **Table (W03-D08).** Both template TemplateDefinitions carry `Index` in `stage-readme-contents-current-items` with keys `Path` and `Purpose` (required) and `Owner` (optional), `minimum_rows` 0, row identity `Path`. Every current index table in the 22 documents has the header `Path | Purpose`.
- **Document-content tables.** `_document_content_table` reads a matrix or index table under an H2, H3 or H4 with the given title, still requiring exactly one such heading, so the matrices and indexes that move to H4 (`Operations Routing Matrix`, `Incident Boundary Matrix`, the Korean-titled document index tables of the guides, policies and runbooks READMEs) stay checked.
- **TemplateDefinitions.** Each of the two template profiles carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path for its profile (registry, schema, its template, its documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validation/document_content.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Meaning map, applied per document.** It is derived from the form's section `content` text; W03-D11's inline dispersal of links does not apply, because this form registers Related Documents.
  - Overview, lead blockquote and reader lists (for example `Stage Readers`, `Audience`) go to Stage Responsibility > Purpose and Readers.
  - Scope (In Scope and Out of Scope as H4) goes to Stage Responsibility > Inputs and Outputs.
  - Structure: the tree, `Path | Purpose` indexes and lists of current members go to Contents > Current Items, their H3 as H4.
  - A matrix, boundary table or classification table goes to Contents > Classification as H4 wherever it sits in the source (for example `Operations Routing Matrix` and `Operations Mutation Boundary` in Stage 05, `Incident Boundary Matrix`, `Physical Form Inventory` and `Deliberately Empty Profiles` in Stage 99, and the responsibility H3s of `.agents/roles/README.md`); in-page and cross-file anchors to these headings keep working because their slugs do not change.
  - Usage: authoring, template, review and check steps go to Workflow > Create and Review; status, promotion, exit and disposition rules go to Workflow > Transition and Exit; a document's own Verification H2 goes to Create and Review as H4.
  - Related Documents: requirement, design, work and operations links go to Related Documents > Upstream and Downstream; policy and template links go to Policy and Templates.
  - Headings keep their relative order, no level is skipped, and the Task records each document's placements and added lines.
- **Policy text.** `document-authoring.md` adds the Stage README to the roles that use their registry forms; the Common forms bullet of `docs/99.templates/README.md` says stage and collection READMEs use the Stage README form and keeps the shared `Overview`, `Scope`, `Structure`, `Usage`, `Related Documents` core only for implementation READMEs (including the four agent and provider READMEs until W03-D16 is resolved), workspace and runtime-governance READMEs.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and README navigation ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data: one form, two TemplateDefinitions with one table each, four profiles' lists, one role binding and two navigation sections.

## Interfaces & Data Structures

- `scripts/validate-markdown-profiles.py`: `_document_content_table` accepts H4 titles.
- `tests/test_readme_navigation.py`: `RepositoryContractTests` (which feeds `## Structure` text for the collection profile from the real registry) is rewritten for `Current Items` as an H3; a stage-style README with complete listing under `Current Items` passes and a missing child fails.
- `tests/test_common_form_tree.py`: `ROLE_BINDINGS` gains `common/readme-collection-index`; the repository-registry tests name exactly the six forms; the `link_only` assertion over repository forms stays unchanged; synthetic cases cover the Index table.
- `tests/test_repository_quality_rules.py`: the document-content reader test extends to H4: a matrix under an H4 is found and a title at two levels is ambiguous and not read.

## Edge Cases & Error Handling

- A router README is not checked for empty sections; review and the Task list carry the none-with-reason lines.
- A README whose Contents has no classification content states so in one Korean line.

## Failure Modes & Fallback / Human Escalation

If any document outside the 22 and the two templates gains a diagnostic, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-STAGEREADME-001 | The registry holds the Stage README form, its TemplateDefinitions and tables, the collection binding and the `Current Items` navigation sections; the four profiles carry no H2 lists; the document-content reader finds an H4 matrix; tests fail first and then pass. |
| VAL-STAGEREADME-002 | The 22 documents and two templates pass the tree, navigation (complete), document-content, author-prompt, residue and markdownlint checks; each document's map and added lines are recorded in the Task; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STAGEREADME-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, navigation and reader tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-STAGEREADME-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
