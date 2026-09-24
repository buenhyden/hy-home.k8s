---
title: "Task: Stage 90 ownership cutover"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-01"
layer: "specs"
artifact_id: "SPEC-0054-TSK-0008"
---

# Task: Stage 90 ownership cutover

## Overview

This is the completed Spec 0054 Task record for WP-008.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-008 execution boundary](../plan.md#wp-008--stage-90-ownership-cutover)

## Task Table

**Plan label:** WP-008

**Depends on:** WP-007

**Current state:** `done`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-008 | VAL-SDLC-008, VAL-SDLC-009, VAL-SDLC-011, VAL-SDLC-012 | Preserve the approved current Research pack and routers while cutting consumers over from the obsolete Audit/Data/cloud-example/learning/llm-wiki/RIA bodies and controls, then remove those bodies without creating an Archive dependency or permanent census. | platform | Done | Retained the latest external-research content under `research/0001-workspace-engineering/`; established category-specific `####-<slug>` pack and Stage 99 template contracts; removed obsolete Stage 90 bodies, RIA/LLM Wiki controls, exclusive fixtures, and live consumers without an Archive dependency. | WP-007 disposition commit `16a8038`; three focused reference-pack tests; strict registry, Markdown, link, lifecycle, affected-surface, agent-legacy, Archive, and repository aggregate gates; WP-008 logical cutover commit |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
without exception. WP-008's accepted-disposition prerequisite, consumer-first
cutover, reachable Git recovery, research preservation boundary, reviews,
rollback, and logical commit are owned by its linked Plan section. It does not
create a Migration, Tombstone, redirect, replacement Research package, or
full-body Archive copy merely to delete an obsolete current owner.

## Verification Summary

WP-008 completed the Task-local disposition without creating a permanent
Stage 90 census or an active Stage 98 dependency. The latest external research
sources, observations, and claims remain available under the numbered Research
pack; the path/frontmatter/link/current-state corrections are the approved
governance cutover. Focused reference tests passed (3), lifecycle tests passed
(93), the full Archive discovery passed (223), and all strict repository
quality gates passed before the atomic handoff to WP-005.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-008](../plan.md#wp-008--stage-90-ownership-cutover) | Done. | Numbered Audit/Data/Research pack contracts, matching Stage 99 templates, consumer-zero removals, preserved external-research content, and focused/full validation evidence. |
