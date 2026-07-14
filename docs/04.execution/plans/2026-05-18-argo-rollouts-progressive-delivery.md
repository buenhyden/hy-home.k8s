---
title: 'Argo Rollouts Progressive Delivery Backfill Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Argo Rollouts Progressive Delivery Backfill Plan

## Overview

This document is the backfill implementation plan for connecting the existing
Argo Rollouts execution contract to the PRD/ARD/ADR/Spec/Task chain. It
improves document traceability and static validation criteria without runtime
changes.

## Context

The `platform-rollouts` Application, AppProject permissions, Rollouts Dashboard
route, metrics NodePort, and reference workload already exist in GitOps docs
and manifests. However, the ARD/Spec/Plan/Task documents linking the Rollouts
PRD and ADR were missing, making the implementation contract hard to find from
the `03.specs` stage.

## Goals & In-Scope

- **Goals**:
  - Backfill the Rollouts current contract into the ARD/Spec/Plan/Task chain.
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
| PLN-001 | Write Rollouts ARD | `docs/02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md` | REQ-PRD-FUN-01 | ARD includes PRD/ADR/Spec/Plan links |
| PLN-002 | Write Rollouts Spec | `docs/03.specs/004-argo-rollouts-progressive-delivery/spec.md` | REQ-PRD-FUN-01..06 | Spec heading/template gate passes |
| PLN-003 | Write Rollouts Task | `docs/04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md` | REQ-PRD-MET-01..04 | Task defines validation evidence |
| PLN-004 | Update backlinks and README indexes | PRD, ADR, README, operations docs | REQ-PRD-FUN-04 | No stale gap text remains |
| PLN-005 | Run validation | validation scripts | REQ-PRD-MET-04 | All static validation passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | docs taxonomy and template headings | `bash scripts/validate-repo-quality-gates.sh .` | PASS |
| VAL-PLN-002 | GitOps | Rollouts Application and kustomization structure | `bash scripts/validate-gitops-structure.sh` | PASS |
| VAL-PLN-003 | Manifest | Kubernetes YAML syntax | `bash scripts/validate-k8s-manifests.sh .` | PASS |
| VAL-PLN-004 | Contract | platform static contracts | `bash infrastructure/tests/verify-contracts-static.sh` | PASS |
| VAL-PLN-005 | Semantic | stale planned-gap text removed | `rg -n "Follow-up Gap\|not created during this PRD remediation" docs/01.requirements` | no matches |

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

## Completion Criteria

- [x] ARD, Spec, Plan, Task chain exists for Rollouts.
- [x] PRD/ADR/operations docs link to the new chain.
- [x] README indexes include Rollouts.
- [x] Verification commands are documented for execution.

## Traceability

- **PRD**: [`../../01.requirements/001-argo-rollouts-progressive-delivery.md`](../../01.requirements/001-argo-rollouts-progressive-delivery.md)
- **ARD**: [`../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md`](../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **ADR**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md)
- **Tasks**: [`../tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](../tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
