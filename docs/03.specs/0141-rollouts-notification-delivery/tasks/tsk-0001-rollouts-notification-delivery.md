---
title: "Rollouts Notification Delivery"
version: "0.4.1"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0141-TSK-0001"
parent_ids: ["SPEC-0141-PLAN-0001"]
---

# Task: Rollouts Notification Delivery

## Overview

Deliver Argo Rollouts completion and abort events to the shared Slack
channel through the Rollouts notification engine. It executes
[SPEC-0141](../spec.md) through [WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-05): handle the two open items, Rollouts notification
  delivery and approval of the four Requirement Packages. The approvals were
  committed in `ab5bcd66`; this Task covers the delivery.
- Decision: [ADR-0054](../../../02.architecture/decisions/0054-platform-decision-current-state-amendment.md)
  clause 2, accepted in `ab5bcd66`.
- Start: branch `docs/requirements-conformance` at `ab5bcd66`.
- Approval (2026-11-05): the operator's request to handle the open
  Rollouts delivery item approves SPEC-0141 and its Plan after review of the
  draft in `401c5e72`. It authorizes the repository change only.
- Correction (2026-11-05): after EVD-008, the Spec's Contracts and Core
  Design now state that the chart values define both triggers and templates.
- Acceptance (2026-11-06): the operator accepted VAL-RND-001 to VAL-RND-003
  and asked to observe the live Slack delivery, which needs the change on
  `main` first.
- Acceptance (2026-11-06): the operator's instruction to record VAL-RND-004
  as accepted once a message arrives, and their report of the 7:59 AM
  message, accept VAL-RND-004.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | Validator assertions, Rollouts values, ExternalSecret, ArgoCD ConfigMap | platform | completed | PASS | EVD-004, EVD-005, EVD-006, EVD-008, EVD-009, EVD-010, EVD-011 |
