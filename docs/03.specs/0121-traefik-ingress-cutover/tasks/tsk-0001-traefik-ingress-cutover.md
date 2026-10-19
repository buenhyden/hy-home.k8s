---
title: "Traefik Ingress Cutover Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0121-TSK-0001"
parent_ids: ["SPEC-0121-PLAN-0001"]
---

# Task: Traefik Ingress Cutover Execution

## Overview

Execute [SPEC-0121](../spec.md) through [WORK-001–004](../plan.md#work-breakdown):
Traefik side by side, live verification, the cutover and its revert evidence.

## Inputs

- The operator's 2026-10-20 instruction to write the ADR-0050 cutover Spec,
  with the Spec, Plan and Task approved in this round and the live cutover in
  later implementation pull requests.
- Start: main `8686ca24` (PR #162 merge), branch
  `docs/spec-0121-traefik-cutover` in a separate worktree.
- The 2026-10-20 observation of the first ingress-nginx v1.15.1 sync:
  - the Application Synced and Healthy at revision 4.15.1;
  - both admission hook Jobs succeeded;
  - the admission webhook carried its CA bundle;
  - `verify-ingress-tls.sh` passed.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | Traefik side by side | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-TC-002](../spec.md#success-criteria--verification-plan) | Live per-route verification | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-TC-003](../spec.md#success-criteria--verification-plan) | Cutover and ingress-nginx removal | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-TC-004](../spec.md#success-criteria--verification-plan) | Revert evidence | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Side-by-side Application status | Live Argo CD status of `platform-traefik` after WORK-001 merges | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TC-001](../spec.md#success-criteria--verification-plan) | pending | none | Side-by-side pull request remains | platform |
| [VAL-TC-002](../spec.md#success-criteria--verification-plan) | pending | none | Live route checks remain | platform |
| [VAL-TC-003](../spec.md#success-criteria--verification-plan) | pending | none | Cutover pull request remains | platform |
| [VAL-TC-004](../spec.md#success-criteria--verification-plan) | pending | none | Revert evidence remains | platform |

## Approval and Safety Boundaries

- **Allowed Paths**:
  - `docs/03.specs/0121-traefik-ingress-cutover/**`
  - `docs/03.specs/README.md`
  - `docs/01.requirements/0004-current-local-gitops-platform.md`
  - `docs/02.architecture/**`
  - `docs/05.operations/**`
  - `gitops/**`
  - `infrastructure/**`
  - `examples/**`
  - `scripts/validation/**`
  - `scripts/validate-infrastructure-contracts.sh`
  - `tests/**`
  - `README.md`
  - `.env.example`
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**:
  - The operator's 2026-10-20 instruction is recorded as approval of SPEC-0121
    and its Plan as written on that date. The operator may revoke or amend it.
  - Each implementation pull request, and each live change outside Argo CD
    sync, needs its own operator approval.
  - Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, the chart render and `qa.py staged` on
  the exact index.
- **Live Validation**: Operator-run checks for WORK-001 to WORK-004.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the pull request of the affected work unit through
  Git; Argo CD restores the previous controller state.
- **Evidence Location**: This Task.

## Verification Summary

Pending.
