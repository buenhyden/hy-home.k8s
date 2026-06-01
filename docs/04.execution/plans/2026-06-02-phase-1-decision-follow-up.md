---
title: 'Phase 1 Decision Follow-up Implementation Plan'
type: plan
status: done
owner: platform
updated: 2026-06-02
---

# Phase 1 Decision Follow-up Implementation Plan

---

## Overview (KR)

이 문서는 2026-06-02 Phase 1 조사 결과에서 확정한 결정 항목을 Phase 2 planning artifact로 고정한다.
작업의 목적은 Stage 00 canonical adapter 모델을 다시 재설계하지 않고, 이미 확인된 결정과 남은 작은 gap을
후속 실행 단위로 분리하는 것이다.

## Context

2026-06-01 Stage 00 canonical adapter workstream은 공통 governance, provider adapter, template contract,
hook/QA contract, model policy, skill/workflow routing, local runtime evidence를 이미 정합화했다.
2026-06-02 Phase 1 continuation audit는 이 완료 상태를 다시 확인했고, 새 구조 재설계보다 현재 결정 항목을
얇은 후속 계획으로 기록하는 것이 적절하다고 판단했다.

### Coverage Reconciliation Note (2026-06-02)

This completed follow-up plan intentionally kept a narrow decision-recording
scope. A later comparison with the original attachment identified broader
Stage 00/Codex harness topics that were not expanded in this plan itself. Those
items are now reconciled in
[Stage 00 Codex Harness Coverage Reconciliation Plan](./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)
and its paired
[Task record](../tasks/2026-06-02-stage-00-codex-harness-coverage-reconciliation.md).
This note does not reopen or change this plan's `status: done`.

### Protected Surface Follow-up Note (2026-06-02)

After the completed reconciliation, the human operator approved
protected-surface edits for items that still needed approval. A targeted
follow-up confirmed `/home/hy/.codex/skills/ouroboros-qa/SKILL.md` now exists
locally and updated the canonical `harness-catalog.md` QA routing row. This
closes DEC-004 for the Codex-local path without installing a new skill or
changing model policy, Codex TOML, CI workflow, Kubernetes manifests, secrets,
or live infrastructure.

## Goals & In-Scope

- **Goals**:
  - Phase 1 decision outcomes를 실행 가능한 Phase 2 plan으로 기록한다.
  - Stage 00 canonical adapter 모델과 `harness-catalog.md` Task-to-Skill Routing을 현행 정본으로 유지한다.
  - HADS, QA skill gap, and local PATH/RTK limitation을 후속 boundary로 명확히 남긴다.
- **In Scope**:
  - Plan document creation under `docs/04.execution/plans/`.
  - Plan README index update.
  - Progress ledger entry for this repo-changing documentation work.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Reopen the completed Stage 00 canonical adapter implementation.
  - Replace `docs/99.templates` with HADS or another documentation standard.
  - Install new skills, mutate model policy, or change provider agent configuration.
- **Out of Scope**:
  - Governance rule edits under `docs/00.agent-governance/**`.
  - Codex TOML, CI workflow, GitHub Actions, Kubernetes manifest, ArgoCD, Vault, or live cluster changes.
  - Direct inspection of private RTK databases, credentials, tokens, or shell history.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Preserve Stage 00 canonical adapter as the current architecture | `docs/02.architecture/decisions/0013-stage-00-canonical-adapter-model.md`, `docs/04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md` | DEC-001 | No new redesign work is introduced; this plan links to the accepted ADR and completed task evidence. |
