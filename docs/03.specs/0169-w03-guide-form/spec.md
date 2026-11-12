---
title: "W03 Guide Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0169"
---

# W03 Guide Form Technical Specification (Spec)

## Overview

This approved change contract is the first phase-2 package of the W03 stage of the external v14.7 execution package. It gives the Guide role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry, adds the TemplateDefinition table contract that W03-D08 requires, and moves the guide template and the one current guide, [GDE-0010](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md), to the form without changing their meaning. The machine model comes from the closed SPEC-0168 and [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md); the user's decisions W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). The [Task](tasks/tsk-0001-w03-guide-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code in the same change): `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `tests/test_common_form_tree.py`, `docs/99.templates/templates/operations/guide.template.md`, `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md`, the Guide paragraph of `.agents/governance/document-authoring.md` (with one sentence on the table contract) and the Operations forms entry of `docs/99.templates/README.md`, each with its frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries. No validation registration changes: no test module is added, and `tests/test_common_form_tree.py`, `tests/test_operations_section_contract.py` and `tests/test_operations_lineage_contract.py` are already registered.
- Not in this package: every other role (Runbook, Policy, Incident, Postmortem, READMEs, `AGENTS.md`, `SKILL.md`, and phase 3), which keep their H2 lists; the README rule IDs; the phase-3 removal of the H2-list model.
- Form-only migration (W03-D01): no sentence of GDE-0010 changes meaning, no fact is added, and no rule is invented. Where the form asks for content the source does not hold, the section states that none exists and why (`explain_none_or_not_applicable`). Frontmatter `version` and `updated` change as a document edit requires.
- No generator; the template stays hand-copied and checked by template parity and the template-mode tree check.
- No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Guide form.** `common_forms.forms` gains the Guide form exactly as COMMON-DOC-FORM-1 1.0.0 defines it: `form_id` `guide`, `title` `Guide`, its `h1`, `language_rule` and `extension_policy`, and four required H2 sections in order, each with two required H3 children: Purpose (Outcome, Boundaries), Prerequisites (Environment, Permissions), Procedure (Actions, Exceptions), Verification (Expected Result, Troubleshooting). Each section keeps the contract's `section_id`, `content`, `required_content`, `prohibited_content`, `empty_policy` and `validation_ids`; `link_only` is false everywhere. `COMMON-ROLE-FORMS.json` lists Troubleshooting as conditional content, but its `definition_ref`, the section contract, makes it a required H3; the section contract governs. The template keeps its H1 `# [Topic Name] Guide`; no check compares it with the form's `h1`.
- **Extension (W03-D03, W03-D04).** One `local_h3` extension, `guide-lifecycle-traceability`, titled `Lifecycle Traceability` under `guide-verification`: condition "a guide in a status the body contract enforces (draft, in-review, active, deprecated) states its promoted owner or an N/A reason"; owner `platform`; verification "the body-contract check"; review "when the Guide form version changes"; removal "when guide lineage has another registered owner".
- **Profiles.** `operation/guide` and `common/template-operation-guide` carry empty H2 lists and drop `substantive_body` and `ordered`, which the tree check replaces. Their `body_contract.section` becomes `Verification`; its table heading, columns and source rules stay.
- **Derived heading lists.** For a profile whose role has a form, the loader derives its `HeadingContract` from the form: `required` is the form's required H2 titles in order, `allowed` all its H2 titles, `forbidden` empty. Every list consumer then reads the form instead of losing its check: `REGISTRY_BODY_SECTION` (`document_contracts.py`, the body-contract section must be a required H2 of the form), the template author-prompt check (`scripts/validation/repository/form_contracts.py`), the generic-residue scope (`scripts/validation/repository/quality.py`) and the heading-validity projection (`scripts/validate-links-and-owners.py`). The Markdown validator already uses the tree, not the lists, for a form profile.
- **Table contract (R45-10 `tables`, W03-D08).** A TemplateDefinition may carry `tables`, each with `name`, `section`, `columns` (each `key`, `meaning`, `data_type`, `required`), `minimum_rows` and `row_identity`, as in the package TemplateDefinition schema. `section` names a section ID or a `local_h3` extension ID of the role's form. `key` is the exact header text. From this package `tables` is required in every TemplateDefinition, as in the package schema, and may be empty; `minimum_rows` 0 is the package's "empty state allowed". Registry checks: the section exists in the form, column keys are unique, `row_identity` names a column, and a table whose name equals the body contract's `table_heading` has the body contract's `required_columns` as its keys in order. The loader copies the template profile's tables onto each authored profile its `source_profile_ids` names, so the document check needs no registry argument; template parity is unchanged because only the template side stores tables. Document check, for a table not owned by the body contract: inside the named section (its body and any H4 under it), every table whose first header cell equals the first column key is that table; its header must equal the keys in order and count (`BODY-TABLE-COLUMNS`); when the section is present, the identified tables together must hold at least `minimum_rows` data rows (`BODY-TABLE-ROWS`). A section heading that is not unique is left to `BODY-H3-DUPLICATE`. Other tables in the section are not checked, so a table whose first header is mistyped is not identified; this is accepted for `Steps`, whose rows are optional. The table named by the body contract's `table_heading` keeps its existing `BODY-CONTRACT-TABLE` and `BODY-CONTRACT-COLUMNS` checks and statuses and is not checked twice. `meaning`, `data_type` and `required` are recorded for authors, not checked by machine.
- **Guide tables.** `Steps` in `guide-procedure-actions` with keys `Step`, `Action`, `Check` (the contract's conditional step/action/check), `minimum_rows` 0, row identity `Step`; `Lifecycle Traceability` in `guide-lifecycle-traceability` with keys `Promoted owner`, `Audience outcome`, `Operating surface`, `minimum_rows` 1, row identity `Promoted owner`.
- **TemplateDefinition.** The guide template profile carries its definition: purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, the consumer paths that exist, positive, negative and regression validation cases, migration (the GDE-0010 meaning map, Git history as retained history, rollback by revert) and `tables`.
- **Template.** The template has the four H2 and eight H3 headings, an author prompt per H3 drawn from its `required_content` (the Outcome prompt keeps the current prompts' learning-purpose classification and authority link), an optional Steps table under Actions, and the `Lifecycle Traceability` H3 with its table under Verification.
- **GDE-0010 meaning map (W03-D11).** Overview and Audience and Goal go to Purpose > Outcome, except the sentences that say what the guide does not own, which go to Boundaries. Prerequisites items split into Environment and Permissions. Guidance becomes Procedure > Actions with its numbered H3 headings as H4; nothing links to an anchor in GDE-0010. Verification and Troubleshooting bullets split into Exceptions (unrun checks and stop conditions), Expected Result (what a PASS does and does not show) and Troubleshooting (recovery of retired paths). Related Documents leaves: each link moves inline by its DOC-07 type, normative to Prerequisites > Permissions, evidence to Verification, navigation to Purpose > Outcome; a link already inline in the body is not repeated (six of the eight are; Agent Execution Policy goes to Permissions and the Reference Maintenance Runbook to Outcome). No Requirement or Spec link is placed in Verification, so the guide's lineage owner read from that H2 is unchanged. Lifecycle Traceability moves under Verification unchanged. Each of the eight H3 holds prose, not only links.
- **Policy text.** `document-authoring.md` and `docs/99.templates/README.md` say Guide uses its registry form, with Lifecycle Traceability under Verification and its classification, readers and goal under Purpose; Policy and Runbook keep theirs under Related Documents until their packages. `document-authoring.md` also states the table contract in one sentence: a TemplateDefinition names each table's section, ordered columns, minimum rows and row identity, and the validator checks column order, count and minimum rows.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by ADR-0059). `tables` is a new key inside `template_definition`, which ADR-0059 decision 3 admits; it adds no top-level key and ADR-0059 stays unchanged.

## Data Modeling & Storage Strategy

Registry data only: one form, one extension, one TemplateDefinition with two tables, and the two guide profiles' lists and body-contract section. No new file outside this package.

## Interfaces & Data Structures

- `scripts/document_contracts.py`: heading lists derived from the form; `REGISTRY_BODY_SECTION` against the derived required list; a frozen table contract type; TemplateDefinition `tables` parsing and their copy onto the source profiles; the registry checks above with rule IDs `REGISTRY_TABLE_SECTION`, `REGISTRY_TABLE_COLUMNS` and `REGISTRY_TABLE_BODY_CONTRACT`.
- `scripts/validate-markdown-profiles.py`: the document table check (`BODY-TABLE-COLUMNS`, `BODY-TABLE-ROWS`), run for authored documents whose profile carries tables, with a small iterator over all tables of a section that reuses `_gfm_table_cells`.
- `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, `scripts/validate-links-and-owners.py`: unchanged code; they read the derived lists.
- `tests/test_common_form_tree.py`: the three tests that assert the repository registry has no form (`test_repository_registry_binds_clear_roles_and_carries_no_form`, `test_repository_registry_loads_without_a_form`, `CurrentRegistryUnchangedTests.test_no_current_profile_uses_the_tree`) are rewritten to assert exactly the Guide form and definition, not weakened. `tests/test_operations_section_contract.py` and `tests/test_operations_lineage_contract.py` build their own section lists from the `operation/guide` entry and stay valid; they are re-run.
- `docs/99.templates/contracts/document-profile.schema.json`: `tables` in `template_definition`.

## Edge Cases & Error Handling

- A table header with escaped pipes or inline code is read by the existing cell parser; no new cell parser.
- A missing Lifecycle Traceability H3 passes the tree check (conditional); the table check skips it (owned by the body contract); the body-contract check fails it for draft, in-review, active and deprecated guides.
- A template is not checked by the document table check; its Lifecycle Traceability placeholder row still satisfies the template-mode body contract, which is always enforced.

## Failure Modes & Fallback / Human Escalation

If any document other than GDE-0010 and the guide template gains a diagnostic, the change is wrong and is fixed before commit. If a GDE-0010 sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the diagnostic counts of the four strict document validators over the whole tree; after must equal before, with zero FAIL lines.
- `python3 scripts/run-contract-tests.py --root . --suite document` and `--suite agent-governance`.
- The four strict document validators, `validate-document-lifecycle.py --root . --mode staged` before each commit, `python3 scripts/validation/repository/quality.py --root .`.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-GUIDEFORM-001 | The registry holds the Guide form, its extension, its TemplateDefinition and tables, and the guide profiles carry no H2 lists; the loaded guide profiles' heading lists equal the form's H2 titles; schema and registry negatives (table section not in the form, duplicate column key, `row_identity` not a column, Lifecycle Traceability keys differing from the body contract, guide profile with H2 lists, body-contract section not a required H2 of the form, TemplateDefinition without `tables`) fail in tests. |
| VAL-GUIDEFORM-002 | The document table check passes its positive cases and fails its negative cases (wrong column order, missing column, extra column, fewer rows than `minimum_rows`), and other tables in the section are ignored, in isolated tests. |
| VAL-GUIDEFORM-003 | The guide template and GDE-0010 pass the tree, table, body-contract, template author-prompt and residue checks; the meaning map is recorded in the Task with every source sentence placed; the two policy texts are updated; diagnostic counts over the rest of the tree are unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GUIDEFORM-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry schema and negative tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GUIDEFORM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Table check positive and negative tests. |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-GUIDEFORM-003 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Strict validators over the tree; exact-index QA. |
