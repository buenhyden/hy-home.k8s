---
title: 'Task: Workspace Skill Expansion (P0-16)'
type: task
status: done
owner: 'platform'
updated: 2026-05-28
---

# Task: Workspace Skill Expansion (P0-16)

## Overview (KR)

이 문서는 P0-16 워크스페이스 전용 AI Agent 스킬 5개 생성 작업의 구현 및 검증 기록이다.
`docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md` 계획에서 파생된 작업을 추적한다.

## Inputs

- **Parent Plan**: `../plans/2026-05-28-workspace-skill-expansion.md`
- **Parent Spec**: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`

## Working Rules

- Every task must define evidence.
- Documentation-only work still needs validation evidence.

## Task Table

| Task ID | Description                                                 | Type | Parent Plan / Phase | Validation / Evidence                                                          | Owner    | Status |
| ------- | ----------------------------------------------------------- | ---- | ------------------- | ------------------------------------------------------------------------------ | -------- | ------ |
| T-001   | Create `.claude/skills/requirements-to-design/skill.md`     | doc  | Phase 1             | `ls .claude/skills/requirements-to-design/skill.md`                            | platform | Done   |
| T-002   | Create `.claude/skills/execution-plan/skill.md`             | doc  | Phase 1             | `ls .claude/skills/execution-plan/skill.md`                                    | platform | Done   |
| T-003   | Create `.claude/skills/task-breakdown/skill.md`             | doc  | Phase 1             | `ls .claude/skills/task-breakdown/skill.md`                                    | platform | Done   |
| T-004   | Create `.claude/skills/ops-runbook/skill.md`                | doc  | Phase 1             | `ls .claude/skills/ops-runbook/skill.md`                                       | platform | Done   |
| T-005   | Create `.claude/skills/knowledge-map/skill.md`              | doc  | Phase 1             | `ls .claude/skills/knowledge-map/skill.md`                                     | platform | Done   |
| T-006   | Update harness-catalog.md Skills table (5 entries)          | doc  | Phase 2             | `grep -c 'requirements-to-design' docs/00.agent-governance/harness-catalog.md` | platform | Done   |
| T-007   | Update harness-catalog.md Task-to-Skill Routing (3 rows)    | doc  | Phase 2             | `grep 'SDD lifecycle' docs/00.agent-governance/harness-catalog.md`             | platform | Done   |
| T-008   | Fix validate-repo-quality-gates.sh pipe-table normalization | impl | Phase 2             | `bash scripts/validate-repo-quality-gates.sh .` exit 0                         | platform | Done   |
| T-009   | Create plan artifact                                        | doc  | Phase 2             | `ls docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`           | platform | Done   |
| T-010   | Create this task artifact                                   | doc  | Phase 2             | `ls docs/04.execution/tasks/2026-05-28-workspace-skill-expansion.md`           | platform | Done   |
| T-011   | Update progress.md                                          | doc  | Phase 2             | Entry exists in progress.md                                                    | platform | Done   |

## Suggested Types

- `doc`
- `impl`

## Verification Summary

- **Test Commands**:

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  ls .claude/skills/requirements-to-design/skill.md
  ls .claude/skills/execution-plan/skill.md
  ls .claude/skills/task-breakdown/skill.md
  ls .claude/skills/ops-runbook/skill.md
  ls .claude/skills/knowledge-map/skill.md
  ```

- **Logs / Evidence Location**: `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Plan**: `../plans/2026-05-28-workspace-skill-expansion.md`
- **Spec**: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`
- **Harness Catalog**: `../../00.agent-governance/harness-catalog.md`
