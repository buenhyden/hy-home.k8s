---
title: 'Task: Argo Notifications Slack Backfill'
type: sdlc/task
status: done
owner: platform
updated: 2026-05-22
---

# Task: Argo Notifications Slack Backfill

## Overview

This document tracks implementation and verification tasks for the ArgoCD
Notifications Slack current-contract backfill. The work is limited to document
traceability and Secret-boundary hardening; live Slack delivery and Vault
writes are out of scope.

## Inputs

- **Parent Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **Parent Plan**: [`../plans/2026-05-18-argo-notifications-slack.md`](../plans/2026-05-18-argo-notifications-slack.md)

## Working Rules

- Write failing tests first for core behavior.
- Every task must define evidence.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `03.specs/`, this document remains the execution-tracking source of truth.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NOTIF-T-001 | Add Notifications ARD | doc | Related Inputs | PLN-001 | ARD exists and links PRD/ADR/Spec/Plan | platform | Done |
| NOTIF-T-002 | Add Notifications Spec | doc | Contracts | PLN-002 | `validate-repo-quality-gates.sh` template heading check | platform | Done |
| NOTIF-T-003 | Add Notifications Plan and Task | doc | Related Documents | PLN-003 | Plan/Task links resolve | platform | Done |
| NOTIF-T-004 | Update upstream/downstream links | doc | Related Documents | PLN-004 | stale gap grep returns no matches | platform | Done |
| NOTIF-T-005 | Run static validation gates | test | Verification | PLN-005 | validation commands PASS | platform | Done |

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
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Eval Commands**:
  - `rg -n "Follow-up Gap|not created during this PRD remediation" docs/01.requirements`
  - `rg -n "slack_token|slack-token|notifications.enabled" docs/03.specs/005-argo-notifications-slack/spec.md`
- **Logs / Evidence Location**:
  - Conversation validation output and git diff for this backfill.
  - 2026-05-22 follow-up: `verify-contracts-static.sh` now explicitly validates ArgoCD Notifications enablement, ConfigMap Slack service/templates/triggers/default triggers, and the Vault-backed ExternalSecret key/property boundary without checking secret values.

## Related Documents

- **Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **Plan**: [`../plans/2026-05-18-argo-notifications-slack.md`](../plans/2026-05-18-argo-notifications-slack.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
