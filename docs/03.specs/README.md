# 03.specs

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 PRD/ARD/ADR을 구현 가능한 기술 계약으로 구체화하는 Spec stage다.
서비스, API, 데이터 모델, Agent 설계, 검증 기준은 이곳에서 하위 구현과 추적 가능해야 한다.

## Audience

이 README의 주요 독자:

- Platform Engineers
- Application Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 기능/서비스 기술 설계와 인터페이스 계약
- 데이터 모델, API 계약, 비기능 요구, 검증 기준
- Agent 역할, 도구, 정책, 평가, 실패 모드 설계

### Out of Scope

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- 실행 추적의 정본 작업 목록

## Structure

```text
03.specs/
├── 001-wsl-k3d-argocd-platform/
│   └── spec.md
├── 002-wsl2-k3d-argocd-ha-platform/
│   └── spec.md
├── 003-platform-expansion/
│   └── spec.md
└── README.md
```

## How to Work in This Area

1. 관련 PRD, ARD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/spec.template.md`에서 시작한다.
3. API/데이터/Agent 보조 문서는 기능 하위 폴더에 두고 상위 `spec.md`와 연결한다.
4. 구현 및 검증 추적은 `04.execution/tasks/`로 연결한다.

## Related References

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [04.execution/tasks](../04.execution/tasks/README.md)

## 목적

이 폴더는 설계 명세(Specification)의 중심이다. SDD(Software Design Description) 관점에서 기능, 서비스, API, 데이터 모델, AI Agent 설계를 구체화한다.

## 문서 책임

- 기능 또는 서비스의 기술 설계
- 인터페이스와 데이터 계약
- 비기능 요구와 운영성
- AI Agent 역할, 도구, 평가, 안전 제약
- API 계약 문서의 부모 위치

## 포함할 내용

- 설계 범위와 비목표
- 관련 PRD / ARD / ADR 입력 링크
- 핵심 설계
- 데이터 모델
- 인터페이스와 계약
- Verification
- 필요 시 API Spec, Agent 설계, 계약 파일

## 포함하지 말아야 할 내용

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- 실행 추적의 정본 작업 목록

위 내용은 각각 `01.requirements/`, `05.operations/policies/`, `05.operations/runbooks/`, `04.execution/tasks/`로 분리한다.

## 권장 내부 구조

```text
03.specs/
  001-feature-name/
    spec.md
    api-spec.md
    agent-design.md
    data-model.md
    tests.md
    contracts/
      openapi.yaml
```

## 기본 문서 역할

- `spec.md`: 기능 전체 설계, 계약, 비기능 요구, 검증 기준
- `api-spec.md`: API 계약 상세
- `agent-design.md`: Agent 역할, 도구, 메모리, 정책, 오케스트레이션
- `data-model.md`: 데이터 구조와 저장 전략
- `tests.md`: TDD 기반 테스트 전략, 테스트 케이스, 평가 항목
- `contracts/`: OpenAPI, gRPC proto, GraphQL schema 등 기계 가독 계약 파일

## API Specifications

이 디렉터리의 기능 또는 서비스 Spec 중 API 계약이 필요한 경우, 별도의 API Spec 문서를 사용한다.

- 위치 예시:
  - `docs/03.specs/<feature-id>/api-spec.md`
- 사용 템플릿:
  - `docs/99.templates/api-spec.template.md`

### 역할 구분

- 메인 Spec:
  - 기능/서비스 전체 설계, 데이터 모델, 비기능 요구, 운영성, 관측성을 다룬다.
- API Spec:
  - HTTP/GraphQL/gRPC 계약, 엔드포인트, 스키마, 인증, 에러, 버저닝, 거버넌스를 상세히 정의한다.

### 금지 규칙

- API Spec을 `docs/api/` 같은 별도 최상위 문서 체계로 분리하지 않는다.
- API Spec은 `03.specs` 아래 기능 단위 하위 문서로 유지한다.

## Spec 작성 규칙

1. 모든 활성 Spec은 관련 PRD와 ARD를 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Criteria와 테스트는 PRD에서 이어지고, 구현 검증은 Task와 연결된다.
4. API가 있다면 API Spec 또는 계약 파일을 함께 둔다.
5. Agent 설계가 있다면 아래 항목을 명시한다.
   - Agent Role & IO Contract
   - Tools & Tool Contract
   - Prompt/Policy Contract
   - Memory & Context Strategy
   - Guardrails
   - Evaluation
   - Failure Modes / Fallback / Human Escalation

## `04.execution/tasks`와의 관계

- 기능 내부의 설계 보조용 `tasks.md` 또는 `tests.md`는 `03.specs/<feature-id>/`에 둘 수 있다.
- 그러나 실행 추적, 스프린트 관리, 검증·평가 기록의 정본은 `04.execution/tasks/`에 둔다.

## Templates

- `../99.templates/spec.template.md`
- `../99.templates/api-spec.template.md`
- `../99.templates/agent-design.template.md`
- `../99.templates/data-model.template.md`
- `../99.templates/tests.template.md`
- `../99.templates/openapi.template.yaml`
- `../99.templates/service.template.proto`
- `../99.templates/schema.template.graphql`

## 문서 인덱스

| 문서                                                                                   | 설명                                                                                                     | 상태   | 최종 수정  |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------ | ---------- |
| [`./001-wsl-k3d-argocd-platform/spec.md`](./001-wsl-k3d-argocd-platform/spec.md)         | WSL2 k3d/k3s + ArgoCD + ESO/Vault + 외부 DB/Valkey 기술 명세                                             | Draft  | 2026-03-27 |
| [`./002-wsl2-k3d-argocd-ha-platform/spec.md`](./002-wsl2-k3d-argocd-ha-platform/spec.md) | Valkey/TLS/최소권한 계약과 `.github` CI 정적 게이트/`verify-contracts-static.sh` 명세를 포함한 기술 명세 | Draft  | 2026-05-09 |
| [`./003-platform-expansion/spec.md`](./003-platform-expansion/spec.md)                   | 2026-03-29 IP 수정 + cert-manager/Dashboard/Istio/Kiali 확장 명세, 현재 실행계약은 Headlamp/172.18.x 기준 | Active | 2026-05-09 |

## 관련 폴더

- `01.requirements/`: Spec이 만족해야 할 요구사항
- `02.architecture/requirements/` / `02.architecture/decisions/`: 설계 경계와 결정 근거
- `04.execution/tasks/`: Spec 구현과 검증 추적

## 예시

- k3d/GitOps 플랫폼 구현 계약은 `001-wsl-k3d-argocd-platform/spec.md`처럼 feature 하위 폴더의 `spec.md`로 관리한다.
