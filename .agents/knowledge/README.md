---
title: "Common Knowledge"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# Common Knowledge

## 문서 개요

### 목적과 독자

이 README는 .agents/knowledge에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 .agents/knowledge의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

이 영역은 방향을 잡는 질문과 공통 용어의 뜻을 묻는 질문에 답한다. 어느 트리가 무엇을 소유하는지, 어떤
도메인에서 무엇을 먼저 열어야 하는지를 알려 준다. 여기에는 포인터와 범위가
정해진 관측 metadata, 그리고 공통 용어 의미만 정의하는 [Repository Vocabulary](glossary.md)가 있다. K8s 로컬 용어는 [작업환경 용어집](../../docs/00.workspace/01.project/glossary.md)이 소유한다. 정책, 설계, 절차, 현재 상태에 대한 서술은 모두 각
행이 가리키는 소유자에게 남는다.

###### Inputs and Outputs

knowledge 문서는 소유자 경로, 읽는 사람이 먼저 여는 진입 경로, 그 행이 유효한
조건을 적는다. 가리키는 본문의 어떤 구간도 다시 옮겨 적지 않고, 사람이 직접
작성하며, 생성기가 쓰지 않는다. 퇴역한 생성 색인은 여기서 다시 만들지 않는다.
이 영역을 두 번째 권한 원본이 아닌 지도로 유지하는 것은 중복 금지 규칙과 그
validator다.

범위 밖: 승인 경계, 권한, 역할 명단, gate 명령, lifecycle 상태, 근거 등급. 이들은
기존 소유자에게 남으며, 그중 하나를 다시 서술하는 행은 편의가 아니라 결함이다.

##### Excluded Responsibilities

이 영역은 정책, 설계, 절차, 현재 상태에 대한 서술을 소유하지 않으며 이는 각 행이 가리키는 소유자에게 남는다. 승인 경계, 권한, 역할 명단, gate 명령, lifecycle 상태, 근거 등급도 범위 밖으로 기존 소유자에게 남고, 그중 하나를 다시 서술하는 행은 결함이다. 가리키는 본문의 구간을 다시 옮겨 적지 않으므로 두 번째 권한 원본이 아니라 지도다.

#### Current Contents

##### Paths

###### Item Index

| Path | Purpose |
| --- | --- |
| [Project Map](project-map.md) | 최상위 트리별 소유 범위와 각각의 진입 문서. |
| [Domain Index](domains.md) | 운영 도메인별 정규 소유자, 진입 경로, 행이 유효한 조건. |
| [Repository Vocabulary](glossary.md) | 공통 작업·거버넌스 용어의 단일 의미 원본과 규칙 소유자 링크. 규칙은 서술하지 않는다(ADR-0058). |
| [K8s Workspace Vocabulary](../../docs/00.workspace/01.project/glossary.md) | K8s 로컬 용어의 뜻을 찾는 작업환경 경로. |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

###### Add and Find

1. 문서를 추가하기 전에 [document authoring](../../docs/00.workspace/03.process/document-authoring.md)을
   읽고 Stage 99 registry에서 knowledge profile을 고른다.
2. 읽는 사람이 이 행 없이는 소유자를 찾아 헤매야 할 때만 행을 추가한다. 소유자의
   자체 색인이 이미 말하는 내용을 반복하는 행은 추가하지 않는다.
3. 소유자 경로와 진입 경로는 트리에 실제로 있는 그대로 적는다. 소유자나 진입
   경로가 없는 행은 검증에 실패한다.
4. 포인터의 유효 조건은 관측 가능한 변화로 적는다. 선택적 관측 metadata는
   source hash와 만료일을 갖춰 context-and-memory 정책을 따르며, 원문 서술을
   복제하거나 변경을 승인하지 않는다.
5. 새 knowledge 포인터 문서를 받아들이면 위 Item Index 표에서 링크하고, 소유자
   세부는 이 라우터에 복사하지 말고 그 문서에 둔다.

###### Upstream and Downstream

- [Common Agent Governance](../README.md)
- [Repository documentation](../../docs/README.md)

###### Policy and Templates

- [Context and Memory](../governance/context-and-memory.md)
- [knowledge-map skill](../skills/knowledge-map/SKILL.md)

##### Checks

이 README는 상태, 승격, 종료 규칙을 따로 두지 않는다. 그런 규칙을 두게 되면 여기에 적는다.

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
