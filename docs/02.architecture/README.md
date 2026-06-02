# 02.architecture

> 요구사항을 아키텍처 요구와 결정 기록으로 연결하는 canonical architecture stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

`02.architecture/`는 요구사항을 시스템 구조와 의사결정으로 연결하는 아키텍처 허브다.
아키텍처 요구사항은 `requirements/`에, 결정 기록은 `decisions/`에 둔다.

이 stage는 현재 실행계약을 보존한다. 현재 repo-backed 실행계약은
[`gitops/`](../../gitops/README.md), [`infrastructure/tests/verify-contracts-static.sh`](../../infrastructure/tests/verify-contracts-static.sh),
정적 검증 스크립트가 우선한다. 현재 구현과 상충하는 old decision/requirement 문서는 활성 stage에 보존하지 않고 [`../98.archive/README.md`](../98.archive/README.md)의 Tombstone 인덱스로만 연결한다.

## Reader Route

| 찾는 것 | 먼저 볼 위치 | 판단 기준 |
| --- | --- | --- |
| 현재 외부 서비스, Headlamp, `172.18.x` 계약 | [`gitops/platform/external-services/`](../../gitops/platform/external-services/), [`gitops/platform/network-policies/`](../../gitops/platform/network-policies/), [`verify-contracts-static.sh`](../../infrastructure/tests/verify-contracts-static.sh) | 현재 desired state와 정적 계약 검증이 우선한다. |
| 시스템 경계와 품질 속성 | [`requirements/`](./requirements/README.md) | ARD는 PRD를 아키텍처 요구와 참조 구조로 확장한다. |
| 기술 선택과 현재 decision record | [`decisions/`](./decisions/README.md) | ADR은 현재 구현 기준의 결정, 대안, 결과를 보존한다. |
| 구현자가 따라야 할 계약 | [`../03.specs/`](../03.specs/README.md) | 파일/manifest/API 수준 상세 설계는 Spec stage가 소유한다. |
| 운영 정책과 복구 절차 | [`../05.operations/`](../05.operations/README.md) | 실행 절차, 정책, runbook은 Operations stage가 소유한다. |

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
3. ARD target은 `docs/02.architecture/requirements/####-<system-or-domain>.md`, ADR target은 `docs/02.architecture/decisions/####-<short-title>.md`를 따른다.
4. 현재 구현과 상충하는 old ARD/ADR은 bulk note로 보존하지 않고 중앙 archive Tombstone으로 이동한다.
5. 구현자가 따라야 할 상세 계약은 `../03.specs/`로 넘긴다.
6. 운영 정책이나 복구 절차는 `../05.operations/`로 넘긴다.

## Link Basis

이 README의 링크 기준 위치는 `docs/02.architecture/`다.

- 하위 아키텍처 폴더는 `./requirements/`, `./decisions/`로 연결한다.
- 인접 stage는 `../01.requirements/`, `../03.specs/`, `../05.operations/`로 연결한다.
- root-level 구현 경로는 `../../gitops/`, `../../infrastructure/`처럼 repository root 기준으로 올라간다.
- ARD/ADR 문서 안의 링크는 각 하위 폴더의 최종 문서 위치 기준으로 다시 계산한다.

## Related Documents

- [Requirements README](../01.requirements/README.md)
- [Architecture Requirements](./requirements/README.md)
- [Architecture Decisions](./decisions/README.md)
- [Specs README](../03.specs/README.md)
- [Operations README](../05.operations/README.md)
- [Document Stage Routing](../00.agent-governance/rules/document-stage-routing.md)
- [Templates README](../99.templates/README.md)
- [Archive Index](../98.archive/README.md)
