---
title: 'Argo Rollouts Progressive Delivery Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-06-04
---

# Argo Rollouts Progressive Delivery Product Requirements

## Overview

이 문서는 `hy-home.k8s` 플랫폼에 Argo Rollouts를 도입하여 canary/blue-green 점진적 배포 전략과 Prometheus 메트릭 기반 AnalysisRun 안전 점검, 실패 시 자동 abort/rollback을 지원하기 위한 제품 요구사항을 정의한다.

## Requirement Status

이 PRD는 current-contract backfill 기준의 active 문서다.
Rollouts GitOps 리소스와 운영 문서는 이미 저장소에 존재하며, 2026-05-18에 ARD/Spec/Plan/Task 추적 체인을 보강했다.
이 문서는 제품 의도와 수용 기준을 소유하고, 구현 가능한 계약은 연결된 downstream 문서가 소유한다.

## Vision

플랫폼 엔지니어와 애플리케이션 팀이 배포 위험을 최소화하면서 점진적으로 새 버전을 출시할 수 있는 표준 GitOps 배포 전략을 갖춘다.

## Problem Statement

현재 플랫폼은 ArgoCD의 기본 `Deployment` 기반 배포만으로는 결함 있는 릴리스가 배포될 경우 즉각적인 서비스 영향을 초래할 수 있다. 점진적 배포(canary, blue-green), 수동 promotion 기본 경계, Prometheus 메트릭 기반 AnalysisRun abort/rollback을 통해 배포 안전성을 높여야 한다.

## Personas

- **Platform Engineer**: Rollouts 컨트롤러를 GitOps로 관리하고, 대시보드 UI로 롤아웃 상태를 시각적으로 확인하고 싶다.
- **Application Team**: `Deployment`를 `Rollout` 리소스로 전환하여 canary/blue-green 전략을 적용하고 싶다.
- **DevOps Engineer**: Prometheus 메트릭 기반 AnalysisRun과 실패 시 자동 rollback 경계로 배포 안정성을 보장하고 싶다.

## Key Use Cases

- **STORY-01**: 운영자가 Rollouts Dashboard UI(`rollouts.127.0.0.1.nip.io`)에서 현재 롤아웃 상태와 진행률을 실시간으로 확인한다.
- **STORY-02**: 애플리케이션 팀이 `Rollout` 리소스로 canary 배포를 정의하고 수동 승인으로 안전하게 promotion한다.
- **STORY-03**: Prometheus 메트릭이 임계값을 초과하면 AnalysisRun이 자동으로 배포를 abort한다.
- **STORY-04**: ArgoCD가 `Rollout` 리소스를 인식하고 sync 상태를 정상적으로 추적한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: 플랫폼은 표준 GitOps 흐름 안에서 Argo Rollouts 기반 점진적 배포 기능을 제공해야 한다. 구체 chart/version 계약은 ADR/Spec이 소유한다.
- **REQ-PRD-FUN-02**: Rollouts Dashboard UI를 `rollouts.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출해야 한다.
- **REQ-PRD-FUN-03**: Controller metrics는 운영자가 rollout 상태와 실패 신호를 관찰할 수 있도록 수집 가능해야 한다.
- **REQ-PRD-FUN-04**: ArgoCD는 Rollouts 관련 리소스를 GitOps sync 상태로 추적할 수 있어야 한다. 구체 AppProject 허용 목록은 downstream Spec이 소유한다.
- **REQ-PRD-FUN-05**: 기본 promotion 정책은 자동 promotion을 강제하지 않아야 하며, 앱별 Rollout은 승인된 AnalysisTemplate으로 실패 시 자동 abort/rollback을 수행할 수 있어야 한다.
- **REQ-PRD-FUN-06**: 표준 local route를 통해 `rollouts.127.0.0.1.nip.io` 접근을 제공해야 한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: 운영자가 Rollouts controller 상태를 확인할 수 있다. Evidence: `argo-rollouts-controller` Deployment `Available=True`.
- **REQ-PRD-MET-02**: 운영자가 Dashboard에서 rollout 진행률을 확인할 수 있다. Evidence: `rollouts.127.0.0.1.nip.io` HTTPS 접근 성공.
- **REQ-PRD-MET-03**: 애플리케이션 팀이 Rollout 리소스를 ArgoCD 상태 모델로 추적할 수 있다. Evidence: ArgoCD가 `Rollout` 리소스를 `Healthy` 또는 `Progressing` 상태로 표시.
- **REQ-PRD-MET-04**: CI가 Rollouts 관련 정적 계약 회귀를 차단한다. Evidence: repo quality gate와 정적 계약 검증 PASS.

## Scope and Non-goals

- **In Scope**:
  - Argo Rollouts 컨트롤러 및 Rollouts Dashboard 제공 요구
  - ArgoCD가 Rollouts 리소스를 추적하기 위한 권한/범위 요구
  - Prometheus 기반 AnalysisTemplate 안전 점검 요구
  - 표준 local route 접근 요구
  - 문서 체인 동기화
- **Out of Scope**:
  - 개별 애플리케이션의 `Deployment` → `Rollout` 전환 (앱 팀 담당)
  - 멀티클러스터 Rollouts
- **Non-goals**:
  - 자동 promotion 강제 (수동 승인이 기본)
  - 플랫폼-wide 커스텀 Analysis metric 표준화

## Risks, Dependencies, and Assumptions

- AppProject allow-list 업데이트 누락 시 ArgoCD sync 실패.
  - **Mitigation**: 후속 Spec/Plan에서 AppProject 변경과 검증 순서를 명시.
- Rollouts Dashboard 접근을 위해 외부 Traefik route 계약이 필요하다.
- cert-manager `mkcert-ca-issuer`가 이미 설치된 상태를 전제한다 (현재 baseline PRD 의존).

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: Update PRD/documentation, run non-destructive static validation, and collect read-only status evidence.
- **Disallowed Actions**: Expand AppProject permissions without approval, mutate the live cluster directly, or change manifests outside an approved downstream stage.
- **Human-in-the-loop Requirement**: Required before AppProject cluster resource allow-list changes or rollout promotion policy changes.
- **Evaluation Expectation**: Verify controller status, Dashboard access, and ArgoCD sync traceability in a downstream validation stage.

## Related Documents

- **ARD**: [`../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md`](../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Plan**: [`../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Task**: [`../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- **PRD**: [`./004-current-local-gitops-platform.md`](./004-current-local-gitops-platform.md) — cert-manager 의존
