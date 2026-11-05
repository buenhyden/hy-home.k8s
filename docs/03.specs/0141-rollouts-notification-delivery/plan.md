---
title: "Rollouts Notification Delivery Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0141-PLAN-0001"
parent_ids: ["SPEC-0141"]
---

# Rollouts Notification Delivery Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No secret value is read, printed or committed; no live cluster action.

## Overview

This plan executes [SPEC-0141](spec.md) on branch
`docs/requirements-conformance` after commit `ab5bcd66`.

## Context

[ADR-0054](../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md)
clause 2 assigns Rollouts completion and abort delivery to the Rollouts
controller's notification engine. [AD-0005](../../02.architecture/descriptions/0005-argo-notifications-slack.md)
and [AD-0004](../../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md)
own the views. Rollback is reverting the implementing commit; no migration is
needed.

## Goals & In-Scope

Close VAL-RND-001 to VAL-RND-003 with repository evidence and hand
VAL-RND-004 to the operator.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RND-001](spec.md#success-criteria--verification-plan), [VAL-RND-002](spec.md#success-criteria--verification-plan) | Change the validator assertions first, then the Rollouts values, the ExternalSecret and `argocd-notifications-cm` | None | [Task](tasks/tsk-0001-rollouts-notification-delivery.md) | Validator FAIL on the old manifests, PASS on the new; rendered chart output |
| WORK-002 | [VAL-RND-003](spec.md#success-criteria--verification-plan) | Update REQ-0002, AD-0005, ADR-0012 and the runbook | WORK-001 | [Task](tasks/tsk-0001-rollouts-notification-delivery.md) | Strict document checks |
| WORK-003 | [VAL-RND-004](spec.md#success-criteria--verification-plan) | Operator live observation of a Rollouts message | WORK-001 | [Task](tasks/tsk-0001-rollouts-notification-delivery.md) | Operator record; DEFER until observed |

## Verification Plan

Run `bash scripts/validate-infrastructure-contracts.sh` before and after the
manifest change, render the chart with `helm template`, run the strict
document checks, and run `python3 scripts/qa.py staged` on each commit.

## Risks & Mitigations

- The OpenBao entry may lack `slack_token`; the ExternalSecret then stays not
  ready and nothing is sent. The operator confirms the entry (RUN-0004).
- A chart value key may differ from the documentation; the rendered output is
  checked against the pinned chart 2.40.9.

## Completion Criteria

VAL-RND-001 to VAL-RND-003 have PASS evidence and an operator decision;
VAL-RND-004 has an operator observation or stays open with its owner.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Rollouts events are delivered by the Rollouts notification engine | [ADR-0054](../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md) | Decision, clause 2 |
