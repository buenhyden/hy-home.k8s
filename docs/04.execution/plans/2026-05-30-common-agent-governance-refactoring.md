---
title: 'Common Agent Governance Refactoring Plan'
type: plan
status: active
owner: 'platform'
updated: 2026-05-30
---


# Common Agent Governance Refactoring Plan

>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.
> - Use relative links only, calculated from the final authored document location.

---

## Overview (KR)

이 문서는 워크스페이스 내 AI 에이전트 거버넌스(Stage 00)를 일관되게 정비하기 위한 실행 계획서다. 템플릿 계약 위반(ARD 네이밍, Policy 템플릿 부재)을 수정하고, 공식 2026-05-29 모델(Gemini 3.1 Pro 등) 기준을 모델 정책에 확립하며, 플랫폼별 하네스가 공통 문서를 중복 없이 참조하도록 재구성한다.

## Context

각 에이전트(Claude, GPT, Gemini) 플랫폼의 구조가 파편화되는 것을 방지하고, 템플릿과 실제 산출물 간의 불일치를 해소하기 위함이다.

## Goals & In-Scope

- **Goals**:
  - 모든 템플릿(policy.template.md 포함)이 README.md 매핑과 실제 파일 구조와 100% 일치하도록 보장한다.
  - ARD 파일명을 템플릿 규약(####-<system-or-domain>.md)에 맞춘다.
  - 모델 정책을 2026-05-29 기준 공식 최신 모델로 고정한다.
- **In Scope**:
  - `docs/99.templates/` 내 파일 이름 변경 및 README 갱신
  - `docs/02.architecture/requirements/` 파일명 리팩터링
  - `docs/00.agent-governance/model-policy.md` 업데이트
  - 플랫폼 하네스(`.agents/GEMINI.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`)의 어댑터-레퍼런스 구조 갱신

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 기존 작성된 설계 문서들의 내부 로직이나 내용 자체의 큰 수정 (파일명 갱신 및 템플릿 갱신 제외)
- **Out of Scope**:
  - Kubernetes 매니페스트 자체 기능 변경
  - 외부 연동 시스템의 스크립트 리팩터링

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- |
| PLN-001 | 템플릿 계약 일치화 | `docs/99.templates/*` | PRD-GOV-02 | README와 파일명이 일치하고, policy 템플릿이 존재함 |
| PLN-002 | ARD 파일 리네임 | `docs/02.architecture/requirements/*.md` | PRD-GOV-04 | 모든 ARD가 `0001-*.md` 형태로 네이밍됨 |
| PLN-003 | 모델 정책 확정 | `docs/00.agent-governance/model-policy.md` | PRD-GOV-01 | 최신 모델명 확정 및 레거시 삭제 |
| PLN-004 | 플랫폼 하네스 어댑터 확인 | `.agents/`, `.claude/`, `.codex/` | PRD-GOV-03 | 각 마크다운이 중복 없이 SSoT를 참조함 |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | Template mapping | `scripts/validate-repo-quality-gates.sh .` | Structural template mapping errors = 0 |

## Risks & Mitigations

| Risk   | Impact | Mitigation   |
| ------ | ------ | ------------ |
| ARD 파일명 갱신 시 기존 문서의 내부 참조 링크 깨짐 | Medium | 일괄 리네임 시 `grep`을 통해 기존 링크들을 함께 업데이트한다. |

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

- **Tasks**: `[../tasks/2026-05-30-governance-refactoring.md]`
