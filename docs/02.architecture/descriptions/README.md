---
title: "02.architecture/descriptions (AD)"
version: "0.4.2"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-10-03"
layer: "architecture"
---
# 02.architecture/descriptions (AD)

> Requirement Package를 시스템 경계, 품질 속성, 참조 아키텍처로 해석하는 AD stage다.

> [!NOTE]
> 이 stage에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../../.agents/README.md)를 따른다.

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

| 문서 | 현재 책임과 후속 경로 |
| --- | --- |
| [AD-0004](./0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 구조. [SPEC-0004](../../98.archive/completed/03.specs/0004-argo-rollouts-progressive-delivery/spec.md)는 완료된 구현의 역사 근거다. |
| [AD-0005](./0005-argo-notifications-slack.md) | ArgoCD Notifications와 Vault/ESO credential 경계. [SPEC-0005](../../98.archive/completed/03.specs/0005-argo-notifications-slack/spec.md)는 완료된 구현의 역사 근거다. |
| [AD-0006](./0006-workspace-agent-governance-platform.md) | 공통 거버넌스 구조의 현재 소유자. [SPEC-0054 WP-013](../../98.archive/completed/03.specs/0054-sdlc-document-and-agent-governance-consolidation/tasks/tsk-0013-transition-only-taxonomy-terminal-cutover.md)은 2026-09-16 완료되었고 잔여 Stage 03 처분은 [SPEC-0083](../../98.archive/completed/03.specs/0083-finished-package-retention/spec.md)·[SPEC-0084](../../98.archive/completed/03.specs/0084-stage03-backlog-closeout/spec.md)로 승계되었다. |
| [AD-0007](./0007-current-local-gitops-platform.md) | 로컬 GitOps 구조의 현재 소유자이며, 실행 가능한 desired state와 검증기가 구체적인 구현 계약을 소유한다. [SPEC-0008](../../98.archive/completed/03.specs/0008-current-local-gitops-platform/spec.md)은 완료된 구현의 증거다. [REQ-0004-FR-0008·REQ-0004-FR-0010](../../01.requirements/0004-current-local-gitops-platform.md)의 미구현 검증 범위는 계속 열려 있으며, SPEC-0049 철회 후 새 구현 package 소유자가 아직 없다. |

## Add and Find

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 AD는 `../../99.templates/templates/architecture/description.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/descriptions/####-<system-or-domain>.md`다. 안정 ID `AD-####`는 frontmatter에 둔다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. AD의 현재 의미와 소비자를 승계한 뒤 실제 lifecycle에 따라 대체되면 `superseded/`, 후속 없이 철회되면 `retired/`에 원래 profile 그대로 본문을 보존한다([ADR-0040](../decisions/0040-archive-reappraisal-and-verifiable-sources.md)). 원본은 두 번째 복구 원장 없이 Git history가 복구하며, ADR도 예외가 아니다. 기존 봉인 provenance는 동결된 역사 증거로 유지한다.
5. 구현 가능한 계약은 `03.specs/`로 내려보내고 양방향 링크를 유지한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/descriptions/`다.

- 같은 폴더의 AD 문서는 `./`로 시작한다.
- sibling ADR stage는 `../decisions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다.
- 새 AD의 실제 Markdown 링크는 최종 AD 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

## Related Documents

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [99.templates AD Template](../../99.templates/templates/architecture/description.template.md)
- [Archive Index](../../98.archive/README.md)
