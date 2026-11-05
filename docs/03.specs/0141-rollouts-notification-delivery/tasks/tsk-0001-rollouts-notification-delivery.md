---
title: "Rollouts Notification Delivery"
version: "0.1.0"
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

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | Validator assertions, Rollouts values, ExternalSecret, ArgoCD ConfigMap | platform | draft | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | REQ-0002, AD-0005, ADR-0012 and runbook text | platform | draft | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | Operator live observation | operator | draft | NOT_RUN | EVD-003 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RND-001](../spec.md#success-criteria--verification-plan), [VAL-RND-002](../spec.md#success-criteria--verification-plan) | WORK-001 | `bash scripts/validate-infrastructure-contracts.sh` before and after; `helm template` | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RND-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RND-004](../spec.md#success-criteria--verification-plan) | WORK-003 | Operator Slack observation | Pending | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RND-001](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-RND-002](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-001 | platform |
| [VAL-RND-003](../spec.md#success-criteria--verification-plan) | pending | none | Run EVD-002 | platform |
| [VAL-RND-004](../spec.md#success-criteria--verification-plan) | pending | none | Operator observes a message | operator |

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

Not run yet.
