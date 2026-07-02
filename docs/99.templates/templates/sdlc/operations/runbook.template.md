---
title: '{Topic Name} Runbook'
type: sdlc/runbook
status: draft
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/05.operations/runbooks/####-<topic>.md -->

# [Topic Name] Runbook

> Use this template for `docs/05.operations/runbooks/####-<topic>.md`.
>
> Rules:
>
> - This document exists for immediate execution.
> - This document is not a policy definition.
> - This document is not a tutorial-first guide.
> - If the main purpose is analysis after the event, write a Postmortem instead.
> - Use relative links only, calculated from the final authored document location.
> - Keep placeholder or optional target paths as code literals until the target exists.

---

## Runbook Type

`bootstrap | recovery | maintenance | hotfix | onboarding | troubleshooting`

## Overview

이 런북은 [서비스 또는 워크플로명]에 대한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

## Purpose

[What operational problem this runbook addresses.]

## Canonical References

- `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- `[../../02.architecture/decisions/####-<short-title>.md]`
- `[../../03.specs/<feature-id>/spec.md]`
- `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`

## When to Use

- [Use case 1]
- [Use case 2]

## Procedure or Checklist

### Checklist

- [ ] [Check 1]
- [ ] [Check 2]

### Procedure

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Verification Steps

- [ ] [Verification command or manual check]

## Observability and Evidence Sources

- **Signals**:
- **Evidence to Capture**:

## Safe Rollback or Recovery Procedure

- [ ] [Recovery step 1]
- [ ] [Recovery step 2]

## Agent Operations (If Applicable)

- **Prompt Rollback**:
- **Model Fallback**:
- **Tool Disable / Revoke**:
- **Eval Re-run**:
- **Trace Capture**:

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/05.operations/runbooks/####-<topic>.md`.

- **Incident examples**: `[../incidents/YYYY/INC-###-<title>/INC-###-<title>.md]`
- **Postmortem examples**: `[../incidents/YYYY/INC-###-<title>/postmortem.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Related ADRs**: `[../../02.architecture/decisions/####-<short-title>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **Operation**: `[../policies/####-<policy-or-standard>.md]`
