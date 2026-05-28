---
title: 'Task: Documentation Governance Consistency'
type: task
status: active
owner: platform
updated: 2026-05-28
---

# Task: Documentation Governance Consistency

---

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스 문서 거버넌스 일관성 정비의 작업 추적 문서다.
`docs/03.specs/007-docs-governance-consistency/spec.md`와 `docs/04.execution/plans/2026-05-28-docs-governance-consistency.md`에서 파생된 작업을 추적한다.

## Inputs

- **Parent Spec**: `[../../03.specs/007-docs-governance-consistency/spec.md]`
- **Parent Plan**: `[../plans/2026-05-28-docs-governance-consistency.md]`

## Working Rules

- 문서 전용 작업이며 인프라 매니페스트는 변경하지 않는다.
- 각 작업 완료 후 검증 커맨드를 실행하고 결과를 Evidence에 기록한다.
- 레거시 파일은 cross-reference 업데이트 완료 후 삭제한다.
- `validate-repo-quality-gates.sh` 통과를 각 커밋의 완료 조건으로 삼는다.

## Task Table

| Task ID | Description                                                                                    | Type | Parent Plan | Validation / Evidence       | Owner    | Status |
| ------- | ---------------------------------------------------------------------------------------------- | ---- | ----------- | --------------------------- | -------- | ------ |
| T-001   | runbook.template.md에 `## Runbook Type` 섹션 삽입                                              | doc  | PLN-001     | grep "Runbook Type" 2 lines | platform | Todo   |
| T-002   | guides/0005, runbooks/0006 삭제; gap-analysis → 90.references/audits/ 이동; cross-ref 업데이트 | doc  | PLN-002     | 참조 grep 없음              | platform | Todo   |
| T-003   | policies 0001-0007에 `## AI Agent Policy Section` 추가                                         | doc  | PLN-003     | 7파일 × 1 match             | platform | Todo   |
| T-004   | runbooks 0001-0011(0006제외) Runbook Type 표준화 + Agent Operations 추가                       | doc  | PLN-004     | RT=1 AO=1 per 10 files      | platform | Todo   |
| T-005   | guides 구조 정렬 — H2 → H3 demote, broken anchor 수정                                          | doc  | PLN-005     | H2 이상화 해소 확인         | platform | Todo   |
| T-006   | plans/tasks `status: complete` → `done` 일괄 변환; 누락 Agent Rollout 섹션 추가                | doc  | PLN-006     | `grep status:complete` 없음 | platform | Todo   |
| T-007   | docs/01-03 cross-reference 검증 패스                                                           | doc  | PLN-007     | quality gates PASS          | platform | Todo   |
| T-008   | post-validate.sh 워크스페이스 스코프 제한; CI validate-policy-gates 추가; progress.md 업데이트 | ops  | PLN-008     | 훅 외부파일 미실행 확인     | platform | Todo   |
| T-009   | 최종 전체 검증 패스                                                                            | ops  | PLN-009     | pre-commit all pass         | platform | Todo   |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1 — Template & Legacy (T-001, T-002)

- [ ] T-001 runbook.template.md Runbook Type 섹션 추가
- [ ] T-002 레거시 파일 삭제 및 audit 문서 이동

### Phase 2 — Operations Compliance (T-003, T-004, T-005)

- [ ] T-003 policies AI Agent Policy Section 추가
- [ ] T-004 runbooks Runbook Type + Agent Operations 표준화
- [ ] T-005 guides H2 → H3 구조 정렬

### Phase 3 — Execution & CI (T-006, T-007, T-008)

- [ ] T-006 plans/tasks status 표준화
- [ ] T-007 docs/01-03 cross-reference 검증
- [ ] T-008 훅 스코프 제한 + CI 정책 게이트 + 거버넌스 메모리 기록

### Phase 4 — Final Validation (T-009)

- [ ] T-009 최종 전체 검증 패스

## Verification Summary

- **Test Commands**: `bash scripts/validate-repo-quality-gates.sh .`
- **Eval Commands**: `pre-commit run --all-files`
- **Logs / Evidence Location**: 각 커밋 메시지 및 `docs/00.agent-governance/memory/progress.md`

## Related Documents

- **Spec**: `[../../03.specs/007-docs-governance-consistency/spec.md]`
- **Plan**: `[../plans/2026-05-28-docs-governance-consistency.md]`
