---
title: "Rollouts Notification Delivery"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-05"
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

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | Validator assertions, Rollouts values, ExternalSecret, ArgoCD ConfigMap | platform | in-progress | PASS | EVD-004, EVD-005, EVD-006 |
| WORK-002 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | REQ-0002, AD-0005, ADR-0012 and runbook text | platform | in-progress | PASS | EVD-007 |
| WORK-003 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | Operator live observation | operator | ready | NOT_RUN | EVD-003 |

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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RND-001](../spec.md#success-criteria--verification-plan) | pending | EVD-005, EVD-006 | Operator decision on PASS evidence | operator |
| [VAL-RND-002](../spec.md#success-criteria--verification-plan) | pending | EVD-004, EVD-005 | Operator decision on PASS evidence | operator |
| [VAL-RND-003](../spec.md#success-criteria--verification-plan) | pending | EVD-007 | Operator decision on PASS evidence | operator |
| [VAL-RND-004](../spec.md#success-criteria--verification-plan) | pending | none | After sync, confirm the OpenBao entry holds `slack_token` and observe a Rollouts message (RUN-0004 Procedure 3) | operator |

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
- Live lane: not run. Delivery needs Argo CD to sync the change and the
  OpenBao `platform/notifications` entry to hold `slack_token`; the operator
  owns VAL-RND-004.
- Review: the independent review is recorded in the implementing change.
- Residual risk: the built-in Rollouts templates replace the removed custom
  Slack attachments, so the message layout differs from the ArgoCD ones.
- Rollback: revert the implementing commit.
