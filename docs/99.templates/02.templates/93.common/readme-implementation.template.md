---
title: "{{TITLE}}"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---
# {{COMPONENT_NAME}}

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for an implementation README: a human document for a code, configuration, agent or provider folder that states the service role, its supported environment, its interfaces, how to develop and check it, and where to operate it. -->

### 책임과 적용 범위

<!-- 작성 규칙: An implementation README owns the human-facing description of its folder and routes readers to canonical owners; it restates no detailed policy and holds no agent-only instruction. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Service
##### Purpose
<!-- 작성 규칙: 구성 요소의 목적, 지원하는 사용 방식, 권한 경계와 이 경로의 책임 owner를 설명한다. -->

<!-- 작성 규칙: 직접 하위 폴더나 파일과 그 진입점을 링크한다. 하위 항목마다 내부 경로는 하나까지만 적고, 트리에는 직접 하위 항목만 보인다. 상태, 날짜, 개수는 각 문서가 직접 가지므로 옮겨 적지 않는다. 경로 매트릭스는 그 멤버를 나열하는 폴더의 README에 둔다. -->

<!-- 작성 규칙: 아키텍처와 Spec 같은 탐색·설계 문서는 이 절에서 링크한다. -->

##### Interfaces
<!-- 작성 규칙: 외부 계약과 경계를 밝히고, 규범 정책과 계약 문서는 이 절에서 링크한다. 해당하는 외부 계약이 없으면 없다는 사실과 이유를 적는다. -->

<!-- 작성 규칙: 이 문서가 외부 인터페이스를 밝힐 때만 아래 External Interfaces 표를 두고, 경계마다 한 행에 생산자, 소비자, 계약 참조, 실패 처리를 이 문서가 밝힌 사실로 적는다. 외부 인터페이스가 없으면 표를 지운다. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Name one boundary. | Name the producer. | Name the consumer. | Link the contract. | State how a failure is handled. |

###### Configuration Boundary
<!-- 작성 규칙: 설정 owner, 입력값, 보호해야 할 외부 상태를 밝힌다. -->

###### Security Boundary
<!-- 작성 규칙: 비밀, 자격 증명, 권한 경계를 밝힌다. 해당하는 경계가 없거나 다른 절에 적었으면 없다는 사실과 이유를 한 줄로 적는다. -->

#### Usage
##### Prerequisites
<!-- 작성 규칙: 이 경로의 포함 범위, 제외 대상과 권한 owner, 실제 환경과 지원 범위를 설명한다. -->

##### Selected Start
<!-- 작성 규칙: 변경하고 실행하는 로컬 절차를 순서대로 설명한다. 해당하는 절차가 없으면 없다는 사실과 이유를 적는다. -->

#### Checks
##### Readiness
<!-- 작성 규칙: 실제 독자가 필요할 때만 이 절에서 정본 검사 owner로 안내하고, 증거와 점검 문서를 링크한다. -->

###### Validation
<!-- 작성 규칙: 결정론적 검사를 나열하고, live 또는 원격 증거의 한계를 표시한다. -->

<!-- 작성 규칙: 명령과 그 출력을 표로 보일 때만 아래 Commands 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Command | Output |
| --- | --- |
| Name one command. | State what it prints or leaves as evidence. |

##### Failure Handling
<!-- 작성 규칙: 관측과 복구 절차를 밝힌다. 해당하는 내용이 없으면 없다는 사실과 이유를 적는다. -->

###### Operations
<!-- 작성 규칙: 설치, 배포, 복구, 문제 해결은 해당 owner 문서로 안내한다. -->

###### Runbook Links
<!-- 작성 규칙: 운영, 거버넌스 owner와 runbook, 가이드를 링크한다. 해당하는 문서가 없으면 없다는 사실과 이유를 적는다. -->

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
