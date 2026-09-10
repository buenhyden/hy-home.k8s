---
title: "Dead Contract and Duplicate Execution Retirement Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-11"
layer: "specs"
artifact_id: "SPEC-0077-PLAN-0001"
---

# Dead Contract and Duplicate Execution Retirement Implementation Plan (Plan)

## Overview

This Plan orders the retirement work the Spec approves into eight independently
revertible packages. Each package owns one rule, names its files, states its
focused RED/GREEN check, and reverts by its own commit without disturbing the
others.

## Context

The stocktake that produced this package observed `python3 scripts/qa.py full`
at `EXIT=0` with 22 of 22 gates passing over 1,126 paths. Every finding below
is therefore a defect a passing run cannot expose: unreachable code, absent-
subject assertions, same-snapshot re-execution, and authored obligations with
no corpus practice. The sequence starts with the removals whose reachability is
already proven and ends with the prose whose subject those removals settle.

## Goals & In-Scope

Remove code and tests no reachable caller executes. Remove assertions whose
subject is absent from the working tree. Reduce each registered gate to one
execution per identical snapshot. Resolve duplicated helpers to the shared
owner that already exists. Give every registered skill an owning role and a
procedure, and give the recurring archive cutover workflow an owner. Close the
routing and document-boundary gaps the stocktake named.

## Non-Goals & Out-of-Scope

No gate changes the rule it enforces. No document route, profile, template,
artifact identifier or lifecycle edge changes. The documentation link boundary
diagnostic and its regressions are unchanged; only its rule owner gains
rationale. No archive payload or sealed record is edited. No push, PR, merge,
branch cleanup, live cluster, provider runtime or network action is performed.

## Work Breakdown

### WP-001: Retire the unreachable cross-document subtree

| Item | Detail |
| --- | --- |
| Subject | `scripts/validate-links-and-owners.py` holds a diagnostic root with no caller, six children reachable only from it, and the constants they alone consume. `tests/test_delegated_execution_ownership.py` reaches one private child. |
| Owns | `scripts/validate-links-and-owners.py`, `tests/test_delegated_execution_ownership.py` |
| Check | The aggregator's function set is unchanged; a repository-wide sweep finds no reference to the removed root; the cross-document gate result is byte-identical before and after. |
| Rollback | Revert the commit. No rule identifier that a reachable path emits is affected. |

### WP-002: Restore honest test collection

| Item | Detail |
| --- | --- |
| Subject | Two classes in one module do not subclass the collector base class and are never collected; a further group of methods has no caller. One ledger traversal globs a filename shape the corpus does not use and iterates nothing while reporting green. |
| Owns | `tests/test_document_lifecycle_archive_cutover.py`, `tests/test_document_lifecycle_migration.py`, `tests/test_validation_tooling_ownership.py` |
| Check | RED first: assert every module-level class whose name marks it as tests subclasses the collector base, and assert the repaired traversal yields a non-empty sequence. Both fail before the repair. |
| Rollback | Revert the commit; collected test count returns to its prior value. |

### WP-003: Remove absent-subject cutover pins

| Item | Detail |
| --- | --- |
| Subject | The lifecycle gate pins a legacy rehome map whose keys live under an absent directory, and a work-package path set naming an absent contract file, together with a base commit those assertions require. Paired tests import the constants. |
| Owns | `scripts/validate-document-lifecycle.py`, `tests/test_document_lifecycle_archive_cutover.py` |
| Check | The lifecycle gate result is unchanged on the current tree; the removed constants have no remaining importer. |
| Rollback | Revert the commit. Git history remains the recovery source for the frozen subjects. |

### WP-004: Stop re-running registered gates inside the unit-test gate

| Item | Detail |
| --- | --- |
| Subject | Assertions that a registered validator passes over the repository re-execute that gate inside `unit-tests` on the same snapshot. One module exists only for that purpose. |
| Owns | the pass-through assertions in their modules, `tests/README.md` if its statement needs no change, and `tests/test_validation_tooling_ownership.py` for the guard |
| Check | RED first: a guard that fails when a test invokes a registered validator against the repository root. Then remove the assertions until it passes. Synthetic coverage in the same modules is unchanged. |
| Rollback | Revert the commit; the gate list and every gate verdict are unchanged either way. |

