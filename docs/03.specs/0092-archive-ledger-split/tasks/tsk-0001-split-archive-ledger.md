---
title: "Split the Archive Ledger"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-26"
layer: "specs"
artifact_id: "SPEC-0092-TSK-0001"
---

# Task: Split the Archive Ledger

## Overview

Execute [SPEC-0092-PLAN-0001](../plan.md). The request owner approved on
2026-09-26 the archive ledger split, a Markdown ledger, ADR-0047 without
superseding ADR-0040, the design, the Spec, and the Plan, with inline
execution. Push, merge, and live actions are not authorized.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0047](../../../02.architecture/decisions/0047-archive-ledger-beside-the-navigation-index.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-ALS-007 | Propose the package | platform | Done | Package, ADR-0047, index rows, and REQ-0003 line | Staged QA |
| WORK-002 | VAL-ALS-001, VAL-ALS-003, VAL-ALS-004 | Registry ledger path and reader routing | platform | Queued | Not executed | Focused tests, whole suite, staged QA |
| WORK-003 | VAL-ALS-002, VAL-ALS-005, VAL-ALS-006 | Move the tables | platform | Queued | Not executed | Comparison, whole suite, staged QA |
| WORK-004 | VAL-ALS-003 | Author instructions | platform | Queued | Not executed | Staged QA |
| WORK-005 | VAL-ALS-007 | Evidence and closure | platform | Queued | Not executed | Full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/98.archive/README.md`, `docs/98.archive/ledger.md`, `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `docs/99.templates/templates/archive/ledger.template.md`, `docs/99.templates/templates/README.md`, `scripts/document_contracts.py`, `scripts/archive_dispositions.py`, `scripts/archive_validation.py`, `scripts/archive_cutover.py`, `scripts/validate-links-and-owners.py`, the tests they own, `.agents/skills/archive-cutover/SKILL.md`, `.agents/governance/document-lifecycle.md`, `.agents/governance/document-authoring.md`, ADR-0047, the SPEC-0091 Task, REQ-0003, the Stage 03 and decisions READMEs, and this package
- **Forbidden Paths**: `docs/98.archive/{completed,retired,superseded,migrations}/**`, lifecycle states and edges, `.github/`
- **Approval Required**: push, pull request, merge, and any live action
- **Static Validation**: focused tests, the whole unit suite before each code commit, staged QA per commit, full QA at closure
- **Live Validation**: none
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the local commits in reverse order
- **Evidence Location**: this Task

## Verification Summary

Pending.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Proposed | Staged QA |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-005](../plan.md#work-breakdown) | Not executed | Pending |
