---
title: "Establish Write-Guard Ownership and Enforcement Honesty"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0074-TSK-0001"
---

# Task: Establish Write-Guard Ownership and Enforcement Honesty

## Overview

This Task owns execution for [SPEC-0074](../spec.md) through the ordered work
packages in [the plan](../plan.md). It records per-package results, the
evidence lane each result belongs to, the approval boundaries observed, and the
limits that remain unobserved. It is queued: no work package has started, and
every result column below records that state rather than an anticipated
outcome.

## Inputs

- [SPEC-0074](../spec.md) for the change contract and the criteria.
- [Implementation Plan](../plan.md) for ordered packages, entry gates, and exit
  evidence.
- [Work lifecycle](../../../../.agents/workflows/work-lifecycle.md) for intake,
  bounded implementation, and completion.
- [Approval and safety](../../../../.agents/governance/approval-and-safety.md)
  for protected actions.
- [Quality policy](../../../../.agents/governance/quality.md) for lane
  meanings, the completion sequence, and the handoff fields.
- Baseline observation: branch `docs/0074-0075-governance-design`, base
  `f5f355f1465dbce217dfbd5ab163b301be879ae7`, twenty-one gates passing under
  `python3 scripts/qa.py full`.
- Observed client identities: `claude 2.1.263` and `codex-cli 0.153.4` on
  Ubuntu 24.04 under WSL2, observed 2026-09-06.

## Task Table

| ID                                    | Upstream criterion | Work item                                                                     | Owner    | Status | Result      | Evidence    |
| ------------------------------------- | ------------------ | ----------------------------------------------------------------------------- | -------- | ------ | ----------- | ----------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-PWG-001        | Extract the guard program to `scripts/` and reduce the Claude hook to an adapter | platform | Done | Guard logic owns one module; the Claude adapter resolves it from its own checkout rather than the tool-supplied project directory | Guard unit module 35 passing before, 37 passing after with two added trust-boundary cases; four probe payloads unchanged; staged profile 11/11 PASS |
| [WORK-002](../plan.md#work-breakdown) | VAL-PWG-001        | Add the Codex adapter and repoint the Codex registration at it                 | platform | Queued | Not started | Not started |
| [WORK-003](../plan.md#work-breakdown) | VAL-PWG-002        | Parse patch-envelope targets as data into the structured path pipeline         | platform | Queued | Not started | Not started |
| [WORK-004](../plan.md#work-breakdown) | VAL-PWG-003        | Correct the enforcement statements and record the open runtime item            | platform | Queued | Not started | Not started |
| [WORK-005](../plan.md#work-breakdown) | VAL-PWG-004, VAL-PWG-005 | Narrow the Claude read-only scope where a role needs no shell            | platform | Queued | Not started | Not started |
| [WORK-006](../plan.md#work-breakdown) | VAL-PWG-004        | Correct the two role guardrails and state the class meaning at its owner       | platform | Queued | Not started | Not started |
| [WORK-007](../plan.md#work-breakdown) | VAL-PWG-006        | Add one evaluation artifact per enumerated failure mode                        | platform | Queued | Not started | Not started |
| [WORK-008](../plan.md#work-breakdown) | VAL-PWG-006        | Anchor groundedness to content and add the unverified-success criterion        | platform | Queued | Not started | Not started |
| [WORK-009](../plan.md#work-breakdown) | VAL-PWG-007        | Record evidence-class separation, deferred items, blockers, and next owners    | platform | Queued | Not started | Not started |
| [WORK-010](../plan.md#work-breakdown) | VAL-PWG-008        | Review the final diff scope, run the full profile, and record the boundaries   | platform | Queued | Not started | Not started |

## Approval and Safety Boundaries

Authorized for this Task: reading repository files and official public
documentation; local edits within the paths the specification authorizes;
non-destructive local validation; a task-owned branch; and reviewed logical
local commits.

Not authorized and not performed: push, pull-request creation, merge, release,
remote workflow dispatch, or branch-protection change; any live Kubernetes,
ArgoCD, Vault, or cloud operation; reading or storing credentials, tokens,
private keys, kubeconfig, plaintext secrets, shell history, environment dumps,
or raw session records; modification of user configuration outside the
repository, including the global hook path; `git reset --hard`, `git clean`,
unapproved stash operations, rebase, amend, force update, branch deletion, or
worktree removal; and running unreviewed external installation scripts.

A model capability tier grants no additional permission. A passing check is not
permission to publish. Any decision that would widen this scope or weaken a
control is escalated to the user rather than taken.

Two pre-existing stashes target removed authority roots and one would
reintroduce the retired progress ledger. They are left untouched; their
disposition is the user's to make.

## Verification Summary

WORK-001 is complete. The guard logic now lives in one module under
`scripts/` and the Claude adapter names its provider and forwards the payload.

Two findings arose during extraction and are recorded rather than smoothed
over. First, resolving the guard program through the project directory made the
guarded tree able to supply the guard, which two existing rejection cases
caught immediately; the adapter now resolves the module from its own checkout
and forwards the project directory as data, which is a stronger trust anchor
than the arrangement it replaces. Second, four structural assertions and one
repository-quality rule named the shell file as the implementation; their
subject moved to the module, so each was retargeted at the module rather than
relaxed, and two new assertions were added for the contracts the split created.


The pre-change baseline is recorded: `python3 scripts/qa.py full` reported
twenty-one gates passing on the working tree containing the two draft
specifications, and `python3 scripts/qa.py staged` reported six gates passing
over the exact index of the specification commit. Any gate that stops passing
during implementation is a regression of the change that preceded it.

Deferred items, each with its blocker and next owner:

- Whether `codex-cli 0.153.4` discovers `.codex/hooks.json`. Blocker: the
  client exposes no local command listing loaded hooks, so the question needs
  a fresh session. Next owner: the user, at a Codex session.
- Native discovery, permission enforcement, model resolution, and hook
  delivery on either provider. Blocker: each requires a fresh authenticated
  session and may incur cost. Next owner: the user.

No repository-static result in this Task is reported as provider-runtime,
hosted, or live evidence.

## Traceability

[SPEC-0074](../spec.md) owns the criteria and [the plan](../plan.md) owns the
ordered packages and their entry gates. This Task owns results and limits.

### Lifecycle Traceability

| Criterion / work item                 | Result      | Evidence                                                       |
| ------------------------------------- | ----------- | -------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Guard extracted without behaviour change; adapter trust anchor corrected | Guard unit module 35 to 37 passing; probe payloads unchanged; staged profile 11/11 PASS |
| [WORK-002](../plan.md#work-breakdown) | Not started | Queued; depends on WORK-001                                     |
| [WORK-003](../plan.md#work-breakdown) | Not started | Queued; failing envelope case recorded in the plan              |
| [WORK-004](../plan.md#work-breakdown) | Not started | Queued; client identities recorded in Inputs                    |
| [WORK-005](../plan.md#work-breakdown) | Not started | Queued; per-role shell determination precedes any change        |
| [WORK-006](../plan.md#work-breakdown) | Not started | Queued; depends on WORK-005                                     |
| [WORK-007](../plan.md#work-breakdown) | Not started | Queued; four enumerated failure modes named in the plan         |
| [WORK-008](../plan.md#work-breakdown) | Not started | Queued; depends on WORK-007                                     |
| [WORK-009](../plan.md#work-breakdown) | Not started | Queued; deferred items already listed in Verification Summary   |
| [WORK-010](../plan.md#work-breakdown) | Not started | Queued; baseline recorded in Verification Summary               |
