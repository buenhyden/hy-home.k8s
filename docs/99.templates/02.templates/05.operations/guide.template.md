---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Topic Name] Guide

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a guide that explains or walks a reader through a stable operating procedure. -->

### 책임과 적용 범위

<!-- 작성 규칙: A guide owns how a reader reaches and checks one operating outcome; execution and recovery steps stay with runbooks and rules stay with policies. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Purpose
##### Audience
<!-- 작성 규칙: 이 가이드가 돕는 독자와 각 독자가 이미 아는 것을 적는다. -->

##### Outcome
<!-- 작성 규칙: 독자가 얻을 작업 결과와 독자를 사실·가정과 구분해 밝히고, 주된 학습 목적을 tutorial/how-to/reference/explanation 가운데 하나로 분류한 뒤 현재 권한 원본과 관련 운영 문서로 연결한다. -->

###### Boundaries
<!-- 작성 규칙: 이 가이드가 다루는 범위와 다루지 않는 비목표를 사실·가정과 구분해 밝히고, 다른 owner가 소유한 항목은 실제 참조로 연결한다. -->

#### Prerequisites
##### Environment
<!-- 작성 규칙: 실행 전에 필요한 도구 판본, 검증된 입력, 접근을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Authority
<!-- 작성 규칙: 허용되는 권한과 보호해야 할 대상을 사실·가정과 구분해 밝히고 규범 정책으로 연결한다. -->

#### Procedure
##### Steps
<!-- 작성 규칙: 순서별 입력, 행동, 기대 출력을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

<!-- 작성 규칙: 순서가 있는 절차일 때만 아래 Steps 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | Describe the action. | Describe the observable result. | State where to stop and who owns the next step. |

##### Expected Results
<!-- 작성 규칙: 성공과 실패의 관측 결과와 확인 방법을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

#### Troubleshooting
##### Symptoms
<!-- 작성 규칙: 진단 방법, 안전한 복구, 담당을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Next Action
<!-- 작성 규칙: 실패, 분기, 중단 조건과 문의 경로를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Lifecycle Traceability
<!-- 작성 규칙: 승격된 owner의 독자 결과와 운영 영역을 구체적으로 적는다. -->

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| Specification or Task owner | State the reader outcome. | Name the system, workflow, or concept covered. |

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
