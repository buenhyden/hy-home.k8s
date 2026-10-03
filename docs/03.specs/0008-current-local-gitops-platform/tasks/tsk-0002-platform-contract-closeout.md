---
title: "Local GitOps Platform Contract Closeout"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-10-03"
layer: "specs"
artifact_id: "SPEC-0008-TSK-0002"
---

# Task: Local GitOps Platform Contract Closeout

## Overview

Close SPEC-0008 after its implementation criteria are checked and its ongoing
authority is routed to the current architecture, executable desired state, and
validation owners. Preserve [Task 0001](tsk-0001-dedicated-k8s-router-and-host-baseline.md)
and the completed [Plan](../plan.md) as dated implementation evidence. This
closeout does not re-run their historical live observations or erase failures.

## Inputs

- [SPEC-0008](../spec.md) and its VAL-SPC-001..005 criteria.
- [REQ-0004](../../../01.requirements/0004-current-local-gitops-platform.md)
  and [AD-0007](../../../02.architecture/descriptions/0007-current-local-gitops-platform.md).
- [ADR-0037](../../../02.architecture/decisions/0037-kiali-operator-installation.md)
  accepts the Kiali Operator already declared in GitOps, while ADR-0046 owns
  its HTTPS Prometheus/Grafana and Tempo service paths.
- Current `gitops/`, `infrastructure/`, and `scripts/` source and the repository
  QA registry.
- Hosted main CI run `36978509630` on `f2b6167be1dae6a066344e9c84719980295d010a`
  (success), plus the independent static acceptance audit for VAL-SPC-002..005.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-SPC-001 | Promote ongoing architecture/execution authority and repoint current consumers | architect, doc-writer, wiki-curator | Queued | Current AD/consumer diff under review | AD-0007; REQ-0004; current policy/runbook links |
| WORK-002 | VAL-SPC-001..005 | Confirm static and hosted acceptance at exact source/review SHA | quality-engineer | Queued | Source-main static PASS; final changed SHA pending | Main CI `36978509630`; `scripts/validate-infrastructure-contracts.sh`, `scripts/validate-gitops-structure.sh`, `scripts/validate-k8s-manifests.sh .` |
| WORK-003 | VAL-SPC-001 | Close and retain the package as completed historical evidence | platform | Queued | Completion text drafted; retention awaits consumer-zero and integrated source | This Task, SPEC-0008, Stage 98 catalog |

## Approval and Safety Boundaries

- **Allowed Paths**: SPEC-0008 package, REQ-0004, AD-0007, current consumer
  citations and their navigation/retention indexes; executable validators only
  when a demonstrated defect requires a separately scoped fix.
- **Forbidden Paths**: frozen Stage 98 bodies and ledgers, secret values,
  credentials, and unrelated desired state.
- **Approval Required**: push, PR, merge, worktree removal, and Stage 98
  disposition follow the repository Git and document-lifecycle boundaries;
  live mutation and external secret work need operator authority.
- **Static Validation**: exact-index staged QA before commit, hosted
  full-equivalent CI for PR and main; direct VAL-SPC-002..005 checks.
- **Live Validation**: DEFER; this document closeout does not run or establish
  current cluster/external runtime state.
- **Secret / Vault Handling**: no secret read, print, or write.
- **Rollback Plan**: revert the closeout commit before Stage 98 retention;
  after retention, follow its separate approved disposition and immutable
  envelope rules.
- **Evidence Location**: this Task and exact hosted CI run/commit identities.

## Verification Summary

At source main `f2b6167be1dae6a066344e9c84719980295d010a`, hosted full-equivalent
CI run `36978509630` succeeded. The independent acceptance audit ran the
infrastructure contract, GitOps structure, and Kubernetes syntax validators:
all passed; the ingress-router assertions for VAL-SPC-005 are in the passing
infrastructure contract validator. These are static and hosted results, not a
new live observation. Final closeout SHA, exact-index QA, and independent
author-separated semantic review remain to be recorded before WORK-001..003
are complete.

REQ-0004-FR-0008 and REQ-0004-FR-0010 remain open for Kustomize render and
Kubernetes schema coverage, per-target depth/tool/fallback evidence, and
ingress reference/resource-kind checks. The request owner scopes those gaps
against the current validators before assigning implementation work. Task 0001
also retains its dated operator handoff and residual live risks. Neither set
of gaps becomes complete merely because this Spec closes.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-SPC-001](../spec.md#success-criteria--verification-plan) | WORK-001 and WORK-003 queued; source-main hosted PASS, final SHA pending | AD-0007 transfer; CI run `36978509630` on `f2b6167be1dae6a066344e9c84719980295d010a` |
| [VAL-SPC-002](../spec.md#success-criteria--verification-plan) | Source-main static PASS; WORK-002 queued | `validate-infrastructure-contracts.sh` |
| [VAL-SPC-003](../spec.md#success-criteria--verification-plan) | Source-main static PASS; WORK-002 queued | `validate-gitops-structure.sh` |
| [VAL-SPC-004](../spec.md#success-criteria--verification-plan) | Source-main static PASS; WORK-002 queued | `validate-k8s-manifests.sh .` |
| [VAL-SPC-005](../spec.md#success-criteria--verification-plan) | Source-main static PASS; WORK-002 queued | Ingress assertions in `validate-infrastructure-contracts.sh` |
