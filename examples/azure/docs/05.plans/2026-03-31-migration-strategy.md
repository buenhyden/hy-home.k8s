# Azure Migration Strategy Plan

## Overview (KR)

본 문서는 로컬 k3s 환경을 2026년 3월 기준 Azure(AKS) 환경으로 이전하기 위한 실행 전략 및 상세 일정을 정의한다. 인프라 구축, 플랫폼 구성, 데이터 마이그레이션, 그리고 최종 서비스 전환 단계를 포괄하며, 발생 가능한 리스크에 대한 완화 방안을 수립한다.

## Purpose

로컬 k3s 서비스의 중단 시간을 최소화하고, 클라우드 네이티브 서비스(AGC, Managed Identity 등)로의 안전한 전환을 보장하기 위한 단계별 가이드라인을 제공한다.

## Canonical References

- **PRD**: [../01.prd/2026-03-31-azure-migration.md](../01.prd/2026-03-31-azure-migration.md)
- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
- **ADR**: [../03.adr/README.md](../03.adr/README.md)

## Implementation Phases

### Phase 1: Foundation Setup (W1)
Azure 구독 내 핵심 네트워크 및 보안 인프라를 프로비저닝한다.
- [ ] VNet 및 Subnet (AKS/AGC 전용) 생성.
- [ ] Entra ID Managed Identity 및 Key Vault 인스턴스 생성.
- [ ] Bicep 인프라 코드 배포 검증.

### Phase 2: Compute & Platform Configuration (W2)
AKS 클러스터를 기동하고 플랫폼 서비스를 구성한다.
- [ ] AKS Cluster 및 Node Pool 프로비저닝.
- [ ] AGC(Application Gateway for Containers) 컨트롤러 및 Gateway API 설치.
- [ ] ArgoCD(GitOps) 및 Secret Store CSI 드라이버 연동.

### Phase 3: Data Migration & Application Deployment (W3)
관리형 서비스로 데이터를 이전하고 애플리케이션을 배포한다.
- [ ] Managed PostgreSQL/Redis 인스턴스 생성 및 데이터 동기화.
- [ ] Workload Identity 기반의 애플리케이션 배포 및 검증.

### Phase 4: Traffic Cutover & Validation (W4)
트래픽을 Azure로 전환하고 최종 시스템 안정성을 확인한다.
- [ ] AGC를 통한 실시간 트래픽 처리 검증 (200 OK 확보).
- [ ] DNS 레코드 갱신 및 서비스 완전 이전.

## Requirements and Prerequisites

- **Tools**: Azure CLI, Bicep CLI, kubectl (v1.30+), Helm.
- **Permissions**: Azure Contributor, User Access Administrator (RBAC 용).
- **Network**: GitHub Actions Runner/VPN 등으로 Azure VNet 접근성 확보.

## Risk Management

- **Risk 1: 데이터 정합성 이슈**: 마이그레이션 중 데이터 유실 가능성.
  - *Mitigation*: 이중화 백업 및 사전 모의 복구(Runbook 09) 수행.
- **Risk 2: AGC 라우팅 복잡성**: Gateway API 설정 오류로 인한 접속 불가.
  - *Mitigation*: Spec(04) 기반의 단계적 카나리 배포 전략 수립.

## Rollback Procedure

만약 Phase 4 전환 중 치명적인 오류 발생 시:
1. DNS 레코드를 즉시 기존 로컬 k3s(로드 밸런서)로 복구.
2. Azure 리소스 상태 보존 후 장애 분석 수행.

## Related Documents

- **Tasks**: [../06.tasks/2026-03-31-migration-tasks.md](../06.tasks/2026-03-31-migration-tasks.md)
- **Runbook**: [../09.runbooks/0001-disaster-recovery.md](../09.runbooks/0001-disaster-recovery.md)
