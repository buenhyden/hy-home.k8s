---
title: '{Policy or Standard Name} Operations Policy'
type: policy
status: draft
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/05.operations/policies/####-<policy-or-standard>.md -->

# [Policy or Standard Name] Operations Policy

> Use this template for `docs/05.operations/policies/####-<policy-or-standard>.md`.
>
> Rules:
>
> - This document defines policy, controls, and approval rules.
> - This document is not a step-by-step recovery procedure.
> - This document is not an onboarding or how-to guide.
> - This document is not an incident timeline or a postmortem.
> - Keep executable command sequences, recovery steps, and operational checklists
>   in the owning runbook. In this policy, describe the required evidence and
>   link the runbook instead of duplicating the procedure.
> - Use relative links only, calculated from the final authored document location.
> - Keep placeholder or optional target paths as code literals until the target exists.

---

## Overview

이 문서는 [정책명] 운영 정책을 정의한다. 적용 범위, 통제 기준, 예외, 검증 방법을 규정한다.

## Policy Scope

[What this policy governs.]

## Applies To

- **Systems**:
- **Agents**:
- **Environments**:

## Controls

- **Required**:
- **Allowed**:
- **Disallowed**:

## Exceptions

- [Exception rule and approval path]

## Verification

- [Evidence required to prove compliance]
- [Owning runbook for command sequence or recovery procedure]

## Review Cadence

- [Monthly / Quarterly / Per release]

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
- **Eval / Guardrail Threshold**:
- **Log / Trace Retention**:
- **Safety Incident Thresholds**:

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/05.operations/policies/####-<policy-or-standard>.md`.

- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Related ADRs**: `[../../02.architecture/decisions/####-<short-title>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Runbook**: `[../runbooks/####-<topic>.md]`
- **Postmortem**: `[../incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md]`
