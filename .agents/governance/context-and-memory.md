---
title: "Context and Memory Policy"
version: "1.4.0"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-10-15"
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
- Hand task-local evidence to its Task owner. Reusable decision context may
  instead be kept in the shared workspace memory store below; durable policy
  and domain knowledge still refresh, supersede, or retire through their
  profile contract.
- Do not read or store credentials, secret values, auth configuration, shell
  history, environment dumps, raw prompts, or complete provider transcripts.
- The `memory/progress.md` ledger is retired under Spec 0054 WP-012 and the
  `memory/` directory under Spec 0065; their bytes are recoverable from Git
  through `MIG-0007` and `MIG-0009`, and neither is restored. Progress and task
  status belong to the owning Spec Task, and durable knowledge stays with the
  responsible policy, skill, operating document, or reference owner. `.agents/knowledge/` maps those owners
  without restating them; it is a pointer surface, never a second store of
  current state.
- Ignored checkpoints are optional recovery aids. Static validation of a
  synthetic checkpoint proves neither actual checkpoint execution nor provider
  memory, hook, or compaction behavior.

### Shared workspace memory store

SPEC-0109, reached through the Stage 03 index (`docs/03.specs/README.md`),
defines one store that Claude and Codex sessions both read and write:
`.workspace-memory/memory.sqlite3` at the main worktree root, resolved from the
Git common directory so every linked worktree reaches the same file. It is
Git-ignored runtime data. Use `scripts/workspace_memory.py`; run `init` once,
and never create a second store when the root cannot be resolved.
If the representative worktree or Git common directory moves, stop and have the
operator reconnect the existing store and verify its workspace identity before
resuming. A separate Git directory layout is currently unsupported; it reports
`MEMORY_UNAVAILABLE` and does not authorize a replacement store.

- A memory body is decision context: why a choice was made, why a check
  failed, how it was resolved and when that applies again. It is never Task
  status, evidence, approval or acceptance, and the store rejects bodies that
  carry those fields. Cite the original record in the Task instead.
- Tiers share one envelope (`workspace_id`, `memory_id`, `tier`, `revision`,
  `owner`, source refs, `eligibility`, `sensitivity`, body). `short-term`
  needs context and narrative, `long-term` a reviewed claim, reason and
  applicability, and `domain` a `domain_id`, symptom, cause and resolution.
- Task completion, session end, compaction, promotion and age never delete
  or summarize a memory. Eligibility (`candidate`, `current`, `needs-review`,
  `superseded`, `withdrawn`) only controls the default view, which returns
  `current` memories whose source refs are unchanged; history keeps every
  revision and conflict and is labelled as history.
- A write names the expected revision. A stale write is kept as a conflict
  when capacity allows, otherwise both revisions are reported and nothing
  changes. A full tier, domain or revision limit refuses only the new write
  with `MEMORY_CAPACITY_EXCEEDED`; ordinary repository work and QA continue.
- An idempotency key is bound to the complete request, including target,
  expected revision, body, sources and scope. Reusing it with different input
  fails with `MEMORY_CONFLICT`; an old result without a request digest cannot
  be replayed as a successful write. Existing revisions remain intact.
- Repository-relative source refs currently retain `path` and `sha256`. A
  source is read from the caller's worktree; a symlink in any path component,
  a non-regular file, an inaccessible file or changed bytes makes it
  unavailable or stale. Default retrieval excludes stale entries. Direct ID
  and history reads can show them for review, never as current authority.
- The SQLite page limit is set and checked on each connection and bounds the
  main database only. The 4 GiB store-area limit remains an observation, not
  a filesystem quota. Backups use a private temporary file, serialize with
  other backups, verify schema, workspace identity, revisions and conflicts,
  then atomically replace the single backup. A failed backup preserves the
  previous valid copy. To restore, stop every writer, remove a leftover
  `memory.sqlite3-journal` beside the store, copy the backup over the store
  file and confirm `pragma integrity_check` returns `ok`; the restored store
  reads the same records.
- Never store credentials, secret values, personal data or raw transcripts;
  the store accepts only `public` or `internal` sensitivity.
- Native Claude and Codex memory stay disabled in project configuration, and
  their existing files are neither deleted nor imported.

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
