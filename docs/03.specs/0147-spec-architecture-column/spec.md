---
title: "Spec Architecture Column"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0147"
---

# Spec Architecture Column Technical Specification (Spec)

## Overview

The AUD-0001 audit left decision D-1: whether a Spec's link to its
constraining architecture is machine-checked. On 2026-11-06 the operator
asked to review D-1 and proceed. A Stage 99 registry change needs this
package. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-spec-architecture-column.md) records it.

## Strategic Boundaries & Non-goals

- In scope: an `Architecture` column in the `sdlc/spec` Lifecycle
  Traceability table, its template, and the test fixtures that build Spec
  tables.
- Non-goals:
  - link-target or reciprocal checks for the new column: the body contract
    has one `reciprocal_evidence` flag, so a target link column would force
    every active Architecture Description to link back to every Spec;
  - any validator code change;
  - rewriting Specs in Git history.
- Open questions: none that change a criterion.

## Contracts

- A Spec's Lifecycle Traceability header is exactly `Requirement ID`,
  `Spec criterion`, `Architecture`, `Verification method`.
- Every `Architecture` cell is non-empty: a link to the constraining
  Architecture Description or ADR, or a stated reason none applies. A cell
  that holds a link is still checked for a broken target by the existing
  link checker.
- Plan, Task, Requirement, AD and ADR contracts are unchanged.

## Core Design

The existing `validate-markdown-profiles.py` already refuses a body-contract
header that differs from `required_columns` (`BODY-CONTRACT-COLUMNS`) and an
empty cell (`BODY-CONTRACT-CELL`). Adding the column to the registry is the
whole enforcement. Constraining architecture:
[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md)
assigns document form to the Stage 99 registry; this change stays there.

## Data Modeling & Storage Strategy

`docs/99.templates/registry.json` `sdlc/spec` `required_columns` gains one
entry. No other data changes.

## Interfaces & Data Structures

The Spec template's Lifecycle Traceability table gains the column. No
command-line interface changes.

## Edge Cases & Error Handling

- Normal: a Spec with the four columns and filled cells passes.
- Error: a Spec with the old three-column header, or an empty
  `Architecture` cell, fails strict profile validation.
- Boundary: no Spec is open, so no current document needs migration;
  completed Specs live only in Git history.

## Failure Modes & Fallback / Human Escalation

A failing consumer test after the change means a fixture still builds the
old header; update that fixture. If the operator rejects the rule, revert the
implementing commit.

## Verification Commands

- `python3 -m unittest tests.test_task_execution_contract`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-ARCH-001 | A focused test fails before and passes after the registry change: the old header and an empty `Architecture` cell are refused, the new header passes |
| VAL-ARCH-002 | The template and every Spec fixture use the new header; strict document checks and the affected unit tests PASS |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCH-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused test red then green |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ARCH-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict document checks and unit tests |
