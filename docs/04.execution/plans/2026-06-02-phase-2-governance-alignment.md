---
title: 'Phase 2 Governance Alignment Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-13
---

# Phase 2 Governance Alignment Plan

## Overview

This document is the implementation plan for fixing Phase 1 Governance
Alignment Audit results into a Phase 2 planning artifact. Phase 2 does not
implement a new structure; it records the already-confirmed Stage 00 canonical
adapter decisions, gap ledger, and deferred live-validation boundary as a
traceable Plan/Task contract under `docs/04.execution`.

## Context

The Phase 1 audit confirmed that ADR-0013's Stage 00 canonical adapter model
should remain in place. The actual drift found by the audit was the stale
`active` lifecycle marker on the 2026-05-30 Antigravity plan/task, which was
resolved in Phase 1 through an in-place docs correction. The remaining risk is
mistaking repo-static validation for live k3d, ArgoCD, Vault, ESO, or
deployment health readiness.

### Phase 3 Follow-up Note (2026-06-02)

The human operator later approved policy, runtime hook, CI, template, CI topology,
model policy, provider config, GitOps manifest, and live validation scope for
Phase 3. Phase 3 keeps ADR-0013 intact, hardens the concrete `.agents/**`
shared asset trigger drift, records model/provider/GitOps manifest no-op
decisions where no drift exists, and runs only approved read-only live validation.

## Goals & In-Scope

- **Goals**:
  - Fix Phase 1 audit results into executable Phase 2 Plan/Task artifacts.
  - Strengthen traceability between ADR-0013, the Phase 1 audit task, execution README indexes, and the progress ledger.
  - Split live runtime validation into a separately approved follow-up.
- **In Scope**:
  - Plan document creation under `docs/04.execution/plans/`.
  - Task document creation under `docs/04.execution/tasks/`.
  - Plans/Tasks README index updates.
  - Phase 1 audit task related-link update.
  - Progress ledger update.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reopen or redesign Stage 00 canonical adapter architecture.
  - Promote HADS into the repository template contract.
  - Change model policy, provider TOML, hook scripts, CI workflow, GitOps manifests, or Kubernetes desired state.
- **Out of Scope**:
  - live k3d, Kubernetes API, ArgoCD, Vault, ESO, deployment, external service, or secret inspection checks.
  - Private RTK database, credential, token, private key, or shell history inspection.
  - Branch merge, push, PR creation, or destructive cleanup.

### Requirements & Acceptance Criteria

| Requirement | Acceptance Criteria |
| --- | --- |
| REQ-P2-001 | Phase 2 Plan exists under `docs/04.execution/plans/`, uses `status: done`, `owner: platform`, and includes required template headings. |
| REQ-P2-002 | Phase 2 Task exists under `docs/04.execution/tasks/`, uses `status: done`, `owner: platform`, and records binary evidence requirements. |
| REQ-P2-003 | Plans and Tasks README indexes include the Phase 2 artifacts with `Done` status and 2026-06-02 date. |
| REQ-P2-004 | Phase 1 audit task links to Phase 2 Plan/Task as downstream planning evidence. |
| REQ-P2-005 | Progress ledger records Phase 2 scope, evidence, and skipped live validation boundary. |
| REQ-P2-006 | Static verification passes, or any limitation is recorded without claiming live runtime readiness. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create the Phase 2 execution plan | `docs/04.execution/plans/2026-06-02-phase-2-governance-alignment.md` | REQ-P2-001 | Plan has required headings, `status: done`, `owner: platform`, and related links. |
| PLN-002 | Create the Phase 2 task record | `docs/04.execution/tasks/2026-06-02-phase-2-governance-alignment.md` | REQ-P2-002 | Task has required headings, acceptance criteria, evidence, rollback, and related links. |
| PLN-003 | Sync execution stage indexes and upstream links | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, Phase 1 audit task | REQ-P2-003, REQ-P2-004 | README rows and Phase 1 related links point to the new Phase 2 artifacts. |
| PLN-004 | Record progress and deferred live-validation boundary | `docs/00.agent-governance/memory/progress.md` | REQ-P2-005 | Progress entry states docs-only scope and skipped live checks. |
| PLN-005 | Run static verification | repo-static validators | REQ-P2-006 | `git diff --check`, LLM Wiki check, repo quality gate, and targeted scans pass. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P2-001 | Diff hygiene | Check whitespace and conflict marker issues | `git diff --check` | Exit 0. |
| VAL-P2-002 | Wiki index | Confirm generated LLM Wiki index remains current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-P2-003 | Repository quality | Run repository governance, template, hook, and static quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-P2-004 | Index coverage | Confirm Phase 2 artifacts are indexed | `rg -n "phase-2-governance-alignment" docs/04.execution/plans/README.md docs/04.execution/tasks/README.md docs/04.execution/plans/2026-06-02-phase-2-governance-alignment.md docs/04.execution/tasks/2026-06-02-phase-2-governance-alignment.md` | All four paths report matches. |
| VAL-P2-005 | Frontmatter and related links | Confirm done lifecycle and related docs are present | `rg -n "status: done\|owner: platform\|## Related Documents" docs/04.execution/plans/2026-06-02-phase-2-governance-alignment.md docs/04.execution/tasks/2026-06-02-phase-2-governance-alignment.md` | Both documents expose done lifecycle and related-document sections. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Phase 2 is mistaken for a new governance redesign | Medium | State that ADR-0013 remains accepted and Phase 2 is docs-only planning traceability. |
| Repo-static checks are mistaken for live runtime readiness | High | Keep live k3d, ArgoCD, Vault, ESO, deployment, and external service checks explicitly deferred. |
| New docs fail template enforcement | Medium | Use `plan.template.md` and `task.template.md`, update README indexes, and run the repo quality gate. |
| Historical memory is rewritten as current truth | Medium | Add a new progress entry and links instead of rewriting older historical entries. |

