---
title: 'Task: Current corpus and transition-control cutover'
type: sdlc/task
status: queued
owner: platform
updated: 2026-08-31
artifact_id: "TSK-0054-0013"
---

# Task: Current corpus and transition-control cutover

## Overview

This is the queued Task record for the remaining Stage 01, 02, 03, and 99
current-corpus convergence and transition-control retirement in WP-013. Named
dispositions are execution candidates, not permanent corpus-count policy.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-013 execution boundary](../plan.md#wp-013--current-corpus-and-transition-control-cutover)

## Task Table

**Plan label:** WP-013

**Depends on:** WP-012; accepted ADR-0031; accepted and completed Spec 0066
result with TSK-0066-0001, Plan 0066, and Spec 0066 all `done`; completed
TSK-0054-0011 parent handoff; and the existing Spec 0054 compatibility pointer
naming this queued Task

**Current state:** `queued`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-013 | VAL-SDLC-001..VAL-SDLC-004, VAL-SDLC-006, VAL-SDLC-009..VAL-SDLC-012 | After the completed child and parent handoffs, converge the reviewed Stage 01/02/03/99 current-owner set, transfer unfinished work and unique authority, then retire residual transition assets against the accepted and completed Spec 0066 routing result without a fixed corpus census. | platform | Queued | Not executed. | Terminal Spec 0066 states, completed TSK-0054-0011, compatibility pointer to this queued Task, consumer/trace/lifecycle parity, Git-first recovery, registry/template parity, delegated routing evidence, and ordered logical commits |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-013 may remove a current document or template only after
its unique authority and unfinished work are transferred or proven absent,
current consumers are zero, and Git-first recovery succeeds. The linked Plan
owns the exact candidate dispositions, reviews, rollback, and four ordered
logical commits: Stage 01/02, Stage 03, Stage 99, then transition controls. The
accepted and completed Spec 0066 result plus the completed TSK-0054-0011
parent handoff are fixed dependencies; their execution does not overlap the
final WP-013 validation-side transition-control unit. This Task cannot activate
until the existing Spec 0054 compatibility pointer already names it while it is
still `queued`.
Each unit is independently validated and can stop before the next unit without
rolling back an already accepted predecessor unit.

## Verification Summary

WP-013 is queued and has no accepted execution evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-013](../plan.md#wp-013--current-corpus-and-transition-control-cutover) | Queued. | No accepted execution evidence yet. |
