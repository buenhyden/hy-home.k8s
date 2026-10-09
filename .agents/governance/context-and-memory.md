---
title: "Context and Memory Policy"
version: "1.2.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-09"
---

# Context and Memory Policy

## Overview

Retain only the context needed to resume safely. Repository state and the
owning SDLC document, not a memory ledger, determine current truth.

## Authority Boundary

This policy owns repository context retention, resume verification, and the
boundary for advisory provider-local memory. It grants no provider/runtime
capability, execution permission, or approval authority; the active execution,
approval, and provider controls continue to own those concerns.

The active Task owns work status, verification, and handoff. Requirements,
ADRs, Specs, Runbooks, and incident records own durable domain knowledge.
Temporary checkpoints and provider-local memory are advisory and confer no
execution authority.

## Governance Context

Compaction and handoff can preserve useful summaries while also carrying stale
assumptions. On resume, re-observe Git state, the active Task, and changed
canonical owners before using remembered paths, results, or approvals.

## Current Contract

- Keep working context bounded, factual, redacted, and scoped to one task.
  Record remaining acceptance criteria and next owner rather than raw sessions.
- Promote recurring knowledge only after review into the appropriate policy,
  skill, operating document, or reference record. Do not create a duplicate
  current-state ledger.
- Durable knowledge about one domain — Kubernetes and GitOps desired state,
  networking, secret handling, observability — stays with that domain's
  operating or reference owner. Reach it through the stage index rather than
  copying it into a governance summary; use
  [`knowledge-map`](../skills/knowledge-map/SKILL.md) to find stale navigation
  without creating a second authority for the same subject.
- Provider-local recall never writes canonical truth directly; verify it
  against the repository first. A provider's memory feature does not change
  repository ownership or permission.
- Discard task-local context after its useful evidence reaches the owner.
  Refresh, supersede, or retire durable knowledge through its profile contract.
- Do not read or store credentials, secret values, auth configuration, shell
  history, environment dumps, raw prompts, or complete provider transcripts.
- The `memory/progress.md` ledger is retired under Spec 0054 WP-012 and the
  `memory/` directory under Spec 0065; their bytes are recoverable from Git
  through `MIG-0007` and `MIG-0009`. Progress and task status belong to the
  owning Spec Task. No governance memory directory remains, so durable
  knowledge stays with the responsible policy, skill, operating document, or
  reference owner. `.agents/knowledge/` maps those owners
  without restating them; it is a pointer surface, never a second store of
  current state.
- Ignored checkpoints are optional recovery aids. Static validation of a
  synthetic checkpoint proves neither actual checkpoint execution nor provider
  memory, hook, or compaction behavior.

### Bounded observation metadata

A reviewed observation may carry a `knowledge-fact` JSON block in an existing
knowledge document. It records provenance, not a copy of the source policy.
All eight fields are required: `owner`, `scope`, `source` (tracked repository path and
SHA-256), `observed_at` (ISO date), `valid_for` (inclusive ISO expiry date),
`invalidated_by` (`source`, `scope`, `approval`, `validity`), `review_status`
(`advisory` or `current` while reusable), and `sensitivity` (`public`).
`current` means reviewed at the named owner; it grants no permission.

Before promoting, correcting or deleting an observation, re-read its owner and
source, verify sensitivity and the current authorization, and record the change
at that owner. Expired or withdrawn observations are not reusable; remove their
active metadata block or refresh it through owner review. A deleted or changed
source invalidates its SHA-256 and every derived cache. Scope, authorization or
expiry changes also invalidate caches even if the file hash is unchanged.
Do not retain secret values, personal data or raw transcripts in metadata.
The validator checks metadata, file identity and dates; it cannot authenticate
an approval or infer whether a writer concealed sensitive content.

### Resume decision

Re-observe the worktree, branch, HEAD and divergence base, relevant file hashes,
staged/unstaged paths and changed consumers before dependent mutation. Compare
current user authorization and revocation state with the Task's scope; a saved
approval is evidence of a past decision, not fresh authority. Resolve any other
writer's ownership before writing shared files.

Stop dependent mutation on a mismatch, expired/deleted/redacted source, revoked
or missing approval, concurrent writer conflict, or partial subprocess result.
Retain completed evidence, identify failed/DEFER lanes, remaining work, rollback
and next owner, then refresh only invalidated evidence. Carry actual
cancellation, observed provider request/resource limits and `Retry-After`
with the affected handoff. Do not create an elapsed-time work deadline,
shared worker allocation or reserve approval from a checkpoint; unknown
account limits remain unverified for the dependent provider request and do
not block independent local work. A summary saying PASS does not waive this
recheck. These are agent and operator obligations, not a claim of native
runtime enforcement.

## Validation and Refresh

Check summaries for stale owner links, duplicated task state, and sensitive
data. Report conflicting memory rather than rewriting the repository to match
it. Use [quality policy](quality.md) for evidence and handoff classification.

## Related Documents

- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Document Lifecycle](document-lifecycle.md)
- Archive Index (`docs/98.archive/README.md`)
- [Approval and Safety](approval-and-safety.md)
