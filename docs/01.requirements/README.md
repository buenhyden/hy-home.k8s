# 01.requirements

> hy-home.k8s 플랫폼의 제품 요구사항(PRD)을 보관하는 canonical stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## Overview

이 경로는 `hy-home.k8s` 플랫폼의 제품 요구사항(PRD)을 보관하는 canonical stage다.
새 기능이나 플랫폼 변화가 어떤 사용자/운영자 가치와 성공/수용 기준을 가져야 하는지 먼저 정의한다.
모든 개발의 시작점이며, '무엇을(What)', '왜(Why)' 개발하는지 설명한다.

### Stage Readers

이 README의 주요 독자:

- Product Owners
- Platform Engineers
- Documentation Writers
- AI Agents

## Stage Contract

### In Scope

- 문제 정의, 사용자/운영자 가치, 성공 지표
- 기능 요구, 수용 기준(Acceptance Criteria), 범위/비범위
- 관련 ARD, Spec, Plan으로 이어지는 요구사항 추적 링크

### Out of Scope

- 상세 구현 방법과 파일 수준 설계
- 구체 기술 스택 결정
- 장애 대응 절차와 운영 명령

포함하지 말아야 할 내용은 각각 `02.architecture/requirements/`, `02.architecture/decisions/`, `03.specs/`, `05.operations/runbooks/`로 분리한다.

## Document Index

```text
01.requirements/
├── 001-argo-rollouts-progressive-delivery.md
├── 002-argo-notifications-slack.md
├── 003-workspace-agent-governance-platform.md
├── 004-current-local-gitops-platform.md
├── 005-workspace-document-assurance-modernization.md
├── 006-workspace-document-lifecycle-and-evidence-consolidation.md
└── README.md
```

## Authoring Workflow