| PLN-002 | Treat Task-to-Skill Routing as the active skill strategy map | `docs/00.agent-governance/harness-catalog.md` | DEC-002 | Future work updates the catalog only when concrete skill availability or routing changes. |
| PLN-003 | Keep HADS as an optional documentation lens | `docs/99.templates/README.md`, `docs/00.agent-governance/harness-catalog.md` | DEC-003 | No HADS migration is planned; canonical template routing remains under `docs/99.templates`. |
| PLN-004 | Leave `qa(ouroboros-qa)` as an unresolved local roster gap | `docs/00.agent-governance/harness-catalog.md` | DEC-004 | If an exact `ouroboros-qa` skill is installed later, update only the QA routing row and related evidence. |
| PLN-005 | Preserve local toolchain boundary for `/home/hy/.local/bin` and RTK | `.codex/CODEX.md`, `RTK.md` | DEC-005 | Use direct binary calls or an explicit PATH prefix; do not inspect private RTK DBs when `rtk gain` fails. |
| PLN-006 | Record this planning artifact and progress evidence | `docs/04.execution/plans/2026-06-02-phase-1-decision-follow-up.md`, `docs/04.execution/plans/README.md`, `docs/00.agent-governance/memory/progress.md` | DEC-006 | New plan follows `plan.template.md`, README index includes it, and progress ledger records checks and limitations. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Diff hygiene | Check for whitespace and conflict marker issues | `git diff --check` | Exit 0. |
| VAL-PLN-002 | Wiki index | Confirm generated LLM Wiki index remains current | `bash scripts/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-PLN-003 | Repository quality | Run repository governance, template, hook, and static quality gates | `bash scripts/validate-repo-quality-gates.sh .` | PASS. |
| VAL-PLN-004 | Scope review | Confirm changed files match this documentation-only plan | `git status --short --branch` | Only the new plan, plans README, and progress ledger are changed. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| This follow-up accidentally reopens completed Stage 00 redesign work | Medium | Keep the plan documentation-only and link to completed ADR/task evidence instead of changing governance rules. |
| HADS is misread as replacing the repository template contract | Medium | State that HADS is optional and that `docs/99.templates` remains canonical. |
| Missing `ouroboros-qa` triggers speculative skill installation or routing edits | Medium | Leave it as a roster gap until the exact skill exists locally or a human approves installation. |
| RTK troubleshooting touches private runtime state | High | Record only command availability and error class; never read private DBs, credentials, tokens, or shell history. |
| Live infrastructure checks are run for a docs-only follow-up | High | Keep live k3d, ArgoCD, Vault, Kubernetes mutation, and external service action out of scope. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Run `git diff --check`, `bash scripts/generate-llm-wiki-index.sh --check`, and `bash scripts/validate-repo-quality-gates.sh .`.
- **Sandbox / Canary Rollout**: Not applicable. This is documentation-only planning work.
- **Human Approval Gate**: Required before installing missing skills, changing model policy, editing CI, or touching live infrastructure.
- **Rollback Trigger**: If validation fails because this plan conflicts with template routing or README indexing, revert only this plan/README/progress change set and keep the Phase 1 decisions in the completed task evidence.
- **Prompt / Model Promotion Criteria**: Not applicable. No model policy or provider agent configuration changes are planned.

## Completion Criteria

- [x] `docs/04.execution/plans/2026-06-02-phase-1-decision-follow-up.md` exists and follows `plan.template.md`.
- [x] `docs/04.execution/plans/README.md` indexes the new plan.
- [x] `docs/00.agent-governance/memory/progress.md` records this documentation work, evidence, and limitations.
- [x] Static verification commands pass or limitations are documented.
- [x] No live cluster, secret, deployment, CI topology, or provider configuration change is performed.

## Related Documents

- **ADR**: [../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Prior Plan**: [./2026-06-01-stage-00-canonical-adapter-redesign.md](./2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Prior Task**: [../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
- **RTK Runtime Notes**: [../../../RTK.md](../../../RTK.md)
- **Codex Runtime Baseline**: [../../../.codex/CODEX.md](../../../.codex/CODEX.md)
- **Coverage Reconciliation Plan**: [./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md](./2026-06-02-stage-00-codex-harness-coverage-reconciliation.md)
