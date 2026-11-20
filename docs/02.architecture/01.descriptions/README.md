---
title: "02.architecture/descriptions (AD)"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 02.architecture/descriptions (AD)

## 문서 개요

### 목적과 독자

이 README는 docs/02.architecture/01.descriptions에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/02.architecture/01.descriptions의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 제품(로컬 k8s GitOps 플랫폼) Requirement Package를 시스템 경계, 품질 속성, 참조 아키텍처로 해석하는 AD collection이다.

작업 시스템 AD(AD-0006)는 [작업 시스템 descriptions](../../00.workspace/02.architecture/01.descriptions/README.md)가 소유한다.

이 경로는 Requirement Package를 시스템 경계, 품질 속성, 데이터 흐름,
보안·관측성·운영성 관점으로 해석하는 AD(Architecture Description) stage다.
여기서 정의한 아키텍처 관점은 ADR과 Spec의 상위 입력으로 사용된다.

AD는 참조 아키텍처와 품질 속성을 설명한다. 단일 기술 선택 자체는 `../02.decisions/`의 ADR에 남기고,
파일 단위 구현 설계나 운영 명령 절차는 각각 `../../03.specs/`, `../../05.operations/`로 넘긴다.

###### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Documentation Writers

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 시스템 경계와 책임
- 품질 속성, 데이터 흐름, 보안/관측성/운영성 요구
- 참조 아키텍처와 하위 ADR/Spec 링크

<a id="out-of-scope"></a>

**Out of Scope**

- 단일 기술 결정 기록
- 세부 구현 파일 설계
- 운영 명령 절차

##### Excluded Responsibilities

이 collection은 단일 기술 결정 기록, 세부 구현 파일 설계, 운영 명령 절차를 소유하지 않는다. 단일 기술 선택은 `../02.decisions/`의 ADR에 남기고, 파일 단위 구현 설계와 운영 명령 절차는 각각 `../../03.specs/`, `../../05.operations/`로 넘긴다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [AD-0004](./0004-argo-rollouts-progressive-delivery.md) | Argo Rollouts 점진적 배포 구조. Argo Rollouts 구조의 소유자다. |
| [AD-0005](./0005-argo-notifications-slack.md) | ArgoCD Notifications와 OpenBao/ESO credential 경계. Notifications 구조의 소유자다. |
| [AD-0006](../../00.workspace/02.architecture/01.descriptions/0006-workspace-agent-governance-platform.md) | 공통 거버넌스 구조의 현재 소유자다. 이전 Spec package는 삭제되었고 Archived Lineage가 요약한다. |
| [AD-0007](./0007-current-local-gitops-platform.md) | 로컬 GitOps 구조의 현재 소유자이며, 실행 가능한 desired state와 검증기가 구체적인 구현 계약을 소유한다. |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

1. 관련 `01.requirements/` 문서를 먼저 읽어 요구사항 경계를 고정한다.
2. 새 AD는 `../../99.templates/02.templates/02.architecture/description.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/01.descriptions/####-<system-or-domain>.md`다. 안정 ID `AD-####`는 frontmatter에 둔다.
3. 주요 설계 결정은 `02.architecture/02.decisions/`에 별도 ADR로 연결한다.
4. 구현 계약은 `03.specs/`에 두고, 그 계약을 작성하는 Spec에서 관련 AD를 인용한다. 역방향 탐색은 이 관계에서 파생한다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/01.descriptions/`다.

- 같은 폴더의 AD 문서는 `./`로 시작한다.
- sibling ADR stage는 `../02.decisions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다.
- 새 AD의 실제 Markdown 링크는 최종 AD 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

###### Upstream and Downstream

- [Architecture README](../README.md)
- [01.requirements](../../01.requirements/README.md)
- [02.architecture/decisions](../02.decisions/README.md)
- [03.specs](../../03.specs/README.md)
- [Archive Index](../../98.archive/README.md)

###### Policy and Templates

- [99.templates AD Template](../../99.templates/02.templates/02.architecture/description.template.md)

##### Checks

1. ADR 전체를 대체할 때는 후속 ADR의 `supersedes`와 Traceability가 이전 ID를 유지하고 AD Archived Lineage가 요약한다. 삭제 전에는 [문서 수명주기 정책](../../00.workspace/03.process/document-lifecycle.md)의 처분 조건을 확인한다. 일부 조항만 개정할 때는 기존 ADR을 보존하고 후속 ADR의 Traceability에 개정 범위를 적는다([ADR-0055](../../00.workspace/02.architecture/02.decisions/0055-governance-decision-current-state-amendment.md)).

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
