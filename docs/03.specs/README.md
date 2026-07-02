# 03.specs

> PRD/ARD/ADR을 구현 가능한 기술 계약과 검증 기준으로 구체화하는 Spec stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 PRD, ARD, ADR을 구현 가능한 기술 계약으로 구체화하는 Spec stage다.
서비스, API, 데이터 모델, Agent 설계, 검증 기준은 이곳에서 하위 구현과 추적 가능해야 한다.

Spec은 실행 기준을 소유하는 문서다.
활성 Spec은 현재 repo-backed 구현과 일치해야 하며, 구현과 상충하는 old Spec은 중앙 archive Tombstone으로 이동한다.

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
- PRD/ARD/ADR과 Plan/Task/Runbook을 잇는 traceability

### Out of Scope

- 제품 우선순위와 사용자 가치 중심 설명
- 전사 운영 정책
- 실시간 장애 대응 절차
- 실행 추적의 정본 작업 목록

위 내용은 각각 `01.requirements/`, `05.operations/policies/`, `05.operations/runbooks/`, `04.execution/tasks/`로 분리한다.

## Structure

```text
03.specs/
├── 004-argo-rollouts-progressive-delivery/
│   └── spec.md
├── 005-argo-notifications-slack/
│   └── spec.md
├── 006-workspace-harness-gap-analysis/
│   └── spec.md
├── 008-current-local-gitops-platform/
│   └── spec.md
├── 009-workspace-harness-research-pack/
│   └── spec.md
├── 010-workspace-harness-implementation-audit-pack/
│   └── spec.md
├── 011-template-contract-governance-migration/
│   └── spec.md
└── README.md
```

## How to Work in This Area

1. 관련 PRD, ARD, ADR 링크를 확인하고 Spec의 입력으로 고정한다.
2. 새 Spec은 `../99.templates/templates/sdlc/specs/spec.template.md`에서 시작하고, canonical target pattern은 `docs/03.specs/<feature-id>/spec.md`다.
3. API/데이터/Agent/Test 보조 문서는 같은 feature 하위 폴더에 두고 상위 `spec.md`와 연결한다.
4. 구현 및 검증 추적은 `04.execution/tasks/`로 연결한다.
5. 현재 구현과 상충하는 historical/superseded 값은 활성 Spec에 보존하지 않고 `../98.archive/README.md`의 Tombstone 인덱스로 분리한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/03.specs/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 같은 stage의 spec은 `./<feature-id>/spec.md`로 연결한다.
- 실행 문서는 `../04.execution/`, 운영 문서는 `../05.operations/`로 연결한다.
- feature-local helper 문서 링크는 `docs/03.specs/<feature-id>/` 안의 최종 파일 위치 기준으로 다시 계산한다.

## Spec Authoring Rules

1. 모든 활성 Spec은 관련 PRD와 ARD를 링크하거나 부재를 명시한다.
2. Verification은 필수다.
3. Acceptance Criteria와 테스트는 PRD에서 이어지고, 구현 검증은 Task와 연결된다.
4. API가 있다면 API Spec 또는 계약 파일을 함께 둔다.
5. Agent 설계가 있다면 Role, Tool, Policy, Memory, Guardrail, Evaluation, Fallback을 명시한다.
6. feature-local `tasks.md` 또는 `tests.md`는 설계 보조 문서이며, 실행 추적 정본은 `../04.execution/tasks/`다.
7. `Related Inputs`는 upstream 요약이고, `Related Documents`는 PRD/ARD/ADR와 Plan/Task/Operations 링크를 함께 담는다.

## Document Index

| 문서 | 설명 | 상태 | 현재성 | 최종 수정 |
| --- | --- | --- | --- | --- |
| [`./004-argo-rollouts-progressive-delivery/spec.md`](./004-argo-rollouts-progressive-delivery/spec.md) | Argo Rollouts 점진적 배포 current-contract backfill 명세 | Active | `platform-rollouts` Application, dashboard, metrics, AppProject 권한, 앱 canary AnalysisTemplate 경계를 현재 계약으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다. | 2026-06-04 |
| [`./005-argo-notifications-slack/spec.md`](./005-argo-notifications-slack/spec.md) | ArgoCD Notifications Slack current-contract backfill 명세 | Active | ArgoCD Notifications, Vault/ESO credential boundary, template/trigger 계약을 현재 기준으로 정리한다. 구현 evidence는 Spec의 Implementation Status를 따른다. | 2026-05-22 |
| [`./006-workspace-harness-gap-analysis/spec.md`](./006-workspace-harness-gap-analysis/spec.md) | Workspace harness Gap analysis와 제한 구현 계약 | Active | WSL2, WSL Linux native Docker, k3d, ArgoCD GitOps, SDD lifecycle, QA, CI/CD, Agent governance의 repo-static 개선 범위를 정의한다. P3 repo desired-state 보완은 별도 실행 증적에 반영됐고, live runtime 검증·secret value 확인·CI ruleset/pinning 정책은 deferred item으로 남긴다. | 2026-06-02 |
| [`./008-current-local-gitops-platform/spec.md`](./008-current-local-gitops-platform/spec.md) | 현재 local GitOps platform baseline Spec | Active | Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 구현 증적을 소유한다. | 2026-06-02 |
| [`./009-workspace-harness-research-pack/spec.md`](./009-workspace-harness-research-pack/spec.md) | Workspace harness/loop engineering research pack 명세 | Draft | `docs/90.references/research/` 아래 통합 연구 팩의 구조, 공식 외부 소스 우선순위, market scan 경계, implementation checklist 포함 방식, 검증 기준을 정의한다. | 2026-07-02 |
| [`./010-workspace-harness-implementation-audit-pack/spec.md`](./010-workspace-harness-implementation-audit-pack/spec.md) | Workspace harness/loop implementation audit pack 명세 | Draft | `docs/90.references/research/` 기준 모델과 repo-backed evidence를 대조해 `docs/90.references/audits/` 아래 4개 구현 현황 감사 보고서와 README를 작성하는 계약을 정의한다. | 2026-07-02 |
| [`./011-template-contract-governance-migration/spec.md`](./011-template-contract-governance-migration/spec.md) | Template contract와 governance migration 명세 | Draft | `docs/99.templates/`를 template forms와 support contracts로 분리하고, frontmatter schema, validator, hook, governance, authored docs 적용을 4단계 migration으로 정의한다. | 2026-07-03 |

## Helper Templates

아래 템플릿은 `docs/03.specs/<feature-id>/` 아래에서 `spec.md`를 보조하는 계약 문서에만 사용한다.

- `../99.templates/templates/sdlc/specs/spec.template.md`
- `../99.templates/templates/sdlc/specs/api-spec.template.md`
- `../99.templates/templates/sdlc/specs/agent-design.template.md`
- `../99.templates/templates/sdlc/specs/data-model.template.md`
- `../99.templates/templates/sdlc/specs/tests.template.md`
- `../99.templates/templates/sdlc/specs/openapi.template.yaml`
- `../99.templates/templates/sdlc/specs/service.template.proto`
- `../99.templates/templates/sdlc/specs/schema.template.graphql`

## Related Documents

- [Docs README](../README.md)
- [01.requirements](../01.requirements/README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md)
- [02.architecture/decisions](../02.architecture/decisions/README.md)
- [04.execution/plans](../04.execution/plans/README.md)
- [04.execution/tasks](../04.execution/tasks/README.md)
- [05.operations/runbooks](../05.operations/runbooks/README.md)
- [Archive Index](../98.archive/README.md)
