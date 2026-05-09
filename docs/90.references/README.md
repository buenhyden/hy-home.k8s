# 90.references

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

> 느리게 변하는 기준 지식, 외부 공식 버전 스냅샷, Agent 학습 자료를 관리한다.

## Overview

이 경로는 `hy-home.k8s`의 현재 설계 판단을 직접 대체하지 않는 참고 자료를 보관한다. 공식 문서 링크, 기술 버전 인벤토리, Agent 관련 개념, 학습 로드맵처럼 여러 stage에서 재사용되는 lookup material을 둔다.

진행 중인 요구사항, 의사결정, 실행 계획, 운영 절차는 각각 `01.prd`부터 `09.runbooks`까지의 canonical stage로 라우팅한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 느리게 변하는 외부 기술 기준과 공식 링크
- repo-backed 버전 인벤토리와 cloud example snapshot
- Agent 관련 참고 개념과 학습 자료
- 다른 stage 문서가 참조하는 glossary/standard/lookup material

### Out of Scope

- 현재 진행 중인 설계 의사결정
- 실행 계획이나 작업 증적
- 운영 절차와 장애 대응 체크리스트
- agent runtime policy의 원본 규칙

## Structure

```text
docs/90.references/
├── agents/                              # Agent 관련 참고 자료
├── learning/                            # 학습 로드맵과 이론 연결 자료
├── tech-stack-version-inventory.md      # repo-backed 버전 기준과 cloud snapshot
└── README.md                            # This file
```

## How to Work in This Area

1. 새 참고 자료가 정책/계약/절차를 정의하는지 확인한다. 그렇다면 `00.agent-governance`, `04.specs`, `08.operations`, `09.runbooks`로 라우팅한다.
2. 버전 기준을 갱신할 때는 실제 manifest/config/example code와 [tech-stack-version-inventory.md](./tech-stack-version-inventory.md)를 같은 변경에서 맞춘다.
3. 외부 공식 기준은 확인일을 명시하고 링크를 남긴다.
4. 새 파일을 만들 경우 [reference template](../99.templates/reference.template.md)을 사용하고 이 README 인덱스를 갱신한다.

## Related References

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Templates README](../99.templates/README.md)
- [Tech Stack Version Inventory](./tech-stack-version-inventory.md)

## 목적

이 폴더는 느리게 변하는 기준 지식과 참고 문서를 저장한다.

## 포함할 내용

- 용어집(Glossary)
- 외부 표준 요약
- 시스템 인벤토리
- 아키텍처 개념 참고
- 공통 FAQ
- Agent 관련 개념 요약

## 포함하지 말아야 할 내용

- 현재 진행 중인 설계 의사결정
- 실행 계획
- 운영 절차

## 관련 폴더

- `00.agent-governance/`: Agent 실행 정책과 거버넌스
- `02.ard/`: 아키텍처 참조 모델
- `99.templates/`: Reference 문서 템플릿
- `agents/`: Agent 관련 참고 자료
- `learning/`: 학습 로드맵과 이론 연결 자료

## 예시

- Agent 관련 참고 자료는 `agents/` 하위에 둔다.
- 학습 로드맵은 `learning/infrastructure-to-theory-roadmap.md`처럼 참고 자료로 둔다.
- 버전 기준은 `tech-stack-version-inventory.md`에서 관리한다.

## Agent 참고 문서 배치 규칙

- 재사용 가능한 Agent 개념, 메모리 전략, 문서화 규칙 요약은 `agents/` 하위에 둔다.
- 특정 기능에 종속된 Agent 설계는 `docs/04.specs/<feature-id>/agent-design.md`에 둔다.
- 실행 계획은 `docs/05.plans/`, 운영 절차는 `docs/07~09/`, 거버넌스 규칙은 `docs/00.agent-governance/`로 분리한다.

## Templates

- `../99.templates/reference.template.md`
