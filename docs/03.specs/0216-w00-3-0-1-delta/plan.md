---
title: "W00 3.0.1 Delta Intake Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-15"
artifact_id: "SPEC-0216-PLAN-0001"
parent_ids: ["SPEC-0216"]
---

# W00 3.0.1 Delta Intake Implementation Plan

## Overview

### Goal and Boundary

This Plan executes [SPEC-0216](spec.md). Once it is complete, the SPEC-0161 Task holds the `3.0.1 Edition Delta` and `3.0.1 Verdicts` tables and one EVD row, and nothing else in the tree has changed apart from this package and its Stage 03 README entry. The work of the `CHANGE` rows, the ledger and every stage after W00 are excluded.

#### Global Constraints

Every work unit inherits the constraints of the approved [Spec](spec.md). Additional constraints:

- Only appended tables and one appended row are written to the SPEC-0161 Task, plus its frontmatter `version` and `updated`.
- `_workspace/` is read, never written.
- The strict document validators and the ledger gate give equal results before and after.

### Assumptions

- `main` is `003b8350`, the worktree is clean and no PR is open (observed 2026-11-15).
- The ledger holds 57 open entries. The `CI-SCOPE` and `AGENT-04` live rows carry rows 7 and 13 of the verdict table.
- AD-0006 and ADR-0060 are touched by no work unit; no interface, migration or rollback beyond the branch applies.

## Dependencies

### Prerequisites

- Spec and Plan approval by the user, recorded in the Task.
- PKG present at `_workspace/governance/workspace_governance_3_0_1_20261115/` with its hashes unchanged.

### Dependency Order

WORK-001 starts after approval and runs as a single unit.

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-W00D-001](spec.md#criteria) | Hash the PKG inputs again; observe the base, PR state and ledger count again; append the two tables and the EVD row to the SPEC-0161 Task; bump its version. | Spec and Plan approval | [Task 0001](tasks/tsk-0001-w00-3-0-1-delta.md) | Hashes equal the manifest; strict validators and ledger gate equal before and after. |

### Change and Rollback

WORK-001 changes only the SPEC-0161 Task. Undo it by deleting the branch before commit, or by reverting the commit after it.

## Verification Plan

### Verification Matrix

| Work Unit | Check | Lane |
| --- | --- | --- |
| WORK-001 | `tools/validate_package.py --root .` and `sha256sum` in PKG | local, read-only |
| WORK-001 | Four strict document validators; `scripts/validate-work-residue-ledger.py --root .` | local static |
| WORK-001 | Staged lifecycle check and `scripts/qa.py staged` on the exact index | local, at commit |

Architecture compliance: no AD, ADR, policy, registry, template or code file changes. The work closes without any live or hosted evidence claim.

### Stage Placement

The validators run before and after the edit. The staged checks run once in the commit hooks on the exact index, and only when the user asks for a commit. No check is repeated at push or PR.

## Risks

### Risks and Mitigations

- **A verdict is read as acceptance of the item.** Possible, Moderate: MEDIUM, mitigate. Owner: platform. Each row names its read scope, and the EVD row states that it accepts nothing.
- **A `CHANGE` row is lost because no ledger entry is seeded.** Possible, Minor: LOW, mitigate. Owner: the named stage. Each row names a live row or the stage prompt that carries it.
- **Digests trip the secret scan.** Likely, Minor: MEDIUM, mitigate. Owner: platform. Reviewed `.secrets.baseline` entries only.

### Escalation

Stop and ask if a current document contradicts a row, or if a PKG hash differs from its manifest. Resume when the user answers.

## Promotion Map

### Durable Meaning

None remains: the tables are analysis for the stage owners.

### Owner and Receipt

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| none | none | none | No durable contract was introduced |
