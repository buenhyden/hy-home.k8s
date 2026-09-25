---
title: "Resolve Deferred Conflicts"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0089-TSK-0001"
---

# Task: Resolve Deferred Conflicts

## Overview

Execute [SPEC-0089-PLAN-0001](../plan.md). The request owner asked on
2026-09-25 for the SPEC-0088 deferrals to be resolved and for conflicting open
packages to be withdrawn, cleaned up, or corrected. Push, merge, Stage 98
moves, and live actions are not authorized.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [SPEC-0088 Task](../../0088-operations-corpus-convergence/tasks/tsk-0001-converge-operations-corpus.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DCR-004, VAL-DCR-005 | Survey the deferrals and open packages | platform | Done | Survey below | This Task |
| WORK-002 | VAL-DCR-001, VAL-DCR-002 | Covered gates and English-first scope | platform | Queued | Not executed | Focused tests and staged QA |
| WORK-003 | VAL-DCR-003 | Correct ADR-0031 and AD-0006 | platform | Queued | Not executed | Link gate and staged QA |
| WORK-004 | VAL-DCR-005 | Withdraw SPEC-0049 and update its consumers | platform | Queued | Not executed | Lifecycle and link gates |
| WORK-005 | VAL-DCR-005, VAL-DCR-006 | Cancel SPEC-0049 Tasks, record evidence, and close | platform | Queued | Not executed | Full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-affected-surfaces.py`, `scripts/validation/`, `scripts/README.md`, the tests they own, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`
- **Forbidden Paths**: `gitops/`, `infrastructure/`, `.github/`, `docs/98.archive/`, and the Stage 99 registry
- **Approval Required**: push, pull request, merge, the retirement move of SPEC-0049, and any live action
- **Static Validation**: focused tests, document gates, staged QA per commit, and full QA on the final tree
- **Live Validation**: DEFER; the Headlamp render is a local chart render, not a cluster read
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert each local commit
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-25, `main` at `a008aa67`)

| Item | Finding | Disposition |
| --- | --- | --- |
| Archive gate double run | `unit-tests` discovers the six modules that `archive-contract-tests` runs, and `full` and the `all-files` and `ci` lanes selected both. The coverage invariant required every gate in `full` | Resolve: `coveredBy` declaration and its invariant |
| English-first scope | The rule checked only `spec.md`; its plan and Task globs named the retired Stage 04 tree. The Korean SPEC-0008 plan and Task are `done` | Resolve: check current plans and Tasks, skip terminal states by registry class |
| ADR-0031, AD-0006 | ADR-0031 calls Spec 0054 active and names `.agents/registry.json`; AD-0006 calls TSK-0013 unfinished. Spec 0054 and TSK-0013 are `done` in `completed/`, and the registry is `.agents/roles/registry.json` | Resolve: factual correction |
| RUN-0004 Headlamp objects | `helm template` of the pinned chart `headlamp` `0.41.0` with the repository values renders ClusterRoleBinding `headlamp-admin` to `cluster-admin` and ServiceAccount `headlamp` | Confirmed; no change |
| SPEC-0008 | Spec active as the current platform contract; Plan and Task `done`. No statement contradicts the tree or SPEC-0088 | Keep |
| SPEC-0086 | Draft, operator-only native observation; consistent with its closed predecessor SPEC-0072 and the provider notes | Keep |
| SPEC-0049 | Draft with seven queued Tasks. It waits on Spec 0048, which was withdrawn and retired; plans a Traefik validator whose subject ADR-0043 retired; names a `.agents/contracts/` location the layout does not have; and treats `conftest` as optional though `policy-gates` requires it. Its own 2026-09-24 note says it cannot activate without a new plan | Withdraw; record the unowned gap at REQ-0004 |

The request owner's 2026-09-24 choice to keep SPEC-0049 for a re-plan is
superseded by the 2026-09-25 instruction to withdraw conflicting packages. The
open scope it named (VAL-PVSE-001 to 003 and 005 to 008: render, schema,
policy, secret, shell-fixture, image, and tool-evidence lanes) has no
validator and stays a requirement gap under REQ-0004-FR-0008 and
REQ-0004-FR-0010, for a new package to plan from current authority.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Survey recorded | This Task |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-005](../plan.md#work-breakdown) | Not executed | Pending |
