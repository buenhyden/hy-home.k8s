---
title: "Establish Provider Native Enforcement Parity"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-06"
layer: "specs"
artifact_id: "SPEC-0073-TSK-0001"
---

# Task: Establish Provider Native Enforcement Parity

## Overview

Execute SPEC-0073-PLAN-0001 as fourteen ordered work packages, each delivered
as one logical commit gated by its exact index snapshot, with the full profile
run once on the final tree before handoff. This record owns execution results,
per-lane evidence, and the limits that remain unobserved.

Execution is under way. WORK-006 delivered the model alignment that WORK-008
and WORK-009 had planned separately, because a binding validator cannot land
before the values it validates; WORK-009 now carries only the permission mode.

## Inputs

- [SPEC-0073](../spec.md)
- [SPEC-0073-PLAN-0001](../plan.md)
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md)
- [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [ADR-0035](../../../02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md)
- [SPEC-0072](../../0072-agent-governance-and-quality-gate-consolidation/spec.md)
- Baseline commit `a57887cbf8d34eed248cb33438073635380966e3` on branch
  `codex/governance-follow-up`; local `main` and `origin/main` both at
  `4053793a41a9cedff1edeaa4a9d3b2a6a80e1272`
- Client identity observed 2026-09-06: `claude 2.1.261`, `codex-cli 0.140.0`,
  `python 3.12.3`, `pre-commit 4.5.1`

## Task Table

| ID                                    | Upstream criterion | Work item                                                                       | Owner    | Status | Result       | Evidence                                                   |
| ------------------------------------- | ------------------ | ------------------------------------------------------------------------------- | -------- | ------ | ------------ | ---------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | VAL-PNP-001 | Record the decision lineage for the current governance topology | platform | Done | ADR-0034 superseded with a reciprocal successor row; ADR-0035 accepted; the index, AD-0006 and REQ-0003 name the current owner | Commit `7bfbf1dd`; staged profile, six gates |
| [WORK-002](../plan.md#work-breakdown) | VAL-PNP-009 | Remove retired-provider and retired-path residue from tracked configuration | platform | Done | Dead pre-commit exclusion, two removed-provider globs, one deleted-test index row and one contradicted stage claim removed | Commit `ce0adb53`; staged profile, six gates |
| [WORK-003](../plan.md#work-breakdown) | VAL-PNP-005 | Make the GitHub Actions security validator reachable from a supported profile | platform | Done | Gate registered on the all-files and CI lanes; its first run found a one-day artifact retention against the seven-day contract | Commit `1f6420ee`; reachability test RED then GREEN |
| [WORK-004](../plan.md#work-breakdown) | VAL-PNP-006 | Reduce duplicated rule implementations and profile membership to one owner | platform | Done | Duplicate Vault and ESO heredoc removed, 441 to 306 lines, both gates still passing; two reported duplications kept as distinct rules | Commit `41648686`; staged profile, seven gates |
| [WORK-005](../plan.md#work-breakdown) | VAL-PNP-007 | Set the commit and handoff evidence proportion in Git policy | platform | Done | The staged profile gates a logical commit; the full profile gates branch finish and handoff | Commit `43711f02`; staged profile, six gates |
| [WORK-006](../plan.md#work-breakdown) | VAL-PNP-003 | Add the per-provider capability-to-model binding to the registry and schema | platform | Done | Binding declared for both providers; twenty-three of twenty-four projections realigned; drift now fails on both sides | Binding tests RED then GREEN; governance validator |
| [WORK-007](../plan.md#work-breakdown) | VAL-PNP-002        | Declare a native execution scope for every Codex role and widen the parity rule | platform | Queued | Not executed | Pending scope tests and governance validator               |
| [WORK-008](../plan.md#work-breakdown) | VAL-PNP-003 | Align every Codex role model with the observed client catalog | platform | Done | Delivered inside WORK-006; the installed client catalog listed only `gpt-5.5`, `gpt-5.4-mini` and `gpt-5.3-codex-spark`, so eleven of twelve prior values named absent models | Governance validator; catalog observed 2026-09-06 |
| [WORK-009](../plan.md#work-breakdown) | VAL-PNP-002 | Align every Claude role model and permission mode with the registry binding | platform | In progress | Models delivered inside WORK-006 as documented aliases; the permission mode remains | Native metadata tests |
| [WORK-010](../plan.md#work-breakdown) | VAL-PNP-004        | Extend the pre-action guard to the shell tool class and name the residual class | platform | Queued | Not executed | Pending guard unit tests and approval-boundary review      |
| [WORK-011](../plan.md#work-breakdown) | VAL-PNP-008        | Correct provider notes to describe native capability against a named client     | platform | Queued | Not executed | Pending provider note review                               |
| [WORK-012](../plan.md#work-breakdown) | VAL-PNP-007        | Add the untrusted input, cost and throughput, and loop termination boundaries   | platform | Queued | Not executed | Pending policy review and link validation                  |
| [WORK-013](../plan.md#work-breakdown) | VAL-PNP-010        | Reconcile Stage 90 research baseline rows with the current tree                 | platform | Queued | Not executed | Pending path sweep and reference pack route test           |
| [WORK-014](../plan.md#work-breakdown) | VAL-PNP-004        | Mirror the pre-action guard as a Codex native hook after observing the payload  | platform | Queued | Not executed | Pending native observation, otherwise `DEFER`              |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/`, `.agents/roles/registry.json`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.agents/roles/registry.schema.json`, `.claude/agents/`,
  `.claude/settings.json`, `.claude/hooks/`, `.claude/provider.md`,
  `.claude/README.md`, `.codex/agents/`, `.codex/provider.md`,
  `.codex/README.md`, `.codex/hooks.json`, `.github/labeler.yml`,
  `.pre-commit-config.yaml`, `README.md`, `docs/02.architecture/decisions/`,
  `docs/03.specs/0073-provider-native-enforcement-parity/`,
  `docs/03.specs/README.md`, `docs/90.references/research/`,
  `docs/99.templates/registry.json`, `docs/99.templates/templates/runtime/`,
  `scripts/validate-agent-governance.py`, `scripts/validation/registry.json`,
  `infrastructure/tests/verify-contracts-static.sh`, `tests/`
- **Forbidden Paths**: the user's staged index and every path it touches,
  `.claude/settings.local.json`, `.claude/*.local.md`, `_workspace/` contents,
  `policy/`, `gitops/`, `infrastructure/` outside the named contract script,
  `secrets/`, sealed record bodies under `docs/98.archive/`
- **Approval Required**: commit authorization per logical package; separate
  authorization for push, pull-request creation, merge, branch cleanup, and any
  hosted or provider-authenticated execution
- **Static Validation**: `python3 -m unittest` for the focused modules,
  `python3 scripts/validate-agent-governance.py --root .`,
  `python3 scripts/qa.py staged` per package, `python3 scripts/qa.py full` once
  before handoff, `git diff --check` and `git diff --cached --check`
- **Live Validation**: `DEFER` — no cluster, Argo CD, Vault, cloud, remote Git,
  or hosted CI operation is authorized by this Task
- **Secret / Vault Handling**: no credential, token, authentication file,
  environment dump, plaintext secret, shell history, or provider transcript is
  read, printed, or recorded; validator failure messages name paths and
  expected values only
- **Rollback Plan**: `git revert` of the owning package commit; a corrective
  change is a new forward commit, never a history rewrite
- **Evidence Location**: this record

## Verification Summary

No package has run. No repository-static, provider-runtime, hosted-CI, or live
result exists for this Task yet.

Baseline observations recorded before work started, which are inputs rather
than results:

- `python3 scripts/validate-agent-governance.py --root .` passed on the
  pre-change tree with two providers, twelve roles, three permission classes,
  sixteen skills, thirty-four handoffs, and thirty-six projections.
- `python3 scripts/qa.py quick` passed on the pre-change tree, selecting eleven
  gates over fifty-eight changed paths in three minutes forty-five seconds.
- `python3 scripts/qa.py --list` reported four profiles, with the quick and
  staged member lists identical and the full and CI member lists identical.

Lanes that will remain `DEFER` unless a separate authorized observation is
made: native discovery, native enforcement, model resolution, authenticated
provider operation, hosted CI execution, live infrastructure behavior, and any
editor-extension behavior, since no provider editor extension is installed.

Residual risk before work starts: the governance validator pins several native
and settings shapes exactly, so each widened rule must add its failing case
first or a real regression can pass silently.

## Traceability

### Lifecycle Traceability

| Criterion / work item                 | Result                                                    | Evidence                                                          |
| ------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Recorded the decision lineage without rewriting either decision body | Commit `7bfbf1dd`; document lifecycle and link validation |
| [WORK-002](../plan.md#work-breakdown) | Removed five tracked entries that could never match or hold true | Commit `ce0adb53`; repository quality and filesystem sweep |
| [WORK-003](../plan.md#work-breakdown) | Registered the orphan gate and fixed the violation its first run found | Commit `1f6420ee`; reachability test and profile listing |
| [WORK-004](../plan.md#work-breakdown) | Removed one duplicate implementation; kept three distinct rules | Commit `41648686`; both gates re-run after removal |
| [WORK-005](../plan.md#work-breakdown) | Stated the commit and handoff evidence proportion | Commit `43711f02`; quality policy cross-reference |
| [WORK-006](../plan.md#work-breakdown) | Capability tier now determines the native model on both providers | Binding tests and governance validator negative cases |
| [WORK-007](../plan.md#work-breakdown) | Not executed; queued                                      | Pending native scope parity tests                                 |
| [WORK-008](../plan.md#work-breakdown) | Codex models realigned to the observed client catalog | Governance validator; recorded catalog identity |
| [WORK-009](../plan.md#work-breakdown) | Claude models realigned to documented aliases; permission mode pending | Native metadata tests |
| [WORK-010](../plan.md#work-breakdown) | Not executed; queued                                      | Pending guard unit tests for the shell tool class                 |
| [WORK-011](../plan.md#work-breakdown) | Not executed; queued                                      | Pending provider note review against the recorded client identity |
| [WORK-012](../plan.md#work-breakdown) | Not executed; queued                                      | Pending policy and link validation                                |
| [WORK-013](../plan.md#work-breakdown) | Not executed; queued                                      | Pending path existence sweep and reference pack route test        |
| [WORK-014](../plan.md#work-breakdown) | Not executed; conditional on a native payload observation | Pending observation, otherwise `DEFER` with next owner            |
