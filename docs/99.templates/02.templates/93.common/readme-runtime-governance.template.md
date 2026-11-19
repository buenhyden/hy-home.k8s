---
title: "{{TITLE}}"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
---
# {{RUNTIME_GOVERNANCE_SURFACE_NAME}}

## Service

### Purpose

<!-- Author prompt: 이 영역의 목적과 주 독자를 설명한다. -->

<!-- Author prompt: 이 영역의 파일마다 그 파일을 읽는 런타임을 짝지어 보인다. -->

### Interfaces

<!-- Author prompt: 이 영역의 외부 계약과 경계를 설명하고, 규범 정책과 계약 문서를 링크한다. -->

<!-- Author prompt: 이 문서가 외부 인터페이스를 밝힐 때만 아래 External Interfaces 표를 두고, 경계마다 한 행에 생산자, 소비자, 계약 참조, 실패 처리를 이 문서가 밝힌 사실로 적는다. 외부 인터페이스가 없으면 표를 지운다. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| Name one boundary. | Name the producer. | Name the consumer. | Link the contract. | State how a failure is handled. |

#### Boundaries

<!-- Author prompt: 설정이 있다는 것과 런타임 동작이 입증되었다는 것을 구분한다. -->

#### Policy Routing

<!-- Author prompt: 모든 규칙은 기준 owner로 안내하고, 여기에서 정책을 다시 쓰지 않는다. -->

#### Workflow Roles

<!-- Author prompt: 자동화 워크플로마다 이름과 맡은 책임을 적는다. -->

#### Workflow Responsibility Matrix

<!-- Author prompt: 워크플로, 트리거, 책임, 증거 등급을 표로 정리한다. -->

#### Security Boundary

<!-- Author prompt: 비밀, 자격 증명, 권한 경계를 밝힌다. 해당하는 경계가 없거나 다른 절에 적었으면 없다는 사실과 이유를 한 줄로 적는다. -->

## Usage

### Prerequisites

<!-- Author prompt: 이 영역이 실제로 동작하는 환경과 지원 범위를 설명한다. -->

### Selected Start

<!-- Author prompt: 변경하고 실행하는 로컬 절차를 순서대로 설명한다. 해당하는 절차가 없으면 없다는 사실과 이유를 적는다. -->

## Checks

### Readiness

<!-- Author prompt: 이 영역을 점검하는 검사와 증거를 링크한다. 해당하는 검사가 없으면 없다는 사실과 이유를 적는다. -->

<!-- Author prompt: 명령과 그 출력을 표로 보일 때만 아래 Commands 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Command | Output |
| --- | --- |
| Name one command. | State what it prints or leaves as evidence. |

#### Source Basis

<!-- Author prompt: 이 영역이 따르는 제품이나 제공자의 원문 문서를 인용한다. -->

### Failure Handling

<!-- Author prompt: 관측과 복구 절차를 밝힌다. 해당하는 내용이 없으면 없다는 사실과 이유를 적는다. -->

#### Runbook Links

<!-- Author prompt: 운영 문서와 runbook을 링크한다. 해당하는 문서가 없으면 없다는 사실과 이유를 적는다. -->
