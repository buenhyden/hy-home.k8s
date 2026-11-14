---
title: "W03 Requirement Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0195-PLAN-0001"
parent_ids: ["SPEC-0195"]
---

# W03 Requirement Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds four constraints: the four Requirements change only by the heading map and the content changes the Spec lists under W03-D55; every requirement ID, statement, priority and acceptance cell is byte-identical before and after; the `Archived Lineage` section of each Requirement is byte-identical before and after; and the diagnostics of the four strict document validators over the tree are equal before and after.

## Overview

Add the Requirement form with its two local H3 extensions to the registry, bind the requirement profile and its template twin to it, give the twin its TemplateDefinition and three tables, have the user review the 68 rationale cells, move the template and the four approved Requirements by the heading map with the new table columns, update the tests and the three texts, and record W03-D55 and the `Downstream owner` handoff. [Task 0001](tasks/tsk-0001-w03-requirement-form.md) owns execution and evidence.

## Context

A read of `main` at `de64c58d` found `sdlc/requirement` and `common/template-sdlc-requirement` with ten required H2 and no form or TemplateDefinition, while the registry holds 18 forms. The four Requirements are all `approved`: REQ-0001 (11 KB), REQ-0002 (13 KB), REQ-0003 (164 KB) and REQ-0004 (28 KB). Each ends with `Archived Lineage` (1, 2, 136 and 15 rows; 122 KB in REQ-0003), which `lineage_retired_identities` and the package-exit rule R3 read at heading level 2 or 3, and which every later package exit extends in REQ-0003. Their only H3 besides `Lifecycle Traceability` and `Archived Lineage` are 16 sections under Overview, Success / Acceptance Criteria, Risks and Traceability; there is no H4. The body contract reads `Lifecycle Traceability` under `Traceability`, both of which the form keeps. No script names `Vision`, `Problem Statement`, `Personas`, `Key Use Cases`, `Success / Acceptance Criteria`, `Scope and Non-goals` or `Risks, Dependencies, and Assumptions`, and none of the 54 fragment links into the four documents names their anchors (37 name `archived-lineage`, 15 a quality scenario or its boundary, one each `reviewed-member-id-transfer` and `traceability`). The requirement table header `Requirement ID`, `Requirement`, `Priority`, `Verification intent` occurs only in the four Requirements and the template; no script or test reads those column names, one REQ-0003 sentence names the `Verification intent` column, and all 68 priority cells are `Must`. The `Downstream owner` column links one architecture description per Requirement in 80 cells; 11 cells are exclusions and 6 carry notes; 10 members are not cited back by that description (one of REQ-0003, nine of REQ-0004). The Stage 01 README still names a `Related Documents` section that no Requirement has. SPEC-0191 edits two REQ-0003 verification cells, SPEC-0192 refuses to generate a Requirement until its creation state is repaired (W03-D48, its own handoff), and SPEC-0188 and SPEC-0189 change the form count before this package.

## Goals & In-Scope

- Registry: the form, two local extensions, two profiles' lists, the TemplateDefinition with its three tables, and the `requirement-basis` reverse-view note.
- Documents: the template and the four Requirements by the heading map; the two renamed table headers, the `Rationale` column with 68 reviewed cells and the trailing `Priority` column; the NFR rows and quality sections under Quality Requirements; each added line and corrected word listed.
- Tests and texts: the form tree and terminal contract tests; the document authoring policy sentence, the Stage 99 README bullet and the Stage 01 README linking rules; the W03-D55 row, the handoff row and the ledger entries.

## Non-Goals & Out-of-Scope

