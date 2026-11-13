---
title: "W03 Small Local Forms Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0186-PLAN-0001"
parent_ids: ["SPEC-0186"]
---

# W03 Small Local Forms Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no document or template heading, sentence or table changes, and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add six form identifiers to the form literal and schema; add the six forms; empty the 12 profiles' H2 lists; move the nine tables to section ids and update the six TemplateDefinition texts; update the policy texts; record W03-D33 to W03-D36. [Task 0001](tasks/tsk-0001-w03-small-local-forms.md) owns execution and evidence.

## Context

SPEC-0178 gave the last three README-shaped local roles their forms; SPEC-0181 and SPEC-0182 fixed the key contract and the empty-section rule. This branch starts from the current W03 stack and is checked against the current `main` before delivery. A read of the tree found:

- six roles with H2 lists and no form, bound by 12 profiles (six sources, six twins), whose lists are exactly the form section sets of the Spec;
- no H3 in any of the eight governed documents or six templates (`domains.md`, `project-map.md`, `glossary.md`, `change-review.md`, `commit-message.md`, `doc-update.md`, `handoff.md`, `results.md` and the templates);
- the H2 titles `Pointer Index`, `Repository Vocabulary`, `Local Extensions` and `Inputs` read by name by two scripts;
- nine tables recorded under heading lines, in four template definitions (vocabulary, task, score, results), against section ids for form roles;
- a form builder that derives the H2 lists from the form and leaves `ordered` false, while the vocabulary profile alone sets `ordered` true;
- the `FormId` literal and schema enum closed at 18, and form tests that pin 12 forms, 18 identifiers and `form is None` for these roles;
- no task or score instance under `.agents/evaluations/`, only their templates;
- a handoff row W03-H28 and decisions W03-D20 and W03-D26 in the SPEC-0161 Task, and no W03-D32 row yet; the first free numbers are those the user gave, W03-D33 to W03-D36.

## Goals & In-Scope

- Code and schema: six form identifiers.
- Registry: six forms, 12 profiles with empty lists, six changed definitions with nine section-id tables.
- Policy texts; W03-D33 to W03-D36 and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: form, parity and registry cases.

## Non-Goals & Out-of-Scope

- Any change to the eight documents or six templates; `reference-report`, `governance-document`, `governance-role` and `provider-native`; the research H3 titles; the full TemplateDefinition record; phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SMALLFORMS-001](spec.md#success-criteria--verification-plan) | Form literal and schema; six forms; profile lists; table sections and definition texts; tests. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-small-local-forms.md) | Failing tests first, then passing; strict registry check; the Task review-digest baseline lines moved in step 1 of the commit order. |
| WORK-002 | [VAL-SMALLFORMS-002](spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document proof; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-small-local-forms.md) | Strict validators, suites, knowledge-surface and prompt-input tests, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the output of the four strict document validators and the six roles' document list before any change.
- Show each changed test failing before its change, then passing.
- Confirm in the Task that the eight documents and six templates are byte-identical before and after (`git diff --stat` empty for them).
- Commit order, four steps: (1) the baseline of the Task review digests alone; (2) the package commit with this package's entry in `docs/03.specs/README.md` and the SPEC-0161 rows W03-D33 to W03-D36; (3) the move of any shifted registry baseline line alone; (4) the implementation with the Task evidence. SPEC-0182 lands first; this package's own three files fall under the open-package layer rule of SPEC-0184. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- If a document gains a diagnostic, stop: fix the form, not the document; report as a repository defect after two failed attempts with no new information.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, schema, the form literal and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval inventory's evidence.

- **A form change breaks a document that reads an H2 by name.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. The titles `Pointer Index`, `Repository Vocabulary`, `Local Extensions` and `Inputs` are copied from the profiles unchanged, and the knowledge-surface and prompt-input tests are in the suite list. Review cue: a failing script test. Signal that raises it: any renamed H2. Rollback: revert the implementation commit.
- **Form order enforcement rejects a document the H2 lists accepted.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. Only the vocabulary profile was ordered; the inventory found the other documents in profile order, and the strict validators run before and after. Review cue: a heading-order diagnostic. Signal that raises it: a new document of these roles in another order. Rollback: revert the implementation commit.
- **Form-identifier parity between code, schema and tests drifts.** Possible, Minor: LOW, monitor. Owner: W05 code. The terminal-contract test compares the literal and the enum and fails first when one side changes. Review cue: that test. Signal that raises it: a form added in one place only. Rollback: revert the implementation commit.
- **Empty-section checks reject a template or document in progress with SPEC-0182.** Unlikely, Minor: LOW, monitor. Owner: W03 author. HEAD holds 151 `BODY-SECTION-BARE` lines, none in the eight documents or six templates, and the forms use `explain_none_or_not_applicable`, as the other forms do, and the strict validators over the tree are compared before and after on the same base. Review cue: a `BODY-SECTION-BARE` diagnostic. Signal that raises it: a rebase onto a changed rule. Rollback: revert the implementation commit.
- **Table sections move to ids and a table check stops matching.** Possible, Minor: LOW, monitor. Owner: W03 author. Nine table entries change (1+3+3+2), the same columns, minimum rows and row identity remain, and the registry check refuses an unknown section id. Review cue: a `REGISTRY_TABLE_SECTION`, `BODY-TABLE-COLUMNS` or `BODY-TABLE-ROWS` diagnostic. Signal that raises it: a section id typo. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The six small local forms | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentences; machine forms in `docs/99.templates/registry.json` |
