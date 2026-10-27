---
title: "Architecture Views"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0126-TSK-0001"
parent_ids: ["SPEC-0126-PLAN-0001"]
---

# Task: Architecture Views

## Overview

Add C4 views and an arc42 coverage table to AD-0007. It executes
[SPEC-0126](../spec.md) through [WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to proceed as recommended; slice
  B of the SPEC-0125 status table covers CR-09.05 and CR-09.07.
- Sources: SPEC-0124 rows `SRC-WERPC-116`, 273, 274 (C4) and 117 (arc42).
- Start: main `5347f851`, branch `docs/c4-arc42-views`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AV-001](../spec.md#success-criteria--verification-plan) | Add the C4 views, element table and deployment mapping | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-AV-002](../spec.md#success-criteria--verification-plan) | Add the arc42 coverage table and template prompt | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-AV-003](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AV-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Diagram validation and source review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AV-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Coverage review and template tests | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AV-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AV-001](../spec.md#success-criteria--verification-plan) | pending | none | Views and review remain | platform |
| [VAL-AV-002](../spec.md#success-criteria--verification-plan) | pending | none | Coverage table and prompt remain | platform |
| [VAL-AV-003](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `docs/02.architecture/descriptions/0007-current-local-gitops-platform.md`
  and `docs/99.templates/templates/architecture/description.template.md`.
- **Forbidden Paths**: manifests, infrastructure, provider settings and
  credentials.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Mermaid validation, focused tests and `qa.py staged`.
- **Live Validation**: none; the views describe tracked desired state.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
