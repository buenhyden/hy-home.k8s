---
title: 'Template Cross-link Fix Implementation Plan'
type: plan
status: complete
owner: 'platform-team'
updated: 2026-05-21
---

# Template Cross-link Fix Implementation Plan

> Use this plan to fix relative path placeholders in all `docs/99.templates/` files and
> to synchronise the display text (backtick code) in every generated document with its
> actual href.
>
> **For agentic workers:** Execute each `- [ ]` step in order. Use `superpowers:executing-plans`
> or `superpowers:subagent-driven-development` to implement task-by-task.

---

## Overview (KR)

이 계획은 `docs/99.templates/` 템플릿 파일들의 Cross-link 플레이스홀더 경로를 Target 위치 기준 올바른 상대 경로로 수정하고,
이미 생성된 문서의 표시 텍스트(backtick 코드)를 실제 href와 일치시키는 작업을 정의한다.

현재 문제: 템플릿의 `Related Documents` 플레이스홀더가 `../` 한 단계 이동을 기준으로 작성되었으나,
대부분의 Target 위치(`decisions/`, `tasks/`, `runbooks/` 등)는 `docs/` 루트까지 2단계 이상 이동이 필요하다.
생성된 파일들의 실제 href는 올바르지만, 표시 텍스트(backtick)가 잘못된 플레이스홀더를 그대로 복사하여 불일치 상태다.

## Context

분석 결과:

- `spec.template.md`와 `prd.template.md`는 이미 올바른 상대 경로를 사용함 (변경 불필요)
- 10개 템플릿은 `../`을 `../../`로 또는 형제 디렉터리 상대 경로로 수정 필요
- 나머지 Target 주석이 있는 Markdown 템플릿 6개는 이미 target-relative placeholder를 사용함
- 생성된 문서와 stage README 53개 파일의 표시 텍스트가 실제 href와 불일치 (링크 동작은 정상)
- 각 Template의 `<!-- Target: ... -->` 주석이 올바른 Target 위치를 명시하고 있으므로 이를 기준으로 상대 경로 계산
- 실제 Markdown 링크는 `docs/99.templates/` 파일 위치 기준으로 검증하고, backtick code literal placeholder는 Target 위치 기준으로 검증

경로 계산 원칙:

- `docs/02.architecture/decisions/` → `docs/` 루트까지 `../../` 필요
- `docs/04.execution/tasks/` → `docs/` 루트까지 `../../` 필요, 형제 `plans/`는 `../plans/`
- `docs/05.operations/runbooks/` → `docs/` 루트까지 `../../`, 형제 `guides/`, `policies/`는 `../`
- `docs/05.operations/incidents/YYYY/` → `05.operations/`까지 `../../`, `docs/` 루트까지 `../../../`
- `docs/05.operations/incidents/postmortems/YYYY/` → `05.operations/`까지 `../../../`

## Goals & In-Scope

- **Goals**:
  - 16개 Target-bearing Markdown 템플릿의 Cross-link 플레이스홀더를 Target 위치 기준으로 검토
  - 수정이 필요한 10개 템플릿의 Cross-link 플레이스홀더를 올바른 상대 경로로 수정
  - 50개 이상 생성 문서와 README 표면의 표시 텍스트(backtick 코드)를 실제 href와 일치시킴
- **In Scope**:
  - `docs/99.templates/` 내 Cross-link가 있는 10개 템플릿 파일
  - `docs/99.templates/` 내 이미 정합한 Target-bearing helper template 6개 검토
  - `docs/02.architecture/decisions/*.md` (ADR 9개)
  - `docs/02.architecture/requirements/*.md` (ARD 3개)
  - `docs/04.execution/plans/*.md` (Plan 6개)
  - `docs/04.execution/tasks/*.md` (Task 6개)
  - `docs/05.operations/guides/*.md` (Guide 5개 — 링크 불일치 있는 것)
  - `docs/05.operations/runbooks/*.md` (Runbook 4개)
  - Root, docs stage, and examples README 문서의 code-label/href 정합성

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 실제 href 링크 경로 변경 (href는 이미 올바름)
  - 문서 내용(Content) 변경
  - PRD/Spec 본문 파일 수정 (PRD/Spec 템플릿과 본문 링크는 이미 올바름)
- **Out of Scope**:
  - `docs/05.operations/incidents/` — 현재 incident 파일 없음
  - `docs/90.references/` — 현재 reference 파일 없음
  - `docs/00.agent-governance/` 거버넌스 파일

## Work Breakdown

