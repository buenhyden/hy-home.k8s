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

- `docs/00.agent-governance/contracts/validation-surfaces.json` is read, not
  rewritten. A move that requires editing it is out of contract.
- No validator's failure semantics change, and no declared `argv` loses
  `--self-test`.
- The corrected reference rule must not require a path named inside a sealed
  Stage 98 record to exist in the current tree.
- Every commit is one logical unit and reverts on its own.
- Evidence is repository-static. It does not prove native discovery, hook
  delivery, authenticated provider runtime, CI, or live cluster readiness.

## Overview

Execute SPEC-0066. The end state is one role-first tree under `scripts/` with a
mirrored `tests/`, one owner per case table, one module-loading convention per
tree, no tracked file over the 800-line ceiling, and a reference rule that
reaches every executable at every depth.

## Context

Measured on the current tree at `b6a310d2`:

| Fact | Value |
| --- | --- |
| Tracked files under `scripts/` | 48 — 31 CLI, 7 library, 10 other |
| Count `scripts/README.md` reasons over | 8 |
| Files over the 800-line ceiling | 23 under `scripts/`, 14 under `tests/` |
| Largest | `reference_information_architecture.py` 8,042; `test_reference_information_architecture.py` 5,770 |
| Production modules reading `tests/fixtures/` | 13 |
| Modules carrying `--self-test` | 13 |
| Module-loading conventions | 3 in `scripts/` (bare 22, `scripts.` 12, importlib 10); 3 in `tests/` (importlib 24, `sys.path` 17, `scripts.` 5) |
| `__init__.py` | absent in both trees |
| Repository-internal 40-character pins | 77 in `scripts/`, 27 in `tests/` |
| Declared validators | 23, none optional |
| Scripts absent from any declared `argv` | 24 |

Two facts were established by execution before this Plan was written. The
reference regex matches one of four sample references, missing every
subdirectory path and every `.py` path. The surface selector returns an
identical sixteen-validator set for the proposed paths and for the current
paths, with `unmatchedPaths` empty.

## Goals & In-Scope

Correct the two reference rules; restate `scripts/README.md` over all forty-eight
files; move modules into the role-first tree; give case tables one owner; unify
the loader conventions; split every file over the ceiling; classify and retire
the commit pins; reconcile the declared and executed validator sets.

## Non-Goals & Out-of-Scope

Reducing the `scripts` surface fan-out from sixteen validators is investigated
and recorded, not executed — its declared fallback makes it an authority
decision. `scripts/document-taxonomy-migration.json` is not deleted; three
validators read it as an authority table. `migrate-document-work-units.py` is not
deleted until its two remaining consumers are promoted to `lib/`.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Classify all 48 scripts and 31 test modules by role, domain, consumer, and ceiling status; classify all 104 commit pins | None | VAL-VTO-002, VAL-VTO-007 | Classification tables recorded in the Task before any move |
| WP-002 | Correct both script-reference rules to be extension-neutral and depth-aware, resolving moved paths through the sealed record | WP-001 | VAL-VTO-001 | RED case on the current tree, then its passing result |
| WP-003 | Restate `scripts/README.md` over all tracked files; split the inventory, tiers, and command contract into `scripts/docs/` | WP-001 | VAL-VTO-002 | Census matches the governed count |
| WP-004 | Unify the module-loading convention in both trees | WP-001 | VAL-VTO-005 | Loader census before and after |
| WP-005 | Move the 7 library modules to `scripts/lib/` | WP-002, WP-004 | VAL-VTO-003 | Selector output unchanged; suite green |
| WP-006 | Move validators into `scripts/validation/<domain>/`; remove `validation`-to-`validation` imports | WP-005 | VAL-VTO-003, VAL-VTO-009 | Import census empty; selector output unchanged |
| WP-007 | Move case tables to `scripts/validation/cases/`; mirror `tests/` onto the scripts tree | WP-006 | VAL-VTO-004 | No `tests/` path read from `scripts/`; suite green |
| WP-008 | Move runners to `qa/` and generators to `setup/`; reconcile the declared and executed validator sets | WP-006 | VAL-VTO-008 | Declared and executed sets differ by nothing unrecorded |
| WP-009 | Split every file over the 800-line ceiling into responsibility modules | WP-006, WP-007 | VAL-VTO-006 | Line-count census under the ceiling |
| WP-010 | Retire the classified pins; promote the two refused deletion candidates' consumers to `lib/` | WP-001, WP-005 | VAL-VTO-007 | Each retired pin resolved through its sealed record |
| WP-011 | Close: clean-checkout gate and suite at the branch tip | All | VAL-VTO-010 | Recorded gate and suite output |

## Verification Plan

Each work package runs the targeted check for its criterion, then the affected
lane. WP-005 through WP-009 additionally re-run the surface selector and compare
its validator set against the pre-move baseline; an unequal set stops the work
package. WP-011 runs the gate and the full suite in a clean checkout.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A move verified by a silenced rule reports a green that carries no information | WP-002 precedes every move, and its RED case proves the rule can fail |
| The corrected rule requires a sealed record's pinned path to exist now | The Spec names this as the defect Spec 0065 removed in four owners; the rule resolves through the record |
| Splitting a monolith changes failure semantics | Each split is a pure move of definitions with the suite green before and after; no predicate is rewritten in a split commit |
| A partial path update leaves a validator unrunnable | `validate_required_validators_have_a_runner` compares `argv` against runner text by substring and fails loudly |
| A pin retired while still load-bearing | WP-001 classifies every pin before WP-010 retires any |

## Completion Criteria

All ten criteria hold, the gate and the full suite pass in a clean checkout at
the branch tip, and every refused candidate is recorded with its reason. Live,
hosted, provider-runtime, and cluster evidence stays out of scope.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-VTO-001](spec.md#success-criteria--verification-plan) | WP-002 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-002](spec.md#success-criteria--verification-plan) | WP-001, WP-003 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-003](spec.md#success-criteria--verification-plan) | WP-005, WP-006 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-004](spec.md#success-criteria--verification-plan) | WP-007 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-005](spec.md#success-criteria--verification-plan) | WP-004 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-006](spec.md#success-criteria--verification-plan) | WP-009 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-007](spec.md#success-criteria--verification-plan) | WP-001, WP-010 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-008](spec.md#success-criteria--verification-plan) | WP-008 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-009](spec.md#success-criteria--verification-plan) | WP-006 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |
| [VAL-VTO-010](spec.md#success-criteria--verification-plan) | WP-011 | [TSK-0066-0001](tasks/tsk-0001-vto-000.md) |

### Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-vto-000.md)
