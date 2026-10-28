---
title: "Review Decisions and C4 Prompt"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0133-TSK-0001"
parent_ids: ["SPEC-0133-PLAN-0001"]
---

# Task: Review Decisions and C4 Prompt

## Overview

Record the operator's decisions on the m0012 `DERIVED_PROPOSAL` cells and the
eight `EXTERNAL` survey CRs, and add the adopted C4 checks to the diagram
author prompt. It executes [SPEC-0133](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator asked for a review of the
  `DERIVED_PROPOSAL` items and the eight external items. After the review the
  operator chose to adopt the C4 prompt, to record the CR-12.01 evidence and
  to record what the other seven items wait on.
- Start: main `8d1ddd2b`, branch `docs/review-decisions-and-c4-prompt`.

### Proposal Decisions

The m0012 2026-10-27 source-support matrix holds five `DERIVED_PROPOSAL`
cells. Every SRC-MEM and SRC-AGENT cell is `EXPLICIT`.

| Item | Decision | Owner or reason |
| --- | --- | --- |
| SRC-SDD-A × Policy (constitution phase) | Already covered | `.agents/governance/` is the standing context; security checks route through `sdlc.md` |
| SRC-SDD-D × Templates (lighter spec form) | Already covered | The Stage 99 spec form already holds every example subsection |
| SRC-C4 × Templates (diagram checklist) | Adopted | Element-label and relationship checks join the diagram prompt in `description.template.md` |
| SRC-ADR × System (decision log) | Already covered | `docs/02.architecture/decisions/` is the decision log with supersession and archival |
| SRC-ADR × Templates (Y-statement) | Not adopted | The template sub-page was not read, so no text supports a change |
| agency-agents catalogue | Not adopted | It duplicates the local role registry and needs an unapproved installer |
| ai-memory | Not adopted | It is one product's tool; the shared workspace memory store already owns this |

### External Items

Observed read-only on 2026-10-28. Only `hy-home.docker` is cloned locally
besides this repository.

| CR | Observable now | Closing action and owner |
| --- | --- | --- |
| CR-01.02 | Atom tables exist only in ignored `_workspace/`; some rows were rewritten from the original attachment | Operator supplies the original text for the rewritten rows or accepts the rewritten text |
| CR-03.06 | No shared edition marker across the repositories | Operator names the edition and records each repository's adopted revision in a joint approval |
| CR-03.07 | Contracts differ in layout between this repository and `hy-home.docker` | The same joint approval, then a semantic comparison |
| CR-08.01 | Both public repositories hold `docs/98.archive/`; the private pair was not read | The joint approval decides unification; the private layouts are readable by GET |
| CR-09.04 | Static evidence covers only this repository and `hy-home.docker` | Operator supplies live cluster and certificate acceptance per area |
| CR-12.01 | See the table below | Operator decides whether the observed setup matches the target; private branch protection needs a paid plan |
| CR-14.03 | The token lacks `read:project`, so Projects cannot be read | Operator runs `gh auth refresh -s read:project` and names the projection Project, if any |
| CR-18.06 | No live provider limit response was observed | Operator approves a bounded live probe or accepts a mock-only record labelled not operational |

### CR-12.01 Observation

Read with `gh api` GET calls at 2026-10-28T00:54Z.

| Repository | Visibility | Default branch | Required checks on default | Approving reviews | Self-hosted runners |
| --- | --- | --- | --- | --- | --- |
| `hy-home.k8s` | public | `main` | `ci-summary`, `style-pr`, `independent-review` | 0 | none; CI runs on `ubuntu-latest` |
| `hy-home.docker` | public | `main` | `candidate-quality` | 0 | not read |
| `blog-data` | private | `main` | not readable: the plan returns an upgrade message | not readable | `hy-home` online |
| `Project-Template` | private | `main` | not readable: the plan returns an upgrade message | not readable | two online, `pr-eph-…` and `trusted-…` |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RD-001](../spec.md#success-criteria--verification-plan) | Add the C4 checks to the diagram author prompt | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-RD-002](../spec.md#success-criteria--verification-plan) | Record the proposal and catalogue decisions | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-RD-003](../spec.md#success-criteria--verification-plan) | Record the external evidence and closing actions | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-RD-004](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RD-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Prompt change | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RD-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Decision record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RD-003](../spec.md#success-criteria--verification-plan) | WORK-003 | External record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-RD-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RD-001](../spec.md#success-criteria--verification-plan) | pending | none | Prompt change remains | platform |
| [VAL-RD-002](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-RD-003](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-RD-004](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md` and
  `docs/99.templates/templates/architecture/description.template.md`.
- **Forbidden Paths**: other repositories, GitHub settings, token scopes,
  validators and the registry.
- **Approval Required**: the operator decided on 2026-10-28 (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: none; GitHub reads are GET calls on metadata.
- **Secret / Vault Handling**: no secret, credential or private file content
  is read.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
