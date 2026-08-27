---
title: 'Task: Responsibility topology and compatibility cutover'
type: sdlc/task
status: queued
owner: platform
updated: 2026-08-22
artifact_id: "TSK-0054-0011"
---

# Task: Responsibility topology and compatibility cutover

## Overview

This is the terminal queued Task record for WP-011.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-011 execution boundary](../plan.md#wp-011--responsibility-topology-and-compatibility-cutover)

## Task Table

**Plan label:** WP-011

**Depends on:** WP-010

**Current state:** `queued`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-011 | VAL-SDLC-010..VAL-SDLC-012 | Move scripts/tests into responsibility directories and retire approved compatibility wrappers at consumer-zero. | platform | Queued | Not executed. | Registry/path parity, imports/CI/pre-commit/affected-lane GREEN, logical commits per responsibility batch |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-011's responsibility graph, consumer-zero retirement,
reviews, rollback, and ordered responsibility-batch commits are owned by its
linked Plan section.

## Verification Summary

WP-011 is queued and has no accepted execution evidence.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-011](../plan.md#wp-011--responsibility-topology-and-compatibility-cutover) | Queued. | No accepted execution evidence yet. |
