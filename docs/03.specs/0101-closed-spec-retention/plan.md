---
title: "Closed Spec Package Retention Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-28"
layer: "specs"
artifact_id: "SPEC-0101-PLAN-0001"
---

# Closed Spec Package Retention Implementation Plan (Plan)

## Global Constraints

The request owner asked for the retention on 2026-09-28. Only the three
packages, their catalog rows, and their current citations change. No retained
body or frozen record changes. Push and merge stay with the request owner.

## Overview

This Plan executes [Spec 0101](spec.md): retain SPEC-0098, SPEC-0099, and
SPEC-0100.

## Context

SPEC-0098 closed in PR #110. SPEC-0099 and SPEC-0100 closed in PR #111, which
must reach the default branch before the move.

## Goals & In-Scope

The retention move, the catalog rows, the REQ-0003 links, and the Stage 03
index.

## Non-Goals & Out-of-Scope

No rewrite of a retained body, and no change to SPEC-0008.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Retain SPEC-0098, SPEC-0099, and SPEC-0100 | PR #111 merged | Envelope on the default branch; trees unchanged since it | Lifecycle and archive gates |
| WP-002 | Record the evidence and close | WP-001 | Move committed | Task record |

## Verification Plan

Run `python3 scripts/qa.py staged` on each commit, and the archive contract
tests and the archive cutover gate on the move.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| A package changes after the envelope | The move compares each tree with the envelope first, and the gates reject drift |
| A current document keeps a moved link | The links-and-owners gate fails it |

## Completion Criteria

VAL-CSP-001 and VAL-CSP-002 pass and the Task records the evidence.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-CSP-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-closed-packages.md) |
| [VAL-CSP-002](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-retain-closed-packages.md) |
