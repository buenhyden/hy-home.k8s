---
title: "Stage 03 Terminal Package Retention Implementation Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0087-PLAN-0001"
---

# Stage 03 Terminal Package Retention Implementation Plan (Plan)

## Global Constraints

The request owner approved this round on 2026-09-24 ("Approve archive, separate
package"). No frozen record, sealed ledger, or retained body is rewritten, and no
registry, profile, state, or edge changes. Each logical commit runs staged QA
over its exact index. Pull requests merge only after the hosted `qa` check
passes.

## Overview

This Plan executes [Spec 0087](spec.md) in two integrations. Each one names a
commit that the default branch already holds as its Retention Envelope.

## Context

[SPEC-0084](../../98.archive/completed/03.specs/0084-stage03-backlog-closeout/spec.md) retained seven units and
left these seven for a separate decision. The request owner made that decision
on 2026-09-24, after SPEC-0047 and SPEC-0050 were withdrawn the same day.

## Goals & In-Scope

Retain the four withdrawn packages in `retired/` and the three done packages in
`completed/`, with every current consumer moved in the same commit, and record
the evidence.

## Non-Goals & Out-of-Scope

No other package, no registry change, no rewrite of a retained body, and no
lowered gate, test pin, or allowlist.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the approval and the survey | None | The request owner approved the round | The Task records each unit, its anchor state, and its consumers |
| WP-002 | Retain SPEC-0047, SPEC-0048, SPEC-0050, and SPEC-0051 in `retired/`, rewriting their current citations | WP-001 | Every member is terminal and the envelope commit is on the default branch | Lifecycle, link, and archive gates |
| WP-003 | Rewrite the SPEC-0054 test pin and move the SPEC-0062 allowlist entry with its test | WP-002 merged | The retained paths are known | Unit tests and the secret-scan gate |
| WP-004 | Retain SPEC-0054, SPEC-0062, and SPEC-0084 in `completed/`, repointing their current citations | WP-003 | The envelope commit is on the default branch | Lifecycle, link, and archive gates |
| WP-005 | Record the results and close this package | WP-001 to WP-004 | Hosted `qa` passes | Staged QA and hosted CI |

## Verification Plan

Each work package runs the lifecycle, link, and archive gates it touches, then
`python3 scripts/qa.py staged` on its exact index. The hosted `qa` check on each
pull request runs the full profile.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A move names a commit the default branch does not hold | Each integration starts from the merged default branch and names its tip |
| A current document keeps a link to a retired unit | The link gate runs over the whole corpus in the move commit |
| Rewriting the SPEC-0054 pin weakens it | The pin keeps its assertion and only its path changes |
| Moving the SPEC-0062 allowlist entry widens the secret scan's exemption | The entry keeps its exact anchored form and only its path changes |

## Completion Criteria

WP-001 to WP-005 pass their exit evidence, every retained unit equals its
envelope object, and the final tree passes staged QA and hosted `qa`.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-STR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
| [VAL-STR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
| [VAL-STR-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
| [VAL-STR-004](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
| [VAL-STR-005](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
| [VAL-STR-006](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-retain-terminal-stage-03-packages.md) |
