---
title: 'Agent Harness Loop Lifecycle Implementation Plan'
version: "1.0"
type: sdlc/plan
layer: "03.specs"
status: done
owner: platform
updated: 2026-07-29
artifact_id: "SPEC-0043-PLAN-0001"
---

# Agent Harness Loop Lifecycle Implementation Plan

## Overview

This Plan executed
[Spec 043](spec.md) after the
repository-static closure of Spec 042. It turns the four memory classes and
provider-neutral evidence boundaries introduced by Specs 041 and 042 into a
bounded loop lifecycle with deterministic retry, termination, checkpoint,
resume, handoff, and durable-memory controls.

Spec 042 closure `90a7d85698cc024e26085ca7caed1b018f78a04e` and
postflight evidence update `023c13dfe4f1643fe29157dde57b5eaae5e495bd`
were observed prerequisites. The exact eight-path activation was committed as
`64e203a4a4ab26239b92a3ee335bce785d938f45`, and its postflight evidence was
recorded by `3b4981ab`. No provider-hook delivery or provider-runtime result is
inferred from that repository-static activation.

## Context

Spec 041 declared `working-short-term`, `durable-long-term`,
`domain-scoped`, and `provider-local-auxiliary` memory, with
`.agent-work/checkpoint.json` as an ignored, advisory recovery carrier and the
repository as the system of record. Spec 042 supplied provider-specific
configuration and evidence boundaries without making provider-local state
authoritative. The executable lifecycle for those declarations was open when
this Plan activated and is closed by the implementation evidence below.

The implementation preserves exact ceilings: at most two automatic
retries after the initial failure for one normalized signature, at most three
automatic recovery actions per task by default, and immediate escalation on
the second identical result with no progress. Permission denial, credential
boundary, secret detection, destructive/live mutation risk, explicit user
stop, and contract/schema corruption are non-retryable.

### Legacy Task ledger inputs

This Task is the durable evidence ledger for the
[Spec 043 Plan](plan.md). It tracks
the reciprocal activation, closed loop lifecycle contract, retry and progress
fixtures, checkpoint/resume behavior, four-class memory lifecycle controls,
routing/provider integration, QA, independent review, atomic closure, and
postflight.

Spec 042 terminal closure `90a7d85698cc024e26085ca7caed1b018f78a04e`
and postflight evidence update
`023c13dfe4f1643fe29157dde57b5eaae5e495bd` are observed prerequisites.
The activation recorded no future activation SHA and did not claim unobserved
checkpoint, provider-hook, provider-runtime, hosted, remote,
credential-bearing, or live results.

