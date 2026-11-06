---
title: "Hook-Delivered Folder Agent Rules Plan"
version: "0.1.1"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0149-PLAN-0001"
parent_ids: ["SPEC-0149"]
---

# Hook-Delivered Folder Agent Rules Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Failing tests are written before the guard change.

## Overview

This plan executes [SPEC-0149](spec.md) on branch
`feat/agents-md-hook-context` from `main` at `296e3379`.

## Context

Sources observed 2026-11-06: the Claude Code memory and hooks documentation
(`instructionFiles` ignored in project settings; nested `AGENTS.md` read
only without a `CLAUDE.md`; `systemMessage` shown to the user;
`additionalContext` added to the model context) and the Codex AGENTS.md and
hooks documentation (root-to-cwd chain at session start; PreToolUse
`additionalContext`). Constraining architecture is [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md). Rollback is
reverting the implementing commit.

## Goals & In-Scope

Close VAL-HOOK-001 to VAL-HOOK-003.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-HOOK-001](spec.md#success-criteria--verification-plan) | Tests first, then the guard's chain and model-context output | None | [Task](tasks/tsk-0001-agents-md-hook-context.md) | Tests FAIL then PASS |
| WORK-002 | [VAL-HOOK-002](spec.md#success-criteria--verification-plan) | Observe a Claude write after the change | WORK-001 | [Task](tasks/tsk-0001-agents-md-hook-context.md) | Observed model context |
| WORK-003 | [VAL-HOOK-003](spec.md#success-criteria--verification-plan) | Update the provider notes, `agent-execution.md` and the audit addendum | WORK-001 | [Task](tasks/tsk-0001-agents-md-hook-context.md) | Strict checks and review |

## Verification Plan

Run the focused tests red then green, the hook and guard suites, the strict
checks, `python3 scripts/qa.py staged`, an independent review, and one
observed Claude write. Codex delivery is recorded as DEFER with the reset
date. Architecture compliance check: the change stays in the shared guard and
leaves both thin adapters unchanged, as AD-0006 requires.

## Risks & Mitigations

- A provider may reject the new output field; Claude is observed in-session,
  Codex stays DEFER, and rollback is one commit.
- Context size grows per write; once-per-session supply and a byte bound
  limit it.

## Completion Criteria

VAL-HOOK-001 to VAL-HOOK-003 have PASS evidence and an operator decision.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| The shared guard supplies folder `AGENTS.md` text to the model on writes | [Agent Execution Policy](../../../.agents/governance/agent-execution.md) | Current Contract, the `AGENTS.md` reading rule |
