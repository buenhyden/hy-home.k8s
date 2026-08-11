# 04.execution/plans

> Stage 03 sibling `plan.md`로 이전된 Plan의 임시 transition index다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

모든 활성 Plan은 관련 `../../03.specs/<id>-<slug>/plan.md`로 이동했다.
이 경로에는 WORK-105 terminal cutover 전까지 이 README만 남고 새 Plan을 작성하지 않는다.

### Collection Readers

이 README의 주요 독자:

- Platform Engineers
- Operators
- Project Maintainers
- AI Agents

## Scope

### In Scope

- 목표, 범위, 단계, 마일스톤
- 위험과 완화 전략
- 검증 게이트, 완료 기준, 롤아웃/롤백 전략
- 하위 Task로 이어지는 실행 단위 참조
- Agent 작업의 offline eval, sandbox/canary, human approval, rollback, prompt/model promotion gate

### Out of Scope

- 요구사항 정본
- 상세 기술 설계 정본
- 실제 작업 증거와 상태 추적의 정본
- 반복 운영 절차와 장애 대응 runbook

이 내용은 각각 `../../01.requirements/`, `../../03.specs/`, `../tasks/`, `../../05.operations/`로 분리한다.

## Item Index

```text
04.execution/plans/
└── README.md
```

## Add and Find

1. `../../03.specs/README.md`에서 관련 work unit을 찾는다.
2. sibling `spec.md`, `plan.md`, `tasks.md`를 함께 검토한다.
3. 이 경로에는 새 Plan을 추가하지 않는다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/plans/`다.

- 활성 Plan은 `../../03.specs/<id>-<slug>/plan.md`로 직접 연결한다.
- Plan 내부의 Spec과 Task 링크는 각각 `spec.md`, `tasks.md` sibling 경로를 사용한다.

### 문서 인덱스

활성 Plan과 Task는 관련 `docs/03.specs/<id>-<slug>/`의 `plan.md`와 `tasks.md`에서 함께 찾는다.

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/tasks](../tasks/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [Plan Template](../../99.templates/templates/sdlc/execution/plan.template.md)
- [Archive Index](../../98.archive/README.md)
