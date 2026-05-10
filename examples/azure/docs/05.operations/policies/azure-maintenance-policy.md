# Azure Maintenance & Operations Policy

## Overview (KR)

로컬 k3s에서 Azure(AKS)로 이전된 인프라의 장기적인 안정성과 가용성을 유지하기 위한 운영 및 점검 정책을 정의한다. 본 운영 가이드는 2026-05-09 공식 지원 스냅샷 기준 Azure 패치 관리 및 보안 준수를 기준으로 작성되었다.

## Maintenance Windows

- **Regular Maintenance**: 매월 세 번째 일요일 02:00 ~ 05:00 (KST).
- **Critical Security Patching**: 취약점 발견 시 즉시 수행 (Rolling Update 방식).

## Operational Standards

### 1. AKS Node Autoupgrade

- **Policy**: `NodeImage` 채택 및 최신 보안 패치 자동 적용.
- **Cycle**: 주간 단위 최신 이미지 체크.

### 2. Database Backup & Retention

- **Service**: Azure Database for PostgreSQL Flexible Server Backup.
- **Retention**: 7일간 기본 보관 (Point-in-time Restore 지원).
- **Redundancy**: 리전 장애 대비 고가용성(HA) 구성 상시 유지.

### 3. Monitoring & Alerting

- **Platform**: Azure Monitor (Metrics) & Log Analytics.
- **Critical Alerts**:
  - CPU/Memory Usage > 85% (Critical)
  - AGC Backend 5xx Error Rate > 1% (High)
  - Key Vault Access Denied Rate > 5% (Security)

## Change Management

1. 모든 변경사항은 Bicep IaC 및 ArgoCD GitOps를 통해 수행한다.
2. 매니페스트 변경 전 `infrastructure/tests` 하위의 정적 분석 및 컨텍스트 검증을 통과해야 한다.
3. 중대 변경 시 PR(Pull Request) 내에 ADR(Architecture Decision Record) 작성을 권장한다.

## KPIs (Success Metrics)

- **Availability**: 월간 가동률 99.9% 이상.
- **Response Time**: AGC 평균 지연 시간(Latency) 100ms 이내.
- **Compliance**: 보안 취약점 0건 유지 (Critical 기준).

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **ARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Runbook**: [../05.operations/runbooks/0001-disaster-recovery.md](../runbooks/0001-disaster-recovery.md)
