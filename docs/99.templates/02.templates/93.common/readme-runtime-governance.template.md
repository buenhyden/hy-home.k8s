---
title: "{{TITLE}}"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---
# {{RUNTIME_GOVERNANCE_SURFACE_NAME}}

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for the runtime-governance README: a human document that states the role of this repository's GitHub automation surface, its supported environment, interfaces, checks and operation owners. -->

### 책임과 적용 범위

<!-- 작성 규칙: The runtime-governance README routes readers from GitHub workflow, repository setting and integration facts to their canonical owners; it restates no detailed policy and holds no agent-only instruction. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Service
##### Purpose
<!-- 작성 규칙: 이 저장소의 GitHub 자동화 표면의 목적과 주 독자를 설명한다. -->

<!-- 작성 규칙: 이 영역의 파일마다 그 파일을 읽는 런타임을 짝지어 보인다. -->

##### Interfaces
<!-- 작성 규칙: 이 영역의 외부 계약과 경계를 설명하고, 규범 정책과 계약 문서를 링크한다. -->

<!-- 작성 규칙: 이 문서가 외부 인터페이스를 밝힐 때만 아래 External Interfaces 표를 두고, 경계마다 한 행에 생산자, 소비자, 계약 참조, 실패 처리를 이 문서가 밝힌 사실로 적는다. 외부 인터페이스가 없으면 표를 지운다. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Name one boundary. | Name the producer. | Name the consumer. | Link the contract. | State how a failure is handled. |

###### Boundaries
<!-- 작성 규칙: 설정이 있다는 것과 런타임 동작이 입증되었다는 것을 구분한다. -->

###### Policy Routing
<!-- 작성 규칙: 모든 규칙은 기준 owner로 안내하고, 여기에서 정책을 다시 쓰지 않는다. -->

###### Workflow Roles
<!-- 작성 규칙: 자동화 워크플로마다 이름과 맡은 책임을 적는다. -->

###### Workflow Responsibility Matrix
<!-- 작성 규칙: 워크플로, 트리거, 책임, 증거 등급을 표로 정리한다. -->

###### Security Boundary
<!-- 작성 규칙: 비밀, 자격 증명, 권한 경계를 밝힌다. 해당하는 경계가 없거나 다른 절에 적었으면 없다는 사실과 이유를 한 줄로 적는다. -->

#### Usage
##### Prerequisites
<!-- 작성 규칙: 이 영역이 실제로 동작하는 환경과 지원 범위를 설명한다. -->

##### Selected Start
<!-- 작성 규칙: 변경하고 실행하는 로컬 절차를 순서대로 설명한다. 해당하는 절차가 없으면 없다는 사실과 이유를 적는다. -->

#### Checks
##### Readiness
<!-- 작성 규칙: 이 영역을 점검하는 검사와 증거를 링크한다. 해당하는 검사가 없으면 없다는 사실과 이유를 적는다. -->

<!-- 작성 규칙: 명령과 그 출력을 표로 보일 때만 아래 Commands 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Command | Output |
| --- | --- |
| Name one command. | State what it prints or leaves as evidence. |

###### Source Basis
<!-- 작성 규칙: 이 영역이 따르는 제품이나 제공자의 원문 문서를 인용한다. -->

##### Failure Handling
<!-- 작성 규칙: 관측과 복구 절차를 밝힌다. 해당하는 내용이 없으면 없다는 사실과 이유를 적는다. -->

###### Runbook Links
<!-- 작성 규칙: 운영 문서와 runbook을 링크한다. 해당하는 문서가 없으면 없다는 사실과 이유를 적는다. -->

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
