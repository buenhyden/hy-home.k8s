# Azure Migration Technical Specification

## Azure Migration Specification

## Overview (KR)

이 문서는 Azure 마이그레이션을 위한 기술 설계와 리소스 구현 명세를 정의한다. Bicep으로 구현될 인프라의 상세 파라미터, 네트워크 대역, SKU 및 구성 계약을 포함한다.

## Strategic Boundaries & Non-goals

- **Owns**: VNet 설계, AKS 노드 풀 구성, AGC 서브넷 및 게이트웨이 리소스, Key Vault 정책.
- **Does Not Own**: 도메인 등록(DNS), 애플리케이션 소스 코드 단위의 최적화.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-31-azure-migration-prd.md](../../01.prd/2026-03-31-azure-migration-prd.md)
- **ARD**: [../../02.ard/2026-03-31-azure-migration-ard.md](../../02.ard/2026-03-31-azure-migration-ard.md)
- **Related ADRs**: [../../03.adr/2026-03-31-adr-agc-selection.md](../../03.adr/2026-03-31-adr-agc-selection.md)

## Contracts

- **Config Contract**: 모든 리소스 이름은 `hyhome-{env}-{resource}` 규칙을 따른다. (예: `hyhome-prod-aks`).
- **Data / Interface Contract**: API 노출은 Gateway API(AGC)의 `HTTPRoute`를 통해서만 허용된다.
- **Governance Contract**: 모든 리소스에는 `Project: hy-home`, `Environment: Production` 태그가 필수 적용된다.

## Core Design

### 1. Networking (VNet)

- **Address Space**: `10.200.0.0/16`
- **Subnets**:
  - `aks-subnet`: `10.200.0.0/22` (Nodes & Pods via CNI Overlay)
  - `agc-subnet`: `10.200.4.0/24` (Dedicated for AGC)
  - `db-subnet`: `10.200.5.0/24` (PostgreSQL Private Link)

### 2. Compute (AKS)

- **SKU**: Standard Tier (Uptime SLA 지원)
- **Node Pool**:
  - `systempool`: Linux, DS2_v2, 2 nodes (System only)
  - `userpool`: Linux, DS3_v2, 3+ nodes (Autoscaling: 3-10)
- **Network Policy**: Azure Network Policy.
- **Identity**: Azure AD Workload Identity Enabled.

### 3. Data Services

- **PostgreSQL**: Flexible Server, GP_Standard_D2s_v3, 32GB Storage, High Availability(Zone-redundant).
- **Redis**: Premium Tier P1 (6GB), No Clustering (Primary/Replica)

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 기존 로컬 DB 스키마를 유지하되, Azure PostgreSQL의 UTF-8 한글 환경 최적화 적용.
- **Migration / Transition Plan**: `pg_dump` 후 Azure VM(Jumpbox)에서 `psql`로 복원하거나, Azure Database Migration Service 활용 고려.

## Verification

Bicep 배포 전 Preflight 체크 및 배포 후 리소스 상태 확인 명령:

```bash
# Bicep Lint & Preview
az deployment group what-if --resource-group rg-hyhome --template-file infrastructure/main.bicep

# AKS Node Status Check
kubectl get nodes -o wide

# AGC Controller Status
kubectl get pods -n azure-alb-system
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Bicep 배포가 오류 없이 완료되고 모든 리소스가 `Succeeded` 상태임.
- **VAL-SPC-002**: `HTTPRoute` 생성 시 AGC에서 Public IP가 할당되고 외부 접속이 가능함.
- **VAL-SPC-003**: Workload Identity를 통해 Pod가 Key Vault 시크릿을 성공적으로 읽어옴.

## Related Documents

- **Plan**: [../../05.plans/2026-03-31-migration-strategy.md](../../05.plans/2026-03-31-migration-strategy.md)
- **Tasks**: [../../06.tasks/2026-03-31-migration-tasks.md](../../06.tasks/2026-03-31-migration-tasks.md)
- **Runbook**: [../../09.runbooks/2026-03-31-fault-tolerance-runbook.md](../../09.runbooks/2026-03-31-fault-tolerance-runbook.md)
