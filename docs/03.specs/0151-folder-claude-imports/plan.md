---
title: "Folder CLAUDE.md Imports Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0151-PLAN-0001"
parent_ids: ["SPEC-0151"]
---

# Folder CLAUDE.md Imports Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Failing tests are written before the check and guard changes.
- The secret-scan baseline line move is committed first
  (`docs/99.templates/AGENTS.md` rule 6).

## Overview

This plan executes [SPEC-0151](spec.md) on branch
`feat/folder-claude-imports` from `main` at `8be06a16`.

## Context

The Claude Code memory documentation (read 2026-11-06) states nested
`CLAUDE.md` loading on read, write and edit, on-demand reload after a
compaction, and relative `@path` imports. Constraining architecture is
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Rollback is reverting the implementing commits.

## Goals & In-Scope

Close VAL-CLI-001 to VAL-CLI-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CLI-001](spec.md#success-criteria--verification-plan) | Tests first, then the pairing check and the Codex-only folder chain | None | [Task](tasks/tsk-0001-folder-claude-imports.md) | Tests FAIL then PASS |
| WORK-002 | [VAL-CLI-002](spec.md#success-criteria--verification-plan) | Add the files, the profile and the documentation | WORK-001 | [Task](tasks/tsk-0001-folder-claude-imports.md) | Strict checks and staged QA |
| WORK-003 | [VAL-CLI-003](spec.md#success-criteria--verification-plan) | Observe a read-only new Claude session | WORK-002 | [Task](tasks/tsk-0001-folder-claude-imports.md) | Observed context |

## Verification Plan

Run the focused tests red then green, the quality and hook suites, the
strict checks, `python3 scripts/qa.py staged`, an independent review and
one new Claude session. Architecture compliance check: Claude uses its native
loading, Codex keeps the shared guard, and the profile lives in the Stage 99
registry, as AD-0006 requires.

## Risks & Mitigations

- If the installed client does not load the folder files, WORK-003 fails and
  the guard change is reverted before merge.

## Completion Criteria

VAL-CLI-001 to VAL-CLI-003 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Each folder `AGENTS.md` has a sibling `CLAUDE.md` importing it | [Agent Execution Policy](../../../.agents/governance/agent-execution.md) | Current Contract, the `AGENTS.md` reading rule |
