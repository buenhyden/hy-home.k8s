---
title: "W03 Architecture Form Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0197-PLAN-0001"
parent_ids: ["SPEC-0197"]
---

# W03 Architecture Form Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds four constraints: the four descriptions change only by the heading map and the content changes the Spec lists; the four Requirements change only by the removed column and their pointer line, with every requirement ID and acceptance-criterion cell byte-identical; no ADR changes; and the diagnostics of the four strict document validators over the tree are equal before and after. The design choices follow W03-D57 as the Spec states them.

## Overview

Add the Architecture form with its two local H3 extensions to the registry, bind the description profile and its template twin to it, give the twin its TemplateDefinition and tables, move the template and the four active descriptions by the heading map, complete the citing rows so that every requirement member is cited, add the derived coverage check, remove the `Downstream owner` column from the requirement body contract, the four Requirements and their template, and update the tests, the texts and the `relationship_contract` entry. [Task 0001](tasks/tsk-0001-w03-architecture-form.md) owns execution and evidence.

## Context

A read of `main` at `de64c58d` found `sdlc/architecture-description` and its template twin with seven required H2 (Overview, Boundaries & Non-goals, Quality Attributes, System Overview & Context, Data Architecture, Infrastructure & Deployment, Traceability) and no form or TemplateDefinition. The four descriptions are all `active`: AD-0004 (10 KB), AD-0005 (10 KB), AD-0006 (62 KB) and AD-0007 (40 KB). They hold 23 H3 besides `Lifecycle Traceability` and `Archived Lineage`, no H4, 20 tables and 85 `Lifecycle Traceability` rows; AD-0006 and AD-0007 end with `Archived Lineage` (42 and 11 rows), whose first column reserves retired identities. No script, test or other document names a removed H2 title. Of the 14 fragment links into the descriptions, ten name `Overview` or an H3 that keeps its anchor, and four name a removed H2 anchor, all in the `arc42 coverage` table of AD-0007. AD-0006 and AD-0007 hold nine positional words outside `Archived Lineage`. The body contract cites requirement members in `Upstream requirement`: AD-0004 cites six of six, AD-0005 six of six, AD-0006 37 of 38 and AD-0007 nine of 18; all nine uncited members of REQ-0004 are named in the `Transferred requirement members` table of AD-0007 and nowhere else in it. The Requirement `Downstream owner` column holds 80 links, one description per Requirement, 11 exclusions and 6 notes; 20 of the links sit on the 23 acceptance-only rows, which name no member, and each of those 20 acceptance criteria is already named by a row of its description; no script names the column, which the link validator reads through `target_link_column`. SPEC-0195 moves the Requirements and leaves this column with a handoff to this package; SPEC-0193 adds `relationship_contract` and `LINK-FRAGMENT`; SPEC-0196, which merges before this package, adds `contract_version` to every definition and the rule `REGISTRY_TEMPLATE_RECORD`, which the new definition must pass.

## Goals & In-Scope

- Registry: the form, two local extensions, the description profiles' lists, the TemplateDefinition with its `contract_version` and tables, the two-column requirement body contract and table contract, and the `requirement-basis` entry.
- Documents: the description template and the four descriptions by the heading map; the reviewed citing rows; the four Requirements and the requirement template without the column; each added line and corrected word listed.
- Code, tests and texts: `REQUIREMENT-COVERAGE` with failing-first tests; the form tree, terminal contract and link boundary tests; the document authoring policy sentence, the Stage 99 README bullet and the Stage 01 and Stage 02 README linking rules; the SPEC-0161 Task rows and ledger entries.

## Non-Goals & Out-of-Scope