- The other five SDLC forms; architecture descriptions, ADRs, Specs, Plans and Tasks; the `Downstream owner` column and the body contract; the Requirement lifecycle domain and its creation state; the generator; scripts; the H2-list model; Q-07.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-REQFORM-001](spec.md#success-criteria--verification-plan) | The form, the two local extensions, the profile lists, the TemplateDefinition and its three tables, the `relationship_contract` note and the tests. | Approved Spec and Plan; SPEC-0187, SPEC-0188, SPEC-0189, SPEC-0191, SPEC-0192, SPEC-0193 and SPEC-0194 merged in that order, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-requirement-form.md) | Failing tests first, then passing; the strict registry validator. |
| WORK-002 | [VAL-REQFORM-002](spec.md#success-criteria--verification-plan) | The rationale table and its review; the template and the four Requirements by the heading map with the new columns; the three texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | WORK-001; the user's review of the rationale table; no other open package editing a Requirement. | [Task 0001](tasks/tsk-0001-w03-requirement-form.md) | The cell, lineage and identity comparisons; the line comparison; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators, the fragment search and, for each Requirement, the sha256 of its `Archived Lineage` section, its reserved identity set and the sha256 of its map of requirement ID, statement, priority and acceptance cells, keyed by requirement ID and serialized in that order, before any change. The comparison is per ID because the NFR rows leave the middle of the table for the Quality Requirements table.
- Show the registry and form tree tests failing first, then passing, including the old header refused by `BODY-TABLE-COLUMNS`.
- Write the rationale table in the Task before touching a document: one row for each of the 68 requirement IDs with the proposed cell and the source it names, or its explained none. The user reviews the table; the documents take exactly the reviewed cells.
- Move the documents smallest first (REQ-0001, REQ-0002, REQ-0004, then REQ-0003) and run the profile validator after each. After each move compare the cell hashes, and compare the sorted non-heading, non-blank lines outside the requirement tables before and after; record every difference in the Task: the added pointer lines, the header of the second table, the REQ-0003 column-name sentence and each corrected positional word.
- Confirm that the `Archived Lineage` hashes and identity sets are equal, that all 16 former H3 titles exist as H4 with the same anchor, that the old header names no longer occur under `docs/01.requirements` and `docs/99.templates`, that each Requirement's `version` took one major raise while the template kept `0.1.0`, and that the staged lifecycle check, which runs the package-exit rules, passes.
- Before each commit, rebase on `main`, repeat the REQ-0003 move if another package appended to it, and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D55 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run `graphify update .` after the change.
- Record the risk class (`medium`: the registry, a template, four approved Requirements and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A rationale cell states a reason no source gives.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. 68 new cells are written into approved Requirements; each names its source or is an explained none, and the user reviews the whole table before any document changes. Review cue: the rationale table in the Task. Signal that raises it: a cell without a named source, or a cell that differs from the reviewed table. Rollback: revert the implementation commit.
- **A requirement ID, statement, priority or acceptance cell changes while the tables are rewritten.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. A map keyed by requirement ID is hashed before and after for each document, so a row that moves to the Quality Requirements table still compares. Review cue: the four hash pairs. Signal that raises it: a differing hash. Rollback: restore the table from the base commit and repeat.
- **A moved sentence changes meaning or is lost.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. 216 KB moves across four approved Requirements; the line comparison shows every difference and the Task lists it for the user. Review cue: the per-document map and difference list. Signal that raises it: a difference that is not a listed line. Rollback: revert the implementation commit.
- **`Archived Lineage` is damaged.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The section is the last of each document and is not edited; its hash and the reserved identity set are compared before and after. Review cue: the four hash pairs. Signal that raises it: a differing hash, or a retired identity that can be minted again. Rollback: restore the section from the base commit.
- **Another package appends to REQ-0003 during the work.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Every package exit appends a lineage row and SPEC-0191 edits two verification cells; this package merges after SPEC-0194 and the REQ-0003 move is repeated on the rebased file. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict in REQ-0003. Rollback: rebase and repeat the move.
- **A move makes a positional word false.** Possible, Minor: LOW, monitor. Owner: W03 author. The read found eleven such words outside `Archived Lineage`, and the map keeps ten true; each correction is listed. Review cue: the search for `below`, `above` and `following` after the move. Signal that raises it: a word that points the wrong way. Rollback: correct the word.
- **A consumer reads a removed heading, anchor or column name.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. No script names the seven removed H2 titles or the old column names, no link names the removed anchors, and `LINK-FRAGMENT` of SPEC-0193 refuses a broken fragment. Review cue: the fragment and header searches before and after. Signal that raises it: a new link or validator diagnostic. Rollback: revert the implementation commit.
- **The hand-written `Downstream owner` column keeps drifting.** Likely, Minor: MEDIUM, monitor. Owner: the Architecture form package's author. Ten members are already missing on the citing side, and under W03-D55 the column stays until that package completes the citing rows. Review cue: the list of uncited members in the Task. Signal that raises it: the Architecture form package closing without the handoff. Rollback: none needed.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The Requirement form, its local H3 extensions and table contracts | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; `common_forms` and the requirement TemplateDefinition in `docs/99.templates/registry.json` |
