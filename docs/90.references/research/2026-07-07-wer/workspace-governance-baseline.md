---
title: 'Reference: Workspace Governance Baseline Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-07
---

# Reference: Workspace Governance Baseline Research

## Overview

이 문서는 `hy-home.k8s` 워크스페이스의 거버넌스 baseline을 2026-07-07 기준의 repo-backed evidence를 기반으로 요약하고 분석하여 정리한다. future agent와 maintainer가 워크스페이스의 목적, 역할, 운영 계약, 거버넌스 규칙, 템플릿, 스크립트, 통합 가이드, SDLC, CI/CD, QA, 보안 경계 및 AI 에이전트 체계를 신속하게 확인하도록 돕는 것이 목적이다.

특히, 2026-07-06에 spec-driven 개발을 거쳐 추가된 `observability-reviewer`와 `network-reviewer` 에이전트의 존재를 로스터에 반영하여 최신성을 확보하였다.

이 문서는 설명용 참고 문서로서, 실제 실행 정책, CI 설정, 인프라 권한, 배포 승인 절차를 직접 정의하거나 변경하지 않는다.

## Purpose

- 워크스페이스 엔지니어링 리서치 팩의 거버넌스 baseline 수립.
- 워크스페이스 목적, 거버넌스, 자동화, 검증 및 문서 Stage 라우팅 체계 요약 보존.
- canonical owner 및 후속 작업 경로를 추적하여 실제 정책 파일을 침범하지 않고 조회 가능하도록 구성.

## Reference Type

- Type: durable-concept / source-ledger
- Source checked: 2026-07-07
- Refresh trigger: 거버넌스 규칙, CI/CD 설정, 템플릿 구성, 프로바이더 어댑터, 혹은 에이전트 로스터의 변경.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 워크스페이스 거버넌스 baseline 요약 및 사실 기술.
  - 거버넌스 개념과 리포지토리 내 실제 canonical owner 간의 매핑.
- **Not authoritative for**:
  - 활성 거버넌스 정책 규정 (Stage 00이 소유).
  - 실 클러스터(k3d/ArgoCD/Vault/ESO)의 배포 및 비밀정보 조작 권한.

## Scope

- 워크스페이스 목적, 운영 모델, 역할, 프로바이더 어댑터, CI/CD 및 QA 검증 레인, 포맷팅, 린팅, 구문 검증, 자동화, 파이프라인, 템플릿, 스크립트, 운영 계약, SDLC 내 위치, 거버넌스 체계 및 규칙, 보안 경계.
- 실 클러스터 검증 및 런타임 갱신 조작은 포함하지 않음.

## Definitions / Facts

### 워크스페이스 목적 및 운영 모델 (Workspace Purpose & Operating Model)
`hy-home.k8s`는 WSL2 + k3d + ArgoCD GitOps 기반 로컬 Kubernetes 홈랩 플랫폼이자, 사람과 AI가 동일한 Spec-Driven Development(SDD) 단계별 문서를 공유하는 협업 프레임워크다.
- **목적**: 설계부터 운영까지의 맥락을 추적 가능하도록 선언형 GitOps와 SDD 문서 체계를 동기화한다.
- **운영 계약**: 모든 변경은 Git 리포지토리 변경 -> 코드 리뷰 -> ArgoCD 자동 동기화(Reconciliation) 구조를 기본으로 하며, 에이전트 단독으로 실 클러스터 리소스를 직접 변경(`kubectl apply` 등)하는 것은 금지된다.

### 역할 및 프로바이더 어댑터 (Roles & Provider Adapters)
거버넌스 규칙과 체크리스트는 `docs/00.agent-governance/rules/` 하위에 위치한다.
- **프로바이더 어댑터 모델**: 공통 거버넌스 계약을 바탕으로 각 AI 어댑터가 프로바이더 고유의 설정을 소유한다. Claude는 `.claude/`, GPT/Codex는 `.codex/`, Gemini는 `.agents/` 디렉터리에 어댑터 설정을 지닌다.
- **로스터에 반영된 AI Agents**: `supervisor`, `k8s-implementer`, `gitops-reviewer`, `code-reviewer`, `security-auditor`, `incident-responder`, `doc-writer`, `wiki-curator` 외에 최신 추가된 `observability-reviewer`, `network-reviewer`를 포함하여 총 10개의 전용 에이전트가 정의되어 거버넌스를 준수하도록 어댑터 매핑이 유지된다.

### CI/CD 및 QA 검증 레인 (CI/CD & QA Evidence Lanes)
QA 및 검증은 다음과 같이 분리되어 운영된다.
- **Repo-static lane (정적 검증)**: 커밋된 매니페스트, 템플릿 준수 여부, 정적 계약 일치 여부를 검증한다. `validate-repo-quality-gates.sh` 스크립트가 이를 총괄한다.
- **CI/toolchain lane (CI 빌드)**: GitHub Actions에 정의된 워크플로우(`ci.yml`)를 통해 `branch-policy`, `pre-commit`, `repo-quality-static`, `manifest-static` 등의 잡을 순차 수행한다.
- **Live runtime lane (실행 검증)**: 별도 승인된 운영 절차나 검증 스크립트(`run-all.sh`)를 운영자가 실행하는 환경으로, 정적/CI 검증 단계에서 임의로 실행 여부를 판단하지 않는다.

