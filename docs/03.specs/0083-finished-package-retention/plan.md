---
title: "Finished Package Retention Implementation Plan"
version: "0.3.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0083-PLAN-0001"
---

# Finished Package Retention Implementation Plan (Plan)

## Global Constraints

No contract, registry, or citation-table changes, and no frozen rewrite. The
request owner authorized repairing the consumers the retention proved wrong,
including `scripts/` and `tests/`, rather than reverting it. Push, pull request,
and merge stay with the request owner. Each logical commit runs staged
QA over its exact index, and the final tree runs one full QA.

## Overview

This Plan executes [Spec 0083](spec.md) in one integration: record the surveys,
record the blocked pair, repoint consumers, retain ten units, record the
disposition of every package that stays, and close.

## Context

[SPEC-0082](../../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md) built and proved
the unit retention machinery on ADR-0038. This round applies it to Stage 03
packages, which are tree units rather than single documents.

## Goals & In-Scope

Retain ten finished packages in `completed/`, each as one exact unit with one
catalog row, with every consumer moved first; record why the two superseded
proposals cannot follow; and record the observed disposition of every Stage 03
package that stays.

## Non-Goals & Out-of-Scope

No retention of SPEC-0068 or SPEC-0070, no change to any contract or gate, no
disposition of a package with a non-terminal member, and no decision on any
package that stays; its state is recorded and returned to the request owner.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Propose this package and record the survey of the nine units | None | The request owner approved the round | The Task records each unit, its anchor state, and its consumers |
| WP-002 | Record the contract conflict that blocks SPEC-0068 and SPEC-0070 and return it to the request owner | WP-001 | The survey named both as `superseded/` candidates | The Task carries both observed diagnostics, the successor their bodies name, and the owning contract |
| WP-003 | Repoint every current consumer of the seven retained units | WP-002 | The survey lists them | Link gate over the whole corpus |
| WP-004 | Retain the seven finished packages in `completed/` with one catalog row each | WP-003 | Consumer zero | Lifecycle and archive gates |
| WP-005 | Re-verify every Retention Catalog row in the full lane, including the seven rows this round adds | WP-004 | The seven retentions are staged | Archive cutover re-verification and full QA |
| WP-006 | Record the results and close this package | WP-001 to WP-005, WP-007 | Full QA on the final tree | Staged and full QA |
| WP-007 | Record the observed disposition of every Stage 03 package that stays | WP-004 | The retained units have left the stage | The Task records each remaining package, its anchor state, and the reason it stays |
| WP-008 | Repair every consumer the retention proved wrong, in documents, validators and the test budget | WP-004 | Full QA named the failing gates | Full QA and the whole unit-test suite pass with no pin lowered |

## Verification Plan

Each work package runs its focused checks first: the link gate for repointing,
`python3 scripts/run-archive-contract-tests.py --root .` for the retention
contract, and `python3 scripts/qa.py staged` for each logical commit. The final
tree runs one `python3 scripts/qa.py full`. Hosted results are recorded only
when observed.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A moved package leaves a broken link in the Stage 98 index | The index is an archive source; its links move to the retained path in the same change |
| A consumer cites a `superseded/` body, which the citation table rejects | No `superseded/` body is added in this round, so no consumer moves onto one |
| A package member is not terminal | The survey checks every member before the move, and such a package stays |
| Seven moves in one change hide a mistake | One commit per disposition class, with staged QA over each exact index |
| A retention is wrong after merge | Retention is frozen; a correction needs its own decision, which the Task states |

## Completion Criteria

WP-001 to WP-006 pass their exit evidence, every frozen file is unmodified, and
the final tree passes staged and full QA.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-FPR-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-003](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-004](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-005](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-006](spec.md#success-criteria--verification-plan) | WP-006 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-007](spec.md#success-criteria--verification-plan) | WP-007 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
| [VAL-FPR-008](spec.md#success-criteria--verification-plan) | WP-008 | [tsk-0001](tasks/tsk-0001-retain-finished-packages.md) |
