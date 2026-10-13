---
title: "Provider Native Permission and Hook Hardening Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0114-PLAN-0001"
parent_ids: ["SPEC-0114"]
---

# Provider Native Permission and Hook Hardening Implementation Plan

## Global Constraints

- Never remove an existing Claude deny entry or admit a wildcard allow.
- A native file, its validator constant and its rejection test change in
  the same commit.
- No live cluster, Vault, Argo CD or remote mutation; probes use dry-run
  or missing targets only.

## Overview

This plan executes [SPEC-0114](spec.md) on branch
`feat/claude-permission-hardening` from main `3897353e`.

## Context

Deny and guard work lands before the allow change, so no allowed command
is exposed by a gap that a later unit closes.

## Goals & In-Scope

Close the nine criteria of the Spec.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PERM-001](spec.md#success-criteria--verification-plan) | Claude secret read and secret-output denies | None | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Governance tests, validator and staged QA |
| WORK-002 | [VAL-PERM-002](spec.md#success-criteria--verification-plan) | Claude option-first cluster and tool mutation denies | WORK-001 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Governance tests, validator and staged QA |
| WORK-003 | [VAL-PERM-003](spec.md#success-criteria--verification-plan) | Claude deletion and history-destroying denies | WORK-002 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Governance tests, validator and staged QA |
| WORK-004 | [VAL-PERM-005](spec.md#success-criteria--verification-plan) | Fail-closed shared guard and adapters | WORK-003 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Failing then passing guard tests and staged QA |
| WORK-005 | [VAL-PERM-004](spec.md#success-criteria--verification-plan) | Claude allow, ask and bypass mode | WORK-004 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Governance tests, validator and staged QA |
| WORK-006 | [VAL-PERM-006](spec.md#success-criteria--verification-plan) | Codex config security keys | WORK-005 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Governance tests, client acceptance and staged QA |
| WORK-007 | [VAL-PERM-007](spec.md#success-criteria--verification-plan) | Codex forbidden rules | WORK-006 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Execpolicy check, validator and staged QA |
| WORK-008 | [VAL-PERM-008](spec.md#success-criteria--verification-plan) | Codex hook path independent of the session directory | WORK-004 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Failing then passing hook test and staged QA |
| WORK-009 | [VAL-PERM-009](spec.md#success-criteria--verification-plan) | Provider notes, READMEs, REQ-0003 links and session probes | WORK-008 | [Task](tasks/tsk-0001-provider-permission-hardening.md) | Probe record, document validators and staged QA |

## Verification Plan

Each unit first adds a test that fails on the current file, then changes
the native file and validator, runs the governance and guard tests and
`qa.py staged` from the validation environment on the exact index. WORK-009
records the refusals observed in a session.

## Risks & Mitigations

- A broad deny can block routine work: each pattern targets one escape,
  and blocked harmless commands are recorded for later narrowing.
- Settings or rules may not reload in a running session: probes record
  whether a new session was needed.
- Codex rules are experimental: the Task records the client version that
  accepted them.

## Completion Criteria

All nine criteria have PASS evidence and an accepted decision in the Task;
push, pull request and merge remain operator-requested actions.
