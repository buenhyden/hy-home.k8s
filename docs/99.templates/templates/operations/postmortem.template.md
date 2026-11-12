---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/postmortem"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
---

# Postmortem: [Incident Title]

## Summary

### Incident Reference

<!-- Author prompt: 대상 incident의 사실 기록을 실제 참조로 링크한다. -->

### Review Scope

<!-- Author prompt: 얻은 교훈과 회고 범위를 요약한다. -->

## Root Cause

### Causal Analysis

<!-- Author prompt: 증거를 바탕으로 분석해 근본 원인과 증상을 구분한다. -->

### Contributing Factors

<!-- Author prompt: 기술, 절차, 조직 측면의 기여 요인을 비난 없이 기록한다. -->

#### What Went Wrong

<!-- Author prompt: 틀린 가정과 제대로 작동하지 않은 통제, 탐지, 협업을 밝힌다. -->

## Impact

### Observed Impact

<!-- Author prompt: 확인된 영향만 적는다. -->

### Detection and Response

<!-- Author prompt: incident를 어떻게 탐지했는지, 어떤 대응 결정이 완화를 돕거나 늦췄는지 설명하고 Incident 타임라인의 증거를 인용한다. -->

### What Went Well

<!-- Author prompt: 선택 항목이다. 영향을 줄인 통제나 대응 행동이 있을 때만 밝히고, 없으면 이 절을 지운다. -->

## Corrective Actions

### Actions

<!-- Author prompt: 재발 방지 조치마다 owner, 기한 상태, Task, 증거를 지정하고, 교훈을 요구사항, 결정, Spec, 가이드, 정책 가운데 알맞은 곳으로 보낸다. -->

<!-- Author prompt: 조치별로 owner와 검증을 나눌 때만 아래 Actions 표를 사용하고, 그렇지 않으면 표를 지운다. -->

| Action | Owner | Verification |
| --- | --- | --- |
| Name one corrective action. | Name the owner. | Describe how completion is verified. |

### Verification

<!-- Author prompt: 조치가 재발을 어떻게 막는지와 종료를 어떻게 검증할지 정하고, 조치 owner, 기한 날짜 또는 상태, 완료 증거, 남은 위험을 나열한다. -->

### Lifecycle Traceability

<!-- Author prompt: 원인이나 조치를 owner, 후속 Task, 피드백 대상에 연결한다. -->

| Root cause or action | Owner and due state | Follow-up Task | Feedback target |
| --- | --- | --- | --- |
| Evidence-backed cause or prevention action | owner / due date / state | Task owner | Requirement, ADR, Spec, Guide, or Policy owner |

## Evidence

### Source Records

<!-- Author prompt: incident 기록, 로그, 결정을 실제 참조로 링크한다. -->

### Review Decision

<!-- Author prompt: 종료 승인자와 검토·게시 결정, 미결 사항을 적는다. -->
