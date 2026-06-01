# 01.requirements

> hy-home.k8s 플랫폼의 제품 요구사항(PRD)을 보관하는 canonical stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 `hy-home.k8s` 플랫폼의 제품 요구사항(PRD)을 보관하는 canonical stage다.
새 기능이나 플랫폼 변화가 어떤 사용자/운영자 가치와 성공/수용 기준을 가져야 하는지 먼저 정의한다.
모든 개발의 시작점이며, '무엇을(What)', '왜(Why)' 개발하는지 설명한다.

## Audience

이 README의 주요 독자:

- Product Owners
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 문제 정의, 사용자/운영자 가치, 성공 지표
- 기능 요구, 수용 기준(Acceptance Criteria), 범위/비범위
- 관련 ARD, Spec, Plan으로 이어지는 요구사항 추적 링크

### Out of Scope

- 상세 구현 방법과 파일 수준 설계
- 구체 기술 스택 결정
- 장애 대응 절차와 운영 명령

포함하지 말아야 할 내용은 각각 `02.architecture/requirements/`, `02.architecture/decisions/`, `03.specs/`, `05.operations/runbooks/`로 분리한다.

## Structure

```text
01.requirements/
├── 2026-03-27-wsl-k3d-argocd-platform.md
├── 2026-03-28-wsl2-k3d-argocd-ha-platform.md
├── 2026-03-29-platform-expansion-dashboard-mesh.md
├── 2026-05-17-argo-rollouts-progressive-delivery.md
├── 2026-05-17-argo-notifications-slack.md
├── 2026-06-01-workspace-agent-governance-platform.md
└── README.md
```

## How to Work in This Area

1. 새 요구사항을 작성하기 전에 같은 문제를 다루는 기존 PRD를 먼저 확인한다.
2. 새 PRD는 `../99.templates/prd.template.md`에서 시작하고, canonical target pattern은 `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md`다.
3. PRD는 문제, persona/use case, 기능 요구, `Success / Acceptance Criteria`, 범위/비범위를 분리한다.
4. 요구사항 변경 시 관련 `02.architecture/requirements/`, `03.specs/`, `04.execution/plans/` 링크를 함께 갱신한다.
5. 구현 파일, manifest, 스크립트, 운영 명령 수준의 상세 설계는 PRD에 직접 확장하지 않고 후속 ARD/Spec/Plan 갭으로 남긴다.
6. Agent 기능 요구에는 허용/금지 행동과 human-in-the-loop 기준을 포함한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/01.requirements/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 동일 stage 문서는 `./`로 시작하는 상대 경로를 사용한다.
- 하위 stage 연결은 `../02.architecture/`, `../03.specs/` 등 인접 stage 경로를 사용한다.
- 새 PRD의 실제 Markdown 링크는 최종 PRD 파일 위치 기준으로 다시 계산하고, 아직 없는 후속 문서는 code literal로 남긴다.

## 연결 규칙

- PRD는 관련 ARD, Spec, Plan, ADR 링크를 가진다.
- Spec은 PRD 요구 ID를 추적한다.
- Agent 기능인 경우 사용 시나리오, 허용/금지 행동, human-in-the-loop 요구를 포함한다.
- 후속 ARD/Spec/Plan이 아직 없으면 없는 링크를 만들지 않고, 문서 인덱스와 PRD의 `Related Documents`에 후속 갭으로 표시한다.
- 오래된 실행계약은 삭제하지 않는다. 대신 historical/superseded/current contract를 분리해 현재 작업 기준을 오해하지 않게 한다.

## 요구사항 읽는 순서

1. 현재 플랫폼 기준은 최신 `current contract` 메모와 `gitops/**`, 검증 스크립트가 소유한다.
2. 날짜가 오래된 PRD는 요구사항 이력과 결정 배경을 설명한다. 현재 구현 기준으로 사용하기 전에 상단 메모와 관련 ADR을 확인한다.
3. `Active` 문서는 현재 작업 기준으로 사용할 수 있지만, 대체된 항목은 PRD 안의 superseded 표시와 관련 ADR을 따른다.
4. `Draft` 문서는 후속 ARD/Spec/Plan이 완성되기 전의 제품 의도다. 구현은 별도 downstream 문서와 승인된 계획이 있어야 시작한다.

