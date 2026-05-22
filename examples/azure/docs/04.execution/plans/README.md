# 04.execution/plans (Implementation Plans)

> 이 경로는 Azure 마이그레이션 프로젝트의 단계별 이행 전략인 릴리스 계획을 관리한다.

## Overview

본 디렉토리는 PRD와 Spec에서 정의된 목표를 달성하기 위한 "단계별 실행 로드맵"을 관리한다. 인프라 프로비저닝, 데이터 이관, 트래픽 전환 등의 타임라인과 리스크 완화 전략을 포함하며, 대규모 마이그레이션의 성공을 위한 지침서 역할을 한다.

## Audience

이 README의 주요 독자:

- Project Managers
- Infrastructure Leads
- AI Agents

## Scope

### In Scope

- Azure 마이그레이션 단계별(Phase 1~4) 이행 전략 (Plan)
- 마이그레이션 타임라인 및 주요 마일스톤 정의
- 리스크 분석 및 대응 방안 (Mitigation)
- 서비스 중단 최소화를 위한 롤백 절차 명세

### Out of Scope

- 개별 세부 태스크 레벨의 상태 추적 (04.execution/tasks 참조)
- 아키텍처 상세 설계 및 기술 명세 (02.architecture/requirements, 03.specs 참조)
- 장애 발생 시의 실시간 가이드 (05.operations/runbooks 참조)

## Structure

```text
04.execution/plans/
├── 2026-03-31-migration-strategy.md    # Azure 마이그레이션 이행 전략
└── README.md                            # 본 문서
```

## How to Work in This Area

1. 새로운 프로젝트 마일스톤이나 릴리스 계획 수립 시 [plan.template.md](../../../../../docs/99.templates/plan.template.md) 템플릿을 준수한다.
2. 모든 계획은 PRD와 Spec의 요구사항을 기반으로 수립한다.
3. [2026-03-31-migration-strategy.md](2026-03-31-migration-strategy.md)는 프로젝트 실행의 기준이 된다.

## Link Basis

이 README의 링크 기준 위치는 `examples/azure/docs/04.execution/plans/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **PARD**: [../01.requirements/2026-03-31-azure-migration.md](../../01.requirements/2026-03-31-azure-migration.md)
- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Task**: [../04.execution/tasks/2026-03-31-migration-tasks.md](../tasks/2026-03-31-migration-tasks.md)

## AI Agent Guidance

1. 실행 계획 수정 시 인적/물적 자원의 가용성을 고려하여 현실적인 타임라인을 제안한다.
2. 리스크 예측(Risk Management) 섹션을 강화하여 잠재적 장애 요소를 미연에 방지한다.
3. 계획 문서 내의 모든 날짜 형식은 YYYY-MM-DD를 표준으로 한다.
