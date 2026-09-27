---
title: "Operations Corpus Convergence Implementation Plan"
version: "0.2.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0088-PLAN-0001"
---

# Operations Corpus Convergence Implementation Plan

## Global Constraints

The request owner authorized the audit, the cleanup, and logical local commits
on 2026-09-25. Push, pull request, merge, remote protection, and live systems
are not authorized. No frozen record, sealed ledger, or retained body is
rewritten. Each logical commit runs staged QA over its exact index.

## Overview

This Plan executes [Spec 0088](spec.md) as local commits on the default branch
checkout, ending with full QA on the final tree.

## Context

The Stage 05 tree already uses the `guides/`, `policies/`, `runbooks/`, and
`incidents/` families, so the round converges meaning rather than moving
directories. The audit survey is recorded in the Task.

## Goals & In-Scope

Remove Stage 05 drift and duplicate ownership, align the marker rule with its
validator, dispose of Stage 98 Operations residue where current policy admits
it, and remove dead or duplicate script logic.

## Non-Goals & Out-of-Scope

No manifest, bootstrap, or workflow change; no Stage 98 body edit; no registry
invariant change; no translation of other Spec packages.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Survey Stage 05, Stage 98 Operations units, and scripts, and record the findings | None | Request approval | Task survey |
| WP-002 | Remove dead or duplicate validation logic and prose pins, and close the secret-output detection gap test-first | WP-001 | Survey | Focused tests and staged QA |
| WP-003 | Converge Stage 05 ownership and correct drifted facts | WP-002 | The prose pins no longer force duplication | Document gates and staged QA |
| WP-004 | Record Stage 98 and script dispositions, residual conflicts, and final evidence | WP-002, WP-003 | All commits pass staged QA | Full QA |

## Verification Plan

Each work package runs the focused gates it touches, then
`python3 scripts/qa.py staged`. WP-004 runs `python3 scripts/qa.py full`.
Hosted `ci-summary` is not observed by this Plan.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A removed helper still has a hidden consumer | Search scripts, tests, workflows, hooks, and active documents before removal, then run the owning tests |
| A validator change breaks the provider write guard, which reads the routing contract on every edit | Keep the routing contract valid at every step and run the affected-surface validator after each change |
| A runbook rewrite drops a recovery path | Every removed procedure is replaced by a link to its single remaining owner |

## Completion Criteria

WP-001 to WP-004 meet their exit evidence and the final tree passes full QA.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-OCC-001](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
| [VAL-OCC-002](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
| [VAL-OCC-003](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
| [VAL-OCC-004](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
| [VAL-OCC-005](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
| [VAL-OCC-006](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-converge-operations-corpus.md) |
