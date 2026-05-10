# ADR-0004: PostgreSQL Flexible Server HA

: PostgreSQL High Availability Strategy

## Overview (KR)

로컬의 Patroni/etcd 기반 PostgreSQL HA 구성을 Azure의 관리형 서비스인 **Azure Database for PostgreSQL Flexible Server**로 대체하고, 리전 수준의 가용성을 확보하기 위해 **Zone-redundant HA** 구성을 채택한다.

## Context

- 로컬 환경에서는 Postgres 쓰기/읽기 엔드포인트를 `172.18.0.15:15432/3`으로 직접 노출하고 있었으나, 클라우드 환경에서는 엔터프라이즈급 안정성과 자동 장애 조치(Failover)가 필요함.
- 프로젝트 전체가 **Wordload Identity (Passwordless)** 체계로 전환됨에 따라, DB 인증 역시 Entra ID(Azure AD) 통합이 요구됨.

## Decisions

- **Resource**: `Microsoft.DBforPostgreSQL/flexibleServers` (v16 기준).
- **High Availability**: `ZoneRedundant` 모드 활성화.
- **Authentication**: `AzureAD` 전용 인증 및 RBAC 권한 할당.
- **Networking**: `Private Endpoint`를 통한 가상 네트워크 격리.

## Alternatives

- **Azure SQL Database**: 기존 PostgreSQL 호환성 유지 및 마이그레이션 비용 최소화를 위해 배제.
- **Single Server (Legacy)**: 향후 단종 예정이며 HA 구성 제약이 많아 배제.

## Consequences

- **Positive**:
  - 관리 오버헤드(Patching, Backup) 완전 제거.
  - 리전 가용성 영역(AZ) 장애 시 자동 장애 조치 보장.
  - 패스워드 없는 보안 인증 달성.
- **Negative / Trade-offs**:
  - 로컬 환경 대비 클라우드 비용 발생 (HA 구성 시 인스턴스 비용 2배).
  - 지연 시간(Latency) 감소를 위한 동일 리전/영역 배치 최적화 필요.

## Verification

- `az postgres flexible-server show` 명령어로 `highAvailability.mode`가 `ZoneRedundant`인지 확인.
- `kubectl` 내에서 `psql` 클라이언트를 통해 Entra ID 토큰으로 로그인 성공 여부 검증.

## Related Documents

- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Bicep**: [../infrastructure/database.bicep](../../infrastructure/database.bicep)