| Task | Description                        | Files / Docs Affected                            | Target REQ  | Validation Criteria                                                       |
| ---- | ---------------------------------- | ------------------------------------------------ | ----------- | ------------------------------------------------------------------------- |
| T-01 | adr.template.md 경로 수정          | `docs/99.templates/adr.template.md`              | REQ-TMP-001 | Related Documents의 4개 경로가 `../../` 또는 `../requirements/` 패턴 사용 |
| T-02 | ard.template.md 경로 수정          | `docs/99.templates/ard.template.md`              | REQ-TMP-001 | Related Documents의 4개 경로 수정                                         |
| T-03 | plan.template.md 경로 수정         | `docs/99.templates/plan.template.md`             | REQ-TMP-001 | Related Documents의 4개 경로 수정                                         |
| T-04 | task.template.md 경로 수정         | `docs/99.templates/task.template.md`             | REQ-TMP-001 | Inputs + Related Documents 5개 경로 수정                                  |
| T-05 | guide.template.md 경로 수정        | `docs/99.templates/guide.template.md`            | REQ-TMP-001 | Related Documents 3개 경로 수정                                           |
| T-06 | runbook.template.md 경로 수정      | `docs/99.templates/runbook.template.md`          | REQ-TMP-001 | Canonical References 4개 + Related Documents 3개 수정                     |
| T-07 | incident.template.md 경로 수정     | `docs/99.templates/incident.template.md`         | REQ-TMP-001 | Runbook Link 셀 + Related Documents 2개 수정                              |
| T-08 | postmortem.template.md 경로 수정   | `docs/99.templates/postmortem.template.md`       | REQ-TMP-001 | Incident Document 셀 + Related Documents 3개 수정                         |
| T-09 | operation.template.md 경로 수정    | `docs/99.templates/operation.template.md`        | REQ-TMP-001 | Related Documents 3개 수정                                                |
| T-10 | reference.template.md 경로 수정    | `docs/99.templates/reference.template.md`        | REQ-TMP-001 | Related Documents 2개 수정                                                |
| T-11 | ADR 생성 파일 표시 텍스트 수정     | `docs/02.architecture/decisions/000{1-9}*.md`    | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-12 | ARD 생성 파일 표시 텍스트 수정     | `docs/02.architecture/requirements/000{1-3}*.md` | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-13 | Plan 생성 파일 표시 텍스트 수정    | `docs/04.execution/plans/2026-*.md` (6개)        | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-14 | Task 생성 파일 표시 텍스트 수정    | `docs/04.execution/tasks/2026-*.md` (6개)        | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-15 | Guide 생성 파일 표시 텍스트 수정   | `docs/05.operations/guides/000{1-4,8}*.md`       | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-16 | Runbook 생성 파일 표시 텍스트 수정 | `docs/05.operations/runbooks/000{1-4}*.md`       | REQ-GEN-001 | backtick 표시 텍스트가 href와 일치                                        |
| T-17 | 최종 통합 검증                     | 전체 docs/                                       | REQ-VAL-001 | 스캔 명령 출력 없음                                                       |

## Template Coverage Matrix

| Template | Target scope | Result |
| --- | --- | --- |
| `prd.template.md` | `docs/01.requirements/` | Already target-relative |
| `ard.template.md` | `docs/02.architecture/requirements/` | Fixed before final integration |
| `adr.template.md` | `docs/02.architecture/decisions/` | Fixed before final integration |
| `spec.template.md` | `docs/03.specs/<feature-id>/` | Already target-relative |
| `api-spec.template.md` | `docs/03.specs/<feature-id>/` | Already target-relative |
| `agent-design.template.md` | `docs/03.specs/<feature-id>/` | Already target-relative |
| `data-model.template.md` | `docs/03.specs/<feature-id>/` | Already target-relative |
| `tests.template.md` | `docs/03.specs/<feature-id>/` | Already target-relative |
| `plan.template.md` | `docs/04.execution/plans/` | Fixed before final integration |
| `task.template.md` | `docs/04.execution/tasks/` | Fixed before final integration |
| `guide.template.md` | `docs/05.operations/guides/` | Fixed before final integration |
| `operation.template.md` | `docs/05.operations/policies/` | Fixed in final integration |
| `runbook.template.md` | `docs/05.operations/runbooks/` | Fixed before final integration |
| `incident.template.md` | `docs/05.operations/incidents/YYYY/` | Fixed in final integration |
| `postmortem.template.md` | `docs/05.operations/incidents/postmortems/YYYY/` | Fixed in final integration |
| `reference.template.md` | `docs/90.references/<category>/` | Fixed in final integration |

