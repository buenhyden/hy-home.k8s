# 04.execution

## Overview

`04.execution/`은 승인된 요구사항과 명세를 실행 순서와 작업 증적으로 변환하는 실행 허브다.
계획은 `plans/`에, 실제 작업 단위와 검증 증적은 `tasks/`에 둔다.

## Audience

- Platform Engineers
- QA Engineers
- Release Coordinators
- AI Agents

## Scope

### In Scope

- 실행 순서, risk, dependency, verification gate
- 작업 단위, 담당 영역, 상태, evidence
- PRD/ARD/ADR/Spec과 운영 문서를 잇는 traceability

### Out of Scope

- 요구사항 원문
- 아키텍처 결정 근거
- 장기 운영 정책
- 반복 복구 절차

## Structure

```text
04.execution/
├── plans/   # Execution, rollout, and migration plans
├── tasks/   # Implementation and validation task lists
└── README.md
```

## How to Work in This Area

1. 변경 순서와 검증 기준은 먼저 `plans/`에 정리한다.
2. 실행 가능한 작업 단위와 evidence는 `tasks/`에 기록한다.
3. 문서만 갱신하더라도 관련 stage README와 링크를 같은 변경에서 맞춘다.
4. live mutation이 필요한 절차는 문서에 직접 실행 지시로 남기지 않고 승인 조건과 GitOps 경계를 명시한다.

## Related References

- [Specs README](../03.specs/README.md)
- [Plans README](./plans/README.md)
- [Tasks README](./tasks/README.md)
- [Operations README](../05.operations/README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
