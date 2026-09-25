---
title: "Converge README Navigation"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0091-TSK-0001"
---

# Task: Converge README Navigation

## Overview

Execute [SPEC-0091-PLAN-0001](../plan.md). The request owner approved on
2026-09-25 the three-part program (README navigation, archive ledger,
language contract), design A for this part, its boundaries, and the Spec.
Push, merge, and live actions are not authorized.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Stage 99 registry](../../../99.templates/registry.json)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-RNC-007 | Propose the package | platform | Done | Committed `3c40f700` | Staged QA 6/6 PASS |
| WORK-002 | VAL-RNC-001, VAL-RNC-002 | Contract, validator, tests, activation | platform | Done | Contract, schema, loader, validator, and 20 tests; 23 READMEs pending | Focused tests, staged QA |
| WORK-003 | VAL-RNC-003 | Stage 03 index; remove `INDEX-*` | platform | Done | Package folder rows without status, currency, or date; `INDEX-*` removed; pinned tests assert the navigation codes | Focused tests, staged QA |
| WORK-004 | VAL-RNC-003 | Stage 90; remove `COLLECTION-INDEX-*` | platform | Done | Stage and research READMEs list collections and packs only; the pack findings column is renamed `Finding`; collection index code removed; two replacement tests | Focused tests, staged QA |
| WORK-005 | VAL-RNC-003 | Knowledge index | platform | Done | Index membership check removed; README existence check kept; replacement completeness test added | Focused tests, staged QA |
| WORK-006 | VAL-RNC-003 | Stage 05 indexes | platform | Done | One two-column document index per collection inside the navigation section; duplicate trees and copied status and date columns removed; the quality check keeps document membership and drops status and date parity | Staged QA |
| WORK-007 | VAL-RNC-005 | Matrices follow their folders | platform | Queued | Not executed | Staged QA |
| WORK-008 | VAL-RNC-004 | Remaining READMEs | platform | Queued | Not executed | Staged QA per area |
| WORK-009 | VAL-RNC-006 | Template guidance | platform | Queued | Not executed | Staged QA |
| WORK-010 | VAL-RNC-007 | Evidence and closure | platform | Queued | Not executed | Full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: tracked `README.md` files except `docs/98.archive/README.md` tables, `docs/99.templates/registry.json`, `docs/99.templates/contracts/document-profile.schema.json`, `docs/99.templates/templates/common/readme-*`, `docs/99.templates/templates/references/*-pack*`, `scripts/document_contracts.py`, `scripts/document_authority.py`, `scripts/validate-links-and-owners.py`, `scripts/validate-knowledge-surface.py`, `scripts/validation/repository/quality.py`, the tests they own, `docs/03.specs/0008-current-local-gitops-platform/spec.md`, REQ-0003, and this package
- **Forbidden Paths**: retained bodies, frozen records, sealed ledgers, lifecycle states and edges, manifests under `gitops/` and `infrastructure/` other than their READMEs, `.github/`
- **Approval Required**: push, pull request, merge, and any live action
- **Static Validation**: focused tests, the registry, profile, and link gates, and staged QA per commit; full QA at closure
- **Live Validation**: none
- **Secret / Vault Handling**: no secret value is read
- **Rollback Plan**: revert the local commits in reverse order
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-25, `main` at `438e69aa`)

A prototype of the rules over the 43 tracked READMEs reported depth, tree,
enumeration, completeness, and copy findings concentrated in `docs/03.specs`,
`docs/90.references`, `docs/98.archive`, `docs/99.templates/templates`,
`gitops`, `infrastructure`, and the root README, and duplicated tree-and-table
lists in five collection READMEs. The Stage 98 README is deferred to the
archive ledger package.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Proposed | Staged QA |
| [WORK-002](../plan.md#work-breakdown) | Contract and validator added | Focused tests and staged QA |
| [WORK-003](../plan.md#work-breakdown) | Stage 03 index routed to packages | Focused tests and staged QA |
| [WORK-004](../plan.md#work-breakdown) | Stage 90 routed to packs | Focused tests and staged QA |
| [WORK-005](../plan.md#work-breakdown) | Knowledge index owned by the contract | Focused tests and staged QA |
| [WORK-006](../plan.md#work-breakdown) | Stage 05 indexes stop copying | Staged QA |
| [WORK-007](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-008](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-009](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-010](../plan.md#work-breakdown) | Not executed | Pending |
