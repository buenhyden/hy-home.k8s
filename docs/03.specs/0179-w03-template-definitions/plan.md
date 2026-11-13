---
title: "W03 TemplateDefinitions for Templates Without a Common Role Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0179-PLAN-0001"
parent_ids: ["SPEC-0179"]
---

# W03 TemplateDefinitions for Templates Without a Common Role Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no heading changes and no document text change other than the m0001 `Sources` table, and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add the nine local roles to the role list and schema and a form-identifier literal; bind the twenty-eight profiles; let the table checks resolve a heading line for a role without a form; record the fourteen TemplateDefinitions and their eighteen tables; migrate the m0001 `Sources` table; record W03-D20, W03-D21 and W03-H13; update the policy texts. [Task 0001](tasks/tsk-0001-w03-template-definitions.md) owns execution and evidence.

## Context

SPEC-0178 closed the last phase-2 role package (PR #243 merged). This branch `claude/w03-template-definitions` starts from `1282f0c0`, the `main` merge of PR #243. A read at that commit found:

- fourteen template profiles with no `document_role` and no TemplateDefinition, and their fourteen source profiles; the registry check accepts a TemplateDefinition only on a template with a role; six SDLC templates with a role and no TemplateDefinition, owed by phase 3;
- identical H2 lists in the three reference report profiles and in the governance contract, provider and role profiles; different lists in the other profiles; no H2 in the two provider-native profiles;
- research reports with 57 distinct H3s, so a form would force them to register or restructure headings, which W03-D09 does not ask;
- eighteen tables in seven templates, some under an H2 and some under an H3; `CommonForm.form_id` typed by the role literal;
- a table check that names a form section ID and returns nothing for a profile without a form, in both the registry and the document validator; template documents not checked against their own tables;
- in current documents, tables that match their template's columns, except the m0001 research `Sources` table, and a research coverage table whose first header `Claim` equals the template's Claim table but which sits under another H3;

## Goals & In-Scope

- Code and schema: nine role identifiers; a form-identifier literal; heading-line resolution in the table checks and `BODY-TABLE-SECTION` for templates.
- Registry: twenty-eight bindings; fourteen TemplateDefinitions with eighteen tables.
- The m0001 `Sources` table; policy texts; W03-D20, W03-D21, W03-H13 and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: role list, registry and document table cases.

## Non-Goals & Out-of-Scope

- Template bodies; other document bodies; forms for these roles; the six SDLC TemplateDefinitions (W03-H13); W03-H07; phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TPLDEF-001](spec.md#success-criteria--verification-plan) | Role list and schema; bindings; table checks; TemplateDefinitions and tables; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-template-definitions.md) | Failing tests first, then passing; strict registry check; any moved baseline line in its own commit first. |
| WORK-002 | [VAL-TPLDEF-002](spec.md#success-criteria--verification-plan) | m0001 `Sources` table; policy texts; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-template-definitions.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators before any change.
- Show each changed test failing before its change, then passing; show the m0001 table failing `BODY-TABLE-COLUMNS` once the research table is recorded and before its migration.
- Record in the Task the m0001 row count before and after and that only that table changed.
- Commit order: the package commit with this Task, this package's entry in `docs/03.specs/README.md` and the W03-D20, W03-D21 and W03-H13 rows; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 bodies unchanged; the ADR-0059 coexistence question goes to phase 3 by W03-H13.
- Record the risk class (`medium`: registry, schema, the role list, two validators, tests and one reference document; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), scored by judgement.

- **A widened role list admits an unintended role.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. Only the nine named identifiers are added, each bound by tests to its profiles. Review cue: an unbound role in review. Signal that raises it: a later role added without review. Rollback: revert the implementation commit.
- **The document table check starts refusing a current document.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The base read found one conflict, migrated here; validator output is compared before and after. Review cue: any new diagnostic. Signal that raises it: a new report written without its template. Rollback: revert the implementation commit.
- **The m0001 migration changes meaning.** Possible, Minor: LOW, accept with review. Owner: W03 author. Row for row, the URL kept in the link, the date and result kept, and `Not graded` stated rather than inferred. Review cue: the acceptance question. Signal that raises it: a reader citing a grade. Rollback: revert the implementation commit.
- **A heading-line section breaks when a template heading is renamed.** Possible, Minor: LOW, monitor. Owner: W03 author. The `BODY-TABLE-SECTION` template check refuses a heading line the template no longer holds. Review cue: a registry diagnostic. Signal that raises it: a template heading edit. Rollback: update the TemplateDefinition with the rename.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| TemplateDefinitions for templates without a common role, and tables named by heading line | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; machine definitions in `docs/99.templates/registry.json` |