### WP-005: Resolve duplicated helpers to the shared owner

| Item | Detail |
| --- | --- |
| Subject | Front-matter parsing, Markdown link parsing, bounded process invocation and unique-mapping construction are each implemented several times while a shared bounded-input owner already exists. |
| Owns | the duplicating modules under `scripts/`, `scripts/validation/repository/bounded_io.py` only if the shared owner needs no change |
| Check | Each converted call site keeps its existing focused test green; the shared owner's bounded-input tests stay green; no new abstraction is added. |
| Rollback | Revert the commit; call sites return to their local helpers. |

### WP-006: Consolidate the skill roster and admit the archive cutover skill

| Item | Detail |
| --- | --- |
| Subject | Two skills are halves of one procedure under one owning role; one skill concedes its severity mapping to a sibling; one mandates a marker no runbook uses; one embeds templates Stage 99 owns. The recurring archive cutover workflow has tooling and Stage 99 profiles but no owning skill. |
| Owns | `.agents/skills/`, `.agents/roles/registry.json`, `.claude/skills/`, `.claude/agents/`, `.codex/agents/` |
| Check | The governance gate resolves every skill reference from the registry; both provider projections match the registry exactly; the admitted package satisfies the skill package shape. |
| Rollback | Revert the commit; the roster returns to its prior membership atomically. |

### WP-007: Close routing and boundary gaps

| Item | Detail |
| --- | --- |
| Subject | The routing registry still routes an absent stage while a quality rule fails if that stage appears; the evaluation root is outside the document target roots although a registry path pattern names its index; one output mode, one selector lane and three declared lanes have no production consumer. |
| Owns | `scripts/validation/registry.json`, `scripts/document_contracts.py`, `scripts/validation/repository/quality.py`, `scripts/select-affected-surfaces.py`, `scripts/validate-affected-surfaces.py` and their focused tests |
| Check | RED first for the evaluation root: the contract validator reports the evaluation index as covered only after the root is added. Routing and selector removals keep the affected-surface contract green. |
| Rollback | Revert the commit; routing and coverage return to their prior values. |

### WP-008: Record the documentation link boundary rationale

| Item | Detail |
| --- | --- |
| Subject | The rule owner states the boundary but not why a stage index is excluded, so a future reader may read the exclusion as an oversight. |
| Owns | `.agents/governance/document-authoring.md` |
| Check | The boundary diagnostic and its regressions are untouched and stay green; the rule owner names the hub as the single external entry point. |
| Rollback | Revert the prose commit; no behavior is involved. |

## Verification Plan

Each package runs its named focused check first in a failing state where the
package declares RED, then in a passing state. After each package, staged QA
runs over the exact index for that logical commit. `full` runs once on the
final working tree; its unit discovery and pre-commit stage are not repeated
under another command name. Hosted evidence for the same profile is observed
separately or recorded as DEFER.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A removal has a consumer the sweep missed | The consuming gate fails closed; revert the single package rather than repairing forward |
| A constant and its importing test are separated | Each constant moves in the same logical unit as its importer |
| A skill removal leaves a dangling registry reference | Registry, both projections and the package move atomically under the governance gate |
| Removing a pass-through also removes synthetic coverage | Deletions are bounded to the named method or class and the module's remaining tests stay green |
| The suite's collected test count changes silently | WP-002 adds the collector-shape guard before any other package runs |

## Completion Criteria

Every Spec criterion has named evidence in the owning Task, `full` returns the
same verdict as the recorded baseline, `git diff --check` is clean, each
package is one reverted-alone commit, and hosted evidence is either observed
or recorded as DEFER with its reason.

## Traceability

The [Spec](spec.md) owns the approved contract and criteria. The
[retirement Task](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md)
owns ordered execution evidence and the handoff record.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DCR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-004](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-005](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-006](spec.md#success-criteria--verification-plan) | WP-006 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-007](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
| [VAL-DCR-008](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-retire-dead-contracts-and-duplicate-execution.md) |
