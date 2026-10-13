---
title: "Historical Fixture Drift in Lifecycle Tests Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0111-PLAN-0001"
parent_ids: ["SPEC-0111"]
---

# Historical Fixture Drift in Lifecycle Tests Implementation Plan

## Global Constraints

- Change tests only; no validator, Registry, template or recorded Task.
- Never remove or loosen an assertion.

## Overview

This plan executes [SPEC-0111](spec.md) on branch
`fix/historical-fixture-drift` from main `07ef6b7e`.

## Context

A scratch clone bisected the failures to `2a9daeb7` (acceptance) and
`9067729b` (execution) and confirmed both repairs: 12 acceptance and six
generation tests pass.

## Goals & In-Scope

- Pin the SPEC-0107 package snapshot in the acceptance tests.
- Project the generation 10 Task into the current form and replace the
  retired completion step in the generation tests.

## Non-Goals & Out-of-Scope

Other failing or slow suites, if any, and validator behavior.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FIXTURE-001](spec.md#success-criteria--verification-plan) | Pin the acceptance test package snapshot | None | [Task](tasks/tsk-0001-historical-fixture-drift.md) | Focused tests and staged QA |
| WORK-002 | [VAL-FIXTURE-002](spec.md#success-criteria--verification-plan) | Project the generation Task and replace the retired edge | None | [Task](tasks/tsk-0001-historical-fixture-drift.md) | Focused tests and staged QA |

## Verification Plan

Each work unit records the failing run on main and the passing run after
the change, then `qa.py staged` from the validation environment on the
exact index.

## Risks & Mitigations

- A projection could hide a real defect: it touches one fixture Task only,
  and a malformed result still fails.
- Replacing the completion step could drop coverage: a new assertion keeps
  the retired edge rejected.

## Completion Criteria

Both criteria have PASS evidence and an accepted decision in the Task;
push and pull request remain operator actions.
