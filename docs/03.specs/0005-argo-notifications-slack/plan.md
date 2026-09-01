---
title: 'Argo Notifications Slack Backfill Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
artifact_id: "SPEC-0005-PLAN-0001"
---

# Argo Notifications Slack Backfill Plan

## Overview

This document is the backfill implementation plan for connecting the existing
ArgoCD Notifications Slack execution contract to the PRD/AD/ADR/Spec/Task
chain. It improves document traceability, Secret boundaries, and validation
criteria without runtime changes.

## Context

ArgoCD Notifications is enabled in `infrastructure/argocd/values-local.yaml`,
and the ConfigMap and ExternalSecret are managed through GitOps under
`gitops/platform/argocd/`. However, the AD/Spec/Plan/Task documents linking
the Notifications PRD and ADR were missing, so the credential boundary and
validation path were not traceable from `03.specs`.

### Legacy Task ledger inputs

This document tracks implementation and verification tasks for the ArgoCD
Notifications Slack current-contract backfill. The work is limited to document
traceability and Secret-boundary hardening; live Slack delivery and Vault
writes are out of scope.

- **Parent Spec**: [`../../03.specs/0005-argo-notifications-slack/spec.md`](spec.md)
- **Parent Plan**: [`../plans/2026-05-18-argo-notifications-slack.md`](plan.md)
## Goals & In-Scope

- **Goals**:
  - Backfill the Notifications current contract into the AD/Spec/Plan/Task chain.
  - Clarify the Vault/ESO security boundary for the Slack token.
  - Separate ArgoCD Notifications from Rollouts chart notifications.
- **In Scope**:
  - Document backfill and README index updates
  - Description of the Notifications ConfigMap/ExternalSecret current contract
  - Static validation and live Slack validation boundary

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Issuing a Slack token or writing to Vault
  - Adding a new notification channel
  - Enabling Rollouts chart notifications
- **Out of Scope**:
  - live Slack notification test
  - Slack workspace/channel operation
  - Alertmanager/PagerDuty/Email integration

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Write Notifications AD | `docs/02.architecture/descriptions/0005-argo-notifications-slack.md` | REQ-0002-FR-0001..06 | AD includes PRD/ADR/Spec/Plan links |
| PLN-002 | Write Notifications Spec | `docs/03.specs/0005-argo-notifications-slack/spec.md` | REQ-0002-FR-0001..06 | Spec heading/template gate passes |
| PLN-003 | Write Notifications Task | `docs/03.specs/0005-argo-notifications-slack/README.md#task-records` | Acceptance criterion 01..05 | Task defines validation evidence |
| PLN-004 | Update backlinks and README indexes | PRD, ADR, README, operations docs | REQ-0002-FR-0002 | No stale gap text remains |
| PLN-005 | Run validation | validation scripts | Acceptance criterion 02 | Secret scan and static contract pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Secret | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-003 | Contract | static notification contract | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|not created during this PRD remediation" docs/01.requirements` | no matches |

### Legacy Task verification evidence

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Eval Commands**:
  - `rg -n "Follow-up Gap|not created during this PRD remediation" docs/01.requirements`
  - `rg -n "slack_token|slack-token|notifications.enabled" docs/03.specs/0005-argo-notifications-slack/spec.md`
- **Logs / Evidence Location**:
  - Conversation validation output and git diff for this backfill.
  - 2026-05-22 follow-up: `verify-contracts-static.sh` now explicitly validates ArgoCD Notifications enablement, ConfigMap Slack service/templates/triggers/default triggers, and the Vault-backed ExternalSecret key/property boundary without checking secret values.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Slack token exposure | High | docs/manifests only reference Vault/ESO keys; run secret scan |
| Confusion with Rollouts chart notifications | High | State `rolloutsChartNotifications.enabled: false` in the Spec |
| Live Slack test mistaken for automatic validation | Medium | Run live validation only from the runbook after human-approved secret preparation |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: repo quality, secret scan, manifest syntax, static contract checks pass.
- **Sandbox / Canary Rollout**: Not applicable for docs-only backfill.
- **Human Approval Gate**: Vault write, Slack token read, live Slack send test require explicit human approval.
- **Rollback Trigger**: validation failure or credential boundary contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `NOTIF-T-001 through NOTIF-T-005` is limited to these Argo Notifications Slack Backfill owners and Task-Table surfaces:
  - `docs/03.specs/0005-argo-notifications-slack/README.md#task-records`
  - `docs/03.specs/0005-argo-notifications-slack/spec.md`
  - `docs/03.specs/0005-argo-notifications-slack/plan.md`
- **Forbidden Paths**: live Kubernetes, Argo CD, Vault, cloud-provider, or notification state; secret values and credentials; and paths outside the Argo Notifications Slack Backfill work-item surfaces.
- **Approval Required**: Human approval is required before Argo Notifications Slack Backfill live reconciliation, direct cluster/provider mutation, secret access, remote notification, deployment, push, merge, or parent-Plan expansion.
- **Static Validation**: Preserve the Argo Notifications Slack Backfill outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Live Validation**: DEFER — Argo Notifications Slack Backfill is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Repository evidence for Argo Notifications Slack Backfill must not read or print Secret data, Vault material, provider credentials, kubeconfigs, auth files, private RTK data, or shell history.
- **Rollback Plan**: Revert the logical Argo Notifications Slack Backfill change set for `NOTIF-T-001 through NOTIF-T-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Argo Notifications Slack Backfill evidence remains in:
  - `docs/03.specs/0005-argo-notifications-slack/README.md#task-records`
  - `docs/03.specs/0005-argo-notifications-slack/spec.md`
  - `docs/03.specs/0005-argo-notifications-slack/plan.md`
## Completion Criteria

- [x] AD, Spec, Plan, Task chain exists for Notifications.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Notifications.
- [x] Verification commands are documented for execution.

## Traceability

- **PRD**: [`../../01.requirements/0002-argo-notifications-slack.md`](../../01.requirements/0002-argo-notifications-slack.md)
- **AD**: [`../../02.architecture/descriptions/0005-argo-notifications-slack.md`](../../02.architecture/descriptions/0005-argo-notifications-slack.md)
- **Spec**: [`../../03.specs/0005-argo-notifications-slack/spec.md`](spec.md)
- **ADR**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Tasks**: [`../tasks/2026-05-18-argo-notifications-slack.md`](README.md#task-records)

### Legacy Task traceability

- **Spec**: [`../../03.specs/0005-argo-notifications-slack/spec.md`](spec.md)
- **Plan**: [`../plans/2026-05-18-argo-notifications-slack.md`](plan.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
