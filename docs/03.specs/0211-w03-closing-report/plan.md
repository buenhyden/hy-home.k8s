---
title: "W03 Closing Report Plan"
version: "2.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0211-PLAN-0001"
parent_ids: ["SPEC-0211"]
---

# W03 Closing Report Implementation Plan

## Overview

### Goal and Boundary

Confirm that W03-D74 and W03-D75 are recorded in the SPEC-0161 Task by an earlier commit (fixed by the user, 2026-11-14), then read the final tree and perform the D72 duties (W03-H10 README and Policy parts, W03-H34, W03-H35, the DOC-12 and DOC-S99 reassignments, the edit of each multi-stage owner, and R45-10 and DOC-11, which this package adds to those duties subject to the user's confirmation in its approval question), append the report tables and the W04 entry statement, run the Final check, and close W03-H10, W03-H34, W03-H35, R45-10, DOC-11 and W03-H20 through the ledger cycle. [Task 0001](tasks/tsk-0001-w03-closing-report.md) owns execution and evidence.

Goals and in-scope:

- The report content of the Spec (execution boundary, item outcomes, decision table, migration table, verification results, acceptance and unfinished work, carried obligation dispositions, old-obligation classification, exit exceptions, W04 entry statement); the D72 duties; the Final check; the closure of W03-H10, W03-H34, W03-H35, R45-10, DOC-11 and W03-H20.

Non-goals and out-of-scope:

- Any code, schema, registry, template or form change; a W03-H10 defect fix (W03-D74 answer 3); the Q-07 preparation (W03-D75); any rewrite of a recorded row; W04 to W11 work; Q-07; cross-repository adoption (W11); tags and hosted CI.

#### Global Constraints

This draft work order follows the [Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no recorded Task row, evidence row, decision, handoff or cell is rewritten, and the SPEC-0161 Task changes by appended lines, the `State` and `Closure` cells of the rows this package closes, the live-table `Owner` and `Resume condition` cells of the rows it reassigns (W03-D74; the live table is entry-authoritative and the legacy rows stay untouched) and its frontmatter `version` and `updated`; no code, schema, registry, template or form is edited; no count, owner or state is typed from memory, because each is read from the final tree and the ledger at implementation; and the diagnostics of the four strict document validators over the tree are equal before and after.

### Assumptions

Read at `main` `eb017bfe` (a base to re-read at commit time):

- `docs/03.specs/` holds one package, SPEC-0161, whose Task is `completed`, carries sections appended after completion and holds the `W03 Decisions` table, the `Residue Handoff` table and the legacy rows W03-H10, W03-H20, W03-H34, W03-H35, DOC-12 and DOC-S99.
- `docs/03.specs/work-residue-ledger.json` held 76 entries, 28 owned by `W03` alone; the gate is `scripts/validate-work-residue-ledger.py` and the view is `scripts/work-residue-ledger.py`.
- W03-D70 to W03-D73 are recorded by the SPEC-0194 implementation commit and may not be on `main` yet; W03-D72 is the source of the D72 duties.
- SPEC-0209 appends the `Disposition Input` table and the corrections; the Q-07 preparation package (SPEC-0212, W03-D75) prepares the number transition before this package; SPEC-0210 adds the creation state of the `requirement` lifecycle and closes W03-H43; both land before this package. The packages SPEC-0194 to SPEC-0208 are drafts or approved and unmerged; their merged state decides every count.

## Dependencies

### Prerequisites

The prerequisites of each work unit are in the Dependencies column of the [Work Breakdown](#work-breakdown) table.

### Dependency Order

The order of the work units follows the Dependencies column of the [Work Breakdown](#work-breakdown) table.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W03REPORT-001](spec.md#criteria) | Read the final tree and the ledger; append the report tables and the dispositions of OPEN-Q03 and WP-10, 11, 12, 13, 17, 18, 47 and 52, the old-obligation classification and the exit exceptions. | W03-D74 and W03-D75 recorded; SPEC-0194 to SPEC-0206, SPEC-0210, the Q-07 preparation package (SPEC-0212) and SPEC-0209 merged. | [Task 0001](tasks/tsk-0001-w03-closing-report.md) | Counts re-read; append-only diff; strict validators. |
| WORK-002 | [VAL-W03REPORT-002](spec.md#criteria) | The D72 duties: the PASS reads for W03-H10 (README and Policy), W03-H34, W03-H35, R45-10 and DOC-11 (the last two once W03-H13 and W03-H15 are terminal), the DOC-12 and DOC-S99 reassignments and the multi-stage owner edits (OPEN-07, OPEN-06, GOV-04, W03-H15, W03-H29) with a correction EVD row each, the matching ledger edits. | WORK-001; if a README or Policy consumer defect is found, W03-D74 answer 3 applies (stop; a small fix package lands first). | [Task 0001](tasks/tsk-0001-w03-closing-report.md) | The ledger gate before and after; diff limited to the named cells. |
| WORK-003 | [VAL-W03REPORT-003](spec.md#criteria) | The W04 entry statement; the Final check before and after the closing commit; the closure of W03-H10, W03-H34, W03-H35, R45-10, DOC-11 and W03-H20. | WORK-002; the user's acceptance. | [Task 0001](tasks/tsk-0001-w03-closing-report.md) | The Final check listing; the gate; staged QA and hooks. |

### Change and Rollback

The rollback, where a risk states one, is under [Risks and Mitigations](#risks-and-mitigations).

## Verification Plan

### Verification Matrix

- Record the four strict document validators and the ledger gate before any change.
- Read every figure again from the tree, the ledger and the Git diffs before writing it; record each observed count beside the figure of the Spec.
- Confirm the diff of the SPEC-0161 Task has added lines, the named `State`, `Closure`, `Owner` and `Resume condition` cells and the frontmatter only.
- Run the ledger gate after each appended report table: no report table may sit under a heading containing `Handoff` or `Conflicts` or lead with an H-ID column.
- Run the Final check with the `\bW03\b` filter on the full `--state open` output, not `--owner`.
- Record the risk class (`low`: appended Task records and ledger data; no code, permission, secret-handling, hook or workflow) and the core-diff checklist.

Completion criteria:

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance. The Spec leaves `draft` with its approval receipt; the open questions are answered by W03-D74 and the Q-07 position by W03-D75. A W03-H10 defect that sends the work to a separate package (W03-D74 answer 3: stop, fix package first) leaves W03-H10 and W03-H20 open: that is the recorded state, not a failure.

### Stage Placement

- Run the Final check twice: after the implementation commit (W03-H20 is the only W03-owned open entry, every later-stage entry has an owner) and after the closing commit (none).
- Merge order: SPEC-0191, SPEC-0207, SPEC-0192 to SPEC-0206 as their dependencies allow, SPEC-0208, SPEC-0210 (after SPEC-0206), the Q-07 preparation package (SPEC-0212, W03-D75), SPEC-0209, then this package; SPEC-0211 stays unmerged while SPEC-0212 is unmerged; the W03 exit follows; DOC-12 and Q-07 come only after W11.
- Commit order: (1) the package commit with this Task, the Korean Stage 03 README entry (no decision row: W03-D74 and W03-D75 are recorded in the SPEC-0161 Task by an earlier commit); (2) `.secrets.baseline` changes alone, for the reviewed digests; (3) the implementation commit: the reassignments, the PASS read rows, the appended report and the ledger `owner` and `resume_condition` edits; (4) after the user's acceptance, the closing commit that appends the `PASS` closure rows, changes the closure cells and deletes the terminal entries; (5) the package exit. Run the staged lifecycle check before each commit.

## Risks

### Risks and Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor).

- **A W03 item is closed that the tree does not support.** Possible, Severe: HIGH, mitigate. Owner: W03 author. Every closure row names the file, line and test it read; a read that finds a gap hands the row to a named owner. Review cue: each PASS read row. Signal that raises it: a closure with no file named.
- **The report becomes a second owner of decisions, registry values or ledger state.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. Tables cite by ID and derive from the ledger. Review cue: any cell that restates a decision text or a count with no read date.
- **A count or owner is stale at merge.** Likely, Moderate: MEDIUM, mitigate. Owner: W03 author. The package merges last; figures are re-read at commit time. Review cue: the diff against current HEAD and the ledger listing.
- **Reassignment is read as hiding DOC-12.** Unlikely, Moderate: LOW, monitor. Owner: W03 author. The entry stays open under owner Q07 with a resume condition and a correction row; no terminal state is set. Review cue: the ledger entry after the edit.
- **The report is read as package completion or W04 approval.** Possible, Moderate: MEDIUM, mitigate. Owner: W03 author. The acceptance table and the W04 entry statement say W03 only, no approval, W04 on the user's selection. Review cue: the W04 entry statement.
- **Not scored:** the state of W05 to W11 and of the other repositories; the report names owners and reads none of their work.

### Escalation

Escalation follows [Failure and Edge Cases](spec.md#failure-and-edge-cases) of the Spec.

## Promotion Map

### Durable Meaning

The durable contracts are the first column of the table under Owner and Receipt.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
