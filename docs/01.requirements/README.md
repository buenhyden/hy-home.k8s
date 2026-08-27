# 01.requirements

> hy-home.k8s 플랫폼의 장기간 유지되는 solution-independent Requirement Package를 보관하는 canonical stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 문제, 목표, stakeholder 요구, 기능·비기능·외부 interface 요구,
제약과 acceptance 기준을 하나의 Requirement Package로 소유한다. Stage 01은
구현 방법과 특정 기술을 고정하지 않고 '무엇을(What)', '왜(Why)' 개발하는지
장기간 유지한다.

### Stage Readers

이 README의 주요 독자:

- Product Owners
- Platform Engineers
- Documentation Writers
- AI Agents

## Stage Contract

### In Scope

- 문제·목표, 사용자 및 stakeholder 요구
- 기능·비기능 요구, 제약, 구현 독립적인 외부 interface 요구
- acceptance 기준, 범위·비범위, 관련 Architecture·Spec 추적 링크

### Out of Scope

- 상세 구현 방법, 변경 한정 설계, 파일 수준 구현 순서
- 구체 기술 스택 결정과 장기적인 구조 결정
- OpenAPI·GraphQL·Proto 같은 실행 가능한 interface 계약
- 장애 대응 절차와 운영 명령

포함하지 말아야 할 내용은 각각 `../02.architecture/descriptions/`,
`../02.architecture/decisions/`, `../03.specs/`,
`../05.operations/runbooks/`로 분리한다. 실행 가능한 OpenAPI·GraphQL·Proto
계약은 이를 구현하는 Stage 03 Spec Package가 소유한다.

현행 작성 경로는 `####-<slug>.md` 하나이며 부모 stage가 문서 유형을 결정한다.
Requirement Package의 안정 ID는 `REQ-####`이고 경로 번호와 반드시
일치한다. PRD, SRS, Interface Requirement를 별도 문서나 profile로 나누지
않는다.

## Document Index

```text
01.requirements/
├── 0001-argo-rollouts-progressive-delivery.md
├── 0002-argo-notifications-slack.md
├── 0003-workspace-agent-governance-platform.md
├── 0004-current-local-gitops-platform.md
├── 0005-workspace-document-assurance-modernization.md
├── 0006-workspace-document-lifecycle-and-evidence-consolidation.md
├── 0007-repository-delivery-and-platform-assurance.md
├── 0008-workspace-document-taxonomy-consolidation.md
└── README.md
```

## Authoring Workflow

1. 같은 문제를 다루는 현재 Requirement Package를 먼저 확인하고 중복 package를 만들지 않는다.
2. `../99.templates/templates/requirements/requirement-package.template.md`를 복사해 `####-<slug>.md`를 만든다. 템플릿은 재사용 가능하도록 `artifact_id`를 비워 두므로, 복사 직후 아직 발급되지 않은 다음 번호를 `REQ-####`로 할당하고 경로 번호와 일치시킨다.
3. package 안의 기능·비기능·interface 요구에는 각각 `REQ-####-FR-####`, `REQ-####-NFR-####`, `REQ-####-IF-####` 형식의 안정 ID를 발급한다. 다른 문서에서도 축약형 `FR-####`가 아니라 전체 ID를 사용하며, 삭제된 ID를 재사용하지 않는다.
4. 문제·목표·stakeholder 요구, 기능·비기능·interface 요구, 제약, acceptance 기준과 범위·비범위를 구현 독립적으로 작성한다.
5. 관련 `../02.architecture/descriptions/`, `../02.architecture/decisions/`, `../03.specs/` 추적 링크를 함께 갱신한다. 변경 가능한 실행 계약과 interface 구현 산출물은 Stage 03에 둔다.
6. Agent 기능 요구에는 허용·금지 행동과 human-in-the-loop 기준을 포함하고, 에이전트 실행 요구사항은 영어로 유지한다.
7. 변경·폐기 시 `status`, `supersedes`, `superseded_by`로 이력을 연결한다. 이전 본문은 Git history가 보존하며, 대규모 권위 이동이나 삭제된 안정 경로에 복구 안내가 필요할 때만 Stage 98 Migration 또는 최소 Tombstone을 남긴다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/01.requirements/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 동일 stage 문서는 `./`로 시작하는 상대 경로를 사용한다.
- 하위 stage 연결은 `../02.architecture/`, `../03.specs/` 등 인접 stage 경로를 사용한다.
- 새 Requirement Package의 실제 Markdown 링크는 최종 파일 위치 기준으로 다시 계산하고, 아직 없는 후속 문서는 code literal로 남긴다.