## 상태 해석

| 상태 | 의미 | 작업 기준 |
| --- | --- | --- |
| Active | 현재 제품 의도를 설명하는 PRD | 관련 ADR/Spec/Plan과 current contract 메모를 함께 확인한다. |
| Draft | 요구사항 초안 또는 후속 설계 대기 상태 | 구현 시작 전 ARD/Spec/Plan 후속 갭을 해소한다. |
| Historical | 초기 요구사항 또는 이전 실행계약 기록 | 배경 자료로 보존하며 현재 실행계약으로 해석하지 않는다. |
| Superseded | 다른 문서나 ADR이 대체한 요구사항 | 대체 문서가 현재 기준을 소유한다. |

## 문서 인덱스

| 문서 | 역할 | 현재성 | 추적성 / 후속 갭 | 최종 수정 |
| --- | --- | --- | --- | --- |
| [`./2026-03-27-wsl-k3d-argocd-platform.md`](./2026-03-27-wsl-k3d-argocd-platform.md) | 초기 WSL2 k3d/k3s + ArgoCD GitOps 플랫폼 PRD | Historical draft | ARD/Spec/Plan/ADR 연결 완료. 현재 런타임은 WSL-native Docker이며 외부 서비스 실행계약은 `172.18.x` repo-backed 계약이 우선. | 2026-05-22 |
| [`./2026-03-28-wsl2-k3d-argocd-ha-platform.md`](./2026-03-28-wsl2-k3d-argocd-ha-platform.md) | HA 플랫폼, TLS, 최소권한, 정적 게이트 요구 PRD | Historical draft | ARD/Spec/Plan/ADR 연결 완료. 현재 런타임은 WSL-native Docker이고 `172.19.x` 값은 이력이며 현재 실행계약은 `172.18.x` 기준. | 2026-05-22 |
| [`./2026-03-29-platform-expansion-dashboard-mesh.md`](./2026-03-29-platform-expansion-dashboard-mesh.md) | cert-manager, Headlamp, Istio/Kiali 확장 PRD | Active with superseded items | ARD/Spec/Plan/ADR 연결 완료. Dashboard 요구는 ADR-0010에 의해 Headlamp로 대체. | 2026-05-17 |
| [`./2026-05-17-argo-rollouts-progressive-delivery.md`](./2026-05-17-argo-rollouts-progressive-delivery.md) | Argo Rollouts canary/blue-green 점진적 배포 PRD | Active current-contract backfill | ARD/Spec/Plan/Task 연결 완료. 현재 GitOps 계약은 `platform-rollouts` Application과 Rollouts 운영 문서가 소유. | 2026-05-18 |
| [`./2026-05-17-argo-notifications-slack.md`](./2026-05-17-argo-notifications-slack.md) | Argo Notifications Slack 알림 PRD | Active current-contract backfill | ARD/Spec/Plan/Task 연결 완료. 현재 Secret 경계는 Vault/ESO/ArgoCD Notifications 문서가 소유. | 2026-05-18 |
| [`./2026-06-01-workspace-agent-governance-platform.md`](./2026-06-01-workspace-agent-governance-platform.md) | Workspace AI Agent governance, Stage 00 canonical adapter, skill-axis routing PRD | Active current-contract backfill | ARD-0006, ADR-0013, Spec 006, Stage 00 canonical adapter Plan/Task 연결 완료. | 2026-06-01 |

## 예시

신규 플랫폼 기능은 `2026-03-29-platform-expansion-dashboard-mesh.md`처럼 사용자 가치, 범위, 성공/수용 기준을 먼저 기록한다.

## Related Documents

- [Docs README](../README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md)
- [03.specs](../03.specs/README.md)
- [04.execution/plans](../04.execution/plans/README.md)
