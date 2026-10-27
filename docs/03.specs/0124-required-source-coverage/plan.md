---
title: "Required Source Coverage Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0124-PLAN-0001"
parent_ids: ["SPEC-0124"]
---

# Required Source Coverage Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals.
- Source pages are read only; nothing from them is installed or run.

## Overview

This plan executes [SPEC-0124](spec.md) on branch
`docs/required-source-coverage` from main `d308fd56`.

## Context

The m0012 register's last refresh was 2026-09-27 under SPEC-0099, which is
now archived.

## Goals & In-Scope

Close VAL-RS-001 and VAL-RS-002.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RS-001](spec.md#success-criteria--verification-plan) | Read the ten sources and add the dated block to m0012 | None | [Task](tasks/tsk-0001-required-source-coverage.md) | Independent source re-read |
| WORK-002 | [VAL-RS-002](spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | WORK-001 | [Task](tasks/tsk-0001-required-source-coverage.md) | Staged QA and hosted checks |

## Verification Plan

An independent reader re-opens a sample of cells, every `NOT_RETRIEVED` and
every `EXPLICIT` value for the four new sources, against the live pages.

## Risks & Mitigations

- A project rule is recorded as a source rule. The contract separates
  `EXPLICIT` from `DERIVED_PROPOSAL`, and the review checks it.
- A failed read is closed as not applicable. `NOT_RETRIEVED` must name the
  failure.

## Completion Criteria

Both criteria have PASS evidence and an accepted decision in the Task.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
