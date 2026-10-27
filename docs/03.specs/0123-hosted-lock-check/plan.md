---
title: "Hosted CI Lock Check Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0123-PLAN-0001"
parent_ids: ["SPEC-0123"]
---

# Hosted CI Lock Check Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- No change to branch protection, Dependabot configuration, the lock,
  provider settings or credentials.

## Overview

This plan executes [SPEC-0123](spec.md) on branch `ci/hosted-lock-check`
from main `a5b430c0`.

## Context

PR #164 and PR #172 were Dependabot security updates whose regenerated lock
dropped `--only-binary :all:`; commits `7195e74e` and `26b85e56` restored it
after review.

## Goals & In-Scope

Close VAL-HL-001 and VAL-HL-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HL-001](spec.md#success-criteria--verification-plan) | Add the step, the reviewed topology and its tests, and the hosted lane wording | None | [Task](tasks/tsk-0001-hosted-lock-check.md) | Validator tests and a failing candidate lock |
| WORK-002 | [VAL-HL-002](spec.md#success-criteria--verification-plan) | Observe the hosted run and staged QA | WORK-001 | [Task](tasks/tsk-0001-hosted-lock-check.md) | Hosted `style-pr` and staged QA |

## Verification Plan

A failing case first: the old validator on a lock without the directive, run
from a scratch copy, then the new step's command on the same copy.

## Risks & Mitigations

- The step executes candidate code. It runs only `trusted-base` scripts with
  `python -I`, and the validator starts no subprocess.
- The condition never matches. A test pins the step text, and the evidence
  includes a candidate whose requirements path changed.

## Completion Criteria

Both criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Hosted lock check on requirements changes | [Quality policy](../../../.agents/governance/quality.md) | Hosted lane: the `style-pr` lock step |
