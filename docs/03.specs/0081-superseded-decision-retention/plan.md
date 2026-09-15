---
title: "Superseded Decision Retention Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0081-PLAN-0001"
---

# Superseded Decision Retention Implementation Plan

## Global Constraints

No frozen Stage 98 record, ledger, retained package, or frozen index row
changes. No validator changes. No live cluster, provider runtime, or network
action is authorized.

## Overview

This Plan executes [Spec 0081](spec.md) in one change: the consumers and the
indexes move to identifiers, and the fifteen decisions move together.

## Context

The ADR-0032 pilot proved the ADR-0038 path on one decision. On 2026-09-15 the
request owner approved each of the fifteen remaining dispositions.

## Goals & In-Scope

An empty superseded set in the decision log with every gate passing.

## Non-Goals & Out-of-Scope

No rewrite of dated history beyond removing link syntax. Push, pull request,
and merge follow the request owner.

## Work Breakdown

| ID     | Work package                                                          | Depends on | Entry gate            | Exit evidence               |
| ------ | --------------------------------------------------------------------- | ---------- | --------------------- | --------------------------- |
| WP-001 | Name the fifteen by identifier in current documents and indexes       | None       | Approved dispositions | Link gate                   |
| WP-002 | Retain the fifteen with rebased links and one catalog row each        | WP-001     | Consumer zero         | Lifecycle and archive gates |
| WP-003 | Record the evidence                                                   | WP-002     | Gates pass            | Staged and full QA          |

## Verification Plan

`python3 scripts/qa.py staged` over the exact index and one
`python3 scripts/qa.py full` on the final tree.

## Risks & Mitigations

| Risk                                                   | Mitigation                                               |
| ------------------------------------------------------ | -------------------------------------------------------- |
| A link among the fifteen resolves to a vacated path     | Re-base through the whole move and prove link equivalence |
| A validator constant still names an old decision path  | It applies only when that path is present in a comparison |

## Completion Criteria

WP-001 to WP-003 pass their exit evidence with every frozen file unmodified.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion                                             | Work package | Expected Task                                              |
| ---------------------------------------------------------- | ------------ | ---------------------------------------------------------- |
| [VAL-SDR-001](spec.md#success-criteria--verification-plan) | WP-002       | [tsk-0001](tasks/tsk-0001-retain-superseded-decisions.md)  |
| [VAL-SDR-002](spec.md#success-criteria--verification-plan) | WP-001       | [tsk-0001](tasks/tsk-0001-retain-superseded-decisions.md)  |
| [VAL-SDR-003](spec.md#success-criteria--verification-plan) | WP-003       | [tsk-0001](tasks/tsk-0001-retain-superseded-decisions.md)  |
