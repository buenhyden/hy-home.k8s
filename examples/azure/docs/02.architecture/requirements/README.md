# 02.architecture/requirements (Architecture Reference Document)

> 이 경로는 Azure 마이그레이션 프로젝트의 거시적 아키텍처와 참조 모델을 관리한다.

## Overview

본 디렉토리는 k3s 로컬 인프라를 2026-05-09 공식 지원 스냅샷 기준 Azure(AKS) 환경으로 이전할 때 프로젝트 전반의 기술적 근거가 되는 아키텍처 참조 명세서를 관리한다. 시스템의 경계, 책임 소유권, 데이터 아키텍처 및 품질 속성을 정의한다.

### Audience

이 README의 주요 독자:

- Solution Architects
- Network Engineers
- Security Architects
- AI Agents

### Scope

#### In Scope

- Azure 마이그레이션 대상 참조 아키텍처 (AKS, AGC,Managed Storage 등)
- 시스템 간 데이터 흐름(Data Flow) 및 계층 분리 전략
- 2026-05-09 공식 지원 스냅샷 기준 Azure 기술 스택의 품질 속성(Performance, Availability 등) 규정
- 리소스 간 소유권 및 결합도(Cohesion / Coupling) 수준 정의

#### Out of Scope

- 기술적 선택의 개별 사유 및 히스토리 (02.architecture/decisions 참조)
- 상세 구현 파라미터 및 Bicep 소스 코드 (03.specs 참조)
- 마이그레이션 실행 절차와 태스크 (04.execution/plans, 04.execution/tasks 참조)

## Snapshot Contract

이 인덱스는 2026-07-12에 저장소 정적 상태로 관찰한 Azure 마이그레이션 예시다. 기반 마이그레이션 기록은 2026-03-31 기준이고, 2026-05-09 지원 상태 언급은 해당 날짜의 주석으로만 유지하며, 이 경로는 active main-stage 소유권이나 provider-latest 가이드를 대체하지 않는다.

## Report Index

```text
02.architecture/requirements/
├── 0001-azure-migration-architecture.md    # Azure 마이그레이션 핵심 아키텍처
└── README.md                                # 본 문서
```

## Refresh and Succession

Spec 030이 `docs/90.references/cloud-examples/azure`로의 후속 통합을 소유한다. Azure 공식 서비스·API·지원 계약 또는 하위 인벤토리가 바뀔 때 이 예시를 다시 검토하며, 실행 자산은 계속 `examples/azure/`에 둔다.

1. 아키텍처 모델 변경 시 [ard.template.md](../../../../../docs/99.templates/templates/sdlc/architecture/ard.template.md) 템플릿을 사용하여 새 문서를 생성한다.
2. 모든 아키텍처 다이어그램은 Mermaid 형식을 사용하며 코드 블록에 포함한다.
3. [0001-azure-migration-architecture.md](0001-azure-migration-architecture.md)는 프로젝트의 기술적 가이드라인으로 유지한다.

## Evidence Boundary

이 README는 저장소 정적 문서 증거만 제공한다. live Azure 구독, AKS, 자격 증명, 비용, 네트워크, secret 또는 provider-latest 준비 상태를 증명하지 않는다.

이 README의 링크 기준 위치는 `examples/azure/docs/02.architecture/requirements/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **ADR**: [../02.architecture/decisions/README.md](../decisions/README.md)

### AI Agent Guidance

1. 아키텍처 명세 수정 전 반드시 상위 PRD의 요구사항이 반영되었는지 정합성을 체크한다.
2. 시스템 경계(Boundaries) 섹션을 명확히 기술하여 에이전트가 소유권을 잘못 판단하지 않도록 한다.
3. 신규 컴포넌트 추가 시 품질 속성에 미치는 영향(예: 성능 저하 가능성)을 반드시 기술한다.
