---
title: "Shared Workspace Memory Store"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0109"
---

# Shared Workspace Memory Store Technical Specification (Spec)

## Overview

Design-only draft for v9 findings F23, F24 and F27: one memory store that
Claude and Codex sessions in this workspace both read and write, retained
across task completion, session end and elapsed time. The operator chose on
2026-10-13 to record the design without implementing it. This draft does
not change the current [context and memory policy](../../../.agents/governance/context-and-memory.md),
which still discards task-local context and keeps no memory directory
(Spec 0054 and Spec 0065 retirements). Adopting this design reverses that
decision and needs its own review and approval.

## Strategic Boundaries & Non-goals

- In scope once approved: a SQLite store, a shared CLI, tier schemas,
  retention, quotas, revision conflicts, backup and native memory
  disablement for both providers.
- Non-goals: memory as Task evidence, approval or acceptance; copying
  policy into memory; collecting private provider sessions or raw
  transcripts; syncing across machines or clones; deleting existing native
  memory files.

## Contracts

- The active Task stays the sole owner of execution status, blockers and
  acceptance. A memory body, `memory_id` or summary PASS is never Task
  evidence.
- Completion, cancellation, session end, compaction, promotion, age and low
  use never delete or lossy-summarize a memory body.
- Eligibility (`candidate`, `current`, `needs-review`, `superseded`,
  `withdrawn`) controls default retrieval only and is separate from
  retention. A changed, deleted or inaccessible source removes derived
  entries from default retrieval and re-checks history access.
- Concurrent writes use an expected revision; silent last-write-wins is
  forbidden. A capacity refusal leaves existing bodies and revisions intact.

## Core Design

One store at the representative worktree root, resolved from
`git rev-parse --git-common-dir` plus a host-local `workspace_id` binding,
at `.workspace-memory/memory.sqlite3` (Git-ignored, excluded from
templates and builds). Linked worktrees use the same physical file; an
unresolvable root reports the store unavailable and never creates a second
database. Writes run in one `BEGIN IMMEDIATE` transaction with a bounded
busy timeout that checks expected revision, idempotency key, tier and domain
usage and payload size, then commits body, revision and usage together.

The store uses the rollback journal (`journal_mode=DELETE`), not WAL. The
review on 2026-10-13 observed the local Python SQLite library at 3.45.1,
which is neither 3.51.3 or later nor one of the named WAL-reset backports
(3.44.6, 3.50.7). The rollback journal avoids that defect, keeps one writer
at a time, and leaves only the database, its transient journal, one backup
and one temporary backup file as runtime files.

## Data Modeling & Storage Strategy

Common envelope: `schema_version`, `workspace_id`, `memory_id`, `tier`,
`revision`, `owner`, `created_at`, `source_refs`, `eligibility`,
`sensitivity`, `body`.

| Tier | Body and specific fields |
| --- | --- |
| short-term | `task_ref`, decision, failure and resolution narrative, open questions, reuse conditions |
| long-term | reviewed claim, reason, applicability, counterexamples and limits, sources |
| domain | `domain_id`, symptom, cause, resolution, compatible environment, applicability |

Proposed initial limits, not yet approved: short-term 64 MiB, long-term
128 MiB, all domains 256 MiB, one domain 64 MiB, one revision payload
256 KiB, main database 1 GiB, whole store area 4 GiB, at most eight runtime
files. Logical usage counts every revision and conflict. `max_page_count`
bounds only the main database; a hard 4 GiB guarantee needs a filesystem
quota, otherwise the limit is reported as observed, not enforced. The
review observed an ext4 root filesystem with no project quota, so the first
implementation reports the area limit as observed only.

## Interfaces & Data Structures

A shared CLI under `scripts/` with: resolve workspace, current query,
bounded history query, write with expected revision, eligibility
correction, usage report and consistent backup. Claude sets
`autoMemoryEnabled: false` in `.claude/settings.json`; the governance
validator already rejects a subagent `memory` field and must admit exactly
this new settings key with the value `false`. Codex uses
`[memories] generate_memories = false` and `use_memories = false`; the
review found both keys in the installed `codex-cli 0.162.1` binary (static
evidence only). `.codex/config.toml` is not validated today, so adoption
adds an exact-content check that admits only that table, rewrites the
`.codex/README.md` and `.codex/provider.md` statements that tie the absent
file to hook registration, and records that Codex reads a project config
only for a trusted project. Disabling Claude auto memory stops the existing
per-project native memory from being read in new sessions; its files are
neither deleted nor imported automatically.

## Edge Cases & Error Handling

`MEMORY_CAPACITY_EXCEEDED` refuses only the new write. A conflict that cannot
be stored returns both revisions and says it was not stored. `SQLITE_FULL`,
`SQLITE_BUSY`, checkpoint stalls and backup failure keep the previous good
backup and report failure. WAL is never shared over a network filesystem.

## Failure Modes & Fallback / Human Escalation

A memory failure never blocks ordinary repository work or QA. Capacity
increases, exceptional deletion and any migration of an existing store are
explicit owner decisions recorded in a Task.

## Verification Commands

- Focused store tests on a temporary database: tier schemas, revision
  conflict, quota refusal without loss, retention after Task completion,
  source-change exclusion, backup replacement and backup failure.
- `python3 scripts/validate-agent-governance.py --root .` for the native
  settings and Codex config checks.
- Record the linked `sqlite3.sqlite_version` with each acceptance run.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-MEMORY-001 | Synthetic store tests show cross-tier schema, expected-revision conflict, quota refusal without loss, retention across completion, default-retrieval exclusion after a source change and a consistent backup. |
| VAL-MEMORY-002 | Two real provider sessions in two worktrees read the same `memory_id`, revision and body from the same file, and neither writes native memory. Static or single-process tests do not satisfy this criterion. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0022](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-MEMORY-001 | Requires an approved requirement change first: FR-0022 currently forbids restoring a shared progress owner, which this store must not become. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-MEMORY-002 | Repository-static versus provider-runtime evidence kept apart. |
