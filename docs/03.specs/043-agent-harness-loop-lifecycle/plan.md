---
title: 'Agent Harness Loop Lifecycle Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-29
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
- **Task**: [Agent Harness Loop Lifecycle Task](tasks.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) and [AD-0006](../../02.architecture/descriptions/ad-0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisite**: Spec 042 closure `90a7d856` and postflight evidence update
  `023c13df`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AHLL-001](spec.md#success-criteria--verification-plan) | AHLL-000, AHLL-001 | [Activation and retry-ceiling evidence](tasks.md#task-table) |
| N/A — VAL-AHLL-002 through VAL-AHLL-004 share the Spec source above | AHLL-001 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-005 through VAL-AHLL-007 share the Spec source above | AHLL-002 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-008 shares the Spec source above | AHLL-003 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
| N/A — VAL-AHLL-009 shares the Spec source above | AHLL-004 | N/A — the reciprocal Task is linked in VAL-AHLL-001 |
