---
title: "Spec Architecture Column"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0147-TSK-0001"
parent_ids: ["SPEC-0147-PLAN-0001"]
---

# Task: Spec Architecture Column

## Overview

Make a Spec's architecture statement machine-checked (audit D-1). It
executes [SPEC-0147](../spec.md) through
[WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): review D-1 and proceed.
- Review (2026-11-06): option B, a required column without link-target or
  reciprocal checks, chosen over a target link column.
- Start: branch `docs/sdlc-cross-artifact-conformance` at `d4338908`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | Focused test and registry column | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | Template and fixtures | platform | draft | NOT_RUN | EVD-002 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused test red then green | Pending Spec approval | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks and unit tests | Pending Spec approval | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ARCH-001](../spec.md#success-criteria--verification-plan) | pending | none | Run the focused test | platform |
| [VAL-ARCH-002](../spec.md#success-criteria--verification-plan) | pending | none | Run the strict checks and tests | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/templates/specs/spec.template.md`,
  `tests/test_task_execution_contract.py`, `tests/fixtures/`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `.agents/governance/sdlc.md`
- **Forbidden Paths**: `scripts/`, product manifests, `secrets/`, provider
  settings
- **Approval Required**: Spec and Plan approval by the operator; merge is
  separate
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

Pending.
