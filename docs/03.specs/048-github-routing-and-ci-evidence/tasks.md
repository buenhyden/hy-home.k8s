---
title: 'Task: GitHub Routing and CI Evidence'
type: sdlc/task
status: draft
owner: platform
updated: 2026-08-02
artifact_id: "TASK-048"
---

# Task: GitHub Routing and CI Evidence

## Overview

This Task is the durable execution ledger for Spec 048. It will record the
GitHub routing contract package, native labeler/CODEOWNERS/hub projection,
affected and aggregate routing, read-only remote metadata, logical commits,
QA, reviews, closure, and Spec 049 handoff. Every row is queued; this draft
claims no implementation, hosted-current result, remote mutation, or live
evidence.

## Inputs

- Parent [Spec 048](spec.md)
- Parent [Implementation Plan](plan.md)
- [PRD-007](../../01.requirements/007-repository-delivery-and-platform-assurance.md),
  [AD-0010](../../02.architecture/descriptions/ad-0010-repository-delivery-evidence-architecture.md),
  and [ADR-0021](../../02.architecture/decisions/0021-canonical-surface-routing-and-evidence-depth.md)
- Spec 047 target disposition and successor matrix
- Current `validation-surfaces.json`, `.github/labeler.yml`,
  `.github/CODEOWNERS`, `.github/README.md`, workflow YAML, repository
  aggregate, GitHub security validator, and read-only remote metadata

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| GRCE-000 | VAL-GRCE-001, VAL-GRCE-008 | Activate reciprocal Spec/Plan/Task path and program row | platform | Queued | Not executed | Staged lifecycle, strict documents, indexes, progress, and activation commit |
| GRCE-001 | VAL-GRCE-001, VAL-GRCE-002, VAL-GRCE-003 | Define focused RED contract/native projection expectations | platform | Queued | Not executed | Focused test and mutation fixture results with stable rule IDs |
| GRCE-002 | VAL-GRCE-001, VAL-GRCE-003 | Implement contract, schema, validator, self-test, and production check | platform | Queued | Not executed | Artifact inventory, schema result, focused unittest, self-test, and production result |
| GRCE-003 | VAL-GRCE-002, VAL-GRCE-003, VAL-GRCE-005 | Align labeler, CODEOWNERS, and GitHub hub claims | platform | Queued | Not executed | Native parity result for all mapped surfaces and tag-only changelog claim |
| GRCE-004 | VAL-GRCE-004, VAL-GRCE-005, VAL-GRCE-008 | Wire affected routing, aggregate ownership, and inventories without duplicate primary execution | platform | Queued | Not executed | Affected/AGQC/security/aggregate results and command-owner matrix |
| GRCE-005 | VAL-GRCE-006, VAL-GRCE-007, VAL-GRCE-008 | Record SHA-bound remote metadata, QA/reviews, closure, and Spec 049 handoff | platform | Queued | Not executed | Metadata observation, DEFER rows, full QA, review dispositions, and closure commit |

## Approval and Safety Boundaries

- **Allowed Paths**: new GitHub routing contract/schema/fixture/validator/test;
  `.github/labeler.yml`, `.github/CODEOWNERS`, `.github/README.md`; current
  validation routing/fixtures, repository aggregate, inventories, reciprocal
  SDLC documents/indexes, and progress.
- **Forbidden Paths**: ignored/private state, secrets, auth caches, provider
  payloads, shell history, RTK logs, workflow logs, and live-system data.
- **Approval Required**: push, PR, remote merge, workflow dispatch/rerun,
  branch-rule/ruleset or review-enforcement change, credential use, release,
  deployment, or live mutation. None is authorized here.
- **Static Validation**: focused self-test/production/unittest, affected
  surfaces, AGQC, GitHub Actions security, strict documents, repository
  aggregate, all-files pre-commit, formatter inspection, both diff checks, and
  independent requirements plus quality/security reviews.
- **Live Validation**: `DEFER`; historical remote observations bind only their
  exact SHA and local-current hosted evidence remains `DEFER`.
- **Secret / Vault Handling**: no log or secret-value reads; diagnostics and
  durable evidence are metadata-only and value-free.
- **Rollback Plan**: revert GRCE commits in reverse order; native projection
  and its matching contract expectation revert together, and validator
  registration plus aggregate invocation revert together.
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`.

## Verification Summary

Not executed. Implementation will record exact artifact versions, contract
counts, mapped surface classes, native projection differences, focused and
aggregate results, formatter effects, remote repository/SHA/time/result/
limitation rows, reviews, logical commits, and successor handoff. Planned
commands and dated historical metadata are not current PASS evidence.

## Traceability

- **Spec**: GitHub Routing and CI Evidence
- **Plan**: GitHub Routing and CI Evidence Implementation Plan
- **Predecessor**: Spec 047 Current Surface and Stash Reconciliation
- **Successor**: Spec 049 Platform Validation and Security Evidence

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [GRCE-000](plan.md#work-breakdown) | Not executed | Queued activation evidence. |
| N/A — GRCE-001 shares the Plan and Spec sources above | Not executed | Queued focused RED evidence. |
| N/A — GRCE-002 shares the Plan and Spec sources above | Not executed | Queued contract package evidence. |
| N/A — GRCE-003 shares the Plan and Spec sources above | Not executed | Queued native projection evidence. |
| N/A — GRCE-004 shares the Plan and Spec sources above | Not executed | Queued affected/aggregate integration evidence. |
| N/A — GRCE-005 shares the Plan and Spec sources above | Not executed | Queued remote metadata, QA, review, and closure evidence. |
