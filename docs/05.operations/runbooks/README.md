---
title: "05.operations/runbooks"
version: "0.1.5"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "operations"
---
# 05.operations/runbooks

> 반복 가능한 운영 작업을 즉시 실행할 수 있는 체크리스트/절차 문서를 관리한다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../../.agents/README.md).

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

### Collection Readers

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

## Item Index

### 문서 인덱스

| 문서 | 설명 |
| --- | --- |
| [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md) | 부트스트랩과 외부 서비스 endpoint 복구의 단일 owner |
| [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md) | OpenBao sealed·auth drift 분류, ESO 복구, CoreDNS·gateway CA 재적용의 단일 owner |
| [`./0003-platform-expansion-bootstrap-runbook.md`](./0003-platform-expansion-bootstrap-runbook.md) | cert-manager/Istio/Kiali 부트스트랩 런북 |
| [`./0004-rollouts-notifications-headlamp-runbook.md`](./0004-rollouts-notifications-headlamp-runbook.md) | Rollouts/Notifications/Headlamp 운영·복구 런북 |
| [`./0007-kiali-observability-connectivity-runbook.md`](./0007-kiali-observability-connectivity-runbook.md) | Kiali 외부 route·Tempo·Grafana auth 진단 런북 |
| [`./0008-argocd-metrics-prometheus-runbook.md`](./0008-argocd-metrics-prometheus-runbook.md) | ArgoCD component 메트릭(in-cluster 수집) 진단 런북 |
| [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md) | in-cluster Alloy 메트릭·로그·remote write·AppProject 진단 런북 |
| [`./0010-github-app-gitops-onboarding-runbook.md`](./0010-github-app-gitops-onboarding-runbook.md) | 앱 GitOps 온보딩·검증·복구 런북 |
| [`./0011-reference-maintenance-runbook.md`](./0011-reference-maintenance-runbook.md) | Stage 90 Audit/Data/Research pack 유지보수 런북 |

## Add and Find

1. 관련 Spec/Operations를 먼저 확인해 계약값을 고정한다.
2. [runbook.template.md](../../99.templates/templates/operations/runbook.template.md)를 기반으로 작성한다.
3. 절차는 명령 실행 순서와 검증 기준을 함께 제시한다.
4. 복구 절차에는 롤백, 재동기화, 증적 수집 단계를 반드시 포함한다.
5. 정책 통제 기준은 런북에 복제하지 말고 [policies](../policies/README.md)로 연결한다.
6. 고위험 명령 예시는 [Operations Mutation Boundary](../README.md#operations-mutation-boundary)를 따른다.

### Usage Instructions

이 영역은 운영자가 정해진 순서대로 실행할 절차가 필요할 때 사용한다.

1. 관련 Policy와 Spec에서 허용 범위와 계약값을 확인한다.
2. Runbook의 `When to Use`와 `Procedure or Checklist`를 따라 실행한다.
3. 실행 후 `Verification Steps`와 `Observability and Evidence Sources`에 맞춰 증적을 남긴다.

### Verification and Monitoring

- Runbook 문서 구조 검증은 [runbook.template.md](../../99.templates/templates/operations/runbook.template.md)와 `scripts/qa.py`를 기준으로 한다.
- 작업 증적은 명령 출력, GitOps diff, ArgoCD sync 상태, dashboard/log snapshot, CI 결과 중 해당 Runbook이 요구하는 항목으로 남긴다.

### Incident and Recovery Links

- Policies: [05.operations/policies](../policies/README.md)
- Incident Records: [05.operations/incidents](../incidents/README.md)
- Postmortems: `../incidents/<year>/inc-####-<slug>/postmortem.md`

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/05.operations/runbooks/`다.

- 같은 폴더의 Runbook 문서는 `./`로 시작한다.
- sibling operations folder는 `../guides/`, `../policies/`, `../incidents/`로 연결한다.
- upstream docs stage는 `../../02.architecture/`, `../../03.specs/`로 연결한다.

## Related Documents

- [05.operations/guides](../guides/README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/incidents](../incidents/README.md)
- [AD](../../02.architecture/descriptions/0007-current-local-gitops-platform.md)
- [ADR](../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- [Spec](../../03.specs/0008-current-local-gitops-platform/spec.md)
- [Operations Policy](../policies/0001-k8s-gitops-operations-policy.md)
- [Runbook Template](../../99.templates/templates/operations/runbook.template.md)
- [Collection Index README Form](../../99.templates/templates/common/readme-collection-index.template.md)
