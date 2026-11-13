---
title: "W03 Work Ledger Contract Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-13"
artifact_id: "SPEC-0185-PLAN-0001"
parent_ids: ["SPEC-0185"]
---

# W03 Work Ledger Contract Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two constraints: no ledger file, schema, script, validator or test is added, and no recorded Task row, EVD row, decision or handoff is rewritten (only the state cells of the `LEDGER` conflict row and the W03-H30 row are refreshed in place); only the sentences named in the Spec change, plus the SPEC-0161 Task rows and this package's README entries.

## Overview

Create `ADR-0060` (`proposed`) that narrows the no-ledger clauses of ADR-0031, ADR-0036, ADR-0047 and ADR-0048 to "no competing progress ledger"; amend REQ-0003 FR-0019, FR-0022, Scope and Non-goals, the Evaluation Expectation and Traceability, and AD-0006; add one clarifying sentence to five governance texts and the knowledge-map Outputs; record W03-D37 to W03-D40, then append the superseding EVD row and refresh the two state cells. [Task 0001](tasks/tsk-0001-w03-work-ledger-contract.md) owns execution and evidence. Package 2 (W03-H30) builds and seeds the ledger.

## Context

A read of the tree found:

- REQ-0003 FR-0019 (line 72), FR-0022 (line 75, check cell "No ledger file exists"), Scope and Non-goals (lines 119 and 121), the Evaluation Expectation (line 143) and Traceability (line 178) disclaim a ledger or "central" state, and line 121 says the single machine ledger "stays not adopted";
- ADR-0036 lines 60-64, ADR-0047 lines 95 and 127, ADR-0048 line 183 and ADR-0031 lines 20, 35, 113 and 122 hold the no-ledger and roster clauses; ADR-0036 states a governance-validator guard that `scripts/validation/repository/quality.py` lines 347-348 and the `.agents` route test, not the governance validator, actually provide; ADR-0036, ADR-0047 and ADR-0048 already carry dated clarifications that point to ADR-0055, the precedent for a scoped amendment;
- AD-0006 lines 41, 95 and 226-231 disclaim a shared progress ledger or central roster, its traceability rows for FR-0019 and FR-0022 are at about lines 369 and 372, and its Archived Lineage list at about lines 420-422;
- `work-lifecycle.md` lines 55 and 124, `context-and-memory.md` lines 17 and 73-74, `quality.md` line 253, `document-authoring.md` lines 185 and 253 and the knowledge-map Outputs mention a progress or other ledger;
- the last decision of the SPEC-0161 Task at HEAD is W03-D31, the last handoff W03-H32 and the last EVD row EVD-042; D32 to D36 come from other packages, so the numbers are re-read at commit time and the later package rebases; the `LEDGER` row says "No conflict; existing rule kept" and EVD-018 says the machine-ledger rejection "agrees with v14.7 and stays";
- the free ADR number is 0060; the lifecycle code admits a new ADR only as `proposed` (`scripts/document_lifecycle.py` lines 285-293), and ADR-0059 and ADR-0055 each reached `accepted` in a second commit after the user's acceptance.

## Goals & In-Scope

- Text: `ADR-0060` and its Korean README entry, the REQ-0003 and AD-0006 sentences, the four dated ADR clarifications, the governance and skill sentences.
- Tracking: in the SPEC-0161 Task, W03-D37 to W03-D40 in the package commit; the superseding EVD row (`Resolves none`, citing 0185 Task evidence IDs) and the two refreshed state cells in the implementation commit.

## Non-Goals & Out-of-Scope

