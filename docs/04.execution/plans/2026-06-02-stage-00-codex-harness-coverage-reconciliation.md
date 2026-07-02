---
title: 'Stage 00 Codex Harness Coverage Reconciliation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-06-02
---

# Stage 00 Codex Harness Coverage Reconciliation Plan

---

## Overview

This document is the implementation plan for reconciling Stage 00/Codex
harness requirements that were narrowed in the 2026-06-02 Phase 1 decision
follow-up plan. The purpose is to complete document traceability by linking
omitted items to existing completion evidence without rewriting the completed
follow-up plan.

## Context

[Phase 1 Decision Follow-up Plan](./2026-06-02-phase-1-decision-follow-up.md)
was a narrow follow-up plan that preserved the Stage 00 canonical adapter model
and separated the remaining QA skill/PATH/RTK gap. Later comparison with the
attached source text confirmed that items such as full Stage 00 investigation,
Codex harness alignment, Model Policy, QA/CI/CD, Template Contract, skill
routing, and branch completion were not decomposed as detailed work items in
that plan itself.

This remediation does not reimplement those items. It links evidence from the
already-completed
[Codex Governance Harness Alignment Plan](./2026-05-31-codex-governance-harness-alignment.md)
and [Stage 00 Canonical Adapter Redesign Plan](./2026-06-01-stage-00-canonical-adapter-redesign.md),
and limits the actual remaining scope to document traceability remediation.

### Approved Protected Surface Follow-up (2026-06-02)

The human operator later approved protected-surface edits for unimplemented
items that still needed approval. The approved implementation is limited to
repo-tracked governance evidence: the now-present Codex-local
`/home/hy/.codex/skills/ouroboros-qa/SKILL.md` path is recorded in
`docs/00.agent-governance/harness-catalog.md`, and progress evidence is recorded
without changing model policy, Codex TOML, CI topology, Kubernetes manifests, or
live infrastructure.

## Goals & In-Scope

- **Goals**:
  - Clearly record the narrowed scope of the Phase 1 follow-up plan and the items that could appear omitted.
  - Track existing completion evidence and remaining action status for each omitted item in the Task record.
  - Update the Plan/Task READMEs and progress ledger so later workers do not re-investigate the same gap.
- **In Scope**:
  - New Plan and Task records under `docs/04.execution/`.
  - A short current-state note in the completed Phase 1 follow-up plan.
  - Plans/Tasks README index updates.
  - Progress ledger evidence and validation commands.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reopen or rewrite the completed Phase 1 follow-up plan status.
  - Re-implement the completed Stage 00 canonical adapter or Codex harness work.
  - Promote HADS into the canonical template contract.
- **Out of Scope**:
  - Stage 00 policy edits, Codex TOML edits, CI workflow edits, or Kubernetes manifest changes unless a new concrete drift is found.
  - Live k3d, ArgoCD, Vault, Kubernetes mutation, secret inspection, or external service actions.
  - Destructive git operations or history rewriting.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| REC-001 | Create the corrective Plan artifact | `docs/04.execution/plans/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md` | TRACE-001 | Plan follows `plan.template.md` and links the prior evidence chain. |
