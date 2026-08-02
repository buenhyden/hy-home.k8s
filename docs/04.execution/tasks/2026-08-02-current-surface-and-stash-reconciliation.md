---
title: 'Task: Current Surface and Stash Reconciliation'
type: sdlc/task
status: draft
owner: platform
updated: 2026-08-02
---

# Task: Current Surface and Stash Reconciliation

## Overview

This Task is the durable execution ledger for Spec 047. It will record the
PRD-007 program activation, current tracked target inventory, canonical
surface/owner mapping, one disposition per target, tracked stash reconciliation
categories, any current-generated residue evidence, reviews, validation, and
the handoff to Spec 048. All rows are queued and this draft claims no
implementation, stash content adoption, stash apply/pop/drop, remote, or live
result.

## Inputs

- Parent [Spec 047](../../03.specs/047-current-surface-and-stash-reconciliation/spec.md)
- Parent [Implementation Plan](../plans/2026-08-02-current-surface-and-stash-reconciliation.md)
- [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md),
  [ARD-0010](../../02.architecture/requirements/0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Current `validation-surfaces.json`, document profile registry, Current audit
  pack, tracked repository inventory, and affected-surface validators
- Preserved stash object
  `6370311e020620cc2743005896cc88db97d15465`; ordinal and parents must be
  re-observed at execution time

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-000 | VAL-CSASR-001, VAL-CSASR-009 | Activate PRD-007 lineage and reciprocal Spec/Plan/Task path | platform | Queued | Not executed | Program registry, projection validator, indexes, staged lifecycle, and activation commit |
| CSASR-001 | VAL-CSASR-001, VAL-CSASR-002, VAL-CSASR-006 | Inventory every tracked target and resolve one surface/owner | platform | Queued | Not executed | Exact `git ls-files` population and affected-surface classification |
| CSASR-002 | VAL-CSASR-002, VAL-CSASR-003 | Record audit delta and `change|no-change|defer` matrix | platform | Queued | Not executed | One Task row per target with observation, disposition, evidence, and successor |
| CSASR-003 | VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007 | Record tracked stash hunk categories without applying or dropping stash | platform | Queued | Not executed | Full stash object/parent metadata, tracked path list, hunk categories, destination owner, and review |
| CSASR-004 | VAL-CSASR-005 | Regenerate only validator-proven stale derived evidence with current producer | platform | Queued | Not executed | Current generator command/result and residue validator evidence, or evidence-backed no-change |
| CSASR-005 | VAL-CSASR-008, VAL-CSASR-009 | Run QA/review, close Spec 047, and hand off to Spec 048 | platform | Queued | Not executed | Focused/strict/affected/aggregate/all-files/diff/review evidence and reciprocal closure |

## Approval and Safety Boundaries

- **Allowed Paths**: PRD-007/ARD-0010/ADR-0021, Spec 047, reciprocal
  Plan/Task and indexes, progress, document profiles, registry projection
  validator/tests, current tracked target metadata, and validator-proven
  `active-corpus-residue-closure.json` regeneration.
- **Forbidden Paths**: ignored/private state, secret values, auth files,
  provider logs, RTK logs, shell history, live-system state, and the stash's
  untracked-parent payload.
- **Approval Required**: any downstream active-target implementation, push,
  PR, remote mutation, workflow dispatch, credential action, live operation,
  or stash apply/pop/drop. None is authorized in this Task.
- **Static Validation**: registry/lifecycle self-tests and staged modes,
  Markdown/link contracts, affected surfaces, residue closure, repository
  aggregate, all-files pre-commit, formatter inspection, diff, and independent
  reviews.
- **Live Validation**: `DEFER`; no hosted/provider/remote/live result can be
  promoted from repository-static evidence.
- **Secret / Vault Handling**: never read or print secret values; record only
  tracked path metadata and redacted contract results.
- **Rollback Plan**: revert the smallest CSASR logical commit in reverse order;
  revert program activation last and preserve the stash throughout.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`; temporary inventories are not
  durable evidence.

## Verification Summary

Not executed. During implementation this section will contain the exact target
disposition matrix, stash ledger, current-generator decision, logical commits,
validator results, review outcomes, formatter effects, limitations, and
successor handoff. Draft rows and planned commands are not PASS evidence.

## Traceability

- **Spec**: Current Surface and Stash Reconciliation
- **Plan**: Current Surface and Stash Reconciliation Implementation Plan
- **Successor**: Spec 048 GitHub Routing and CI Evidence
- **Stash state**: preserved until Spec 051 finishing gate

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [CSASR-000](../plans/2026-08-02-current-surface-and-stash-reconciliation.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — CSASR-001 shares the Plan and Spec sources above | Not executed | Queued tracked inventory evidence. |
| N/A — CSASR-002 shares the Plan and Spec sources above | Not executed | Queued disposition matrix evidence. |
| N/A — CSASR-003 shares the Plan and Spec sources above | Not executed | Queued tracked stash reconciliation evidence. |
| N/A — CSASR-004 shares the Plan and Spec sources above | Not executed | Queued current-generator evidence or no-change proof. |
| N/A — CSASR-005 shares the Plan and Spec sources above | Not executed | Queued closure and handoff evidence. |
