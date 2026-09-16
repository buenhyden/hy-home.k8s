---
title: "ADR-0032 Retention Pilot Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "done"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0080-PLAN-0001"
---

# ADR-0032 Retention Pilot Implementation Plan

## Global Constraints

No frozen Stage 98 record, ledger, retained package, or frozen index row
changes. The other fifteen superseded decisions stay in Stage 02. No live
cluster, provider runtime, or network action is authorized.

## Overview

This Plan executes [Spec 0080](spec.md): close the SPEC-0079 residual risks,
prove frozen links through the catalog, repoint the current consumers, and
retain ADR-0032.

## Context

On 2026-09-15 the request owner chose a one-decision pilot over moving all
sixteen superseded decisions, because moving them would rewrite 99 links in 40
documents. Review of the pilot found that three frozen ledgers link ADR-0032 and
that REQ-0003 and SPEC-0054 still cited it as authority.

## Goals & In-Scope

Retain ADR-0032 through the ADR-0038 machine path with every gate passing and no
frozen byte changed.

## Non-Goals & Out-of-Scope

No other decision moves, no frozen rewrite, and no rewrite of citations that do
not name ADR-0032. Push, pull request, and merge follow the request owner.

## Work Breakdown

| ID     | Work package                                                                               | Depends on | Entry gate                  | Exit evidence                                  |
| ------ | ------------------------------------------------------------------------------------------ | ---------- | --------------------------- | ---------------------------------------------- |
| WP-001 | Compare moved bodies through link rebasing and derive the frozen-generation registry       | None       | SPEC-0079 residual risks    | Unit discovery                                 |
| WP-002 | Resolve frozen Stage 98 links to a catalog-retained source                                 | WP-001     | Frozen ledgers link ADR-0032 | Link regressions                               |
| WP-003 | Repoint current consumers and the `archive-cutover` skill to ADR-0038                      | None       | Consumer census             | Link gate                                      |
| WP-004 | Retain ADR-0032 with one catalog row                                                       | WP-001 to WP-003 | Consumer zero         | Staged and full QA                             |

## Verification Plan

Each work package runs its focused regressions; the final tree runs
`python3 scripts/qa.py staged` over the exact index and one
`python3 scripts/qa.py full`.

## Risks & Mitigations

| Risk                                                     | Mitigation                                                              |
| -------------------------------------------------------- | ----------------------------------------------------------------------- |
| A frozen link breaks when its target leaves its stage     | WP-002 resolves it through the catalog row that names the original path |
| A current consumer keeps ADR-0032 as authority            | WP-003 cites the successor before the move                              |
| The retained copy drifts from its source                  | WP-001 compares it through link rebasing                                |

## Completion Criteria

WP-001 to WP-004 pass their exit evidence and the final tree passes staged and
full QA with every frozen file unmodified.

## Traceability

[Spec](spec.md) owns the contract and criteria.

### Lifecycle Traceability

| Spec criterion                                             | Work package | Expected Task                                   |
| ---------------------------------------------------------- | ------------ | ----------------------------------------------- |
| [VAL-ARP-001](spec.md#success-criteria--verification-plan) | WP-004       | [tsk-0001](tasks/tsk-0001-retain-adr-0032.md)   |
| [VAL-ARP-002](spec.md#success-criteria--verification-plan) | WP-002       | [tsk-0001](tasks/tsk-0001-retain-adr-0032.md)   |
| [VAL-ARP-003](spec.md#success-criteria--verification-plan) | WP-003       | [tsk-0001](tasks/tsk-0001-retain-adr-0032.md)   |
| [VAL-ARP-004](spec.md#success-criteria--verification-plan) | WP-001       | [tsk-0001](tasks/tsk-0001-retain-adr-0032.md)   |
