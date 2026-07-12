# Azure Migration Documentation Hub

> K3s 로컬 인프라의 Azure(AKS) 전 이전을 위한 통합 문서 센터

## Overview

이 경로는 `hy-home.k8s` 프로젝트의 로컬 Kubernetes 환경을 Azure 클라우드로 마이그레이션할 때 참고하는 설계, 계획, 작업 및 운영 지식 예시를 관리한다. 버전 현재성은 [Tech Stack Version Inventory](../../../docs/90.references/data/tech-stack-version-inventory.md)의 `Cloud Example Snapshot`을 기준으로 확인하며, 현재 로컬 플랫폼의 active SSoT나 실제 Azure 배포 절차를 대체하지 않는다.

### Audience

이 README의 주요 독자:

- Platform Engineers
- Infrastructure Operations
- Cloud Architects
- AI Agents

### Scope

#### In Scope

- **01.requirements**: 제품 요구사항 정의 및 성공 지표
- **02.architecture/requirements**: 참조 아키텍처 및 품질 속성
- **02.architecture/decisions**: 주요 기술적 선택 배경 (AGC, Workload Identity 등)
- **03.specs**: 리소스 모델링 및 상세 기술 사양
- **04.execution/plans**: 단계별 마이그레이션 전략 및 로드맵
- **04.execution/tasks**: 상세 구현 태스크 및 검증 로그
- **05.operations/guides**: 배포 가이드 및 온보딩 절차
- **05.operations/policies**: 클라우드 운영 정책 및 거버넌스
- **05.operations/runbooks**: 장애 대응 및 긴급 복구 매뉴얼

#### Out of Scope

- 애플리케이션 비즈니스 로직 소스 코드
- AWS 또는 GCP 등 타 클라우드 아키텍처 (별도 경로에서 관리)
- 레거시 하드웨어 폐기 절차
- 실제 Azure 구독 프로비저닝 또는 live cluster 변경

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 Azure 마이그레이션 예시다. 기반 마이그레이션 기록은 2026-03-31 기준이고, 2026-05-09 지원 상태 언급은 해당 날짜의 주석으로만 유지하며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
examples/azure/docs/
├── 01.requirements/           # Product Requirements
├── 02.architecture/requirements/           # Architecture Reference
├── 02.architecture/decisions/           # Architecture Decision Records
├── 03.specs/         # Technical Specifications
├── 04.execution/plans/         # Migration Strategies
├── 04.execution/tasks/         # Implementation Tasks
├── 05.operations/guides/        # Deployment Guides
├── 05.operations/policies/    # Ops Policies
├── 05.operations/runbooks/      # Recovery Procedures
└── README.md         # This hub file
```

### Tech Stack

이 표의 기준 날짜와 지원 상태는 [Tech Stack Version Inventory](../../../docs/90.references/data/tech-stack-version-inventory.md)의 `Cloud Example Snapshot`을 따른다.

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| Platform   | Azure Kubernetes Service (AKS)            | AKS 1.35 target, CNI Overlay |
| Networking | Application Gateway for Containers (AGC)  | Gateway API Standard      |
| Database   | Azure DB for PostgreSQL Flexible Server   | High Availability Enabled |
| Cache      | Azure Cache for Redis                     | Premium Tier              |
| Security   | Azure Key Vault + Workload Identity       | Passwordless Auth         |
| IaC        | Bicep                                     | Resource Module Pattern   |

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/azure`로의 후속 통합을 소유한다. Azure 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/azure/`에 둔다.

1. **Requirement First**: 변경 사항은 항상 [01.requirements](01.requirements/README.md)에서 시작하여 하위 문서로 전파한다.
2. **Standard Templates**: 모든 문서는 `docs/99.templates/` 산하의 최신 템플릿을 사용하여 작성한다.
3. **Traceability**: 문서 내 상호 참조는 반드시 상대 경로를 사용하여 링크를 유지한다.
4. **Reference Boundary**: 실제 Azure 배포 전에는 provider 공식 지원 버전, 비용, RBAC, 네트워크 경계를 다시 확인한다.
5. **Agent Guidance**: 에이전트는 작업 전 [04.execution/tasks](04.execution/tasks/README.md)를 확인하고 진행 상황을 업데이트한다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live Azure 구독, AKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/azure/docs/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Main Project README](../../../README.md)
- [Local Infrastructure Specs](../../../infrastructure/README.md)
- [Governance Rules](../../../docs/00.agent-governance/README.md)