### 연결 규칙

- Requirement Package는 관련 AD, ADR, Spec 링크를 가진다.
- AD와 Spec은 `REQ-####-(FR|NFR|IF)-####` 전체 요구 ID를 추적한다.
- Agent 기능인 경우 사용 시나리오, 허용/금지 행동, human-in-the-loop 요구를 포함하고, 에이전트 실행 요구사항은 영어로 유지한다.
- 후속 AD/ADR/Spec이 아직 없으면 없는 링크를 만들지 않고, 문서 인덱스와 Requirement Package의 `Related Documents`에 후속 갭으로 표시한다.
- 현재 구현과 맞지 않는 변경 한정 실행 계약을 Stage 01에 보존하지 않는다. 필요한 이전 경로 증거는 Stage 98 중앙 인덱스를 통해 조회한다.

### 요구사항 읽는 순서

1. 현재 로컬 GitOps 플랫폼 기준은 [`0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md)와 `gitops/**`, `infrastructure/**`, `scripts/**` 정적 검증 증적이 소유한다.
2. `active` 문서는 현재 요구 권위다. downstream AD/ADR/Spec과 구현 증적을 함께 확인한다.
3. `draft` 문서는 아직 현재 요구 권위가 아닌 초안이다. 구현은 승인된 downstream Spec과 Plan이 있어야 시작한다.
4. 과거 문서가 필요한 경우 활성 문서에서 개별 Tombstone으로 직접 이동하지 않고 [`../98.archive/README.md`](../98.archive/README.md)의 중앙 인덱스를 통해 확인한다.

### 상태 해석

| 상태 | 의미 | 작업 기준 |
| --- | --- | --- |
| `draft` | 검토 중이며 아직 현재 권위가 아닌 요구 초안 | 구현 시작 전 승인과 downstream Spec/Plan 갭을 해소한다. |
| `active` | 현재 solution-independent 요구 권위 | 관련 AD/ADR/Spec과 current 구현 증적을 함께 확인한다. |
| `superseded` | 새 Requirement Package가 대체한 이전 권위 | `superseded_by`와 새 문서의 `supersedes`를 상호 연결하며 Stage 01에 유지한다. |
| `retired` | 대체 없이 의도적으로 종료한 요구 | 종료 사유와 마지막 추적 대상을 남기고 신규 구현의 권위로 사용하지 않는다. |
| `withdrawn` | 승인 전에 철회한 요구 | 철회 사유를 남기고 downstream 구현을 시작하지 않는다. |

### 문서 인덱스

| 문서 | 역할 | 현재성 | 추적성 / 후속 갭 | 최종 수정 |
| --- | --- | --- | --- | --- |
| [`./0001-argo-rollouts-progressive-delivery.md`](./0001-argo-rollouts-progressive-delivery.md) | Argo Rollouts canary/blue-green 점진적 배포 Requirement Package | `active` current-contract backfill | AD/Spec/Plan/Task 연결 완료. 현재 GitOps 계약은 `platform-rollouts` Application, Prometheus AnalysisTemplate workload pattern, Rollouts 운영 문서가 소유. | 2026-06-04 |
| [`./0002-argo-notifications-slack.md`](./0002-argo-notifications-slack.md) | Argo Notifications Slack 알림 Requirement Package | `active` current-contract backfill | AD/Spec/Plan/Task 연결 완료. 현재 Secret 경계는 Vault/ESO/ArgoCD Notifications 문서가 소유. | 2026-06-04 |
| [`./0003-workspace-agent-governance-platform.md`](./0003-workspace-agent-governance-platform.md) | Workspace AI Agent governance, provider-native harness, loop, model, and evidence program Requirement Package | `active` | AD-0006과 accepted current ADR-0019 및 Specs 041–046의 repository-local closure를 정의한다. ADR-0013은 accepted historical predecessor이고 provider-runtime readiness는 계속 별도 evidence lane이다. | 2026-08-01 |
| [`./0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md) | 현재 repo-backed local GitOps 플랫폼 baseline Requirement Package | `active` | AD-0007, ADR-0014, Spec 008, docs alignment Plan/Task 연결 완료. | 2026-06-02 |
| [`./0005-workspace-document-assurance-modernization.md`](./0005-workspace-document-assurance-modernization.md) | Workspace document assurance modernization program Requirement Package | `superseded` | AD-0008, ADR-0015/0016과 Spec 026–032 및 각 canonical Plan/Task의 repository-static 구현 완료 증적을 소유한다. | 2026-07-14 |
| [`./0006-workspace-document-lifecycle-and-evidence-consolidation.md`](./0006-workspace-document-lifecycle-and-evidence-consolidation.md) | Workspace document lifecycle, archive, reference, and QA evidence consolidation program Requirement Package | `superseded` | 2026-07-28 기준 AD-0009, ADR-0017/0018/0020, Specs 034–040과 통합 repository-static contract는 exact 14-path terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`에서 종료됐다. Final frontier는 `0/0·6/3·3`이고 reviewed digest `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`은 terminal requirements/quality/security approval을 받았다. Parent `35d8552ba423e3e2d92294ddeb81674392b8f333`부터 closure까지 explicit-ref와 clean-tree aggregate는 PASS이며, evidence-update commit 자체와 hosted/provider/remote/live는 주장하지 않는다. | 2026-07-28 |
| [`./0007-repository-delivery-and-platform-assurance.md`](./0007-repository-delivery-and-platform-assurance.md) | Repository delivery, GitHub routing, platform validation, IaC QA, and local integration assurance program Requirement Package | `active` | AD-0010과 ADR-0021을 기반으로 Spec 047을 첫 tranche로 두고 planned Specs 048–051의 경계를 정의한다. REQ-0004/AD-0007/ADR-0014/Spec 008의 current platform topology 소유권과 remote/live approval boundary는 유지한다. Requirement Package 자체는 active·governing 상태를 유지하고 2026-08-07부터 REQ-0008 document taxonomy consolidation 기간 동안 실행만 일시 중단된다. Spec 047과 그 Plan/Task는 draft로 되돌아갔고, Spec 052가 `done`에 도달하면 통합된 구조에서 실행을 재개한다. | 2026-08-07 |
| [`./0008-workspace-document-taxonomy-consolidation.md`](./0008-workspace-document-taxonomy-consolidation.md) | Workspace SDLC taxonomy, document/agent-governance authority, and validator consolidation program Requirement Package | `active` | AD-0011, accepted current ADR-0024, transition predecessor ADR-0023, Spec 052를 통해 Stage 03 work-unit 통합, Stage 04 execution 폐지, Stage 05 유지, Release 제외, stable filename/date 예외, AI agent governance 및 validator 정리를 정의한다. REQ-0007 Specs 047–051은 통합 완료까지 실행 중단 상태다. | 2026-08-11 |

### 예시

신규 플랫폼 기능은 [`0004-current-local-gitops-platform.md`](./0004-current-local-gitops-platform.md)처럼 사용자 가치, 범위, 성공/수용 기준과 전체 요구 ID를 현재 구현 증적에 연결한다.

## Related Documents

- [Docs README](../README.md)
- [02.architecture/descriptions](../02.architecture/descriptions/README.md)
- [03.specs](../03.specs/README.md)
- [Archive Index](../98.archive/README.md)
