# 04.execution/tasks

> Stage 03 sibling `tasks.md`로 이전된 Task의 임시 transition index다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

모든 활성 Task는 관련 `../../03.specs/<id>-<slug>/tasks.md`로 이동했다.
이 경로에는 WORK-105 terminal cutover 전까지 이 README만 남고 새 Task를 작성하지 않는다.

### Collection Readers

이 README의 주요 독자:

- Platform Engineers
- Operators
- QA/Verification Reviewers
- AI Agents

## Scope

### In Scope

- 구현, 테스트, 평가, 문서, 운영 작업 단위
- Parent Spec/Plan 링크와 phase/Task ID 추적
- 검증 기준, 실행 명령, 로그 또는 evidence 위치
- 소유자, 상태, 완료 여부, handoff 메모
- Agent 작업의 prompt, tool, memory, guardrail, eval, observability task

### Out of Scope

- 전체 시스템 설계 설명
- 운영 정책 정의
- 장애 대응 절차
- 근본 원인 분석
- future implementation narrative without executable task evidence

이 내용은 각각 `../../03.specs/`, `../../05.operations/policies/`, `../../05.operations/runbooks/`, `../../05.operations/incidents/`로 분리한다.

## Item Index

```text
04.execution/tasks/
└── README.md
```

## Add and Find

1. `../../03.specs/README.md`에서 관련 work unit을 찾는다.
2. sibling `spec.md`, `plan.md`, `tasks.md`를 함께 검토한다.
3. 이 경로에는 새 Task를 추가하지 않는다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/tasks/`다.

- 활성 Task는 `../../03.specs/<id>-<slug>/tasks.md`로 직접 연결한다.
- Task 내부의 Spec과 Plan 링크는 각각 `spec.md`, `plan.md` sibling 경로를 사용한다.

### 문서 인덱스

활성 Plan과 Task는 관련 `docs/03.specs/<id>-<slug>/`의 `plan.md`와 `tasks.md`에서 함께 찾는다.

## Related Documents

- [Execution README](../README.md)
- [Docs README](../../README.md)
- [03.specs](../../03.specs/README.md)
- [04.execution/plans](../plans/README.md)
- [05.operations/incidents](../../05.operations/incidents/README.md)
- [Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
- [Archive Index](../../98.archive/README.md)
