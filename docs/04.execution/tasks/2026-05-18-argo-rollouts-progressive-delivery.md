---
title: 'Task: Argo Rollouts Progressive Delivery Backfill'
type: task
status: done
owner: platform
updated: 2026-05-22
---

# Task: Argo Rollouts Progressive Delivery Backfill

## Overview (KR)

이 문서는 Argo Rollouts current contract backfill의 구현·검증 작업 목록이다.
작업 대상은 문서 추적성 보강이며, live cluster 변경은 포함하지 않는다.

## Inputs

- **Parent Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Parent Plan**: [`../plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../plans/2026-05-18-argo-rollouts-progressive-delivery.md)

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `03.specs/`, this document remains the execution-tracking source of truth.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ROL-T-001 | Add Rollouts ARD | doc | Related Inputs | PLN-001 | ARD exists and links PRD/ADR/Spec/Plan | platform-team | Done |
| ROL-T-002 | Add Rollouts Spec | doc | Contracts | PLN-002 | `validate-repo-quality-gates.sh` template heading check | platform-team | Done |
| ROL-T-003 | Add Rollouts Plan and Task | doc | Related Documents | PLN-003 | Plan/Task links resolve | platform-team | Done |
| ROL-T-004 | Update upstream/downstream links | doc | Related Documents | PLN-004 | stale gap grep returns no matches | platform-team | Done |
| ROL-T-005 | Run static validation gates | test | Verification | PLN-005 | validation commands PASS | platform-team | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Eval Commands**:
  - `rg -n "Follow-up Gap|이번 PRD 정비에서 생성하지 않음" docs/01.requirements`
  - `rg -n "notifications.enabled: false|notifications.enabled: true" docs/03.specs/004-argo-rollouts-progressive-delivery/spec.md docs/03.specs/005-argo-notifications-slack/spec.md`
- **Logs / Evidence Location**:
  - Conversation validation output and git diff for this backfill.
  - 2026-05-22 follow-up: `verify-contracts-static.sh` now explicitly validates the `platform-rollouts` Application, `argo-rollouts` namespace, AppProject permissions, dashboard TLS host/secret, chart notifications disabled boundary, and metrics NodePort contract.

## Related Documents

- **Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Plan**: [`../plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
