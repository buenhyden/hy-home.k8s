---
title: "Generation Boundary and Retention Fixtures"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0014"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Generation Boundary and Retention Fixtures

## Overview

Restore faithful fixture inputs for migration admission and whitespace
retention classification. All published contracts and original evidence stay
with their existing owners.

## Inputs

- [Spec VAL-P02-014](../spec.md#success-criteria--verification-plan) and
  [Plan WORK-014](../plan.md#work-breakdown).
- PR135 exact `179a88c9` reports CI failure; capped diagnostics are not exhaustive.
- Three named REDs and the corrected structured cause record are retained
  externally. Two admission/replay failures precede later controls; the
  whitespace case records thirty local failed subcases.
- Immutable after-boundary commit `2a03a5e03d6134542dc8c1d8eafc6b63e9f50fcb`
  and the existing typed `retention_class_of` production predicate.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-014 | [VAL-P02-014](../spec.md#success-criteria--verification-plan) | Correct immutable boundary inputs and typed retention oracle | platform | frontmatter | NOT_RUN | pending | Implementation not yet executed; see EVD-P02-140 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-140 | [VAL-P02-014](../spec.md#success-criteria--verification-plan) | WORK-014 | Three named REDs and permitted independent cause review | Unchanged PR135 head with original declared public inventories | FAIL | External named-red receipt `f12a1f14` and corrected causes `3581c1db`; private raw direct audit NOT_OBSERVED/DEFER | rejected |

## Approval and Safety Boundaries

- **Allowed Paths**: This Task, its Spec and Plan, `tests/test_task_execution_contract.py`,
  `tests/test_validation_tooling_ownership.py`.
- **Forbidden Paths**: Production, Registry/schema, templates, archive bodies,
  hooks/gates/limits, and earlier completed evidence.
- **Approval Required**: Existing scoped unit-commit/push/merge authorization
  covers this fixture repair. Exact hosted and integrated-main admission remain
  required for protected delivery; remote actions belong to the delivery owner.
- **Static Validation**: Registered-form first-appearance metadata, hook-first
  final inputs, four existing generation methods and one whitespace method,
  actual staged/message checks, prospective and actual scoped completion,
  separate semantic and available evidence review.
- **Live Validation**: DEFER; repository-only fixtures.
- **Secret / Vault Handling**: No credentials; private raw direct inspection
  rejected by automatic approval review remains deferred, with no workaround.
- **Rollback Plan**: Normal reviewed forward correction preserving all history.
- **Evidence Location**: This Task and external original receipts; ignored
  creation/closing raw attachments bind their actual snapshots.

## Verification Summary

Draft scope only. No implementation or GREEN is claimed. The independent
reviewer accepted the minimum fixture causes using permitted structured
results and public source; private raw direct audit was automatically rejected
and remains NOT_OBSERVED/DEFER. Original RED branches not reached stay
unobserved; thirty local subcase failures do not establish all hosted failures.
All four shared generation methods and the whitespace method are planned,
with the original conservative declarations and closed inventories preserved.
Registered-form provenance, own index/message checks and implementation
results remain pending. Local full and affected execution are excluded;
affected selection metadata may be observed without execution.
