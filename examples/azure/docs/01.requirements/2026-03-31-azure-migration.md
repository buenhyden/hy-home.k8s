---
title: 'Azure Migration PRD (Product Requirements Document)'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-06
---

# Azure Migration PRD (Product Requirements Document)

## Overview

본 문서는 로컬 k3s/k3d 환경의 `hy-home.k8s` 인프라를 2026-05-09 공식 지원 스냅샷 기준 Azure(AKS) 환경으로 마이그레이션하기 위한 요구사항을 정의한다. 로컬 환경의 관리 복잡성과 가용성 한계를 해결하고, 클라우드 네이티브 관리형 서비스(AGC, Managed Identity, PostgreSQL Flexible)를 통해 엔터프라이즈급 안정성을 확보하는 것이 목표다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Current Situation Audit (Analysis)

로컬 `hy-home.k8s` 인프라는 다음과 같이 구성되어 있다.

- **Cluster**: k3d v1.35.0 (1 Server, 3 Agents).
- **Ingress/LB**: MetalLB (Layer 2) 및 Ingress-Nginx 또는 Traefik (k3d 기본).
- **Secrets**: HashiCorp Vault (`vault.127.0.0.1.nip.io`).
- **Database**: 외부 PostgreSQL 인스턴스 (`172.18.0.15:15432`).
- **Cache**: 외부 Valkey (Redis-compatible) 인스턴스 (`172.18.0.9:6379`).
- **Observability**: Prometheus/Alloy/Loki/Tempo/Grafana의 개별 외부 스택.

### Pain Points

1. **관리 오버헤드**: 데이터베이스 및 캐시의 고가용성(HA)을 로컬에서 수동으로 관리해야 함.
2. **보안/인증**: Vault 토큰 및 정적 자격 증명(Database Password) 관리가 분산되어 있음.
3. **확장성**: 단일 물리 노드(또는 VM)의 리소스 한계로 인해 스케일 아웃이 불가능함.

## Target Requirements (2026-05-09 Snapshot)

### Functional Requirements (FR)

- **REQ-PRD-001**: AKS 1.35 target 클러스터로의 모든 워크로드 이전 및 무중단 가동.
- **REQ-PRD-002**: L7 입구(Ingress)는 **Application Gateway for Containers (AGC)**와 **Gateway API (v1)**를 도입한다.
- **REQ-PRD-003**: 인프라 인증은 **Managed Identity** 및 **Workload Identity (OIDC Federation)** 체계로 일원화한다 (Passwordless).
- **REQ-PRD-004**: 모든 시크릿은 Azure Key Vault와 **Secret Store CSI Driver**를 연동하여 파일로 마운트한다.

### Non-Functional Requirements (NFR)

- **REQ-NFR-101 (Security)**: Entra ID 통합을 통한 RBAC 통제 및 테넌트 격리.
- **REQ-NFR-102 (Availability)**: PostgreSQL 및 Redis의 99.9% 이상 관리형 가용성 보장 (Zone-redundant HA).
- **REQ-NFR-103 (Maintainability)**: 모든 인프라는 Bicep(IaC)으로 정의하고, 앱 배포는 ArgoCD(GitOps)를 표준으로 한다.

## Success / Acceptance Criteria

1. Bicep을 통한 Azure 리소스 배포 성공 및 AKS 노드 Readiness 확보.
2. 외부 트래픽이 AGC를 통해 AKS 내부 서비스로 정상 라우팅됨 (200 OK).
3. Pod 내부에서 패스워드 없이 DB 및 Key Vault에 접근 성공 (Workload Identity 검증).

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../03.specs/azure-migration/spec.md)
- **ADR**: [../02.architecture/decisions/README.md](../02.architecture/decisions/README.md)
