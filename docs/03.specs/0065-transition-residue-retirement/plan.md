---
title: 'Transition Residue Retirement Implementation Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-08-31
artifact_id: "SPEC-0065-PLAN-0001"
---

# Transition Residue Retirement Implementation Plan (Plan)

## Overview

This plan sequences the three retirements designed in [Spec 0065](spec.md). The
order is set by dependency: the independent retirement runs first so that a
failure in the shared one cannot be confused with it, and the Stage 99 release
precedes the deletion it admits.

## Context

Measured on 2026-08-30 at `eb68a4fe`, the tip of the Spec 0054 WP-012 work:

| Measure | Value |
| --- | --- |
| `Registry` dataclass fields | 5, none named `route_state` |
| `route_state` branches in the link validator | 10 |
| Functions returning early on `!= "transition"` | 5 |
| 40-hex pins in `IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS` | 12 |
| 40-hex pins in `scripts/` | 126 |
| Registry profiles routing zero paths after WP-012 | 1 (`governance/progress-ledger`) |
| Documents under `docs/00.agent-governance/memory/` | 1, its own README |

## Goals & In-Scope

Retire the transition-only alias and handoff machinery, release the `MIG-0004`
Stage 99 current-inventory requirement for targets a later sealed row retires,
and retire the two governance forms, the three profiles that route them, and the
Stage 00 memory directory.

## Non-Goals & Out-of-Scope

No change to `_document_taxonomy_transition_manifest` or
`scripts/document-taxonomy-migration.json`, which own a live redirect
projection. No change to the `MIG-0004` row census, Stage 99 action-target map,
or any constant that proves a move. No change to any other governance profile,
template, or Stage 00 directory.

## Global Constraints

Every work package ends with the gates and the full suite green. Freeze source
files for the duration of a suite run: the archive owner loads its sibling link
validator from disk at call time, so a mid-run edit pairs mismatched modules.
Stage every edit before running a validator: the `MIG-0004` proof requires
index and worktree parity across Stage 01 to Stage 03 Markdown, so an unstaged
edit fails the whole repository's recovery proof.

## Work Breakdown

| ID | Work | Depends on | Exit |
| --- | --- | --- | --- |
| WP-001 | Classify every candidate against its machine fact and record the table in the Task | — | VAL-TRR-001 recorded and approved |
| WP-002 | Retire the transition-only alias and handoff machinery | WP-001 | VAL-TRR-002; suite green |
| WP-003 | Release the Stage 99 current-inventory requirement, RED first | WP-001 | VAL-TRR-003; suite green |
| WP-004 | Extend and seal MIG-0008, delete both forms, retire three profiles and the memory directory | WP-003 | VAL-TRR-004, VAL-TRR-005; suite green |
| WP-005 | Clean-checkout verification and handoff | WP-002, WP-004 | VAL-TRR-006 |

### WP-002 — transition-only machinery

Retire `_archive_transition_handoff`, `_reviewed_stage90_move_edges`,
`_reviewed_source_pinned_alias_edges`, `_reviewed_immutable_historical_alias_edges`,
`_immutable_historical_redirects`, `IMMUTABLE_HISTORICAL_ALIAS_SOURCE_BLOBS`,
and the branches that run only when the route state equals `"transition"`.
Collapse the two `== "terminal"` guards, which are always taken, rather than
deleting the bodies they guard.

### WP-003 — Stage 99 target release

Add a failing case: a Stage 99 target retired by a later sealed row is absent,
and `_validate_mig0004_rows_and_targets` refuses it. Then release the
requirement for exactly that case, leaving `validate_mig0004_historical_targets`
and the row census untouched. Add the narrowing case: a Stage 99 target with no
retiring row is still required to be present.

### WP-004 — forms, profiles and directory

Extend draft `MIG-0008` with the `memory.template.md` row, seal it, and delete
both forms in the same commit, because a sealed row whose legacy path is still
present is refused. Retire `governance/progress-ledger`,
`governance/progress-entry`, and `governance/memory` from the registry, and
generalize the append-template parity rule, which names the retired profile by
identity. Remove `docs/00.agent-governance/memory/` and repoint anything that
cited its README to `policies/context-and-memory.md`.

## Verification Plan

Per work package: the affected or staged validation lane, `pre-commit run`
against the staged index, and the direct suites the change touches. At the
branch tip, in a clean clone: the repository quality gates and the full
`unittest` suite, by the command CI runs.

Repository-static evidence only. No CI, provider-runtime, remote, or live
result is produced or claimed.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A released Stage 99 target loses real protection | The release is scoped to targets a sealed row retires; a narrowing test holds the unretired case |
| A `route_state` branch is reachable after all | The condition is proved from the `Registry` dataclass fields, not from call-site inspection |
| Retiring a profile leaves a path unrouted | The registry validator reports `uncovered` and is run on every staged change |
| A deletion breaks an inbound link from a terminal document | The link validator is run before the deletion is committed, not after |

## Completion Criteria

All six Spec criteria met, or any unmet criterion recorded in the Task with the
clause that refuses it. Gates and the full suite green in a clean checkout at
the branch tip.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-TRR-001](spec.md#success-criteria--verification-plan) | WP-001 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
| [VAL-TRR-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
| [VAL-TRR-003](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
| [VAL-TRR-004](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
| [VAL-TRR-005](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
| [VAL-TRR-006](spec.md#success-criteria--verification-plan) | WP-005 | [SPEC-0065-TSK-0001](tasks/tsk-0001-trr-000.md) |
