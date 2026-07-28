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
| AHLL-000 | VAL-AHLL-001 through VAL-AHLL-009 | Activate reciprocal Spec/Plan/Task frontier after Spec 042 closure and postflight. | platform | In Progress | Exact-eight activation proposal prepared; staged validation, independent review, commit identity, and postflight are not yet observed. | Spec 042 closure/postflight are cited; Spec/Plan/Task, indexes, progress, and only the Spec 043 registry relation comprise the bounded proposal. |
| AHLL-001 | VAL-AHLL-001 through VAL-AHLL-004 | Implement closed loop lifecycle/state/failure/progress contracts, validator, and deterministic fixtures. | platform | Queued | Not executed. | Fixtures must prove two retries after the initial same-signature failure, three default task recovery actions, second identical no-progress stop, and immediate stop for all six non-retryable classes. |
| AHLL-002 | VAL-AHLL-005 through VAL-AHLL-007 | Implement atomic checkpoint validation, repository-wins resume, and four-class memory lifecycle controls. | platform | Queued | Not executed. | Redacted fixtures must cover stale task/worktree/base/contract rejection plus promotion, refresh, expiry, archive/GC, redaction, conflict, compaction, and handoff. |
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

The exact-eight activation proposal changes only reciprocal lifecycle records.
It does not claim that the planned loop lifecycle or checkpoint validators
exist, that `.agent-work/checkpoint.json` has been written, that provider hooks
delivered events, or that any provider/runtime/hosted/remote/live lane passed.

The proposed contract retains these exact future assertions: no more than two
automatic retries after the initial same-signature failure; no more than three
default automatic recovery actions per task; immediate escalation on the
second identical result with no progress; and no retry for permission denial,
credential boundary, secret detection, destructive/live mutation risk,
explicit user stop, or contract/schema corruption. Repository state and
canonical SDLC owners win every resume or memory conflict. Promotion, refresh,
expiry, archive/GC, redaction, compaction, and handoff require deterministic
implementation and fixture evidence before they can be reported as executable.

AHLL-000 remains in progress until the exact staged proposal passes its
declared repository-static gates and independent review. Its future commit
identity, explicit-ref lifecycle interval, and clean-tree postflight must be
recorded only after observation.

## Traceability

- **Plan**: [Agent Harness Loop Lifecycle Implementation Plan](../plans/2026-07-29-agent-harness-loop-lifecycle.md)
- **Spec**: [Agent Harness Loop Lifecycle](../../03.specs/043-agent-harness-loop-lifecycle/spec.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) / [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AHLL-000](../plans/2026-07-29-agent-harness-loop-lifecycle.md#work-breakdown) | In Progress — exact-eight activation proposal is prepared but not yet validated or committed. | Spec 042 closure/postflight are observed; staged gates, reviewer verdicts, activation commit, and postflight remain required. |
| [AHLL-001](../../03.specs/043-agent-harness-loop-lifecycle/spec.md#success-criteria--verification-plan) | Queued — loop lifecycle contract and fixtures are not implemented. | Exact retry, recovery, no-progress, non-retryable, state, failure, and progress assertions remain required. |
| N/A — AHLL-002 shares the Plan and Spec sources linked above | Queued — checkpoint and memory lifecycle controls are not implemented. | Atomic/redacted checkpoint, repository-wins resume, promotion, refresh, expiry, archive/GC, conflict, compaction, and handoff evidence remain required. |
| N/A — AHLL-003 shares the Plan and Spec sources linked above | Queued — routing and provider projections are not integrated. | Focused selection, aggregate ordering, and non-transitive provider evidence remain required. |
| N/A — AHLL-004 shares the Plan and Spec sources linked above | Queued — terminal QA/review/closure is not executed. | Focused/strict/lifecycle/aggregate/all-files/diff, independent review, atomic closure, explicit-ref, and clean-tree postflight remain required. |