`readme.template.md` has no fixed Target because README files live at multiple
depths. Its example links must either resolve relative to the template file or be
rewritten by the author for the final README location.

## Verification Plan

| ID          | Level      | Description                       | Command / How to Run                                                                                                     | Pass Criteria                                                                                |
| ----------- | ---------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| VAL-PLN-001 | Structural | 템플릿 경로 패턴 확인             | `grep -n "Related Documents" -A 6 docs/99.templates/adr.template.md`                                                     | `../../01.requirements/`, `../requirements/`, `../../03.specs/`, `../../04.execution/plans/` |
| VAL-PLN-002 | Structural | 생성 파일 불일치 스캔             | fenced code block을 제외하고 backtick code label과 href를 직접 비교                                                     | mismatch 0건                                                                                 |
| VAL-PLN-003 | Structural | 내부 Markdown 링크 존재 확인      | fenced code block을 제외하고 `README.md`와 `docs/**/*.md`의 상대 Markdown 링크 target을 확인                              | missing target 0건                                                                           |
| VAL-PLN-004 | Content    | 실제 파일 존재 확인               | `ls docs/02.architecture/requirements/0001-wsl-k3d-argocd-platform.md docs/03.specs/001-wsl-k3d-argocd-platform/spec.md` | 두 파일 모두 존재                                                                            |

## Risks & Mitigations

| Risk                                 | Impact | Mitigation                                                      |
| ------------------------------------ | ------ | --------------------------------------------------------------- |
| 표시 텍스트 수정 중 href 실수로 변경 | High   | Edit 도구의 old_string/new_string을 표시 텍스트만 정확히 타겟팅 |
| 파일 수가 많아 일부 누락             | Medium | Task 17 통합 검증 스캔으로 전수 확인                            |
| hook이 다른 품질 게이트 위반 감지    | Low    | 각 Task 완료 후 즉시 검증 명령 실행                             |

## Completion Criteria

- [x] 16개 Target-bearing Markdown 템플릿 검토 완료
- [x] 수정이 필요한 10개 템플릿 파일의 Cross-link 플레이스홀더가 Target 위치 기준 올바른 상대 경로 사용
- [x] 50개 이상 생성 문서와 README 표면의 표시 텍스트(backtick)가 실제 href와 일치
- [x] fenced code block 제외 Markdown 링크 target 확인에서 missing target 0건
- [x] fenced code block 제외 code-label/href 비교에서 mismatch 0건
- [x] `docs/00.agent-governance/memory/progress.md`에 작업 완료 entry 추가

## Template Improvement Plan

`docs/99.templates/readme.template.md` is intentionally generic, but README
targets vary by directory depth. A future template hardening pass should add
target-specific path guidance for root README, `docs/README.md`, and nested
stage READMEs, or convert the instructional example links into code literal path
tables so authors must recalculate final relative links for the target location.

## Historical Execution Notes

이 계획서는 2026-05-17에 템플릿 cross-link 정합화 작업을 완료한 이력 문서다. 기존 `Task Detail` 섹션에는 이미 완료된 T-01부터 T-17까지의 단계별 실행 지시가 unchecked checklist 형태로 남아 있어, `status: complete`와 충돌하고 후속 독자가 재실행 작업으로 오해할 수 있었다.

보존된 완료 증적:

- Work Breakdown 표의 T-01부터 T-17까지의 작업 범위와 검증 기준
- Template Coverage Matrix
- Verification Plan과 Completion Criteria
- Related Documents

## Migration Note

- 파일 삭제, 이동, 이름 변경은 수행하지 않았다.
- `rg` 기준으로 이 파일 외부에서 제거 대상 `Task Detail` heading이나 하위 task heading을 참조하는 링크는 없었다.
- 상세 실행 지시는 완료 이력으로 통합하고, 현재 템플릿 링크 규칙의 정본은 `docs/99.templates/README.md`와 `docs/00.agent-governance/rules/documentation-protocol.md`에 둔다.

## Related Documents

- **Templates**: [`../../99.templates/README.md`](../../99.templates/README.md)
- **Documentation Protocol**: [`../../00.agent-governance/rules/documentation-protocol.md`](../../00.agent-governance/rules/documentation-protocol.md)
- **Stage Authoring Matrix**: [`../../00.agent-governance/rules/stage-authoring-matrix.md`](../../00.agent-governance/rules/stage-authoring-matrix.md)
