# 04.execution/tasks

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 Plan과 Spec에서 파생된 구현, 검증, 평가 작업 단위의 canonical stage다.
단순 TODO가 아니라 작업 ID, 상태, 검증 기준, 증거를 함께 보존하는 실행 추적 위치다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Operators
- QA/Verification Reviewers
- AI Agents

## Scope

### In Scope

- 구현, 테스트, 평가, 문서, 운영 작업 단위
- Parent Spec/Plan 링크
- 검증 기준, 실행 명령, 증거, 상태

### Out of Scope

- 전체 시스템 설계 설명
- 운영 정책 정의
- 장애 대응 절차
- 근본 원인 분석

## Structure

```text
04.execution/tasks/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion.md
├── 2026-05-09-github-qa-ci-remediation.md
├── 2026-05-09-k3d-agent-first-remediation.md
├── 2026-05-09-scripts-inventory-remediation.md
└── README.md
```

## How to Work in This Area

1. 작업의 Parent Spec 또는 Parent Plan을 먼저 확인한다.
2. 새 Task 문서는 `../99.templates/task.template.md`에서 시작한다.
3. 각 작업은 검증 방법과 증거 위치를 함께 기록한다.
4. 설계 보조용 `tasks.md`와 실행 추적 정본을 혼동하지 않는다.

## Related References

- [Docs README](../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/plans](../plans/README.md)
- [05.operations/incidents](../../05.operations/incidents/README.md)

## 목적

이 폴더는 구현·검증·평가 작업(Task) 단위를 저장한다. 이 폴더의 문서는 단순 TODO가 아니라, Spec과 Plan에서 파생된 실행 가능한 작업 목록의 정본(canonical location)이어야 한다.

## 문서 책임

- 구현 작업 추적
- 검증 및 테스트 작업 추적
- 평가(Eval) 작업 추적
- 작업 증거와 완료 상태 기록

## 포함할 내용

1. Parent Spec 또는 Parent Plan 링크
2. 작업 식별자와 설명
3. 작업 유형
4. 검증 기준과 증거
5. 소유자와 상태
6. 필요 시 테스트 명령, Eval 명령, 로그 위치

## 포함하지 말아야 할 내용

- 전체 시스템 설계 설명
- 운영 정책 정의
- 장애 대응 절차
- 근본 원인 분석

위 내용은 각각 `03.specs/`, `05.operations/policies/`, `05.operations/runbooks/`, `05.operations/incidents/postmortems/`로 분리한다.

## 핵심 원칙

1. Task는 상위 Spec 또는 Plan을 참조한다.
2. 핵심 동작은 테스트 우선(TDD)을 기본값으로 한다.
3. Agent 기능은 일반 테스트 외에 Eval을 함께 가진다.
4. 각 Task는 증거(Evidence)와 검증 방법을 포함한다.

## 권장 Task 필드

- Task ID
- Description
- Type (`impl | test | eval | doc | ops`)
- Parent Spec ID / Section
- Parent Plan ID / Phase
- Validation / Evidence
- Owner
- Status

## Agent 전용 Task 타입 예시

- prompt
- tool
- memory
- guardrail
- eval
- observability

## `03.specs`와의 관계

기능 수준에서 밀접한 `tasks.md`는 `03.specs/<feature-id>/`에 둘 수 있다. 그러나 그것은 설계 보조 문서다. 팀 실행용, 스프린트용, 검증 집계용 작업 문서는 `04.execution/tasks/`를 기본 위치이자 정본 위치로 사용한다.

## Templates

- `../99.templates/task.template.md`

## 문서 인덱스

| 문서                                                                                       | 설명                                                                                 | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----- | ---------- |
| [`2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)         | TDD/검증 중심 실행 Task 목록과 증적 기준                                             | Draft | 2026-03-27 |
| [`2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | RED/GREEN/REFACTOR 기반 TLS/Ingress + CI static contract/workflow-security 작업 Task | Draft | 2026-03-28 |
| [`2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 Task, 현재 실행계약은 Headlamp/172.18.x 기준 | Done  | 2026-05-09 |
| [`2026-05-09-k3d-agent-first-remediation.md`](./2026-05-09-k3d-agent-first-remediation.md) | k3d 운영 문서와 Agent-first 실행 계약의 GitOps-first 충돌 보정 Task | Done  | 2026-05-09 |
| [`2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md) | `scripts/` 인벤토리 조사와 README 실행 계약 보정 Task | Done  | 2026-05-09 |
| [`2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md) | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 Task | Done  | 2026-05-09 |

## 관련 폴더

- `03.specs/`: Task의 상위 기술 명세
- `04.execution/plans/`: Task의 상위 실행 계획
- `05.operations/incidents/`: 사고 대응 및 회고 후속 작업 근거

## 예시

- 구현 작업은 `impl` 타입으로 기록한다.
- 검증 작업은 실행 명령과 증거를 포함해 `test` 타입으로 기록한다.
