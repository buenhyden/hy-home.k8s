# AWS Migration Product Requirements Document

## Overview (KR)

이 문서는 로컬 K3s/k3d 기반의 Kubernetes 인프라를 2026-05-09 공식 지원 스냅샷 기준의 AWS 클라우드 환경으로 이식하기 위한 제품 요구사항을 정의한다. 이를 통해 시스템의 확장성, 가용성, 보안성을 강화하고 관리형 서비스를 통해 운영 부담을 최소화하는 것을 목표로 한다.

## Vision

- **고가용성 확보**: 로컬 단일 노드의 한계를 극복하고 AWS Multi-AZ 기반의 무중단 인프라 구축.
- **운영 자동화**: Karpenter 및 Managed Services를 활용하여 인프라 프로비저닝 및 확장 자동화.
- **클라우드 네이티브 현대화**: 2026년 기준 최신 AWS 보안 및 네트워크 기술(EKS Pod Identity, VPC Lattice) 적용.

## Problem Statement

- **현재 로컬 환경(K3s/k3d)**: 자원 제약으로 인한 확장성 한계 및 하드웨어 장애 시 단일 장애점(SPOF) 존재.
- **운영 부하**: DB, Redis, Vault 등을 직접 관리해야 하므로 가용성 확보 및 백업 관리에 많은 노력이 소요됨.
- **네트워크 가시성 부족**: 서비스 간 연결 관리 및 보안 정책 적용이 복잡하고 수동적임.

## Personas

- **Platform Engineer**: 클라우드 인프라를 효율적으로 구축/관리하고 운영 자동화를 달성하고자 함.
- **Application Developer**: 인프라 복잡성 없이 안정적인 환경에서 애플리케이션을 배포하고 Managed Service의 혜택을 누리고자 함.

## Key Use Cases

- **STORY-01**: 개발자는 RDS(PostgreSQL) 및 ElastiCache(Redis)를 수동 설정 없이 고가용성으로 즉각 활용한다.
- **STORY-02**: 운영자는 Karpenter를 통해 부하에 따라 워커 노드가 초 단위로 자동 확장 및 축소되어 비용과 성능을 최적화한다.
- **STORY-03**: 시스템은 AWS Secrets Manager와 ESO 통합을 통해 시크릿을 안전하게 관리하고 애플리케이션에 주입한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: EKS 클러스터는 Multi-AZ 구조로 구축되어 단일 가용 영역 장애에도 서비스를 유지해야 한다.
- **REQ-PRD-FUN-02**: 모든 데이터 저장 서비스(DB, Cache)는 AWS Managed Service로 대체되어 자동 백업 및 패치를 지원해야 한다.
- **REQ-PRD-FUN-03**: 인프라는 Terraform(IaC)으로 정의되어 코드 기반으로 재현 및 관리 가능해야 한다.

## Success Criteria

- **REQ-PRD-MET-01**: 인프라 구축 후 가용성 99.9% 이상 달성 (Service Level Objective).
- **REQ-PRD-MET-02**: 수동 노드 관리 제로화 (Karpenter에 의한 100% 자동 스케일링).
- **REQ-PRD-MET-03**: 마이그레이션 후 핵심 서비스의 응답 지연 시간이 로컬 대비 일정 수준 이하로 유지되거나 개선됨.

## Scope and Non-goals

- **In Scope**:
  - AWS VPC, EKS 클러스터 설계 및 구축.
  - RDS PG, ElastiCache Redis, Secrets Manager 설정.
  - Terraform 및 Kubernetes Manifest 예시 코드 리포지토리 구축.
- **Out of Scope**:
  - 실제 애플리케이션 코드의 비즈니스 로직 수정 (인프라 환경 설정 변경만 포함).
  - 온프레미스 장비와의 하이브리드 연결 (Direct Connect 등 제외).
- **Non-goals**:
  - 멀티 클라우드(Azure, GCP 등) 동시 지원 (AWS 단일 타겟 최적화).

## Risks, Dependencies, and Assumptions

- **의존성**: AWS 계정 및 적절한 IAM 권한이 사전 확보되어야 함.
- **가정**: 2026-05-09 기준 EKS 1.35 target과 standard support set이 사용 가능함.
- **리스크**: 클라우드 비용 발생에 따른 예산 관리 필요 (FinOps 측면 고려).

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-aws-cloud-native-architecture.md](../02.architecture/requirements/0001-aws-cloud-native-architecture.md)
- **ADR**: [../02.architecture/decisions/0001-aws-managed-services-selection.md](../02.architecture/decisions/0001-aws-managed-services-selection.md)
- **Plan**: [../04.execution/plans/2026-03-31-aws-migration-roadmap.md](../04.execution/plans/2026-03-31-aws-migration-roadmap.md)
