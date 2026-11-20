---
title: "02.architecture"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 02.architecture

## 문서 개요

### 목적과 독자

이 README는 docs/02.architecture에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/02.architecture의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 제품(로컬 k8s GitOps 플랫폼)의 요구를 아키텍처 구조와 결정 기록으로 연결하는 canonical architecture stage다.

작업 방식 자체(문서 계약, 에이전트 거버넌스, QA·CI, Git·릴리스, 문서 처분)의 구조와 결정은
[작업 시스템 architecture](../00.workspace/02.architecture/README.md)가 소유한다. 이 stage는 클러스터,
GitOps, 네트워크, 보안, 시크릿, 관측 같은 제품 구조와 결정만 둔다.

`02.architecture/`는 요구사항을 시스템 구조와 의사결정으로 연결하는 아키텍처 허브다.
Architecture Description은 `01.descriptions/`에, 결정 기록은 `02.decisions/`에 둔다.

이 stage는 현재 구조와 결정을 보존한다.
[`gitops/`](../../gitops/)와 [`정적 계약 검사`](../../scripts/validate-infrastructure-contracts.sh)는
선언된 구현과 검사 범위의 근거다. 요구와 구현이 다르면
[SDLC의 충돌 해결 순서](../00.workspace/03.process/sdlc.md#requirements)에 따라
현재 사용자 요구와 승인된 계약을 기준으로 해당 소유자에서 바로잡는다. ADR을 포함해 더 이상 현재가 아닌 문서는 current consumer와 의미를
승계한 뒤 이 stage를 떠난다. Architecture Description의 Archived Lineage 표에 요약하고 [문서 수명주기 정책](../00.workspace/03.process/document-lifecycle.md)에 따른 처분 전 확인을 거쳐 삭제한다. 원본은 확인된 Git 이력에서 복구한다([ADR-0053](../00.workspace/02.architecture/02.decisions/0053-unvalidated-archive.md)). Stage 98은
검증하지 않는 기록 보관소이며 현재 실행 권위가 아니다.

###### Stage Readers

- Platform Engineers
- GitOps Operators
- Architecture Reviewers

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 시스템 경계, 품질 속성, 배포 구조, 데이터/인프라 관점의 요구사항
- 선택지, 결정 근거, 결과를 남기는 Architecture Decision Record
- Requirement Package, Spec, Plan, Operations 문서로 이어지는 추적 링크

<a id="out-of-scope"></a>

**Out of Scope**

- 제품 요구사항 원문
- 파일 단위 구현 명세
- 실행 순서와 작업 증적
- 반복 운영 절차

##### Excluded Responsibilities

이 stage는 제품 요구사항 원문, 파일 단위 구현 명세, 실행 순서와 작업 증적, 반복 운영 절차를 소유하지 않는다. 상세 구현 계약은 `../03.specs/`로, 운영 정책이나 복구 절차는 `../05.operations/`로 넘긴다. 구현 선언은 `gitops/`와 정적 검증 소스에서 확인하되, 요구와의 불일치는 SDLC 소유자가 정한 순서로 해결한다. 더 이상 현재가 아닌 문서는 현재 실행 권위가 아니다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [01.descriptions/](./01.descriptions/) | Architecture Description과 참조 모델 |
| [02.decisions/](./02.decisions/) | 아키텍처 결정 기록(ADR) |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

##### Owners

###### Reader Route

| 찾는 것 | 먼저 볼 위치 | 판단 기준 |
| --- | --- | --- |
| 현재 외부 서비스 host 주소·gateway hostname, Headlamp, network policy 계약 | [`gitops/platform/external-services/`](../../gitops/platform/external-services/), [`gitops/platform/network-policies/`](../../gitops/platform/network-policies/), [`validate-infrastructure-contracts.sh`](../../scripts/validate-infrastructure-contracts.sh) | 현재 선언과 검사 범위를 확인한다. 요구와의 불일치는 SDLC 충돌 해결 순서를 따른다. |
| 시스템 경계와 품질 속성 | [`01.descriptions/`](./01.descriptions/) | AD는 Requirement Package를 현재 구조와 참조 모델로 해석한다. |
| 기술 선택과 현재 decision record | [`02.decisions/`](./02.decisions/) | ADR은 현재 구현 기준의 결정, 대안, 결과를 보존한다. |
| 구현자가 따라야 할 계약 | [`../03.specs/`](../03.specs/) | 파일/manifest/API 수준 상세 설계는 Spec stage가 소유한다. |
| 운영 정책과 복구 절차 | [`../05.operations/`](../05.operations/) | 실행 절차, 정책, runbook은 Operations stage가 소유한다. |

#### Usage

##### Entry Points

1. 요구사항을 시스템 경계와 품질 속성으로 확장할 때는 `01.descriptions/`를 갱신한다.
2. 기술 선택이나 운영 모델 결정은 `02.decisions/`에 ADR로 기록한다.
3. AD target은 `docs/02.architecture/01.descriptions/####-<system-or-domain>.md`, ADR target은 `docs/02.architecture/02.decisions/####-<short-title>.md`를 따른다. 유형은 부모 폴더가 결정하고 안정 ID는 frontmatter의 `AD-####`/`ADR-####`로 유지한다.
4. 구현자가 따라야 할 상세 계약은 `../03.specs/`로 넘긴다.
5. 운영 정책이나 복구 절차는 `../05.operations/`로 넘긴다.
6. Architecture Description에는 arc42의 목적별 구조를 비례적으로 적용하고,
   C4 System Context/Container를 우선 검토한다. Component·Dynamic·Deployment
   view는 실제 이해 가치가 있을 때만 사용하며, Kubernetes manifest와 GitOps
   desired state를 문서 본문에 복제하지 않는다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/`다.

- 하위 아키텍처 폴더는 `./01.descriptions/`, `./02.decisions/`로 연결한다.
- 인접 stage는 `../01.requirements/`, `../03.specs/`, `../05.operations/`로 연결한다.
- root-level 구현 경로는 `../../gitops/`, `../../infrastructure/`처럼 repository root 기준으로 올라간다.
- AD/ADR 문서 안의 링크는 각 하위 폴더의 최종 문서 위치 기준으로 다시 계산한다.
- AD는 자신이 다루는 Requirement의 각 member를 `Lifecycle Traceability`의 `Upstream requirement` 열에서 인용한다. Requirement는 downstream 링크 열을 두지 않으며, 인용되지 않은 member는 `REQUIREMENT-COVERAGE` 검사가 거부한다.

###### Upstream and Downstream

- [Requirements README](../01.requirements/README.md)
- [Architecture Descriptions](./01.descriptions/README.md)
- [Architecture Decisions](./02.decisions/README.md)
- [Specs README](../03.specs/README.md)
- [Operations README](../05.operations/README.md)
- [Archive Index](../98.archive/README.md)

###### Policy and Templates

- [Document Stage Routing](../00.workspace/03.process/document-authoring.md)
- [Templates README](../99.templates/README.md)

##### Checks

1. ADR 전체를 대체할 때는 후속 ADR의 `supersedes`와 Traceability가 이전 ID를 유지하고 AD Archived Lineage가 요약한다. 삭제 전에는 [문서 수명주기 정책](../00.workspace/03.process/document-lifecycle.md)의 처분 조건을 확인한다. 일부 조항만 개정할 때는 기존 ADR을 보존하고 후속 ADR의 Traceability에 개정 범위를 적는다.

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
