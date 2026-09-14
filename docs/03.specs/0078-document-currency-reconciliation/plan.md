---
title: "Document Currency Reconciliation Implementation Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-09-14"
layer: "specs"
artifact_id: "SPEC-0078-PLAN-0001"
---

# Document Currency Reconciliation Implementation Plan (Plan)

## Overview

This Plan orders the reconciliation the Spec approves into six packages that
each revert by their own commit. Every correction is checked against the
implementation before it is written.

## Context

Four read-only audits covered Stage 01/02, Stage 05/90, the hub, indexes and
templates, and the incomplete Stage 03 packages. The lifecycle validator
compares a whole change from its base, so each document may take only one
declared edge per change; the Plan sequences dispositions accordingly.

## Goals & In-Scope

Correct statements that conflict with the implementation. Bring accepted
decisions, stage indexes and dated references into line with the tree. Move
implemented or overtaken Stage 03 packages one lifecycle edge and record why.

## Non-Goals & Out-of-Scope

No implementation, manifest, script, test, workflow or registry change. No
sealed archive record or archive index row change. No second lifecycle edge
and no registry edge addition. Push, merge and branch cleanup follow the request
owner's approval; no live cluster, provider runtime or network action is
performed.

## Work Breakdown

### WP-001: Correct operations documents

| Item | Detail |
| --- | --- |
| Subject | Runbooks, the service-mesh policy and the QA guide name absent files, wrong resource names, unusable commands and rules the manifests break. |
| Owns | `docs/05.operations/` |
| Check | Every corrected command, path and name resolves in the tree; the operations indexes match their documents' dates. |
| Rollback | Revert the commit. |

### WP-002: Correct requirement, architecture, hub and template documents

| Item | Detail |
| --- | --- |
| Subject | Current owners named as superseded decisions, archive-model prose that ADR-0032 replaced, stale link text and template inventory gaps. |
| Owns | `docs/01.requirements/`, `docs/02.architecture/` except the decision supersession set, `docs/README.md`, `docs/98.archive/README.md` prose, `docs/99.templates/templates/README.md` |
| Check | Strict profile and link gates pass; the archive cutover gate still passes. |
| Rollback | Revert the commit. |

### WP-003: Reconcile the decision log

| Item | Detail |
| --- | --- |
| Subject | ADR-0027 was superseded by ADR-0028 without the lifecycle move, and ADR-0009's install clauses contradict the Kiali Application. |
| Owns | ADR-0009, ADR-0027, ADR-0028, a proposed ADR-0037 and the decisions index |
| Check | The lifecycle gate accepts the reciprocal supersession; the new decision is created in its initial state. |
| Rollback | Revert the commit. |

### WP-004: Annotate dated reference observations

| Item | Detail |
| --- | --- |
| Subject | Stage 90 observations about bootstrap pins, image versions, CI jobs and evidence paths no longer hold. |
| Owns | `docs/90.references/` |
| Check | Original observation dates are unchanged; the registry index-parity gate passes. |
| Rollback | Revert the commit. |

### WP-005: Take the next lifecycle edge for implemented Stage 03 work

| Item | Detail |
| --- | --- |
| Subject | Packages whose work is implemented or overtaken still carry draft, queued or active state, and their bodies cite a deleted script and retired paths. |
| Owns | the affected Stage 03 package documents and `docs/03.specs/README.md` |
| Check | Each changed document moves one declared edge; the index-status gate passes. |
| Rollback | Revert the commit. |

### WP-006: Record deferred dispositions

| Item | Detail |
| --- | --- |
| Subject | Withdrawals of never-activated drafts, second edges and native runtime acceptance cannot be made in this change. |
| Owns | the reconciliation Task |
| Check | Every deferred disposition names its blocker and next owner. |
| Rollback | Revert the commit. |

## Verification Plan

Each logical commit passes `python3 scripts/qa.py staged` over its exact index.
One `python3 scripts/qa.py full` runs on the final tree. Hosted CI is recorded
only for an observed commit.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| An audit finding is wrong | Re-verify each finding against the tree before editing; unreproduced findings stay unchanged and are recorded |
| A historical record is rewritten | Add dated notes beside dated sections instead of editing them |
| A disposition needs two edges | Take one edge and record the second as a follow-up |

## Completion Criteria

All six packages are committed with passing staged QA, the final tree passes
`full`, and the Task records every correction, every unreproduced finding and
every deferred disposition with its owner.

## Traceability

The [Spec](spec.md) owns the contract and criteria. The
[reconciliation Task](tasks/tsk-0001-reconcile-document-currency.md) owns
execution evidence and the handoff record.

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-DCU-001](spec.md#success-criteria--verification-plan) | WP-001 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-001](spec.md#success-criteria--verification-plan) | WP-002 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-002](spec.md#success-criteria--verification-plan) | WP-003 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-005](spec.md#success-criteria--verification-plan) | WP-004 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-003](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-004](spec.md#success-criteria--verification-plan) | WP-005 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
| [VAL-DCU-006](spec.md#success-criteria--verification-plan) | WP-006 | [tsk-0001](tasks/tsk-0001-reconcile-document-currency.md) |