### 포맷팅, 린팅, 구문 검증 (Formatting, Linting & Syntax Validation)
- **포맷팅**: `.editorconfig`가 전역 코딩 스타일을 규정하며, Prettier는 기본 셋에 포함되지 않고 Markdownlint 및 Git diff check로 포인트를 짚어낸다.
- **린팅**: `markdownlint-cli2`가 마크다운 문서 품질을 제어하고, `shellcheck`와 `shfmt`가 쉘 스크립트를 검사하며, `actionlint` 및 `zizmor`가 GitHub Actions 보안/구조를 검증한다.
- **구문 검증**: 쉘 스크립트의 경우 `bash -n`을 통해 기본 문법 오류를 local 및 CI 단계에서 원천 차단한다.

### 자동화, 파이프라인, 워크플로우 (Automation, Pipeline & Workflow)
- **자동화**: Dependabot을 통한 의존성 자동 업데이트, PR 생성 시 라벨링 자동화(`labeler.yml`), 인사말 댓글 작성(`greetings.yml`) 등 관리성 자동화가 적용되어 있다.
- **파이프라인 및 워크플로우**: Actions CI 파이프라인은 최소 권한(`permissions: contents: read`)을 준수하며, lifecycle hook 스크립트(`docs/00.agent-governance/hooks/*.sh`)가 에이전트 동작 시 자동 포맷팅 및 거버넌스 규칙 준수 검증을 보조적으로 가동한다.

### 템플릿 및 통합 가이드 (Templates & Integration Guides)
- **템플릿**: `docs/99.templates/` 산하에 PRD, ARD, ADR, Spec, Plan, Task, Runbook, Reference 등의 표준 마크다운 템플릿이 정의되어 있다. 문서의 생성 위치와 템플릿 간의 맵은 [Template Routing Contract](../../../99.templates/support/template-routing.md)에 종속된다.
- **통합 가이드**: `docs/05.operations/guides/0010-ci-cd-qa-reference-guide.md` 등은 로컬 검증 및 CI 활용법을 상세히 안내하는 역할을 담당한다.

### 스크립트 및 검증 (Scripts & Validation)
`scripts/README.md`에 정의된 정적/동적 검증 스크립트가 플랫폼의 기본 가드레일을 이룬다.
- `validate-repo-quality-gates.sh`: 문서의 단계별 연결성과 마크다운 헤더 준수, 깨진 링크 등을 종합 검증한다.
- `validate-gitops-structure.sh`, `validate-k8s-manifests.sh`: GitOps Kustomize 구조 및 쿠버네티스 리소스 유효성을 평가한다.
- `check-secret-handling.sh`, `validate-policy-gates.sh`: plaintext secrets 유출 및 정책(Namespace 임의 생성 불가 등) 준수 여부를 Conftest나 python fallback으로 감사한다.

### 운영 계약 및 승인 경계 (Operating Contract & Approval Boundaries)
에이전트와 운영자 간의 행위 한계를 정의한다.
- **Default**: 리포지토리 desired state의 PR 작성 및 정적 검증 증적 제출만 수행.
- **Exceptions (승인 필요)**: 실 클러스터 상태 수정, 비밀 정보 갱신, Actions 권한 확대, tag 릴리즈 푸시 등.
- 외부 API 검색/조회는 무해하나, API를 통한 데이터 전송이나 외부 유료 작업 구동은 운영자 명시 승인이 동반되어야 한다.

### SDLC 내 위치 (SDLC Position)
이 연구 자료는 Stage 90 reference에 소속되어 향후 요구사항(Stage 01), 설계(Stage 02/03), 실행(Stage 04), 운영(Stage 05)을 수행하는 AI 에이전트와 사람이 근거 자료로 활용하는 정적 Lookup 공간이다. 이 참조 문서 자체로 배포 파이프라인에 변경을 줄 수 없다.

### 보안 경계 (Security Boundary)
plaintext secrets의 리포지토리 커밋 금지, 최소 권한의 GITHUB_TOKEN 할당, gitleaks/detect-secrets를 활용한 secret leaks 방어, 외부 리소스 조작에 대한 휴먼 승인 등이 유기적으로 설계되어 동작한다.

## Sources

- [AGENTS.md](../../../../AGENTS.md)
- [Root README](../../../../README.md)
- [.codex/CODEX.md](../../../../.codex/CODEX.md)
- [Bootstrap Governance](../../../00.agent-governance/rules/bootstrap.md)
- [Documentation Protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../../00.agent-governance/rules/document-stage-routing.md)
- [Agent Quality Standards](../../../00.agent-governance/rules/quality-standards.md)
- [Harness Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Common Governance & Mappings](../../../00.agent-governance/common-governance.md)
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../../scripts/README.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [Template Routing Contract](../../../99.templates/support/template-routing.md)

## Review and Freshness

- Review cadence: 거버넌스 변경 혹은 에이전트 로스터 수정 시
- Last reviewed: 2026-07-07
- Next review trigger: 거버넌스 규칙 변경, 어댑터 명세 수정, CI/CD 워크플로우 전면 개편

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Harness Catalog**: [../../../00.agent-governance/harness-catalog.md](../../../00.agent-governance/harness-catalog.md)
- **Spec**: [../../../03.specs/017-workspace-engineering-research-pack/spec.md](../../../03.specs/017-workspace-engineering-research-pack/spec.md)
- **Plan**: [../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/plans/2026-07-07-workspace-engineering-research-pack-refresh.md)
- **Task**: [../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md](../../../04.execution/tasks/2026-07-07-workspace-engineering-research-pack-refresh.md)
