---
title: "SDLC Document Sync and Remaining v9 Gaps Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0113-PLAN-0001"
parent_ids: ["SPEC-0113"]
---

# SDLC Document Sync and Remaining v9 Gaps Implementation Plan

## Global Constraints

- Keep completed history; add dated successor notes only.
- No Stage 99 schema, validator constant or workflow change.
- Never loosen a test or remove original-text protection.

## Overview

This plan executes [SPEC-0113](spec.md) on branch
`docs/sdlc-sync-and-v9-gaps` from main `86daf815`.

## Context

The operator chose to reorder `AGENTS.md` sections for F02. The
investigations found the other gaps narrow and the F39 selection free of
duplicates and of misrouted README changes.

## Goals & In-Scope

Close the six criteria of the Spec.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SYNC-001](spec.md#success-criteria--verification-plan) | Correct stale requirements, architecture and Spec text | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Document validators and staged QA |
| WORK-002 | [VAL-SYNC-002](spec.md#success-criteria--verification-plan) | Frozen-exclusion cross-check test and fix recipe | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Failing then passing test and staged QA |
| WORK-003 | [VAL-SYNC-003](spec.md#success-criteria--verification-plan) | Four F05 claim statuses in the Stage 99 README | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Document validators and staged QA |
| WORK-004 | [VAL-SYNC-004](spec.md#success-criteria--verification-plan) | F18 evidence correction | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Document validators and staged QA |
| WORK-005 | [VAL-SYNC-005](spec.md#success-criteria--verification-plan) | Remove the stale `.hadolint.yaml` route | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Validation registry tests and staged QA |
| WORK-006 | [VAL-SYNC-006](spec.md#success-criteria--verification-plan) | `AGENTS.md` common and Codex-only blocks | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Governance validator, tests and staged QA |
| WORK-007 | [VAL-SYNC-007](spec.md#success-criteria--verification-plan) | Bound the memory store Git call with a timeout | None | [Task](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) | Failing then passing tooling test, store tests and staged QA |

## Verification Plan

Each work unit runs its focused check and `qa.py staged` from the
validation environment on the exact index before its commit.

## Risks & Mitigations

- Editing approved or completed documents could trip lifecycle checks: the
  fallback in the Spec moves the note to a current owner.
- An exclusion test could freeze a legitimate future change: it compares
  against the Registry, which remains the owner.

## Completion Criteria

All six criteria have PASS evidence and an accepted decision in the Task;
push and pull request remain operator actions.
