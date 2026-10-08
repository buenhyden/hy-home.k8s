---
title: "CI/CD 및 QA 검증 경계 가이드"
version: "1.3.0"
type: "operation/guide"
status: "active"
owner: "platform"
updated: "2026-10-08"
layer: "operations"
artifact_id: "GDE-0010"
---

# CI/CD 및 QA 검증 경계 가이드

## Overview

이 가이드는 변경 작성자가 로컬 정적 검증, GitHub Actions branch metadata,
승인된 런타임 검증을 서로 다른 증적 등급으로 해석하도록 돕는다. 실행 순서나
복구 절차를 복제하지 않고, 현재 검증 진입점과 증적의 한계를 안내한다.

## Audience and Goal

주된 학습 목적은 `explanation`이다. 독자는 검증 결과가 어떤 증적 등급을
뜻하는지 구분한다. 검증 명령의 구현은 `scripts/README.md`, CI job 구성은
`.github/workflows/ci.yml`, 실행·복구 절차는 연결된 Runbook이 소유한다.

- 문서·GitOps·자동화 변경을 작성하거나 검토하는 개발자
- 정적 검증 결과를 운영 증적으로 해석하는 플랫폼 운영자
- 허용된 범위 안에서 검증을 수행하고 handoff를 작성하는 AI Agent

## Prerequisites

- 저장소 checkout과 변경 범위에 대한 읽기 권한
- [Quality Policy](../../../.agents/governance/quality.md)의 증적 경계 이해
- 변경한 표면의 소유 Spec, Policy, Runbook 확인
- live cluster나 외부 서비스 검증이 필요하면 별도의 명시적 승인

## Guidance

### 1. 변경 표면을 먼저 분류한다

`python3 scripts/validate-affected-surfaces.py --root .`는 registry 계약과
추적된 경로의 라우팅을 검사한다. 실제 변경 경로 선택과 실행은 아래 QA
진입점이 소유한다. 라우팅 결과는 실행 권한이나 live 검증 권한을 부여하지 않는다.

### 2. 가장 작은 로컬 검증에서 시작한다

| 변경 상태 | 권장 진입점 | 증적 의미 |
| --- | --- | --- |
| 일반 문서 변경 | 공통 diff·style 검사와 선택된 문서 profile·관계·링크·상태 검사 | 문서 내용·형식과 현재 owner만 로컬에서 확인; 동작 회귀 suite를 추가하지 않음 |
| 구현·validator·QA 계약 변경 | 바뀐 규칙의 focused 회귀와, 작업 트리 입력에 별도 증거가 필요할 때 `python3 scripts/qa.py quick` | 새 동작의 실패·경계 사례를 해당 입력에서 확인 |
| staged 변경 | `git diff --cached --check`, 실제 메시지 검사 및 선택된 `python3 scripts/qa.py staged` | 정확한 Git index snapshot과 commit 문법을 서로 다른 입력으로 확인 |
| global QA 계약 변경 또는 명시적 한정 감사 | 변경 목적에 해당하는 named 동작·Archive·보안 회귀와 선택된 affected/staged gate | 사전 도구·예산 확인 후 필요한 보호만 확인; full/ci sweep·blanket unit discovery는 선택하지 않음 |
| hosted CI | GitHub Actions의 branch result·`ci-summary`와 별도 PR `style-pr` | 각각의 PR SHA/run에서 branch metadata와 선택된 style만 확인; 목적·문서 내용 QA를 대리하지 않음 |

명령과 옵션의 현재 정의는 [`scripts/README.md`](../../../scripts/README.md)를
따른다. 문서에 고정된 validator 개수나 fixture 개수를 성공 기준으로 삼지
않는다. 문서 링크·owner 검사는 로컬 QA에만 속하며, 로컬 target 통과가
외부 URL 가용성을 증명하지 않는다.

### 3. 호스팅 CI의 소유 경계를 확인한다

