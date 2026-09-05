---
title: "Consolidate Agent Governance and Quality Gates"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0001"
---

# Task: Consolidate Agent Governance and Quality Gates

## Overview

Execute SPEC-0072-PLAN-0001 as four logical commits and record repository-static
and hosted evidence without claiming provider-runtime or live-cluster behavior.

## Inputs

- [SPEC-0072](../spec.md)
- [SPEC-0072-PLAN-0001](../plan.md)
- [ADR-0034](../../../02.architecture/decisions/0034-stage-00-governance-and-unified-quality-gates.md)
- Main baseline `69ae876221410370f13b190c463d88f02f02932a`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-AGQ-001, VAL-AGQ-002 | Move registry, canonical roles, and skills to Stage 00; remove `.agents/` | platform | In progress | Pending | Governance commit and focused tests |
| WORK-002 | VAL-AGQ-003, VAL-AGQ-004, VAL-AGQ-008 | Add tested QA runner/registry and remove duplicate gate/fixture surfaces | platform | Queued | Not executed | QA commit and red/green test output |
| WORK-003 | VAL-AGQ-005, VAL-AGQ-007 | Reconcile current governance, SDLC, QA, CI/CD, and template guidance | platform | Queued | Not executed | Documentation/reference sweep |
| WORK-004 | VAL-AGQ-006 | Simplify GitHub Actions and verify hosted execution | platform | Queued | Not executed | Workflow commit, PR run, `ci-summary` |

## Approval and Safety Boundaries

- **Allowed Paths**: `.github/`, `.claude/`, `.codex/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/`, `scripts/`, `tests/`, `.pre-commit-config.yaml`, `.graphifyignore`
- **Forbidden Paths**: live credentials, secret values, external provider state, cluster state, release state
- **Approval Required**: merge, live deployment/reconciliation, provider authentication, credential access
- **Static Validation**: focused unit tests, QA profiles, pre-commit, actionlint, zizmor, GitHub Actions run
- **Live Validation**: DEFER — not required or authorized for repository governance consolidation
- **Secret / Vault Handling**: do not read, print, mutate, or validate secret values; retain static secret-handling gates
- **Rollback Plan**: revert the owning logical commit; no live system rollback is required
- **Evidence Location**: this Task, Git commits, pull-request checks, and workflow job logs

## Verification Summary

Execution is in progress. Results are recorded only after each named command or
hosted check completes over the branch bytes.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| WORK-001 | In progress | ADR/Spec/Plan/Task authority established on isolated branch |
| WORK-002 | Not executed | Pending QA runner red/green cycle |
| WORK-003 | Not executed | Pending current-reference reconciliation |
| WORK-004 | Not executed | Pending workflow and hosted CI evidence |
