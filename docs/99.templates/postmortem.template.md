---
title: 'Postmortem: {Incident Title}'
type: postmortem
status: draft
owner: '{team-or-person}'
updated: YYYY-MM-DD
---

<!-- Target: docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md -->

# Postmortem: [Incident Title]

> Use this template for `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md`.
>
> Rules:
>
> - Analyze root cause and prevention after the incident is stabilized.
> - Keep factual incident chronology linked to the Incident document.
> - Use relative links only, calculated from the final authored document location.
> - Keep placeholder or optional target paths as code literals until the target exists.

---

## Overview (KR)

이 문서는 사고의 구조적 원인과 재발 방지 조치를 분석하는 Postmortem 문서다. 비난 없는 분석과 시스템 개선에 집중한다.

## Incident Summary

| Field             | Value                                                      |
| ----------------- | ---------------------------------------------------------- |
| Incident ID       | `INC-YYYYMMDD-XXX`                                         |
| Incident Date     | `YYYY-MM-DD`                                               |
| Analysis Date     | `YYYY-MM-DD`                                               |
| Severity          | `SEV-1 / SEV-2 / SEV-3`                                    |
| Incident Document | `[../../YYYY/YYYY-MM-DD-<incident>.md]` |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Impact

- **Affected Users or Systems**:
- **Operational Impact**:
- **Business / Maintenance Impact**:

## Timeline

| Time (UTC) | Event                                               |
| ---------- | --------------------------------------------------- |
| HH:MM      | [Detection / investigation / mitigation / resolved] |

## Root Cause Analysis

### Primary Root Cause

[Systemic cause.]

### Contributing Factors

- [Factor 1]
- [Factor 2]

### Detection Gaps

- [Gap 1]
- [Gap 2]

## What Went Well

- [Point 1]

## What Went Wrong

- [Point 1]

## Action Items

| Action        | Owner  | Priority | Ticket / Reference | Status  |
| ------------- | ------ | -------- | ------------------ | ------- |
| [Action item] | [Name] | High     | [Link]             | Pending |

## Prevention and Verification

- [Prevention work]
- [Verification rule]

## Required Documentation Feedback Loop

- **ADR updates**:
- **Spec updates**:
- **Operation updates**:
- **Runbook updates**:
- **Guardrail / Eval updates**:

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md`.

- **Runbook**: `[../../../runbooks/####-<topic>.md]`
- **Operation**: `[../../../policies/####-<policy-or-standard>.md]`
- **Incident**: `[../../YYYY/YYYY-MM-DD-<incident>.md]`
- **Spec**: `[../../../../03.specs/<feature-id>/spec.md]`
- **Related ADRs**: `[../../../../02.architecture/decisions/####-<short-title>.md]`
