---
title: 'Task: Template Cross-link Fix'
type: task
status: done
owner: platform
updated: 2026-05-21
---

# Task: Template Cross-link Fix

---

## Overview (KR)

이 문서는 `docs/99.templates/` 템플릿 파일들의 Cross-link 플레이스홀더 경로 정합화 및
생성된 문서 표시 텍스트(backtick 코드) 수정 작업의 실행 추적 문서다.
2026-05-17~2026-05-21 기간에 완료되었으며, 현재 템플릿 링크 규칙의 정본은
`docs/99.templates/README.md`와 `docs/00.agent-governance/rules/documentation-protocol.md`에 위치한다.

## Inputs

- **Parent Plan**: `[../plans/2026-05-17-template-crosslink-fix.md]`

## Working Rules

- 문서 전용 작업이며 인프라 매니페스트는 변경하지 않는다.
- 실제 href 링크 경로는 변경하지 않는다 (href는 이미 올바름).
- 표시 텍스트(backtick code label)만 href와 일치시킨다.

## Task Table

| Task ID | Description                                                    | Type | Parent Plan | Validation / Evidence                                  | Owner    | Status |
| ------- | -------------------------------------------------------------- | ---- | ----------- | ------------------------------------------------------ | -------- | ------ |
| T-001   | adr.template.md — Related Documents 경로 수정                  | doc  | T-01        | `../../01.requirements/`, `../requirements/` 패턴 적용 | platform | Done   |
| T-002   | ard.template.md — Related Documents 경로 수정                  | doc  | T-02        | 4개 경로 수정 완료                                     | platform | Done   |
| T-003   | plan.template.md — Related Documents 경로 수정                 | doc  | T-03        | 4개 경로 수정 완료                                     | platform | Done   |
| T-004   | task.template.md — Inputs + Related Documents 경로 수정        | doc  | T-04        | 5개 경로 수정 완료                                     | platform | Done   |
| T-005   | guide.template.md — Related Documents 경로 수정                | doc  | T-05        | 3개 경로 수정 완료                                     | platform | Done   |
| T-006   | runbook.template.md — Canonical References + Related 경로 수정 | doc  | T-06        | 7개 경로 수정 완료                                     | platform | Done   |
| T-007   | incident.template.md — Runbook Link + Related 경로 수정        | doc  | T-07        | 3개 경로 수정 완료                                     | platform | Done   |
| T-008   | postmortem.template.md — Incident Document + Related 수정      | doc  | T-08        | 4개 경로 수정 완료                                     | platform | Done   |
| T-009   | policy.template.md — Related Documents 경로 수정            | doc  | T-09        | 3개 경로 수정 완료                                     | platform | Done   |
| T-010   | reference.template.md — Related Documents 경로 수정            | doc  | T-10        | 2개 경로 수정 완료                                     | platform | Done   |
| T-011   | ADR 생성 파일 표시 텍스트 수정 (9개)                           | doc  | T-11        | backtick label = href 일치 확인                        | platform | Done   |
| T-012   | ARD 생성 파일 표시 텍스트 수정 (3개)                           | doc  | T-12        | backtick label = href 일치 확인                        | platform | Done   |
| T-013   | Plan 생성 파일 표시 텍스트 수정 (6개)                          | doc  | T-13        | backtick label = href 일치 확인                        | platform | Done   |
| T-014   | Task 생성 파일 표시 텍스트 수정 (6개)                          | doc  | T-14        | backtick label = href 일치 확인                        | platform | Done   |
| T-015   | Guide 생성 파일 표시 텍스트 수정 (5개)                         | doc  | T-15        | backtick label = href 일치 확인                        | platform | Done   |
| T-016   | Runbook 생성 파일 표시 텍스트 수정 (4개)                       | doc  | T-16        | backtick label = href 일치 확인                        | platform | Done   |
| T-017   | 최종 통합 검증                                                 | ops  | T-17        | `validate-repo-quality-gates.sh` PASS                  | platform | Done   |

## Suggested Types

- `doc`
- `ops`

## Phase View

### Phase 1 — Template Cross-link Fix (T-001~T-010)

- [x] T-001 adr.template.md 경로 수정
- [x] T-002 ard.template.md 경로 수정
- [x] T-003 plan.template.md 경로 수정
- [x] T-004 task.template.md 경로 수정
- [x] T-005 guide.template.md 경로 수정
- [x] T-006 runbook.template.md 경로 수정
- [x] T-007 incident.template.md 경로 수정
- [x] T-008 postmortem.template.md 경로 수정
- [x] T-009 policy.template.md 경로 수정
- [x] T-010 reference.template.md 경로 수정

### Phase 2 — Generated Document Label Fix (T-011~T-016)

- [x] T-011 ADR 9개 표시 텍스트 수정
- [x] T-012 ARD 3개 표시 텍스트 수정
- [x] T-013 Plan 6개 표시 텍스트 수정
- [x] T-014 Task 6개 표시 텍스트 수정
- [x] T-015 Guide 5개 표시 텍스트 수정
- [x] T-016 Runbook 4개 표시 텍스트 수정

### Phase 3 — Final Validation (T-017)

- [x] T-017 최종 통합 검증 완료

## Verification Summary

- **Test Commands**: `bash scripts/validate-repo-quality-gates.sh .` — PASS (2026-05-21)
- **Eval Commands**: `pre-commit run --all-files` — all pass
- **Logs / Evidence Location**: `docs/04.execution/plans/2026-05-17-template-crosslink-fix.md` (Completion Criteria 항목)

## Related Documents

- **Plan**: `[../plans/2026-05-17-template-crosslink-fix.md]`
- **Templates**: `[../../99.templates/README.md]`
- **Documentation Protocol**: `[../../00.agent-governance/rules/documentation-protocol.md]`
