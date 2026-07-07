---
title: 'Reference: Automation Pipeline Workflow QA Research'
type: content/reference
status: draft
owner: platform
updated: 2026-07-07
---

# Reference: Automation Pipeline Workflow QA Research

## Overview

이 문서는 워크스페이스 `hy-home.k8s` 내의 자동화(Automation), 파이프라인(Pipeline), 워크플로우(Workflow), 그리고 CI/CD와 연계된 QA 검증 루프(QA evidence loop)를 2026-07-07 기준의 리포지토리 실제 구성 상태와 업스트림 모범 사례를 기반으로 정리한다.

본 참조 자료는 설명용 참고 문서로서, 실제 워크플로우 쉘 명령, Actions 스케줄링, 혹은 의존성 린터 규칙 등을 물리적으로 수정하거나 직접 갱신하지 않는다.

## Purpose

- 워크스페이스 내에 내장된 자동화 작업과 CI 잡 파이프라인 간의 위계와 의미 분석.
- 피드백 루프의 핵심 측정 지표(DORA Metrics, Fowler CI)를 정적 가이드라인으로 정리.
- 검증 툴과 Actions 파이프라인의 보안/운영 매핑lookup 제공.

## Reference Type

- Type: durable-concept / external-standard-snapshot / dated-implementation-audit
- Source checked: 2026-07-07
- Refresh trigger: Actions 워크플로우 YAML 파일 수정, pre-commit 구성 훅 변경, DORA 메트릭스 또는 CI 철학 개정.

## Authority Boundary

- **Authoritative for**:
  - 2026-07-07 기준 리포지토리 내 자동화 및 파이프라인 구조 요약.
  - 외부 파이프라인/QA 개념과 로컬 검증 매트릭스 간의 lookup 연결.
- **Not authoritative for**:
  - Actions workflow permissions 및 secrets 접근 권한 부여.
  - Dependabot 주기 또는 stale 봇 스케줄 직접 제어.

## Scope

- GitHub Actions 워크플로우 구조, 권한 통제, 비밀정보 취급 규칙, 의존성 캐싱 및 아티팩트 보존, 수명주기 피드백 루프, DORA 배포 메트릭스, 로컬 쉘 검증 루프.
- 실 클러스터 상의 동적 릴리즈 배포 및 secret decryption 테스트 제외.

## Definitions / Facts

### 1. 자동화, 워크플로우, 파이프라인 모델 (Automation, Workflow & Pipeline)
- **자동화 (Automation)**: 워크스페이스 내 린팅, changelog 생성, stale issues 정리 등 기계가 정기적 혹은 이벤트 기반으로 실행하는 작업을 의미한다.
- **워크플로우 (Workflow)**: `.github/workflows/` 하위의 개별 YAML 파일로 정의된 Actions 작업 명세.
- **파이프라인 (Pipeline)**: 이벤트 트리거에서 출발하여 Job, Step, local validators, `$GITHUB_STEP_SUMMARY`를 거쳐 Task 기록에 수렴하는 전체 검증 및 증적 제출의 유기적 흐름.
- **QA Gate (검증 게이트)**: 변경의 병합 가능 여부를 가리는 제어 장치. 본 리포지토리의 주 검증 게이트는 `ci.yml` 파일이다.

### 2. GitHub Actions 워크플로우 구성 및 잡 그래프 (Workflow Graph)
리포지토리는 아래의 5대 워크플로우를 가동하여 정형화된 파이프라인을 구축하고 있다.
- **`ci.yml` (QA Gate)**: PR 생성 혹은 main push 시 실행되는 핵심 파이프라인. `branch-policy` -> `changes` (경로별 빌드 분기) -> `pre-commit` -> `repo-quality-static` & `manifest-static` -> `ci-summary` 순으로 전개된다.
- **`generate-changelog.yml` (Release evidence)**: tag 생성 시 구동되어 `CHANGELOG.md` 아티팩트를 업로드하고 요약을 남겨 릴리즈 증적을 보존한다.
- **`labeler.yml`, `greetings.yml`, `stale.yml` (Maintenance)**: PR 자동 라벨링, 신규 참여자 인사말 작성, 오랫동안 묵혀진 issue/PR Stale 경고 및 닫기 등의 저장소 위생 작업을 이행한다.

