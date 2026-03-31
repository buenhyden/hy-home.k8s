# 04.specs (Technical Specification)

> 이 경로는 Azure 마이그레이션 프로젝트의 상세 기술 설계 및 인터페이스 명세를 관리한다.

## Overview

본 디렉토리는 PRD와 ARD에서 정의된 요구사항 및 아키텍처 모델을 기술적으로 구체화한 "상세 명세서(Spec)"를 보관한다. Bicep 인프라 파라미터, Kubernetes 리소스 규격, 인증 연동 방식(Workload Identity), 그리고 Gateway API 설정 등의 기술적 구현 세부 정보를 포함한다.

## Audience

이 README의 주요 독자:

- Implementation Engineers
- DevOps Specialists
- AI Agents

## Scope

### In Scope

- Azure Bicep 인프라 모듈 사양 및 연동 파라미터
- Kubernetes Gateway API 및 HTTPRoute 리소스 규격
- Azure Workload Identity / Federated Credential 상세 설정
- Managed Database 및 Redis 서비스 연동 인터페이스 명세
- 테스트 및 검증(Verification) 시나리오

### Out of Scope

- 거시적 아키텍처 참조 모델 (02.ard 참조)
- 기술 선택의 역사적 배경 및 대안 (03.adr 참조)
- 마이그레이션 전략 및 일정 (05.plans 참조)

## Structure

```text
04.specs/
├── azure-migration/             # Azure 마이그레이션 상세 기술 명세
│   └── spec.md
└── README.md                    # 본 문서
```

## How to Work in This Area

1. 새로운 기술 기능 또는 시스템 연동 설계 시 [spec.template.md](../../../docs/99.templates/spec.template.md) 템플릿을 사용하여 새 문서를 생성한다.
2. 모든 문서는 01~03번 산출물의 고유 아이디를 참조하여 추적성을 유지한다.
3. [azure-migration/spec.md](./azure-migration/spec.md)는 개발 단계에서 구현의 기준점이 된다.

## Related References

- **PRD**: [../01.prd/2026-03-31-azure-migration.md](../01.prd/2026-03-31-azure-migration.md)
- **ARD**: [../02.ard/0001-azure-migration-architecture.md](../02.ard/0001-azure-migration-architecture.md)
- **Task**: [../06.tasks/2026-03-31-migration-tasks.md](../06.tasks/2026-03-31-migration-tasks.md)

## AI Agent Guidance

1. 명세서 작성 시 실제 인프라 리소스 이름과 식별자가 Bicep 소스 코드와 일치하는지 확인한다.
2. 검증(Verification) 섹션에 명시된 명령어가 실제 환경에서 실행 가능한지 검증한다.
3. 아키텍처 문서(ARD) 변경 시 관련 명세서(Spec)의 동기화 여부를 상시 체크한다.
