---
title: 'Task: Workspace Skill Expansion (P0-16)'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-13
---

# Task: Workspace Skill Expansion (P0-16)

## Overview

This document records implementation and verification for creating five
workspace-specific AI Agent skills for P0-16. It tracks tasks derived from
`docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`.

## Inputs

- **Parent Plan**: `../plans/2026-05-28-workspace-skill-expansion.md`
- **Parent Spec**: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`

## Task Table

| Task ID | Description                                                 | Type | Parent Plan / Phase | Validation / Evidence                                                          | Owner    | Status |
| ------- | ----------------------------------------------------------- | ---- | ------------------- | ------------------------------------------------------------------------------ | -------- | ------ |
| T-001   | Create `.claude/skills/requirements-to-design/skill.md`     | doc  | Phase 1             | `ls .claude/skills/requirements-to-design/skill.md`                            | platform | Done   |
| T-002   | Create `.claude/skills/execution-plan/skill.md`             | doc  | Phase 1             | `ls .claude/skills/execution-plan/skill.md`                                    | platform | Done   |
| T-003   | Create `.claude/skills/task-breakdown/skill.md`             | doc  | Phase 1             | `ls .claude/skills/task-breakdown/skill.md`                                    | platform | Done   |
| T-004   | Create `.claude/skills/ops-runbook/skill.md`                | doc  | Phase 1             | `ls .claude/skills/ops-runbook/skill.md`                                       | platform | Done   |
| T-005   | Create `.claude/skills/knowledge-map/skill.md`              | doc  | Phase 1             | `ls .claude/skills/knowledge-map/skill.md`                                     | platform | Done   |
| T-006   | Update harness-catalog.md Skills table (5 entries)          | doc  | Phase 2             | `grep -c 'requirements-to-design' docs/00.agent-governance/harness-catalog.md` | platform | Done   |
| T-007   | Update harness-catalog.md Task-to-Skill Routing (3 rows)    | doc  | Phase 2             | `grep 'SDD lifecycle' docs/00.agent-governance/harness-catalog.md`             | platform | Done   |
| T-008   | Fix validate-repo-quality-gates.sh pipe-table normalization | impl | Phase 2             | `bash scripts/validate-repo-quality-gates.sh .` exit 0                         | platform | Done   |
| T-009   | Create plan artifact                                        | doc  | Phase 2             | `ls docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`           | platform | Done   |
| T-010   | Create this task artifact                                   | doc  | Phase 2             | `ls docs/04.execution/tasks/2026-05-28-workspace-skill-expansion.md`           | platform | Done   |
| T-011   | Update progress.md                                          | doc  | Phase 2             | Entry exists in progress.md                                                    | platform | Done   |

## Approval and Safety Boundaries

- **Allowed Paths**: `T-001 through T-011` is limited to these Workspace Skill Expansion (P0-16) owners and Task-Table surfaces:
  - `docs/04.execution/tasks/2026-05-28-workspace-skill-expansion.md`
  - `docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `.claude/skills/requirements-to-design/skill.md`
  - `.claude/skills/execution-plan/skill.md`
  - `.claude/skills/task-breakdown/skill.md`
  - `.claude/skills/ops-runbook/skill.md`
- **Forbidden Paths**: runtime manifests, provider or CI settings, secret values, generated/local state, and paths outside the Workspace Skill Expansion (P0-16) work items and linked evidence owners.
- **Approval Required**: Human approval is required before Workspace Skill Expansion (P0-16) protected-file expansion, deletion/relocation, runtime/CI/provider mutation, credential access, publication, push, or merge beyond the parent Plan.
- **Static Validation**: Preserve the Workspace Skill Expansion (P0-16) outcomes and limitations recorded in Verification Summary; use these recorded checks:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `ls .claude/skills/requirements-to-design/skill.md`
  - `ls .claude/skills/execution-plan/skill.md`
  - `ls .claude/skills/task-breakdown/skill.md`
- **Live Validation**: DEFER — Workspace Skill Expansion (P0-16) is closed by repository-static/documentation evidence; historical live commands, if any, are not authority for a new cluster, provider, external-service, or deployment claim.
- **Secret / Vault Handling**: No secret value is required for Workspace Skill Expansion (P0-16); do not read or print tokens, credentials, Vault/Kubernetes Secret data, kubeconfigs, auth files, private logs, or shell history.
- **Rollback Plan**: Revert the logical Workspace Skill Expansion (P0-16) change set for `T-001 through T-011` and restore its allowed implementation/evidence paths with this Task and parent Plan; documentation rollback does not authorize live mutation.
- **Evidence Location**: Durable Workspace Skill Expansion (P0-16) evidence remains in:
  - `docs/04.execution/tasks/2026-05-28-workspace-skill-expansion.md`
  - `docs/04.execution/plans/2026-05-28-workspace-skill-expansion.md`
  - `docs/03.specs/006-workspace-harness-gap-analysis/spec.md`
  - `docs/00.agent-governance/memory/progress.md`

## Verification Summary

- **Test Commands**:

  ```bash
  bash scripts/validate-repo-quality-gates.sh .
  ls .claude/skills/requirements-to-design/skill.md
  ls .claude/skills/execution-plan/skill.md
  ls .claude/skills/task-breakdown/skill.md
  ls .claude/skills/ops-runbook/skill.md
  ls .claude/skills/knowledge-map/skill.md
  ```

- **Logs / Evidence Location**: `docs/00.agent-governance/memory/progress.md`

## Traceability

- **Plan**: `../plans/2026-05-28-workspace-skill-expansion.md`
- **Spec**: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`
- **Harness Catalog**: `../../00.agent-governance/harness-catalog.md`
