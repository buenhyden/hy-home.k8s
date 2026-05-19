---
title: 'WSL2 k3s/k3d + ArgoCD GitOps Platform Product Requirements'
type: prd
status: draft
owner: platform-team
updated: 2026-05-17
---

# WSL2 k3s/k3d + ArgoCD GitOps Platform Product Requirements

## Overview (KR)

이 문서는 Windows WSL2(Ubuntu) 환경에서 k3d(k3s) 기반 멀티노드 Kubernetes 플랫폼과 ArgoCD GitOps 파이프라인을 구축하기 위한 제품 요구사항을 정의한다. 외부 서비스(Vault, PostgreSQL, Valkey) 연동과 문서 추적성을 핵심 성공 기준으로 삼는다.

> **현재 실행계약 메모 (2026-05-09)**: 이 PRD는 초기 플랫폼 요구사항 기록이다. 현재 repo-backed 외부 서비스 실행계약은 `gitops/platform/external-services/`, `gitops/platform/network-policies/`, `infrastructure/tests/verify-contracts-static.sh`의 `172.18.x` EndpointSlice/CIDR 값이 우선한다.

## Requirement Status

이 PRD는 초기 플랫폼 요구사항을 보존하는 historical draft다.
현재 구현 기준은 위 current contract 메모와 연결된 ARD/Spec/Plan이 소유한다.
이 문서의 오래된 네트워크 값은 실행계약이 아니라 요구사항 이력으로 읽어야 한다.

## Vision

Create a reproducible, secure, and automation-first local platform that mirrors production-grade GitOps workflows for development and operations teams.

## Problem Statement

현재 로컬/개발 Kubernetes 환경은 배포 표준, 시크릿 관리, 외부 데이터 서비스 연동 방식이 분산되어 있어 재현성·보안성·운영 효율이 낮다. 표준화된 GitOps 기반 아키텍처와 문서 체계를 통해 이를 해결해야 한다.

## Personas

- **Platform Engineer**: WSL 기반에서 빠르게 클러스터를 재구축하고 정책을 강제하고 싶다.
- **DevOps Engineer**: Git 기반 선언형 배포와 롤백/복구 경로를 일관되게 운영하고 싶다.
- **Application Team**: Vault/DB/Cache 연결을 Kubernetes 표준 리소스로 안정적으로 소비하고 싶다.

## Key Use Cases

- **STORY-01**: 엔지니어는 WSL2에서 `1 server + 3 agents` k3d 클러스터를 재현 가능하게 구축한다.
- **STORY-02**: 운영자는 ArgoCD App-of-Apps로 플랫폼 구성요소를 선언형으로 배포/동기화한다.
- **STORY-03**: 애플리케이션은 ESO를 통해 Vault에서 시크릿을 동기화해 사용한다.
- **STORY-04**: 애플리케이션/ArgoCD는 외부 PostgreSQL/Valkey를 Kubernetes 표준 인터페이스(Service) 경유로 사용한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: k3d 클러스터는 `servers=1`, `agents=3` 토폴로지를 제공해야 한다.
- **REQ-PRD-FUN-02**: k3s 기본 Traefik은 비활성화하고 ingress-nginx를 사용해야 한다.
- **REQ-PRD-FUN-03**: ArgoCD는 Helm 기반으로 설치/업그레이드 가능해야 한다.
- **REQ-PRD-FUN-04**: App-of-Apps + ApplicationSet으로 앱 선언을 자동 생성/동기화해야 한다.
- **REQ-PRD-FUN-05**: Vault 연동은 ESO + Kubernetes Auth를 사용해야 한다.
- **REQ-PRD-FUN-06**: 외부 PostgreSQL은 안정적인 고정 endpoint 계약으로 노출되어야 한다. 초기 기록의 `172.30.0.0/24` 값은 historical requirement이며, 현재 값은 current contract 메모의 repo-backed 계약을 따른다.
- **REQ-PRD-FUN-07**: PostgreSQL은 Service + EndpointSlice로 래핑하고, Valkey는 ExternalName Service, Vault는 외부 URL 계약을 사용해야 한다.
- **REQ-PRD-FUN-08**: ArgoCD 백엔드는 외부 Valkey를 사용해야 한다.
- **REQ-PRD-FUN-09**: 문서 체계는 `01.requirements`부터 `05.operations`까지의 산출물과 상호 상대링크를 제공해야 한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: Platform Engineer가 로컬 클러스터를 30분 이내 재구축할 수 있다. Evidence: 연결된 Plan/Task의 bootstrap 검증 기록.
- **REQ-PRD-MET-02**: 운영자가 ArgoCD 동기화 상태를 안정적으로 확인할 수 있다. Evidence: 테스트 시나리오 기준 ArgoCD 동기화 성공률 99% 이상.
- **REQ-PRD-MET-03**: Documentation Writer와 AI Agent가 PRD에서 downstream 문서로 이동할 수 있다. Evidence: 문서 링크 무결성 검사에서 깨진 상대 링크 0건.
- **REQ-PRD-MET-04**: Security Engineer가 최소권한과 egress 제한을 검증할 수 있다. Evidence: RBAC 최소권한, Vault 정책, egress 제한 검증 통과.

## Scope and Non-goals

- **In Scope**:
  - WSL2 + Docker Desktop 백엔드 기준 클러스터/배포/연동 설계
  - ArgoCD, ESO, 외부 Vault, 외부 PostgreSQL, 외부 Valkey 통합 아키텍처
  - 현재 docs taxonomy 문서화 및 추적성 정립
- **Out of Scope**:
  - 클라우드 관리형 Kubernetes(EKS/AKS/GKE) 배포
  - 애플리케이션 비즈니스 로직 구현
- **Non-goals**:
  - 프로덕션 SLA 직접 보장
  - Vault/DB 고가용성 클러스터 구성 자체 구현

## Risks, Dependencies, and Assumptions

- Docker Desktop/WSL 네트워크 설정이 조직 표준과 충돌할 수 있다.
- 외부 Valkey를 ArgoCD 백엔드로 사용할 때 Helm 값 스키마 차이가 발생할 수 있다.
- 버전은 문서 작성 시점 기준 고정 후 Task-001에서 최신 Stable 재검증을 수행한다.

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: 문서 생성/갱신, 검증 명령 실행, 링크 무결성 검사.
- **Disallowed Actions**: 승인 없는 파괴적 변경(`reset --hard`, 데이터 삭제).
- **Human-in-the-loop Requirement**: 보안 정책 완화, 운영 범위 확장 시 승인 필요.
- **Evaluation Expectation**: 체크리스트 기반 기술/문서 검증 결과를 명시.

## Related Documents

- **ARD**: [`../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md`](../02.architecture/requirements/0001-wsl-k3d-argocd-platform.md)
- **Spec**: [`../03.specs/001-wsl-k3d-argocd-platform/spec.md`](../03.specs/001-wsl-k3d-argocd-platform/spec.md)
- **Plan**: [`../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md`](../04.execution/plans/2026-03-27-wsl-k3d-argocd-platform.md)
- **ADR**: [`../02.architecture/decisions/0001-k3d-topology-and-network.md`](../02.architecture/decisions/0001-k3d-topology-and-network.md), [`../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md), [`../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../02.architecture/decisions/0003-eso-vault-k8s-auth.md), [`../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md`](../02.architecture/decisions/0004-external-services-endpoints-and-valkey-backend.md)
