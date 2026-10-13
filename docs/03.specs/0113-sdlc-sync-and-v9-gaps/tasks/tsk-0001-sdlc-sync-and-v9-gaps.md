---
title: "SDLC Document Sync and Remaining v9 Gaps"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0113-TSK-0001"
parent_ids: ["SPEC-0113-PLAN-0001"]
---

# Task: SDLC Document Sync and Remaining v9 Gaps

## Overview

Execute the six work units of the [Plan](../plan.md) for
[SPEC-0113](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0113](../spec.md) and its [Plan](../plan.md).
- Operator request on 2026-10-13: check that requirements, architecture
  and Spec documents follow the revisions, and review and proceed with F22,
  F02, F18, F05 and F39; the operator chose the section reorder for F02.
- Main `86daf8158f0b03875b1ffa47f2cd86c4914ed391`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | Correct stale requirements, architecture and Spec text | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | Frozen-exclusion cross-check test and fix recipe | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | Four F05 claim statuses in the Stage 99 README | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | F18 evidence correction | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-005 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | Remove the stale `.hadolint.yaml` route | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-006 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | `AGENTS.md` common and Codex-only blocks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | WORK-004 commit index | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | WORK-005 commit index | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | WORK-006 commit index | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks | platform |
| [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-003 checks | platform |
| [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-004 checks | platform |
| [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-005 checks | platform |
| [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-006 checks | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package; `docs/03.specs/README.md`;
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`;
  `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`;
  `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`;
  the SPEC-0106, SPEC-0108, SPEC-0109, SPEC-0110, SPEC-0111 and SPEC-0112
  package documents (notes and appended evidence only);
  `docs/99.templates/README.md`; `scripts/README.md`;
  `scripts/validation/registry.json`; `AGENTS.md`;
  `tests/test_validation_tooling_ownership.py`.
- **Forbidden Paths**: `.pre-commit-config.yaml` exclusion removal,
  `docs/99.templates/registry.json` and schemas, validators, workflows,
  frozen Archive payloads, live cluster, Vault and secret material.
- **Approval Required**: the operator approved SPEC-0113 and its Plan for
  implementation on 2026-10-13 after reviewing the draft at `535d8c11`;
  push, pull request and merge await the operator.
- **Static Validation**: focused tests, document validators and staged QA
  from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
