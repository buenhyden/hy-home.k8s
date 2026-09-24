---
title: "Provider Native Runtime Observation Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0086-PLAN-0001"
---

# Provider Native Runtime Observation Implementation Plan

## Global Constraints

No agent may authorize, simulate, or infer the native session on the
operator's behalf. No repository-static or hosted-CI result may be promoted
to runtime evidence. No new registry, contract file, gate, or permission
change is authorized by this Plan; a defect found during observation is
recorded and routed to its own owner rather than fixed inline.

## Overview

Execute [Spec 0086](spec.md): obtain one operator-authorized native session
per provider (Claude, Codex) and record discovery, invocation/model-access,
sandbox/permission enforcement, and hook event-delivery results against the
Spec's eight criteria.

## Context

SPEC-0072's Task recorded `WORK-009` as the one remaining open item after its
static acceptance was complete: an operator-authorized native session that no
repository-static run can supply. SPEC-0072 closed on 2026-09-24 with that
deferral transferred to this package rather than claimed as passed. This Plan
does not repeat SPEC-0072's static work; it owns only the native observation.

## Goals & In-Scope

- Obtain one operator-authorized Claude session and one operator-authorized
  Codex session.
- Record discovery, invocation/model-access, sandbox/permission enforcement,
  and hook event-delivery results for each provider.
- Record any defect found during observation with a named owner, without
  fixing it inline in this package.

## Non-Goals & Out-of-Scope

- Any governance, QA, or gate consolidation behavior change; that scope
  stays with SPEC-0072 and its successors.
- Any live infrastructure, credential, or provider account action.
- Widening any role's permission class or sandbox mode.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Obtain an operator-authorized Claude session and observe discovery, invocation, sandbox enforcement, and event delivery | Operator authorization | This package is active | Dated Task record for VAL-PNRO-001, 003, 005, 007 |
| WP-002 | Obtain an operator-authorized Codex session and observe the same four properties | Operator authorization | This package is active | Dated Task record for VAL-PNRO-002, 004, 006, 008 |
| WP-003 | Close this package with observed results only | WP-001, WP-002 | Both sessions observed or explicitly declined | Task and package close with no static-to-runtime promotion |

## Verification Plan

Each work package's only verification is the dated, attributed session record
itself; no repository-static command substitutes for it. A declined or
unavailable session is recorded as `DEFER` with the operator named as next
owner rather than left unrecorded.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| An agent promotes static configuration as if it were runtime evidence | This Plan and its Task explicitly forbid that promotion; every criterion requires a dated session record |
| The operator is unavailable | Record `DEFER` with the operator as next owner rather than stalling the package in an ambiguous state |
| A defect is found during observation | Record it with a named owner and route it to its own package; do not fix it inline here |

## Completion Criteria

Both providers are observed against all eight criteria, or each unobserved
criterion is recorded `DEFER` with the operator as next owner. No criterion is
closed on repository-static or hosted-CI evidence alone.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-PNRO-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-003](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-005](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-007](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-002](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-004](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-006](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
| [VAL-PNRO-008](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-observe-provider-native-runtime.md) |
