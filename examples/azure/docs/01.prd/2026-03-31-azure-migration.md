# Azure Migration PRD (Product Requirements Document)

## Overview (KR)

본 문서는 로컬 k3s/k3d 환경의 프로젝트 인프라를 2026년 3월 기준 Azure(AKS) 환경으로 이전하기 위한 제품 요구사항을 정의한다. 기존 로컬 리소스의 제약(가용성, 성능, 관리 오버헤드)을 해결하고, 클라우드 네이티브 관리형 서비스(PostgreSQL, Redis, Key Vault, AGC)를 통해 고가용성과 보안성을 확보하는 것을 최상위 목표로 한다.

## Summary

`hy-home.k8s` 프로젝트는 기존 로컬 하드웨어(k3s) 기반의 운영에서 탈피하여, 글로벌 가용성과 현대적인 보안 거버넌스(Entra ID 통합)가 보장되는 Azure Managed 환경으로 전격 이전한다. 인프라 관리를 위한 최소한의 노력을 지향하며(Serverless/Managed), 모든 인증은 Passwordless(Workload Identity) 체계로 전환한다.

## Boundaries & Use Cases

- **Target Systems**: AKS v1.30+, Azure Database for PostgreSQL Flexible, Azure Cache for Redis, Azure Key Vault, Azure App Gateway for Containers (AGC).
- **Core Use Case**:
  - 로컬 k3s에서 실행되던 모든 워크로드의 AKS 무중단 이전.
  - 외부 트래픽의 AGC 및 Gateway API 기반 라우팅.
  - Azure Key Vault와 Kubernetes Secret Store CSI 드라이버를 통합한 시크릿 관리.

## Requirements

### Functional Requirements (FR)
- **REQ-PRD-001**: AKS 클러스터는 Azure CNI Overlay 및 Workload Identity(OIDC) 기능을 지원해야 한다.
- **REQ-PRD-002**: L7 부하 분산은 Gateway API를 통해 Application Gateway for Containers(AGC)와 연동되어야 한다.
- **REQ-PRD-003**: 모든 데이터베이스(PostgreSQL)는 관리형 Flexible Server를 사용하며, 고가용성(High Availability) 옵션을 유지한다.
- **REQ-PRD-004**: 캐시는 Azure Cache for Redis를 통해 외부화하며, 클러스터링을 지원한다.

### Non-Functional Requirements (NFR)
- **REQ-NFR-101 (Security)**: 모든 서비스 자격 증명은 고정된 Secret 대신 Managed Identity와 Federated Identity Credential(Workload Identity)을 사용한다.
- **REQ-NFR-102 (Availability)**: 핵심 인프라는 2026년 3월 기준 Azure SLA 99.95% 이상을 준수하는 리전 및 티어로 구성한다.
- **REQ-NFR-103 (Manageability)**: 모든 인프라는 Bicep(IaC)을 통해 형상 관리되며, 배포는 ArgoCD(GitOps)를 표준으로 한다.

## Success Criteria

1. Bicep 배포가 정상적으로 완료되고, AKS 클러스터가 Healthy 상태로 기동됨.
2. 외부 도메인을 통한 서비스 접속이 AGC 및 Gateway API를 통해 200 OK로 반환됨.
3. Pod 내부에서 패스워드 없이 Azure Key Vault 및 PostgreSQL에 접근 가능함 (Workload Identity 검증).

## Related Documents

- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **Plan**: [../05.plans/2026-03-31-migration-strategy.md](../05.plans/2026-03-31-migration-strategy.md)
- **ADR**: [../03.adr/0001-cni-overlay.md](../03.adr/0001-cni-overlay.md)