| WORK-002 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | REQ-0002, AD-0005, ADR-0012 and runbook text | platform | completed | PASS | EVD-007 |
| WORK-003 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | Operator live observation | operator | completed | PASS | EVD-016 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` before and after; `helm template` | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` (GNU bash 5.2) after changing only its assertions | Working tree on `6793346c` with the old manifests | FAIL | Local run, 2026-11-05T12:19Z, exit 1: `required file not found: gitops/platform/eso/rollouts-notification-secret.yaml`, as expected | no | none |
| EVD-005 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` before and after; `helm template` | Working tree on `6793346c` with the new manifests | PASS | Local run, exit 0; negative probes (a `trigger.on-rollout-aborted` key in `argocd-notifications-cm`, a changed `$slack-token` reference) each exit 1; `shellcheck` 0.9.0 clean; `helm template` v3.22.0 renders the values as EVD-006 records | yes | EVD-001 |
| EVD-006 | [VAL-RND-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `helm template` (v3.22.0) of `argo-rollouts` 2.40.9 with the Application values; `kubectl kustomize` of `gitops/platform/eso` and `gitops/platform/argocd` | Working tree on `6793346c` | PASS | Local run; `argo-rollouts-notification-configmap` renders `service.slack` (`token: $slack-token`) and one subscription of `on-rollout-completed` and `on-rollout-aborted` to `slack:hy-home-alerts`; both kustomizations build | yes | none |
| EVD-007 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Staged index on `6793346c` | PASS | Local run, every gate PASS; platform-assurance-depth keeps its usual CRD-schema and live-observation DEFER rows; `python3 scripts/qa.py staged` with the validation venv from `.github/requirements/ci-validation.txt` | yes | EVD-002 |
| EVD-008 | [VAL-RND-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent review of the implementing change | Commit `e6c4c065` | FAIL | gitops-reviewer report: the Rollouts controller ships no triggers or templates, so with only `notifiers` and `subscriptions` nothing is sent; EVD-005 and EVD-006 prove the static contract and render only, not delivery | yes | none |
| EVD-009 | [VAL-RND-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` after adding trigger and template assertions | Working tree on `e6c4c065` | FAIL | Local run, 2026-11-05T13:20Z, exit 1: `pattern not found ... trigger\.on-rollout-completed`, as expected | no | none |
| EVD-010 | [VAL-RND-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` and `helm template` (v3.22.0) of `argo-rollouts` 2.40.9 | Working tree on `e6c4c065` with the triggers and templates | PASS | Local run, exit 0; the rendered ConfigMap holds `service.slack`, `subscriptions`, both `trigger.on-rollout-*` and both `template.rollout-*` keys; `shellcheck` clean | yes | none |
| EVD-011 | [VAL-RND-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent review of the implementing change | Commit `d708b826` | PASS | gitops-reviewer re-review: both triggers map to the `RolloutCompleted` and `RolloutAborted` event reasons, the templates use only fields of the Rollouts context, the attachments JSON is valid, and the rendered ConfigMap sends both events; two wording defects fixed in the closing change | yes | EVD-008 |
| EVD-012 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | `main` at `04e23039` (PR #207 merged 2026-11-05T15:41Z), context `k3d-hyhome` | DEFER | 2026-11-05T15:43Z read-only `kubectl`: Argo CD Applications `platform-rollouts` and `platform-eso-config` report sync `Unknown` with `ComparisonError`; the repo server cannot resolve `github.com` or fetch the `argo-helm` chart (`lookup github.com on 10.43.0.10:53: server misbehaving`); CoreDNS forwards to the node `/etc/resolv.conf` while the host resolves `github.com`; the change is not deployed, so no Rollouts message can be sent. Resume after cluster DNS egress is restored and Argo CD syncs; next owner: operator | yes | none |
| EVD-013 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | `main` at `04e23039`, context `k3d-hyhome`, after the operator restarted `k3d-hyhome-agent-0` | DEFER | 2026-11-05T16:01Z read-only `kubectl`: node DNS resolves `github.com` again; Argo CD synced `platform-rollouts` and `platform-eso-config`; `argo-rollouts-notification-configmap` holds `service.slack`, `subscriptions`, both `trigger.on-rollout-*` and both `template.rollout-*` keys. Delivery is still blocked: ClusterSecretStore `vault-backend` reports `Ready=False InvalidProviderConfig` since 2026-11-02T04:34Z, so every ExternalSecret, including `argo-rollouts-notification-secret`, reports `SecretSyncedError`. Resume after the store recovers (RUN-0002); next owner: operator | yes | none |
| EVD-014 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | `main` at `c26f9b14`, context `k3d-hyhome`, after the operator unsealed OpenBao | DEFER | 2026-11-05T16:13Z: OpenBao had been sealed since its 2026-11-02T07:22Z restart, so the external Traefik dropped its route and the ESO login got a 404; after the operator unsealed it, `vault-backend` reports `Ready=True` and all seven ExternalSecrets, including `argo-rollouts-notification-secret`, report `SecretSynced`. 2026-11-05T16:20Z: the operator patched a test annotation onto the `apps/adminer` pod template; revision 6 passed its canary steps and analysis, and at 16:23:40Z the controller fired `on-rollout-completed` to `slack:hy-home-alerts`, but Slack rejected it with `invalid_auth`; `argocd-notifications-controller` reports the same `invalid_auth` with the same `platform/notifications` `slack_token`. The trigger, template and subscription work; the token is not valid. Resume after the operator replaces `slack_token` in OpenBao; next owner: operator | yes | none |
| EVD-015 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | `main` at `1a34b3d3`, context `k3d-hyhome`, after the operator replaced `slack_token` (OpenBao `platform/notifications` version 2, 22:49Z) and force-synced both ExternalSecrets | DEFER | The new token passes Slack `auth.test`; at 22:54:37Z revision 8 of `apps/adminer` (annotation `hy-home/notify-test=retest-1`) completed and the controller fired `on-rollout-completed`, but Slack answered `not_in_channel`: the bot was not a member of `#hy-home-alerts`. Resume after the operator invites the bot; next owner: operator | yes | none |
| EVD-016 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | `main` at `1a34b3d3`, context `k3d-hyhome`, after the operator invited the bot to `#hy-home-alerts` | PASS | 2026-11-05T22:59:30Z: revision 9 of `apps/adminer` (annotation `retest-2`) completed all six canary steps, the controller logged no send error, and the operator observed "Rollout adminer has been completed." with namespace `apps` and image `adminer:4.8.1` in `#hy-home-alerts` at 7:59 AM KST | yes | EVD-003, EVD-012, EVD-013, EVD-014, EVD-015 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RND-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-010, EVD-011 | Operator accepted on 2026-11-06 | platform |
| [VAL-RND-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-005 | Operator accepted on 2026-11-06 | platform |
| [VAL-RND-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Operator accepted on 2026-11-06 | platform |
| [VAL-RND-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-016 | Operator observed the message and accepted on 2026-11-06 | operator |

## Approval and Safety Boundaries

- **Allowed Paths**: `gitops/apps/root/platform-rollouts-app.yaml`,
  `gitops/platform/eso/`, `gitops/platform/argocd/argocd-notifications-cm.yaml`,
  `scripts/validate-infrastructure-contracts.sh`, `docs/01.requirements/0002-argo-notifications-slack.md`,
  `docs/02.architecture/`, `docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`,
  `docs/03.specs/`
- **Forbidden Paths**: `secrets/`, any OpenBao write
- **Approval Required**: the operator's 2026-11-05 request authorizes the
  repository change; writing the OpenBao entry and any live action stay with
  the operator.
- **Static Validation**: `bash scripts/validate-infrastructure-contracts.sh`,
  strict document checks, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER — operator observation of a Rollouts message
- **Secret / Vault Handling**: no token is read or printed; the ExternalSecret
  references `platform/notifications` only
- **Rollback Plan**: revert the implementing commit
- **Evidence Location**: this Task

## Verification Summary

- Repository-static lanes: PASS (EVD-005 to EVD-007). The validator was
  changed first and failed on the old manifests (EVD-004).
- Acceptance: the operator accepted VAL-RND-001 to VAL-RND-004 on
  2026-11-06.
- Live lane: PASS (EVD-016). Earlier attempts were blocked by node DNS,
  the sealed OpenBao, an invalid Slack token and the bot's missing channel
  membership (EVD-012 to EVD-015); the operator cleared each one.
- Review: EVD-008 found that the first change sent nothing because the
  controller has no default triggers or templates; the fix defines both
  (EVD-010), and the re-review passed (EVD-011).
- Residual risk: only the completion message was observed live; the abort
  path shares the same service, subscription and token.
- Rollback: revert the implementing commit.
