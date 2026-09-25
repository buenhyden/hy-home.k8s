---
title: "03.specs"
version: "0.6.0"
type: "common/readme-stage-index"
status: "active"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
---
# 03.specs

> Requirement Package와 Architecture를 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../.agents/README.md).

## Overview

이 경로는 Requirement Package, AD, ADR을 구현 가능한 기술 계약으로
구체화하는 Spec stage다. 서비스 동작, API 계약, 변경 한정 설계와 검증
기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 실행 기준을 소유하는 문서다.
Spec은 목표 계약을 담으므로 아직 구현되지 않은 동작을 포함할 수 있다. 관측된 구현과의 의도된 차이는
구현 대기이며, `completed`(현재 철자 `done`)는 수용 조건과 검사한 구현이 일치할 때만 인정한다. 끝난 package는
처분이 승인될 때까지 이 stage에서 기다리고, 승인되면 ADR-0040에 따라 `98.archive/completed/`에 package
단위로 원본 Git object 그대로 보존되며, Retention Catalog가 원래 경로를 한 번 명명하고 원본은 Git history가 복구한다.

### Stage Readers

이 README의 주요 독자:

- Platform Engineers
- Application Developers
- Documentation Writers
- AI Agents

## Stage Contract

### In Scope

- 기능/서비스 기술 설계와 인터페이스 계약
- 데이터 모델, API 계약, 비기능 요구, 검증 기준
- Agent 역할, 도구, 정책, 평가, 실패 모드 설계
- Requirement Package/AD/ADR과 Plan/Task/Runbook을 잇는 traceability

### Out of Scope

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- work-unit 밖의 실행 추적 정본

위 내용은 각각 `01.requirements/`, `05.operations/policies/`,
`05.operations/runbooks/`, 그리고 각 Stage 03 work-unit의
`tasks/tsk-####-<slug>.md` records로 분리한다.

## Document Index

각 package 폴더는 자신의 탐색을 스스로 소유한다. `spec.md`는 변경 계약을,
`plan.md`는 구현 순서와 위험을, `tasks/`는 package-local Task 기록을
소유한다. 이 README는 package 폴더까지만 안내하며, 각 package의 상태와
날짜는 그 package의 `spec.md` frontmatter가 소유한다.

package는 폐기·완료·중복·상충이 증명되고 lifecycle 정규화, consumer 전환,
Git 복구가 끝난 뒤에만 현재 트리를 떠나 [Archive](../98.archive/README.md)에
보존된다. 아래 목록은 시점 목록이며 고정 roster나 개수 불변식이 아니다.

```text
03.specs/
├── 0008-current-local-gitops-platform/
├── 0072-agent-governance-and-quality-gate-consolidation/
├── 0085-archive-reappraisal-and-document-standards/
├── 0086-provider-native-runtime-observation/
├── 0087-stage03-terminal-package-retention/
├── 0088-operations-corpus-convergence/
├── 0089-deferred-conflict-resolution/
├── 0090-spec0049-retirement/
├── 0091-readme-navigation-contract/
└── README.md
```

| Package | 목적 |
| --- | --- |
| [0008-current-local-gitops-platform/](./0008-current-local-gitops-platform/) | 현재 local GitOps platform baseline의 구현 계약 |
| [0072-agent-governance-and-quality-gate-consolidation/](./0072-agent-governance-and-quality-gate-consolidation/) | 공통 agent governance와 local·CI QA 통합 |
| [0085-archive-reappraisal-and-document-standards/](./0085-archive-reappraisal-and-document-standards/) | Archive 재평가와 문서 표준(ADR-0040 cutover) |
| [0086-provider-native-runtime-observation/](./0086-provider-native-runtime-observation/) | Claude·Codex native runtime 관측 |
| [0087-stage03-terminal-package-retention/](./0087-stage03-terminal-package-retention/) | 종료된 Stage 03 package 보존 |
| [0088-operations-corpus-convergence/](./0088-operations-corpus-convergence/) | 운영 문서 역할 정리와 검증 script 정리 |
| [0089-deferred-conflict-resolution/](./0089-deferred-conflict-resolution/) | SPEC-0088 보류 충돌 해소 |
| [0090-spec0049-retirement/](./0090-spec0049-retirement/) | SPEC-0049 `retired/` 보존 |
| [0091-readme-navigation-contract/](./0091-readme-navigation-contract/) | README 탐색 계약 |

## Authoring Workflow

1. 관련 Requirement Package, AD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<####-slug>/spec.md`다.
3. 변경 한정 설계와 실행 계약은 `spec.md`, 구현 순서·위험·검증·rollback은 `plan.md`, 실행 증거는 package-local Task record가 소유한다. 실행 가능한 API 계약은 해당 Spec Package가 소유한다.
4. 장기 구조는 Stage 02 Architecture Description으로, 중요한 장기 결정은 ADR로 승격한다. 폐기된 Stage 04 경로는 새 문서에서 사용하지 않는다.
5. 종단 처분은 Stage 98 disposition이 기록한다. 끝난 package는 consumer-zero 뒤 `98.archive/completed/`에 보존하고, 대체되거나 후속 없이 철회된 단독 문서는 `superseded/` 또는 `retired/`에 본문 그대로 보존한다. 경로 이동은 본문 없는 `migrations/`가 현재 owner를 명명한다([ADR-0040](../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)). 원본 바이트는 Git history가 복구한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 package는 `./<####-numbering>-<feature-id>/` 폴더로 연결한다.
- 실행 문서는 같은 work-unit의 `plan.md`와 `tasks/tsk-####-<slug>.md`, 운영 문서는 `../05.operations/`로 연결한다.
- feature-local helper 문서 링크는 `docs/03.specs/<####-numbering>-<feature-id>/` 안의 최종 파일 위치 기준으로 다시 계산한다.

### Spec Authoring Rules

1. 모든 활성 Spec은 관련 Requirement Package와 Architecture 입력을 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Contract와 테스트 의도는 Requirement Package에서 이어지고, 구현 검증은 Task record와 연결된다.
4. 실행 가능한 인터페이스 계약은 실제 구현 소유 경로에 두고 Spec에서 그 owner와 검증을 추적한다.
5. Agent 변경은 목표·동작·경계·실패 조건을 Spec에, 구현 순서와 rollback을 Plan에 기록한다.
6. Feature-local Task records가 해당 work-unit의 실행과 evidence를 소유한다. Validator의 독립 실행 테스트와 fixture는 top-level `tests/`와 `tests/fixtures/` 아래에 두고, production module은 이를 import하거나 runtime data로 읽지 않는다. `validation/tests/` 또는 Spec-package-local test control plane은 만들지 않는다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 Requirement Package/AD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

### Helper Templates

아래 템플릿은 `docs/03.specs/<####-slug>/` 패키지와 해당 Spec이 소유하는 실행 가능 인터페이스 계약에 사용한다.

- `../99.templates/templates/specs/spec.template.md`
- `../99.templates/templates/specs/plan.template.md`
- `../99.templates/templates/specs/task.template.md`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/descriptions](../02.architecture/descriptions/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
