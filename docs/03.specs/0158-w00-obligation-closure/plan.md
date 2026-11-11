---
title: "W00 Obligation Closure Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0158-PLAN-0001"
parent_ids: ["SPEC-0158"]
---

# W00 Obligation Closure Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds two execution constraints. First, no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability) and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret, following commit `f3dcab6d`. Second, negative cases run only on disposable copies outside the repository or on recorded evidence.

## Overview

Record the six W00 closure tables defined in [SPEC-0158](spec.md). [Task 0001](tasks/tsk-0001-w00-obligation-closure.md) owns the tables, evidence and criterion acceptance.

## Context

On 2026-11-11 the user asked whether the W00 prompt's items were complete. A re-check of the committed SPEC-0154 and SPEC-0155 Tasks found five unrecorded items and six files handed to more than one stage. The user chose to close W00 before finishing W01 (the SPEC-0157 draft is parked outside the repository) and limited the inventory to cited files. This branch, `claude/w00-closure`, starts at `7963dd04`, the tip of open PR #222. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design; no interface, migration or rollback surface beyond this package changes.

## Goals & In-Scope

- Record the 22 USER22 links, the pull-request table, the negative-case results, the primary-writer table, the OPEN-item dispositions and the cited-file inventory.
- Check completeness with a negative copy and obtain an independent review.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- Editing any file a primary writer is assigned to; each change stays with its stage.
- Reopening the 1,250-line atomization or the 14,028-pair classification.
- A whole-tree inventory.
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLOSE-001](spec.md#success-criteria--verification-plan), [VAL-CLOSE-002](spec.md#success-criteria--verification-plan), [VAL-CLOSE-003](spec.md#success-criteria--verification-plan) | Record the six tables, check completeness, obtain independent review. | Approved Spec and Plan; completed SPEC-0154, SPEC-0155 and SPEC-0156. | [Task 0001](tasks/tsk-0001-w00-obligation-closure.md) | Completeness check with a negative copy, recorded negative cases, independent review, strict document checks and commit hooks. |

## Verification Plan

- Check that USER22 items 01–22 each appear once with a state, that every open item names a stage, that every OPEN item has a disposition and every inventory path is tracked, and that a negative copy is detected.
- Have an independent read-only reviewer check the USER22 links, OPEN dispositions and writer assignments.
- Run the strict document checks, the staged lifecycle check and the active commit hooks on the exact index.
- Architecture compliance: confirm no AD, ADR or governance policy file changed.

## Risks & Mitigations

- **The USER22 carrying-ID mapping is a reading, not a package fact.** Mitigation: the Task says so, and the reviewer checks it.
- **Owner-column citations overstate writers.** Mitigation: the writer table names the real primary writer from each stage's main writing scope.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, and the operator's acceptance. Completion closes W00's recording obligations only; open, blocked and not-certified items stay with their owners.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
