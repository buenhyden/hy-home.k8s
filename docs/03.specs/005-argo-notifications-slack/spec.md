---
title: 'Argo Notifications Slack Technical Specification'
type: spec
status: active
owner: platform-team
updated: 2026-05-21
---

# Argo Notifications Slack Specification

## Overview (KR)

이 문서는 ArgoCD Notifications 기반 Slack 알림의 현재 repo-backed 기술 계약을 정의한다.
ArgoCD Helm values, Notifications ConfigMap, Vault-backed ExternalSecret, default subscriptions, 앱별 opt-in annotation을 구현과 검증의 기준으로 고정한다.

## Strategic Boundaries & Non-goals

- **Owns**: ArgoCD Notifications 활성화, Slack service template, triggers, Vault/ESO credential reference, validation evidence.
- **Does Not Own**: Slack workspace/channel 관리, Rollouts chart notifications, PagerDuty/Email/Alertmanager integration.
- **Non-goals**: 평문 credential bootstrap, per-app 자동 channel routing, live Slack test without human-approved secret.

## Related Inputs

- **PRD**: [`../../01.requirements/2026-05-17-argo-notifications-slack.md`](../../01.requirements/2026-05-17-argo-notifications-slack.md)
- **ARD**: [`../../02.architecture/requirements/0005-argo-notifications-slack.md`](../../02.architecture/requirements/0005-argo-notifications-slack.md)
- **Related ADRs**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md)

## Contracts

- **Config Contract**:
  - ArgoCD Helm values: `infrastructure/argocd/values-local.yaml`
  - `notifications.enabled: true`
  - Notifications ConfigMap: `gitops/platform/argocd/argocd-notifications-cm.yaml`
  - Notifications ExternalSecret: `gitops/platform/argocd/argocd-notifications-secret.yaml` # pragma: allowlist secret
  - Vault remote key: `platform/notifications`
  - Vault property: `slack_token`
  - Kubernetes Secret key: `slack-token` # pragma: allowlist secret
- **Data / Interface Contract**:
  - Slack service reads `$slack-token`.
  - Default triggers: `on-health-degraded`, `on-sync-failed`.
  - App opt-in annotation: `notifications.argoproj.io/subscribe.<trigger>.slack: <channel>`.
  - Runtime controller: `argocd-notifications-controller`.
- **Governance Contract**:
  - Slack token values never appear in Git.
  - Vault writes are human-approved external bootstrap only.
  - Rollouts chart notifications remain disabled; Rollouts event notification templates live in ArgoCD Notifications ConfigMap.

## Core Design

- **Component Boundary**:
  - ArgoCD Helm values activate the built-in Notifications controller.
  - GitOps ConfigMap owns templates and triggers.
  - ExternalSecret owns secret material synchronization.
  - Applications opt into non-default channel behavior with annotations.
- **Key Dependencies**:
  - ArgoCD Helm release.
  - External Secrets Operator and Vault `vault-backend`.
  - Slack workspace token and channel permissions.
  - Rollouts events where rollout-specific templates are used.
- **Tech Stack**:
  - ArgoCD Notifications, ESO, Vault KV, Slack API, Kubernetes ConfigMap/Secret.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Credential reference: `remoteRef.key=platform/notifications`, `property=slack_token`.
  - Config entries: `service.slack`, `template.*`, `trigger.*`, `defaultTriggers`.
  - Application annotations declare optional subscriptions.
- **Migration / Transition Plan**:
  - Existing GitOps ConfigMap and ExternalSecret remain the source of truth.
  - Future channels must add template/service entries through PR and update operations policy/runbook.

## Interfaces & Data Structures

### Core Interfaces

```yaml
notifications:
  argocdHelmValues: infrastructure/argocd/values-local.yaml
  enabled: true
  configMap: gitops/platform/argocd/argocd-notifications-cm.yaml
  secret:
    externalSecret: gitops/platform/argocd/argocd-notifications-secret.yaml
    vaultKey: platform/notifications
    vaultProperty: slack_token
    kubernetesKey: slack-token
  defaults:
    - on-health-degraded
    - on-sync-failed
  appOptInAnnotation: notifications.argoproj.io/subscribe.<trigger>.slack
  rolloutsChartNotifications:
    enabled: false
```

## API Contract (If Applicable)

