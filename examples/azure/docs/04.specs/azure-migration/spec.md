# Azure Migration Technical Specification (Spec)

## Overview (KR)

본 문서는 k3s/k3d 환경에서 Azure AKS로 인프라를 이전하기 위한 기술 설계 및 구현 명세서다. PRD와 ARD에서 정의된 요구사항을 기술적으로 구체화하며, Bicep을 이용한 리소스 배포 파라미터, Gateway API(v1) 트래픽 라우팅, 그리고 Workload Identity(OIDC) 통합 설정을 기술한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Azure Bicep 구성 (main.bicep, agc.bicep)
  - GitHub Actions/ArgoCD를 위한 Managed Identity 관리 체계
  - AGC(ALB Controller) 및 Gateway API 리소스 정의
  - Managed PostgreSQL/Redis 연결 설정 명세
- **Does Not Own**:
  - 기존 로컬 환경 하드웨어 관리
  - 애플리케이션 소스 코드 레벨의 리팩토링 (인프라 통합 계층에 집중)

## Related Inputs

- **PRD**: [../../01.prd/2026-03-31-azure-migration.md](../../01.prd/2026-03-31-azure-migration.md)
- **ARD**: [../../02.ard/0001-azure-migration-architecture.md](../../02.ard/0001-azure-migration-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0001-cni-overlay.md](../../03.adr/0001-cni-overlay.md)
  - [../../03.adr/0002-agc-gateway-api.md](../../03.adr/0002-agc-gateway-api.md)
  - [../../03.adr/0003-workload-identity.md](../../03.adr/0003-workload-identity.md)

## Contracts

- **Config Contract**: Bicep parameter 기반의 환경 변수 관리 (Regional/Teiring).
- **Data / Interface Contract**:
  - Identity: Federated Credential (Issuer: AKS OIDC URL, Subject: system:serviceaccount:namespace:sa).
  - Networking: Gateway API (Classic-Ingress 대신 Gateway/HTTPRoute 사용).
- **Governance Contract**: 모든 리소스는 `Project: hy-home-k8s`, `Env: prod` 태그 준수.

## Core Design

- **Component Boundary**:
  - Foundation: Azure VNet (Private Subnets for AKS/AGC).
  - Compute: Managed clusters (AKS) with System/User Node Pools.
  - Traffic: Application Gateway for Containers (v2).
  - Persistence: Azure DB for PostgreSQL Flexible Server, Azure Cache for Redis.
- **Tech Stack**:
  - IaC: Bicep
  - Runtime: AKS (Kubernetes 1.30+)
  - Auth: OIDC / Workload Identity
  - L7 ALB: Application Gateway for Containers (AGC)

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: Bicep 모듈화를 통해 네트워크, 컴퓨팅, 영속성 계층을 분리하여 확장성 확보.
- **Transition Plan**: 05.plans의 실행 계획을 따르며, 초기 클러스터 프로비저닝 후 플랫폼 구성을 선행한다.

## Verification

### Automated Verification
```bash
# Bicep lint validation
az bicep lint --file examples/azure/infrastructure/main.bicep

# Kube-linter for manifests
kube-linter lint examples/azure/kubernetes/
```

### Manual Verification
- `kubectl get gateway`를 통해 AGC Gateway 리소스가 `Programmed: True`인지 확인.
- `az identity federated-credential show` 결과의 `issuer`와 AKS OIDC URL 일치 여부 확인.

## Success Criteria & Verification Plan

- **VAL-SPC-001**: Bicep을 통한 Azure 리소스 생성이 오류 없이 완료됨.
- **VAL-SPC-002**: 외부 도메인을 통해 AGC로 유입된 트래픽이 AKS 파드로 정상 도달함.
- **VAL-SPC-003**: 파드 내부에서 패스워드 없이 Key Vault 시크릿 마운트가 성공함.

## Related Documents

- **Plan**: [../../05.plans/2026-03-31-migration-strategy.md](../../05.plans/2026-03-31-migration-strategy.md)
- **Runbook**: [../../09.runbooks/0001-disaster-recovery.md](../../09.runbooks/0001-disaster-recovery.md)
