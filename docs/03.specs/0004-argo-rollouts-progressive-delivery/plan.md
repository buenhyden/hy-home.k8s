---
title: 'Argo Rollouts Progressive Delivery Backfill Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-07-13
artifact_id: "SPEC-0004-PLAN-0001"
---

# Argo Rollouts Progressive Delivery Backfill Plan

## Overview

This document is the backfill implementation plan for connecting the existing
Argo Rollouts execution contract to the PRD/AD/ADR/Spec/Task chain. It
improves document traceability and static validation criteria without runtime
changes.

## Context

The `platform-rollouts` Application, AppProject permissions, Rollouts Dashboard
route, metrics NodePort, and reference workload already exist in GitOps docs
and manifests. However, the AD/Spec/Plan/Task documents linking the Rollouts
PRD and ADR were missing, making the implementation contract hard to find from
the `03.specs` stage.

### Legacy Task ledger inputs

This document tracks implementation and verification tasks for the Argo
Rollouts current-contract backfill. The work is limited to document
traceability hardening; live cluster changes are out of scope.

- **Parent Spec**: [`../../03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](spec.md)
- **Parent Plan**: [`../plans/2026-05-18-argo-rollouts-progressive-delivery.md`](plan.md)
## Goals & In-Scope

- **Goals**:
  - Backfill the Rollouts current contract into the AD/Spec/Plan/Task chain.
  - Separate ownership for Rollouts chart notifications and ArgoCD Notifications.
  - Make validation commands and operations document links traceable through one path.
- **In Scope**:
  - Document backfill and README index updates
  - Description of the `platform-rollouts` current contract
  - Static validation and live validation boundary

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Adding new Rollouts functionality
  - Changing automatic promotion policy
  - Enabling Rollouts chart notifications
- **Out of Scope**:
  - live cluster mutation
  - Per-workload Rollout migration
  - Slack credential bootstrap

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Write Rollouts AD | `docs/02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md` | REQ-0001-FR-0001 | AD includes PRD/ADR/Spec/Plan links |
| PLN-002 | Write Rollouts Spec | `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md` | REQ-0001-FR-0001..06 | Spec heading/template gate passes |
| PLN-003 | Write Rollouts Task | `docs/03.specs/0004-argo-rollouts-progressive-delivery/README.md#task-records` | Acceptance criterion 01..04 | Task defines validation evidence |
| PLN-004 | Update backlinks and README indexes | PRD, ADR, README, operations docs | REQ-0001-IF-0001 | No stale gap text remains |
| PLN-005 | Run validation | validation scripts | Acceptance criterion 04 | All static validation passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | GitOps | Rollouts Application and kustomization structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-003 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-004 | Contract | platform static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|not created during this PRD remediation" docs/01.requirements` | no matches |

### Legacy Task verification evidence

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Eval Commands**:
  - `rg -n "Follow-up Gap|not created during this PRD remediation" docs/01.requirements`
  - `rg -n "notifications.enabled: false|notifications.enabled: true" docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md docs/03.specs/0005-argo-notifications-slack/spec.md`
- **Logs / Evidence Location**:
  - Conversation validation output and git diff for this backfill.
  - 2026-05-22 follow-up: `verify-contracts-static.sh` now explicitly validates the `platform-rollouts` Application, `argo-rollouts` namespace, AppProject permissions, dashboard TLS host/secret, chart notifications disabled boundary, and metrics NodePort contract.
## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Backfill document mistaken for future implementation | High | Keep status active and state current-contract backfill at the top |
| Rollouts chart notifications are enabled by mistake | High | Separate chart notifications disabled state and ArgoCD Notifications ownership in the Spec |
| Live validation runs as if it were static validation | Medium | Separate live `kubectl`/`curl` evidence into runbook evidence |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: repo quality, GitOps structure, manifest syntax, static contract checks pass.
- **Sandbox / Canary Rollout**: Not applicable for docs-only backfill.
- **Human Approval Gate**: Live promotion, abort, undo, or cluster mutation requires explicit human approval.
- **Rollback Trigger**: validation failure or stale current/historical contradiction.
- **Prompt / Model Promotion Criteria**: Not applicable.

### Legacy Task approval and rollback boundaries

- **Allowed Paths**: `ROL-T-001 through ROL-T-005` is limited to these Argo Rollouts Progressive Delivery Backfill owners and Task-Table surfaces:
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/README.md#task-records`
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/plan.md`
- **Forbidden Paths**: live Kubernetes, Argo CD, Vault, cloud-provider, or notification state; secret values and credentials; and paths outside the Argo Rollouts Progressive Delivery Backfill work-item surfaces.
- **Approval Required**: Human approval is required before Argo Rollouts Progressive Delivery Backfill live reconciliation, direct cluster/provider mutation, secret access, remote notification, deployment, push, merge, or parent-Plan expansion.
- **Static Validation**: Preserve the Argo Rollouts Progressive Delivery Backfill outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
- **Live Validation**: DEFER — Argo Rollouts Progressive Delivery Backfill is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: Repository evidence for Argo Rollouts Progressive Delivery Backfill must not read or print Secret data, Vault material, provider credentials, kubeconfigs, auth files, private RTK data, or shell history.
- **Rollback Plan**: Revert the logical Argo Rollouts Progressive Delivery Backfill change set for `ROL-T-001 through ROL-T-005` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Argo Rollouts Progressive Delivery Backfill evidence remains in:
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/README.md#task-records`
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/spec.md`
  - `docs/03.specs/0004-argo-rollouts-progressive-delivery/plan.md`
## Completion Criteria

- [x] AD, Spec, Plan, Task chain exists for Rollouts.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Rollouts.
- [x] Verification commands are documented for execution.

## Traceability

- **PRD**: [`../../01.requirements/0001-argo-rollouts-progressive-delivery.md`](../../01.requirements/0001-argo-rollouts-progressive-delivery.md)
- **AD**: [`../../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md`](../../02.architecture/descriptions/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../../03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](spec.md)
- **ADR**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **Tasks**: [`../tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](plan.md)

### Legacy Task traceability

- **Spec**: [`../../03.specs/0004-argo-rollouts-progressive-delivery/spec.md`](spec.md)
- **Plan**: [`../plans/2026-05-18-argo-rollouts-progressive-delivery.md`](plan.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
