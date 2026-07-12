# 03.specs (Technical Specification)

> 이 경로는 Azure 마이그레이션 프로젝트의 상세 기술 설계 및 인터페이스 명세를 관리한다.

## Overview

본 디렉토리는 PRD와 ARD에서 정의된 요구사항 및 아키텍처 모델을 기술적으로 구체화한 "상세 명세서(Spec)"를 보관한다. Bicep 인프라 파라미터, Kubernetes 리소스 규격, 인증 연동 방식(Workload Identity), 그리고 Gateway API 설정 등의 기술적 구현 세부 정보를 포함한다.

### Audience

이 README의 주요 독자:

- Implementation Engineers
- DevOps Specialists
- AI Agents

### Scope

#### In Scope

- Azure Bicep 인프라 모듈 사양 및 연동 파라미터
- Kubernetes Gateway API 및 HTTPRoute 리소스 규격
- Azure Workload Identity / Federated Credential 상세 설정
- Managed Database 및 Redis 서비스 연동 인터페이스 명세
- 테스트 및 검증(Verification) 시나리오

#### Out of Scope

- 거시적 아키텍처 참조 모델 (02.architecture/requirements 참조)
- 기술 선택의 역사적 배경 및 대안 (02.architecture/decisions 참조)
- 마이그레이션 전략 및 일정 (04.execution/plans 참조)

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 Azure 마이그레이션 예시다. 기반 마이그레이션 기록은 2026-03-31 기준이고, 2026-05-09 지원 상태 언급은 해당 날짜의 주석으로만 유지하며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
03.specs/
├── azure-migration/             # Azure 마이그레이션 상세 기술 명세
│   └── spec.md
└── README.md                    # 본 문서
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/azure`로의 후속 통합을 소유한다. Azure 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/azure/`에 둔다.

1. 새로운 기술 기능 또는 시스템 연동 설계 시 [spec.template.md](../../../../docs/99.templates/templates/sdlc/specs/spec.template.md) 템플릿을 사용하여 새 문서를 생성한다.
2. 모든 문서는 01~03번 산출물의 고유 아이디를 참조하여 추적성을 유지한다.
3. [azure-migration/spec.md](azure-migration/spec.md)는 개발 단계에서 구현의 기준점이 된다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live Azure 구독, AKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/azure/docs/03.specs/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../01.requirements/2026-03-31-azure-migration.md)
- **AARD**: [../02.architecture/requirements/0001-azure-migration-architecture.md](../02.architecture/requirements/0001-azure-migration-architecture.md)
- **Task**: [../04.execution/tasks/2026-03-31-migration-tasks.md](../04.execution/tasks/2026-03-31-migration-tasks.md)

### AI Agent Guidance

1. 명세서 작성 시 실제 인프라 리소스 이름과 식별자가 Bicep 소스 코드와 일치하는지 확인한다.
2. 검증(Verification) 섹션에 명시된 명령어가 실제 환경에서 실행 가능한지 검증한다.
3. 아키텍처 문서(ARD) 변경 시 관련 명세서(Spec)의 동기화 여부를 상시 체크한다.