### 3. Permissions 및 Token 보안 경계
- **Least Privilege `GITHUB_TOKEN`**: `ci.yml`과 `generate-changelog.yml`은 최상단에 `permissions: contents: read`를 전역 선언하여 쓰기 권한이 탈취되는 위험을 최소화한다.
- **Credential Isolation**: checkout 단계에서 `persist-credentials: false`를 지정하여 Actions 실행 도중 임의의 스크립트가 리포지토리 쓰기 자격 증명을 유출하는 시나리오를 무력화한다.
- **Write Permissions Isolation**: 오직 `labeler`, `greetings`, `stale`과 같은 관리성 워크플로우만 해당하는 job 레벨에서 필요한 범위의 write 권한을 허용한다.

### 4. CI 피드백 루프 및 delivery metrics
마틴 파울러의 CI(Continuous Integration) 사상에 기반하여, 에이전트의 코딩 작업은 '커밋 시점의 완결성'을 지향해야 한다.
DORA(DevOps Research and Assessment) 프레임워크에 따른 5대 핵심 인도 지표(Delivery Metrics)의 워크스페이스 컨텍스트는 다음과 같다.
- **Deployment Frequency (배포 빈도)**: GitOps desired state 변경 PR이 병합되어 main branch로 수렴하는 빈도.
- **Lead Time for Changes (변경 지연 시간)**: Plan 작성부터 main 병합 및 ArgoCD 자동 동기화 완료까지 걸리는 소요 시간.
- **Change Failure Rate (변경 실패율)**: 배포 후 롤백 또는 장애 복구 작업이 필요해지는 변경 건수의 비율.
- **Time to Restore Service (서비스 복구 시간)**: 실 장애 발생 시 ArgoCD 롤백 또는 break-glass operations를 수행해 정상화하기까지의 소요 시간.
- **Deployment Rework Rate (재작업 비율)**: static validation 실패 혹은 코드 리뷰 거절로 인해 동일 작업에 재투입되는 비율.

에이전트는 이 5가지 지표를 최소화하도록 작은 변경 단위(Task-by-task commit)를 생성하고, 로컬 검증 피드백 루프를 반복 구동하여 재작업 비율을 0%에 수렴시켜야 한다.

### 5. 로컬 검증 루프의 유기적 흐름 (Local Validation Loop)
에이전트는 리모트 Actions CI의 피드백을 기다리기 전, 로컬 쉘 환경에서 다음 스크립트들을 실행해 검증 루프를 완성한다.
1. `validate-repo-quality-gates.sh .`: 마크다운 및 taxonomy 연결성 검사.
2. `validate-gitops-structure.sh`: Kustomization 파일 의존 구조 및 ArgoCD 애플리케이션 연결 상태 확인.
3. `validate-k8s-manifests.sh .`: YAML 구문 및 kube-linter 통과 여부 검사.
4. `check-secret-handling.sh .` & `validate-policy-gates.sh .`: plaintext secrets 방지 및 Rego 컴플라이언스 만족 확인.
5. `verify-contracts-static.sh`: 외부 Postgres/Valkey 서비스 연결 포트/네임 계약 만족 확인.

## Sources

- Martin Fowler, Continuous Integration (<https://martinfowler.com/articles/continuousIntegration.html>)
- DORA Metrics guide (<https://dora.dev/guides/dora-metrics/>)
- GitHub Actions workflow syntax, permissions, and security guidance
- [CI/CD & QA Reference Guide](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Scripts README](../../../../scripts/README.md)

## Review and Freshness

- Review cadence: Actions workflow YAML 파일 갱신 또는 로컬 검증 스크립트 수정 시
- Last reviewed: 2026-07-07
- Next review trigger: CI 빌드 잡 수정, DORA 지표 측정 체계 도입 시

## Related Documents

- **Parent research README**: [README.md](../README.md)
- **References README**: [../../README.md](../../README.md)
- **Workspace baseline**: [workspace-governance-baseline.md](workspace-governance-baseline.md)
- **Formatting reference**: [spec-sdlc-ci-qa-formatting.md](spec-sdlc-ci-qa-formatting.md)
- **CI/CD QA guide**: [../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md](../../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
