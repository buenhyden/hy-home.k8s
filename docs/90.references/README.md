# 90.references

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

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

## 권장 하위 구조

- `glossary/`
- `standards/`
- `architecture/`
- `agents/`
- `learning/`

## Agent 참고 문서 배치 규칙

- 재사용 가능한 Agent 개념, 메모리 전략, 문서화 규칙 요약은 `agents/` 하위에 둔다.
- 특정 기능에 종속된 Agent 설계는 `docs/04.specs/<feature-id>/agent-design.md`에 둔다.
- 실행 계획은 `docs/05.plans/`, 운영 절차는 `docs/07~09/`, 거버넌스 규칙은 `docs/00.agent-governance/`로 분리한다.

## Templates

- `../99.templates/reference.template.md`

## 관련 폴더

- `00.agent-governance/`: Agent 실행 정책과 거버넌스
- `02.ard/`: 아키텍처 참조 모델
- `99.templates/`: Reference 문서 템플릿

## 예시

- Agent 관련 참고 자료는 `agents/` 하위에 둔다.
- 학습 로드맵은 `learning/infrastructure-to-theory-roadmap.md`처럼 참고 자료로 둔다.
- 버전 기준은 `tech-stack-version-inventory.md`에서 관리한다.
