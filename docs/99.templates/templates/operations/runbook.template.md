---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "{{OWNER}}"
updated: "{{YYYY_MM_DD}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Topic Name] Runbook

## Overview

<!-- Author prompt: 운영 목표, 범위가 정해진 시스템, 안전한 종료 상태를 밝힌다. -->

## Runbook Type

<!-- Author prompt: 운영자 역할, 그 역할이 결정하는 범위, 필요한 권한을 밝히고, 이 반복 절차가 정책이나 가이드가 아니라 runbook에 속하는 이유를 적는다. -->

## When to Use

<!-- Author prompt: 트리거, 사전 조건, 권한, 중단 조건을 정한다. -->

## Procedure or Checklist

<!-- Author prompt: 모든 조치, 기대 결과, escalation 경계를 관측할 수 있게 적는다. -->

| Step | Action | Expected result | Stop / escalate when |
| --- | --- | --- | --- |
| 1 | Perform one bounded operation. | State the observable safe result. | State the failure or ambiguity that stops execution. |

## Verification Steps

<!-- Author prompt: 결정론적 검사와 이름 붙은 증거로 완료를 입증한다. -->

## Observability and Evidence Sources

<!-- Author prompt: 승인된 지표, 로그, 이벤트와 증거 보존 위치를 적는다. -->

## Safe Rollback or Recovery Procedure

<!-- Author prompt: 범위가 정해진 롤백 단계, 복구 확인, 사람에게 넘기는 escalation을 적는다. -->

## Traceability

<!-- Author prompt: 승격된 권한, 트리거나 통제, 증거 또는 복구 owner를 연결한다. -->

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| Policy, Specification, or Task owner | Named trigger or control | Named evidence or recovery owner |
