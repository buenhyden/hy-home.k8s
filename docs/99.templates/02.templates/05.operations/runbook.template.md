---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Topic Name] Runbook

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a runbook that carries an operator through one executable operating procedure, its checks and its recovery. -->

### 책임과 적용 범위

<!-- 작성 규칙: A runbook owns the preconditions, steps, stop conditions, validation and recovery of one operating procedure; stable explanations stay with guides and rules with policies. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Trigger and Scope
##### Trigger
<!-- 작성 규칙: 실행 트리거와 복구·운영 목표, 반복 절차의 실행자와 안전한 종료 상태를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Targets
<!-- 작성 규칙: 범위가 정해진 서비스·환경·영향 범위를 사실·가정과 구분해 밝히고, 관련 아키텍처·색인·동반 runbook은 실제 참조로 연결한다. -->

#### Preflight
##### Authority
<!-- 작성 규칙: 소유자 승인, 권한, 환경 확인과 실행자·실행 유형을 사실·가정과 구분해 밝히고 규범 정책·결정은 실제 참조로 연결한다. -->

##### Environment
<!-- 작성 규칙: 백업, 가용성, 동시 작업, 비밀 보호를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

#### Procedure
##### Steps
<!-- 작성 규칙: 확인된 명령, 입력, 실행 책임과 모든 조치의 기대 결과를 관측할 수 있게 적고, mutating 명령에는 경계 표지를 함께 둔다. -->

<!-- 작성 규칙: 아래 Steps 표에 단계마다 순서, 행동, 관측할 결과, 실패 시 중단 지점과 다음 책임자를 이 런북이 밝힌 사실로만 적는다. 실제 단계를 적기 전에는 열만 둔다. -->

| Step | Action | Expected Result | On Failure |
| --- | --- | --- | --- |
| 1 | Describe one bounded operation. | Describe the observable result. | State where to stop and who owns the next step. |

##### Stop Conditions
<!-- 작성 규칙: 관측 기준, 실행을 멈추는 실패·모호함, 추가 승인이 필요한 조건, escalation 경계를 적는다. -->

#### Verification
##### Expected Results
<!-- 작성 규칙: 결정론적 완료 검사와 기대 상태, 관찰 가능한 지표·로그·이벤트, 읽기 확인을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Unverified Conditions
<!-- 작성 규칙: 실제로 관측한 증거, 보존 위치, 판본, 남은 제한을 밝히고 증거 문서는 실제 참조로 연결한다. -->

##### Lifecycle Traceability
<!-- 작성 규칙: 승격된 권한, 트리거나 통제, 증거 또는 복구 owner를 구체적으로 적는다. -->

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| Policy, Specification, or Task owner | Named trigger or control | Named evidence or recovery owner |

#### Escalation
##### Next Owner
<!-- 작성 규칙: 운영자, 인계 근거, 복구 불가 조건과 사람에게 넘기는 경로를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

##### Recovery or Forward Repair
<!-- 작성 규칙: 원복 조건, 절차, 데이터 보존을 사실·가정과 구분해 밝힌다. 실행이 상태나 산출물을 바꾸지 않으면 그 사실과 이유를 적는다. -->

##### Recovery Procedures
<!-- 작성 규칙: 선택 항목이다. 단계의 원복이 아닌 복구·수정 절차(안전한 수정 또는 roll-forward 복구 단계와 복구 확인)가 있을 때만 쓰고, 없으면 이 절을 지운다. -->

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
