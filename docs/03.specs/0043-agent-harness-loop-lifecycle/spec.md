---
title: 'Agent Harness Loop Lifecycle Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-01
artifact_id: "SPEC-0043"
---

# Agent Harness Loop Lifecycle Specification

## Overview

This specification defines a bounded, observable, and recoverable execution
loop shared by local/Antigravity, Claude, Codex, and Gemini projections. It
turns repeated failures into deterministic stop/escalation or evaluation input
instead of open-ended retries. The fixed external-source observation cutoff is
**2026-07-10 10:00 Asia/Seoul** (`2026-07-10T01:00:00Z`).

The design follows the repository-as-system-of-record and mechanical-feedback
principles in [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
and the trace-to-eval feedback pattern in the
[Agent Improvement Loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop).

## Strategic Boundaries & Non-goals

- **Owns**: failure normalization, retry budgets, progress detection,
  checkpoint schema, compaction/resume, handoff, escalation, and deterministic
  loop fixtures.
- **Depends on**: Spec 042 provider metadata and comparable runtime evidence.
- **Feeds**: Spec 044 role evals and model-fitness decisions.
- **Does not own**: provider authentication, model admission, CI topology,
  task-specific business logic, or a durable conversation store.
- **Non-goals**: guaranteeing completion through retries, preserving full
  transcripts, hiding failures with fallback, or granting tools beyond the
  parent task.

## Contracts

### Retry and termination limits

- The same normalized failure signature may receive at most **2 automatic
  retries** after its initial failed attempt.
- A task receives at most **3 automatic recovery actions by default** across
  all signatures. A lower role/task limit wins; increasing the default needs
  an approved contract change.
- If the same normalized result occurs twice with no progress delta, the loop
  stops and escalates immediately even when budget remains.
- Permission denial, credential boundary, secret detection, destructive/live
  mutation risk, explicit user stop, or contract/schema corruption are
  non-retryable.

### Progress contract

Progress is a deterministic delta in at least one authorized dimension:
changed intended file state, fewer failing assertions, a newly satisfied
criterion, a narrowed reproducible failure, or an approved handoff artifact.
More tokens, repeated commands, changed wording, or an unverified fallback are
not progress.

### Checkpoint contract

The provider-neutral transient checkpoint is `.agent-work/checkpoint.json`.
It is ignored, local, replaceable, and advisory. It contains only task ID,
contract version, role/provider, attempt/recovery counters, normalized failure
class/signature digest, completed and remaining work, bounded validation
summary, next action, stop/handoff state, and repository base/working-state
identifiers.

It must not contain credentials, tokens, account identifiers, auth file paths
or contents, environment dumps, shell history, full/raw prompts or transcripts,
secret-bearing command output, or ignored private diagnostics.

## Core Design

### State machine

`ready -> running -> validating -> completed` is the success path.
Recoverable failure moves `validating -> retry-assessment -> running` only when
the signature and task budgets allow it and the proposed action differs from
the failed action. Other outcomes move to `blocked`, `escalated`, or `aborted`.

### Failure normalization

The normalized signature uses validator/result class, stable command ID, exit
class, bounded sanitized diagnostic code, affected scope, and contract
version. It excludes timestamps, random paths, credentials, raw stdout/stderr,
provider prose, and volatile IDs. Equivalent failures across providers may
share a semantic class while retaining provider-specific evidence references.

### Compaction and resume

Before compaction, write the minimal checkpoint and a human-readable handoff
summary. On resume, rediscover the repository root, reread current governance,
inspect Git status/diff and owned paths, validate the checkpoint contract and
base identity, recompute remaining work, and discard stale or conflicting
checkpoint claims. Repository state always wins.

### Feedback loop

A repeated, stable failure becomes one of: a regression fixture, a clarified
instruction, a validator improvement, a role/eval case, or an owned external
limitation. Promotion requires evidence and review; raw traces are not copied
into governance.

## Data Modeling & Storage Strategy

The checkpoint is single-task transient state and is overwritten atomically.
Durable evidence is promoted to the canonical Task, Spec, progress ledger,
eval corpus, or provider canary record. A loop event record contains task,
role/provider, state transition, attempt/recovery counters, signature digest,
progress delta class, result class, validation evidence reference, stop reason,
handoff owner, and redaction result.

Fixtures use synthetic paths and diagnostics. They must not embed real tokens,
auth artifacts, user identities, or private provider output.

## Interfaces & Data Structures

- `normalizeFailure(result) -> {failureClass, signatureDigest, retryable}`
- `measureProgress(before, after) -> {progressed, deltaClasses}`
- `decideNext(loopState, budgets, failure, progress) -> retry | stop | escalate`
- `writeCheckpoint(state) -> redacted transient record`
- `resume(checkpoint, repositoryState) -> validated next state or rejection`
- `handoff(state) -> bounded result/evidence/limitation/next-owner summary`

Provider adapters may invoke native hooks or explicit commands, but all must
produce the same state and verdict semantics. A provider hook is never assumed
to be a permission gate on another provider.

## Edge Cases & Error Handling

- Two different tools may surface the same underlying validation failure;
  normalize by semantic diagnostic rather than command prose.
- A formatter mutation can be progress only after the diff is reviewed and
  the relevant validation improves.
- A checkpoint from another worktree, branch, task, or contract version is
  rejected or explicitly migrated; it is never replayed silently.
- Missing checkpoint data causes safe repository rediscovery, not failure to
  resume.
- Provider context compaction without native hook delivery still uses the
  explicit checkpoint/handoff command path.
- Network/transient errors may be retryable, but the same signature and task
  ceilings still apply.

## Failure Modes & Fallback / Human Escalation

- **Same result twice/no progress**: stop and report the signature, attempted
  actions, evidence, and decision needed.
- **Retry budget exhausted**: escalate; do not reset counters through model or
  provider fallback.
- **Sensitive checkpoint candidate**: reject the write, redact to the allowed
  schema, and raise a security finding if exposure occurred.
- **Stale repository base**: discard the proposed next action and rebuild state
  from the repository before continuing.
- **Unavailable reviewer/provider**: preserve a bounded handoff and record the
  work as BLOCKED rather than self-approving.
- **Requested authority expansion**: stop and ask the human owner for the exact
  new permission or external action.

## Verification Commands

Spec 043 must introduce focused loop and checkpoint fixtures before the common
repository gates:

```bash
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --self-test
python3 scripts/validate-agent-checkpoint.py --root . --self-test
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
git diff --check
```

The first three commands are implemented repository-static deliverables. They
validate the provider-neutral loop and checkpoint contracts without claiming
provider-hook delivery, provider runtime, hosted CI, remote, credential, live,
or actual ignored-checkpoint execution.

## Success Criteria & Verification Plan

- **VAL-AHLL-001**: Same-signature fixtures permit no more than two automatic
  retries and preserve the initial attempt separately.
- **VAL-AHLL-002**: Task fixtures permit no more than three default automatic
  recovery actions across failure signatures.
- **VAL-AHLL-003**: The second same-result/no-progress observation terminates
  and escalates even when another numeric budget remains.
- **VAL-AHLL-004**: Non-retryable permission, secret, destructive/live, user
  stop, and contract-corruption classes stop immediately.
- **VAL-AHLL-005**: Checkpoint schema and negative fixtures reject every
  prohibited sensitive or transcript field.
- **VAL-AHLL-006**: Resume rereads repository state and rejects stale task,
  worktree, base, and contract claims.
- **VAL-AHLL-007**: Compaction/handoff retains enough bounded state to continue
  or escalate without a full transcript.
- **VAL-AHLL-008**: Repeated stable failures route to reviewed fixture,
  instruction, validator, eval, or limitation owners.
- **VAL-AHLL-009**: Focused lifecycle tests, strict document checks,
  repository quality gate, and diff checks PASS.

Implementation commits `8a995014d76a92763df420321919e493ec37323e`,
`95a6ee03ff2cdff03cb399b4815ba229b5ff27e8`,
`f0190643e443c28c36e4e54b001589b3a162c903`, and
`9d8a2a368849dbab947eff0e9fb066afc6d239a4` implement the bounded loop,
checkpoint and four-class memory lifecycle, routing/provider projection, and
review remediation. Lifecycle `59`, checkpoint `82`, combined focused tests
`39`, affected surfaces `21/21` with `16` validators, lifecycle self-test
`668`, strict registry `457`, aggregate, all-files, and diff gates passed.
Requirements review returned `COMPLIANT`; quality and security returned
`APPROVED` after every finding was `ADDRESSED`. External and actual
`.agent-work/checkpoint.json` execution claims remain unobserved.

## Traceability

- **Program requirement**: [PRD 003](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **Architecture**: [AD 0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
- **Proposed decision**: [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Predecessor**: [Spec 042](../0042-provider-native-runtime-and-model-evidence/spec.md)
- **Successor**: [Spec 044](../0044-agent-roster-evaluation-and-admission/spec.md)
- **Execution Plan**: [Agent Harness Loop Lifecycle Implementation Plan](plan.md)
- **Task evidence**: [Agent Harness Loop Lifecycle Task](plan.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0011](../../01.requirements/0003-workspace-agent-governance-platform.md#functional-requirements) | VAL-AHLL-001 | Same-signature fixtures prove the retry ceiling. |
| N/A — VAL-AHLL-002 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-002 | Task-budget fixtures prove the recovery ceiling. |
| N/A — VAL-AHLL-003 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-003 | No-progress fixtures prove early stop and escalation. |
| N/A — VAL-AHLL-004 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-004 | Non-retryable fixtures prove immediate termination. |
| N/A — VAL-AHLL-005 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-005 | Checkpoint redaction fixtures prove sensitive-data exclusion. |
| N/A — VAL-AHLL-006 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-006 | Resume fixtures prove stale-state rejection. |
| N/A — VAL-AHLL-007 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-007 | Compaction/handoff fixtures prove bounded recovery state. |
| N/A — VAL-AHLL-008 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-008 | Feedback routing proves durable owner assignment. |
| N/A — VAL-AHLL-009 shares the PRD-0003 source linked in VAL-AHLL-001 | VAL-AHLL-009 | Focused and aggregate QA prove reviewable handoff. |
