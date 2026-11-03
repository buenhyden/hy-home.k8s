---
title: "02.architecture/descriptions (AD)"
version: "0.6.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-28"
layer: "architecture"
---
# 02.architecture/descriptions (AD)

> Requirement Package를 시스템 경계, 품질 속성, 참조 아키텍처로 해석하는 AD stage다.

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

## Scope

### In Scope

- 시스템 경계와 책임
- 품질 속성, 데이터 흐름, 보안/관측성/운영성 요구
- 참조 아키텍처와 하위 ADR/Spec 링크

### Out of Scope

- 단일 기술 결정 기록
- 세부 구현 파일 설계
- 운영 명령 절차

## Structure

| Path | Purpose |
| --- | --- |
| [AD-0004](./0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 구조. Argo Rollouts 구조의 소유자다. |
| [AD-0005](./0005-argo-notifications-slack.md) | ArgoCD Notifications와 Vault/ESO credential 경계. Notifications 구조의 소유자다. |
| [AD-0006](./0006-workspace-agent-governance-platform.md) | 공통 거버넌스 구조의 현재 소유자다. 이전 Spec package는 삭제되었고 Archived Lineage가 요약한다. |
| [AD-0007](./0007-current-local-gitops-platform.md) | 로컬 GitOps 구조의 현재 소유자이며, 실행 가능한 desired state와 검증기가 구체적인 구현 계약을 소유한다. |

## Usage

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 AD는 `../../99.templates/templates/architecture/description.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/descriptions/####-<system-or-domain>.md`다. 안정 ID `AD-####`는 frontmatter에 둔다.
3. 주요 설계 결정은 `02.architecture/decisions/`에 별도 ADR로 연결한다.
4. 대체된 ADR의 ID는 후속 ADR의 `supersedes`와 Traceability가 유지하고, AD Archived Lineage가 요약하며, 같은 변경에서 삭제한다. 원본은 Git history가 복구한다([ADR-0053](../decisions/0053-unvalidated-archive.md)).
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
