# 05.operations/policies

> GitOps 플랫폼 운영 정책과 통제 기준(허용/금지/예외/검증)을 관리한다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 플랫폼 운영 정책의 단일 기준점이다.
외부 서비스 런타임 분리, Vault 단일 소스, GitOps 경로/브랜치 게이트, 포트 계약 준수 같은 운영 규칙을 문서화한다.

정책 문서는 “무엇이 허용되고 금지되는가”와 “어떤 증적이 필요한가”를 정의한다.
명령 순서, 반복 실행 체크리스트, bootstrap/break-glass 절차, 복구 절차는 [runbooks](../runbooks/README.md), 배경과 온보딩 설명은 [guides](../guides/README.md), 정책 위반이나 장애 기록은 [incidents](../incidents/README.md)로 보낸다.

| 필요 상황 | 문서 유형 |
| --- | --- |
| Required/Allowed/Disallowed 기준이 필요함 | Policy |
| 예외 승인 경로와 검토 주기를 확인해야 함 | Policy |
| 검증에 필요한 증적 종류를 정의해야 함 | Policy |
| 명령을 순서대로 실행하거나 복구해야 함 | Runbook으로 이동 |
| 실행 가능한 명령 블록이나 체크리스트를 작성해야 함 | Runbook으로 이동 |
| 작업 배경과 사용법을 익혀야 함 | Guide로 이동 |

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책 문서(Operations Policy)
- 통제 항목(Required/Allowed/Disallowed)
- 예외 승인 흐름
- 정책 검증 방법 및 검토 주기

### Out of Scope

- 실행 절차 중심의 명령 순서 문서
- 장애 타임라인/사후 분석
- 온보딩 중심 가이드

## Structure

```text
docs/05.operations/policies/
├── 0001-k8s-gitops-operations-policy.md                         # k3d/ArgoCD/ESO/Vault 운영 정책
├── 0002-wsl2-k3d-gitops-ha-operations-policy.md                 # WSL2 HA + TLS/최소권한 + CI 게이트 정책
├── 0003-service-mesh-cert-manager-policy.md                     # cert-manager/Istio/Kiali 운영 통제
├── 0004-rollouts-notifications-headlamp-policy.md               # Rollouts/Notifications/Headlamp 운영 통제
├── 0005-observability-platform-operations-policy.md             # ArgoCD/Grafana/포트 계약 정책
├── 0006-k8s-observability-operations-policy.md                  # 관측성 스택 운영 정책
├── 0007-app-gitops-onboarding-policy.md                         # 앱 GitOps 온보딩 운영 정책
└── README.md                                                    # This file
```

## How to Work in This Area

1. 정책 수정 전에 관련 Spec/Runbook을 확인한다.
2. [operation.template.md](../../99.templates/operation.template.md)를 기준으로 섹션을 유지한다.
3. 통제 변경 시 검증 명령과 예외 승인 흐름을 함께 갱신한다.
4. 문서 변경 후 이 README 인덱스를 동기화한다.
5. 정책 문서에는 실행 절차를 복제하지 않는다. 검증은 필요한 증적과 성공 기준만 남기고, 실행 가능한 명령 순서와 체크리스트는 소유 runbook 링크로 연결한다.
6. live cluster mutation, Vault write, kubeconfig 변경 예시는 human-approved, bootstrap-only, break-glass 문맥 없이는 추가하지 않는다.

## Link Basis

이 README의 링크 기준 위치는 `docs/05.operations/policies/`다.

- 같은 폴더의 Policy 문서는 `./`로 시작한다.
- sibling operations folder는 `../guides/`, `../runbooks/`, `../incidents/`로 연결한다.
- upstream docs stage는 `../../02.architecture/`, `../../03.specs/`, `../../04.execution/`로 연결한다.

## Related Documents

- [05.operations/guides](../guides/README.md)
- [05.operations/runbooks](../runbooks/README.md)
- [05.operations/incidents](../incidents/README.md)
- [03.specs](../../03.specs/README.md)
- [ARD](../../02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md)
- [Spec](../../03.specs/002-wsl2-k3d-argocd-ha-platform/spec.md)
- [Runbook](../runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- [Operation Template](../../99.templates/operation.template.md)
- [README Template](../../99.templates/readme.template.md)

## 문서 인덱스

| 문서                                                                                                     | 설명                                                                                    | 상태   | 최종 수정  |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------ | ---------- |
| [`./0001-k8s-gitops-operations-policy.md`](./0001-k8s-gitops-operations-policy.md)                         | 외부 런타임 분리 + Vault 단일 소스 + GitOps 게이트 운영 정책                            | Active | 2026-05-21 |
| [`./0002-wsl2-k3d-gitops-ha-operations-policy.md`](./0002-wsl2-k3d-gitops-ha-operations-policy.md)         | WSL2 HA 운영 통제(TLS/Traefik 경계, EndpointSlice, 최소권한, CI 게이트, 감사 항목) 정책 | Active | 2026-05-25 |
| [`./0003-service-mesh-cert-manager-policy.md`](./0003-service-mesh-cert-manager-policy.md)                 | cert-manager/Headlamp/Istio/Kiali 운영 통제(TLS/sidecar/Kiali auth/Traefik 계약) 정책   | Active | 2026-05-21 |
| [`./0004-rollouts-notifications-headlamp-policy.md`](./0004-rollouts-notifications-headlamp-policy.md)     | Argo Rollouts/Notifications(Slack)/Headlamp 운영 통제 정책                              | Active | 2026-05-21 |
| [`./0005-observability-platform-operations-policy.md`](./0005-observability-platform-operations-policy.md) | Istio 포트 네이밍/Grafana Anonymous Access/ArgoCD NodePort 예약 정책                    | Active | 2026-05-22 |
| [`./0006-k8s-observability-operations-policy.md`](./0006-k8s-observability-operations-policy.md)           | k8s 메트릭 NodePort 예약/in-cluster Alloy/alert_rules 로드 패턴 정책                    | Active | 2026-05-22 |
| [`./0007-app-gitops-onboarding-policy.md`](./0007-app-gitops-onboarding-policy.md)                         | 앱 온보딩 운영 정책 (Rollout 필수/이미지 태그/Istio 포트 명명/Traefik/Vault 규칙)       | Active | 2026-05-22 |
