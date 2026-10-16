---
title: "Local QA Rightsizing Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0117-PLAN-0001"
parent_ids: ["SPEC-0117"]
---

# Local QA Rightsizing Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to `.github/workflows/**`, remote settings or credentials.

## Overview

This plan executes [SPEC-0117](spec.md) on branch
`qa/spec-0117-local-qa-rightsizing` from main `f062294c`.

## Context

The operator-requested audit of 2026-10-16 found the phase-one items listed in
the Spec. A test timing run on `main` then showed three failing modules that no
selected lane executes.

## Goals & In-Scope

Close VAL-QR-001 to VAL-QR-005.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-QR-001](spec.md#success-criteria--verification-plan) | Repair the three failing test modules at their root cause | None | [Task](tasks/tsk-0001-local-qa-rightsizing.md) | Focused tests, staged QA |
| WORK-002 | [VAL-QR-002](spec.md#success-criteria--verification-plan) | Replace copied pins in the CI Python contract with consistency checks | None | [Task](tasks/tsk-0001-local-qa-rightsizing.md) | Focused tests, staged QA |
| WORK-003 | [VAL-QR-003](spec.md#success-criteria--verification-plan) | Remove chart version arguments from the ingress validator | None | [Task](tasks/tsk-0001-local-qa-rightsizing.md) | Focused tests, staged QA |
| WORK-004 | [VAL-QR-004](spec.md#success-criteria--verification-plan) | Remove prose lists, retired denylists, CODEOWNERS requirement, dead surfaces and unused lanes | None | [Task](tasks/tsk-0001-local-qa-rightsizing.md) | Focused tests, staged QA |
| WORK-005 | [VAL-QR-005](spec.md#success-criteria--verification-plan) | Add `independent-review` to delivery procedures; correct the README `.github/` line | None | [Task](tasks/tsk-0001-local-qa-rightsizing.md) | Document checks, independent review |

## Verification Plan

Each work unit runs its focused test modules and `qa.py staged` on the exact
index. The branch receives one independent read-only review before its PR.

## Risks & Mitigations

- A removed assertion hid a real regression: each removal names the owner that
  still holds the protection; without one the item is deferred.
- Parallel edits collide: work units touch disjoint files.

## Completion Criteria

All five criteria have PASS evidence and an accepted decision in the Task;
push, pull request and merge follow the operator's request and RUN-0013.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
