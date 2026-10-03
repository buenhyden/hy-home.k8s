---
title: "Local GitOps Platform Contract Closeout"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
| WORK-001 | VAL-SPC-001 | Promote ongoing architecture/execution authority and repoint current consumers | architect, doc-writer, wiki-curator | Done | AD-0007, executable sources, and Stage 05 own current guidance; ADR-0037 resolves Kiali install-mode drift | `0fa90adce026c5400a086896df32e5b7cdaa437a`; independent read-only semantic review `/root/spec0008_review` found no remaining issue |
| WORK-002 | VAL-SPC-001..005 | Confirm static and hosted acceptance at the source and closeout snapshots | quality-engineer | Done | Source-main hosted QA and static criteria PASS; closeout staged QA PASS; PR hosted QA remains the delivery gate | Main CI `36978509630` at `f2b6167be1dae6a066344e9c84719980295d010a`; staged QA 13/13 at `0fa90adc` index and 6/6 at `37c57e15` index |
| WORK-003 | VAL-SPC-001 | Close the package and prepare its separately authorized completed retention | platform | Done | Spec and both Tasks completed; Plan was already completed; current consumers migrated. Retention follows after the source is integrated on main. | This Task, SPEC-0008, AD-0007; later Stage 98 Retention Catalog tree envelope |

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
infrastructure contract validator. The closeout authority transfer index passed
all 13 staged gates before commit `0fa90adce026c5400a086896df32e5b7cdaa437a`;
the Task transition index passed all 6 staged gates before commit
`37c57e15cf1ac418ffcbcfb67aabc435c84e0f76`. The final Task-only evidence
edit receives its own staged QA and the PR's immutable checkout receives hosted
full QA before integration. These are static and hosted results, not a new live
observation.

The independent read-only reviewer `/root/spec0008_review`, separate from the
authors, checked the authority transfer against current manifests and decisions.
Its ADR, index, and PostgreSQL README findings were corrected; the reviewer
reported no remaining semantic finding. The user explicitly authorized
completion and retention on 2026-10-03. Retention is a separate cutover after
this package's source tree is reachable from `origin/main`; it moves every
package member byte-for-byte and records one tree envelope in the Stage 98
Retention Catalog. This Task's completion does not claim that future move or
current live-cluster health.

REQ-0004-FR-0008 and REQ-0004-FR-0010 remain open for Kustomize render and
Kubernetes schema coverage, per-target depth/tool/fallback evidence, and
ingress reference/resource-kind checks. The request owner scopes those gaps
against the current validators before assigning implementation work. Task 0001
also retains its dated operator handoff and residual live risks. Neither set
of gaps becomes complete merely because this Spec closes.

The handoff snapshot is branch `codex/spec0008-closeout` after
`37c57e15cf1ac418ffcbcfb67aabc435c84e0f76`, based on source main
`f2b6167be1dae6a066344e9c84719980295d010a`. The scope is current-authority
documents, operational readers, and GitOps README facts; no desired-state or
secret value changed. The platform owner retains the REQ-0004 validation gaps;
the operator retains Task 0001's dated live-runtime follow-ups. Roll back the
unarchived closeout through ordinary forward `git revert` commits, subject to
the same checks; the later retention has its own immutable envelope and
separate reversal review.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [VAL-SPC-001](../spec.md#success-criteria--verification-plan) | Closeout staged PASS; source-main hosted PASS; PR hosted delivery pending | AD-0007 promotion and current consumers; CI run `36978509630`; independent read-only review |
| [VAL-SPC-002](../spec.md#success-criteria--verification-plan) | Static PASS | `validate-infrastructure-contracts.sh` on source main and staged closeout index |
| [VAL-SPC-003](../spec.md#success-criteria--verification-plan) | Static PASS | `validate-gitops-structure.sh` on source main and staged closeout index |
| [VAL-SPC-004](../spec.md#success-criteria--verification-plan) | Static PASS | `validate-k8s-manifests.sh .` on source main and staged closeout index |
| [VAL-SPC-005](../spec.md#success-criteria--verification-plan) | Static PASS | Ingress assertions in `validate-infrastructure-contracts.sh` |
