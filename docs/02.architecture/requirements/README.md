# 02.architecture/requirements (ARD)

> PRD를 시스템 경계, 품질 속성, 참조 아키텍처 요구로 확장하는 ARD stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 PRD 요구를 시스템 경계, 품질 속성, 데이터 흐름, 보안·관측성·운영성 요구로 확장하는 ARD(Architecture Reference Document) stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

ARD는 참조 아키텍처와 품질 속성을 설명한다. 단일 기술 선택 자체는 `../decisions/`의 ADR에 남기고,
파일 단위 구현 설계나 운영 명령 절차는 각각 `../../03.specs/`, `../../05.operations/`로 넘긴다.

### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 시스템 경계와 책임
- 품질 속성, 데이터 흐름, 보안/관측성/운영성 요구
- 참조 아키텍처와 하위 ADR/Spec 링크

### Out of Scope

- 단일 기술 결정 기록
- 세부 구현 파일 설계
- 운영 명령 절차

## Item Index

```text
02.architecture/requirements/
├── 0004-argo-rollouts-progressive-delivery.md
├── 0005-argo-notifications-slack.md
├── 0006-workspace-agent-governance-platform.md
├── 0007-current-local-gitops-platform.md
├── 0008-workspace-document-assurance-operating-model.md
├── 0009-document-lifecycle-evidence-operating-model.md
└── README.md
```

## Add and Find

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 ARD는 `../../99.templates/templates/sdlc/architecture/ard.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/requirements/####-<system-or-domain>.md`다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. 현재 구현과 상충하는 old/superseded ARD는 `../../98.archive/README.md`에만 인덱싱하고, 활성 ARD는 archive Tombstone에 직접 연결하지 않는다.
5. 구현 가능한 계약은 `03.specs/`로 내려보내고 양방향 링크를 유지한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/requirements/`다.

- 같은 폴더의 ARD 문서는 `./`로 시작한다.
- sibling ADR stage는 `../decisions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../04.execution/`, `../../05.operations/`로 연결한다.
- 새 ARD의 실제 Markdown 링크는 최종 ARD 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Current ARD Index

| 문서 | 역할 | 문서 상태 | 현재성 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [`./0004-argo-rollouts-progressive-delivery.md`](./0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 참조 아키텍처 | Active | Current-contract backfill. `platform-rollouts` Application, dashboard, metrics, AppProject 경계를 소유한다. | [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md) |
| [`./0005-argo-notifications-slack.md`](./0005-argo-notifications-slack.md) | ArgoCD Notifications Slack 알림 참조 아키텍처 | Active | Current-contract backfill. ArgoCD Notifications와 Vault/ESO credential 경계를 소유한다. | [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md) |
| [`./0006-workspace-agent-governance-platform.md`](./0006-workspace-agent-governance-platform.md) | Workspace AI Agent governance와 Stage 00 canonical adapter 참조 아키텍처 | Active | Stage 00 core, shared `.agents` SSoT, local/Antigravity adapters, Claude/Codex native role files, repository-local baselines, validation evidence, and absent/`DEFER` Gemini CLI native 경계를 소유한다. | [`../decisions/0013-stage-00-canonical-adapter-model.md`](../decisions/0013-stage-00-canonical-adapter-model.md) |
| [`./0007-current-local-gitops-platform.md`](./0007-current-local-gitops-platform.md) | 현재 local GitOps platform reference architecture | Active | Current repo-backed baseline. Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer 경계를 소유한다. | [`../../03.specs/008-current-local-gitops-platform/spec.md`](../../03.specs/008-current-local-gitops-platform/spec.md) |
| [`./0008-workspace-document-assurance-operating-model.md`](./0008-workspace-document-assurance-operating-model.md) | Workspace document assurance 운영 모델 | Accepted | Registry, template, authored document, validation, CI/QA, provider, protected-surface 책임과 데이터 흐름을 정의한다. | [`../../03.specs/026-document-contract-registry/spec.md`](../../03.specs/026-document-contract-registry/spec.md) |
| [`./0009-document-lifecycle-evidence-operating-model.md`](./0009-document-lifecycle-evidence-operating-model.md) | Document lifecycle, full-body archive, reference currentness, and QA evidence 운영 모델 | Active | 기존 registry를 유지하면서 lineage, lifecycle, archive, retention, reference, CI cutover 경계를 정의한다. | [`../../03.specs/034-authority-and-lineage-foundation/spec.md`](../../03.specs/034-authority-and-lineage-foundation/spec.md) |

## Related Documents

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [99.templates ARD Template](../../99.templates/templates/sdlc/architecture/ard.template.md)
- [Archive Index](../../98.archive/README.md)
