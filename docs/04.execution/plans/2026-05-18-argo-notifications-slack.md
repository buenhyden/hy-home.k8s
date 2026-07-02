---
title: 'Argo Notifications Slack Backfill Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-05-21
---

# Argo Notifications Slack Backfill Plan

## Overview

This document is the backfill implementation plan for connecting the existing
ArgoCD Notifications Slack execution contract to the PRD/ARD/ADR/Spec/Task
chain. It improves document traceability, Secret boundaries, and validation
criteria without runtime changes.

## Context

ArgoCD Notifications is enabled in `infrastructure/argocd/values-local.yaml`,
and the ConfigMap and ExternalSecret are managed through GitOps under
`gitops/platform/argocd/`. However, the ARD/Spec/Plan/Task documents linking
the Notifications PRD and ADR were missing, so the credential boundary and
validation path were not traceable from `03.specs`.

## Goals & In-Scope

- **Goals**:
  - Backfill the Notifications current contract into the ARD/Spec/Plan/Task chain.
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
| PLN-001 | Write Notifications ARD | `docs/02.architecture/requirements/0005-argo-notifications-slack.md` | REQ-PRD-FUN-01..06 | ARD includes PRD/ADR/Spec/Plan links |
| PLN-002 | Write Notifications Spec | `docs/03.specs/005-argo-notifications-slack/spec.md` | REQ-PRD-FUN-01..06 | Spec heading/template gate passes |
| PLN-003 | Write Notifications Task | `docs/04.execution/tasks/2026-05-18-argo-notifications-slack.md` | REQ-PRD-MET-01..05 | Task defines validation evidence |
| PLN-004 | Update backlinks and README indexes | PRD, ADR, README, operations docs | REQ-PRD-FUN-02 | No stale gap text remains |
| PLN-005 | Run validation | validation scripts | REQ-PRD-MET-02 | Secret scan and static contract pass |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | Secret | plaintext secret scan | `bash scripts/check-secret-handling.sh .` | PASS |
| VAL-PLN-003 | Contract | static notification contract | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-004 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|not created during this PRD remediation" docs/01.requirements` | no matches |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Slack token exposure | High | docs/manifests only reference Vault/ESO keys; run secret scan |
| Confusion with Rollouts chart notifications | High | State `rolloutsChartNotifications.enabled: false` in the Spec |
| Live Slack test mistaken for automatic validation | Medium | Run live validation only from the runbook after human-approved secret preparation |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: repo quality, secret scan, manifest syntax, static contract checks pass.
- **Sandbox / Canary Rollout**: Not applicable for docs-only backfill.
- **Human Approval Gate**: Vault write, Slack token read, live Slack send test require explicit human approval.
- **Rollback Trigger**: validation failure or credential boundary contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable.

## Completion Criteria

- [x] ARD, Spec, Plan, Task chain exists for Notifications.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Notifications.
- [x] Verification commands are documented for execution.

## Related Documents

- **PRD**: [`../../01.requirements/2026-05-17-argo-notifications-slack.md`](../../01.requirements/2026-05-17-argo-notifications-slack.md)
- **ARD**: [`../../02.architecture/requirements/0005-argo-notifications-slack.md`](../../02.architecture/requirements/0005-argo-notifications-slack.md)
- **Spec**: [`../../03.specs/005-argo-notifications-slack/spec.md`](../../03.specs/005-argo-notifications-slack/spec.md)
- **ADR**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md)
- **Tasks**: [`../tasks/2026-05-18-argo-notifications-slack.md`](../tasks/2026-05-18-argo-notifications-slack.md)
