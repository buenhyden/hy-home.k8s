<!-- Target: docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md -->
# Task: [Task Name]

> Use this template for `docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md`.
>
> Rules:
>
> - Task documents are traceability-first.
> - Core behavior should default to TDD.
> - Agent work must include eval tasks where applicable.
> - This is the execution-tracking location.
> - Feature-local task notes under `04.specs/` are secondary.

---

## Overview (KR)

이 문서는 [기능 또는 작업 흐름명]의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../04.specs/<feature-id>/spec.md]`
- **Parent Plan**: `[../05.plans/YYYY-MM-DD-<feature>.md]`

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `04.specs/`,
- This document remains the source of truth.

## Task Table

| ID | Task | Type | Spec | Plan | Proof | Owner | Stat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | [Action] | impl | SPC-001 | P1 | `pytest` | [Name] | Todo |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [ ] T-001 [Description]

### Phase 2

- [ ] T-002 [Description]

## Verification Summary

- **Test Commands**:
- **Eval Commands**:
- **Logs / Evidence Location**:
