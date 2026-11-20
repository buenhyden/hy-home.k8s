---
title: "90.references/data"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 90.references/data

## 문서 개요

### 목적과 독자

이 README는 docs/90.references/03.data에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/90.references/03.data의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 오래 유지할 data pack, 그 dataset, dataset 출처를 두는 곳이다.

`data/`는 오래 유지할 dataset 자료를 둔다. 저장소가 의존하는 데이터의 형태와
출처, 각 스냅샷을 수집한 방법, 갱신·보존 경계가 여기에 해당한다. 이후의 plan,
spec, guide, task가 인용할 수 있는 안정적인 조회 영역이다. 그렇다고 이 폴더가
활성 정책의 소유자가 되지는 않는다.

이 폴더는 활성 거버넌스 정책, runtime 권한, 배포 절차, live cluster 준비 상태,
provider 계약을 정의하지 않는다. 이것들은 계속 `.agents/`,
`docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`,
`docs/05.operations/`의 정본 소유자가 맡는다.

###### Collection Readers

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- data pack 색인 자료
- dataset의 형태, 출처, 수집 방법 기록
- 갱신·보존 경계를 명시한, 관찰 날짜가 붙은 스냅샷
- `docs/99.templates/02.templates/90.references/data-pack.template.md`로 만든 pack README
- `docs/99.templates/02.templates/90.references/data.template.md`로 만든 dataset

<a id="out-of-scope"></a>

**Out of Scope**

- 활성 거버넌스 정책이나 provider 실행 규칙
- runtime roster 변경, hook 연결, 권한 변경
- live k3d, ArgoCD, OpenBao, ESO, Kubernetes, cloud, provider runtime, secret 검사
- secret 값, credential, 가리지 않은 민감 기록
- 운영 runbook, release gate, 배포 승인, incident 대응

##### Excluded Responsibilities

이 폴더는 활성 거버넌스 정책, runtime 권한, 배포 절차, live cluster 준비 상태, provider 계약을 정의하지 않으며, 이는 계속 `.agents/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`의 정본 소유자가 맡는다. secret 값, credential, 가리지 않은 민감 기록과 운영 runbook, release gate, 배포 승인, incident 대응도 범위 밖이다.

#### Current Contents

##### Paths

```text
data/
└── README.md                          # This file
```

이 collection은 현재 data pack을 보유하지 않는다. 이는 현재 처분 결과일 뿐이며,
고유한 목적과 출처 경계를 갖춘 data pack의 추가를 금지하지 않는다.

| Path | Purpose |
| --- | --- |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

1. data pack 자료를 추가하거나 바꾸기 전에 해당 Spec 패키지(`docs/03.specs/`)가 있으면 그 Plan과 Task를 읽는다.
2. `data/####-<slug>/README.md`는
   [data-pack.template.md](../../99.templates/02.templates/90.references/data-pack.template.md)로 만들고,
   작성하는 dataset는 `data/####-<slug>/m####-<slug>.md` 경로에
   [data.template.md](../../99.templates/02.templates/90.references/data.template.md)로 만든다.
3. pack 멤버에는 pack 내부의 `m####` 번호를 매기고, 각 dataset에는 소속 pack의
   `DATA-####-m####` artifact identity를 붙인다.
4. 모든 스냅샷에 수집 날짜, 방법, 보존 경계를 기록하고 secret 값은 절대 저장하지 않는다.
5. 활성 정책, 구현 계약, runbook, task 증거는 여기서 다시 정의하지 말고 각 정본 소유자에게 돌려보낸다.
6. data pack 목록이 바뀌면 이 README의 색인을 갱신한다. 상위 [90.references README](../README.md)의 링크가 영향을 받으면 해당 링크도 갱신한다. 검증 증거는 소유 Task에 기록한다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/03.data/`다.

- 번호가 붙은 pack 참조는 대상 파일이 생긴 뒤 `./####-<slug>/<filename>.md` 형식을 쓴다.
- 상위 reference로 가는 링크는 `../README.md`를 쓴다.
- 정본 소유 stage는 `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, `../../05.operations/`를 쓴다.
- pack README와 멤버에서 저장소 최상위 소스를 가리킬 때는 `../../../../<path>`를 쓴다.
- 선택 사항이거나 계획 중인 대상 경로는 대상이 생길 때까지 code literal로 둔다.

###### Upstream and Downstream

- [90.references README](../README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../00.workspace/06.maintenance/0011-reference-maintenance-runbook.md)

###### Policy and Templates

- [Data Pack Template](../../99.templates/02.templates/90.references/data-pack.template.md)
- [Data Reference Template](../../99.templates/02.templates/90.references/data.template.md)
- [Templates README](../../99.templates/README.md)

##### Checks

이 README는 상태 전환·승격·종료 규칙을 따로 정하지 않는다.

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
