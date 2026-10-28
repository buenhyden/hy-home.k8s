---
title: "Release Body Limit Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0137-PLAN-0001"
parent_ids: ["SPEC-0137"]
---

# Release Body Limit Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No release is published by this work.

## Overview

This plan executes [SPEC-0137](spec.md) on branch `fix/release-body-limit`
from `26b0543b`, the SPEC-0136 release-preparation head.

## Context

The PR #191 review found that the `0.1.0` notes exceed GitHub's Release body
limit and that `publish` has no length handling.

## Goals & In-Scope

Close VAL-RB-001 to VAL-RB-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RB-001](spec.md#success-criteria--verification-plan) | Derive a bounded Release body | None | [Task](tasks/tsk-0001-release-body-limit.md) | Failing-then-passing test |
| WORK-002 | [VAL-RB-002](spec.md#success-criteria--verification-plan) | Use the body in publish and describe it in RUN-0012 | WORK-001 | [Task](tasks/tsk-0001-release-body-limit.md) | Release tests and runbook |
| WORK-003 | [VAL-RB-003](spec.md#success-criteria--verification-plan) | Independent review and hosted checks | WORK-002 | [Task](tasks/tsk-0001-release-body-limit.md) | Review and hosted checks |

## Verification Plan

The new test fails on the unchanged tool and passes after the change; the
whole release test module runs after it.

## Risks & Mitigations

- The summary hides the notes. The body links to the full tagged section.
- The limit changes upstream. It is one named constant.

## Completion Criteria

All three criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Release body limit rule | [RUN-0012](../../05.operations/runbooks/0012-main-release-preparation-runbook.md) | Verification |
