---
title: 'Reference: Spec SDLC CI QA Formatting Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-07
---

# Reference: Spec SDLC CI QA Formatting Research

## Overview

이 문서는 스펙 주도 개발(Spec-driven development), SDLC 및 Secure SDLC 표준, CI/CD 아키텍처, QA 검증 분류, 포맷팅 및 린팅 체계를 2026-07-07 기준의 리포지토리 실제 구성 상태와 최신 외부 소스 검증 결과를 조합하여 정리한다.

이 문서는 설명용 참고 문서로서, 실제 워크스페이스의 Actions 워크플로우 실행 로직, 린터 규칙, 템플릿 검증 정책 등을 직접 재정의하거나 간섭하지 않는다.

## Purpose

- 스펙 주도 개발의 근거 자료와 타당성 증명.
- NIST SSDF(Secure Software Development Framework) 및 공급망 보안 요건을 로컬 검증 매트릭스와 동기화.
- 포맷팅/린팅/구문 검증의 정적 규칙과 CI 파이프라인의 구조적 상호관계를 규정.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-07
- Refresh trigger: SDD 산출물 양식 변경, Actions 워크플로우 설정 수정, pre-commit 훅 버전 업그레이드.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 스펙 주도 개발, SDLC, CI/CD, QA, 포맷팅 분석 및 개념 설명.
  - 리포지토리 정적 검증 스크립트와 대응하는 외부 규칙 사양 간의 lookup.
- **Not authoritative for**:
  - Actions 실행 권한 및 빌드 잡 통제.
  - pre-commit 훅 규칙 개별 활성화 제어.

## Scope

- 스펙 주도 개발 단계 정의, SDLC/S-SDLC 표준, CI/CD Actions 잡 그래프, QA 검증 레인 분류, 포맷팅/린팅/구문 검증 도구 분석, 정적 검증 매트릭스.
- 실제 배포 동기화 테스트 및 Secrets 런타임 검증 제외.

## Definitions / Facts

### 1. 스펙 주도 개발 (Spec-driven Development; SDD)
GitHub Spec Kit의 `Spec -> Plan -> Tasks -> Implement` 모델과 거의 동일하게, 본 워크스페이스는 요구사항(Stage 01)과 아키텍처(Stage 02)로부터 도출된 설계 명세(Stage 03 Spec)를 실행 계획(Stage 04 Plan)과 개별 작업 기록(Stage 04 Task)으로 연결한다. 에이전트는 계획되지 않은 코딩 작업을 수행할 수 없으며, 모든 쓰기 행위는 Spec 및 Plan 문서의 trace를 남겨야 한다.

### 2. SDLC 및 Secure SDLC (Secure-SDLC)
NIST SP 800-218(SSDF) 및 SP 800-204D(Cloud-Native DevSecOps 공급망 보안) 표준에 부합하도록, 본 워크스페이스는 보안 검증 단계를 SDLC 프로세스 자체에 유기적으로 통합한다.
- **인프라/코드의 보안**: plaintext secrets의 리포지토리 내 유입을 정적 check 스크립트로 상시 스캔하며, Vault HCL 정책 예제를 참조함으로써 에이전트의 툴 실행 권한이 최소 권한을 유지하도록 통제한다.
- **공급망 보안**: GitHub Actions 내 서드파티 Action의 태그 고정(Pinning), `GITHUB_TOKEN`에 대한 전역 contents: read 최소 권한 적용, 의존성 업데이트 자동 스캔(Dependabot)을 이행한다.

### 3. CI/CD (Continuous Integration / Continuous Deployment)
GitHub Actions는 이 리포지토리의 중앙 집중식 통합 파이프라인이다.
- **`ci.yml` 잡 그래프**:
  - `branch-policy` (PR 브랜치 네이밍 규칙 검사)
  - `changes` (변경 파일 패스 감지 및 타겟 빌드 필터링)
  - `pre-commit` (정적 린터 매트릭스 구동)
  - `repo-quality-static` (`validate-repo-quality-gates.sh`를 활용한 문서/거버넌스 정합성 검사)
  - `manifest-static` (Kubernetes manifests 유효성 및 static infra contract 검사)
  - `ci-summary` (각 단계 실패/성공 여부 최종 요약)
- **보안 파이프라인**: Actions 내 `persist-credentials: false` 설정을 통해 체크아웃 자격 증명이 불필요하게 다음 step으로 흘러가는 것을 막는다.

