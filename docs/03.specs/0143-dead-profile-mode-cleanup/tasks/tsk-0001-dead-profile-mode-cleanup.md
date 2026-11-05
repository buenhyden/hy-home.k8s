---
title: "Dead Profile Mode Cleanup"
version: "0.1.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0143-TSK-0001"
parent_ids: ["SPEC-0143-PLAN-0001"]
---

# Task: Dead Profile Mode Cleanup

## Overview

Remove the profile and frontmatter modes that no registry value produces, and
the validator branches that only they reach. It executes
[SPEC-0143](../spec.md) through [WORK-001–002](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): clean up the dead modes, the follow-up SPEC-0142
  left.
- Approval (2026-11-06): the operator approved SPEC-0143 and its Plan after
  review of the draft in `efba0179`, and asked for a pull request and merge.
- Start: branch `refactor/dead-profile-modes` from `main` at `0b00f3a3`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | Type regression test and narrowed `Literal` types | platform | ready | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | Unreachable branches and helper code | platform | ready | NOT_RUN | EVD-002 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Type regression test | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Code search, document suite, strict document checks and repository quality check | Pending | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DPM-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-DPM-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/document_contracts.py`,
  `scripts/validate-markdown-profiles.py`,
  `scripts/validation/repository/quality.py`,
  `tests/test_document_terminal_contract.py`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/` schemas and registry, current
  document bodies outside the Allowed Paths
- **Approval Required**: Spec and Plan approval by the operator; push and
  merge are separate.
- **Static Validation**: document contract suite, strict document checks,
  repository quality check, `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

Not run yet.
