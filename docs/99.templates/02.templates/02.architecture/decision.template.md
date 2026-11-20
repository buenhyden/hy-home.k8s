---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# {{ARTIFACT_ID}}: [Short Title]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for an architecture decision record that states the context, the chosen option and its authority, the alternatives, the consequences and the traceability of one durable decision. -->

### 책임과 적용 범위

<!-- 작성 규칙: An ADR owns one durable decision, its decision maker, effect and lineage; the current structure it changes stays with the Architecture Description, requirements with the Requirement and implementer-level contracts with the Spec. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Context
##### Problem and Drivers
<!-- 작성 규칙: state the forces, constraints, and evidence that require one decision. -->

##### Decision Scope
<!-- 작성 규칙: name concerns deliberately excluded from this decision. -->
<!-- 작성 규칙: state the scope of the decision and the consumers it affects. -->

#### Options
##### Considered Options
<!-- 작성 규칙: list the alternatives actually considered, each named as the option it is. -->

##### Trade-offs
<!-- 작성 규칙: compare credible alternatives and why they were not selected. -->

| Option | Benefit | Cost and Risk | Reason |
| --- | --- | --- | --- |
| <!-- 작성 규칙: Name one considered option. --> | <!-- 작성 규칙: State what choosing it gains, as this record states it. --> | <!-- 작성 규칙: State its cost and risk, as this record states them. --> | <!-- 작성 규칙: State why it was chosen or not selected, as this record states it. --> |

#### Decision
##### Chosen Option
<!-- 작성 규칙: summarize the decision, decision state, and affected boundary. -->
<!-- 작성 규칙: record one decision precisely enough for downstream implementation. -->

##### Authority and Effect
<!-- 작성 규칙: name the decision makers and the decision date when they differ from the owner and the updated date, and state how compliance will be confirmed. -->

###### Sources
<!-- 작성 규칙: name the requirement IDs and architecture views this decision serves or constrains. -->

###### Supersession
<!-- 작성 규칙: when a predecessor or successor decision exists, name it and its current or historical reference; remove this section when none exists. -->

##### Lifecycle Traceability
<!-- 작성 규칙: map decision lineage, replacement state, and affected specifications. -->

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| Architecture owner | Supersedes {{PREDECESSOR_ADR_ID}} or N/A — first decision | {{AFFECTED_SPEC_LINK}} or N/A — SPEC-xxxx left the tree; Git history recovers it |

#### Consequences
##### Impacts
<!-- 작성 규칙: record positive, negative, and operational consequences. -->

##### Follow-up
<!-- 작성 규칙: state the follow-up work, who owns it, how the decision is recovered if it fails, and how it is verified. -->

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
