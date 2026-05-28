---
title: 'Workspace Skill Expansion Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-05-28
---

# Workspace Skill Expansion Implementation Plan

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스에서 SDD 라이프사이클과 운영 자동화를
보강하는 5개 신규 로컬 스킬 생성 실행 계획이다.
22개 P0 워크스트림 감사(2026-05-28)에서 식별된 P0-16 갭을 해소한다.

## Context

2026-05-28 워크스페이스 개선 미션(Coverage Ledger + Integrated Gap Analysis)
수행 결과 `.claude/skills/` 에 7개 후보 스킬 중 5개가 누락된 것이 확인되었다.
기존 11개 스킬은 GitOps/Kubernetes/문서 라우팅/감사 워크플로우를 커버하지만,
SDD 라이프사이클 연결(요구사항→설계, 설계→계획, 계획→태스크)과
운영 런북 작성/거버넌스 인덱스 유지 패턴이 로컬 스킬로 명시되지 않았다.

## Goals & In-Scope

- **Goals**: 5개 신규 워크스페이스 전용 스킬 생성, harness-catalog 업데이트, progress.md 기록
- **In Scope**:
  - `.claude/skills/requirements-to-design/skill.md`
  - `.claude/skills/execution-plan/skill.md`
  - `.claude/skills/task-breakdown/skill.md`
  - `.claude/skills/ops-runbook/skill.md`
  - `.claude/skills/knowledge-map/skill.md`
  - `docs/00.agent-governance/harness-catalog.md` Skills 표 + Task-to-Skill Routing 업데이트
  - `docs/00.agent-governance/memory/progress.md` 신규 항목 추가

## Non-Goals & Out-of-Scope

- Compose Stack Agent: Docker Compose 범위가 외부 서비스 워크스페이스 소속; 연기
- Policy Gate Agent: OPA/Conftest P3 deferrals 미완료; 연기
- .codex/agents/ TOML 미러: 스킬 파일은 agent 미러 대상이 아님 (agents/\*.md만 미러)
- 구조적 변경 없는 파일 대량 수정

## Requirements & Acceptance Criteria

| ID     | 요구사항                            | 완료 기준                    |
| ------ | ----------------------------------- | ---------------------------- |
| REQ-01 | 5개 스킬 파일 생성                  | 파일 존재 + frontmatter 포함 |
| REQ-02 | harness-catalog Skills 표 업데이트  | 5개 신규 항목 추가           |
| REQ-03 | Task-to-Skill Routing 표 업데이트   | SDD lifecycle 라우팅 행 추가 |
| REQ-04 | progress.md 항목 추가               | 이 미션 결과 기록            |
| REQ-05 | validate-repo-quality-gates.sh 통과 | 종료 코드 0                  |

## Work Breakdown

| 단계 | 작업                                | 우선순위 |
| ---- | ----------------------------------- | -------- |
| 1    | 5개 스킬 파일 생성                  | P1       |
| 2    | harness-catalog.md 업데이트         | P1       |
| 3    | progress.md 업데이트                | P1       |
| 4    | validate-repo-quality-gates.sh 실행 | P1       |

## Risks & Mitigations

| 위험                                             | 완화                                       |
| ------------------------------------------------ | ------------------------------------------ |
| harness-catalog 업데이트 누락으로 스킬 발견 불가 | 스킬 생성 직후 catalog 업데이트            |
| 스킬 범위 과도한 확장                            | 각 스킬은 명확한 When NOT to Use 섹션 포함 |

## Verification Plan

```bash
bash scripts/validate-repo-quality-gates.sh .
ls .claude/skills/requirements-to-design/skill.md
ls .claude/skills/execution-plan/skill.md
ls .claude/skills/task-breakdown/skill.md
ls .claude/skills/ops-runbook/skill.md
ls .claude/skills/knowledge-map/skill.md
```

## Agent Rollout & Evaluation Gates (If Applicable)

N/A — 이 계획은 인프라 및 문서 작업을 다루며 AI Agent 모델/프롬프트 배포에 해당하지 않는다.

## Completion Criteria

- 5개 스킬 파일이 `.claude/skills/` 아래 각각 `skill.md`로 존재한다.
- `docs/00.agent-governance/harness-catalog.md` Skills 표에 5개 신규 행이 추가된다.
- Task-to-Skill Routing 표에 SDD lifecycle 라우팅 행이 추가된다.
- `docs/00.agent-governance/memory/progress.md`에 이 미션 항목이 기록된다.
- `bash scripts/validate-repo-quality-gates.sh .` 종료 코드 0.

## Rollback

- 신규 스킬 파일 삭제
- harness-catalog.md에서 추가된 행 제거
- progress.md에서 추가된 항목 제거

## Related Documents

- Parent Gap Analysis: `../../00.agent-governance/memory/progress.md`
- Task record: `../tasks/2026-05-28-workspace-skill-expansion.md`
- harness-catalog: `../../00.agent-governance/harness-catalog.md`
- Spec 006: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`
