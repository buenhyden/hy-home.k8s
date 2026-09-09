---
title: "CI/CD 및 QA 검증 경계 가이드"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "platform"
updated: "2026-09-09"
layer: "operations"
artifact_id: "GDE-0010"
---

# CI/CD 및 QA 검증 경계 가이드

## Overview

이 가이드는 변경 작성자가 로컬 정적 검증, GitHub Actions 호스팅 검증,
승인된 런타임 검증을 서로 다른 증적 등급으로 해석하도록 돕는다. 실행 순서나
복구 절차를 복제하지 않고, 현재 검증 진입점과 증적의 한계를 안내한다.

## Guide Type

Concept guide. 검증 명령의 구현은 `scripts/README.md`, CI job 구성은
`.github/workflows/ci.yml`, 실행·복구 절차는 연결된 Runbook이 소유한다.

## Target Audience

- 문서·GitOps·자동화 변경을 작성하거나 검토하는 개발자
- 정적 검증 결과를 운영 증적으로 해석하는 플랫폼 운영자
- 허용된 범위 안에서 검증을 수행하고 handoff를 작성하는 AI Agent

## Prerequisites

- 저장소 checkout과 변경 범위에 대한 읽기 권한
- [Quality Policy](../../../.agents/governance/quality.md)의 증적 경계 이해
- 변경한 표면의 소유 Spec, Policy, Runbook 확인
- live cluster나 외부 서비스 검증이 필요하면 별도의 명시적 승인

## Step-by-step Instructions

### 1. 변경 표면을 먼저 분류한다

`python3 scripts/validate-affected-surfaces.py --root .`는 registry 계약과
추적된 경로의 라우팅을 검사한다. 실제 변경 경로 선택과 실행은 아래 QA
진입점이 소유한다. 라우팅 결과는 실행 권한이나 live 검증 권한을 부여하지 않는다.

### 2. 가장 작은 로컬 검증에서 시작한다

| 변경 상태 | 권장 진입점 | 증적 의미 |
| --- | --- | --- |
| 작업 트리 변경 | `python3 scripts/qa.py quick` 및 focused test | 해당 변경의 빠른 정적 확인 |
| staged 변경 | `python3 scripts/qa.py staged` | 정확한 Git index snapshot의 확인 |
| 전체 저장소 | `python3 scripts/qa.py full` | 현재 checkout의 정적 계약 확인 |

명령과 옵션의 현재 정의는 [`scripts/README.md`](../../../scripts/README.md)를
따른다. 문서에 고정된 validator 개수나 fixture 개수를 성공 기준으로 삼지
않는다.

### 3. 호스팅 CI의 소유 경계를 확인한다

`.github/workflows/ci.yml`이 job 이름, 의존 관계, 실행 조건의 canonical
source이며, job과 required check의 현재 구성은
[GitHub Configuration Hub](../../../.github/repository-surface.md)가 설명한다.
이 문서는 job 목록을 복제하지 않는다. 로컬 성공은 호스팅 환경의
권한·event·required-check 상태까지 증명하지 않는다.

### 4. 증적 등급을 구분해 handoff한다

- 로컬 정적 검증: checkout에 있는 파일과 도구의 계약을 확인한다.
- 호스팅 CI: GitHub event와 workflow 환경에서 동일 변경을 확인한다.
- 런타임 검증: 승인된 운영자가 실제 cluster/service 상태를 확인한다.

handoff 기록 항목은
[Quality Policy](../../../.agents/governance/quality.md)의 handoff evidence
contract가 소유한다. 이 문서는 그 항목을 줄여 옮기지 않는다.
브랜치 SHA나 고정된 문서 수를 별도의 운영 진실로 복제하지 않는다.

### 5. 규칙별 실행 소유자와 메시지 검증을 구분한다

| 규칙 | 실행 소유자 | 유지되는 경계 |
| --- | --- | --- |
| 파일 형식·lint | native 도구 설정과 full/ci의 pre-commit gate | 두 Provider shell adapter에 같은 기준을 적용하고, formatter의 snapshot 변경은 실패로 기록한다 |
| GitHub Actions 보안 | zizmor와 repository Actions validator | 서로 다른 규칙을 유지한다. validator는 `unpinned-uses` 억제를 금지한다 |
| secret 검사 | snapshot Gitleaks, native staged Gitleaks, detect-secrets와 domain/history validator | 입력과 위협 모델이 다르므로 이름만으로 합치지 않는다 |
| 커밋 메시지 | `.cz.toml`과 Commitizen commit-msg stage | full 파일 검사는 메시지 검증을 대신하지 않는다 |

Dockerfile 도입 시 lint owner와 설정을 함께 도입한다. 대상이 없는 설정은
남기지 않는다.

특정 workstation의 hooksPath는 공통 규범이 아니다. 유효한 출처와 hook
연결만 좁게 확인하고 기존 설정을 유지한다. 실제 메시지의 명시적 검증과
정상 active hook 실행은 [Git policy](../../../.agents/governance/git.md)를 따른다.
수동 PASS를 native 설치·실행 증거로 기록하지 않는다.

## Common Pitfalls

- 로컬 PASS를 required check 또는 배포 성공으로 표현하지 않는다.
- 문서에 CI job 수나 fixture 수를 고정해 currentness를 대체하지 않는다.
- 실패한 aggregate gate를 더 작은 PASS 몇 개로 상쇄하지 않는다.
- live cluster, Vault, 외부 API 검증은 정적 QA의 기본 범위로 확장하지 않는다.
- 퇴역 문서의 경로를 redirect 문서로 유지하지 않고 현재 owner로 소비자를
  직접 연결한다.

## Traceability

- [Quality Policy](../../../.agents/governance/quality.md)
- [Agent Execution Policy](../../../.agents/governance/agent-execution.md)
- [Scripts Router](../../../scripts/README.md)
- [Reference Maintenance Runbook](../runbooks/0011-reference-maintenance-runbook.md)
- [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md)

### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| [SPEC-0054-TSK-0006](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0006-stage-05-ownership-cutover.md) | 검증 결과의 범위와 한계를 구분해 handoff한다. | local validators, GitHub Actions, approved runtime evidence |
