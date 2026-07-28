---
title: 'Task: Agent Harness Loop Lifecycle'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-29
---

# Task: Agent Harness Loop Lifecycle

## Overview

This Task is the durable evidence ledger for the
[Spec 043 Plan](../plans/2026-07-29-agent-harness-loop-lifecycle.md). It tracks
the reciprocal activation, closed loop lifecycle contract, retry and progress
fixtures, checkpoint/resume behavior, four-class memory lifecycle controls,
routing/provider integration, QA, independent review, atomic closure, and
postflight.

Spec 042 terminal closure `90a7d85698cc024e26085ca7caed1b018f78a04e`
and postflight evidence update
`023c13dfe4f1643fe29157dde57b5eaae5e495bd` are observed prerequisites.
This activation records no future activation SHA and no unobserved checkpoint,
provider-hook, provider-runtime, hosted, remote, credential-bearing, or live
result.

## Inputs

- [Agent Harness Loop Lifecycle Implementation Plan](../plans/2026-07-29-agent-harness-loop-lifecycle.md)
- [Spec 043](../../03.specs/043-agent-harness-loop-lifecycle/spec.md)
- [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md)
- [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- [Harness machine contract](../../00.agent-governance/contracts/harness-contract.json)
- [Memory boundary](../../00.agent-governance/memory/README.md)
- [Provider runtime evidence contract](../../00.agent-governance/contracts/provider-runtime-evidence.json)
- Spec 042 closure `90a7d85698cc024e26085ca7caed1b018f78a04e`
  and postflight `023c13dfe4f1643fe29157dde57b5eaae5e495bd`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AHLL-000 | VAL-AHLL-001 through VAL-AHLL-009 | Activate reciprocal Spec/Plan/Task frontier after Spec 042 closure and postflight. | platform | Done | Exact-eight activation committed as `64e203a4`; explicit-ref lifecycle, clean-tree aggregate, all-files pre-commit, and independent review passed. | Activation postflight is recorded in `memory/progress.md` by `3b4981ab`; requirements were `COMPLIANT` and quality/security was `APPROVED`. |
| AHLL-001 | VAL-AHLL-001 through VAL-AHLL-004 | Implement closed loop lifecycle/state/failure/progress contracts, validator, and deterministic fixtures. | platform | Done | Closed contract, schema, focused validator, 47-case self-test fixture, and 17 unit tests committed as `8a995014`. | Production/self-test/unit/diff checks passed; requirements were `COMPLIANT` and quality/security was `APPROVED`. Exact fixtures prove two retries after the initial same-signature failure, three default task recovery actions, lower role/task limits, second identical no-progress stop, and all six non-retryable classes. |
| AHLL-002 | VAL-AHLL-005 through VAL-AHLL-007 | Implement atomic checkpoint validation, repository-wins resume, and four-class memory lifecycle controls. | platform | In Progress | Checkpoint schema, validator, synthetic fixture, and focused tests are being implemented against the AHLL-001 contract. | Redacted fixtures must cover stale task/worktree/base/contract rejection plus promotion, refresh, expiry, archive/GC, redaction, conflict, compaction, and handoff. |
| AHLL-003 | VAL-AHLL-008 | Integrate focused validation routing, repository aggregate, and provider projection semantics. | platform | Queued | Not executed. | Affected surfaces must select one validator owner; provider delivery remains local and cannot promote runtime or override repository verdicts. |
| AHLL-004 | VAL-AHLL-009 | Run focused/strict/lifecycle/aggregate/all-files QA, independent review, atomic closure, and postflight. | platform | Queued | Not executed. | Commands, reviewer verdicts, implementation/closure commits, explicit-ref, clean-tree postflight, rollback, and external limitations will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 043 and reciprocal Plan/Task/index/progress lineage;
  the single Spec 043 registry relation; later Plan-owned loop/checkpoint
  contract and schema, focused validators, synthetic fixtures, tests, routing,
  aggregate, and bounded provider/governance projections.
- **Forbidden Paths**: Credentials, tokens, auth files/caches, account
  identities, environment dumps, shell history, private diagnostics, raw
  prompts/transcripts, provider response bodies, user/home configuration,
  durable conversation storage, provider authentication/run, current
  `12/4/48`, role/model admission, unrelated CI, infrastructure,
  Kubernetes/GitOps, Vault, ESO, Argo CD, cloud, deployment, and release state.
- **Approval Required**: Push, merge, workflow dispatch, provider or GitHub
  settings, dependency installation, publication, networked provider
  execution, credentials, remote/live state, and scope expansion require
  separate explicit human approval.
- **Static Validation**: Focused loop/checkpoint validators; affected-surface
  checks; document lifecycle self-test and staged/explicit-ref modes; strict
  registry, Markdown, links/owners; aggregate; all-files pre-commit; formatter,
  status, and both diff checks.
- **Live Validation**: `DEFER`. Provider discovery/authenticated runs, hosted
  Actions, remote, Kubernetes, Vault, ESO, Argo CD, cloud, deployment, and
  credential results are not authorized or inferred.
- **Secret / Vault Handling**: Do not open, print, copy, hash, store, or report
  secrets, credentials, auth data, raw prompts/transcripts, provider bodies,
  environment dumps, shell history, or private diagnostics. Use synthetic
  redaction markers only in negative fixtures.
- **Rollback Plan**: Revert the newest AHLL logical unit, rerun its focused
  checks and the aggregate, and revert activation last. Never reset, clean,
  rewrite shared history, or overwrite unrelated work.
- **Evidence Location**: This Task owns observed results; the Plan owns
  execution order; Spec 043 owns criteria; the harness contract owns memory
  class declarations; later loop/checkpoint contracts own executable state.

## Verification Summary

The exact-eight activation changed only reciprocal lifecycle records and was
committed as `64e203a4a4ab26239b92a3ee335bce785d938f45`; its explicit-ref,
clean-tree aggregate, all-files, and independent review postflight is recorded
in `memory/progress.md`. AHLL-001 then committed the closed provider-neutral
loop contract and focused validator as
`8a995014d76a92763df420321919e493ec37323e`; its production, 47-case
self-test, and 17 focused unit tests passed independent requirements and
quality/security review. This evidence does not claim that the checkpoint
validator passes, that `.agent-work/checkpoint.json` has been written, that
provider hooks delivered events, or that any provider/runtime/hosted/remote/live
lane passed.

The proposed contract retains these exact future assertions: no more than two
automatic retries after the initial same-signature failure; no more than three
default automatic recovery actions per task; immediate escalation on the
second identical result with no progress; and no retry for permission denial,
credential boundary, secret detection, destructive/live mutation risk,
explicit user stop, or contract/schema corruption. Repository state and
canonical SDLC owners win every resume or memory conflict. Promotion, refresh,
expiry, archive/GC, redaction, compaction, and handoff require deterministic
implementation and fixture evidence before they can be reported as executable.

AHLL-000 and AHLL-001 are complete. AHLL-002 is now the active implementation
frontier; its checkpoint and memory lifecycle evidence must be observed before
AHLL-003 routing and aggregate integration begins.

## Traceability

- **Plan**: [Agent Harness Loop Lifecycle Implementation Plan](../plans/2026-07-29-agent-harness-loop-lifecycle.md)
- **Spec**: [Agent Harness Loop Lifecycle](../../03.specs/043-agent-harness-loop-lifecycle/spec.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) / [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AHLL-000](../plans/2026-07-29-agent-harness-loop-lifecycle.md#work-breakdown) | Done — exact-eight activation and postflight completed. | Activation `64e203a4`; postflight evidence `3b4981ab`; lifecycle, aggregate, all-files, diff, and independent review gates passed. |
| [AHLL-001](../../03.specs/043-agent-harness-loop-lifecycle/spec.md#success-criteria--verification-plan) | Done — loop lifecycle contract and fixtures committed as `8a995014`. | Production and 47-case self-test PASS; 17 focused tests PASS; requirements `COMPLIANT`; quality/security `APPROVED`. |
| N/A — AHLL-002 shares the Plan and Spec sources linked above | In Progress — checkpoint and memory lifecycle controls are being implemented. | Atomic/redacted checkpoint, repository-wins resume, promotion, refresh, expiry, archive/GC, conflict, compaction, and handoff evidence remain required. |
| N/A — AHLL-003 shares the Plan and Spec sources linked above | Queued — routing and provider projections are not integrated. | Focused selection, aggregate ordering, and non-transitive provider evidence remain required. |
| N/A — AHLL-004 shares the Plan and Spec sources linked above | Queued — terminal QA/review/closure is not executed. | Focused/strict/lifecycle/aggregate/all-files/diff, independent review, atomic closure, explicit-ref, and clean-tree postflight remain required. |
