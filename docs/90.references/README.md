# 90.references

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

> 느리게 변하는 기준 지식, 외부 공식 스냅샷, 버전 인벤토리, Agent 학습 자료를 관리한다.

## Overview

이 경로는 `hy-home.k8s`의 요구사항, 아키텍처 결정, 구현 계약, 운영 절차를 직접 대체하지 않는 durable reference 영역이다. 공식 문서 링크, 기술 버전 인벤토리, 외부 기준 스냅샷, Agent 관련 개념, 학습 로드맵처럼 여러 stage에서 재사용되는 lookup material을 둔다.

진행 중인 요구사항, 의사결정, 실행 계획, 운영 절차는 각각 `01.requirements`부터 `05.operations/runbooks`까지의 canonical stage로 라우팅한다.

`90.references`는 사실과 기준값을 보존하는 곳이다. 단, 이 폴더의 문서가 실행 명령, 배포 승인, live cluster 변경 절차, agent runtime policy를 새로 정의해서는 안 된다.

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
- 특정 날짜에 확인한 외부 공식 지원 범위와 source checked metadata

### Out of Scope

- 현재 진행 중인 설계 의사결정
- 실행 계획이나 작업 증적
- 운영 절차와 장애 대응 체크리스트
- agent runtime policy의 원본 규칙
- live cluster mutation, Vault writes, deployment approval, release gate 자체

## Structure

```text
docs/90.references/
├── agents/                              # Agent 관련 참고 자료
├── learning/                            # 학습 로드맵과 이론 연결 자료
├── tech-stack-version-inventory.md      # repo-backed 버전 기준과 cloud snapshot
└── README.md                            # This file
```

## How to Work in This Area

1. 새 참고 자료가 정책/계약/절차를 정의하는지 확인한다. 그렇다면 `00.agent-governance`, `03.specs`, `05.operations/policies`, `05.operations/runbooks`로 라우팅한다.
2. 버전 기준을 갱신할 때는 실제 manifest/config/example code와 [tech-stack-version-inventory.md](./tech-stack-version-inventory.md)를 같은 변경에서 맞춘다.
3. 외부 공식 기준은 확인일을 명시하고 링크를 남긴다.
4. 새 파일을 만들 경우 [reference template](../99.templates/reference.template.md)을 사용하고 이 README 인덱스를 갱신한다.
5. 모든 reference 문서는 `Reference Type`, `Authority Boundary`, `Review and Freshness`를 포함해야 한다.

## Role and Authority Boundary

`90.references`의 역할은 다음 네 가지다.

| 역할 | 설명 | 예시 | 소유하지 않는 것 |
| --- | --- | --- | --- |
| Durable concept reference | 여러 stage가 반복 참조하는 느리게 변하는 개념을 설명한다. | glossary, Agent 개념, 학습 로드맵 | 기능별 설계, 실행 계획 |
| Version contract inventory | repo-backed manifest/config와 함께 검증되는 버전 기준을 모은다. | k3s image, Helm chart, GitHub Actions pin | 실제 upgrade 실행 절차 |
| External standard snapshot | 특정 날짜에 확인한 외부 공식 지원 범위를 기록한다. | EKS/AKS 지원 버전, upstream retirement notice | cloud live deployment 지침 |
| Learning/reference roadmap | 구현 경험을 이론 학습 자료와 연결한다. | infrastructure-to-theory roadmap | 운영 runbook, incident response |

권한 경계는 다음과 같다.

- `90.references`는 factual lookup과 dated snapshot의 SSoT다.
- 제품 요구는 `01.requirements`, 아키텍처 요구/결정은 `02.architecture`, 구현 계약은 `03.specs`, 실행 계획/작업 증적은 `04.execution`, 운영 지식은 `05.operations`가 SSoT다.
- `90.references/tech-stack-version-inventory.md`의 버전 값은 실제 repo manifest/config와 함께 유지될 때만 기준값으로 취급한다.
- 외부 기준은 시간에 따라 바뀌므로 `Source checked`, `Last reviewed`, refresh trigger를 남긴다.

## Required Reference Format

새 reference 문서는 [reference.template.md](../99.templates/reference.template.md)의 필수 heading을 유지한다.

- `Purpose`: 이 reference가 존재하는 이유
- `Reference Type`: version-contract-inventory, external-standard-snapshot, durable-concept, learning-roadmap, glossary, faq 중 하나
- `Authority Boundary`: authoritative for / not authoritative for
- `Scope`: 포함/제외 범위
- `Definitions / Facts`: 재사용 가능한 사실, 용어, 기준값
- `Sources`: 공식 또는 repo-backed source
- `Review and Freshness`: 검토 주기, 마지막 검토일, 갱신 trigger
- `Related Documents`: 이 reference를 소비하는 stage 문서

## Related References

- [Docs README](../README.md)
- [Agent Governance Hub](../00.agent-governance/README.md)
- [Templates README](../99.templates/README.md)
- [Tech Stack Version Inventory](./tech-stack-version-inventory.md)

## 목적

이 폴더는 느리게 변하는 기준 지식, dated external snapshot, repo-backed version inventory, 학습 참고 문서를 저장한다.

## 포함할 내용

- 용어집(Glossary)
- 외부 표준 요약
- 시스템 인벤토리
- 아키텍처 개념 참고
- 공통 FAQ
- Agent 관련 개념 요약
- 외부 공식 기준의 확인일이 있는 snapshot

## 포함하지 말아야 할 내용

- 현재 진행 중인 설계 의사결정
- 실행 계획
- 운영 절차
- release approval, incident response, live mutation 절차

## 관련 폴더

- `00.agent-governance/`: Agent 실행 정책과 거버넌스
- `02.architecture/requirements/`: 아키텍처 참조 모델
- `99.templates/`: Reference 문서 템플릿
- `agents/`: Agent 관련 참고 자료
- `learning/`: 학습 로드맵과 이론 연결 자료

## 예시

- Agent 관련 참고 자료는 `agents/` 하위에 둔다.
- 학습 로드맵은 `learning/infrastructure-to-theory-roadmap.md`처럼 참고 자료로 둔다.
- 버전 기준은 `tech-stack-version-inventory.md`에서 관리한다.

## Agent 참고 문서 배치 규칙

- 재사용 가능한 Agent 개념, 메모리 전략, 문서화 규칙 요약은 `agents/` 하위에 둔다.
- 특정 기능에 종속된 Agent 설계는 `docs/03.specs/<feature-id>/agent-design.md`에 둔다.
- 실행 계획은 `docs/04.execution/plans/`, 운영 절차는 `docs/05.operations/runbooks/`, 운영 정책은 `docs/05.operations/policies/`, 거버넌스 규칙은 `docs/00.agent-governance/`로 분리한다.

## 문서 인덱스

| 문서 | Reference Type | 역할 | Freshness 기준 |
| --- | --- | --- | --- |
| [tech-stack-version-inventory.md](./tech-stack-version-inventory.md) | version-contract-inventory / external-standard-snapshot | repo-backed 버전 기준과 cloud example snapshot | manifest/config/example version 변경 또는 외부 공식 지원 범위 변경 |
| [learning/infrastructure-to-theory-roadmap.md](./learning/infrastructure-to-theory-roadmap.md) | learning-roadmap | 인프라 구현 경험과 CS/CE 이론 연결 | 학습 자료나 repo 구현 축이 크게 바뀔 때 |
| [agents/README.md](./agents/README.md) | durable-concept index | Agent reference 하위 폴더의 범위와 라우팅 | Agent reference 문서 추가/이동 시 |

## Templates

- `../99.templates/reference.template.md`
