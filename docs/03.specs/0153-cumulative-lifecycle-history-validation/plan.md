---
title: "Cumulative Lifecycle History Validation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0153-PLAN-0001"
parent_ids: ["SPEC-0153"]
---

# Cumulative Lifecycle History Validation Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) under the user's separate 2026-11-11 scoped approval. Preserve the original SPEC-0152 and accepted ADR-0056 bytes and evidence. Keep all current Git history and lifecycle caps; do not change Registry states, schemas, receipts or gates. Local commits wait for the actual broad-history checks, affected QA and independent review to pass.

## Overview

Repair the two observed cumulative-history paths in [SPEC-0153](spec.md): bounded ADR copy provenance and registered Task-template first-record replay, then remove redundant historical context work while retaining every required check. [Task 0001](tasks/tsk-0001-cumulative-lifecycle-history-validation.md) owns execution evidence and acceptance.

## Context

Actual local `f6c1c875` → `38ec2bea` explicit-ref session `71672` failed `LIFECYCLE-CREATE` for ADR-0056 absent → accepted. Actual `f6c1c875` → `4033d38e` explicit-ref session `77072` separately failed `LIFECYCLE-CREATE` for the SPEC-0152 Task absent → completed. Adjacent `4033d38e` → `38ec2bea` explicit-ref session `99517` passed; it does not prove the broad ranges. Read-only source tracing found Git `C004` from retained ADR-0055 and `C002` from the registered Task template. Isolating the copy signals lets first edges pass, then repeated full evidence snapshots exceed the existing 16 MiB work cap. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the system view; accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) is an immutable decision, not a file to amend for this validator repair.

## Goals & In-Scope

- Add RED/GREEN focused historical fixtures for both valid broad ranges and each named negative boundary.
- In `scripts/validate-document-lifecycle.py`, admit only a proposed ADR with an unchanged retained same-profile source, absent target and distinct unique canonical IDs, and an unchanged registered Task template whose `draft` initial state follows the ordinary route or whose `ready`/`in-progress`/`blocked` initial state passes its existing local extension and applicable context checks. Git copy score and chosen source are not authorship proof.
- Reduce repeated full-snapshot work for ordinary ADR edges and evidence-valid Task replay, preserving Task parent, evidence, receipt, terminal and cancellation obligations and all existing budgets.
- Check actual broad explicit-ref and local CI modes, affected QA, exact index and independent semantic/security review. Keep hosted and live evidence separate.

## Non-Goals & Out-of-Scope

- No rewrite of accepted ADR-0056, closed SPEC-0152 or its Task evidence, and no Git history rewrite.
- No initial-state, Registry, schema, receipt, global copy, candidate/event or 16 MiB budget change. No unrelated Task template-copy route or bypass of contextual evidence.
- No remote push, PR, merge, hosted CI, deployment or live operation in this work order.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HIST-001](spec.md#success-criteria--verification-plan), [VAL-HIST-002](spec.md#success-criteria--verification-plan), [VAL-HIST-003](spec.md#success-criteria--verification-plan) | Reproduce both failures; implement the two typed copy boundaries and context-efficient replay; check preserved negatives and actual histories. | User-approved Spec/Plan and exact-byte independent review; AD-0006 and accepted ADR-0056 stay unchanged. | [Task 0001](tasks/tsk-0001-cumulative-lifecycle-history-validation.md) | Focused RED/GREEN regressions, actual local broad explicit-ref/CI, affected QA, independent review. |

## Verification Plan

Run `tests/test_document_lifecycle_cumulative_history.py` with a failing positive case before source edits, then passing positive and negative cases afterward. Test valid `C004` and `C095` ADR heuristic copies, registered first `in-progress` Task and their later forward transitions. Include wrong ID, source changed/deleted, cross-profile source, rename, direct first accepted ADR or terminal Task, invalid edge, missing Task authority/evidence, ordinary Task copy and Spec/Plan receipt failures at both low and high copy scores. Exercise large unrelated corpus under the unchanged 16 MiB budget and a separate bound-exceeded refusal. Compare actual `f6c1c875` → `4033d38e` and `f6c1c875` → `38ec2bea` in local explicit-ref and CI modes; retain the already observed adjacent `4033d38e` → `38ec2bea` PASS as its own fact. Run affected quick and active exact-index staged checks only after approval. Record input, command, exit result, limits and reviewer disposition in the Task.

## Risks & Mitigations

- A broad copy exception could admit a disguised rename or reused identity; require the exact typed unchanged source, absent target, distinct unique canonical IDs and valid first-edge state, with low- and high-score negative fixtures. Similarity alone has no authority.
- Task replay optimization could drop a parent or evidence obligation; compare required contextual results on valid and invalid histories, including cancellation and terminal cases, before accepting a faster path.
- Real history may expose another unrelated diagnostic; retain it as observed evidence and return scope changes to Spec review rather than weakening a guard or claiming an overall PASS.

## Completion Criteria

All three criteria need applicable observed PASS evidence, no unresolved required failures, independent review without a blocking finding, and the operator's criterion acceptance. The actual broad local ranges must pass under unchanged bounds while protected negatives remain rejected. The user's approval of this Spec and Plan authorizes bounded implementation and permits local commits only after the full-history checks pass; it does not accept Task criteria or establish hosted results.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