`.github/workflows/ci.yml`이 job 이름, 의존 관계, 실행 조건의 canonical
source이며, job과 required check의 현재 구성은
[GitHub Configuration Hub](../../../.github/repository-surface.md)가 설명한다.
호스팅 workflow는 로컬 QA를 다시 실행하거나 PASS로 대리하지 않는다.
이 문서는 job 목록을 복제하지 않는다. 로컬 성공은 호스팅 환경의
권한·event·required-check 상태까지 증명하지 않는다.

### 4. 증적 등급을 구분해 handoff한다

- 로컬 정적 검증: checkout에 있는 파일과 도구의 계약을 확인한다.
- 호스팅 CI: event와 branch metadata, 선택된 PR style의 적용 가능한 결과를
  각자의 SHA/run에서만 확인한다.
- 런타임 검증: 승인된 운영자가 실제 cluster/service 상태를 확인한다.

handoff 기록 항목은
[Quality Policy](../../../.agents/governance/quality.md)의 handoff evidence
contract가 소유한다. 이 문서는 그 항목을 줄여 옮기지 않는다.
브랜치 SHA나 고정된 문서 수를 별도의 운영 진실로 복제하지 않는다.

### 5. 규칙별 실행 소유자와 메시지 검증을 구분한다

| 규칙 | 실행 소유자 | 유지되는 경계 |
| --- | --- | --- |
| 파일 형식·lint | native 도구 설정과 최종 local index의 선택된 pre-commit style gate; 별도 PR style job은 다른 merge 입력 | 로컬 커밋 직전에 확인하고 동일 local leaf는 한 번만 실행한다. formatter의 snapshot 변경은 실패로 기록한다 |
| GitHub Actions 보안 | zizmor와 repository Actions validator | 서로 다른 규칙을 유지한다. validator는 `unpinned-uses` 억제를 금지한다 |
| secret 검사 | snapshot Gitleaks, native staged Gitleaks, detect-secrets와 domain/history validator | 입력과 위협 모델이 다르므로 이름만으로 합치지 않는다 |
| 커밋 메시지 | `.cz.toml`과 Commitizen commit-msg stage | 선택된 파일 검사는 메시지 검증을 대신하지 않는다 |

도구별 규칙 소유와 suppression 기준은
[Formatting and Linting Policy](../../../.agents/governance/formatting-and-linting.md),
hook 연결과 커밋 메시지 검증 절차는
[Git policy](../../../.agents/governance/git.md)가 소유한다.

## Verification and Troubleshooting

- 로컬 PASS를 required check 또는 배포 성공으로 표현하지 않는다.
- 문서에 CI job 수나 fixture 수를 고정해 currentness를 대체하지 않는다.
- 실패한 aggregate gate를 더 작은 PASS 몇 개로 상쇄하지 않는다.
- 퇴역한 full/ci의 과거 `NOT_RUN`은 해당 입력의 역사로 보존한다. 현재 선택된
  필수 검사가 미실행이면 그 검사에 `NOT_RUN`과 다음 owner를 기록한다.
  `NOT_APPLICABLE`는 검사 대상이 없을 때만 사용한다.
- live cluster, Vault, 외부 API 검증은 정적 QA의 기본 범위로 확장하지 않는다.
- 퇴역 문서의 경로를 redirect 문서로 유지하지 않고 현재 owner로 소비자를
  직접 연결한다.

## Related Documents

- [Quality Policy](../../../.agents/governance/quality.md)
- [Agent Execution Policy](../../../.agents/governance/agent-execution.md)
- [Scripts Router](../../../scripts/README.md)
- [Release Preparation Runbook](../runbooks/0012-main-release-preparation-runbook.md)
- [Reference Maintenance Runbook](../runbooks/0011-reference-maintenance-runbook.md)

### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| N/A — SPEC-0054-TSK-0006 was retained with its package by SPEC-0087 | 검증 결과의 범위와 한계를 구분해 handoff한다. | local validators, GitHub Actions, approved runtime evidence |
