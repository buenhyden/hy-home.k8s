---
title: "Reconcile Document Currency"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-14"
layer: "specs"
artifact_id: "SPEC-0078-TSK-0001"
---

# Task: Reconcile Document Currency

## Overview

This Task owns execution of the six approved packages, the evidence for each
logical commit, the final full result and the handoff record. It records
observed results only and never promotes a repository-static result to hosted,
provider-runtime or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, boundaries and criteria.
- [Plan](../plan.md) owns package order, ownership and rollback.
- Baseline: `python3 scripts/qa.py full` at `EXIT=0`, 22 of 22 gates `PASS`,
  on the tree of commit `404d422c`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-DCU-001 | Correct operations documents | platform | Queued | Not executed | Per-finding tree evidence and staged QA |
| WORK-002 | VAL-DCU-001 | Correct requirement, architecture, hub and template documents | platform | Queued | Not executed | Strict document gates and archive cutover gate |
| WORK-003 | VAL-DCU-002 | Reconcile the decision log | platform | Queued | Not executed | Lifecycle gate |
| WORK-004 | VAL-DCU-005 | Annotate dated reference observations | platform | Queued | Not executed | Registry index-parity gate |
| WORK-005 | VAL-DCU-003, VAL-DCU-004 | Take the next lifecycle edge for implemented Stage 03 work | platform | Queued | Not executed | Lifecycle and index-status gates |
| WORK-006 | VAL-DCU-006 | Record deferred dispositions | platform | Queued | Not executed | This record |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/01.requirements/`, `docs/02.architecture/`,
  `docs/03.specs/`, `docs/05.operations/`, `docs/90.references/`,
  `docs/README.md`, `docs/99.templates/templates/README.md`, and the prose of
  `docs/98.archive/README.md` outside its manifest comment and index table.
- **Forbidden Paths**: sealed records under `docs/98.archive/`,
  `docs/99.templates/registry.json` and contracts, `gitops/`, `infrastructure/`,
  `policy/`, `secrets/`, `scripts/`, `tests/`, `.github/`, `.agents/`.
- **Approval Required**: The request owner approved reconciliation, lifecycle
  status changes, remediation of separate defects found during the work, and
  commit, merge, push and branch cleanup after completion. Withdrawing
  never-activated drafts through an undeclared edge is not approved.
- **Static Validation**: staged QA per logical commit, one
  `python3 scripts/qa.py full` on the final tree, and `git diff --check`.
- **Live Validation**: DEFER. No live cluster, provider runtime or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential or private configuration
  file is read or printed.
- **Rollback Plan**: Each package is one commit that reverts alone.
- **Evidence Location**: This Task record.

## Verification Summary

Not executed. Results, limitations, review disposition, residual risk and next
owner are recorded here as work advances.

## Traceability

Each work item below carries its observed result and durable evidence.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Not executed. | Pending operations correction evidence. |
| [WORK-002](../plan.md#work-breakdown) | Not executed. | Pending document gate evidence. |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Pending decision log evidence. |
| [WORK-004](../plan.md#work-breakdown) | Not executed. | Pending reference evidence. |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Pending lifecycle evidence. |
| [WORK-006](../plan.md#work-breakdown) | Not executed. | Pending handoff evidence. |
