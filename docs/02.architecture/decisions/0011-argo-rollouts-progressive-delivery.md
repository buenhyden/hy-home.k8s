# ADR-0011: Argo Rollouts for Progressive Delivery

## Overview (KR)

Argo Rollouts를 플랫폼에 도입하여 canary/blue-green 배포 전략을 지원한다.
Rollouts Dashboard UI를 함께 설치하여 시각적 롤아웃 상태 관리를 제공한다.

## Context

현재 플랫폼은 ArgoCD의 기본 Deployment 기반 배포만 지원한다.
점진적 배포(canary, blue-green)와 Prometheus 메트릭 기반 자동 promotion/abort가 필요하다.
Argo Rollouts는 ArgoCD와 동일 생태계(argoproj)에서 기본 통합을 제공한다.

> **현재 실행계약 메모 (2026-05-09)**: 아래 외부 Prometheus `172.19.x` 주소는 2026-03-30 기준의 역사적 `infra_net` 계약이다. 현재 repo-backed 실행계약은 `gitops/platform/external-services/prometheus-external.yaml`, 관련 NetworkPolicy, 정적 검증 스크립트의 `172.18.0.10` 값이 우선한다.

## Decision

- Argo Rollouts v1.9.0 (chart 2.40.9)을 `argo-rollouts` namespace에 설치한다.
- Chart: `argoproj.github.io/argo-helm`, chart name: `argo-rollouts`
- Rollouts Dashboard를 함께 활성화하고 `rollouts.127.0.0.1.nip.io`로 노출한다.
- Controller metrics 활성화 (외부 Prometheus `172.19.0.20`으로 수집).
- 기본 promotion 전략: 수동 승인 (analysis-run 없이).
- Prometheus analysis provider는 외부 Prometheus endpoint 사용.

## Explicit Non-goals

- 자동 promotion (수동 프로모션 기본)
- 멀티클러스터 Rollouts
- 커스텀 Analysis metric 정의 (초기 설치 범위 외)

## Alternatives

| 옵션          | 평가                                                         |
| ------------- | ------------------------------------------------------------ |
| Argo Rollouts | ArgoCD 네이티브 통합, Prometheus 분석, Rollouts Dashboard UI |
| Flagger       | Flagger는 Istio/Nginx 컨트롤러 의존성 강하여 추가 복잡도     |
| 수동 배포     | 안전하지만 자동화 없음                                       |

## Consequences

- `argo-rollouts` namespace 추가
- AppProject에 `argoproj.github.io/argo-helm` repo, `argo-rollouts` namespace 추가
- AppProject clusterResourceWhitelist에 `Rollout`, `AnalysisTemplate`, `ClusterAnalysisTemplate`, `AnalysisRun` 추가
- 외부 Traefik artifact `rollouts-k3d.yaml` 필요
- 앱 팀은 `Deployment` → `Rollout` manifest 변환 필요 (apps namespace에서)

## Status

Accepted — 2026-03-30

## Related Documents

- [ADR-0002](./0002-argocd-helm-and-gitops-model.md) — ArgoCD GitOps 모델
- [ADR-0012](./0012-argo-notifications-slack.md) — Rollouts 이벤트 알림
- [PRD](../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md)
- [ARD](../requirements/0004-argo-rollouts-progressive-delivery.md)
- [Spec](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- [Plan](../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- [Task](../../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
