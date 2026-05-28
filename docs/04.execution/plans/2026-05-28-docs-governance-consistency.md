---
title: 'Documentation Governance Consistency Implementation Plan'
type: plan
status: active
owner: platform
updated: 2026-05-28
---

# Documentation Governance Consistency Implementation Plan

---

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스 문서 거버넌스 일관성 정비의 실행 계획서다.
`docs/99.templates/`를 canonical SSoT로 삼아, 템플릿 준수율이 낮은 operations/execution 계층을 우선 정비하고
레거시 파일을 제거한 뒤 CI/훅 스코프를 보완한다.

## Context

워크스페이스의 5개 문서 스테이지(01-05)와 7개 템플릿 타입 중 operations 계층의 템플릿 준수율이 낮다.

- `docs/05.operations/policies`: 14% — AI Agent Policy Section 전체 누락
- `docs/05.operations/runbooks`: 27% — Agent Operations 9/11 누락, Runbook Type 템플릿 미반영
- `docs/04.execution`: Plans 81%, Tasks 60% — status 어휘 불일치, 선택 섹션 불일치
- 레거시 2개 파일, 346KB 감사 문서 경로 오류, post-validate 훅 워크스페이스 스코프 버그

## Goals & In-Scope

- **Goals**: 모든 문서 타입의 템플릿 필수 섹션 준수율 100% 달성, 레거시 파일 제거, CI 정책 게이트 추가
- **In Scope**: policies(7), runbooks(10), guides(일부), plans/tasks 전체, runbook.template.md, post-validate.sh, ci.yml

## Non-Goals & Out-of-Scope

- **Non-goals**: 기능 설계 변경, 인프라 매니페스트 변경
- **Out of Scope**: gitops/ 변경, 클러스터 Live 상태 변경, incidents/ (이미 완료)

## Work Breakdown

| Task    | Description                                                          | Files / Docs Affected                                                              | Validation Criteria     |
| ------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------- |
| PLN-001 | runbook.template.md에 Runbook Type 섹션 추가                         | `docs/99.templates/runbook.template.md`                                            | grep 확인 2 lines       |
| PLN-002 | 레거시 파일 삭제 및 harness audit 이동                               | guides/0005, runbooks/0006, plans+tasks gap-analysis, 90.references/audits/ 신규   | 참조 파일 없음          |
| PLN-003 | policies 7개에 AI Agent Policy Section 추가                          | `docs/05.operations/policies/0001-0007`                                            | 7개 × 1 match           |
| PLN-004 | runbooks 10개 Runbook Type 표준화 + Agent Operations 추가            | `docs/05.operations/runbooks/0001-0011` (0006 제외)                                | RT=1 AO=1 per file      |
| PLN-005 | guides 구조 정렬 — H2 → H3 demote, anchor 수정                       | `docs/05.operations/guides/0002,0006,0007,0008`                                    | H2 이상화 해소          |
| PLN-006 | plans/tasks status 표준화 및 누락 섹션 추가                          | `docs/04.execution/plans/*.md`, `tasks/*.md`                                       | `status: complete` 없음 |
| PLN-007 | docs/01-03 cross-reference 검증                                      | `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`                    | quality gates PASS      |
| PLN-008 | post-validate.sh 스코프 제한 + CI 정책 게이트 + 거버넌스 메모리 기록 | `.claude/hooks/post-validate.sh`, `.github/workflows/ci.yml`, `memory/progress.md` | 훅 workspace-only       |
| PLN-009 | 최종 전체 검증 패스                                                  | 모든 변경 파일                                                                     | pre-commit all pass     |

## Verification Plan

| ID          | Level       | Description                 | Command / How to Run                                                          | Pass Criteria |
| ----------- | ----------- | --------------------------- | ----------------------------------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural  | AI Agent Policy Section 7/7 | `grep -c "AI Agent Policy Section" docs/05.operations/policies/000[1-7]-*.md` | 7파일 × 1     |
| VAL-PLN-002 | Structural  | Runbook Type 10/10          | `grep -l "## Runbook Type" docs/05.operations/runbooks/*.md \| wc -l`         | 10            |
| VAL-PLN-003 | Structural  | Agent Operations 10/10      | `grep -l "## Agent Operations" docs/05.operations/runbooks/*.md \| wc -l`     | 10            |
| VAL-PLN-004 | Structural  | status 어휘                 | `grep -r "^status: complete$" docs/04.execution/`                             | 출력 없음     |
| VAL-PLN-005 | Integration | Quality gates               | `bash scripts/validate-repo-quality-gates.sh .`                               | PASS          |
| VAL-PLN-006 | Integration | Pre-commit                  | `pre-commit run --all-files`                                                  | all pass      |
| VAL-PLN-007 | Integration | 레거시 참조 없음            | `grep -r "0005-new-app\|0006-new-app" docs/`                                  | 출력 없음     |

## Risks & Mitigations

| Risk                                   | Impact | Mitigation                                                 |
| -------------------------------------- | ------ | ---------------------------------------------------------- |
| cross-reference 깨짐                   | High   | 파일 삭제 전 `grep -rl` 로 참조 파일 전수 확인 후 업데이트 |
| markdownlint auto-fix 충돌             | Medium | 영향 파일에 인라인 disable directive 적용                  |
| validate-policy-gates.sh conftest 부재 | Low    | CI 추가 전 graceful exit 0 동작 검증                       |

## Agent Rollout & Evaluation Gates (If Applicable)

N/A — 이 계획은 문서 및 훅 정비 작업이며 AI Agent 모델/프롬프트 배포에 해당하지 않는다.

## Completion Criteria

- [ ] PLN-001~009 모두 완료
- [ ] `validate-repo-quality-gates.sh` PASS
- [ ] `pre-commit run --all-files` all pass
- [ ] 레거시 파일 참조 없음
- [ ] `docs/00.agent-governance/memory/progress.md` 업데이트 완료

## Related Documents

- **Spec**: `[../../03.specs/007-docs-governance-consistency/spec.md]`
- **Tasks**: `[../tasks/2026-05-28-docs-governance-consistency.md]`
