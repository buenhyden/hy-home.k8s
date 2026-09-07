---
title: "Adopt Common Knowledge and Prompt Surfaces"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-07"
layer: "specs"
artifact_id: "SPEC-0075-TSK-0001"
---

# Task: Adopt Common Knowledge and Prompt Surfaces

## Overview

This Task owns execution for [SPEC-0075](../spec.md) through the ordered work
packages in [the plan](../plan.md). It records per-package results, the
evidence lane each result belongs to, the approval boundaries observed, and the
limits that remain unobserved. It is in progress: the packages below record their
actual state, and a row that has not run says so rather than anticipating an
outcome.

WP-001 and WP-002 landed before this record was reconciled, so the earlier
`queued` state understated the tree. That gap is corrected here rather than
backdated: the rows carry the commits that produced them.

## Inputs

- [SPEC-0075](../spec.md) for the change contract and the criteria.
- [Implementation Plan](../plan.md) for ordered packages, entry gates, and exit
  evidence.
- [Work lifecycle](../../../../.agents/workflows/work-lifecycle.md) for intake,
  bounded implementation, and completion.
- [Approval and safety](../../../../.agents/governance/approval-and-safety.md)
  for protected actions.
- [Document authoring](../../../../.agents/governance/document-authoring.md)
  and the Stage 99 registry for profile selection and template routing.
- [Quality policy](../../../../.agents/governance/quality.md) for lane
  meanings, the completion sequence, and the handoff fields.
- Baseline observation: branch `docs/0074-0075-governance-design`, base
  `f5f355f1465dbce217dfbd5ab163b301be879ae7`, twenty-one gates passing under
  `python3 scripts/qa.py full`.
- Upstream observation: `msitarzewski/agency-agents` head
  `1454492577d1af4884722837f491fef14b501e21`, authored 2026-09-05, MIT
  licensed, observed 2026-09-06.

## Task Table

