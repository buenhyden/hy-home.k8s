---
title: "W02 3.0.1 Disposition Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0219-PLAN-0001"
parent_ids: ["SPEC-0219"]
---

# W02 3.0.1 Disposition Implementation Plan

## Overview

### Goal and Boundary

This Plan executes [SPEC-0219](spec.md). When it is complete:

- the 18 approved or transferred entries are closed and deleted from the ledger;
- the two seeds exist;
- every open entry is stated by function, owner and completion condition;
- the final cutover targets are listed.

Nothing is deleted outside the ledger, and nothing in code, tests, policy, forms or the remote changes.

#### Global Constraints

Every work unit inherits the constraints of the approved [Spec](spec.md). Additional constraints:

- A row and its ledger entry change together, and the gate runs after each step.
- No entry outside the user's four approved groups and the two transfers is closed.

### Assumptions

- `main` is `c6513839`, and the ledger holds 57 entries.
- The gate accepts one PASS EVD row as the Closure of several rows.
- No architecture view or ADR changes; the rollback is the branch.

## Dependencies

### Prerequisites

- The user's withdrawal approval of 2026-11-15, recorded in the Spec.
- Spec and Plan approval.

### Dependency Order

WORK-001 (closures) runs first. WORK-002 (seeds and tables) reads the ledger after it.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W02D-001](spec.md#criteria) | Append five closure EVD rows to the SPEC-0161 Task (groups A to D and the transfers). Make the 18 rows and entries terminal, run the gate, delete the entries, run the gate. | Approval | [Task 0001](tasks/tsk-0001-w02-disposition.md) | Gate PASS after each step; 39 entries. |
| WORK-002 | [VAL-W02D-002](spec.md#criteria) | Seed W05-H09 and Q07-H01; append the `W02 Disposition` and `Q07 Target Preparation` tables and one EVD row. | WORK-001 | [Task 0001](tasks/tsk-0001-w02-disposition.md) | Gate PASS at 41 entries; strict validators. |

### Change and Rollback

Both units are record and ledger edits. Undo by deleting the branch, or by reverting the merge commit after merge.

## Verification Plan

### Verification Matrix

| Work Unit | Check | Lane |
| --- | --- | --- |
| WORK-001 | `scripts/validate-work-residue-ledger.py --root .` after each step | local static |
| WORK-002 | Ledger gate; four strict document validators | local static |
| All | `qa.py staged` through the hooks | local static, at commit |

Architecture compliance: ADR-0060 is followed and not changed.

### Stage Placement

The gate runs at each step, and the staged QA runs once per commit.

## Risks

### Risks and Mitigations

- **An entry outside the approved groups is closed.** Unlikely, Severe: MEDIUM, mitigate. Owner: platform. The script closes only the 18 named IDs and asserts the count.
- **A withdrawal is read as completed work.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. Each closure row says "withdrawn by the user's approval" or "transferred to", never "completed".
- **A seed restates what an open entry already carries.** Possible, Minor: LOW, mitigate. Owner: platform. W03-H11, W05-H06 and W05-H08 are checked against W05-H09, and the overlap is named.

### Escalation

Stop and ask if an approved item turns out to hold a still-valid function that no other entry carries.

## Promotion Map

### Durable Meaning

None: the ledger and the SPEC-0161 Task are the owners.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
