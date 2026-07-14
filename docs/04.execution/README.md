# 04.execution

> 승인된 요구사항과 명세를 실행 계획과 작업 증적으로 변환하는 execution stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`04.execution/`은 승인된 요구사항, 아키텍처 결정, 명세를 실행 순서와 작업 증적으로 변환하는 실행 허브다.
`plans/`는 구현 전에 실행 순서, 위험, 검증 게이트, 롤아웃/롤백 기준을 고정하고, `tasks/`는 구현·검증 작업의 상태와 evidence를 보존한다.

### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- QA Engineers
- Release Coordinators
- AI Agents

## Stage Contract

### In Scope

- 실행 순서, dependency, risk, verification gate, rollout/rollback boundary
- 구현, 테스트, 평가, 문서, 운영 작업 단위와 상태
- PRD/ARD/ADR/Spec과 운영 문서를 잇는 traceability
- 문서-only 작업의 검증 evidence와 handoff 기록

### Out of Scope

- 요구사항 원문과 acceptance criteria 정본
- 아키텍처 결정 근거와 상세 기술 설계 정본
- 장기 운영 정책과 반복 복구 절차
- live cluster mutation, direct ArgoCD action, secret write 절차

이 내용은 각각 `01.requirements/`, `02.architecture/`, `03.specs/`, `05.operations/`로 분리한다.

## Document Index

```text
04.execution/
├── plans/   # Execution order, risk control, gates, rollout and rollback plans
├── tasks/   # Implementation, verification, status, and evidence records
└── README.md
```

## Authoring Workflow

1. 실행 순서와 검증 기준은 먼저 `plans/`에 정리한다.
2. 실행 가능한 작업 단위, 상태, evidence는 `tasks/`에 기록한다.
3. 새 Plan은 `../99.templates/templates/sdlc/execution/plan.template.md`, 새 Task는 `../99.templates/templates/sdlc/execution/task.template.md`에서 시작한다.
4. 문서만 갱신하더라도 관련 stage README와 upstream/downstream 링크를 같은 변경에서 맞춘다.
5. live mutation이 필요한 절차는 실행 지시로 남기지 않고 human approval 조건과 GitOps 경계를 명시한다.
6. 완료를 주장하기 전에 repo-backed validation과 남은 제한 사항을 Task evidence에 남긴다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/04.execution/`다.

- 상위 docs stage는 `../`로 시작하는 상대 경로를 사용한다.
- 하위 실행 폴더는 `./plans/`, `./tasks/`로 연결한다.
- Plan에서 Task를 연결할 때는 `../tasks/`가 아니라 authored file 위치 기준 상대 경로를 다시 계산한다.

## Related Documents

- [Specs README](../03.specs/README.md)
- [Plans README](./plans/README.md)
- [Tasks README](./tasks/README.md)
- [Operations README](../05.operations/README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
