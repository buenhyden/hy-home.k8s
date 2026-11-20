---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/postmortem"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# Postmortem: [Incident Title]

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Give authors one form for a postmortem that records the root cause, the confirmed impact, the corrective actions and their evidence for one incident. -->

### 책임과 적용 범위

<!-- 작성 규칙: A postmortem owns the causal analysis, contributing factors, corrective actions and review decision for one incident; the observed facts and timeline stay in the incident record. -->

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 이 문서를 작성할 때 필요한 실제 입력, 권한과 전제를 밝힌다. -->

### 본문과 규칙

<!-- 작성 규칙: 아래 역할별 절의 내용과 표를 해당 문서의 실제 사실로 채운다. -->

#### Facts
##### Timeline
<!-- 작성 규칙: 대상 incident의 사실 기록을 실제 참조로 링크한다. -->

###### Review Scope
<!-- 작성 규칙: 얻은 교훈과 회고 범위를 요약한다. -->

##### Impact
<!-- 작성 규칙: 확인된 영향만 적는다. -->

###### Detection and Response
<!-- 작성 규칙: incident를 어떻게 탐지했는지, 어떤 대응 결정이 완화를 돕거나 늦췄는지 설명하고 Incident 타임라인의 증거를 인용한다. -->

##### What Went Well
<!-- 작성 규칙: 선택 항목이다. 영향을 줄인 통제나 대응 행동이 있을 때만 밝히고, 없으면 이 절을 지운다. -->

#### Causes
##### Contributing Factors
<!-- 작성 규칙: 기술, 절차, 조직 측면의 기여 요인을 비난 없이 기록한다. -->

###### What Went Wrong
<!-- 작성 규칙: 틀린 가정과 제대로 작동하지 않은 통제, 탐지, 협업을 밝힌다. -->

###### Causal Analysis
<!-- 작성 규칙: 증거를 바탕으로 분석해 근본 원인과 증상을 구분한다. -->

##### Uncertainty
<!-- 작성 규칙: 아직 확인되지 않은 원인·가정·증거와 그것을 확정할 증거를 적는다. -->

#### Actions
##### Prevention
<!-- 작성 규칙: 재발 방지 조치마다 owner, 기한 상태, Task, 증거를 지정하고, 교훈을 요구사항, 결정, Spec, 가이드, 정책 가운데 알맞은 곳으로 보낸다. -->

<!-- 작성 규칙: 아래 Actions 표에 조치마다 owner, 실행·완료 조건, 실제 근거를 적는다. 근거가 아직 없으면 none을 쓰고, 실제 조치가 생기기 전에는 열만 둔다. -->

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| Name one corrective action. | Name the owner. | State the completion condition and how it is verified. | Link the actual evidence, or none. |

##### Owners and Checks
<!-- 작성 규칙: 조치가 재발을 어떻게 막는지와 종료를 어떻게 검증할지 정하고, 조치 owner, 기한 날짜 또는 상태, 완료 증거, 남은 위험을 나열한다. -->

###### Source Records
<!-- 작성 규칙: incident 기록, 로그, 결정을 실제 참조로 링크한다. -->

###### Review Decision
<!-- 작성 규칙: 종료 승인자와 검토·게시 결정, 미결 사항을 적는다. -->

##### Lifecycle Traceability
<!-- 작성 규칙: 원인이나 조치를 owner, 후속 Task, 피드백 대상에 연결한다. -->

| Root cause or action | Owner and due state | Follow-up Task | Feedback target |
| --- | --- | --- | --- |
| Evidence-backed cause or prevention action | owner / due date / state | Task owner | Requirement, ADR, Spec, Guide, or Policy owner |

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
