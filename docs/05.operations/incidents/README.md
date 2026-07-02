# 05.operations/incidents

> 사고 사실 기록과 postmortem을 보관하는 incident stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 사고 사실 기록과 사고 후 회고를 보관하는 canonical stage다.
실시간 대응 기록과 구조적 재발 방지 분석을 같은 stage 안에서 분리해 보존한다.

Incident Record는 “무슨 일이 있었는가”를 기록한다.
Postmortem은 “왜 허용됐고 무엇을 바꿀 것인가”를 기록한다.
일반 정책은 [policies](../policies/README.md), 실행 복구 절차는 [runbooks](../runbooks/README.md)에 둔다.

현재 tracked incident record와 postmortem 문서는 없다.
첫 사고 기록이 필요할 때만 `YYYY/` 또는 `postmortems/YYYY/` 하위 경로를 만든다.

## Incident Boundary Matrix

| Artifact | Path rule | Template | Creation rule | Current state |
| --- | --- | --- | --- | --- |
| `Incident Record` | `./YYYY/YYYY-MM-DD-<incident>.md` | [incident.template.md](../../99.templates/templates/sdlc/operations/incident.template.md) | Create only for a real incident fact record. | No tracked incident records. |
| `Postmortem` | `./postmortems/YYYY/YYYY-MM-DD-<incident>.md` | [postmortem.template.md](../../99.templates/templates/sdlc/operations/postmortem.template.md) | Create only after incident stabilization when root cause/prevention analysis is needed. | No tracked postmortems. |

## Audience

이 README의 주요 독자:

- Operators
- Incident Commanders
- Platform Engineers
- AI Agents

## Scope

### In Scope

- Incident Record: 영향, 타임라인, 가설, 대응, 증거, 후속 액션
- Postmortem: 근본 원인, 기여 요인, 감지 공백, 재발 방지 액션
- 관련 Runbook, Operation, ADR, Spec 링크

### Out of Scope

- 일반 운영 정책
- 실행 절차 중심 런북
- 기능 요구사항 또는 상세 설계

## Structure

```text
05.operations/incidents/
├── YYYY/              # Incident records, created when the first incident is recorded
├── postmortems/YYYY/  # Postmortems, created when the first postmortem is recorded
└── README.md          # This file
```

## How to Work in This Area

1. 대응 중에는 [incident.template.md](../../99.templates/templates/sdlc/operations/incident.template.md)로 사실 기록을 시작한다.
2. 사고 종료 후 구조 분석이 필요하면 [postmortem.template.md](../../99.templates/templates/sdlc/operations/postmortem.template.md)를 사용한다.
3. Runbook/Operations/ADR/Spec 링크를 남겨 재발 방지 액션을 추적한다.
4. 비밀 값, 토큰, 개인 식별 정보는 사고 기록에 직접 남기지 않는다.
5. 사고가 없는 상태에서는 README만 유지하고 빈 placeholder 파일을 만들지 않는다.

## Record Purpose

이 영역은 운영 중 학습과 대응 기록을 저장한다.

- Incident Record는 장애 또는 이상 상황에서 무엇이 발생했는지, 영향 범위가 무엇인지, 즉시 어떤 대응을 했는지 기록한다.
- Postmortem은 사건 이후 근본 원인, 기여 요인, 재발 방지 조치, 학습 내용을 정리한다.

## Expected Record Shape

기록 문서는 가능한 경우 다음 항목을 포함한다.

- Summary
- Impact
- Affected Systems / Routes
- Timeline
- Root Cause 또는 Current Hypothesis
- Immediate Remediation
- Follow-up Actions
- Related Specs / ADRs / Runbooks / Policies

## Review Expectations

- Incident는 사실 기록과 대응 경위를 빠르게 복원할 수 있어야 한다.
- Postmortem은 비난보다 학습과 재발 방지에 초점을 맞춘다.
- 후속 조치는 Plan 또는 Task와 연결하고, 관련 Policy/Runbook 갱신 필요 여부를 확인한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/05.operations/incidents/`다.

- Incident record는 `./YYYY/YYYY-MM-DD-<incident>.md` 경로를 사용한다.
- Postmortem은 `./postmortems/YYYY/YYYY-MM-DD-<incident>.md` 경로를 사용한다.
- sibling operations folder는 `../policies/`, `../runbooks/`, `../guides/`로 연결한다.

## Related Documents

- [Operations README](../README.md)
- [05.operations/policies](../policies/README.md)
- [05.operations/runbooks](../runbooks/README.md)
- [99.templates](../../99.templates/README.md)
- [Incident Template](../../99.templates/templates/sdlc/operations/incident.template.md)
- [Postmortem Template](../../99.templates/templates/sdlc/operations/postmortem.template.md)
