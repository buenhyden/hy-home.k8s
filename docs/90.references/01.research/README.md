---
title: "90.references/research"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 90.references/research

## 문서 개요

### 목적과 독자

이 README는 docs/90.references/01.research에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/90.references/01.research의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 연구 팩과 보고서, 출처 기록과 연구 종합을 두는 곳이다.

`01.research/`는 워크스페이스 엔지니어링과 아카이브 보존·출처에 관한 연구 팩을
둔다. 출처에 근거한 발견, 관찰 날짜가 붙은 출처 확인, 종합을
이후의 plan, spec, guide, task가 인용할 수 있는 안정적인 조회 영역이지만
이 폴더가 활성 정책의 소유자가 되지는 않는다.

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

- 연구 팩 색인 자료
- 오래 유지할 출처 원장과 출처 우선순위 메모
- 공식 출처와 저장소 근거 증거 요약
- 분명히 표시한 경우의 비권위 market scan 요약
- `docs/99.templates/02.templates/90.references/research-pack.template.md`로 만든 pack README
- `docs/99.templates/02.templates/90.references/research.template.md`로 만든 보고서

<a id="out-of-scope"></a>

**Out of Scope**

- 활성 거버넌스 정책이나 provider 실행 규칙
- runtime roster 변경, hook 연결, 권한 변경
- live k3d, ArgoCD, OpenBao, ESO, Kubernetes, cloud, provider runtime, secret 검사
- 운영 runbook, release gate, 배포 승인, incident 대응
- 생성되었거나 병행 관리되는 `docs/superpowers/**` 내용

##### Excluded Responsibilities

이 폴더는 활성 거버넌스 정책, runtime 권한, 배포 절차, live cluster 준비 상태, provider 계약을 정의하지 않으며, 이는 계속 `.agents/`, `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/05.operations/`의 정본 소유자가 맡는다. 운영 runbook, release gate, 배포 승인, incident 대응도 범위 밖이다.

#### Current Contents

##### Paths

```text
01.research/
├── 0001-workspace-engineering/
├── 0002-archive-retention-and-provenance/
└── README.md
```

###### Research Pack Index

| Path | Purpose |
| --- | --- |
|   [0001-workspace-engineering/](./0001-workspace-engineering/) | 후속 workspace engineering research pack |
|   [0002-archive-retention-and-provenance/](./0002-archive-retention-and-provenance/) | archive 보존과 출처 research pack |

각 pack README는 보고서별 연구 책임을 안내하는 `## Pack Index`를 소유한다.
보고서의 lifecycle·관찰일은 각 보고서가, 출처·주장·요구사항 대응은 pack의
해당 보고서가 소유한다. 이 collection은 pack 탐색만 안내한다.

현재 research pack은 `01.research/####-<slug>/`에만 있다. 네 자리 번호는 Research
안에서 유일하고 slug는 의미 있는 kebab-case이며 날짜가 아니다. pack 안의 보고서는
registry가 요구하는 `m####-` identity prefix 뒤에 의미 있는 주제 이름을 붙인다.
이 prefix는 identity이지 정렬 키가 아니다. 새 보고서 파일 이름에 `part-*.md`,
날짜, 두 번째 정렬 prefix를 붙이지 않는다.

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

1. research pack 자료를 추가하거나 바꾸기 전에 해당 Spec 패키지(`docs/03.specs/`)가 있으면 그 Plan과 Task를 읽는다.
2. pack README는
   [research-pack.template.md](../../99.templates/02.templates/90.references/research-pack.template.md)로,
   작성하는 보고서는
   [research.template.md](../../99.templates/02.templates/90.references/research.template.md)로 만든다.
3. 주장마다 출처와 관찰 날짜를 기록하고 `Sources`, `Review and Freshness`에서 근거와 갱신 조건을 명시한다. 주장별 출처를 표로 대조할 때는 `Claim-Source Matrix`를 사용한다.
4. market scan 자료보다 공식 문서와 저장소 근거 증거를 우선한다.
5. market 발견은 비권위 자료로 표시하고, 공식 출처나 저장소 근거를 뒤집는 데 쓰지 않는다.
6. 활성 정책, 구현 계약, runbook, task 증거는 여기서 다시 정의하지 말고 각 정본 소유자에게 돌려보낸다.
7. research pack 목록이 바뀌면 이 README의 색인을 갱신한다. 상위 [90.references README](../README.md)의 링크가 영향을 받으면 해당 링크도 갱신한다. 검증 증거는 소유 Task에 기록한다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/90.references/01.research/`다.

- 같은 폴더의 research 참조는 대상 파일이 생긴 뒤에만 `./`를 쓴다.
- 번호가 붙은 pack 참조는 대상 파일이 생긴 뒤 `./####-<slug>/<filename>.md` 형식을 쓴다.
- 상위 reference로 가는 링크는 `../README.md`를 쓴다.
- 정본 소유 stage는 `../../../.agents/`, `../../01.requirements/`, `../../02.architecture/`, `../../03.specs/`, `../../05.operations/`를 쓴다.
- 이 collection README에서 저장소 최상위 소스를 가리킬 때는 `../../../<path>`를 쓴다.
- pack README와 member는 한 단계 더 깊으므로 저장소 최상위에 `../../../../<path>`, stage에 `../../../<stage>/`를 쓴다. 최종 파일 위치에서 상대 경로를 계산한다.
- 선택 사항이거나 계획 중인 대상 경로는 대상이 생길 때까지 code literal로 둔다.

###### Source Priority

연구 출처끼리 어긋나면 다음 우선순위를 따른다.

1. 로컬 정책, 계약, task, 운영에 대해서는 저장소의 정본 소유자
2. 외부 사실에 대해서는 제품, provider, 표준, upstream 프로젝트의 공식 문서
3. 커밋된 manifest, 스크립트, 설정, template 같은 저장소 근거 증거
4. 현재 동작을 밝혀 줄 때의 공식 issue tracker, release note, 구현 저장소
5. market scan, vendor 마케팅, 블로그, 포럼, benchmark, 비교 자료

market scan 발견은 권위가 없다. 맥락, 지형, 용어를 파악하는 데 참고할 수는
있지만 market scan 자료라고 표시해야 하며 공식 문서, 저장소 근거 증거, 저장소의
정본 소유자를 뒤집을 수 없다.

###### Upstream and Downstream

- [90.references README](../README.md)
- [Agent Governance Hub](../../../.agents/README.md)
- [Reference Maintenance Runbook](../../00.workspace/06.maintenance/0011-reference-maintenance-runbook.md)

###### Policy and Templates

- [Research Reference Template](../../99.templates/02.templates/90.references/research.template.md)
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
