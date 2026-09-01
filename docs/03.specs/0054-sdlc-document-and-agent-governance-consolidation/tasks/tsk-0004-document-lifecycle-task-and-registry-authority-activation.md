---
title: 'Task: Document lifecycle, Task, and registry authority activation'
type: sdlc/task
status: done
owner: platform
updated: 2026-08-28
artifact_id: "SPEC-0054-TSK-0004"
---

# Task: Document lifecycle, Task, and registry authority activation

## Overview

This Task records the completed WP-004 document authority cutover. WP-003 now
consumes its registry, profile lifecycle, Task topology, and recovery boundary.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-004 execution boundary](../plan.md#wp-004--document-lifecycle-task-and-registry-authority-activation)

## Task Table

**Plan label:** WP-004

**Depends on:** WP-002

**Current state:** `done`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-004 | VAL-SDLC-001..VAL-SDLC-006, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Activate flat Requirement Packages, prefix-free Architecture, Spec Task packages, profile lifecycles, Stage 99 document authority, generic recovery, and responsibility-oriented document validators. | platform | Done | WP-004A/B/C and their independent review fixes are complete; WP-003 is unblocked. | Authority `bdb1031f..211e167f`; corpus `a3b1dafd..7a770c3c`; templates and final fixes `a8bc8c0b..bb55a1ae`; sealed MIG-0004 |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-004's exact cutover files, validation commands, reviews,
rollback, and three ordered logical commits are owned by its linked Plan
section.

## Verification Summary

- Registry, strict Markdown/link ownership, staged lifecycle, affected-surface,
  and MIG-0004 recovery checks passed at the WP-004 handoff. The final staged
  required suite passed 308 tests; later sealed-target and Task-route fixes
  passed their focused regressions and relevant production checks.
- Independent code, Python, and security reviews closed their Critical and
  Important findings; the final whole-WP review approved the cutover through
  `bb55a1ae`.
- The full quality wrapper still reported WP-003-owned
  `AGQC-LEGACY-CONSUMER` for a retired harness-map token in the historical
  progress record. This is an explicit successor obligation, not a WP-004
  full-wrapper PASS. Historical progress was not rewritten to hide it.
- [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
  retains the exact sealed source/target recovery proof. No runtime, hosted CI,
  deployment, push, or merge result is claimed.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-004](../plan.md#wp-004--document-lifecycle-task-and-registry-authority-activation) | Done. | Three authority/corpus/template units and forward review fixes through `bb55a1ae`; production document/recovery gates and independent reviews passed, with the inherited WP-003 legacy-consumer obligation stated above. |
