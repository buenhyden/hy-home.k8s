---
title: "Close the Stage 03 Backlog"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0084-TSK-0001"
---

# Task: Close the Stage 03 Backlog

## Overview

This Task records the round: the survey each disposition starts from, the two
contract gaps it closes, the edges it takes, the retentions, the repairs those
retentions prove necessary, and the closure. It records observed results only
and never promotes a repository-static result to hosted, provider-runtime, or
live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: on 2026-09-16 the request owner approved this round with blanket
  authorization for individual completion, move, and deletion, and chose the
  registry gap-fills, the frontmatter reader consolidation, and the retention
  moves over the narrower alternatives offered.
- The survey reads the registry's own domain, profile, unit, mode, and class
  definitions, so a candidate here is a candidate the gates recognize.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SBC-001 | Record the survey of every remaining Stage 03 package | platform | Queued | Pending | This Task |
| WORK-002 | VAL-SBC-002 | Close the two registry gaps as gap-fills | platform | Queued | Pending | Registry diff and lifecycle gate |
| WORK-003 | VAL-SBC-003 | Close SPEC-0071, SPEC-0078, SPEC-0062, and SPEC-0054 | platform | Queued | Pending | Lifecycle gate |
| WORK-004 | VAL-SBC-004 | Withdraw SPEC-0048 and SPEC-0051 and cancel their Tasks | platform | Queued | Pending | Lifecycle gate |
| WORK-005 | VAL-SBC-005 | Repair SPEC-0006's stale sibling path and close it | platform | Queued | Pending | Link gate |
| WORK-006 | VAL-SBC-006 | Retain SPEC-0068 and SPEC-0070 in `superseded/` | platform | Queued | Pending | Archive gates |
| WORK-007 | VAL-SBC-007 | Record the dated disposition note of every package that stays | platform | Queued | Pending | This Task and the stage index |
| WORK-008 | VAL-SBC-008 | Resolve the duplicated frontmatter readers to one owner | platform | Queued | Pending | Unit tests and full QA |
| WORK-009 | VAL-SBC-009 | Retain every package that reached `done` in `completed/` | platform | Queued | Pending | Link, lifecycle, and archive gates |
| WORK-010 | VAL-SBC-010 | Repair the consumers the retention proves wrong | platform | Queued | Pending | Full QA and the unit-test suite |
| WORK-011 | VAL-SBC-011 | Close SPEC-0077 with its blocked criteria recorded as deferrals | platform | Queued | Pending | Lifecycle gate and this Task |
| WORK-012 | VAL-SBC-012 | Close this package with its results | platform | Queued | Pending | Staged and full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: the sixteen Stage 03 packages this round disposes of, their
  consumers in documents, in `scripts/` and in `tests/`, the `sdlc/spec` profile
  and the `spec-plan` domain in `docs/99.templates/registry.json`, the Stage 98
  index, the Stage 03 index, `.gitleaks.toml`, and this package.
- **Forbidden Paths**: frozen records, sealed ledgers, and retained bodies under
  `docs/98.archive/`; every registry key, profile, domain, state, and edge other
  than the two named; `gitops/`, `infrastructure/`, `policy/`, `secrets/`,
  `.github/`.
- **Approval Required**: the disposition of each package in this round, granted
  on 2026-09-16. Push, pull request, and merge are not approved.
- **Static Validation**: focused checks per work item, `python3 scripts/qa.py
  staged` per logical commit, and one `python3 scripts/qa.py full` on the final
  tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed. The `.gitleaks.toml` change moves one path-exact
  allowlist entry and reads no secret.
- **Rollback Plan**: Revert the commits before integration; after integration a
  retained unit is frozen and only a forward decision changes it.
- **Evidence Location**: This Task record.

## Verification Summary

Pending. The results of each work item are recorded here as they are observed.

This record, its Spec and its Plan stay in their creation states, `queued` and
`draft`. The lifecycle gate compares a change with its base, where this package
does not yet exist, so a document created in the same change keeps its
zero-indegree state and activation is the next reviewed change.

Every result recorded here is repository-static. No hosted CI run, provider
runtime, live cluster, or network action is claimed by any of them, and push,
pull request, and merge stay with the request owner.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Queued. | This Task. |
| [WORK-002](../plan.md#work-breakdown) | Queued. | Registry diff and lifecycle gate. |
| [WORK-003](../plan.md#work-breakdown) | Queued. | Lifecycle gate. |
| [WORK-004](../plan.md#work-breakdown) | Queued. | Lifecycle gate. |
| [WORK-005](../plan.md#work-breakdown) | Queued. | Link gate. |
| [WORK-006](../plan.md#work-breakdown) | Queued. | Archive gates. |
| [WORK-007](../plan.md#work-breakdown) | Queued. | This Task and the stage index. |
| [WORK-008](../plan.md#work-breakdown) | Queued. | Unit tests and full QA. |
| [WORK-009](../plan.md#work-breakdown) | Queued. | Link, lifecycle, and archive gates. |
| [WORK-010](../plan.md#work-breakdown) | Queued. | Full QA and the unit-test suite. |
| [WORK-011](../plan.md#work-breakdown) | Queued. | Lifecycle gate and this Task. |
| [WORK-012](../plan.md#work-breakdown) | Queued. | Staged and full QA. |
