---
title: 'Antigravity Governance Implementation Plan'
type: plan
status: active
owner: 'Antigravity'
updated: 2026-05-30
---

# Antigravity Governance Implementation Plan

---

## Overview (KR)

이 문서는 `docs/00.agent-governance/**`에 정의된 공통 AI Agent 거버넌스를 워크스페이스 목적에 맞게 검토 및 수정하고, 그 결과를 기준으로 `.agents/**`와 `GEMINI.md` 등 Antigravity 전용 하네스 및 도구 구조를 재정비하기 위한 실행 계획서다.

## Context

Gemini (Antigravity) 에이전트가 `hy-home.k8s` 리포지토리에서 워크스페이스 목적에 맞는 특화 하네스를 갖추도록 하기 위함. 특히, 모델 정책(Gemini 3.1 Pro/Gemini 3.5 Flash)과 템플릿 계약 라우팅을 명확히 하는 것이 핵심이다.

## Goals & In-Scope

- **Goals**: 공통 거버넌스와 일관되게 Antigravity(Gemini) 전용 워크스페이스 룰과 워크플로우를 정비한다.
- **In Scope**:
  - `docs/00.agent-governance/providers/gemini.md` 갱신
  - `.agents/GEMINI.md` 갱신
  - `.agents/rules/workspace-rules.md` 생성
  - `.agents/workflows/qa-cicd-workflow.md` 생성

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- |
| PLN-001 | 공통 거버넌스 갱신 | `docs/00.agent-governance/providers/gemini.md` | GOV-01 | 하네스 구조 및 정책 추가 |
| PLN-002 | 로컬 베이스라인 갱신 | `.agents/GEMINI.md` | GOV-02 | 템플릿 계약 및 워크플로우 명시 |
| PLN-003 | 전용 규칙 생성 | `.agents/rules/workspace-rules.md` | GOV-03 | Template-first 내용 작성 |
| PLN-004 | 전용 워크플로우 생성 | `.agents/workflows/qa-cicd-workflow.md` | GOV-04 | QA/CI/CD 단계 정의 |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | 파일 존재 여부 | `ls -l .agents/rules/` | `workspace-rules.md` 확인 |
| VAL-PLN-002 | Content | 모델 정책 명시 | `grep "Gemini 3.1 Pro" .agents/GEMINI.md` | 결과가 존재해야 함 |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **Tasks**: `[../tasks/2026-05-30-antigravity-governance.md]`

## Non-Goals & Out-of-Scope

- N/A

## Risks & Mitigations

- N/A