### Agent Rollout & Evaluation Gates

- **Offline Eval Gate**: `git diff --check`, `bash scripts/generate-llm-wiki-index.sh --check`, `bash scripts/validate-repo-quality-gates.sh .`, and targeted index/frontmatter scans.
- **Sandbox / Canary Rollout**: Not applicable. This is documentation-only planning work.
- **Human Approval Gate**: Required before live k3d, ArgoCD, Vault, ESO, deployment, secret inspection, CI topology, model policy, provider config, or GitOps manifest changes.
- **Rollback Trigger**: If template routing or README indexing fails, revert only the Phase 2 Plan/Task, README rows, Phase 1 related-link additions, and progress ledger entry.
- **Prompt / Model Promotion Criteria**: Not applicable. No prompt, model, or provider policy is changed.

## Completion Criteria

- [x] Phase 2 Plan is created and indexed.
- [x] Phase 2 Task is created and indexed.
- [x] Phase 1 audit task links to Phase 2 downstream evidence.
- [x] Progress ledger records Phase 2 scope and deferred live-validation boundary.
- [x] Static verification commands pass or limitations are documented.
- [x] No live cluster, secret, deployment, CI workflow, provider config, hook script, model policy, or GitOps manifest change is performed.

### Rollback

- Remove `docs/04.execution/plans/2026-06-02-phase-2-governance-alignment.md`.
- Remove `docs/04.execution/tasks/2026-06-02-phase-2-governance-alignment.md`.
- Remove the Phase 2 rows from Plans/Tasks README indexes.
- Remove Phase 2 links from the Phase 1 audit task.
- Remove the Phase 2 progress ledger entry.

## Traceability

- Parent Spec: N/A — pre-Spec execution record.
- **ADR**: [../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Phase 1 Plan**: [./2026-06-02-phase-1-decision-follow-up.md](./2026-06-02-phase-1-decision-follow-up.md)
- **Phase 1 Audit Task**: [../tasks/2026-06-02-phase-1-governance-alignment-audit.md](../tasks/2026-06-02-phase-1-governance-alignment-audit.md)
- **Tasks**: [../tasks/2026-06-02-phase-2-governance-alignment.md](../tasks/2026-06-02-phase-2-governance-alignment.md)
- **Phase 3 Plan**: [./2026-06-02-phase-3-protected-surface-hardening.md](./2026-06-02-phase-3-protected-surface-hardening.md)
- **Phase 3 Task**: [../tasks/2026-06-02-phase-3-protected-surface-hardening.md](../tasks/2026-06-02-phase-3-protected-surface-hardening.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Document Stage Routing**: [../../00.agent-governance/rules/document-stage-routing.md](../../00.agent-governance/rules/document-stage-routing.md)
- **Plan Template**: [../../99.templates/templates/sdlc/execution/plan.template.md](../../99.templates/templates/sdlc/execution/plan.template.md)
