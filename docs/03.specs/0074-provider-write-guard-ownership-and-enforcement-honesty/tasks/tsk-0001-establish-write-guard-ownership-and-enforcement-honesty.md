---
title: "Establish Write-Guard Ownership and Enforcement Honesty"
version: "0.7.0"
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
| [WORK-002](../plan.md#work-breakdown) | VAL-PWG-001        | Add the Codex adapter and repoint the Codex registration at it                 | platform | Done | Codex registers its own adapter; no provider directory names the other's path | Three added ownership cases fail before and pass after; guard module 40 passing; staged profile 6/6 PASS |
| [WORK-003](../plan.md#work-breakdown) | VAL-PWG-002        | Parse patch-envelope targets as data into the structured path pipeline         | platform | Done | A patch write now receives the manifest, secret-adjacency and document-route evaluation a structured write receives, in both payload forms | Eleven envelope cases, nine failing before and all passing after; guard module 40 to 51 passing; staged profile PASS |
| [WORK-004](../plan.md#work-breakdown) | VAL-PWG-003        | Correct the enforcement statements and record the open runtime item            | platform | Done | Provider notes now separate registration, documented capability and observation; the discovery question is recorded as unresolved with its procedure and next owner | Reviewed provider text against the recorded client identities; staged profile 6/6 PASS |
| [WORK-005](../plan.md#work-breakdown) | VAL-PWG-004, VAL-PWG-005 | Narrow the Claude read-only scope where a role needs no shell            | platform | Done | Two of six roles narrowed through the existing per-role override; the shared class is unchanged in count and behaviour | Three scope cases failing before and passing after; governance validator PASS; governance module 41 passing |
| [WORK-006](../plan.md#work-breakdown) | VAL-PWG-004        | Correct the two role guardrails and state the class meaning at its owner       | platform | Done | No guardrail in the class offers an action its tool scope cannot perform; the approval policy states the provider asymmetry and the corrected sandbox fact | Repository sweep for the carve-out phrasing returns nothing; staged profile 6/6 PASS |
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

WORK-001 through WORK-006 are complete. The guard logic now lives in one module under
`scripts/` and each provider registers its own thin adapter. The Codex
registration named a file inside the Claude adapter directory; it now names
`.codex/hooks/pre-tool-use.sh`, and a structured payload produces the same
advisory through either adapter.

The Codex adapter README previously stated that no project `hooks/` directory
is adopted. That statement is now false, so it was corrected in the same
change rather than left to contradict the tree.

WORK-003 closed the observed silence. The payload recorded at intake, an
`apply_patch` naming `gitops/test.yaml`, produced no message and exit status
zero; it now produces the same Kubernetes manifest advisory the equivalent
structured write produces, in the string form and the argument-vector form
alike. Because the targets enter the structured path pipeline rather than the
advisory shell list, they also inherit the symbolic-link, repository-root and
retired-path rejections that pipeline already enforced. The envelope body is
never interpreted: a body line resembling a shell redirection contributes no
target.

The shell path is deliberately unchanged and remains advisory. Routing by
payload shape does not disable it, and a payload naming the patch tool while
carrying something else still reaches the shell observer.

WORK-004 replaced the statement that the Codex registration runs the Claude
script, and recorded three things the notes had blended. Whether the installed
Codex client discovers `.codex/hooks.json` is unresolved: the binary's project
path table names `.codex/hooks` while the repository registers
`.codex/hooks.json`, binary strings are indicative rather than conclusive, and
no local subcommand lists loaded hooks. Because delivery is unproven, the
enforced boundary for a non-authoring role on that provider is recorded as the
operating-system sandbox rather than the hook. The observed `PreToolUse`
response contract is recorded per provider, and the guard emits only fields
that client accepts.

The `read-only-evidence` asymmetry is now stated at the Claude provider note
rather than implied: the class withholds structured write tools while leaving a
shell there, and binds an operating-system sandbox on Codex. The difference is
documented and accepted, not presented as parity.

WORK-005 recorded a per-role determination before changing anything. The test
applied was whether a role's required skills instruct running a tool, or its
stated evidence form is a command result.

- `code-reviewer` keeps a shell. Its inputs are changed paths, and reading a
  difference needs a command; the tracked permission allowlist already admits
  the read-only `git diff` forms.
- `gitops-reviewer` keeps a shell. `k8s-validate` instructs running YAML and
  schema validation, kube-linter, GitOps structure checks, and secret-handling
  checks, and the role's required evidence is a repository-backed validation
  result.
- `security-auditor` keeps a shell. Its skills are pattern catalogues rather
  than command procedures, but narrowing the role that owns secret-exposure and
  privilege findings carries more risk than the narrowing removes.
- `network-reviewer` keeps a shell. Its required evidence is a static command
  or a manifest relationship; removing the shell would delete one of the two
  evidence forms its own contract offers.
- `incident-responder` is narrowed. `incident-postmortem` and `rca-methodology`
  are analytical document procedures with no tool instruction, its inputs are
  supplied observations rather than gathered ones, and its guardrail already
  says to remain read-only during analysis.
- `observability-reviewer` is narrowed. Its guardrail restricts it to
  manifest-static review, and neither `ops-runbook` nor `risk-report` instructs
  running a tool for a review.

Narrowing used the registry's existing per-role override, the mechanism
`docs-researcher` already used, so no new registry mechanism appeared and the
three shared permission classes are unchanged in count and behaviour. The Codex
side needed no change: both narrowed roles already bind the operating-system
read-only sandbox there.

One observation is recorded without action. `observability-reviewer` references
`ops-runbook`, whose steps include saving a runbook file and updating a README,
which a read-only role cannot perform. Read as a review standard rather than an
authoring instruction the reference is coherent, so no change is made here; a
decision to split that skill would need its own scope.

WORK-006 removed the two guardrails that offered an edit on request, an action
the class has no structured write tool to perform. A sweep for that phrasing
across the role bodies now returns nothing.

The approval policy gained the class meaning and lost one inaccurate clause. It
had stated that only an operating-system sandbox bounds the advisory class and
that this repository does not enable one; the Codex projections bind
`sandbox_mode` per permission class, so that clause was false and is corrected
rather than left standing. The policy now also records that a patch envelope
reaches the structured evaluation while a shell target is reported and never
blocked.

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
| [WORK-002](../plan.md#work-breakdown) | Codex adapter added and its registration repointed | Three ownership cases red then green; guard module 40 passing; staged profile 6/6 PASS |
| [WORK-003](../plan.md#work-breakdown) | Patch targets reach the structured pipeline in both payload forms | Nine of eleven envelope cases red before, all green after; the reported silent payload now warns |
| [WORK-004](../plan.md#work-breakdown) | Enforcement statements corrected; delivery recorded as unproven | Provider notes dated against `claude 2.1.263` and `codex-cli 0.153.4`; staged profile 6/6 PASS |
| [WORK-005](../plan.md#work-breakdown) | incident-responder and observability-reviewer narrowed; four roles keep a shell with recorded reasons | Determination recorded per role below; scope cases red then green; governance validator PASS |
| [WORK-006](../plan.md#work-breakdown) | Impossible carve-outs removed; class meaning stated at its policy owner | Carve-out sweep returns nothing; approval policy corrected on the sandbox claim; staged profile 6/6 PASS |
| [WORK-007](../plan.md#work-breakdown) | Not started | Queued; four enumerated failure modes named in the plan         |
| [WORK-008](../plan.md#work-breakdown) | Not started | Queued; depends on WORK-007                                     |
| [WORK-009](../plan.md#work-breakdown) | Not started | Queued; deferred items already listed in Verification Summary   |
| [WORK-010](../plan.md#work-breakdown) | Not started | Queued; baseline recorded in Verification Summary               |