1. 새 요구사항을 작성하기 전에 같은 문제를 다루는 기존 PRD를 먼저 확인한다.
2. 새 PRD는 `../99.templates/templates/sdlc/requirements/prd.template.md`에서 시작하고, canonical target pattern은 `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`다.
3. PRD는 문제, persona/use case, 기능 요구, `Success / Acceptance Criteria`, 범위/비범위를 분리한다.
4. 요구사항 변경 시 관련 `02.architecture/requirements/`, `03.specs/`, `04.execution/plans/` 링크를 함께 갱신한다.
5. 구현 파일, manifest, 스크립트, 운영 명령 수준의 상세 설계는 PRD에 직접 확장하지 않고 후속 ARD/Spec/Plan 갭으로 남긴다.
6. Agent 기능 요구에는 허용/금지 행동과 human-in-the-loop 기준을 포함하고, `AI Agent Requirements` 섹션은 영어로 작성한다.
7. 현재 구현과 상충하는 old/superseded PRD는 full-body Archive Record로 보존하되 `../98.archive/README.md`에만 인덱싱하고, 활성 PRD는 개별 record에 직접 연결하지 않는다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/01.requirements/`다.

- 상위 문서는 `../`로 시작하는 상대 경로를 사용한다.
- 동일 stage 문서는 `./`로 시작하는 상대 경로를 사용한다.
- 하위 stage 연결은 `../02.architecture/`, `../03.specs/` 등 인접 stage 경로를 사용한다.
- 새 PRD의 실제 Markdown 링크는 최종 PRD 파일 위치 기준으로 다시 계산하고, 아직 없는 후속 문서는 code literal로 남긴다.

### 연결 규칙

- PRD는 관련 ARD, Spec, Plan, ADR 링크를 가진다.
- Spec은 PRD 요구 ID를 추적한다.
- Agent 기능인 경우 사용 시나리오, 허용/금지 행동, human-in-the-loop 요구를 포함하고, 에이전트 실행 요구사항은 영어로 유지한다.
- 후속 ARD/Spec/Plan이 아직 없으면 없는 링크를 만들지 않고, 문서 인덱스와 PRD의 `Related Documents`에 후속 갭으로 표시한다.
- 현재 구현과 맞지 않는 old 실행계약은 활성 PRD에 보존하지 않고 provenance가 검증된 Archive Record로 이동한다.

### 요구사항 읽는 순서

1. 현재 로컬 GitOps 플랫폼 기준은 [`004-current-local-gitops-platform.md`](./004-current-local-gitops-platform.md)와 `gitops/**`, `infrastructure/**`, `scripts/**` 정적 검증 증적이 소유한다.
2. `Active` 문서는 현재 작업 기준으로 사용할 수 있지만, downstream ARD/ADR/Spec/Plan과 구현 증적을 함께 확인한다.
3. `Draft` 문서는 후속 ARD/Spec/Plan이 완성되기 전의 제품 의도다. 구현은 별도 downstream 문서와 승인된 계획이 있어야 시작한다.
4. 과거 문서가 필요한 경우 활성 문서에서 개별 Archive Record로 직접 이동하지 않고 [`../98.archive/README.md`](../98.archive/README.md)의 중앙 인덱스를 통해서만 확인한다.

### 상태 해석

| 상태 | 의미 | 작업 기준 |
| --- | --- | --- |
| Active | 현재 제품 의도를 설명하는 PRD | 관련 ADR/Spec/Plan과 current contract 메모를 함께 확인한다. |
| Draft | 요구사항 초안 또는 후속 설계 대기 상태 | 구현 시작 전 ARD/Spec/Plan 후속 갭을 해소한다. |
| Done | 승인된 범위와 수용 기준을 repository-static 증적으로 종료한 PRD | 연결된 ARD/ADR/Spec/Plan/Task와 로컬 검증 증적을 함께 확인하며, remote/live/secret 검증으로 확대 해석하지 않는다. |
| Archived | 현재 구현과 상충하거나 대체된 요구사항 기록 | 활성 stage에는 본문을 두지 않고 full-body Archive Record를 [`../98.archive/README.md`](../98.archive/README.md)에만 인덱싱한다. |

### 문서 인덱스

| 문서 | 역할 | 현재성 | 추적성 / 후속 갭 | 최종 수정 |
| --- | --- | --- | --- | --- |
| [`./001-argo-rollouts-progressive-delivery.md`](./001-argo-rollouts-progressive-delivery.md) | Argo Rollouts canary/blue-green 점진적 배포 PRD | Active current-contract backfill | ARD/Spec/Plan/Task 연결 완료. 현재 GitOps 계약은 `platform-rollouts` Application, Prometheus AnalysisTemplate workload pattern, Rollouts 운영 문서가 소유. | 2026-06-04 |
| [`./002-argo-notifications-slack.md`](./002-argo-notifications-slack.md) | Argo Notifications Slack 알림 PRD | Active current-contract backfill | ARD/Spec/Plan/Task 연결 완료. 현재 Secret 경계는 Vault/ESO/ArgoCD Notifications 문서가 소유. | 2026-06-04 |
| [`./003-workspace-agent-governance-platform.md`](./003-workspace-agent-governance-platform.md) | Workspace AI Agent governance, Stage 00 canonical adapter, skill-axis routing PRD | Active current-contract backfill | ARD-0006, ADR-0013, Spec 006, Stage 00 canonical adapter Plan/Task 연결 완료. | 2026-06-01 |
| [`./004-current-local-gitops-platform.md`](./004-current-local-gitops-platform.md) | 현재 repo-backed local GitOps 플랫폼 baseline PRD | Active | ARD-0007, ADR-0014, Spec 008, docs alignment Plan/Task 연결 완료. | 2026-06-02 |
| [`./005-workspace-document-assurance-modernization.md`](./005-workspace-document-assurance-modernization.md) | Workspace document assurance modernization program PRD | Done | ARD-0008, ADR-0015/0016과 Spec 026–032 및 각 canonical Plan/Task의 repository-static 구현 완료 증적을 소유한다. | 2026-07-14 |
| [`./006-workspace-document-lifecycle-and-evidence-consolidation.md`](./006-workspace-document-lifecycle-and-evidence-consolidation.md) | Workspace document lifecycle, archive, reference, and QA evidence consolidation program PRD | Active | ARD-0009, ADR-0017/0018, Specs 034–040의 기반 우선 다중 Spec 구현을 소유한다. | 2026-07-15 |

### 예시

신규 플랫폼 기능은 [`004-current-local-gitops-platform.md`](./004-current-local-gitops-platform.md)처럼 사용자 가치, 범위, 성공/수용 기준을 현재 구현 증적과 함께 기록한다.

## Related Documents

- [Docs README](../README.md)
- [02.architecture/requirements](../02.architecture/requirements/README.md)
- [03.specs](../03.specs/README.md)
- [04.execution/plans](../04.execution/plans/README.md)
- [Archive Index](../98.archive/README.md)
