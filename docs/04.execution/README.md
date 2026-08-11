# 04.execution

> Stage 03 co-location cutover 동안 이전 execution route를 설명하는 임시 navigation stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

활성 Plan과 Task는 각 `../03.specs/<id>-<slug>/`의 `plan.md`와 `tasks.md`에
Spec과 함께 위치한다. `04.execution/`에는 WORK-105 terminal cutover 전까지
경로 전환을 설명하는 README 세 개만 남으며 새 실행 문서를 작성하지 않는다.

### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- QA Engineers
- Project Maintainers
- AI Agents

## Stage Contract

### In Scope

- Stage 03 sibling Plan/Task로 향하는 전환 안내
- terminal taxonomy 활성화 전의 호환성 경계

### Out of Scope

- 새 Plan/Task 작성 또는 실행 증거 소유
- 요구사항, 아키텍처, Spec, 운영 문서의 정본
- live cluster mutation, direct ArgoCD action, secret write 절차

이 내용은 각각 `01.requirements/`, `02.architecture/`, `03.specs/`, `05.operations/`로 분리한다.

## Document Index

```text
04.execution/
├── plans/   # transition README only
├── tasks/   # transition README only
└── README.md
```

## Authoring Workflow

1. 활성 작업 단위는 `../03.specs/<id>-<slug>/`에서 찾는다.
2. Spec, Plan, Task 링크는 sibling 파일명을 사용한다.
3. 이 경로에는 새 문서나 실행 증거를 추가하지 않는다.
4. WORK-105 terminal cutover가 완료되면 이 전환 README도 제거한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/`다.

- 상위 docs stage는 `../`로 시작하는 상대 경로를 사용한다.
- 하위 전환 README는 `./plans/`, `./tasks/`로 연결한다.
- 활성 Plan과 Task는 최종 Stage 03 sibling 위치로 직접 연결한다.

## Related Documents

- [Specs README](../03.specs/README.md)
- [Plans README](./plans/README.md)
- [Tasks README](./tasks/README.md)
- [Operations README](../05.operations/README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
