---
title: "Explicit Multi-row Task Summary Writer"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0002"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Explicit Multi-row Task Summary Writer

## Overview

This follow-up owns the implementation and observed evidence for
[VAL-P02-002](../spec.md#success-criteria--verification-plan). The completed
parent Spec/Plan and [original Task](tsk-0001-lifecycle-normalization.md)
retain their historical acceptance and EVD-P02-013/014. The [Plan](../plan.md)
owns WORK-002 order; this Task alone owns actual execution results.
Its eventual `completed` state records local source acceptance, not a claim
that authorized remote integration has already happened. PR and integrated
main SHA results require separate observed evidence.

## Inputs

- Direct approved P02 follow-up plan: explicit opt-in Task status generation,
  four local logical commits, focused and exact-index checks, independent
  read-only review, and initial local handoff. The request owner's later
  instruction authorizes work-unit commits, push and merge through required
  hosted checks. Local full and affected execution are excluded
  for this follow-up only; their results are `NOT_RUN`, not a global policy
  change. No authenticated external approval is inferred.
- Starting snapshot: clean `main` at `9067729bf6679a0cd536362113be261056c32dd6`,
  clean preserved P01 tip `df3281d06a931bff6784bcc462800fab23bbb1c9`,
  new clean `codex/p02-task-summary` worktree at the P01 tip. Neither prior
  worktree is the writer of this Task.
- Current [Stage 99 contract](../../../99.templates/registry.json),
  [Task form](../../../99.templates/templates/specs/task.template.md), and
  [quality policy](../../../../.agents/governance/quality.md). Python 3.12.3,
  Git 2.43.0, and pre-commit 4.6.1 are available. `core.hooksPath` selects
  `scripts/githooks`; hook delivery and commit-message execution must be
  observed per candidate. The validation runner supplies bounded child
  time/output limits; exact selected gates are determined from each index.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-002 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | Extract shared summary, implement opt-in writer, verify and hand off | repo-tooling-engineer | frontmatter | NOT_RUN | pending | Focused and staged evidence pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-015 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused RED/GREEN and historical summary regression | Exact source and test snapshots pending | NOT_RUN | Pending | pending |
| EVD-P02-016 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Initial draft exact-index staged check | Tree `2b63fc32e90b4126397c37348a7137bc602e159b` at base `df3281d0…` | FAIL | [Verification Summary](#verification-summary) | pending |
| EVD-P02-017 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Completion anchor and independent semantic review | Final candidate pending | NOT_RUN | Pending | pending |
| EVD-P02-018 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Repaired draft exact-index staged/message checks and semantic review | Tree `d3a0bcbb7191d017ef467f086c80f6554c73d054` at base `df3281d0…` | PASS | [Verification Summary](#verification-summary) | accepted |
| EVD-P02-019 | [VAL-P02-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Current and subsequent exact-index staged/message checks | Changed authorization and future logical indexes pending | NOT_RUN | Pending | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/document_contracts.py`, new `scripts/sync-task-status.py`, new `tests/test_task_summary_writer.py`, focused existing Task tests if necessary, `docs/99.templates/README.md`, `docs/99.templates/templates/specs/task.template.md`, and this Spec/Plan/new Task.
- **Forbidden Paths**: Registry generation or Schema, registered validator/hook behavior, original Task/EVD-P02-013/014, frozen Archive, native provider state, secrets, live resources, and unrelated user changes.
- **Approval Required**: The direct user plan authorizes scoped local authoring, checks, review, and four normal local commits; the later user instruction also authorizes work-unit push and merge after required review and hosted checks. Worktree removal, Archive mutation, native trust and live work remain outside this scope. No approval actor authentication or revocation check is claimed.
- **Static Validation**: Focused RED/GREEN for changed behavior, existing Task aggregation regression, actual index staged QA and message check before each commit; final completion mode and independent read-only review. Affected selection only; local affected and full execution `NOT_RUN` under this follow-up's explicit exclusion. The exact PR SHA's required hosted checks gate merge; the integrated main SHA's hosted result is checked after merge before integration acceptance.
- **Live Validation**: DEFER — not requested or authorized; repository-static results cannot establish runtime activation.
- **Secret / Vault Handling**: Do not read or print secret values; use public contract paths and synthetic fixtures only.
- **Rollback Plan**: Use a reviewed forward corrective commit or forward revert of the scoped P02 commits, preserving historical evidence and both existing worktrees.
- **Evidence Location**: This Task for execution outcomes; bounded raw output can remain in ignored local scratch without becoming a second source of truth.

## Verification Summary

Initial draft index `2b63fc32e90b4126397c37348a7137bc602e159b`
ran canonical staged QA: 5/6 selected gates PASS and repository-quality FAIL
`EXECUTABLE-HISTORY` because the draft Spec named the planned executable
before it existed. The actual message check passed. The failing gate's raw
output is retained under `/tmp/hy-p02-c1-staged.stdout` (SHA-256
`459659fe593f4a6a5a2fa289a303daf9e8cb06fd5f525313cbff4bf65ed0bb85`).
The draft Spec now describes the planned interface without citing a nonexistent
executable. The repaired draft tree `d3a0bcbb7191d017ef467f086c80f6554c73d054`
then passed all six selected staged gates and the same exact message passed
Commitizen. Raw staged output is `/tmp/hy-p02-c1-repair-staged.stdout`
(SHA-256 `1e07ba4bff6ca568f2ac89204b7b8bdb99686d7adab19ea4dc883c13ac08dce5`).
A distinct read-only code-reviewer checked that tree and reported no material
finding. This proof predates the later authorized push/merge scope and is not
reused for the changed index.

The next authorization-update tree
`474200c39284a4dddfb26a52636de8e39755cdc4` passed 6/6 staged gates and
the actual message check, but independent review found two remaining
historical remote-action prohibitions stated as current. That candidate was
not committed. The Spec/Plan now scope those words to original WORK-001 or
remove their current application; the new index requires fresh checks and
review.

The following tree `52023d0756b1aa9748324dedc3ee097f8c62b956` also passed
6/6 staged gates and the message check, but review found an impossible check
order: an integrated SHA cannot be validated before merge. That candidate was
not committed. The Task now assigns PR hosted checks before merge and
integrated main SHA checks after merge; this revised index awaits review and
staged validation.

At draft intake the implementation, focused regression, current staged/message,
completion, and independent review checks are `NOT_RUN/pending`. Selected
affected gates will be recorded without executing the affected lane. Full QA
is `NOT_RUN/not-required` locally for this follow-up; hosted full checks remain
pending on delivered revisions. Residual risk and next
owner are repo-tooling-engineer until source checks and independent review
establish acceptance; remote push/merge are authorized but unobserved, and
operator-owned native/live observations remain `DEFER`.
