---
title: 'Task: Stage 90 ownership cutover'
type: sdlc/task
status: in-progress
owner: platform
updated: 2026-08-31
artifact_id: "TSK-0054-0008"
---

# Task: Stage 90 ownership cutover

## Overview

This is the sole active Spec 0054 Task record for WP-008.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-008 execution boundary](../plan.md#wp-008--stage-90-ownership-cutover)

## Task Table

**Plan label:** WP-008

**Depends on:** WP-007

**Current state:** `in-progress`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-008 | VAL-SDLC-008, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Preserve the approved current Research pack and routers while cutting consumers over from the obsolete Audit/Data/cloud-example/learning/llm-wiki/RIA bodies and controls, then remove those bodies without creating an Archive dependency or permanent census. | platform | In Progress | Activated after the reviewed WP-007 disposition and atomic state handoff; no ownership mutation is accepted yet. | WP-007 disposition commit `16a8038`; current consumer map; focused semantic, link, recovery, and quality gates; logical cutover commit |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-008's accepted-disposition prerequisite, consumer-first
cutover, reachable Git recovery, research preservation boundary, reviews,
rollback, and logical commit are owned by its linked Plan section. It does not
create a Migration, Tombstone, redirect, replacement Research package, or
full-body Archive copy merely to delete an obsolete current owner.

## Verification Summary

WP-008 is active after WP-007 completed. The state handoff carries no accepted
ownership-cutover evidence; implementation begins from the Task-local
disposition and preserved Research boundary.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-008](../plan.md#wp-008--stage-90-ownership-cutover) | In Progress. | Activated after WP-007 completion; no ownership-cutover evidence is accepted yet. |
