# 02.architecture

## Overview

`02.architecture/`는 요구사항을 시스템 구조와 의사결정으로 연결하는 아키텍처 허브다.
아키텍처 요구사항은 `requirements/`에, 결정 기록은 `decisions/`에 둔다.

## Audience

- Platform Engineers
- GitOps Operators
- Architecture Reviewers
- AI Agents

## Scope

### In Scope

- 시스템 경계, 품질 속성, 배포 구조, 데이터/인프라 관점의 요구사항
- 선택지, 결정 근거, 결과를 남기는 Architecture Decision Record
- PRD, Spec, Plan, Operations 문서로 이어지는 추적 링크

### Out of Scope

- 제품 요구사항 원문
- 파일 단위 구현 명세
- 실행 순서와 작업 증적
- 반복 운영 절차

## Structure

```text
02.architecture/
├── requirements/  # Architecture requirements and reference models
├── decisions/     # Architecture decision records
└── README.md
```

## How to Work in This Area

1. 요구사항을 시스템 경계와 품질 속성으로 확장할 때는 `requirements/`를 갱신한다.
2. 기술 선택이나 운영 모델 결정은 `decisions/`에 ADR로 기록한다.
3. 구현자가 따라야 할 상세 계약은 `../03.specs/`로 넘긴다.
4. 운영 정책이나 복구 절차는 `../05.operations/`로 넘긴다.

## Related References

- [Requirements README](../01.requirements/README.md)
- [Architecture Requirements](./requirements/README.md)
- [Architecture Decisions](./decisions/README.md)
- [Specs README](../03.specs/README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
