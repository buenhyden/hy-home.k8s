---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Topic Name] Runbook

## Purpose

<!-- Author prompt: 운영 목표, 범위가 정해진 시스템, 반복 절차의 실행자와 안전한 종료 상태를 밝힌다. -->

## Trigger and Preconditions

<!-- Author prompt: 트리거, 사전 조건, 권한, 중단 조건을 정한다. -->

## Procedure

<!-- Author prompt: 모든 조치, 기대 결과, escalation 경계를 관측할 수 있게 적는다. -->

| Step | Action | Expected result | Stop / escalate when |
| --- | --- | --- | --- |
| 1 | Perform one bounded operation. | State the observable safe result. | State the failure or ambiguity that stops execution. |

## Verification

<!-- Author prompt: 결정론적 완료 검사, 관찰 가능한 지표·로그·이벤트, 증거 보존 위치를 적는다. -->

## Recovery and Escalation

<!-- Author prompt: 안전한 수정 또는 roll-forward 복구 단계, 복구 확인, 중단 기준과 사람에게 넘기는 경로를 적는다. -->

## Related Documents

<!-- Author prompt: 승격된 권한, 트리거나 통제, 증거 또는 복구 owner를 연결한다. -->

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| Policy, Specification, or Task owner | Named trigger or control | Named evidence or recovery owner |
