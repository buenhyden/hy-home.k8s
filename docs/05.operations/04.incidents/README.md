---
title: "05.operations/incidents"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---
# 05.operations/incidents

## 문서 개요

### 목적과 독자

이 README는 docs/05.operations/04.incidents에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/05.operations/04.incidents의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 사고 사실 기록과 postmortem을 보관하는 incident stage다.

이 경로는 사고 사실 기록과 사고 후 회고를 보관하는 canonical stage다.
실시간 대응 기록과 구조적 재발 방지 분석을 같은 stage 안에서 분리해 보존한다.

Incident Record는 “무슨 일이 있었는가”를 기록한다.
Postmortem은 “왜 허용됐고 무엇을 바꿀 것인가”를 기록한다.
일반 정책은 [policies](../02.policies/README.md), 실행 복구 절차는 [runbooks](../03.runbooks/README.md)에 둔다.

현재 tracked incident record와 postmortem 문서는 없다.
첫 사고 기록이 필요할 때만 `<year>/inc-####-<slug>/` 하위 경로를 만든다.
Incident Record와 Postmortem은 각각 고정 basename `incident.md`와
`postmortem.md`를 사용한다.

###### Collection Readers

이 README의 주요 독자:

- Operators
- Incident Commanders
- Platform Engineers

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- Incident Record: 영향, 타임라인, 관찰된 사실, 대응, 증거, 후속 액션
- Postmortem: 근본 원인, 기여 요인, 감지 공백, 재발 방지 액션
- 관련 Runbook, Operation, ADR, Spec 링크

<a id="out-of-scope"></a>

**Out of Scope**

- 일반 운영 정책
- 실행 절차 중심 런북
- 기능 요구사항 또는 상세 설계

##### Excluded Responsibilities

이 collection은 일반 운영 정책, 실행 절차 중심 런북, 기능 요구사항 또는 상세 설계를 소유하지 않는다. 일반 정책은 policies에, 실행 복구 절차는 runbooks에 둔다. 현재 tracked incident record와 postmortem 문서는 없으며, 첫 사고 기록이 필요할 때만 `<year>/inc-####-<slug>/` 하위 경로를 만든다.

#### Current Contents

##### Paths

```text
05.operations/04.incidents/
├── <year>/
└── README.md
```

사고 기록은 `<year>/inc-####-<slug>/` 폴더에 두며, 그 안의 `incident.md`가
사실 기록을, 분석이 필요할 때만 만드는 `postmortem.md`가 사후 분석을 소유한다.

| Path | Purpose |
| --- | --- |

##### Owners

###### Incident Boundary Matrix

| Artifact | Path rule | Template | Creation rule | Current state |
| --- | --- | --- | --- | --- |
| `Incident Record` | `./<year>/inc-####-<slug>/incident.md` | [incident.template.md](../../99.templates/02.templates/05.operations/incident.template.md) | Create only for a real incident fact record. | No tracked incident records. |
| `Postmortem` | `./<year>/inc-####-<slug>/postmortem.md` | [postmortem.template.md](../../99.templates/02.templates/05.operations/postmortem.template.md) | Create only after incident stabilization when root cause/prevention analysis is needed. | No tracked postmortems. |

#### Usage

##### Entry Points

1. 대응 중에는 [incident.template.md](../../99.templates/02.templates/05.operations/incident.template.md)로 사실 기록을 시작한다.
2. Incident Record는 `<year>/inc-####-<slug>/incident.md`로 작성하고 frontmatter `artifact_id`를 `inc-<NNNN>-<NNNN>` 형식으로 기록한다.
3. 사고 종료 후 구조 분석이 필요하면 [postmortem.template.md](../../99.templates/02.templates/05.operations/postmortem.template.md)를 사용하고 `artifact_id`를 `inc-<NNNN>-<NNNN>-PM` 형식으로 기록한다.
4. Runbook/Policy/ADR/Spec 링크를 남겨 재발 방지 액션을 추적한다.
5. 비밀 값, 토큰, 개인 식별 정보는 사고 기록에 직접 남기지 않는다.
6. 사고가 없는 상태에서는 README만 유지하고 빈 placeholder 파일을 만들지 않는다.

###### Record Purpose

이 영역은 운영 중 학습과 대응 기록을 저장한다.

- Incident Record는 장애 또는 이상 상황에서 무엇이 발생했는지, 영향 범위가 무엇인지, 즉시 어떤 대응을 했는지 기록한다.
- Postmortem은 사건 이후 근본 원인, 기여 요인, 재발 방지 조치, 학습 내용을 정리한다.

###### Expected Record Shape

Incident Record는 다음 항목을 포함한다.

- Impact: Affected Users, Observed Scope(그 아래 H4 Event, Current Status)
- Response: Timeline(그 아래 H4 Decisions), Actions
- Resolution: Verified State, Remaining Work(그 아래 H4 Evidence Sources), Lifecycle Traceability

Postmortem은 다음 항목을 포함한다.

- Facts: Timeline(그 아래 H4 Review Scope), Impact(그 아래 H4 Detection and Response), 선택 항목인 What Went Well
- Causes: Contributing Factors(그 아래 H4 Causal Analysis와 What Went Wrong), Uncertainty
- Actions: Prevention, Owners and Checks(그 아래 H4 Source Records, Review Decision), Lifecycle Traceability

###### Review Expectations

- Incident는 사실 기록과 대응 경위를 빠르게 복원할 수 있어야 한다.
- Postmortem은 비난보다 학습과 재발 방지에 초점을 맞춘다.
- 후속 조치는 Plan 또는 Task와 연결하고, 관련 Policy/Runbook 갱신 필요 여부를 확인한다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/05.operations/04.incidents/`다.

- Incident record는 `./<year>/inc-####-<slug>/incident.md` 경로를 사용한다.
- Postmortem은 같은 incident 폴더의 `./<year>/inc-####-<slug>/postmortem.md` 경로를 사용한다.
- sibling operations folder는 `../02.policies/`, `../03.runbooks/`, `../01.guides/`로 연결한다.

###### Upstream and Downstream

- [Operations README](../README.md)
- [05.operations/policies](../02.policies/README.md)
- [05.operations/runbooks](../03.runbooks/README.md)

###### Policy and Templates

- [99.templates](../../99.templates/README.md)
- [Incident Template](../../99.templates/02.templates/05.operations/incident.template.md)
- [Postmortem Template](../../99.templates/02.templates/05.operations/postmortem.template.md)

##### Checks

1. Incident status는 `detected → investigating → mitigated → resolved` 순서를 따르고, 역할·다음 checkpoint·종료 근거를 함께 갱신한다.
2. Postmortem status는 `draft → in-review → published`를 따르며 action closure evidence 없이 완료를 선언하지 않는다.

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
