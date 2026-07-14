# Azure Infrastructure (Bicep)

> 이 경로는 Bicep을 이용한 Azure 리소스 프로비저닝 코드를 관리한다.

## Overview

본 디렉토리는 Azure Kubernetes Service (AKS), Application Gateway for Containers (AGC), Azure Database for PostgreSQL, Azure Cache for Redis 등 하드 인프라를 정의하고 배포하는 Bicep 템플릿을 포함한다. 2026년 표준인 Azure CNI Overlay 및 Workload Identity 설정을 코드로 구현한다.

### Audience

이 README의 주요 독자:

- DevOps Engineers
- Cloud Platform Team
- AI Agents

### Scope

#### In Scope

- Bicep 기반 인프라 정의 파일 (main, agc 등)
- 리전, 노드 수, 티어 등 인프라 파라미터 관리
- 시스템 할당 및 사용자 할당 관리 ID 설정
- 가상 네트워크(VNet) 및 서브넷(Delegation 포함) 정의

#### Out of Scope

- Kubernetes 내부 매니페스트 (kubernetes/ 참조)
- GitOps 설정 (gitops/ 참조)
- 애플리케이션 소스 코드

## Structure

```text
infrastructure/
├── main.bicep      # 전체 리소스 오케스트레이션 및 AKS 정의
├── agc.bicep       # Application Gateway for Containers 정의
└── README.md       # 본 문서
```

## Configuration Boundary

Inject deployment parameters rather than hardcoding provider state,
credentials, or secret values. This dated Bicep example is repository-static
reference material; an approved Azure subscription and operator-owned runtime
are required for any deployment or what-if evidence.

## Validation

Run `az bicep lint` and the documented
`az deployment group what-if --resource-group <rg-name> --template-file main.bicep`
only in an approved provider context. Static documentation validation does not
prove Azure deployment readiness.

## Operations

### Working Procedure

1. [main.bicep](main.bicep)을 통해 전체 리소스 관계를 파악한다.
2. 배포 전 `az bicep lint` 명령어로 코드 무결성을 검증한다.
3. 리소스 생성 시 [Azure dated snapshot](../../../docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md#definitions--facts)에 보존된 명세와 현재 공식 자료를 함께 검토한다.
4. 배포 전 검토 명령어 예시:

   ```bash
   az deployment group what-if --resource-group <rg-name> --template-file main.bicep
   ```

### Link Basis

이 README의 링크 기준 위치는 `examples/azure/infrastructure/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

### Reference Links

- **Spec snapshot**: [Azure retained specification](../../../docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md#definitions--facts)
- **ADR snapshot**: [Azure retained decisions](../../../docs/90.references/cloud-examples/azure/2026-07-12-azure-example-snapshot.md#definitions--facts)
- **GitOps**: [../gitops/README.md](../gitops/README.md)

### AI Agent Guidance

1. 리소스 정의 변경 시 반드시 관련 ADR 및 Spec과 일치하는지 확인한다.
2. 모듈화된 배포 구조를 선호하며, 상호 의존성을 명확히 관리한다.
3. 배포 파라미터는 하드코딩하지 않고 변수나 파라미터를 통해 주입받도록 구성한다.

## Related Documents

- [Azure executable example entrypoint](../README.md)
- [Azure provider snapshot handoff](../../../docs/90.references/cloud-examples/azure/README.md)
