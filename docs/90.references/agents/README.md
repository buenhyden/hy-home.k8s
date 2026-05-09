# 90.references/agents

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## 목적

이 폴더는 저장소 전반에서 재사용되는 Agent 개념 문서와 느리게 변하는 참고 지식을 저장한다.

## Overview

여기에는 특정 기능 하나에 묶이지 않는 Agent 관련 기준 지식만 둔다. 예를 들어 메모리 시스템 개념, 문서 라우팅 기준, 반복적으로 참조하는 Agent 패턴 요약이 여기에 해당한다.

기능 또는 서비스에 종속된 Agent 설계는 이 폴더가 아니라 `docs/04.specs/<feature-id>/agent-design.md`가 정본 위치다.

## Audience

이 README의 주요 독자:

- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Agent 메모리, 컨텍스트, 오케스트레이션에 대한 재사용 가능한 참고 문서
- 여러 기능에서 공통으로 참조하는 Agent 설계 원칙 요약
- 장기 보존 가치가 있는 Agent 운영 개념 정리

### Out of Scope

- 기능별 Agent 상세 설계
- 구현 계획 및 작업 추적 문서
- 거버넌스 정책 원문

## Structure

```text
agents/
├── README.md          # This file
└── <topic>.md         # Durable agent reference documents
```

## How to Work in This Area

1. 새 문서를 만들기 전에 `docs/99.templates/reference.template.md`를 먼저 확인한다.
2. 기능 범위에 묶인 내용이면 `docs/04.specs/<feature-id>/agent-design.md`로 보낸다.
3. 실행 순서나 롤아웃이 핵심이면 `docs/05.plans/`로 보낸다.
4. 새 문서를 추가하면 이 README와 상위 `docs/90.references/README.md`의 구조 설명이 계속 맞는지 확인한다.

## Related References

- [90.references README](../README.md)
- [04.specs README](../../04.specs/README.md)
- [Templates README](../../99.templates/README.md)
