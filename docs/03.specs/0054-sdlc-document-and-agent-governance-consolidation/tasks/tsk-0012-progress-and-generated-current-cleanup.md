---
title: "Task: Progress and generated-current cleanup"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-08-30"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0012"
---

# Task: Progress and generated-current cleanup

## Overview

Execution record for WP-012. The progress ledger is retired, the validators
that pinned it are retired with it, and the one part that a sealed record
refuses is recorded rather than forced.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-012 execution boundary](../plan.md#wp-012--progress-and-generated-current-cleanup)
- [MIG-0007](../../../98.archive/migrations/0007-agent-progress-ledger-retirement.md)
- [MIG-0008](../../../98.archive/migrations/0008-progress-append-form-retirement.md)

## Task Table

**Plan label:** WP-012

**Depends on:** WP-011

**Current state:** `done`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-012 | VAL-SDLC-009..VAL-SDLC-012 | Transfer global progress into Spec Tasks and Git, then remove stale generated-current residue. | platform | Done | Ledger retired; progress-prefix and whole-file SHA validators retired; memory surface partly retained, see residuals. | `08c1373c`, `959bd64d`, `89ae40a8` |

### What was executed

`docs/00.agent-governance/memory/progress.md` is deleted. It held 938488 bytes
over 19086 lines and 232 of the 234 commit pins across
`docs/00.agent-governance/`, `.agents/`, `.claude/` and `.codex/`. Its bytes are
recoverable through MIG-0007, which carries its source commit, blob, and content
digest. No Tombstone accompanies it: ADR-0030 admits one only for a deleted path
that needs a durable replacement owner and forbids one where a Migration and Git
recovery suffice.

Twelve current documents link the ledger. Eight already resolved as MIG-0005
consumers; the remaining four are registered in MIG-0007. Registration, not
terminal status, is what admits such a link, because it records that a reviewer
examined the citation at a named commit.

The Plan's instruction to remove the progress-prefix and whole-file SHA
validators is met by retiring the unit that held them.
`COMPLETED_HISTORY_APPEND_ONLY_PREFIX_BYTES` held the ledger's 768684-byte
prefix position and `COMPLETED_HISTORY_ALIAS_SOURCE_BLOBS` its whole-file blob,
alongside 45 others. `Registry` declares no `route_state` field, so
`getattr(registry, "route_state", "terminal")` resolves to `"terminal"` on every
run and `_reviewed_completed_history_alias_edges` returned the empty mapping
unconditionally. Forty-hex pins in `scripts/` fall from 172 to 126.

The two remaining Plan checklist items were already satisfied and are not
re-executed. Spec 0052 WORK-113 is `done` and its Plan row records the transfer
to WORK-054-012. The graphify outputs are ignored by `.gitignore` and no
`graphify-out/` path is tracked, so their consumer count is zero.

### Enabling changes, and one reversal

Two changes were needed before the deletion could be green.

A historical consumer's proof reads its document from Git; the additional
comparison against the working tree proved nothing further about the past and
only froze the present. A consumer a sealed row retires is now released from
that comparison, in `archive_validation` and in the link validator, with the
Git-side proof unchanged.

`_batch_blob_bytes` sent its whole request as one `git cat-file --batch`.
Measured on this tree the proof requested exactly 128 objects against a budget
of 128, so the next migration row or consumer would have failed the whole
repository's recovery proof. The request is now split into batches that each fit
the budget, with the aggregate byte budget threaded across them.

One design was tried and reverted. Admitting any registry-terminal document to
link a retired path replaced review with status, and
`test_public_link_diagnostics_do_not_admit_an_unregistered_done_consumer`
already stated that invariant. The test is right; the rule was removed and
consumer registration used instead.

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
without exception. Direct human approval on 2026-08-30 authorized the recovery
proof change this Task required, after the blocking clause was measured and
presented.

No push, publish, merge, or remote operation is performed by this Task. GitOps
remains the only path to cluster state; this work touches no live cluster.

## Verification Summary

Per commit: the affected or staged validation lane, `pre-commit run` against the
staged index, and the direct suites the change touches. Recorded per commit
message with counts.

At the branch tip, in a clean checkout:

- `bash scripts/validate-repo-quality-gates.sh .`
- `python3 -m unittest discover --start-directory tests --top-level-directory tests --pattern 'test_*.py'`

Results are recorded in `### Handoff` below. Repository-static evidence only; it
proves nothing about CI, provider runtime, remote, or live readiness.

### Residuals

Three items are diagnosed and left, each with the clause that refuses it.

`docs/99.templates/templates/governance/progress.template.md` and the two
registry profiles that route it, `governance/progress-ledger` and
`governance/progress-entry`, are not retired. The form is a `moved` target of
the sealed MIG-0004. `validate_mig0004_historical_targets` already proves those
moves against a pinned commit, but `_validate_mig0004_rows_and_targets` also
requires every Stage 99 target to be present in the current staged inventory, so
deleting the form raises `RECOVERY-MIGRATION-TARGET: current staged target set
differs`. `governance/progress-ledger` therefore still routes nothing. MIG-0008
records the design and the refusal and stays in draft.

The Plan's "remove the Stage 00 memory surface" is partly met. `memory/progress.md`
is gone and `memory/README.md` is rewritten to state that the directory holds no
progress ledger. The directory itself is retained because
`memory.template.md` is a MIG-0004 Stage 99 target under the same clause.

`_reviewed_immutable_historical_alias_edges`,
`_reviewed_source_pinned_alias_edges` and `_immutable_historical_redirects` are
gated on the same always-false `route_state` condition and hold a further 12
blob pins. Retiring them is a separate classification under the Spec 0063
discard-list rule.

### Handoff

- **Scope**: `docs/00.agent-governance/memory/`, `docs/98.archive/migrations/`,
  `scripts/archive_validation.py`, `scripts/validate-links-and-owners.py`,
  `docs/00.agent-governance/policies/context-and-memory.md`, and the two test
  modules that cover them.
- **Commits**: `90b5a745`, `2a74c122`, `08c1373c`, `959bd64d`, `f6eb1636`,
  `89ae40a8`.
- **Rollback**: each commit is one logical unit; `git revert` restores the prior
  state. The deleted bytes remain in Git history at the commits MIG-0007 and
  MIG-0008 record.
- **Review disposition**: self-reviewed against the Spec 0063 classification
  rule and the Spec 0064 diagnosis. No second reviewer.
- **Residual risk**: the consumer release and the batch split both loosen a
  recovery-proof guard. Each is narrowed by a test, and a regression surfaces as
  a gate or suite failure on the next cycle.
- **Unavailable checks**: no CI, provider-runtime, remote, or live evidence was
  produced.
- **Next owner**: platform, for the three residuals above and for the merge of
  this branch.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-012](../plan.md#wp-012--progress-and-generated-current-cleanup) | Done, with three recorded residuals. | Commits and verification above |
| N/A — Spec 0064 is terminal, so it can neither record this itself nor add the reciprocal a link would require | Spec 0064 `VAL-AGS-002` is now met: the ledger is retired and no inbound link breaks. | `08c1373c` |
| N/A — Spec 0052 is terminal, so its Plan cannot add the reciprocal a link would require | Spec 0052 `WORK-113` was already transferred to this work package and closed. | `docs/03.specs/0052-document-taxonomy-consolidation/plan.md`, WORK-113 row |