- The ledger file, schema, derivation script, validator, seed and tests (package 2), Stage 90 documents, hold, disposition and retention entries, rewriting recorded rows, and phase 3.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LEDGER-001](spec.md#success-criteria--verification-plan) | Write `ADR-0060` as `proposed` with its README entry and the four dated clarifications; amend REQ-0003 and AD-0006. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-w03-work-ledger-contract.md) | Strict validators; each sentence read against the ADR decision text. |
| WORK-002 | [VAL-LEDGER-002](spec.md#success-criteria--verification-plan) | Governance and knowledge-map sentences; the superseding EVD row and refreshed state cells; regression and exact-index QA; then the Task Evidence row with the user's ADR-0060 acceptance answer and the `proposed` to `accepted` flip alone. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-work-ledger-contract.md) | Strict validators, suites, quality gate, markdownlint, staged QA and hooks; the `rg` checks. |

## Verification Plan

- Record the four strict document validators before any change.
- Re-verify every cited line number against the current file before each edit; the sentence decides the target.
- Run the `rg` checks of the Spec and read every hit against the rule stated there.
- Commit order: (1) the package commit with this Task, the Korean Stage 03 README entry and decision rows W03-D37 to W03-D40; (2) `.secrets.baseline` changes alone; (3) the implementation with `ADR-0060` as `proposed`, its README entry, the four dated clarifications, the REQ-0003, AD-0006 and governance text, the superseding EVD row and the two state cells; then a distinct Task Evidence row recording the user's ADR-0060 acceptance answer (actor user); (4) the `proposed` to `accepted` flip alone; then the Task evidence and the criterion acceptance. Run the staged lifecycle check before each commit. The acceptance of the ADR is not asked inside the acceptance of VAL-LEDGER-001.
- Merge order: other packages append to the same governance files, READMEs and the SPEC-0161 Task; re-read and rebase before each commit and renumber appended rows on collision.
- Architecture compliance: ADR-0031, ADR-0036, ADR-0047 and ADR-0048 bodies unchanged except the dated clarification paragraph; AD-0006 changes only the named places.
- Record the risk class (`medium`: requirement, architecture and governance text with a policy-direction change; no registry, code, permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval review's evidence.

- **The amendment is read as restoring a progress ledger or as a second owner of execution state.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. The review found the draft clauses narrow and the entry `state` limited to open or terminal, never a Task status. Review cue: the `rg` read of remaining hits. Signal that raises it: a sentence that lets the ledger hold status or evidence. Rollback: revert the implementation commit.
- **The lifecycle create and accept edge fails.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. A new ADR can only enter as `proposed`, and ADR-0055 and ADR-0059 needed a second commit. Commit 3 creates it `proposed` and commit 4 flips it alone. Review cue: the staged lifecycle check. Signal that raises it: a lifecycle edge diagnostic. Rollback: set the status back to `proposed`.
- **Concurrent packages edit the same governance files, READMEs and the SPEC-0161 Task.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Cited lines are located by sentence, appended numbers are re-read at commit time and the later package rebases. Review cue: the diff against current HEAD before each commit. Signal that raises it: a duplicate ID or moved-line diagnostic. Rollback: renumber or correct before commit.
- **The FR-0019 must lands before its implementation.** Possible, Minor: LOW, monitor. Owner: W03 author. Its own check cell says "Built by the W03-H30 package 2", and W03-H30 stays open until package 2 passes. Review cue: the W03-H30 state cell. Signal that raises it: a reviewer reading the check as already passing. Rollback: revert the FR-0019 sentence.
- **A cited line moved or a clause was missed, leaving a contradictory no-ledger sentence.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Each edit is located by its sentence and the `rg` check lists leftovers. Review cue: the `rg` check. Signal that raises it: a hit that neither forbids a competing ledger nor names the retired structure. Rollback: correct the sentence.
- **ADR acceptance is taken as given before the user's recorded answer.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The flip commit follows the distinct Task Evidence row. Review cue: the ADR `status`. Signal that raises it: `accepted` with no recorded answer. Rollback: set the status back to `proposed`.

## Completion Criteria

Both criteria need PASS evidence, no unresolved required failure and the operator's acceptance. ADR-0060's acceptance is a separate recorded answer, not part of either criterion.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Work residue ledger rule: residue only, no competing progress ledger | `ADR-0060`; [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) FR-0019 and FR-0022 | The ADR decision text and the two requirement rows; the ledger itself and its schema follow in package 2 |
