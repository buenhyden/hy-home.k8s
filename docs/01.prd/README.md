# 01. PRD (Product Requirements)

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 `hy-home.k8s` 플랫폼의 제품 요구사항(PRD)을 보관하는 canonical stage다.
새 기능이나 플랫폼 변화가 어떤 사용자/운영자 가치와 성공 기준을 가져야 하는지 먼저 정의한다.

## Audience

이 README의 주요 독자:

- Product Owners
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 문제 정의, 사용자/운영자 가치, 성공 지표
- 기능 요구, 수용 기준, 범위/비범위
- 관련 ARD, Spec, Plan으로 이어지는 요구사항 추적 링크

### Out of Scope

- 상세 구현 방법과 파일 수준 설계
- 구체 기술 스택 결정
- 장애 대응 절차와 운영 명령

## Structure

```text
01.prd/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion-dashboard-mesh.md
└── README.md
```

## How to Work in This Area

1. 새 요구사항을 작성하기 전에 같은 문제를 다루는 기존 PRD를 먼저 확인한다.
2. 새 PRD는 `../99.templates/prd.template.md`에서 시작한다.
3. 요구사항 변경 시 관련 `02.ard/`, `04.specs/`, `05.plans/` 링크를 함께 갱신한다.
4. Agent 기능 요구에는 허용/금지 행동과 human-in-the-loop 기준을 포함한다.

## Related References

- [Docs README](../README.md)
- [02.ard](../02.ard/README.md)
- [04.specs](../04.specs/README.md)
- [05.plans](../05.plans/README.md)

## 목적

제품의 목표, 사용자 가치, 그리고 성공 기준을 정의한 문서다.
모든 개발의 시작점이며, '무엇을(What)', '왜(Why)' 개발하는지 설명한다.

## 포함할 내용

- 문제 정의
- 사용자/운영자 가치
- 기능 요구
- 성공 지표
- 수용 기준(Acceptance Criteria)
- 범위(In Scope)와 비범위(Out of Scope)

## 포함하지 말아야 할 내용

- 상세 구현 방법
- 구체 기술 스택 선택
- 개별 파일 수준 설계
- 장애 대응 절차

위 내용은 각각 `02.ard/`, `03.adr/`, `04.specs/`, `09.runbooks/`로 분리한다.

## 연결 규칙

- PRD는 관련 ARD, Spec, Plan 링크를 가진다.
- Spec은 PRD 요구 ID를 추적한다.
- Agent 기능인 경우 사용 시나리오, 허용/금지 행동, human-in-the-loop 요구를 포함한다.

## Templates

- `../99.templates/prd.template.md`

## 문서 인덱스

| 문서                                                                                                   | 설명                                                                               | 상태   | 최종 수정  |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ------ | ---------- |
| [`2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md)                     | WSL2 기반 k3d/k3s + ArgoCD GitOps 플랫폼 PRD                                       | Draft  | 2026-03-27 |
| [`2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md)             | WSL2 멀티노드 HA + TLS + 최소권한 + 변경영역 기반 CI 정적 게이트 요구를 포함한 PRD | Draft  | 2026-05-09 |
| [`2026-03-29-platform-expansion-dashboard-mesh.md`](./2026-03-29-platform-expansion-dashboard-mesh.md) | 2026-03-29 cert-manager/Dashboard/Istio/Kiali 확장 PRD, 현재 실행계약은 Headlamp/172.18.x 기준 | Active | 2026-05-09 |

## 관련 폴더

- `02.ard/`: PRD 요구를 시스템 경계와 품질 속성으로 확장한다.
- `04.specs/`: PRD 요구를 구현 가능한 계약으로 구체화한다.
- `05.plans/`: PRD와 Spec을 실행 순서로 전환한다.

## 예시

- 신규 플랫폼 기능은 `2026-03-29-platform-expansion-dashboard-mesh.md`처럼 사용자 가치, 범위, 성공 기준을 먼저 기록한다.
