---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-description"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [System or Domain Name] Architecture Description (AD)

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for one system view that distinguishes the approved structure, the current configuration, and directly observed deployment and behavior. -->

### 책임과 적용 범위

<!-- 작성 규칙: An architecture description owns the target and current structure of one system, the evidence boundary of its operational observations, and the requirement-to-architecture relation. It cites every requirement it serves and links the decisions and Spec contracts at their current owners. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Context and Boundaries
##### System Boundary
<!-- 작성 규칙: define system boundaries, what the system owns and does not own, and explicit non-goals. -->

###### Purpose and Readers
<!-- 작성 규칙: identify the architecture subject, its stakeholders and the readers this description serves, and state who owns the structure description. -->

###### Context
<!-- 작성 규칙: name the external dependencies, actors and trust boundaries the system consumes or serves. -->

##### Constraints
<!-- 작성 규칙: state the constraints that limit the architecture; a description without a constraints table explains where its constraints are recorded. -->

| Architecture ID | Constraint | Affected Components |
| --- | --- | --- |
| <!-- 작성 규칙: Name a free-text constraint identifier. --> | <!-- 작성 규칙: State the constraint as a checkable fact. --> | <!-- 작성 규칙: Name the components or views it limits. --> |

#### Structure
##### Building Blocks
<!-- 작성 규칙: Describe components, actors, trust boundaries, and major interactions declared by the current sources. Identify approved target structure that those sources do not yet declare. -->
<!-- 작성 규칙: Use proportionate context and container views to show responsibilities, labels, and relationships, or explain an omitted view. -->
<!-- 작성 규칙: Give every diagram a title, scope, intended reader, legend, and editable source. Label each element with its name, type and responsibility, and give each relationship a direction and a label that states its purpose and protocol. -->

##### Interfaces
<!-- 작성 규칙: state data ownership, flow, retention, integrity constraints and the contracts between components. -->
<!-- 작성 규칙: keep the External Interfaces table below only when this description states an external interface; give each boundary one row with its producer, consumer, contract reference and failure handling as this description states them, and keep only the header while a stated fact is missing. Delete the table when the description states no external interface. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| <!-- 작성 규칙: Name one boundary. --> | <!-- 작성 규칙: Name the producer. --> | <!-- 작성 규칙: Name the consumer. --> | <!-- 작성 규칙: Link the contract. --> | <!-- 작성 규칙: State how a failure is handled. --> |

#### Runtime Behavior
##### Normal Flow
<!-- 작성 규칙: Identify the declared deployment topology and its configuration owners. Cite actual runtime observations with their input, environment, and result. Identify any unobserved scope and its verification owner. -->

##### Failure and Recovery
<!-- 작성 규칙: define failure boundaries and what each failure leaves intact. -->

#### Quality Scenarios
##### Scenarios
<!-- 작성 규칙: make quality attributes measurable and link each to a requirement. -->

<!-- 작성 규칙: For each material quality concern, state a requirement-linked scenario. -->
<!-- 작성 규칙: Name the stimulus, operating environment, expected response, and measurable threshold; an adjective alone is not a scenario. -->

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| <!-- 작성 규칙: Name the requirement-backed attribute. --> | <!-- 작성 규칙: State the triggering event. --> | <!-- 작성 규칙: State the operating condition. --> | <!-- 작성 규칙: State the system response. --> | <!-- 작성 규칙: State a measurable threshold. --> |

##### Trade-offs
<!-- 작성 규칙: state what the structure gives up for each quality it favors, using only facts from this description and its ADRs. -->

#### Decisions and Adoption
##### Decisions
<!-- 작성 규칙: State core structural choices and link each significant decision to its owning ADR. -->

###### Requirement Mapping
<!-- 작성 규칙: name the requirement this description serves and cite each of its members in the Lifecycle Traceability table. -->

##### Adoption Boundaries
<!-- 작성 규칙: Explain differences between approved targets, current declarations, and observed operation. Link the evidence and responsible owners, including lineage for Specs or evidence that left the tree. Optionally map arc42 sections to their current owners and explain omissions. -->

##### Lifecycle Traceability
<!-- 작성 규칙: map requirements and boundaries to the decisions or specifications that own them. -->

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| REQ-0001-NFR-0001 | Name one measurable attribute or architecture boundary. | ADR or Specification owner |

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
