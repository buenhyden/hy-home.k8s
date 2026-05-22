---
title: 'Incident: {Incident Title}'
type: incident
status: draft
owner: '{team-or-person}'
updated: YYYY-MM-DD
---

<!-- Target: docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md -->

# Incident: [Incident Title]

INC-YYYYMMDD-XXX / [Short Incident Title]

> Use this template for `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md`.
>
> Rules:
>
> - Record facts, status, and response state.
> - Separate confirmed facts from current hypotheses.
> - Do not place the final root cause analysis here; move that to the Postmortem.
> - Use relative links only, calculated from the final authored document location.
> - Keep placeholder or optional target paths as code literals until the target exists.

---

## Overview (KR)

이 문서는 사고의 영향, 현재 상태, 주요 대응 흐름을 기록하는 Incident 문서다. 사실 기록과 대응 로그에 집중한다.

## Incident Metadata

| Field           | Value                                                                      |
| --------------- | -------------------------------------------------------------------------- |
| Incident ID     | `INC-YYYYMMDD-XXX`                                                         |
| Severity        | `SEV-1 / SEV-2 / SEV-3`                                                    |
| Status          | `Investigating / Identified / Mitigating / Monitoring / Resolved / Closed` |
| Detection Time  | `YYYY-MM-DD HH:MM UTC`                                                     |
| Primary Service | [Affected service]                                                         |
| Evidence Source | [Log / dashboard / report]                                                 |
| Runbook Link    | `[../../runbooks/####-<topic>.md]`                                         |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Incident Summary

[Short summary.]

## Impact

- [Impact 1]
- [Impact 2]

## Timeline

| Time (UTC) | Actor  | Detail          |
| ---------- | ------ | --------------- |
| HH:MM      | [Name] | [What happened] |

## Current Hypothesis / Response State

- **Current Hypothesis**:
- **Mitigation Actions**:
- **Resolution State**:

## Evidence

- [Evidence 1]
- [Evidence 2]

## Follow-up Actions

- [ ] [Action] — Owner: [Name]

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md`.

- **Postmortem**: `[../postmortems/YYYY/YYYY-MM-DD-<incident>.md]`
- **Spec**: `[../../../03.specs/<feature-id>/spec.md]`
- **Related ADRs**: `[../../../02.architecture/decisions/####-<short-title>.md]`
- **Runbook**: `[../../runbooks/####-<topic>.md]`
- **Operation**: `[../../policies/####-<policy-or-standard>.md]`
