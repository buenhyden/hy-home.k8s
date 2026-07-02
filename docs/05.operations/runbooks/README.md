# 05.operations/runbooks

> 반복 가능한 운영 작업을 즉시 실행할 수 있는 체크리스트/절차 문서를 관리한다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 운영자가 장애 상황 또는 재구축 상황에서 바로 실행 가능한 절차를 제공한다.
정책 정의는 [policies](../policies/README.md), 가이드 설명은 [guides](../guides/README.md), 사고 분석은 [incidents](../incidents/README.md)에서 관리한다.

런북은 “정해진 순서로 실행하고, 증적을 남기고, 실패 시 복구하는 문서”다.
배경 설명과 온보딩은 [guides](../guides/README.md), 허용/금지/예외 기준은 [policies](../policies/README.md), 실제 사고 기록은 [incidents](../incidents/README.md)로 보낸다.

| 필요 상황                                | 문서 유형     |
| ---------------------------------------- | ------------- |
| 명령 순서, 검증 기준, 복구 경로가 필요함 | Runbook       |
| 장애 시그니처를 보고 대응해야 함         | Runbook       |
| 정책의 허용/금지 기준을 확인해야 함      | Policy로 이동 |
| 작업 배경과 선행 지식을 익혀야 함        | Guide로 이동  |

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 실행 순서 중심 체크리스트
- 검증 커맨드와 성공 기준
- 오류 시그니처 기반 트러블슈팅
- 안전한 롤백/복구 절차

### Out of Scope

- 정책 통제의 정의 자체
- 튜토리얼 중심 배경 설명
- 사고 원인 분석 보고서

## Structure

```text
docs/05.operations/runbooks/
├── 0001-argocd-platform-bootstrap-runbook.md               # k3d + ArgoCD 부트스트랩/복구 런북
├── 0002-argocd-eso-vault-recovery-runbook.md               # Vault/ESO 복구 + TLS/CI 계약 회귀 검증
├── 0003-platform-expansion-bootstrap-runbook.md             # cert-manager/Headlamp/Istio/Kiali 부트스트랩
├── 0004-rollouts-notifications-headlamp-runbook.md          # Rollouts/Notifications/Headlamp 운영
├── 0007-kiali-observability-connectivity-runbook.md         # Kiali 관측성 연결 복구
├── 0008-argocd-metrics-prometheus-runbook.md                # ArgoCD metrics/Prometheus 복구
├── 0009-k8s-observability-runbook.md                        # 관측성 스택 장애 진단
├── 0010-github-app-gitops-onboarding-runbook.md             # GitHub 앱 온보딩 절차
├── 0011-reference-maintenance-runbook.md                     # 90.references 유지보수 절차
└── README.md                                                # This file
```

## How to Work in This Area

1. 관련 Spec/Operations를 먼저 확인해 계약값을 고정한다.
2. [runbook.template.md](../../99.templates/templates/sdlc/operations/runbook.template.md)를 기반으로 작성한다.
3. 절차는 명령 실행 순서와 검증 기준을 함께 제시한다.
4. 복구 절차에는 롤백, 재동기화, 증적 수집 단계를 반드시 포함한다.
5. 정책 통제 기준은 런북에 복제하지 말고 [policies](../policies/README.md)로 연결한다.
6. live cluster mutation, Vault write, kubeconfig 변경 예시는 human-approved, bootstrap-only, break-glass 문맥을 유지한다.

## Usage Instructions

이 영역은 운영자가 정해진 순서대로 실행할 절차가 필요할 때 사용한다.

1. 관련 Policy와 Spec에서 허용 범위와 계약값을 확인한다.
2. Runbook의 `When to Use`와 `Procedure or Checklist`를 따라 실행한다.
3. 실행 후 `Verification Steps`와 `Observability and Evidence Sources`에 맞춰 증적을 남긴다.

## Verification and Monitoring

- Runbook 문서 구조 검증은 [runbook.template.md](../../99.templates/templates/sdlc/operations/runbook.template.md)와 `scripts/validate-repo-quality-gates.sh`를 기준으로 한다.
- 작업 증적은 명령 출력, GitOps diff, ArgoCD sync 상태, dashboard/log snapshot, CI 결과 중 해당 Runbook이 요구하는 항목으로 남긴다.
- live cluster, Vault, Kubernetes mutation은 human-approved bootstrap 또는 break-glass 작업에서만 실행한다.

## Incident and Recovery Links

- Policies: [05.operations/policies](../policies/README.md)
- Incident Records: [05.operations/incidents](../incidents/README.md)
- Postmortems: `../incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md`

## Link Basis

이 README의 링크 기준 위치는 `docs/05.operations/runbooks/`다.

- 같은 폴더의 Runbook 문서는 `./`로 시작한다.
- sibling operations folder는 `../guides/`, `../policies/`, `../incidents/`로 연결한다.
- upstream docs stage는 `../../02.architecture/`, `../../03.specs/`, `../../04.execution/`로 연결한다.

## Related Documents

- [05.operations/guides](../guides/README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/incidents](../incidents/README.md)
- [ARD](../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- [ADR](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- [Spec](../../03.specs/008-current-local-gitops-platform/spec.md)
- [Operations Policy](../policies/0002-wsl2-k3d-gitops-ha-operations-policy.md)
- [Runbook Template](../../99.templates/templates/sdlc/operations/runbook.template.md)
- [README Template](../../99.templates/templates/common/readme.template.md)

## 문서 인덱스

| 문서                                                                                                       | 설명                                                                   | 상태   | 최종 수정  |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------ | ---------- |
| [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)               | 검증 커맨드 기반 부트스트랩/트러블슈팅/복구 런북                       | Active | 2026-05-22 |
| [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)               | Vault sealed/EndpointSlice/Auth drift 분류 + ESO 복구 + TLS/Ingress + CI 정적 계약 회귀 검증 런북 | Active | 2026-06-02 |
| [`./0003-platform-expansion-bootstrap-runbook.md`](./0003-platform-expansion-bootstrap-runbook.md)         | cert-manager/Headlamp/Istio/Kiali 부트스트랩 및 증상별 복구 런북       | Active | 2026-06-02 |
| [`./0004-rollouts-notifications-headlamp-runbook.md`](./0004-rollouts-notifications-headlamp-runbook.md)   | Argo Rollouts/Notifications/Headlamp 설치 및 운영 런북                 | Active | 2026-05-09 |
| [`./0007-kiali-observability-connectivity-runbook.md`](./0007-kiali-observability-connectivity-runbook.md) | Kiali 관측성 서비스 연결 장애 진단 및 복구 런북                        | Active | 2026-05-09 |
| [`./0008-argocd-metrics-prometheus-runbook.md`](./0008-argocd-metrics-prometheus-runbook.md)               | ArgoCD 메트릭 NodePort/Prometheus 수집 장애 진단 및 복구 런북          | Active | 2026-05-09 |
| [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)                               | kube-state-metrics/alloy/alert_rules/AppProject 장애 진단 런북         | Active | 2026-05-09 |
| [`./0010-github-app-gitops-onboarding-runbook.md`](./0010-github-app-gitops-onboarding-runbook.md)         | GitHub 레포 기반 앱 온보딩 절차 런북 (최소 템플릿 + adminer reference) | Active | 2026-05-26 |
| [`./0011-reference-maintenance-runbook.md`](./0011-reference-maintenance-runbook.md)                       | `90.references` reference/version/LLM Wiki 유지보수 절차 런북          | Active | 2026-05-17 |
