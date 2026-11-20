---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: ["{{PARENT_ID}}"]
---

# [Feature Name] Implementation Plan

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for the work order of one Spec that states the goal, shared constraints, dependencies, work units, verification, risks and promotion of durable meaning. -->

### 책임과 적용 범위

<!-- 작성 규칙: A Plan owns the order of the work for one approved Spec: its units and their criteria, the verification and its placement, the risks with their rollback and the promotion of each durable contract to its current owner; the change contract stays with the Spec and execution and evidence stay with the Task. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Overview
##### Outcome
<!-- 작성 규칙: identify the specification being executed and the intended completion state. -->
<!-- 작성 규칙: list bounded outcomes this plan is authorized to deliver. -->
<!-- 작성 규칙: state excluded work, protected surfaces, and deferred decisions. -->

##### Constraints
<!-- 작성 규칙: summarize current evidence, constraints, and prerequisite decisions. -->
<!-- 작성 규칙: name the architecture views or ADRs, interfaces, migration and rollback this plan touches, or say that none apply. -->

###### Global Constraints
<!-- 작성 규칙: Link the approved Spec constraints and state only additional execution constraints here. -->
<!-- 작성 규칙: Every work package inherits the approved Spec constraints. -->

###### Risks and Mitigations
<!-- 작성 규칙: record delivery, compatibility, and rollback risks with owners. -->

###### Escalation
<!-- 작성 규칙: name the blocking conditions, the questions for the user and the condition to resume. -->

#### Dependencies
##### Prerequisites
<!-- 작성 규칙: name the existing contracts, consumers, authorities and environments this plan needs before work starts, or say that none apply. -->

##### Shared Resources
<!-- 작성 규칙: name the files, environments, registries and locks that more than one work unit uses, and how their use is ordered, or say that none are shared. -->

#### Work Breakdown
##### Work Units
<!-- 작성 규칙: order work packages by dependency and make each entry and exit gate observable. -->

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [AC-0001]({{SPEC_RELATIVE_PATH}}#criteria) | One bounded implementation outcome | None | [Task]({{TASK_RELATIVE_PATH}}) | Named deterministic check and expected evidence |

<!-- 작성 규칙: give each work unit one row in the table below: its outcome, the units it depends on, its owner, the paths it may write, the criteria it serves and the checks it selects. -->

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | One bounded implementation outcome | none | {{OWNER}} | Name the paths this unit may write. | AC-0001 | Name the selected checks. |

###### Change and Rollback
<!-- 작성 규칙: state what each work unit changes, how, and the order in which a change is undone. -->

##### Dependency Edges
<!-- 작성 규칙: state the inputs, outputs and entry conditions that order one work unit after another. -->

#### Verification Plan
##### Selected Checks
<!-- 작성 규칙: map every work package to deterministic checks and evidence lanes. -->
<!-- 작성 규칙: include an architecture compliance check that each work package stays within the views and ADRs named in Assumptions; a departure returns the Spec to in-review. -->
<!-- 작성 규칙: define the conditions that close work without claiming live evidence. -->
<!-- 작성 규칙: give each selected check one row in the Checks table below: its unique guarantee, required input, trust boundary, the condition that selects it and the evidence type it must produce. -->

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| <!-- 작성 규칙: Name one stable check ID. --> | <!-- 작성 규칙: State what only this check guarantees. --> | <!-- 작성 규칙: State the input it needs. --> | <!-- 작성 규칙: State what the check trusts and what it cannot prove. --> | <!-- 작성 규칙: State the condition that selects it. --> | <!-- 작성 규칙: Name the evidence type it must produce. --> |

##### Evidence Plan
<!-- 작성 규칙: state at which commit, push, pull request or merge each check runs and how repeats are avoided. -->

#### Promotion Map
##### Durable Owners
<!-- 작성 규칙: Use this section as the sole durable-contract promotion receipt for this Plan. -->
<!-- 작성 규칙: Name each lasting contract and one current `.agents/` governance, or Stage 01, 02, or 05 authority. -->
<!-- 작성 규칙: Link that authority with one relative Markdown link and give its concrete section or member. -->
<!-- 작성 규칙: For a Registry-realized contract, link the current rule that delegates mechanics to Stage 99. -->
<!-- 작성 규칙: State in the Acceptance cell the condition under which the promotion counts as done. -->
<!-- 작성 규칙: If nothing durable is promoted, use only the row `none | none | none | No durable contract was introduced`. -->
<!-- 작성 규칙: Record actual receiving owner updates before claiming promotion. -->

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| {{DURABLE_CONTRACT}} | [{{CURRENT_AUTHORITY_TITLE}}]({{CURRENT_AUTHORITY_PATH}}) | {{ACCEPTANCE_CONDITION}} | {{LOCATION_IN_OWNER}} |

##### Consumer Updates
<!-- 작성 규칙: name the contracts and operating meaning that remain after the work is complete, or say that none remain. -->

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 사용 방법과 적용 대상을 설명한다. -->

### 확인 기준

<!-- 작성 규칙: 이 문서 유형에 해당하는 확인 방법과 한계를 적는다. -->

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 현재 정본의 관계와 탐색 링크만 연결한다. 실제 의미 관계가 있으면 Relation에 requires/designs/implements/verifies/operates/defines/cites 중 하나를, Target에 현재 문서의 상대 Markdown 링크 하나를 적는다. 단순 탐색 링크는 표 밖에 둔다. -->

| Relation | Target |
| --- | --- |

### 외부 근거

<!-- 작성 규칙: 외부 근거가 있으면 출처와 채택 범위를 적고, 없으면 그 이유를 명시한다. -->
