---
title: 'Task: Current Surface and Stash Reconciliation'
type: sdlc/task
status: draft
owner: platform
updated: 2026-08-07
artifact_id: "TASK-0047"
---

# Task: Current Surface and Stash Reconciliation

## Overview

This Task is the durable execution ledger for Spec 047. It will record the
PRD-0007 program activation, current tracked target inventory, canonical
surface/owner mapping, one disposition per target, tracked stash reconciliation
categories, any current-generated residue evidence, reviews, validation, and
the handoff to Spec 048. CSASR-000 is in progress and all later rows remain
queued. This activation claims no target implementation, stash content
adoption, stash apply/pop/drop, remote, or live result.

## Inputs

- Parent [Spec 047](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-0007](../../01.requirements/0007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Current `validation-surfaces.json`, document profile registry, Current audit
  pack, tracked repository inventory, and affected-surface validators
- Preserved stash object
  `6370311e020620cc2743005896cc88db97d15465`; ordinal and parents must be
  re-observed at execution time

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CSASR-000 | VAL-CSASR-001, VAL-CSASR-009 | Activate PRD-0007 lineage and reciprocal Spec/Plan/Task path | platform | In Progress | Exact activation set is under validation; activation SHA is not preclaimed | Program registry, projection validator, indexes, staged lifecycle, and activation commit |
| CSASR-001 | VAL-CSASR-001, VAL-CSASR-002, VAL-CSASR-006 | Inventory every tracked target and resolve one surface/owner | platform | Queued | Not executed | Exact `git ls-files` population and affected-surface classification |
| CSASR-002 | VAL-CSASR-002, VAL-CSASR-003 | Record audit delta and `change|no-change|defer` matrix | platform | Queued | Not executed | One Task row per target with observation, disposition, evidence, and successor |
| CSASR-003 | VAL-CSASR-004, VAL-CSASR-006, VAL-CSASR-007 | Record tracked stash hunk categories without applying or dropping stash | platform | Queued | Not executed | Full stash object/parent metadata, tracked path list, hunk categories, destination owner, and review |
| CSASR-004 | VAL-CSASR-005 | Regenerate only validator-proven stale derived evidence with current producer | platform | Queued | Not executed | Current generator command/result and residue validator evidence, or evidence-backed no-change |
| CSASR-005 | VAL-CSASR-008, VAL-CSASR-009 | Run QA/review, close Spec 047, and hand off to Spec 048 | platform | Queued | Not executed | Focused/strict/affected/aggregate/all-files/diff/review evidence and reciprocal closure |

## Approval and Safety Boundaries

- **Allowed Paths**: PRD-0007/AD-0010/ADR-0021, Spec 047, reciprocal
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

CSASR-000 starts from clean branch HEAD
`7a1923d0a93143e3f8d106e98ac5bee25e2a10b5` and observes preserved stash
object `6370311e020620cc2743005896cc88db97d15465`. It activates only the PRD-0007
lineage and reciprocal SDLC path; it does not preclaim its own commit SHA or
any CSASR-001 through CSASR-005 result.

Later work will add the exact target disposition matrix, stash ledger,
current-generator decision, logical commits, validator results, review
outcomes, formatter effects, limitations, and successor handoff.

## Traceability

- **Spec**: [Current Surface and Stash Reconciliation](spec.md)
- **Plan**: [Current Surface and Stash Reconciliation Implementation Plan](plan.md)
- **Successor**: Spec 048 GitHub Routing and CI Evidence
- **Stash state**: preserved until Spec 051 finishing gate

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [CSASR-000](plan.md#work-breakdown) | In Progress | The reciprocal activation set is being validated; commit SHA is not yet claimed. |
| N/A — CSASR-001 shares the Plan and Spec sources above | Not executed | Queued tracked inventory evidence. |
| N/A — CSASR-002 shares the Plan and Spec sources above | Not executed | Queued disposition matrix evidence. |
| N/A — CSASR-003 shares the Plan and Spec sources above | Not executed | Queued tracked stash reconciliation evidence. |
| N/A — CSASR-004 shares the Plan and Spec sources above | Not executed | Queued current-generator evidence or no-change proof. |
| N/A — CSASR-005 shares the Plan and Spec sources above | Not executed | Queued closure and handoff evidence. |
