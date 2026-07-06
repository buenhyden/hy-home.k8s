---
title: 'Azure Migration Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-07-06
---

# Azure Migration Implementation Plan

## Overview

이 문서는 로컬 k3s 인프라를 Azure 클라우드로 이식하기 위한 단계별 실행 계획과 마일스톤을 정의한다.

## Snapshot Boundary

This document is an example-local SDLC snapshot for cloud migration reference. It follows the repository's Cloud Example Snapshot boundary and is not live provider-latest guidance.

## Milestones

| Milestone | Description | Target Date | Status |
| :--- | :--- | :--- | :--- |
| **M1: Design** | PRD, ARD, ADR, Spec 설계 완료 | 2026-03-31 | [x] |
| **M2: Infrastructure** | Bicep을 통한 Azure 리소스 프로비저닝 | 2026-04-05 | [ ] |
| **M3: Platform** | AKS 초기 설정 및 ArgoCD 부트스트랩 | 2026-04-10 | [ ] |
| **M4: Workloads** | 관리형 서비스 연동 및 애플리케이션 배포 | 2026-04-15 | [ ] |
| **M5: Verification** | 성능/보안 테스트 및 운영 환경 이관 | 2026-04-20 | [ ] |

## Phase 1: Infrastructure Provisioning

- Bicep을 사용하여 VNet, Subnet(AKS, Data) 구성.
- AKS 클러스터 생성 (System/User Node Pool).
- Azure Database for PostgreSQL Flexible Server 배포.
- Azure Cache for Redis 배포.
- Azure Key Vault 및 Private Link 구성.

## Phase 2: Platform Bootstrapping

- AKS 클러스터 RBAC 구성 및 kubectl 접속 확인.
- Helm을 통한 ArgoCD 설치 및 Azure용 values 적용.
- cert-manager를 통한 Let's Encrypt TLS 발급(Azure DNS-01) 설정.
- Application Gateway for Containers(ALB) 컨트롤러 설치.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Task**: [../04.execution/tasks/0001-aks-cluster-provisioning.md](../tasks/0001-aks-cluster-provisioning.md)