- ADRs and the ADR form; the Spec, Plan and Task forms; requirement tables, statements and acceptance cells; the list items under a Requirement's Downstream Links; a per-member reverse view tool; the Requirement creation state; the H2-list model; Q-07.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ADFORM-001](spec.md#success-criteria--verification-plan) | The form, the two local extensions, the description profiles' lists, the TemplateDefinition and its tables, and the form tree tests. | Approved Spec and Plan; SPEC-0195 and SPEC-0196 merged in that order, then this package; rebase on `main` and renumber appended rows before each commit. | [Task 0001](tasks/tsk-0001-w03-architecture-form.md) | Failing tests first, then passing; the strict registry validator with `REGISTRY_TEMPLATE_RECORD`. |
| WORK-002 | [VAL-ADFORM-002](spec.md#success-criteria--verification-plan) | The description template and the four descriptions by the heading map, with the `arc42 coverage` links and any false positional word corrected. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-architecture-form.md) | The line, lineage and identity comparisons; strict validators and markdownlint. |
| WORK-003 | [VAL-ADFORM-003](spec.md#success-criteria--verification-plan) | The reviewed citing rows; `REQUIREMENT-COVERAGE` and its tests; the column removal in the body contract, the four Requirements and the requirement template; the `relationship_contract` entry; the texts; the SPEC-0161 Task rows and ledger entries; regression and exact-index QA. | WORK-002; the user's review of the two tables; no other open package editing a Requirement or a description. | [Task 0001](tasks/tsk-0001-w03-architecture-form.md) | The member citation list; the cell comparison; strict validators, suites, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Record the four strict document validators, the fragment links into the descriptions, the member citation list and, for each document with `Archived Lineage`, the section's sha256 and reserved identity set before any change; record the sha256 of each Requirement's ordered requirement ID and acceptance-criterion cells.
- Show the form tree tests and each coverage case failing first, then passing, and the derived record of the description template passing `REGISTRY_TEMPLATE_RECORD`.
- Move the descriptions smallest first (AD-0004, AD-0005, AD-0007, then AD-0006) and run the profile validator after each. After each move compare the sorted non-heading, non-blank lines before and after and record every difference in the Task.
- Write two tables in the Task before WORK-003 touches a document: the new citing rows with the heading each cell comes from, and the disposition of the 36 removed cells the coverage check does not account for (the 17 that are not a single link and the 20 links on acceptance-only rows, one in both groups) with the place each fact has afterwards. The user reviews both; the documents take exactly the reviewed rows.
- Add the citing rows first and show the coverage rule passing over the tree with the column still present; then remove the column, so no commit leaves a member without a written relation.
- Confirm that the cell hashes, the `Archived Lineage` hashes and the identity sets are equal, that all 23 former H3 titles exist as H4 with the same anchor, and that no member is uncited.
- Before each commit, rebase on `main`, repeat a document move if another package edited that document, and renumber the rows this package appends to the SPEC-0161 Task. Commit order: the package commit with the W03-D57 row; then `.secrets.baseline` changes alone; then the implementation with the Task evidence. Run `graphify update .` after the code change.
- Record the risk class (`medium`: the registry, two templates, eight current documents, one validator rule and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read.

- **A new citing row states something its description does not say.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. About ten rows are written into active descriptions; each cell names its source heading and the user reviews the table first. Review cue: the citing-row table in the Task. Signal that raises it: a cell without a source, or a row that differs from the reviewed table. Rollback: revert the implementation commit.
- **Removing the column drops a fact.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. 36 cells are not reproduced by a member's citing row: 17 hold an exclusion or a note and 20 are links on acceptance-only rows. Each gets a row in the disposition table and the user reviews it. Review cue: the disposition table in the Task. Signal that raises it: a removed cell with no row, or a row with no place. Rollback: restore the column from the base commit.
- **The coverage rule blocks a legitimate Requirement or misses a gap.** Possible, Moderate: MEDIUM, monitor. Owner: W05 code. It reads registry-declared columns only, counts enforced statuses only and has a case for each branch, including the exclusion line of W03-D57. Review cue: the rule's tests and the member citation list. Signal that raises it: a diagnostic on a document the package did not touch, or an uncited member that passes. Rollback: revert the implementation commit.
- **A moved sentence changes meaning or is lost.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. 123 KB moves across four active descriptions; the line comparison shows every difference and the Task lists it. Review cue: the per-description map and difference list. Signal that raises it: a difference that is not a listed line. Rollback: revert the implementation commit.
- **`Archived Lineage` is damaged.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The section is the last of AD-0006, AD-0007 and each Requirement and is not edited; hashes and identity sets are compared. Review cue: the hash pairs. Signal that raises it: a differing hash. Rollback: restore the section from the base commit.
- **Another package edits REQ-0003 or a description during the work.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Every package exit appends to REQ-0003, and SPEC-0195 and SPEC-0196 merge before this package; the affected move is repeated on the rebased file. Review cue: the base commit recorded in the Task. Signal that raises it: a merge conflict. Rollback: rebase and repeat the move.
- **A link or positional word points at a removed heading.** Possible, Minor: LOW, monitor. Owner: W03 author. Four `arc42 coverage` links and nine positional words are known; `LINK-FRAGMENT` refuses a broken fragment. Review cue: the fragment list before and after. Signal that raises it: a link validator diagnostic. Rollback: correct the link.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The Architecture form, its local H3 extensions and table contracts | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms sentence; `common_forms` and the description TemplateDefinition in `docs/99.templates/registry.json` |
| The requirement-to-architecture relation written once by the description, with derived coverage | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Link and relationship rule; the `requirement-basis` entry of `relationship_contract` and `REQUIREMENT-COVERAGE` |
