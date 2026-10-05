---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/incident"
status: "detected"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
---

# Incident: [Incident Title]

## Overview

<!-- Author prompt: 관측된 사건, 현재 상태, 대응 범위를 요약한다. -->

## Incident Metadata

<!-- Author prompt: incident ID, 심각도, 시작 또는 탐지 시각, frontmatter status에서 파생한 현재 상태, 영향받은 환경, 다음 점검 시점을 기록한다. 허용 상태값은 Registry의 operation/incident 프로필을 따른다. -->

| Field | Value |
| --- | --- |
| Severity | SEV-1 / SEV-2 / SEV-3 / SEV-4 |
| Started / detected | {{TIMESTAMP}} / {{TIMESTAMP}} |
| Current state | frontmatter `status`의 현재 값 |
| Next checkpoint | {{TIMESTAMP}} or N/A — closed |

## Roles and Coordination

<!-- Author prompt: incident commander, operations lead, communications owner, escalation owner를 적는다. N/A는 이유가 있을 때만 쓴다. -->

## Impact

<!-- Author prompt: 영향받은 사용자와 서비스, 지속 시간, 확인된 한계를 적는다. -->

## Timeline

<!-- Author prompt: 시각이 붙은 관측, 결정, 조치를 사후 추론 없이 기록한다. -->

## Response State

<!-- Author prompt: 현재 맡은 역할, 완화 조치, escalation, 다음 점검 시점을 추적한다. -->

## Evidence

<!-- Author prompt: 비밀이 없는 로그, 지표, 변경, 보존된 산출물을 링크한다. -->

## Follow-up Actions

<!-- Author prompt: owner와 기한 상태가 있는 후속 Task를 만든다. 근본 원인 분석은 여기에서 하지 않는다. -->

## Closure

<!-- Author prompt: resolved 상태일 때만 frontmatter resolved_at에 실제 시간대 포함 시각을 기록하고 해결 증거를 본문에 적는다. 해결 전에는 시각을 미리 채우지 않는다. 종료 owner와 남은 위험을 함께 기록한다. -->

## Traceability

<!-- Author prompt: 타임라인의 조치와 증거를 후속 Task의 owner에 연결한다. -->

### Lifecycle Traceability

| Timeline or action | Evidence | Follow-up Task |
| --- | --- | --- |
| Timestamped observation or response action | Named incident evidence | Task owner or N/A — no follow-up required |
