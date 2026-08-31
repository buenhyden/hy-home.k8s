---
title: 'Validation Tooling Ownership Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: 2026-08-31
artifact_id: "PLAN-0066"
---

# Validation Tooling Ownership Implementation Plan

## Global Constraints

- Spec 0066 is the delegated execution owner for Spec 0054 WP-010 and WP-011.
  Spec 0054 retains integrated acceptance ownership.
- Proposed [ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
  defines the target current-corpus and validation-routing ownership. It does
  not activate this Plan while it remains proposed. Activation first requires
  its `proposed → accepted` transition and `supersedes` relation; all five
  predecessors' `accepted → superseded` transitions and reciprocal
  `superseded_by: ADR-0031` links; and the two-clause ADR-0030 scoped-amendment
  note plus Decisions README state/explanation and current `Proposed ADR-0031`
  label updates in one validated logical change. ADR-0030 otherwise remains
  `accepted` and gains no lifecycle supersession relation.
- The existing validation-surface JSON and schema move atomically from
  `docs/00.agent-governance/contracts/` to `scripts/validation/registry.*`.
  Source and target never operate as two current registries.
- The registry owns routing only. Rule semantics remain in responsible modules;
  point-in-time inventory and disposition belong in the active Task and Git
  diff, not a permanent all-file ledger.
- Tests and fixtures remain under top-level `tests/` and `tests/fixtures/`.
  Production modules may not import from or read those paths.
- No fixed entrypoint count, module line limit, negative-case count, branch-tip
  SHA, or terminal inventory count is an invariant.
- Each logical change is independently testable and reversible. A wrapper is
  deleted only with current-consumer-zero and unique-diagnostic-zero evidence.
- Existing required CI check names remain stable until authorized remote
  protection-rule verification supports a separate decision.
- This Plan remains `draft`, and its only Task remains `queued`, until the
  design review and activation checkpoint are complete.
- After WP-009 and its owning Task finish, TSK-0054-0010 becomes the sole active
  parent Task in a separate lifecycle-valid handoff. That handoff also moves
  the existing Spec 0054 `standaloneExecutions` task pointer to
  TSK-0054-0010. It then owns one atomic activation transaction before this
  Plan executes: accept ADR-0031; supersede its five named predecessors with
  reciprocal relations; update the two scoped ADR-0030 clauses, the Decisions
  README, every current `Proposed ADR-0031` label, and the Stage 03
  validator-test placement rules; update this package README's current-state
  prose and the Current Spec Index row from `Draft` to `Active`; add the narrow
  package-local delegated-component gate and focused tests; activate
  Spec/Plan/Task 0066, move the parent compatibility pointer to TSK-0054-0011,
  complete TSK-0054-0010, and activate TSK-0054-0011 as the sole parent
  acceptance Task. The thin package README already exists; its state projection
  and the Current Spec Index are updated and verified in that transaction.
  TSK-0066-0001 does not activate itself or split that transfer
  across batches. No Spec 0066 standalone row is created, and existing Task
  transitions are reused without a Stage 99 lifecycle or code-projection
  change.

## Overview

This Plan corrects validation ownership without creating another control plane.
It first establishes reliable current-reference and staged-index behavior, then
moves the existing routing contract, removes production test dependencies and
self-tests, assigns each rule one semantic owner, thins runners, and retires
only compatibility paths that have no consumers or unique behavior.

Selection equivalence is required only for the atomic registry move. After that
checkpoint, routing may be intentionally simplified when the Task records the
old and new selection, the reason, and focused evidence.

## Context

The current audit found these structural risks:

- executable-reference matching does not cover all current extensions and
  depths;
- the affected selector routes validation changes broadly enough to duplicate
  work across aggregate, hooks, and CI;
- the aggregate contains rule meaning that belongs to responsibility owners;
- production modules embed self-tests or consume test fixtures;
- compatibility wrappers overlap with direct validator consumers;
- branch/current-state pins and duplicated historical aliases obscure Git-first
  recovery and the bounded sealed-Migration exception;
- staged checks can appear green without proving the index was the evaluated
  subject.

Exact counts remain Task evidence and may change as concurrent work lands. They
are not copied into the contract.

## Goals & In-Scope

1. Make current executable references extension-neutral and depth-aware while
   preserving Git-first historical recovery and bounded sealed-record
   exceptions.
2. Move and reuse the existing validation-surface contract and schema at the
   scripts-owned path with no coexistence period.
3. Make the registry the single routing graph and validator modules the single
   semantic owners.
4. Replace production `--self-test` and production fixture reads with
   independent top-level tests and production-owned data where required.
5. Simplify aggregates, runners, hooks, and CI routing without changing required
   external check names before remote verification.
6. Remove wrappers, dead fixtures, aliases, and current-state pins only after
   their surviving owner and recovery path are proved.
7. Preserve deterministic staged/index behavior, bounded I/O, explicit UTF-8,
   subprocess timeouts, and actionable diagnostics.

## Non-Goals & Out-of-Scope

- No live cluster, provider runtime, hosted CI, push, merge, deployment, or
  branch-protection mutation.
- No forced consolidation into a predetermined number of entrypoints.
- No split performed solely to satisfy a line-count ceiling.
- No permanent ledger row for every script, test, fixture, hook, pin, or audit
  decision.
- No acceptance of a missing executable merely because an active Spec proposes
  the path.
- No reintroduction of the retired `route_state` option.
- No relocation of validator tests into `scripts/validation/tests/`.
- No exact approval-sentence roster or source-code exception map for package
  approval.

Spec 0054 work packages outside WP-010 and WP-011 remain with Spec 0054.

## Work Breakdown

| ID | Work package | Depends on | Exit evidence |
| --- | --- | --- | --- |
| WP-001 | Verify the parent-owned activation transaction is complete and capture the validation-tooling baseline before mutation; do not repeat any ADR, README, lifecycle, compatibility-pointer, or delegated-state transition | None | Accepted ADR/README reciprocity, active package-local states, Spec 0066 router and Current Spec Index active-state parity, no foreign parent Plan/Task execution link, no Spec 0066 standalone row, the existing Spec 0054 row pointing to active TSK-0054-0011, completed TSK-0054-0010, focused delegated-ownership test results, and point-in-time baseline evidence |
| WP-002 | Correct current executable-reference validation so extension and depth do not silence it; distinguish current references from Git-first historical recovery and bounded sealed-record exceptions | WP-001 | Focused cases for present, missing, Git-recoverable, and sealed-exception references |
| WP-003 | Atomically move the existing validation-surface JSON and schema to `scripts/validation/registry.*` and update all consumers | WP-002 | No source copy remains; schema passes; identical selection across the move |
| WP-004 | Build or adapt independent behavior tests for ownership duplication, aggregate rule leakage, missing references, orphan fixtures, bounded I/O, subprocess timeout, pin classification, and staged ambiguity | WP-002 | Each behavior fails against its defect and passes after its owner is corrected; no fixed case count |
| WP-005 | Record the point-in-time ownership and disposition in this Task, then remove dead code and classify rules by responsibility | WP-003, WP-004 | Task-local owner/disposition table linked to current paths and diff; no permanent all-file ledger |
| WP-006 | Remove production `--self-test` branches and production dependencies on `tests/` or `tests/fixtures/`; move shared runtime data to a production-owned path when needed | WP-004, WP-005 | Independent tests pass; production import/read sweep is empty for top-level test paths |
| WP-007 | Consolidate or split validator modules by semantic responsibility, eliminate duplicate rule ownership, and promote genuinely shared bounded primitives to `scripts/lib/` | WP-005, WP-006 | One semantic owner per rule; responsibility and duplication evidence for each split or merge |
| WP-008 | Reduce aggregates and domain runners to dispatch/normalization, preserving each responsible validator's diagnostic contract | WP-007 | Aggregate and runner rule-logic scans; focused behavior parity |
| WP-009 | Prove current-consumer-zero and unique-diagnostic-zero for each wrapper or alias, then retire only proven candidates | WP-008 | Per-candidate consumer sweep, diagnostic comparison, and recovery evidence |
| WP-010 | Simplify registry selection, hook invocation, and CI jobs intentionally; preserve required CI check names pending authorized remote verification | WP-003, WP-008, WP-009 | Before/after selected lanes with rationale; duplicate invocation audit; external check names unchanged or separately approved |
| WP-011 | Remove current-state SHA/digest tracking, retain only owned immutable external pins and sealed recovery coordinates, and update validation documentation | WP-005, WP-010 | Pin classification, owner/update-or-recovery evidence, current-state pin sweep |
| WP-012 | Finish implementation and independent review; pass and commit every acceptance-bearing focused and broad gate; obtain Spec 0054 integrated acceptance through TSK-0054-0011; then perform only the Spec 0066 state closure and post-state lifecycle/diff confirmation | All | Committed clean-checkout evidence before acceptance, parent acceptance record, `TSK-0066-0001 in-progress → done`, Plan/Spec `active → done`, and post-state lifecycle/diff PASS |

## Verification Plan

Each work package runs its focused independent tests before the affected and
staged lanes. Changes that touch document governance also run registry,
Markdown, cross-link, and lifecycle validation. Every logical change runs
worktree and staged diff checks.

WP-003 captures the same representative path set immediately before and after
the registry move and requires identical selected validators and unmatched-path
results. WP-010 does not use that equivalence as a permanent constraint; it
records intentional routing differences and proves the resulting lane still
covers the changed responsibility.

WP-001 verifies the parent-owned activation cases in the focused top-level
test module created by TSK-0054-0010. The positive case requires one closed
package-local Spec 0066 Plan/Task component plus reciprocal Spec 0054↔0066
links under accepted ADR-0031. Negative cases cover missing reciprocity,
proposed ADR authority, multiple candidate parents, foreign Plan/Task links,
state mismatch, and a duplicate child standalone row.

WP-012 verifies from a clean checkout at the branch tip. Repository-static
success does not imply hosted CI, branch protection, provider runtime, or live
cluster success.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A move is validated by a rule that cannot see the moved executable | WP-002 establishes extension- and depth-aware current-reference cases before any move |
| Source and target registries diverge during migration | WP-003 is one logical move with all consumers updated and source removal required for completion |
| Routing simplification silently loses coverage | WP-003 requires move-time equivalence; WP-010 records and tests each intentional later difference |
| Production loses behavior when embedded self-tests are removed | WP-004 establishes independent coverage before WP-006 removes each self-test |
| Fixtures become a hidden runtime API | WP-006 forbids production reads from top-level tests and assigns reusable runtime data a production owner |
| Consolidation changes rule meaning | WP-007 uses semantic responsibility and diagnostic behavior, not filenames or line counts, as the boundary |
| A wrapper is removed while a consumer or unique failure remains | WP-009 requires both consumer-zero and unique-diagnostic-zero evidence |
| A required CI check rename blocks merging | WP-010 preserves external check names until remote protection state is verified with authorization |
| Staged validation evaluates worktree state | Focused cases require index-bound selection and fail-closed ambiguity handling |
| A load-bearing immutable pin is removed | WP-011 requires owner and update/recovery evidence before retention or retirement |

## Completion Criteria

Activation occurs only after design review through the parent-owned atomic
transaction described above. That precondition moves Spec and Plan to `active`,
TSK-0066-0001 and TSK-0054-0011 to `in-progress`, and TSK-0054-0010 to
`done`. WP-001 begins only after those states and their focused evidence
exist. No ADR acceptance or activation change is part of this design
checkpoint.

Completion requires all Spec criteria to hold, focused and broad static checks
to pass in a clean checkout, all remaining wrappers and pins to name their
owners, and all intentional routing differences to be explained. All
implementation, independent review, and acceptance-bearing focused, affected,
staged, registry, Markdown, link, lifecycle, aggregate, and diff checks finish
and are committed while TSK-0066-0001 remains `in-progress`. It then publishes
that review-ready evidence. TSK-0054-0011 reviews it, records Spec 0054
integrated acceptance, and remains `in-progress` while Spec 0066 performs a
state-only closure: TSK-0066-0001 moves `in-progress → done`, and its Plan and
Spec move `active → done`. The closure reruns lifecycle and diff checks only to
confirm the terminal states; it does not add implementation or acceptance
evidence. A later parent handoff atomically moves TSK-0054-0011 to `done` and
the existing Spec 0054 compatibility pointer to queued TSK-0054-0013. Only a
subsequent lifecycle-valid change may activate TSK-0054-0013.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-VTO-001](spec.md#success-criteria--verification-plan) | WP-001, WP-012 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-002](spec.md#success-criteria--verification-plan) | WP-003 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-003](spec.md#success-criteria--verification-plan) | WP-003, WP-010 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-004](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-005](spec.md#success-criteria--verification-plan) | WP-005, WP-007, WP-008 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-006](spec.md#success-criteria--verification-plan) | WP-004, WP-006 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-007](spec.md#success-criteria--verification-plan) | WP-009 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-008](spec.md#success-criteria--verification-plan) | WP-004, WP-007, WP-012 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-009](spec.md#success-criteria--verification-plan) | WP-005, WP-011 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-010](spec.md#success-criteria--verification-plan) | WP-010 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-011](spec.md#success-criteria--verification-plan) | WP-012 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |

### Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-vto-000.md)
- [Proposed ADR-0031](../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
- [Current Spec Index](../README.md#current-spec-index)
- Parent acceptance boundary: `SPEC-0054`, `WP-010`, `WP-011`,
  `TSK-0054-0010`, and `TSK-0054-0011`; the reciprocal rendered relation is
  owned by this package's Spec rather than a foreign Plan/Task execution link.