| ID                                    | Upstream criterion | Work item                                                                  | Owner    | Status | Result      | Evidence    |
| ------------------------------------- | ------------------ | -------------------------------------------------------------------------- | -------- | ------ | ----------- | ----------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-CKP-002        | Author the successor decision and mark the prior decision superseded        | platform | Done | ADR-0036 restates ADR-0035's authority-location, skill-routing, gateway, preservation and validation clauses and revises only the unadopted-directory clause; it records the reason each remaining optional directory stays unadopted and why the adopted surface is not the retired generated index. ADR-0035 carries `superseded_by` and a reciprocal successor row with its body intact; both decisions are indexed | Commits `4583e88c`, `22ff2f4d`; strict lifecycle and link validation PASS |
| [WORK-002](../plan.md#work-breakdown) | VAL-CKP-002        | Align the governance README and the context-and-memory routing sentence     | platform | Done | The governance README structure table names both surfaces, the configuration boundary states the adopted position with a per-directory reason for the three that stay unadopted, and the authority-decision link moves to ADR-0036. The context-and-memory routing sentence names the map without granting it authority | Commit `38136bec`; `grep -rn "are not adopted" .agents/ docs/02.architecture/` returns no match; staged profile 6 gates PASS |
| [WORK-003](../plan.md#work-breakdown) | VAL-CKP-003        | Add the knowledge and prompt profiles with templates                        | platform | Queued | Not started | Not started |
| [WORK-004](../plan.md#work-breakdown) | VAL-CKP-001        | Create the knowledge surface and register it in the surface contract        | platform | Queued | Not started | Not started |
| [WORK-005](../plan.md#work-breakdown) | VAL-CKP-004        | Add the knowledge owner-path and non-duplication validator                  | platform | Queued | Not started | Not started |
| [WORK-006](../plan.md#work-breakdown) | VAL-CKP-001        | Wire the knowledge consumers at the navigation skill and the intake step    | platform | Queued | Not started | Not started |
| [WORK-007](../plan.md#work-breakdown) | VAL-CKP-001        | Create the prompt surface with its four contracts                           | platform | Queued | Not started | Not started |
| [WORK-008](../plan.md#work-breakdown) | VAL-CKP-005        | Implement the deterministic prompt input builder                            | platform | Queued | Not started | Not started |
| [WORK-009](../plan.md#work-breakdown) | VAL-CKP-001        | Add the command entry points and retire the VS Code surface                 | platform | Queued | Not started | Not started |
| [WORK-010](../plan.md#work-breakdown) | VAL-CKP-006, VAL-CKP-010 | Consolidate the responsibility documents and carry every consumer      | platform | Queued | Not started | Not started |
| [WORK-011](../plan.md#work-breakdown) | VAL-CKP-007        | Correct the reference pack and add the current dated observation            | platform | Queued | Not started | Not started |
| [WORK-012](../plan.md#work-breakdown) | VAL-CKP-008        | Record the upstream re-observation and the zero-adoption conclusion         | platform | Queued | Not started | Not started |
| [WORK-013](../plan.md#work-breakdown) | VAL-CKP-009        | Give each duplicated rule one execution owner with retention reasons        | platform | Queued | Not started | Not started |
| [WORK-014](../plan.md#work-breakdown) | VAL-CKP-011        | Record the commit-tooling limitation with a user-run remedy                 | platform | Queued | Not started | Not started |

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
repository, including the global hook path and user editor settings;
`git reset --hard`, `git clean`, unapproved stash operations, rebase, amend,
force update, branch deletion, or worktree removal; installation of the
upstream persona catalog or execution of unreviewed external scripts.

The successor decision revises one clause of an accepted decision. That
revision is the authorized scope of this Task; widening it to other clauses,
or adopting a directory the decision keeps unadopted, requires separate
approval.

No entry point this Task creates makes a paid model call mandatory, and no
commit-time hook gains a network dependency.

Two pre-existing stashes target removed authority roots and one would
reintroduce the retired progress ledger. They are left untouched; their
disposition is the user's to make. `_workspace/task-3-trace-fix-report.md` and
the empty `_workspace/repo-support/` directory are pre-existing untracked
residue owned by earlier work and are not removed by this Task.

## Verification Summary

Two work packages have executed. WP-001 produced the successor decision and the
supersession record; WP-002 removed the superseded position from the active
policy text. Each ran the staged profile against its own index snapshot before
its commit, and each reported every gate passing. Neither result is provider,
hosted, or live evidence.

The pre-change baseline is recorded: `python3 scripts/qa.py full` reported
twenty-one gates passing on the working tree containing the two draft
specifications. Any gate that stops passing during implementation is a
regression of the change that preceded it.

One observation is already recorded as a limitation rather than a control: on
this workstation the global `core.hooksPath` points outside the repository, so
the repository's commit-time hooks, including the conventional-commit check, do
not run at commit time. The global configuration is not modified; WP-014
records a repository-local remediation the user runs.

Deferred items, each with its blocker and next owner:

- Whether either client discovers the adopted surfaces or loads a contract.
  Blocker: each requires a fresh authenticated session. Next owner: the user.

No repository-static result in this Task is reported as provider-runtime,
hosted, or live evidence.

## Traceability

[SPEC-0075](../spec.md) owns the criteria and [the plan](../plan.md) owns the
ordered packages and their entry gates. This Task owns results and limits.

### Lifecycle Traceability

| Criterion / work item                 | Result      | Evidence                                                          |
| ------------------------------------- | ----------- | ----------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done        | ADR-0036 accepted, ADR-0035 superseded with a reciprocal row, both indexed |
| [WORK-002](../plan.md#work-breakdown) | Done        | No active file states the superseded position; staged profile PASS        |
| [WORK-003](../plan.md#work-breakdown) | Not started | Queued; profile coverage gap recorded in the plan Context          |
| [WORK-004](../plan.md#work-breakdown) | Not started | Queued; depends on WORK-003                                        |
| [WORK-005](../plan.md#work-breakdown) | Not started | Queued; failing validator cases enumerated in the plan             |
| [WORK-006](../plan.md#work-breakdown) | Not started | Queued; consumer read points named in the plan                     |
| [WORK-007](../plan.md#work-breakdown) | Not started | Queued; four contracts named in the plan                           |
| [WORK-008](../plan.md#work-breakdown) | Not started | Queued; failing builder cases enumerated in the plan               |
| [WORK-009](../plan.md#work-breakdown) | Not started | Queued; identifier collision check precedes any command entry      |
| [WORK-010](../plan.md#work-breakdown) | Not started | Queued; consumers of the seven documents recorded in plan Context  |
| [WORK-011](../plan.md#work-breakdown) | Not started | Queued; pack inaccuracies recorded in plan Context                 |
| [WORK-012](../plan.md#work-breakdown) | Not started | Queued; upstream observation recorded in Inputs                    |
| [WORK-013](../plan.md#work-breakdown) | Not started | Queued; scope coverage proof precedes any hook removal             |
| [WORK-014](../plan.md#work-breakdown) | Not started | Queued; hook path limitation already recorded above                |
