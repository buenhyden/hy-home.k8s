---
title: "Context and Memory Policy"
version: "1.8.1"
type: "governance/rule"
status: "active"
owner: "platform"
updated: "2026-11-17"
---

# Context and Memory Policy

## Purpose and Scope

### Objective

Retain only the context needed to resume safely. Repository state and the
owning SDLC document, not a memory ledger, determine current truth; the retired progress ledger stays retired, and the work residue ledger of ADR-0060 is a different, residue-only owner.

### Applies To

Compaction and handoff can preserve useful summaries while also carrying stale
assumptions. Resume only through the [resume decision](#resume-decision).

- Archive Index (`docs/98.archive/README.md`)

#### Exclusions

This policy excludes no subject within its scope; if one is excluded, name it and its owner here.

## Rules

### Requirements

| Rule ID | Condition | Level | Evidence | Status |
| --- | --- | --- | --- | --- |
| CTX-R001 | Always | required | Semantic review | active |
| CTX-R002 | When promoting recurring knowledge | required | Semantic review | active |
| CTX-R003 | Always | required | `knowledge-surface` | active |
| CTX-R004 | Always | required | Semantic review | active |
| CTX-R005 | Always | required | Semantic review | active |
| CTX-R006 | Always | required | `workspace-memory-regressions` | active |
| CTX-R007 | Always | required | `repository-quality` | active |
| CTX-R008 | Always | required | Semantic review | active |
| CTX-R009 | When using the shared workspace memory store | required | `workspace-memory-regressions` | active |
| CTX-R010 | When writing a memory body | required | `workspace-memory-regressions` | active |
| CTX-R011 | When writing a memory in a tier | required | `workspace-memory-regressions` | active |
| CTX-R012 | Always | required | `workspace-memory-regressions` | active |
| CTX-R013 | When writing a memory | required | `workspace-memory-regressions` | active |
| CTX-R014 | When an idempotency key is reused | required | `workspace-memory-regressions` | active |
| CTX-R015 | When a memory carries source refs | required | `workspace-memory-regressions` | active |
| CTX-R016 | Always | required | `workspace-memory-regressions` | active |
| CTX-R017 | Always | required | `workspace-memory-regressions` | active |
| CTX-R018 | Always | required | `agent-governance` | active |
| CTX-R019 | When a reviewed observation carries a knowledge-fact block | required | `knowledge-surface` | active |
| CTX-R020 | Before dependent mutation, on resume | required | Semantic review | active |

- `CTX-R001` Keep working context bounded, factual, redacted, and scoped to one task.
  Record remaining acceptance criteria and next owner rather than raw sessions.
- `CTX-R002` Promote recurring knowledge only after review into the appropriate policy,
  skill, operating document, or reference record.
- `CTX-R003` Durable knowledge about one domain — Kubernetes and GitOps desired state,
  networking, secret handling, observability — stays with that domain's
  operating or reference owner. Reach it through the stage index rather than
  copying it into a governance summary; use
  [`knowledge-map`](../skills/knowledge-map/SKILL.md) to find stale navigation
  without creating a second authority for the same subject.
- `CTX-R004` Provider-local recall never writes canonical truth directly; verify it
  against the repository first. A provider's memory feature does not change
  repository ownership or permission.
- `CTX-R005` Hand task-local evidence to its Task owner. Reusable decision context may
  instead be kept in the shared workspace memory store below; durable policy
  and domain knowledge still refresh, supersede, or retire through their
  profile contract.
- `CTX-R006` Do not read or store credentials, secret values, personal data, auth
  configuration, shell history, environment dumps, raw prompts, or complete
  provider transcripts, in the store or its metadata.
- `CTX-R007` The `memory/progress.md` ledger and the `memory/` directory are retired and
  neither is restored; Git history recovers their bytes. The work residue ledger is not the retired ledger. Progress and task
  status belong to the owning Spec Task, and durable knowledge stays with the
  responsible policy, skill, operating document, or reference owner. `.agents/knowledge/` maps those owners
  without restating them; it is a pointer surface, never a second store of
  current state. Its one exception, `glossary.md`, owns term meanings and
  states no rule (ADR-0058).
- `CTX-R008` A checkpoint is an optional, untracked human aid; no repository tool creates
  one. Static validation of a synthetic checkpoint proves neither actual
  checkpoint execution nor provider memory, hook, or compaction behavior.

#### Shared workspace memory store

`CTX-R009`

SPEC-0109 (Git history: package `0109-shared-workspace-memory` under
`docs/03.specs/` at commit `69445fca`) defined one store that Claude and Codex sessions both read and write:
`.workspace-memory/memory.sqlite3` at the main worktree root, resolved from the
Git common directory so every linked worktree reaches the same file. It is
Git-ignored runtime data. Use `scripts/workspace_memory.py`; run `init` once,
and never create a second store when the root cannot be resolved.
If the representative worktree or Git common directory moves, stop and have the
operator reconnect the existing store and verify its workspace identity before
resuming. A separate Git directory layout is currently unsupported; it reports
`MEMORY_UNAVAILABLE` and does not authorize a replacement store.

- `CTX-R010` A memory body is decision context: why a choice was made, why a check
  failed, how it was resolved and when that applies again. It is never Task
  status, evidence, approval or acceptance, and the store rejects bodies that
  carry those fields. Cite the original record in the Task instead.
- `CTX-R011` Tiers share one envelope (`workspace_id`, `memory_id`, `tier`, `revision`,
  `owner`, source refs, `eligibility`, `sensitivity`, body). `short-term`
  needs context and narrative, `long-term` a reviewed claim, reason and
  applicability, and `domain` a `domain_id`, symptom, cause and resolution.
- `CTX-R012` Task completion, session end, compaction, promotion and age never delete
  or summarize a memory. Eligibility (`candidate`, `current`, `needs-review`,
  `superseded`, `withdrawn`) only controls the default view, which returns
  `current` memories whose source refs are unchanged; history keeps every
  revision and conflict and is labelled as history.
- `CTX-R013` A write names the expected revision. A stale write is kept as a conflict
  when capacity allows, otherwise both revisions are reported and nothing
  changes. A full tier, domain or revision limit refuses only the new write
  with `MEMORY_CAPACITY_EXCEEDED`; ordinary repository work and QA continue.
- `CTX-R014` An idempotency key is bound to the complete request, including target,
  expected revision, body, sources and scope. Reusing it with different input
  fails with `MEMORY_CONFLICT`; an old result without a request digest cannot
  be replayed as a successful write. Existing revisions remain intact.
- `CTX-R015` Repository-relative source refs currently retain `path` and `sha256`. A
  source is read from the caller's worktree; a symlink in any path component,
  a non-regular file, an inaccessible file or changed bytes makes it
  unavailable or stale. Default retrieval excludes stale entries. Direct ID
  and history reads can show them for review, never as current authority.
- `CTX-R016` The SQLite page limit is set and checked on each connection and bounds the
  main database only. The 4 GiB store-area limit remains an observation, not
  a filesystem quota. Backups use a private temporary file, serialize with
  other backups, verify schema, workspace identity, revisions and conflicts,
  then atomically replace the single backup. A failed backup preserves the
  previous valid copy. To restore, stop every writer, remove a leftover
  `memory.sqlite3-journal` beside the store, copy the backup over the store
  file and confirm `pragma integrity_check` returns `ok`; the restored store
  reads the same records.
- `CTX-R017` The store accepts only `public` or `internal` sensitivity.
- `CTX-R018` Native Claude and Codex memory stay disabled in project configuration, and
  their existing files are neither deleted nor imported.

#### Bounded observation metadata

`CTX-R019`

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
The validator checks metadata, file identity and dates; it cannot authenticate
an approval or infer whether a writer concealed sensitive content.

#### Resume decision

`CTX-R020`

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
with the affected handoff. Deadlines, worker allocations and reserve approvals are not created from a
checkpoint (see [quality](quality.md#validation-runner-envelope)); unknown
account limits remain unverified for the dependent provider request and do
not block independent local work. A summary saying PASS does not waive this
recheck. These are agent and operator obligations, not a claim of native
runtime enforcement.

### Exceptions

This policy defines no exception condition of its own; exceptions follow the approval and safety policy's operator approval route. If this policy needs its own, state it here.

#### Approval and Review

Approval and review conditions are stated under Requirements.

## Enforcement

### Mechanisms

Check summaries for stale owner links, duplicated task state, and sensitive
data. Report conflicting memory rather than rewriting the repository to match
it. Use [quality policy](quality.md) for evidence and handoff classification.

### Limits

Temporary checkpoints and provider-local memory are advisory and confer no execution authority, and this policy grants no provider or runtime capability, execution permission or approval authority. Its checks look for stale owner links, duplicated task state and sensitive data, and conflicting memory is reported rather than used to rewrite the repository.

## Ownership

### Owner

This policy owns repository context retention, resume verification, and the
boundary for advisory provider-local memory. It grants no provider/runtime
capability, execution permission, or approval authority; the active execution,
approval, and provider controls continue to own those concerns.

The active Task owns work status, verification, and handoff. Requirements,
ADRs, Specs, Runbooks, and incident records own durable domain knowledge.
Temporary checkpoints and provider-local memory are advisory and confer no
execution authority.

- [Work Lifecycle](../workflows/work-lifecycle.md)
- [Document Lifecycle](document-lifecycle.md)
- [Approval and Safety](approval-and-safety.md)
- [Quality Policy](quality.md)

#### Responsibilities

Responsibilities are stated under Owner and Requirements.

### Review Triggers

This policy changes as a governed-document change under the work lifecycle and the document lifecycle policy, with no adoption step of its own; if it needs one, state it here.
