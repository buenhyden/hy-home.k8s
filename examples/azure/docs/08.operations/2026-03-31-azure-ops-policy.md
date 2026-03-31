# Azure Infrastructure Operations Policy

## Overview (KR)

이 문서는 Azure AKS 환경으로 이전된 `hy-home.k8s` 인프라의 운영 정책을 정의한다. 보안 통제, 리소스 관리 기준, 그리고 정책 준수 여부 검증 방법을 규정한다.

## Policy Scope

Azure Subscription 내의 모든 AKS 클러스터, VNet, Managed Databases(PostgreSQL, Redis) 및 Key Vault 리소스의 설정 및 운영 방식을 규제한다.

## Applies To

- **Systems**: AKS, Azure Database for PostgreSQL, Azure Cache for Redis, Azure Key Vault.
- **Environments**: production, staging (Azure).

## Controls

- **Required**:
  - 모든 리소스는 Bicep(IaC)을 통해 배포되어야 함.
  - AKS Workload Identity를 사용한 패스워드리스 인증 적용 필수.
  - 데이터베이스의 High Availability(Zone-redundancy) 설정 활성화.
- **Allowed**:
  - 개발 목적의 Burstable tier(B-series) SKU 사용 (단, production 제외).
  - 긴급 장애 복구를 위한 수동 스케일 조절 (사후 보고 필수).
- **Disallowed**:
  - 공용 인터넷에 노출된 Private Endpoint 없는 데이터베이스.
  - 루트 사용자에 의한 직접적인 시크릿 접근 (Key Vault RBAC 사용).
  - `0.0.0.0/0` 허용 인바운드 규칙 (AGC 제외).

## Exceptions

- **Emergency Hotfix**: 중대 장애 발생 시 임시 권한(Privileged) 부여 가능, 24시간 이내 원복 및 보고.
- **External Vendor**: 보안 심의 완료 후 특정 IP 대역에 대한 한시적 허용.

## Verification

- **Compliance Check**: `az resource list --tag Project=hy-home` 명령을 통해 태그 누락 리소스 매월 전수 조사.
- **Security Audit**: Microsoft Defender for Cloud의 점수를 90% 이상 유지.

## Review Cadence

- **Quarterly**: 분기별 아키텍처 및 비용 최적화 리뷰.
- **Per Major Update**: AKS 메이저 버전 업데이트 시 영향도 평가.

## Related Documents

- **ARD**: [../02.ard/2026-03-31-azure-migration-ard.md](../02.ard/2026-03-31-azure-migration-ard.md)
- **Runbook**: [../09.runbooks/2026-03-31-fault-tolerance-runbook.md](../09.runbooks/2026-03-31-fault-tolerance-runbook.md)
- **Spec**: [../04.specs/2026-03-31-resource-specs.md](../04.specs/2026-03-31-resource-specs.md)
