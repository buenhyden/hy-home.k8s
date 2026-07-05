---
title: 'Reference: Workspace Harness Gap Analysis'
type: content/reference
status: active
owner: platform
updated: 2026-05-28
---

# Reference: Workspace Harness Gap Analysis

---

## Overview

이 문서는 2026-05-24에 수행된 `hy-home.k8s` 워크스페이스 전체 거버넌스 감사 결과의 참조 기록이다.
감사 범위, 발견된 Gap 요약, 후속 조치 트래킹 문서 링크를 제공한다.

## Purpose

워크스페이스의 Harness/Agent 거버넌스 Gap을 체계적으로 식별하고 우선순위를 정한 감사 이력을 보존한다.
동일한 감사 사이클을 반복하거나 회귀를 점검할 때 기준점으로 활용한다.

## Reference Type

- Type: `version-contract-inventory`
- Source checked: 2026-05-24
- Refresh trigger: 새로운 governance harness cycle 또는 docs/99.templates 대규모 변경 시 재수행

## Authority Boundary

- **Authoritative for**:
  - 2026-05-24 시점의 워크스페이스 거버넌스 Gap 목록 및 우선순위
  - 감사 시점의 template 준수율 수치
- **Not authoritative for**:
  - 현재 운영 정책 — `docs/05.operations/policies/`
  - 현재 실행 계획 — `docs/04.execution/plans/`
  - 현재 구현 계약 — `docs/03.specs/`

## Scope

- **Covered**: docs/01.requirements, 02.architecture, 03.specs, 04.execution, 05.operations, 99.templates, scripts/, .github/workflows/, shared governance hooks
- **Not covered**: gitops/ 매니페스트, infrastructure/ 스크립트 구현 내용

## Definitions / Facts

감사 시점(2026-05-24) 기준 주요 Gap 수치:

- `docs/05.operations/policies`: 템플릿 준수율 14% — AI Agent Policy Section 전체 누락
- `docs/05.operations/runbooks`: 템플릿 준수율 27% — Agent Operations 9/11 누락
- `docs/04.execution/plans`: 81% — Agent Rollout 섹션 누락
- `docs/04.execution/tasks`: 60% — status 어휘 불일치 (`done`/`complete`)
- 레거시 파일: guides/0005 (Superseded by 0008), runbooks/0006 (Superseded by 0010)
- 감사 문서 경로 오류: 346KB plan이 `docs/04.execution/plans/`에 잘못 배치됨

## Sources

- 원본 감사 계획 (삭제됨): `docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md`
- 원본 감사 태스크 (삭제됨): `docs/04.execution/tasks/2026-05-24-workspace-harness-gap-analysis.md`
- 연관 스펙: `[../../03.specs/006-workspace-harness-gap-analysis/spec.md]`
- 후속 P3 실행 계획: `[../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md]`

## Review and Freshness

- Review cadence: 다음 governance harness 감사 사이클 시
- Last reviewed: 2026-05-28 (governance consistency 정비 작업 중 이동)
- Next review trigger: `docs/99.templates/` 대규모 구조 변경 또는 신규 docs stage 추가

## Related Documents

- **Gap Analysis Spec**: `[../../03.specs/006-workspace-harness-gap-analysis/spec.md]`
- **Remediation Plan (P3)**: `[../../04.execution/plans/2026-05-24-p3-gitops-secret-runtime-remediation.md]`
- **Archive Index**: `[../../98.archive/README.md]`
- **Reference maintenance runbook**: `[../../05.operations/runbooks/0011-reference-maintenance-runbook.md]`