This feature does not expose a repository-owned external API.
The interface contract is ArgoCD Notifications ConfigMap syntax, ESO remote references, and application annotations.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: 문서/manifest 유지보수 보조자는 notification wiring을 검증하되 credential material을 조회하거나 출력하지 않는다.
- **Inputs**: PRD/ARD/ADR, ArgoCD values, ConfigMap, ExternalSecret, operations policy/runbook.
- **Outputs**: documentation, non-secret manifest diffs, validation evidence.
- **Success Definition**: Slack notification contract is traceable without exposing credentials.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `bash scripts/check-secret-handling.sh .`, `bash infrastructure/tests/verify-contracts-static.sh`, runtime `kubectl` checks for human/operator use.
- **Permission Boundary**: no Vault writes, Slack token reads, or live notification tests without explicit approval.
- **Failure Handling**: static mismatch is fixed through PR; runtime send failures route to the runbook.

## Prompt / Policy Contract (If Applicable)

- Do not replace `$slack-token` with a real token.
- Do not enable Rollouts chart notifications when working on ArgoCD Notifications.
- Do not mention actual Slack channels unless they are already non-secret repository policy.

## Memory & Context Strategy (If Applicable)

- Record reusable doc-chain and secret-handling lessons in `docs/00.agent-governance/memory/progress.md`.
- Do not create standalone memory docs for this backfill.

## Guardrails (If Applicable)

- **Input Guardrails**: verify all credential paths from repo files, not memory or logs.
- **Output Guardrails**: secret-like literals must remain placeholders or references.
- **Blocked Conditions**: missing Vault secret blocks live Slack validation, not static docs validation.
- **Escalation Rule**: credential bootstrap or Slack workspace permission change requires a human.

## Evaluation (If Applicable)

- **Eval Types**: static secret scan, static contract verification, runtime controller/ExternalSecret/log checks.
- **Metrics**: validation gate pass/fail; ExternalSecret Ready; controller Pod Running; Slack send/error log evidence.
- **Datasets / Fixtures**: non-secret templates in `argocd-notifications-cm.yaml`.
- **How to Run**: use verification commands below and the related runbook for live checks.

## Edge Cases & Error Handling

- Empty Slack token causes controller send errors even when ConfigMap syntax is valid.
- ExternalSecret Ready=False indicates Vault path, property, or ESO connectivity drift.
- Rollouts event templates may not fire if the event context is unavailable; application health/sync triggers remain the default baseline.
- App annotations can route to invalid channels if Slack permissions are missing.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: Notifications controller is not running.
  - **Fallback**: verify `notifications.enabled: true`, ArgoCD sync state, and Pod events.
  - **Human Escalation**: chart value changes require PR review.
- **Failure Mode**: Slack sends fail.
  - **Fallback**: verify ExternalSecret readiness and controller logs without printing token values.
  - **Human Escalation**: Vault token bootstrap and Slack permission repair require a human.

## Verification Commands

```bash
bash scripts/check-secret-handling.sh .
bash infrastructure/tests/verify-contracts-static.sh
kubectl -n argocd get pods | grep notification
kubectl -n argocd get externalsecret argocd-notifications-secret
kubectl -n argocd logs deploy/argocd-notifications-controller --tail=50 | grep -i 'slack\|error\|sent'
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: ArgoCD Helm values keep `notifications.enabled: true`.
- **VAL-SPC-002**: `argocd-notifications-cm` defines Slack service, required templates, triggers, and default triggers.
- **VAL-SPC-003**: `argocd-notifications-secret` references Vault key/property without plaintext token material.
- **VAL-SPC-004**: secret handling scan returns zero plaintext credential findings.
- **VAL-SPC-005**: runtime validation, when intentionally run, shows controller readiness and Slack send/error evidence.

## Related Documents

- **PRD**: [`../../01.requirements/2026-05-17-argo-notifications-slack.md`](../../01.requirements/2026-05-17-argo-notifications-slack.md)
- **ARD**: [`../../02.architecture/requirements/0005-argo-notifications-slack.md`](../../02.architecture/requirements/0005-argo-notifications-slack.md)
- **Related ADRs**: [`../../02.architecture/decisions/0012-argo-notifications-slack.md`](../../02.architecture/decisions/0012-argo-notifications-slack.md), [`../../02.architecture/decisions/0003-eso-vault-k8s-auth.md`](../../02.architecture/decisions/0003-eso-vault-k8s-auth.md)
- **Plan**: [`../../04.execution/plans/2026-05-18-argo-notifications-slack.md`](../../04.execution/plans/2026-05-18-argo-notifications-slack.md)
- **Tasks**: [`../../04.execution/tasks/2026-05-18-argo-notifications-slack.md`](../../04.execution/tasks/2026-05-18-argo-notifications-slack.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
- **Operations Policy**: [`../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`](../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md)
