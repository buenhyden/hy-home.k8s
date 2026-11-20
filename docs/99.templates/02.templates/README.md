---
title: "99.templates/02.templates"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 99.templates/02.templates

## 문서 개요

### 목적과 독자

이 카탈로그는 현재 문서 양식을 찾고 작성하는 저자를 위한 안내다.

### 책임과 적용 범위

platform은 이 카탈로그의 경로 안내를 유지하며, 정확한 profile과 계약은 아래에 연결된 Registry가 소유한다.

## 내용 계약

### 입력과 전제

작성할 문서의 경로와 Registry profile을 먼저 확인한다.

### 본문과 규칙


#### Responsibility

##### Purpose

이 디렉터리는 저장소가 인정하는 모든 authored 문서의 physical form을 담는다.
Form directory는 navigation을 위해 physical responsibility surface별로 묶고,
파일 이름은 그 form이 만드는 문서 kind를 말한다. Directory 이름은 Registry profile
family를 정의하지 않는다. 예를 들어 `specs/plan.template.md`는 `sdlc/plan`
profile의 form이다. Form은 계약을 정의하지 않는다. 공통 외피와 역할별 종류는
[common document contract](../01.contracts/common-document-contract.json)가,
profile별 경로·상태·역할별 payload는 [registry](../registry.json)와
[frontmatter schema](../01.contracts/frontmatter.schema.json)가
소유하고, form은 그 계약을 저자가 채울 수 있는 모양으로 보여줄 뿐이다.

###### Inputs and Outputs

<a id="in-scope"></a>
**In Scope**

- 각 profile이 소유하는 physical form 파일
- 저자가 채워야 할 값의 placeholder와 `작성 규칙` 안내

<a id="out-of-scope"></a>
**Out of Scope**

- profile 선택 규칙, key 문법, lifecycle 상태 (registry와 schema가 소유)
- 완성된 문서의 예시나 사본
- form 디렉터리별 README (이 카탈로그 하나만 둔다)

##### Excluded Responsibilities

이 디렉터리는 profile 선택 규칙, key 문법, lifecycle 상태를 소유하지 않으며, 이는 [registry](../registry.json)와 [frontmatter schema](../01.contracts/frontmatter.schema.json)가 소유한다. 완성된 문서의 예시나 사본도 두지 않고, form 디렉터리별 README도 따로 두지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| [00.workspace/](./00.workspace/) | vocabulary (workspace 공통 어휘) |
| [01.requirements/](./01.requirements/) | requirement-package |
| [02.architecture/](./02.architecture/) | decision, description |
| [03.specs/](./03.specs/) | spec, plan, task |
| [05.operations/](./05.operations/) | guide, incident, policy, postmortem, runbook |
| [90.references/](./90.references/) | audit·data·research 의 pack form과 reference form |
| [91.agent-governance/](./91.agent-governance/) | knowledge, prompt, role, skill |
| [92.runtime/](./92.runtime/) | provider, claude-agent (Markdown), claude-command (Markdown), codex-agent (TOML) |
| [93.common/](./93.common/) | rule (W·A 정책 공통), repository, stage-index, collection-index, implementation, workspace-staging, runtime-governance entrypoint README form |
| [94.evaluations/](./94.evaluations/) | evaluation-task.template.md, evaluation-score.template.md, evaluation-results.template.md |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

1. 만들려는 문서의 경로로 [registry](../registry.json)에서 profile을 하나만
   해석하고, 그 profile이 지정한 form을 읽는다.
2. 새 form은 그 form이 만드는 문서 이름으로 짓고, 기존 physical responsibility
   grouping에 두며, 디렉터리 이름을 파일 이름에 반복하지 않는다. Profile family와
   form 경로의 대응은 Registry에 명시한다.
3. 새 form은 Registry의 "template_source"와
   "relationships.source_profile_ids"에 명시적으로 연결한다. source가 없는
   required form, 소유 profile이 없는 form, 암묵적 공유 form은 계약 위반이다.
   각 form에는 `mode: template`인 `common/template-*` profile이 하나씩 있으며,
   그 profile이 원본 profile을 source로 가리킨다. native Codex TOML도
   `common/template-exception-provider-native-codex` profile을 가진다.
4. 확장자는 그 form을 읽는 런타임이 읽는 확장자를 쓴다.
   Native Markdown form은 공통 외피 안의 단일 `native-payload` fence에서
   원문을 추출하고, 실제 provider 출력에는 이 외피를 넣지 않는다.

###### Upstream and Downstream

- [Stage 99 README](../README.md)

###### Policy and Templates

- [Document Profile Registry](../registry.json)
- [Frontmatter Schema](../01.contracts/frontmatter.schema.json)
- [Document Authoring Policy](../../00.workspace/03.process/document-authoring.md)

##### Checks

이 README는 상태, 승격, 종료 규칙을 따로 두지 않는다. 그런 규칙을 두게 되면 여기에 적는다.

## 적용과 확인

### 적용 방법

아래 Entry Points 절에서 profile과 form을 선택한다.

### 확인 기준

선택한 form의 template profile과 Registry 연결을 엄격 검증한다.

## 관계와 출처

### 관련 문서

아래 역할별 본문에 연결된 Registry와 작성 정책이 현재 소유자다.

### 외부 근거

외부 근거는 이 카탈로그의 계약 근거로 사용하지 않는다.
