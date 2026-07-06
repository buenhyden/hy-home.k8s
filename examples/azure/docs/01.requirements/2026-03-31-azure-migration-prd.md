---
title: 'Azure Migration Product Requirements Document'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-06
---

# Azure Migration Product Requirements Document

## Overview

이 문서는 `hy-home.k8s` 로컬 인프라를 Azure 클라우드로 마이그레이션하기 위한 제품 요구사항을 정의한다. 로컬 환경의 물리적 제약을 극복하고, 2026년 기준 최신 Azure 관리형 서비스를 활용하여 엔터프라이즈급의 확장성, 보안성 및 가동성을 확보하는 것을 목표로 한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Vision

로컬 제약이 없는 시스템 확장이 가능하며, 클라우드 네이티브 보안 모델(Workload Identity)을 통해 안전하고 유지보수가 용이한 글로벌 인프라 기반을 구축한다.

## Problem Statement

현재 K3s/k3d 로컬 환경은 다음과 같은 제약이 있다:

- **확장성 부족**: 로컬 하드웨어 자원의 한계로 대규모 워크로드 배포가 어려움.
- **운영 부담**: 데이터베이스(PostgreSQL), 하이브리드 캐시(Valkey) 등의 수동 관리 및 백업 복구 절차의 복잡성.
- **보안 격리 미비**: 물리적 네트워크 내에서의 시크릿 관리와 외부 접근 제어의 한계.

## Personas

- **Platform Engineer**: 인프라 프로비저닝 자동화 및 클러스터 관리 효율성 필요.
- **Application Developer**: 안정적인 런타임 환경과 간편한 시크릿 접근 수단(Identity 기반) 필요.
- **SRE/Ops**: 중앙 집중화된 모니터링 및 실시간 장애 대응 체계 필요.

## Key Use Cases

- **STORY-01**: 개발자는 로컬 환경과 동일한 GitOps 워크플로우를 통해 Azure AKS 클러스터에 애플리케이션을 배포할 수 있어야 한다.
- **STORY-02**: 시스템은 트래픽 증가 시 AKS 노드 풀을 자동으로 확장하여 서비스 연속성을 보장해야 한다.
- **STORY-03**: 모든 서비스는 패스워드 없이 Managed Identity를 통해 Azure Key Vault와 DB에 접근해야 한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: AKS 클러스터는 Azure CNI Overlay 네트워킹을 사용해야 한다.
- **REQ-PRD-FUN-02**: 모든 L7 트래픽은 Application Gateway for Containers (AGC)를 통해 처리되어야 한다.
- **REQ-PRD-FUN-03**: 데이터베이스 및 캐시는 Azure 관리형 서비스(PostgreSQL Flexible, Redis)로 대체되어야 한다.
- **REQ-PRD-FUN-04**: 2026년 보안 표준인 Entra ID Workload Identity를 지원해야 한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: 인프라 배포 자동화율 100% (Bicep/IaC 기반).
- **REQ-PRD-MET-02**: 애플리케이션 가동률(SLA) 99.9% 이상 확보.
- **REQ-PRD-MET-03**: 시크릿 관리 체계 전환 완료 (Vault -> Key Vault + Identity).

## Scope and Non-goals

- **In Scope**: AKS 클러스터 구성, AGC 네트워킹, 관리형 DB/Redis 연동, Workload Identity 설정, 문서화.
- **Out of Scope**: 프론트엔드/백엔드 애플리케이션 코드 수정 (인프라 연동 레이어 제외), 레거시 데이터 완전 마이그레이션 도구 개발.
- **Non-goals**: 로컬 k3s 클러스터의 기능을 Azure에서 100% 동일하게 복제하는 것(더 나은 클라우드 네이티브 방식으로 개선하는 것이 목표).

## Risks, Dependencies, and Assumptions

- **Cloud Cost**: 관리형 서비스 사용에 따른 비용 발생 (사전 견적 필요).
- **Network Latency**: 로컬 시스템과 Azure 간의 데이터 이관 시 네트워크 지연 고려 필요.
- **Entra ID Access**: 적절한 Azure Subscription 및 권한(Owner 이상)이 확보되어 있어야 함.

## Related Documents

- **AARD**: [../02.architecture/requirements/2026-03-31-azure-migration-ard.md](../02.architecture/requirements/2026-03-31-azure-migration-ard.md)
- **Spec**: [../03.specs/2026-03-31-resource-specs.md](../03.specs/2026-03-31-resource-specs.md)
- **Plan**: [../04.execution/plans/2026-03-31-migration-strategy.md](../04.execution/plans/2026-03-31-migration-strategy.md)
- **ADR**: [../02.architecture/decisions/2026-03-31-adr-agc-selection.md](../02.architecture/decisions/2026-03-31-adr-agc-selection.md)
