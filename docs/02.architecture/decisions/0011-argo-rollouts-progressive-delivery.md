---
title: 'ADR-0011: Argo Rollouts for Progressive Delivery'
type: adr
status: accepted
owner: platform
updated: 2026-06-04
---

# ADR-0011: Argo Rollouts for Progressive Delivery

## Overview (KR)

Argo Rollouts를 플랫폼에 도입하여 canary/blue-green 배포 전략을 지원한다.
Rollouts Dashboard UI를 함께 설치하여 시각적 롤아웃 상태 관리를 제공한다.

## Context

현재 플랫폼은 ArgoCD의 기본 Deployment 기반 배포만으로는 점진적 배포 안전성을 충분히 표현하기 어렵다.
점진적 배포(canary, blue-green), Prometheus 메트릭 기반 AnalysisRun, 실패 시 자동 abort/rollback 경계가 필요하다.
Argo Rollouts는 ArgoCD와 동일 생태계(argoproj)에서 기본 통합을 제공한다.

## Decision

- Argo Rollouts v1.9.0 (chart 2.40.9)을 `argo-rollouts` namespace에 설치한다.
- Chart: `argoproj.github.io/argo-helm`, chart name: `argo-rollouts`
- Rollouts Dashboard를 함께 활성화하고 `rollouts.127.0.0.1.nip.io`로 노출한다.
- Controller metrics 활성화 (외부 Prometheus `172.18.0.10`으로 수집).
- 기본 promotion 정책은 자동 promotion을 강제하지 않는다. 앱별 Rollout은 승인된 Prometheus AnalysisTemplate을 사용할 수 있다.
- Prometheus analysis provider는 외부 Prometheus endpoint 사용.

## Explicit Non-goals

- 자동 promotion 강제 (수동 프로모션 기본)
- 멀티클러스터 Rollouts
- 플랫폼-wide 커스텀 Analysis metric 표준화

## Consequences

- `argo-rollouts` namespace 추가
- AppProject에 `argoproj.github.io/argo-helm` repo, `argo-rollouts` namespace 추가
- AppProject `platform`은 Rollouts chart repo와 `argo-rollouts` namespace를 허용하고, AppProject `apps` namespaceResourceWhitelist는 workload consumption을 위해 `Rollout`, `AnalysisTemplate`을 허용
- 외부 Traefik artifact `rollouts-k3d.yaml` 필요
- 앱 팀은 `Deployment` → `Rollout` manifest 변환 필요 (apps namespace에서)

## Alternatives

| 옵션          | 평가                                                         |
| ------------- | ------------------------------------------------------------ |
| Argo Rollouts | ArgoCD 네이티브 통합, Prometheus 분석, Rollouts Dashboard UI |
| Flagger       | Flagger는 Istio/Nginx 컨트롤러 의존성 강하여 추가 복잡도     |
| 수동 배포     | 안전하지만 자동화 없음                                       |

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
