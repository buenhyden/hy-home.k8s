---
title: "02.architecture/descriptions (AD)"
version: "0.1.0"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-05"
layer: "architecture"
---
# 02.architecture/descriptions (AD)

> Requirement Package를 시스템 경계, 품질 속성, 참조 아키텍처로 해석하는 AD stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../../.agents/README.md).

## Overview

이 경로는 Requirement Package를 시스템 경계, 품질 속성, 데이터 흐름,
보안·관측성·운영성 관점으로 해석하는 AD(Architecture Description) stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

AD는 참조 아키텍처와 품질 속성을 설명한다. 단일 기술 선택 자체는 `../decisions/`의 ADR에 남기고,
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
02.architecture/descriptions/
├── 0004-argo-rollouts-progressive-delivery.md
├── 0005-argo-notifications-slack.md
├── 0006-workspace-agent-governance-platform.md
├── 0007-current-local-gitops-platform.md
└── README.md
```

## Add and Find

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 AD는 `../../99.templates/templates/architecture/description.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/descriptions/####-<system-or-domain>.md`다. 안정 ID `AD-####`는 frontmatter에 둔다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. AD의 현재 의미와 소비자를 승계한 뒤 실제 lifecycle 및 ADR-0032에 따라 superseded 또는 ended-without-successor record로 구분한다. 정확한 source Git bytes와 봉인 provenance를 보존하며 ADR 본문은 decision log에 남긴다.
5. 구현 가능한 계약은 `03.specs/`로 내려보내고 양방향 링크를 유지한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/descriptions/`다.

- 같은 폴더의 AD 문서는 `./`로 시작한다.
- sibling ADR stage는 `../decisions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다.
- 새 AD의 실제 Markdown 링크는 최종 AD 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Current AD Index

| 문서 | 역할 | 문서 상태 | 현재성 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [`./0004-argo-rollouts-progressive-delivery.md`](./0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 참조 아키텍처 | Active | Current-contract backfill. `platform-rollouts` Application, dashboard, metrics, AppProject 경계를 소유한다. | [`../../03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/0004-argo-rollouts-progressive-delivery/spec.md) |
| [`./0005-argo-notifications-slack.md`](./0005-argo-notifications-slack.md) | ArgoCD Notifications Slack 알림 참조 아키텍처 | Active | Current-contract backfill. ArgoCD Notifications와 Vault/ESO credential 경계를 소유한다. | [`../../03.specs/0005-argo-notifications-slack/spec.md`](../../03.specs/0005-argo-notifications-slack/spec.md) |
| [AD-0006](./0006-workspace-agent-governance-platform.md) | Agent·문서·검증 authority 구조 | Active | 현재 Registry와 Stage 00/99, execution/history, native/static/runtime 경계 및 이전 AD 책임 승계. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md), WP-013 미완료 |
| [AD-0007](./0007-current-local-gitops-platform.md) | 로컬 GitOps와 delivery assurance 구조 | Active | Desired-state topology, external interfaces, layered validation, native IaC, revision/namespace evidence; AD-0006과 공통 경계 분리. | [Spec 0047](../../03.specs/0047-current-surface-and-stash-reconciliation/spec.md) 재개; 0048..0051 미완료 |

## Related Documents

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [99.templates AD Template](../../99.templates/templates/architecture/description.template.md)
- [Archive Index](../../98.archive/README.md)
