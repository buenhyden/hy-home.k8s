---
title: "CI/CD 및 QA 검증 경계 가이드"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "platform"
updated: "2026-09-07"
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

`python3 scripts/validate-affected-surfaces.py --root .`는 변경된 경로에 맞는
정적 검증 후보를 제시한다. 이 결과는 실행 권한을 부여하지 않으며, 변경하지
않은 표면까지 무조건 검증하라는 고정 fixture도 아니다.

### 2. 가장 작은 로컬 검증에서 시작한다

| 변경 상태 | 권장 진입점 | 증적 의미 |
| --- | --- | --- |
| 작업 트리 변경 | 영향 표면별 validator/test | 해당 변경의 빠른 정적 확인 |
| staged 변경 | `python3 scripts/run-validation-lane.py --root . --lane staged --paths-file <paths.nul> --delimiter nul` | 커밋 후보 범위의 통합 확인 |
| 전체 저장소 | `python3 scripts/qa.py full` | 현재 checkout의 정적 계약 확인 |

명령과 옵션의 현재 정의는 [`scripts/README.md`](../../../scripts/README.md)를
따른다. 문서에 고정된 validator 개수나 fixture 개수를 성공 기준으로 삼지
않는다.

### 3. 호스팅 CI의 소유 경계를 확인한다

`.github/workflows/ci.yml`이 job 이름, 의존 관계, 실행 조건의 canonical
source다. 현재 주요 검증 면은 branch policy, change classification,
pre-commit, repository quality, agent governance, manifest validation,
summary로 나뉜다. 로컬 성공은 호스팅 환경의 권한·event·required-check
상태까지 증명하지 않는다.

### 4. 증적 등급을 구분해 handoff한다

- 로컬 정적 검증: checkout에 있는 파일과 도구의 계약을 확인한다.
- 호스팅 CI: GitHub event와 workflow 환경에서 동일 변경을 확인한다.
- 런타임 검증: 승인된 운영자가 실제 cluster/service 상태를 확인한다.

handoff에는 실행한 진입점, 결과, 실행하지 못한 검증과 그 이유를 기록한다.
브랜치 SHA나 고정된 문서 수를 별도의 운영 진실로 복제하지 않는다.

### 5. 규칙별 실행 소유자와 이 워크스테이션의 한계를 구분한다

한 규칙은 실행 소유자를 하나만 가진다. 중복이 남아 있다면 그 이유가 기록되어
있어야 하며, 기록 없는 중복은 정리 대상이다. 2026-09-07 확인 결과는 다음과 같다.

| 규칙 | 실행 소유자 | 판정 |
| --- | --- | --- |
| 컨테이너 매니페스트 린트(`hadolint`) | `.pre-commit-config.yaml`의 훅 하나 | 중복 없음. 어떤 검증 스크립트도 이 린터를 실행하지 않으며, 현재 저장소에는 추적되는 Dockerfile이 없다. 훅을 제거하면 소유권 이전이 아니라 향후 커버리지 삭제가 되므로 유지한다 |
| GitHub Actions 액션 핀 고정 | 서드파티 린터(`zizmor`)와 저장소 validator 양쪽 | 의도된 인터록이므로 양쪽 유지. `scripts/validate-github-actions-security.py`가 `unpinned-uses` 규칙의 `disable: true` 억제를 금지하므로, validator는 린터 규칙이 꺼지는 것을 막는 역할을 한다 |
| 커밋 훅 스위트 | full 프로파일 안의 실행 | 유지. 아래 한계 때문에 이 워크스테이션에서는 full 프로파일 실행이 유일한 실행 경로다 |

**커밋 도구 한계(2026-09-07 관측).** 이 워크스테이션의 전역
`core.hooksPath`가 저장소 밖(`/home/hy/.codex/git-hooks`)을 가리킨다. 저장소의
`.git/hooks/pre-commit`과 `commit-msg`는 설치되어 있으나 커밋 시점에 실행되지
않으며, conventional-commit 검사도 커밋 시점에 동작하지 않는다. 이것은 한계이지
동작하는 통제가 아니다.

전역 설정은 변경하지 않는다. 사용자가 직접 실행하는 저장소-로컬 복구는 다음과
같다.

```bash
git config --local core.hooksPath .git/hooks
```

이 설정은 이 저장소에만 적용되고 전역 설정을 건드리지 않는다. 되돌리려면
`git config --local --unset core.hooksPath`를 실행한다.

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
