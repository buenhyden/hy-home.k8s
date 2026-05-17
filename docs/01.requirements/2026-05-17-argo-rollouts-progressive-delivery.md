---
title: 'Argo Rollouts Progressive Delivery Product Requirements'
type: prd
status: draft
owner: platform-team
updated: 2026-05-17
---

# Argo Rollouts Progressive Delivery Product Requirements

## Overview (KR)

이 문서는 `hy-home.k8s` 플랫폼에 Argo Rollouts를 도입하여 canary/blue-green 점진적 배포 전략과 Prometheus 메트릭 기반 자동 promotion/abort를 지원하기 위한 제품 요구사항을 정의한다.

## Vision

플랫폼 엔지니어와 애플리케이션 팀이 배포 위험을 최소화하면서 점진적으로 새 버전을 출시할 수 있는 표준 GitOps 배포 전략을 갖춘다.

## Problem Statement

현재 플랫폼은 ArgoCD의 기본 `Deployment` 기반 배포만 지원한다. 한 번에 전체를 교체하는 방식은 결함 있는 릴리스가 배포될 경우 즉각적인 서비스 영향을 초래한다. 점진적 배포(canary, blue-green)와 Prometheus 메트릭 기반 자동 promotion/abort를 통해 배포 안전성을 높여야 한다.

## Personas

- **Platform Engineer**: Rollouts 컨트롤러를 GitOps로 관리하고, 대시보드 UI로 롤아웃 상태를 시각적으로 확인하고 싶다.
- **Application Team**: `Deployment`를 `Rollout` 리소스로 전환하여 canary/blue-green 전략을 적용하고 싶다.
- **DevOps Engineer**: Prometheus 메트릭 기반 자동 promotion/abort로 배포 안정성을 보장하고 싶다.

## Key Use Cases

- **STORY-01**: 운영자가 Rollouts Dashboard UI(`rollouts.127.0.0.1.nip.io`)에서 현재 롤아웃 상태와 진행률을 실시간으로 확인한다.
- **STORY-02**: 애플리케이션 팀이 `Rollout` 리소스로 canary 배포를 정의하고 수동 승인으로 안전하게 promotion한다.
- **STORY-03**: Prometheus 메트릭이 임계값을 초과하면 AnalysisRun이 자동으로 배포를 abort한다.
- **STORY-04**: ArgoCD가 `Rollout` 리소스를 인식하고 sync 상태를 정상적으로 추적한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: Argo Rollouts v1.9.0(chart 2.40.9)을 `argo-rollouts` namespace에 GitOps 방식으로 설치해야 한다.
- **REQ-PRD-FUN-02**: Rollouts Dashboard UI를 `rollouts.127.0.0.1.nip.io`(ingress-nginx + cert-manager TLS)로 노출해야 한다.
- **REQ-PRD-FUN-03**: Controller metrics를 활성화하고 외부 Prometheus endpoint에서 수집할 수 있어야 한다.
- **REQ-PRD-FUN-04**: ArgoCD AppProject에 `argo-rollouts` namespace와 Rollouts 관련 CRD(`Rollout`, `AnalysisTemplate`, `ClusterAnalysisTemplate`, `AnalysisRun`)를 허용해야 한다.
- **REQ-PRD-FUN-05**: 기본 promotion 전략은 수동 승인(analysis-run 없이)을 사용해야 한다.
- **REQ-PRD-FUN-06**: 외부 Traefik router를 통해 `rollouts.127.0.0.1.nip.io` 접근을 라우팅해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: `argo-rollouts-controller` Deployment `Available=True`.
- **REQ-PRD-MET-02**: `rollouts.127.0.0.1.nip.io` Dashboard HTTPS 접근 성공(mkcert CA 신뢰).
- **REQ-PRD-MET-03**: ArgoCD가 `Rollout` 리소스 sync 상태를 정상적으로 추적(`Healthy`/`Progressing`).
- **REQ-PRD-MET-04**: CI 정적 게이트(`verify-contracts-static.sh`) PASS.

## Scope and Non-goals

- **In Scope**:
  - Argo Rollouts 컨트롤러 및 Rollouts Dashboard GitOps 설치
  - AppProject 허용 목록 업데이트 (CRD, namespace)
  - 외부 Traefik router 설정
  - 문서 체인 동기화
- **Out of Scope**:
  - 개별 애플리케이션의 `Deployment` → `Rollout` 전환 (앱 팀 담당)
  - 멀티클러스터 Rollouts
- **Non-goals**:
  - 자동 promotion (수동 승인이 기본)
  - 커스텀 Analysis metric 정의 (초기 설치 범위 외)
  - Prometheus analysis provider 연동 (후속 Phase)

## Risks, Dependencies, and Assumptions

- AppProject allow-list 업데이트 누락 시 ArgoCD sync 실패.
  - **Mitigation**: Plan에서 AppProject 업데이트를 Rollouts 설치 전 단계로 명시.
- Rollouts Dashboard 접근을 위해 외부 Traefik repo에서 별도 artifact(`rollouts-k3d.yaml`) 필요.
- cert-manager `mkcert-ca-issuer`가 이미 설치된 상태를 전제한다 (PRD `2026-03-29` 의존).

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: GitOps manifest 생성/갱신, 상태 검증, 문서 갱신.
- **Disallowed Actions**: 승인 없는 AppProject 권한 확장, 직접 클러스터 조작.
- **Human-in-the-loop Requirement**: AppProject clusterResourceWhitelist 변경 시 승인 필요.
- **Evaluation Expectation**: 컨트롤러 상태, Dashboard 접근, ArgoCD sync 추적을 검증 스크립트로 확인.

## Related Documents

- **ADR**: [`../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)
- **PRD**: [`./2026-03-29-platform-expansion-dashboard-mesh.md`](./2026-03-29-platform-expansion-dashboard-mesh.md) — cert-manager 의존