| REC-002 | Create the corrective Task artifact with coverage matrix | `docs/04.execution/tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md` | TRACE-002 | Task follows `task.template.md` and maps omitted items to evidence or no-op boundaries. |
| REC-003 | Add a current-state scope note to the completed follow-up plan | `docs/04.execution/plans/2026-06-02-phase-1-decision-follow-up.md` | TRACE-003 | The note preserves `status: done` and points to this corrective plan. |
| REC-004 | Update execution stage indexes | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md` | TRACE-004 | Both README tables and structures include the new artifacts. |
| REC-005 | Record progress and verification evidence | `docs/00.agent-governance/memory/progress.md` | TRACE-005 | Progress entry records checks, limitations, and no-live-infra boundary. |
| REC-006 | Record approved protected-surface follow-up for the QA routing gap | `docs/00.agent-governance/harness-catalog.md`, this plan, paired task, progress ledger | TRACE-006 | The exact Codex-local `ouroboros-qa` path is recorded without model, CI, Kubernetes, secret, or live infrastructure mutation. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-REC-001 | Structural | New Plan keeps required template metadata and headings | Targeted heading/frontmatter scan | PASS |
| VAL-REC-002 | Structural | New Task keeps required template metadata and headings | Targeted heading/frontmatter scan | PASS |
| VAL-REC-003 | Index | Plans/Tasks README include the new artifacts | Targeted `rg` check | Both README files report the new path. |
| VAL-REC-004 | Diff hygiene | Check whitespace and conflict markers | `git diff --check` | Exit 0. |
| VAL-REC-005 | Wiki index | Confirm generated LLM Wiki index remains current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-REC-006 | Repository quality | Run repository governance, template, hook, and static quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-REC-007 | Scope review | Confirm changed files match the documentation-only reconciliation | `git status --short --branch` | Only Plan/Task docs, execution READMEs, and progress ledger are changed. |
| VAL-REC-008 | Protected surface review | Confirm the approved follow-up only updates repo-tracked governance evidence | `git diff --name-only` plus targeted QA path scan | No model policy, Codex TOML, CI workflow, Kubernetes manifest, secret, or live infrastructure file is changed. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Reconciliation is mistaken for a new Stage 00 redesign | Medium | State that prior Stage 00 and Codex harness implementation evidence remains canonical. |
| Completed plan history is rewritten | Medium | Keep the old plan `status: done` and add only a current-state note. |
| Existing evidence links become stale | Medium | Link directly to Plan/Task records that own the completed work. |
| Documentation-only work triggers live infrastructure action | High | Keep live k3d, ArgoCD, Vault, Kubernetes mutation, and secret inspection out of scope. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Run targeted template scans, `git diff --check`,
  `bash scripts/generate-llm-wiki-index.sh --check`, and
  `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable. This is documentation-only traceability work.
- **Human Approval Gate**: Satisfied on 2026-06-02 for repo-tracked
  protected-surface evidence edits. Live infrastructure, secret inspection,
  deployment mutation, CI topology changes, Kubernetes manifests, Codex TOML,
  and model policy remain unchanged unless a separate concrete drift is found.
- **Rollback Trigger**: If this reconciliation introduces broken links, template drift, or validator failure, revert only this corrective Plan/Task/README/progress change set.
- **Prompt / Model Promotion Criteria**: Not applicable. No model policy or provider agent configuration changes are planned.

## Completion Criteria

- [x] Corrective Plan artifact exists and follows `plan.template.md`.
- [x] Corrective Task artifact exists and follows `task.template.md`.
- [x] Completed Phase 1 follow-up plan links to this reconciliation without changing its done status.
- [x] Plans and Tasks README indexes include the new artifacts.
- [x] Progress ledger records this reconciliation and verification evidence.
- [x] Required static validation commands pass.
- [x] No live cluster, secret, deployment, CI topology, or provider configuration change is performed.
- [x] Approved protected-surface follow-up records the now-present Codex-local `ouroboros-qa` path without changing model, CI, Kubernetes, secret, or live infrastructure surfaces.

## Related Documents

- **Original Follow-up Plan**: [./2026-06-02-phase-1-decision-follow-up.md](./2026-06-02-phase-1-decision-follow-up.md)
- **Task**: [../tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md](../tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)
- **Codex Harness Plan**: [./2026-05-31-codex-governance-harness-alignment.md](./2026-05-31-codex-governance-harness-alignment.md)
- **Codex Harness Task**: [../tasks/2026-05-31-codex-governance-harness-alignment.md](../tasks/2026-05-31-codex-governance-harness-alignment.md)
- **Stage 00 Canonical Adapter Plan**: [./2026-06-01-stage-00-canonical-adapter-redesign.md](./2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Stage 00 Canonical Adapter Task**: [../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