- [Agent Harness Loop Lifecycle Implementation Plan](plan.md)
- [Spec 043](spec.md)
- [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- [Harness machine contract](../../00.agent-governance/contracts/harness-contract.json)
- [Memory boundary](../../00.agent-governance/memory/README.md)
- [Provider runtime evidence contract](../../00.agent-governance/contracts/provider-runtime-evidence.json)
- Spec 042 closure `90a7d85698cc024e26085ca7caed1b018f78a04e`
  and postflight `023c13dfe4f1643fe29157dde57b5eaae5e495bd`
## Goals & In-Scope

- Define a closed provider-neutral loop lifecycle contract, schema, state
  machine, failure normalization, progress semantics, and deterministic
  mutation fixtures.
- Enforce the exact signature retry, task recovery, same-result/no-progress,
  and non-retryable termination rules from Spec 043.
- Implement atomic, redacted checkpoint validation and repository-first resume
  that rejects stale task, worktree, base, contract, or ownership claims.
- Implement memory promotion, refresh, expiry, archive/garbage-collection,
  redaction, conflict, compaction, and handoff controls without storing raw
  prompts or transcripts.
- Integrate focused validators into independent affected-surface routing,
  aggregate QA, and provider projections without treating provider hooks as
  cross-provider permission gates.

## Non-Goals & Out-of-Scope

- Provider installation, authentication, account/model resolution, or
  credential-bearing Claude, Codex, Gemini, hosted, remote, or live execution.
- A durable conversation store, full transcript preservation, raw trace
  promotion, or provider-local state becoming repository authority.
- Role/model admission, current `12/4/48` promotion, or eval fitness decisions
  owned by Spec 044.
- Legacy consumer deletion or CI cutover owned by Spec 045, and program
  acceptance owned by Spec 046.
- GitHub settings, Kubernetes, GitOps, Vault, ESO, Argo CD, cloud,
  infrastructure, deployment, or release mutation.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| AHLL-000 | Activate reciprocal Spec 043 Plan/Task lineage | Spec 042 closure and postflight | `90a7d856` and `023c13df` are observed; lifecycle frontier is clean | Exact-eight proposal passes strict document, lifecycle, aggregate, all-files, diff, and independent review gates without preclaiming its commit |
| AHLL-001 | Implement loop lifecycle contract, schema, validator, and deterministic fixtures | AHLL-000 | Active reciprocal Spec/Plan/Task | State machine, normalized failures, progress deltas, two-after-initial signature retries, three task recovery actions, second no-progress stop, and all six non-retryable classes validate |
| AHLL-002 | Implement checkpoint/resume and memory lifecycle controls | AHLL-001 | Loop state and verdict semantics validate | Atomic redacted checkpoint, repository-wins resume, promotion, refresh, expiry, archive/GC, redaction, conflict, compaction, and handoff fixtures pass |
| AHLL-003 | Integrate routing, aggregate QA, and provider projections | AHLL-002 | Focused lifecycle and checkpoint validators pass | Affected paths select one owner; aggregate ordering is deterministic; local/Claude/Codex/Gemini projections preserve common verdicts without runtime promotion |
| AHLL-004 | Run QA/review, close atomically, and record postflight | AHLL-003 | Stable implementation proposal with no unresolved blocking findings | Focused/strict/lifecycle/aggregate/all-files/diff PASS, independent requirements/quality/security approval, exact-eight terminal closure, explicit-ref, and clean-tree postflight |

## Verification Plan

| Lane | Commands or method | Required result |
| --- | --- | --- |
| Loop lifecycle | `python3 scripts/validate-agent-loop-lifecycle.py --root .`; `--self-test` | Closed lifecycle/state/retry/progress/failure contract and mutation fixtures pass |
| Checkpoint and memory | `python3 scripts/validate-agent-checkpoint.py --root . --self-test` | Redaction, atomic-write shape, repository-wins resume, stale rejection, and memory lifecycle controls pass |
| Documents | Strict document registry, Markdown profile, links/owners, and staged/explicit-ref lifecycle checks | Zero route, body-contract, link, owner, or reciprocal-transition findings |
| Routing | Affected-surface self-test and production selection | Contract, checkpoint, provider, governance, script, and test paths select the intended validators exactly once |
| Repository QA | `bash scripts/validate-repo-quality-gates.sh .`; `pre-commit run --all-files`; status and both diff checks | Aggregate final marker, applicable hooks, and clean formatter/diff evidence |
| Independent review | Requirements, quality, and security reviewers inspect the stable proposal | No unresolved Critical or Important finding |
| External evidence | Provider runtime, hosted CI, remote, and live lanes | `DEFER`, `ABSENT`, or `BLOCKED` unless separately authorized and observed |

The focused loop and checkpoint commands are observed AHLL-001/AHLL-002
deliverables and pass with the terminal evidence recorded in the Task.

### Legacy Task verification evidence

The exact-eight activation changed only reciprocal lifecycle records and was
committed as `64e203a4a4ab26239b92a3ee335bce785d938f45`; its explicit-ref,
clean-tree aggregate, all-files, and independent review postflight is recorded
in `memory/progress.md`. AHLL-001 then committed the closed provider-neutral
loop contract and focused validator as
`8a995014d76a92763df420321919e493ec37323e`; its production, 47-case
self-test, and 17 focused unit tests passed independent requirements and
quality/security review. AHLL-002 then committed the closed checkpoint and
four-class memory lifecycle implementation as
`95a6ee03ff2cdff03cb399b4815ba229b5ff27e8`. Its 78-case mutation matrix,
34 combined loop/checkpoint tests, exact helper admission, role-audit
production evidence, applicable pre-commit hooks, and independent requirements
and quality/security reviews passed.

The executable contract retains these exact assertions: no more than two
automatic retries after the initial same-signature failure; no more than three
default automatic recovery actions per task; immediate escalation on the
second identical result with no progress; and no retry for permission denial,
credential boundary, secret detection, destructive/live mutation risk,
explicit user stop, or contract/schema corruption. Repository state and
canonical SDLC owners win every resume or memory conflict. The checkpoint
validator enforces promotion, refresh, expiry, archive/GC, redaction,
compaction, and handoff through tracked synthetic evidence; it does not read or
write the ignored actual checkpoint.

AHLL-000 through AHLL-003 are complete. AHLL-003 committed canonical routing,
aggregate ownership, closed feedback destinations, and bounded provider
projections as
`f0190643e443c28c36e4e54b001589b3a162c903`. Lifecycle `54`-case
self-test, `19` focused tests, `78` checkpoint mutations, affected-surface
selection, strict documents, aggregate, applicable pre-commit, diff, and
independent review passed. AHLL-004 then became the closure frontier completed
by the review remediation and terminal evidence below.

AHLL-004 whole-tranche review then found a loop-to-checkpoint failure-shape
drift, incomplete checkpoint token-family redaction, lifecycle raw-output key
and symlink-input fail-open paths, and a token-family completeness follow-up.
Commit `9d8a2a368849dbab947eff0e9fb066afc6d239a4` closed those findings with one
canonical `failureClass` plus `sha256:<64hex>` interface, synthetic-only
GitHub/Slack/OpenAI/Google token probes, boolean-only policy declaration
exceptions, and regular-file/path-escape guards. Lifecycle `59`, checkpoint
`82`, combined tests `39`, staged lifecycle, strict documents, affected
surfaces, aggregate, all-files, and both diff checks passed. Requirements
returned `COMPLIANT`; quality and security returned `APPROVED` after every
finding was `ADDRESSED`. Evidence update
`4bc3da7621c84048e1aee3b146482f9d7e62bbaa` records the remediation and
review results. The clean implementation/evidence head then passed lifecycle
`668`, whole-tranche explicit-ref, focused, strict, affected, aggregate,
all-files, status, and both diff gates. AHLL-004 is complete with the
exact-eight terminal proposal; its future closure SHA and post-closure
evidence event remain unobserved.

This evidence does not claim provider hook delivery, provider runtime, hosted
CI, remote, credential-bearing, live, or actual `.agent-work/checkpoint.json`
execution.
## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Retry budgets reset through provider or model fallback | Key budgets by task and normalized signature, preserve counters across handoff, and fail closed on incompatible state | platform |
| Repeated wording is mistaken for progress | Accept only deterministic authorized deltas such as intended file state, failing assertion count, satisfied criterion, narrowed reproduction, or approved handoff | quality-engineer |
| Stale checkpoint overwrites newer repository work | Rediscover repository root/status/diff and reject mismatched task, worktree, base, contract, or owner claims; repository state always wins | platform |
| Memory promotion captures sensitive or conversational data | Closed schema, allowlisted fields, redaction, synthetic negative fixtures, and review-gated canonical ownership | security-auditor |
| Expired or duplicate memory persists indefinitely | Require refresh/expiry decisions and reviewed archive/GC dispositions with provenance and canonical-owner conflict checks | platform |
| Native hooks imply cross-provider enforcement | Treat hooks as provider-local delivery mechanisms only; common validators and repository evidence own verdict semantics | platform |
| Rollback damages concurrent work | Commit in dependency order and revert the newest AHLL unit only; never reset, clean, or overwrite unrelated work | platform |

### Legacy Task approval and rollback boundaries

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
## Completion Criteria

- AHLL-000 through AHLL-004 have observed results in the reciprocal Task.
- The loop contract enforces at most two same-signature retries after the
  initial failure, three task recovery actions by default, and the second
  same-result/no-progress stop.
- Permission denial, credential boundary, secret detection, destructive/live
  mutation risk, explicit user stop, and contract/schema corruption stop
  without retry.
- Checkpoints are atomic, bounded, redacted, ignored, replaceable, and
  advisory; repository state wins every resume conflict.
- Promotion, refresh, expiry, archive/GC, redaction, conflict, compaction, and
  handoff controls are closed-schema and fixture tested across all four memory
  classes.
- Focused, affected, strict, lifecycle, aggregate, all-files, formatter, diff,
  and independent-review gates pass before atomic closure.
- Provider runtime, hosted CI, remote, credential-bearing, and live results
  retain their separately observed verdicts and are never inferred from
  repository-static PASS.

AHLL-000 through AHLL-004 are complete through evidence head
`4bc3da7621c84048e1aee3b146482f9d7e62bbaa`. The bounded lifecycle,
checkpoint/four-class memory controls, routing/provider integration, review
remediation, focused `59/82/39`, lifecycle `668`, strict, affected, aggregate,
all-files, diff, and independent-review gates passed. The exact eight-path
terminal proposal closes this Plan without preclaiming its future closure SHA
or post-closure evidence update.

## Traceability

- **Spec**: [Agent Harness Loop Lifecycle](spec.md)
- **Task**: [Agent Harness Loop Lifecycle Task](README.md#task-records)
- **Program**: [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) and [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisite**: Spec 042 closure `90a7d856` and postflight evidence update
  `023c13df`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AHLL-001](spec.md#success-criteria--verification-plan) | AHLL-000, AHLL-001 | [Activation and retry-ceiling evidence](tasks/tsk-0001-ahll-000.md) |
| N/A — VAL-AHLL-002 through VAL-AHLL-004 share the Spec source above | AHLL-001 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-005 through VAL-AHLL-007 share the Spec source above | AHLL-002 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-008 shares the Spec source above | AHLL-003 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-009 shares the Spec source above | AHLL-004 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |

### Legacy Task traceability

- **Plan**: [Agent Harness Loop Lifecycle Implementation Plan](plan.md)
- **Spec**: [Agent Harness Loop Lifecycle](spec.md)
- **Program**: [PRD-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) / [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

#### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AHLL-000](plan.md#work-breakdown) | Done — exact-eight activation and postflight completed. | Activation `64e203a4`; postflight evidence `3b4981ab`; lifecycle, aggregate, all-files, diff, and independent review gates passed. |
| [AHLL-001](spec.md#success-criteria--verification-plan) | Done — loop lifecycle contract and fixtures committed as `8a995014`. | Production and 47-case self-test PASS; 17 focused tests PASS; requirements `COMPLIANT`; quality/security `APPROVED`. |
| N/A — AHLL-002 shares the Plan and Spec sources linked above | Done — checkpoint and four-class memory lifecycle controls committed as `95a6ee03`. | Loop/checkpoint production and self-tests, 34 combined tests, role-audit `53/33/20 · 21/25/6/1`, applicable pre-commit hooks, requirements `COMPLIANT`, and quality/security `APPROVED` after fix re-review passed. |
| N/A — AHLL-003 shares the Plan and Spec sources linked above | Done — routing, feedback ownership, aggregate, and provider projections committed as `f0190643`. | Lifecycle `54` self-test, `19` focused tests, checkpoint `78`, affected-surface `13` selection cases and `16` validators, strict documents, aggregate, applicable pre-commit, diff, `SPEC: COMPLIANT`, and `QUALITY: APPROVED` passed after fix re-review. |
| N/A — AHLL-004 shares the Plan and Spec sources linked above | Done — findings are fixed in `9d8a2a36`, evidence is recorded by `4bc3da76`, and the exact-eight terminal proposal is prepared. | Lifecycle `59`, checkpoint `82`, focused tests `39`, lifecycle `668`, staged/strict/affected/aggregate/all-files/diff PASS; requirements `COMPLIANT`; quality/security `APPROVED`; future closure SHA and postflight are unclaimed. |
