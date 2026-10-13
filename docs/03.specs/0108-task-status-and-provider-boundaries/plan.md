---
title: "Task Status Derivation and Provider Boundaries Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0108-PLAN-0001"
parent_ids: ["SPEC-0108"]
---

# Task Status Derivation and Provider Boundaries Implementation Plan

## Global Constraints

- Preserve recorded Task status and frozen Archive bodies; derive, never
  rewrite.
- Keep every Claude denial other than the four requested ask entries.
- Validate each logical commit on its exact index; no retired full/ci sweep.
- Push, pull request and merge remain the user's decisions.

## Overview

This plan executes [SPEC-0108](spec.md) in three logical commits on branch
`feat/task-summary-roles-ko` from main `57f44c4446e9ad0e9c8ae87e81c1d208aa7f3c8b`,
followed by the Task record.

## Context

All earlier Specs (0105–0107) are completed, so no open package owned this
scope. A read-only consumer map found that `document_from_text` gates every
lifecycle reader, while the profile and link validators read frontmatter
status directly. Three of 27 current Tasks are multi-row and all keep a
status that already equals their derivation.

## Goals & In-Scope

- Derive an omitted multi-row Task summary in every reader and retire the
  explicit writer.
- Let provider-root READMEs follow their Korean-first profile and translate
  the roles router.
- Move four remote Git and GitHub commands to the Claude ask list.

## Non-Goals & Out-of-Scope

Translation of the eight pending READMEs, the shared memory store
([SPEC-0109](../0109-shared-workspace-memory/spec.md)), Codex native
configuration and the remaining v9 phases. (SPEC-0113 note, 2026-10-13:
SPEC-0110 later translated the eight READMEs.)

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TSKSUM-002](spec.md#success-criteria--verification-plan) | README language exception, pending list and Korean roles router | None | [Task](tasks/tsk-0001-task-status-and-provider-boundaries.md) | Language tests, profile validator and staged QA |
| WORK-002 | [VAL-TSKSUM-003](spec.md#success-criteria--verification-plan) | Claude ask list and exact permission validation | None | [Task](tasks/tsk-0001-task-status-and-provider-boundaries.md) | Governance tests, governance validator and staged QA |
| WORK-003 | [VAL-TSKSUM-001](spec.md#success-criteria--verification-plan) | Shared Task status reader, optional profile key and writer retirement | WORK-001 | [Task](tasks/tsk-0001-task-status-and-provider-boundaries.md) | Task contract and derivation tests, validators and staged QA |

## Verification Plan

Each work unit records a focused failing case before repair and its passing
result, then `python3 scripts/qa.py staged` on the exact index before its
commit. Pre-existing failures on the clean base are recorded separately and
are not attributed to this package.

## Risks & Mitigations

- An omitted status could silently disable an enforcement path: every
  reader calls the one helper, and an unreadable table fails as missing.
- Removing `status` from the global schema could loosen other profiles:
  their Registry key sets still require it.
- A widened permission: the validator compares the complete permission
  mapping.

## Completion Criteria

All three criteria have concrete PASS evidence and one accepted decision in
the Task; push, pull request, hosted CI and native prompt observation are
recorded as separate, unexecuted lanes unless the user runs them.
