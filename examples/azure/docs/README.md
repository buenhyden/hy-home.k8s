# Azure Migration Documentation Hub

> K3s 로컬 인프라의 Azure(AKS) 전 이전을 위한 통합 문서 센터

## Overview

이 경로는 `hy-home.k8s` 프로젝트의 로컬 Kubernetes 환경을 Azure 클라우드로 마이그레이션하기 위한 모든 설계, 계획, 작업 및 운영 지식을 관리한다. 2026-05-09 공식 지원 스냅샷 기준의 Azure 클라우드 네이티브 아키텍처를 지향하며, 총 9개의 표준화된 디렉토리 구조를 통해 체계적인 지식 관리를 수행한다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Infrastructure Operations
- Cloud Architects
- AI Agents (Antigravity)

## Scope

### In Scope

- **01.prd**: 제품 요구사항 정의 및 성공 지표
- **02.ard**: 참조 아키텍처 및 품질 속성
- **03.adr**: 주요 기술적 선택 배경 (AGC, Workload Identity 등)
- **04.specs**: 리소스 모델링 및 상세 기술 사양
- **05.plans**: 단계별 마이그레이션 전략 및 로드맵
- **06.tasks**: 상세 구현 태스크 및 검증 로그
- **07.guides**: 배포 가이드 및 온보딩 절차
- **08.operations**: 클라우드 운영 정책 및 거버넌스
- **09.runbooks**: 장애 대응 및 긴급 복구 매뉴얼

### Out of Scope

- 애플리케이션 비즈니스 로직 소스 코드
- AWS 또는 GCP 등 타 클라우드 아키텍처 (별도 경로에서 관리)
- 레거시 하드웨어 폐기 절차

## Structure

```text
examples/azure/docs/
├── 01.prd/           # Product Requirements
├── 02.ard/           # Architecture Reference
├── 03.adr/           # Architecture Decision Records
├── 04.specs/         # Technical Specifications
├── 05.plans/         # Migration Strategies
├── 06.tasks/         # Implementation Tasks
├── 07.guides/        # Deployment Guides
├── 08.operations/    # Ops Policies
├── 09.runbooks/      # Recovery Procedures
└── README.md         # This hub file
```

## Tech Stack (2026-05-09 Snapshot)

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| Platform   | Azure Kubernetes Service (AKS)            | AKS 1.35 target, CNI Overlay |
| Networking | Application Gateway for Containers (AGC)  | Gateway API Standard      |
| Database   | Azure DB for PostgreSQL Flexible Server   | High Availability Enabled |
| Cache      | Azure Cache for Redis                     | Premium Tier              |
| Security   | Azure Key Vault + Workload Identity       | Passwordless Auth         |
| IaC        | Bicep                                     | Resource Module Pattern   |

## How to Work in This Area

1. **Requirement First**: 변경 사항은 항상 [01.prd](./01.prd/README.md)에서 시작하여 하위 문서로 전파한다.
2. **Standard Templates**: 모든 문서는 `docs/99.templates/` 산하의 최신 템플릿을 사용하여 작성한다.
3. **Traceability**: 문서 내 상호 참조는 반드시 상대 경로를 사용하여 링크를 유지한다.
4. **Agent Guidance**: 에이전트는 작업 전 [06.tasks](./06.tasks/README.md)를 확인하고 진행 상황을 업데이트한다.

## Related References

- [Main Project README](../../../README.md)
- [Local Infrastructure Specs](../../../infrastructure/README.md)
- [Governance Rules](../../../docs/00.agent-governance/README.md)
