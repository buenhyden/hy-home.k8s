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

| 검증 단계                    | 구동 명령                            | 검증 목적                                                                 | 실행 범위     |
| ---------------------------- | ------------------------------------ | ------------------------------------------------------------------------- | ------------- |
| **차분 위생 검사**           | `git diff --check`                   | 공백 오류 및 병합 충돌 표시 잔재 감지                                     | Local 정적만  |
| **위키 인덱스 Freshness**    | `generate-llm-wiki-index.sh --check` | generated wiki index 문서와 실제 spec 간의 링크 최신성 보장               | Local/CI 정적 |
| **리포지토리 품질 게이트**   | `validate-repo-quality-gates.sh .`   | 문서 taxonomies, 템플릿 적합성, mirror-parity, 쉘 문법 검사               | Local/CI 정적 |
| **GitOps 구조 검사**         | `validate-gitops-structure.sh`       | Kustomization 의존성, ArgoCD App-of-Apps 구조 분석                        | Local/CI 정적 |
| **Kubernetes 스펙 검사**     | `validate-k8s-manifests.sh .`        | YAML 문법 및 kube-linter 정적 경고 검출                                   | Local/CI 정적 |
| **plaintext 비밀 유출 검사** | `check-secret-handling.sh .`         | manifest 내에 인코딩되지 않은 secrets 패턴 스캔 및 적색 경보              | Local/CI 정적 |
| **정책 위반 검사 (Rego)**    | `validate-policy-gates.sh .`         | namespace 강제 생성, wildcard AppProject, latest image tags 감지          | Local/CI 정적 |
| **인프라 정적 계약 검증**    | `verify-contracts-static.sh`         | Vault/Postgres/Valkey 포트, TLS Ingress 네이밍 등의 정적 선언 정합성 대조 | Local/CI 정적 |
| **린터 매트릭스 총합**       | `pre-commit run --all-files`         | 커밋 전 hygiene, lint, zizmor, hadolint, actionlint 통합 구동             | Local/CI 정적 |

### 6. SDLC 문서 유형별 역할 및 목적 (SDLC Document Taxonomy)

SDD 라이프사이클의 각 스테이지는 고유한 문서 유형을 산출한다. 각 유형은 `docs/99.templates/templates/sdlc/**`에 정본 템플릿을 가지며, 아래 표는 리포지토리 실제 템플릿을 근거로 각 문서의 역할과 목적을 정리한다. 문서 유형과 스테이지는 [Template Routing Contract](../../../99.templates/support/template-routing.md)가 1:1로 강제한다.

| 문서 유형                                 | 스테이지        | 정본 템플릿                              | 역할 및 목적                                                                                                               |
| ----------------------------------------- | --------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **PRD** (Product Requirements)            | 01.requirements | `sdlc/requirements/prd.template.md`      | 사용자 가치, 문제 정의, 성공 기준을 명확히 하여 후속 설계·구현의 기준을 세운다. "무엇을·왜"에 답한다.                      |
| **ARD** (Architecture Reference Document) | 02.architecture | `sdlc/architecture/ard.template.md`      | 시스템 경계, 책임, 데이터 흐름, 품질 속성, 운영 관점을 정의하는 지속적 참조 아키텍처 기준서.                               |
| **ADR** (Architecture Decision Record)    | 02.architecture | `sdlc/architecture/adr.template.md`      | 특정 아키텍처 결정의 배경·대안·결과를 불변 기록으로 추적한다. 단일 결정 단위이며 사후에 supersede만 될 뿐 수정되지 않는다. |
| **Spec** (Technical Specification)        | 03.specs        | `sdlc/specs/spec.template.md`            | 요구사항·아키텍처로부터 도출된 기술 설계와 구현 계약(contract)을 확정한다. 에이전트 쓰기 행위의 trace 기준점.              |
| **Plan** (Implementation Plan)            | 04.execution    | `sdlc/execution/plan.template.md`        | Spec을 실행 가능한 단계·의존성·위험 요인으로 분해한 구현 계획.                                                             |
| **Task** (Task Record)                    | 04.execution    | `sdlc/execution/task.template.md`        | 구현·검증 작업의 실제 수행 및 증적(validation evidence)을 추적하는 실행 레코드.                                            |
| **Guide**                                 | 05.operations   | `sdlc/operations/guide.template.md`      | 특정 독자가 작업을 이해·재현하도록 단계별 절차와 주의사항을 제공하는 설명형 문서.                                          |
| **Runbook**                               | 05.operations   | `sdlc/operations/runbook.template.md`    | 운영자가 즉시 따라 할 수 있는 실행 절차와 검증 기준을 정의한다. Guide보다 실행 지향적이고 결정론적.                        |
| **Incident**                              | 05.operations   | `sdlc/operations/incident.template.md`   | 사고의 영향·현재 상태·대응 로그를 사실 중심으로 기록한다. 실시간 대응 시점에 작성.                                         |
| **Postmortem**                            | 05.operations   | `sdlc/operations/postmortem.template.md` | 사고의 구조적 근본 원인과 재발 방지 조치를 비난 없이(blameless) 분석한다. Incident 종료 후 작성.                           |
| **Policy**                                | 05.operations   | `sdlc/operations/policy.template.md`     | 운영 정책의 적용 범위, 통제 기준, 예외, 검증 방법을 규정하는 규범 문서.                                                    |

- **Incident 대 Postmortem**: Incident는 "지금 무슨 일이 벌어지고 있는가"의 사실·타임라인 기록이고, Postmortem은 사후에 "왜 발생했고 어떻게 재발을 막는가"의 분석이다. 두 문서는 서로 다른 시점·목적을 가지므로 별도 유형으로 분리된다.
- **Guide 대 Runbook**: Guide는 이해·학습을 돕는 설명형이고, Runbook은 운영자가 결정론적으로 실행하는 절차형이다.
- **Release**: 태스크 체크리스트에는 포함되나, 2026-07-07 기준 리포지토리에는 전용 Stage 문서 템플릿이 없다. 릴리스 기록은 Conventional Commits 기반 커밋 메시지와 CHANGELOG/릴리스 노트 관행([git-workflow](../../../00.agent-governance/rules/agentic.md) 계열)으로 처리되며, 별도 SDLC 문서 유형으로 승격되지 않은 상태다. 향후 릴리스 게이트가 필요하면 Stage 05 operations 하위에 신규 템플릿으로 정의하는 것이 정합적이다.

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
