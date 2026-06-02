---
title: 'Task: {Task Name}'
type: task
status: draft
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md -->

# Task: [Task Name]

> Use this template for `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`.
>
> Rules:
>
> - Task documents are traceability-first.
> - Core behavior should default to TDD.
> - Agent work must include eval tasks where applicable.
> - This is the canonical execution-tracking location; feature-local task notes under `03.specs/` are secondary.
> - Use relative links only, calculated from the final authored document location.

---

## Overview (KR)

이 문서는 [기능 또는 작업 흐름명]의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Parent Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- Repo-static validation must not be reported as live runtime readiness unless a separate live check was approved and run.
- If a feature-local `tasks.md` exists under `03.specs/`, this document remains the execution-tracking source of truth.
- Remove optional boilerplate sections when they do not add task-specific evidence or execution clarity.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner  | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ------ | ------ |
| T-001   | [Action]    | impl | SPC-001 / §2          | Phase 1             | `pytest ...`          | [Name] | Todo   |

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

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`.

- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`
- **Tests**: `[../../03.specs/<feature-id>/tests.md]`
