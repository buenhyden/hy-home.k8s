# Azure Migration Technical Specification

## Overview (KR)

로컬 k3s 환경을 Azure(AKS)로 이전하기 위한 엔지니어링 세부 규격을 정의한다. 본 명세는 Bicep 코드 구현 및 Kubernetes 매니페스트 작성의 기준이 되며, 2026-05-09 공식 지원 스냅샷 기준 Azure 기술 표준을 준수한다.

## System Specification

### 1. Compute (AKS)

- **Version**: AKS 1.35 target.
- **Node Pool**:
  - System Pool: `Standard_D2s_v3` (Min 2 nodes).
  - OS: Azure Linux (CBL-Mariner).
- **Network Plugin**: Azure CNI Overlay.

### 2. Networking (AGC)

- **Ingress Controller**: Application Gateway for Containers (ALB Controller).
- **API Standard**: Kubernetes Gateway API (v1).
- **Security**:
  - Subnet delegation to `Microsoft.ServiceNetworking/trafficControllers`.
  - TLS 1.2+ mandatory for all listeners.

### 3. Identity & Authentication

- **Mechanism**: Entra ID Workload Identity (OIDC Federation).
- **Policy**: Passwordless authentication for DB and Key Vault.
- **Role Assignment**: RBAC-based access control (Least Privilege).

### 4. Persistence & Cache

- **Database**: Azure Database for PostgreSQL Flexible Server.
  - Sizing: `Burstable B1ms` (for example) / `General Purpose` (for prod).
  - Storage: 32GB LRS.
- **Cache**: Azure Cache for Redis (Premium).
  - Version: v6.0+.
  - Connectivity: Private Endpoint only.

## Technical Standards (2026-03)

- **VAL-SPEC-001**: 모든 외부 도메인은 AGC의 Frontend IP를 경유해야 한다.
- **VAL-SPEC-002**: 모든 시크릿은 Key Vault에 보관하며, Pod 내에서는 CSI Driver를 통해 파일로만 마운트한다.
- **VAL-SPEC-003**: 인프라 배포는 `main.bicep` 모듈화를 통해 재사용성을 확보한다.

## Resource Mapping Table

| Local Component | Azure Replacement | Standard Note |
| :--- | :--- | :--- |
| MetalLB | Azure Public IP + AGC | Layer 4/7 Isolation |
| Ingress-Nginx | AGC Gateway API | Native Cloud Ingress |
| Vault | Azure Key Vault | Entra ID Integrated |
| PostgreSQL | PG Flexible Server | Zone-Redundant HA |
| Valkey | Azure Cache for Redis | Managed Redundancy |

## Related Documents

- **PRD**: [../../01.prd/2026-03-31-azure-migration.md](../../01.prd/2026-03-31-azure-migration.md)
- **ARD**: [../../02.ard/0001-azure-migration-architecture.md](../../02.ard/0001-azure-migration-architecture.md)
- **ADR**: [../../03.adr/README.md](../../03.adr/README.md)
