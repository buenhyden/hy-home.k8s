# 04.execution/tasks (Execution Tasks)

> 이 경로는 Azure 마이그레이션 프로젝트의 개별 작업 진행 상황과 검증 결과를 관리한다.

## Overview

본 디렉토리는 실행 계획(04.execution/plans)을 실제 수행 가능한 가장 작은 작업 단위(Task ID: T-*)로 분해하여 관리한다. 각 작업의 수행 여부, 담당자, 상태 및 검증 증적(Evidence)을 기록하는 "작업 일지" 역할을 한다.

## Audience

이 README의 주요 독자:

- Implementation Engineers
- AI Agents
- Future Auditors

## Scope

### In Scope

- Azure 마이그레이션 개별 작업 추적표 (Task)
- 단계별(Phase 1~4) 작업 분해 및 상태
- 각 작업 수행 후의 검증 증적 (Logs, Screenshots, Commands)
- TDD 기반의 구현 관리

### Out of Scope

- 상위 수준의 이행 로드맵 (04.execution/plans 참조)
- 아키텍처 및 기술 명세 (02.architecture/requirements, 03.specs 참조)
- 실제 Bicep 및 Kubernetes 코드

## Structure

```text
04.execution/tasks/
├── 2026-03-31-migration-tasks.md    # Azure 마이그레이션 작업 추적표
└── README.md                         # 본 문서
```

## How to Work in This Area

1. [2026-03-31-migration-tasks.md](2026-03-31-migration-tasks.md)를 통해 현재 작업 진행 상태를 확인한다.
2. 새 작업 할당 시 [task.template.md](../../../../../docs/99.templates/templates/sdlc/execution/task.template.md) 템플릿을 준수한다.
3. 작업 완료 시 반드시 검증 증적(Evidence) 섹션을 갱신한다.

## Link Basis

이 README의 링크 기준 위치는 `examples/azure/docs/04.execution/tasks/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- **Spec**: [../03.specs/azure-migration/spec.md](../../03.specs/azure-migration/spec.md)
- **Plan**: [../04.execution/plans/2026-03-31-migration-strategy.md](../plans/2026-03-31-migration-strategy.md)
- **Runbook**: [../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)

## AI Agent Guidance

1. 모든 구현 작업은 반드시 Task ID(T-*)와 연결되어야 한다.
2. 작업 수행 전후의 상태 변화를 명확히 기록한다.
3. `Todo`에서 `In Progress`, `Completed`로 상태 전환 시 관련 증적을 누락하지 않는다.
