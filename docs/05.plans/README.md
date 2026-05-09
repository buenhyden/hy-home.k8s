# 05.plans

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 승인된 요구와 기술 계약을 실행 순서, 위험 관리, 검증 게이트로 전환하는 Plan stage다.
Plan은 구현을 시작하기 전 작업 흐름, 롤아웃/롤백, 완료 기준을 합의하는 문서다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Operators
- Project Maintainers
- AI Agents

## Scope

### In Scope

- 목표, 범위, 단계, 마일스톤
- 위험과 완화 전략
- 검증 게이트, 완료 기준, 롤아웃/롤백 전략
- 하위 Task로 이어지는 실행 단위 참조

### Out of Scope

- 요구사항 정본
- 상세 기술 설계 정본
- 실제 작업 증거와 상태 추적의 정본

## Structure

```text
05.plans/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion.md
├── 2026-05-09-github-qa-ci-remediation.md
├── 2026-05-09-k3d-agent-first-remediation.md
├── 2026-05-09-scripts-inventory-remediation.md
└── README.md
```

## How to Work in This Area

1. 관련 PRD/ARD/ADR/Spec을 먼저 읽고 계획의 입력을 고정한다.
2. 새 Plan은 `../99.templates/plan.template.md`에서 시작한다.
3. Plan 변경 시 관련 `06.tasks/`의 Parent Plan/Phase 링크를 확인한다.
4. 완료된 계획은 검증 결과와 후속 문서 링크를 남긴다.

## Related References

- [Docs README](../README.md)
- [04.specs](../04.specs/README.md)
- [06.tasks](../06.tasks/README.md)
- [08.operations](../08.operations/README.md)

## 목적

이 폴더는 실행 계획(Plan)을 저장한다. Plan은 언제, 누가, 어떤 순서로, 어떤 제약과 위험을 관리하며 작업을 진행하는지 정의한다.

## 포함할 내용

- 목표와 범위
- 단계(Phase) 또는 추적 표
- 위험과 완화 전략
- 검증 게이트
- 완료 기준
- 롤아웃/롤백 전략

## AI Agent 계획에 추가할 내용

- Offline Eval 통과 기준
- Canary/Sandbox Rollout
- Human Approval Gate
- Prompt/Model 버전 승격 기준
- Rollback 조건

## 연결 규칙

- Plan은 PRD/ARD/Spec/ADR를 참조한다.
- Task는 Plan의 단계 또는 Task ID를 상위 참조로 가진다.

## Templates

- `../99.templates/plan.template.md`

## 문서 인덱스

| 문서                                                                                       | 설명                                                                            | 상태  | 최종 수정  |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ----- | ---------- |
| [`2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)         | WSL2 GitOps 플랫폼 단계별 실행 계획                                             | Draft | 2026-03-27 |
| [`2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | TLS/최소권한 유지 + 변경영역 기반 CI 정적 게이트 + 롤백 규칙을 포함한 실행 계획 | Draft | 2026-03-28 |
| [`2026-03-29-platform-expansion.md`](./2026-03-29-platform-expansion.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 계획, 현재 실행계약은 Headlamp/172.18.x 기준 | Done  | 2026-05-09 |
| [`2026-05-09-k3d-agent-first-remediation.md`](./2026-05-09-k3d-agent-first-remediation.md) | k3d 운영 문서와 Agent-first 실행 계약의 GitOps-first 충돌 보정 계획 | Done  | 2026-05-09 |
| [`2026-05-09-scripts-inventory-remediation.md`](./2026-05-09-scripts-inventory-remediation.md) | `scripts/` 인벤토리 조사와 README 실행 계약 보정 계획 | Done  | 2026-05-09 |
| [`2026-05-09-github-qa-ci-remediation.md`](./2026-05-09-github-qa-ci-remediation.md) | `.github` QA, CI, 브랜치 정책, PR intake 계약 보정 계획 | Done  | 2026-05-09 |

## 관련 폴더

- `04.specs/`: 계획의 입력이 되는 기술 명세
- `06.tasks/`: 계획을 실행 가능한 작업으로 나눈 기록
- `08.operations/`: 롤아웃과 운영 정책 기준

## 예시

- 플랫폼 확장 작업은 `2026-03-29-platform-expansion.md`처럼 단계, 위험, 검증 게이트를 포함한다.
