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

## Purpose

### Trigger and Outcome

<!-- Author prompt: 실행 트리거와 복구·운영 목표, 반복 절차의 실행자와 안전한 종료 상태를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

### Scope

<!-- Author prompt: 범위가 정해진 서비스·환경·영향 범위를 사실·가정과 구분해 밝히고, 관련 아키텍처·색인·동반 runbook은 실제 참조로 연결한다. -->

## Preconditions

### Authority and Access

<!-- Author prompt: 소유자 승인, 권한, 환경 확인과 실행자·실행 유형을 사실·가정과 구분해 밝히고 규범 정책·결정은 실제 참조로 연결한다. -->

### Safety Checks

<!-- Author prompt: 백업, 가용성, 동시 작업, 비밀 보호를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

## Steps

### Actions

<!-- Author prompt: 확인된 명령, 입력, 실행 책임과 모든 조치의 기대 결과를 관측할 수 있게 적고, mutating 명령에는 경계 표지를 함께 둔다. -->

<!-- Author prompt: 트리거별로 조치와 원복을 나눌 때만 아래 Triggers 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Trigger | Action | Rollback |
| --- | --- | --- |
| Name the condition that starts the action. | Describe one bounded operation. | Describe the undo, or state why none exists. |

### Stop Conditions

<!-- Author prompt: 관측 기준, 실행을 멈추는 실패·모호함, 추가 승인이 필요한 조건, escalation 경계를 적는다. -->

## Validation

### Service Checks

<!-- Author prompt: 결정론적 완료 검사와 기대 상태, 관찰 가능한 지표·로그·이벤트, 읽기 확인을 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->

### Evidence

<!-- Author prompt: 실제로 관측한 증거, 보존 위치, 판본, 남은 제한을 밝히고 증거 문서는 실제 참조로 연결한다. -->

### Lifecycle Traceability

<!-- Author prompt: 승격된 권한, 트리거나 통제, 증거 또는 복구 owner를 구체적으로 적는다. -->

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| Policy, Specification, or Task owner | Named trigger or control | Named evidence or recovery owner |

## Recovery

### Recovery Procedures

<!-- Author prompt: 선택 항목이다. 단계의 원복이 아닌 복구·수정 절차(안전한 수정 또는 roll-forward 복구 단계와 복구 확인)가 있을 때만 쓰고, 없으면 이 절을 지운다. -->

### Rollback

<!-- Author prompt: 조건부 항목이다. 실행이 상태나 산출물을 바꿀 때만 원복 조건, 절차, 데이터 보존을 사실·가정과 구분해 밝히고, 아니면 이 절을 지운다. -->

### Escalation

<!-- Author prompt: 운영자, 인계 근거, 복구 불가 조건과 사람에게 넘기는 경로를 사실·가정과 구분해 밝히고 실제 참조로 연결한다. -->
