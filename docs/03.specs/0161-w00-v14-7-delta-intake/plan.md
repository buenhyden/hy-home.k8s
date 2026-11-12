---
title: "W00 v14.7 Delta Intake Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0161-PLAN-0001"
parent_ids: ["SPEC-0161"]
---

# W00 v14.7 Delta Intake Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds one execution constraint: no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability), `.secrets.baseline` entries marking reviewed document digests as non-secret and, at exit, the REQ-0003 Archived Lineage.

## Overview

Record the W00 v14.7 delta tables defined in [SPEC-0161](spec.md). [Task 0001](tasks/tsk-0001-w00-v14-7-delta-intake.md) owns the tables, evidence and criterion acceptance.

## Context

On 2026-11-12 the user supplied the v14.7 W00 prompt and the package location `_workspace/workspace_execution_tasks/`. SPEC-0154 to SPEC-0160 consumed package v14.2 and are closed. This branch, `claude/w00-v14-7-intake`, starts at `4a47cb40`, the tip of `main` after PR #227. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design; no interface, migration or rollback surface beyond this package changes.

## Goals & In-Scope

- Record the edition delta, requirement-change links, pull-request table, handoff tables, OPEN dispositions, conflicts and read denominator.
- Check completeness with a negative copy and obtain an independent review.
- Add this package to the Stage 03 README.

## Non-Goals & Out-of-Scope

- Editing any file a writer stage is assigned to.
- Reopening the 1,250-line atomization, the 14,028-pair classification or the 208 legacy packages.
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DELTA-001](spec.md#success-criteria--verification-plan), [VAL-DELTA-002](spec.md#success-criteria--verification-plan) | Record the delta tables, check completeness, obtain independent review. | Approved Spec and Plan; completed SPEC-0154 to SPEC-0160. | [Task 0001](tasks/tsk-0001-w00-v14-7-delta-intake.md) | Completeness check with a negative copy, independent review, strict document checks and commit hooks. |

## Verification Plan

- Check that every changed row, clause and OPEN identifier appears once with a state, that every open row names a writer, that every cited path is tracked, and that a negative copy is detected.
- Have an independent read-only reviewer check the links, writers and dispositions.
- Run the strict document checks, the staged lifecycle check and the active commit hooks on the exact index.
- Architecture compliance: confirm no AD, ADR or governance policy file changed.

## Risks & Mitigations

- **The delta base is v14.1, not the exact v14.2 bytes.** Mitigation: v14.1 precedes v14.2, so every v14.2 change is inside the measured delta; the Task says so.
- **Agent surveys read some large files only in part.** Mitigation: the read denominator marks them PARTIAL, and the writer stage re-reads them before editing.

## Completion Criteria

Both criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance. Completion closes W00's v14.7 recording obligations only; open and decision-needed rows stay with their writers. At package exit the REQ-0003 Traceability sentence that links this package is replaced by its Archived Lineage summary.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
