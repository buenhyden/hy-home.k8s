---
title: "90.references"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 90.references

## 문서 개요

### 목적과 독자

이 README는 docs/90.references에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/90.references의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 감사, 외부 조사, 데이터 등 비권위 참고 자료를 관리한다.

`docs/90.references/`는 워크스페이스와 관련된 출처 기반 참고 자료를 둔다.
이 Stage는 요구사항, 아키텍처, 구현 명세, 운영 절차, Agent 정책을 정의하거나
대체하지 않는다. 현재 실행 동작과 버전 값은 Stage 01/02 문서 및 실제
매니페스트·설정·잠금 파일이 소유한다.

###### Inputs and Outputs

<a id="out-of-scope"></a>

**Out of Scope**

- AI Agent governance, role, skill, provider, permission, runtime policy
- 제품 요구사항, 현재 아키텍처, 구현 계약, 실행 Task 증거
- 운영 Guide, Policy, Runbook, Incident, Postmortem
- 배포 승인, live mutation, secret-bearing procedure
- 매니페스트·설정·잠금 파일을 복제한 현재 버전 인벤토리
- generated wiki, redirect, 이전 본문 복제본, 영구 corpus census
- `audits/`, `data/`, `research/` 밖의 느슨한 authored reference

Stage 90 자료는 공통 거버넌스(`.agents/`)와 현재 Stage 01/02/03/05 owner를
인용할 수 있지만,
Stage 98의 문서나 파일을 인용하거나 cross-link하지 않는다. 일반 처분의
본문 복구는 Git history가 담당한다. 승인된 최종 전환 대상의 처분은
[문서 수명주기 정책](../00.workspace/03.process/document-lifecycle.md#rules)을 따른다.

##### Excluded Responsibilities

이 stage는 요구사항, 아키텍처, 구현 명세, 운영 절차, Agent 정책을 정의하거나 대체하지 않으며, 현재 실행 동작과 버전 값은 Stage 01/02 문서 및 실제 매니페스트·설정·잠금 파일이 소유한다. AI Agent governance, 운영 Guide·Policy·Runbook·Incident, 배포 승인, live mutation, secret-bearing procedure도 이 stage 밖에 있다. Stage 98의 문서나 파일은 인용하거나 cross-link하지 않는다.

#### Current Contents

##### Paths

```text
docs/90.references/
├── audits/
├── data/
├── research/
├── AGENTS.md
├── CLAUDE.md
└── README.md
```

| Path | Purpose |
| --- | --- |
| [02.audits/](./02.audits/) | 감사 pack collection |
| [03.data/](./03.data/) | 데이터 pack collection |
| [01.research/](./01.research/) | 외부 조사 pack collection |
| [AGENTS.md](./AGENTS.md) | 이 stage에 적용되는 AI 에이전트 지시 |
| [CLAUDE.md](./CLAUDE.md) | Claude가 이 stage의 `AGENTS.md`를 불러오게 하는 한 줄 `@AGENTS.md` import |

세 collection은 동일한 3단 구조를 따른다: collection router `README.md`,
pack router `####-<slug>/README.md`, 그리고 pack member `####-<slug>/m####-<slug>.md`.
각 collection README가 자신의 pack을, 각 pack README가 자신의 member와 연구
책임을 안내한다. 관찰일·lifecycle·주장·coverage는 해당 보고서가 소유하며
라우터는 이를 중복 관리하지 않는다.

##### Owners

###### In Scope

| Category | Purpose | Required boundary |
| --- | --- | --- |
| Audit | 특정 시점의 저장소 상태를 출처와 함께 비교한 비권위 감사 | 관찰일, 범위, 증거, 미확인 항목을 명시한다. |
| Research | 외부 공식 자료와 저장소 증거를 종합한 조사 | 출처, 확인일, freshness trigger, 추론 한계를 명시한다. |
| Data | 독립적인 참고 가치가 있는 bounded dataset 또는 lookup material | 생성·수집 출처와 갱신 책임을 명시하고 실행 입력으로 승격하지 않는다. |

#### Usage

##### Entry Points

1. 새 자료가 정책·요구·설계·절차·실행 증거를 정의하는지 확인하고, 그렇다면
   공통 거버넌스와 Stage 01/02/03/05의 canonical owner에 작성한다.
2. Reference로 유지할 자료는 고유 목적, provenance, observation date,
   authority boundary, freshness trigger, 현재 consumer를 확인한다.
3. 현재 pack은 `audits/####-<slug>/`, `data/####-<slug>/`,
   `research/####-<slug>/` 중 하나에만 둔다. `####`는 category 안에서 고유한
   네 자리 번호이고 `<slug>`는 날짜가 아닌 의미 기반 kebab-case 이름이다.
4. pack `README.md`는 category와 일치하는
   [Audit](../99.templates/02.templates/90.references/audit-pack.template.md),
   [Data](../99.templates/02.templates/90.references/data-pack.template.md), 또는
   [Research](../99.templates/02.templates/90.references/research-pack.template.md)
   template을 사용한다. 내부 report는 같은 family의
   [Audit Reference](../99.templates/02.templates/90.references/audit.template.md),
   [Data Reference](../99.templates/02.templates/90.references/data.template.md),
   [Research Reference](../99.templates/02.templates/90.references/research.template.md)
   template을 사용한다. 관찰일은 frontmatter 또는 source metadata에만 둔다.
5. 목록이나 링크가 바뀌면 이 router와 category router를 같은 변경에서 갱신한다.
   일반 처분과 승인된 최종 전환은 위 수명주기 정책을 따른다.
6. 참조 자료를 실행 입력이나 중복 control plane으로 사용하지 않는다.
7. [일반 문서 변경의 검사 선택](../00.workspace/04.quality/quality.md#ordinary-document-selection)에
   따라 변경 문서의 형식, 관계, 링크와 수명주기 상태를 확인한다.
   경로나 제목 앵커의 이동·삭제가 기존 참조에 영향을 주면 해당 대상을
   인용하는 문서의 링크도 검사한다.

###### Upstream and Downstream

- [Docs Hub](../README.md)
- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Specs](../03.specs/README.md)
- [Operations](../05.operations/README.md)
- [Reference Maintenance Runbook](../00.workspace/06.maintenance/0011-reference-maintenance-runbook.md)

###### Policy and Templates

- [Agent Governance Hub](../../.agents/README.md)
- [Research Reference Template](../99.templates/02.templates/90.references/research.template.md)

##### Checks

전이와 종료: 해당 없음 — 이 stage README는 상태 전이나 종료 규칙을 따로 두지 않는다.

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
