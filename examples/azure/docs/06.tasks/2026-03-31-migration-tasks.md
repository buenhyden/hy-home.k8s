# Azure Migration Execution Tasks

## Overview (KR)

본 문서는 로컬 k3s 환경을 2026년 3월 기준 Azure(AKS) 환경으로 이전하기 위한 실행 태스크를 정의한다. 실행 계획(05.plans)을 실제 수행 가능한 가장 작은 작업 단위(Task ID: T-*)로 분해하여 관리한다. 각 작업의 수행 여부, 담당자, 상태 및 검증 증적(Evidence)을 기록한다.

## Status Summary

- **Total Tasks**: 12
- **Completed**: 4
- **In Progress**: 2
- **Todo**: 6

## Phase 1: Foundation Setup (Infra)

- **T-001**: Azure VNet 및 Subnet(AKS/AGC 전용) 생성.
  - *Status*: `Completed`
  - *Evidence*: `az network vnet list` 성공.
- **T-002**: Managed Identity(UAMI) 및 Federated Identity Credential(OIDC) 기초 설정.
  - *Status*: `Completed`
  - *Evidence*: Bicep deployment successful (`main.bicep`).
- **T-003**: Azure Key Vault 프로비저닝 및 CSI Driver 접근 권한 부여.
  - *Status*: `Completed`
  - *Evidence*: `az keyvault list` 성공.

## Phase 2: Platform Configuration (K8s)

- **T-101**: AKS Cluster v1.30+ 프로비저닝 및 노드 풀 구성.
  - *Status*: `Completed`
  - *证据*: `kubectl get nodes` Ready 상태 확인.
- **T-102**: AGC(Application Gateway for Containers) Traffic Controller 설치.
  - *Status*: `In Progress`
  - *Task*: Helm chart deployment for ALB Controller.
- **T-103**: Gateway API (v1) 리소스 배포 및 AGC 연동 검증.
  - *Status*: `Todo`

## Phase 3: Data & Apps (App Layer)

- **T-201**: Azure Database for PostgreSQL Flexible Server(HA) 배포.
  - *Status*: `Todo`
- **T-202**: Azure Cache for Redis 전환 설정 및 연결 정보 업데이트.
  - *Status*: `Todo`
- **T-203**: Workload Identity 기반의 애플리케이션 파드 배포 및 Secret CSI 연동 검증.
  - *Status*: `In Progress`

## Phase 4: Final Cutover (Ops)

- **T-301**: AGC 기반의 실시간 트래픽 처리 검증 (L7 Routing).
  - *Status*: `Todo`
- **T-302**: DNS 전환 및 SSL 인증서 갱신 (Key Vault 통합).
  - *Status*: `Todo`
- **T-303**: 기존 로컬 k3s 리소스 정지 및 프로젝트 완료 보고.
  - *Status*: `Todo`

## Verification

### Automated Verification
```bash
# Verify Gateway API resources in cluster
kubectl get gateway,httproute -A
```

### Manual Verification
- `kubectl describe pods`를 통해 `azure-wi` 관련 설정 확인.
- `az monitor metrics list`를 통해 리소스 실시간 지표 확인.

## Related Documents

- **Plan**: [../05.plans/2026-03-31-migration-strategy.md](../05.plans/2026-03-31-migration-strategy.md)
- **Runbook**: [../09.runbooks/0001-disaster-recovery.md](../09.runbooks/0001-disaster-recovery.md)
- **Spec**: [../04.specs/azure-migration/spec.md](../04.specs/azure-migration/spec.md)
