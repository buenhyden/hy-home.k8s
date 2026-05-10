# ADR-0003: Azure Workload Identity for Passwordless Auth

## Overview (KR)

이 문서는 AKS 기반 애플리케이션의 인증 체계로 Azure Workload Identity를 전격 도입한 기록이다.

## Context

전통적으로 애플리케이션이 클라우드 서비스(DB, Key Vault)를 사용할 때 고정된 비밀번호(Secret)나 수동 관리형 주체(Service Principal)를 사용한다. 이는 보안 위험과 관리 복잡성을 증대시킨다. 2026년 기준, 모든 클라우드 자원 접근은 비밀번호가 없는(Passwordless) 환경이어야 한다.

## Decision

- **Azure Workload Identity**를AKS 클러스터의 표준 인증 플랫폼으로 사용한다.
- 애플리케이션의 Kubernetes Service Account를 Azure Managed Identity(User-assigned)와 Federated Identity Credential로 연동(FedID)한다.
- 모든 SDK와 통신 시 DefaultAzureCredential 라이브러리를 사용하여 로컬/클라우드 통용성을 확보한다.

## Explicit Non-goals

- 레거시 Azure AD Pod Identity 사용.
- 고정된 Client Secret 및 Key를 통한 환경 변수 기반 인증.

## Consequences

- **Positive**:
  - 보안 강화: 하드코딩된 비밀번호 제거, 자동 자격 증명 갱신.
  - 관리 간소화: 개별 워크로드에 고유 소유권을 부여하여 감사가 쉬움.
  - 성능 및 안정성: 오픈 소스 OIDC 표준을 따르므로 Pod Identity보다 빠르고 가벼움.
- **Trade-offs**:
  - 로컬 테스트 시 Azure CLI 로그인 또는 별도 인증 브릿지 구성을 위한 초기 설정 공수.

## Alternatives

### Azure AD Pod Identity (Legacy)

- Good: 전통적인 방식.
- Bad: 성능 이슈, 2024년 이후 점진적으로 지원 중단, 복잡한 NMI/MIC 컴포넌트 필요.

### Manual Key Management (Vault integration only)

- Good: 클라우드 종속성이 낮을 수 있음.
- Bad: Key Vault 접근 자체를 위한 Key 관리가 다시 필요하여 순환 참조 문제 발생.

## Related Documents

- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../requirements/0001-azure-migration-architecture.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
