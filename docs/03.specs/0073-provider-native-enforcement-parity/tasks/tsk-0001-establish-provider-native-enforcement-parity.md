---
title: "Establish Provider Native Enforcement Parity"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
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

Work has not started. Every row below is queued and every result reads as not
executed until its package runs.

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
| [WORK-001](../plan.md#work-breakdown) | VAL-PNP-001        | Record the decision lineage for the current governance topology                 | platform | Queued | Not executed | Pending lifecycle and link validation                      |
| [WORK-002](../plan.md#work-breakdown) | VAL-PNP-009        | Remove retired-provider and retired-path residue from tracked configuration     | platform | Queued | Not executed | Pending repository quality and filesystem sweep            |
| [WORK-003](../plan.md#work-breakdown) | VAL-PNP-005        | Make the GitHub Actions security validator reachable from a supported profile   | platform | Queued | Not executed | Pending reachability test and profile listing              |
| [WORK-004](../plan.md#work-breakdown) | VAL-PNP-006        | Reduce duplicated rule implementations and profile membership to one owner      | platform | Queued | Not executed | Pending gate comparison and focused tests                  |
| [WORK-005](../plan.md#work-breakdown) | VAL-PNP-007        | Set the commit and handoff evidence proportion in Git policy                    | platform | Queued | Not executed | Pending policy review against the completion sequence      |
| [WORK-006](../plan.md#work-breakdown) | VAL-PNP-003        | Add the per-provider capability-to-model binding to the registry and schema     | platform | Queued | Not executed | Pending binding tests and governance validator             |
| [WORK-007](../plan.md#work-breakdown) | VAL-PNP-002        | Declare a native execution scope for every Codex role and widen the parity rule | platform | Queued | Not executed | Pending scope tests and governance validator               |
| [WORK-008](../plan.md#work-breakdown) | VAL-PNP-003        | Align every Codex role model with the observed client catalog                   | platform | Queued | Not executed | Pending governance validator and recorded catalog identity |
| [WORK-009](../plan.md#work-breakdown) | VAL-PNP-002        | Align every Claude role model and permission mode with the registry binding     | platform | Queued | Not executed | Pending native metadata tests                              |
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
| [WORK-001](../plan.md#work-breakdown) | Not executed; queued behind approval to begin             | Pending lifecycle and link validation on the changed decisions    |
| [WORK-002](../plan.md#work-breakdown) | Not executed; queued                                      | Pending repository quality and document contract validation       |
| [WORK-003](../plan.md#work-breakdown) | Not executed; queued                                      | Pending validation-surface contract test                          |
| [WORK-004](../plan.md#work-breakdown) | Not executed; queued                                      | Pending before-and-after gate comparison                          |
| [WORK-005](../plan.md#work-breakdown) | Not executed; queued                                      | Pending policy review against the completion sequence             |
| [WORK-006](../plan.md#work-breakdown) | Not executed; queued                                      | Pending registry binding tests                                    |
| [WORK-007](../plan.md#work-breakdown) | Not executed; queued                                      | Pending native scope parity tests                                 |
| [WORK-008](../plan.md#work-breakdown) | Not executed; queued                                      | Pending governance validator with recorded catalog identity       |
| [WORK-009](../plan.md#work-breakdown) | Not executed; queued                                      | Pending native metadata tests                                     |
| [WORK-010](../plan.md#work-breakdown) | Not executed; queued                                      | Pending guard unit tests for the shell tool class                 |
| [WORK-011](../plan.md#work-breakdown) | Not executed; queued                                      | Pending provider note review against the recorded client identity |
| [WORK-012](../plan.md#work-breakdown) | Not executed; queued                                      | Pending policy and link validation                                |
| [WORK-013](../plan.md#work-breakdown) | Not executed; queued                                      | Pending path existence sweep and reference pack route test        |
| [WORK-014](../plan.md#work-breakdown) | Not executed; conditional on a native payload observation | Pending observation, otherwise `DEFER` with next owner            |
