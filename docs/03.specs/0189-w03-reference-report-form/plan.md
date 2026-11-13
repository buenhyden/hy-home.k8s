---
title: "W03 Reference Report Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0189-PLAN-0001"
parent_ids: ["SPEC-0189"]
---

# W03 Reference Report Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three constraints: no document or template heading, sentence or table changes, none of the 13 published Stage 90 members is touched, and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add the `reference-report` identifier to the form literal and schema; add the form with its 31 conditional H3 sections and 39 extensions; empty the six profiles' H2 lists; move the nine tables to section ids and update the three TemplateDefinition texts; update the policy texts; update the W03-H28 row. [Task 0001](tasks/tsk-0001-w03-reference-report-form.md) owns execution and evidence.

## Context

SPEC-0186 and SPEC-0188 gave the other local roles their forms and recorded W03-D33 to W03-D36; this branch starts after both and is checked against the current `main` before delivery. A read of the tree on 2026-11-13 found:

- one role with H2 lists and no form, bound by six profiles (three sources, three twins), whose lists are exactly the eight H2 titles of the Spec;
- 17 authored files (2 audit, 15 research including `0002-archive-retention-and-provenance/m0001`) and no data report; 13 of the 17 are published and 4 are not;
- 60 distinct (H2, H3) pairs in research, 18 shared by two or more documents and 42 in one document of which 3 are template titles; 5 audit pairs, all template titles; 5 data template titles; a registered total of 31 conditional and 39 `local_h3` titles;
- a trial of the form in a scratch copy of `HEAD` (the form literal and schema enum extended, the form and the six empty lists added, the nine tables moved) passed `validate-markdown-profiles.py --mode strict` and `validate-document-contract-registry.py` with no diagnostic and no document change, including `Sources` link-only; before the `link_only` value of `Sources` was set the strict check reported `BODY-SECTION-EMPTY` for the `Sources` of `m0013-scope-application-index.md`, which is why the Spec fixes it;
- nine tables recorded under heading lines (audit 4, research 2 of which one under the H2 `Sources`, data 3), against section ids for form roles;
- the `FormId` literal and schema enum closed at the count SPEC-0188 leaves, and form tests that pin `form is None` for this role;
- the REFERENCE_PUBLISHED_REWRITE check that refuses a staged change to a published member.

## Goals & In-Scope

- Code and schema: one form identifier.
- Registry: one form, six profiles with empty lists, three changed definitions with nine section-id tables.
- Policy texts; the W03-H28 row and an evidence row in the SPEC-0161 Task with the package commit.
- Tests: form, parity, registry and published-member cases; `LocalRoleTableTests` and the heading-line template test move to a synthetic no-form profile while the heading-line validator code stays (retirement is local-forms package 4).

## Non-Goals & Out-of-Scope

- Any change to the 17 documents, the pack READMEs or the three templates; `provider-native`; the governance roles; the full TemplateDefinition record; phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REFFORM-001](spec.md#success-criteria--verification-plan) | Form literal and schema; the form and its extensions; profile lists; table sections and definition texts; tests. | Approved Spec and Plan; SPEC-0186 and SPEC-0188 landed. | [Task 0001](tasks/tsk-0001-w03-reference-report-form.md) | Failing tests first, then passing; strict registry check; the Task review-digest baseline lines moved in step 1 of the commit order. |
| WORK-002 | [VAL-REFFORM-002](spec.md#success-criteria--verification-plan) | Policy texts; unchanged-document and published-member proof; regression and exact-index QA. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-reference-report-form.md) | Strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Re-scan the H3 titles of the 17 documents and three templates by script (fences and comments excluded) and record the counts (60, 18, 42, 3; 5; 5) before the form is written; a different count stops the work.
- Record the output of the four strict document validators and the SHA-256 of the 13 published members before any change.
- Show each changed test failing before its change, then passing.
- Confirm in the Task that the 17 documents and three templates are byte-identical before and after (`git diff --stat` empty for them) and that the registry validator reports no `REFERENCE_PUBLISHED_REWRITE`.
- Commit order, four steps: (1) the baseline of the Task review digests alone; (2) the package commit with this package's entry in `docs/03.specs/README.md`; (3) the move of any shifted registry baseline line alone; (4) the implementation with the Task evidence. SPEC-0186 and SPEC-0188 land first; this package's own three files fall under the open-package layer rule of SPEC-0184. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Stop rule: if any document or template gains a diagnostic, fix the form, not the document; never edit or stage a published member; report as a repository defect after two failed attempts with no new information, and ask the user when the form cannot be written without a document change.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Record the risk class (`medium`: registry, schema, the form literal and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval inventory's evidence.

- **A published member is changed by the migration.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The package edits no document and the trial in a scratch copy needed none; the registry validator refuses a staged change to a published member and the Task records the hashes before and after. Review cue: `git diff --stat` over `docs/90.references/`. Signal that raises it: any document diagnostic that tempts a text fix. Rollback: revert the implementation commit.
- **A document H3 is missing from the registered 70 titles.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The scan is repeated by script before the form is written and the strict validators run before and after; the trial found no `BODY-H3-UNSUPPORTED`. Review cue: a `BODY-H3-UNSUPPORTED`, `BODY-H3-PARENT` or `BODY-H3-ORDER` diagnostic. Signal that raises it: a document added to the tree after the scan. Rollback: revert the implementation commit.
- **A registered H3 with no consumer or a title that drifts.** Possible, Minor: LOW, monitor. Owner: W03 author. The 39 extensions are one-document titles including dated ones, and a published member never changes, so a title can lose its consumer only by supersession; each extension names its removal condition. Review cue: the extension `removal` text at the next form review. Signal that raises it: a retired or superseded member. Rollback: revert the implementation commit.
- **Link-only `Sources` lets a report with only a list of links pass.** Possible, Minor: LOW, monitor. Owner: W03 author. W03-D36 fixes the choice; the form's `Sources` `required_content` asks for the link, grade and retrieval date (stated in the Spec), and semantic review reads the section. Review cue: the semantic review of a new report. Signal that raises it: a report whose `Sources` holds links and no grade. Rollback: revert the implementation commit.
- **Form-identifier parity between code, schema and tests drifts after SPEC-0188.** Possible, Minor: LOW, monitor. Owner: W05 code. The terminal-contract test compares the literal and the enum and fails first when one side changes, and counts are read from the landed state. Review cue: that test. Signal that raises it: a form added in one place only. Rollback: revert the implementation commit.
- **Table sections move to ids and a table check stops matching.** Possible, Minor: LOW, monitor. Owner: W03 author. Nine table entries change (4+2+3), the same columns, minimum rows and row identity remain, and the registry check refuses an unknown section id; the trial passed the registry validator. Review cue: a `REGISTRY_TABLE_SECTION`, `BODY-TABLE-COLUMNS` or `BODY-TABLE-ROWS` diagnostic. Signal that raises it: a section id typo. Rollback: revert the implementation commit.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The reference-report local form | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentences; machine form in `docs/99.templates/registry.json` |