### 4. QA (포맷팅, 코드 스타일 린팅, 문법 오류)
QA 검증은 피드백 주기와 타겟 신뢰 수준에 따라 3개 레인으로 분류된다.

#### 1) 포맷팅 (Formatting)
- **EditorConfig**: `.editorconfig` 파일에 명시된 스타일(UTF-8, LF line endings, spaces indentation, trailing whitespace trimming 등)을 준수한다.
- **Prettier**: 리포지토리의 기본 포맷터 셋에는 포함되어 있지 않으며, pre-commit 내 hygiene 훅과 `git diff --check`를 사용해 불필요한 공백과 포맷 깨짐을 제어한다.

#### 2) 코드 스타일 린팅 (Linting / Static Analysis)
- **Markdown**: `markdownlint-cli2`가 마크다운 스타일과 구문을 체크한다.
- **Shell Scripts**: `shellcheck`가 쉘 스크립트 스타일 가이드를 검증한다.
- **Actions Workflow**: `actionlint` 및 `zizmor`가 Actions YAML과 보안 안티패턴을 감시한다.
- **Kubernetes manifests**: `kube-linter` 및 `conftest` (Rego 정책)가 보안 컴플라이언스 및 배포 모범 사례 준수를 평가한다.

#### 3) 문법 오류 (Syntax Error / Compilation)
- **Shell**: `bash -n` 명령어를 활용하여 쉘 스크립트의 구문 문법 오류를 검출한다.
- **YAML / JSON**: `check-yaml` 및 `check-json`을 활용하여 선언 파일의 구문 깨짐을 방어한다.

### 5. 로컬 정적 검증 매트릭스 (Repo-local Validation Matrix)

| 검증 단계 | 구동 명령 | 검증 목적 | 실행 범위 |
| --- | --- | --- | --- |
| **차분 위생 검사** | `git diff --check` | 공백 오류 및 병합 충돌 표시 잔재 감지 | Local 정적만 |
| **위키 인덱스 Freshness** | `generate-llm-wiki-index.sh --check` | generated wiki index 문서와 실제 spec 간의 링크 최신성 보장 | Local/CI 정적 |
| **리포지토리 품질 게이트** | `validate-repo-quality-gates.sh .` | 문서 taxonomies, 템플릿 적합성, mirror-parity, 쉘 문법 검사 | Local/CI 정적 |
| **GitOps 구조 검사** | `validate-gitops-structure.sh` | Kustomization 의존성, ArgoCD App-of-Apps 구조 분석 | Local/CI 정적 |
| **Kubernetes 스펙 검사** | `validate-k8s-manifests.sh .` | YAML 문법 및 kube-linter 정적 경고 검출 | Local/CI 정적 |
| **plaintext 비밀 유출 검사** | `check-secret-handling.sh .` | manifest 내에 인코딩되지 않은 secrets 패턴 스캔 및 적색 경보 | Local/CI 정적 |
| **정책 위반 검사 (Rego)** | `validate-policy-gates.sh .` | namespace 강제 생성, wildcard AppProject, latest image tags 감지 | Local/CI 정적 |
| **인프라 정적 계약 검증** | `verify-contracts-static.sh` | Vault/Postgres/Valkey 포트, TLS Ingress 네이밍 등의 정적 선언 정합성 대조 | Local/CI 정적 |
| **린터 매트릭스 총합** | `pre-commit run --all-files` | 커밋 전 hygiene, lint, zizmor, hadolint, actionlint 통합 구동 | Local/CI 정적 |

## Sources

- NIST SSDF SP 800-218 (<https://csrc.nist.gov/pubs/sp/800/218/final>)
- NIST SP 800-204D (<https://csrc.nist.gov/pubs/sp/800/204/d/final>)
- GitHub Actions workflow syntax and security hardening reference
- GitHub Spec Kit Repository (<https://github.com/github/spec-kit>)
- EditorConfig specification (<https://editorconfig.org/>)
- markdownlint and pre-commit documentation
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../../scripts/README.md)

## Review and Freshness

- Review cadence: pre-commit 훅 또는 Actions 워크플로우 정의 변경 시
- Last reviewed: 2026-07-07
- Next review trigger: CI 워크플로우 변경, 린터 설정 변경

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Infrastructure security reference**: [kubernetes-infrastructure-security.md](kubernetes-infrastructure-security.md)
- **CI/CD QA guide**: [../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
