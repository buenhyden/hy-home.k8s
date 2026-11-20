---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/requirement"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Feature or System Name] Requirement Package

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a Requirement package that states the problem, scope, functional and quality requirements, acceptance conditions and traceability of one product or system outcome. -->

### 책임과 적용 범위

<!-- 작성 규칙: A Requirement owns the user value, its stable member requirements with their rationale and acceptance, and the acceptance boundary; architecture, decisions and change contracts stay with the Stage 02 and Stage 03 owners. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Overview
##### Problem and Outcome
<!-- 작성 규칙: state the problem with evidence, the cost of leaving it unresolved and the measurable outcome this work enables, separating fact from assumption and linking real references. -->

##### Stakeholders
<!-- 작성 규칙: identify the affected roles, their goals and constraints, and who writes, reviews and accepts the requirement. -->

#### Scope
##### In Scope
<!-- 작성 규칙: describe observable user journeys and the authorized scope without prescribing architecture. -->

##### Constraints and Exclusions
<!-- 작성 규칙: separate explicit non-goals and future options from constraints, and record product risks, dependencies, assumptions and validation owners. -->

#### Requirements
##### Functional Requirements
<!-- 작성 규칙: assign package-dependent stable IDs to functional and implementation-independent interface requirements; give each a statement, a one-sentence rationale that names its source (or explains why none is recorded), its acceptance evidence and its priority (`must`, `should` or `could`). -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0001-FR-0001 | State one testable functional requirement. | State the reason and name its source, or explain why none is recorded. | Name the observable acceptance evidence. | must |
| REQ-0001-IF-0001 | State one implementation-independent external interface requirement. | State the reason and name its source, or explain why none is recorded; interface_refs: REQ-0001-FR-0001 | Name the observable contract evidence. | must |

##### Quality Requirements
<!-- 작성 규칙: assign stable IDs and state each quality characteristic, its measurement environment and its target or decision-needed value in the same columns as Functional Requirements; when no quality requirement applies, say so in one sentence and delete the table. -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0001-NFR-0001 | State one measurable non-functional constraint. | State the reason and name its source, or explain why none is recorded. | Name the observable quality evidence. | must |

#### Traceability
##### Sources
<!-- 작성 규칙: name the upstream requirements, decisions and constraints this requirement derives from or depends on. -->

##### Verification Links
<!-- 작성 규칙: link the architecture descriptions, decisions and Specs that own the downstream contracts. -->

###### Acceptance Conditions
<!-- 작성 규칙: define measurable conditions that establish product success. -->

###### Verification Method
<!-- 작성 규칙: state how each acceptance condition is verified, or point to the Acceptance column and the acceptance-criterion column of Lifecycle Traceability when they state it. -->

##### Lifecycle Traceability
<!-- 작성 규칙: map each requirement to its acceptance criterion; the architecture description or Spec that owns it cites it in its own requirement column. -->

| Requirement ID | Acceptance criterion |
| --- | --- |
| REQ-0001-FR-0001 | State one measurable functional acceptance condition. |
| REQ-0001-NFR-0001 | State one measurable quality acceptance condition. |
| REQ-0001-IF-0001 | State one measurable interface acceptance condition. |

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
