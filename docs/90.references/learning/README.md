# 90.references/learning

> [!NOTE]
> All AI agent interactions with this directory must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## 목적

이 폴더는 `hy-home.k8s`의 구현 경험을 CS/CE 이론, 학습 로드맵, 장기 학습 프롬프트로 연결하는 reference 자료를 저장한다.

## Overview

`learning/`은 운영 절차나 실행 계획이 아니라 학습 방향을 보존하는 공간이다. GitOps, Kubernetes, 네트워크, 분산 시스템, AI infrastructure 같은 구현 경험을 이론 학습 주제로 연결하는 durable learning-roadmap 문서를 둔다.

현재 플랫폼 계약, 버전 기준, 운영 정책, 런북은 이 폴더가 아니라 각 canonical stage가 소유한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 인프라 구현 경험과 CS/CE 이론을 연결하는 학습 로드맵
- 장기 학습용 durable concept 정리
- 읽기 목록, 학습 질문, 미니 프로젝트 아이디어
- 여러 stage에서 반복 참조할 수 있는 학습 방향 자료

### Out of Scope

- 현재 플랫폼 요구사항, 아키텍처 결정, 구현 계약
- 실행 계획, 작업 증적, 운영 절차, 장애 대응
- repo-backed 버전 인벤토리와 cloud example snapshot
- Agent runtime policy, provider policy, hook permission 원문

## Structure

```text
learning/
├── infrastructure-to-theory-roadmap.md  # 인프라 구현 경험과 이론 학습 연결
└── README.md                            # This file
```

## How to Work in This Area

1. 새 learning reference는 [reference template](../../99.templates/reference.template.md)을 기반으로 작성한다.
2. 문서가 운영 절차를 안내하면 `docs/05.operations/runbooks/` 또는 `docs/05.operations/guides/`로 라우팅한다.
3. 문서가 버전 기준이나 외부 공식 지원 범위를 고정하면 `docs/90.references/versions/`로 라우팅한다.
4. 학습 자료에는 `Reference Type`, `Authority Boundary`, `Review and Freshness`를 유지한다.
5. 새 learning 문서를 추가하거나 이동하면 이 README와 상위 [90.references README](../README.md)를 함께 갱신한다.

## Related References

- [90.references README](../README.md)
- [Infrastructure to Theory Roadmap](./infrastructure-to-theory-roadmap.md)
- [Templates README](../../99.templates/README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
