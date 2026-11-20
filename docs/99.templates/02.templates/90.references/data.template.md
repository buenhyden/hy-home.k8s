---
title: "{{TITLE}}"
version: "0.1.0"
type: "reference/data"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# Reference: [Item Name]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a Stage 90 data member that records a reproducible repository-fact snapshot with its observation boundary and sources. -->

### 책임과 적용 범위

<!-- 작성 규칙: A data member owns its dated evidence and states what it cannot establish; it never becomes policy or current authority by itself. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Purpose
##### Consumers
<!-- 작성 규칙: identify the referenced subject, reader need, and observation boundary. -->

<!-- 작성 규칙: Identify this Data member as a reproducible repository-fact snapshot and name its consumer. -->

###### Related Documents
<!-- 작성 규칙: link canonical consumers, successor evidence, and source ledgers. -->

##### Boundaries
<!-- 작성 규칙: state what this reference can and cannot establish. -->

#### Provenance
##### Collection
<!-- 작성 규칙: Define included repositories, paths, commits, time boundary, exclusions, and consumers. -->

<!-- 작성 규칙: cite the producing repository objects and observation dates. -->

| Source | Revision or observation | Derivation |
| --- | --- | --- |
| <!-- 작성 규칙: Name the source path or object. --> | <!-- 작성 규칙: Pin the revision or date. --> | <!-- 작성 규칙: Explain the transformation. --> |

| Field | Producer |
| --- | --- |
| <!-- 작성 규칙: Name a field of the schema table below. --> | <!-- 작성 규칙: Name the producing surface. --> |

###### Generation and Refresh

| Generation command | Refresh trigger | Owner |
| --- | --- | --- |
| <!-- 작성 규칙: State a reproducible command. --> | <!-- 작성 규칙: State the change that makes this stale. --> | <!-- 작성 규칙: Name the maintainer. --> |

##### Versions and Dates
<!-- 작성 규칙: Pin each input revision and the observation date; an access date is not a publication date. -->

#### Interpretation
<!-- 작성 규칙: distinguish observed repository facts from interpretation. -->

##### Schema and Units

| Field | Type | Unit | Meaning | Limits |
| --- | --- | --- | --- | --- |
| <!-- 작성 규칙: Name a stable field. --> | <!-- 작성 규칙: State the value type. --> | <!-- 작성 규칙: State the unit, or none. --> | <!-- 작성 규칙: Define its meaning. --> | <!-- 작성 규칙: State precision, missing values or cost. --> |

###### Repository Facts
<!-- 작성 규칙: Record the dataset facts with their source revision without importing credentials or private runtime state. -->

##### Limits
<!-- 작성 규칙: state refresh triggers, staleness risks, and current-truth owner. -->

###### Staleness Boundaries
<!-- 작성 규칙: State what this snapshot cannot establish after its source or scope changes; link the current owner for live meaning. -->

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
