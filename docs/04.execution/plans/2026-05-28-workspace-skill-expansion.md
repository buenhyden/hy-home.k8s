---
title: 'Workspace Skill Expansion Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-05-28
---

# Workspace Skill Expansion Implementation Plan

## Overview

This document is the implementation plan for creating five new local skills
that harden the SDD lifecycle and operations automation in the `hy-home.k8s`
workspace. It closes the P0-16 gap identified by the 22-workstream P0 audit on
2026-05-28.

## Context

The 2026-05-28 workspace improvement mission (Coverage Ledger + Integrated Gap
Analysis) found that five of seven candidate skills were missing from
`.claude/skills/`. The existing 11 skills covered GitOps/Kubernetes,
documentation routing, and audit workflows, but did not explicitly define
local skills for SDD lifecycle links (requirements to design, design to plan,
plan to tasks), operations runbook authoring, or governance index maintenance.

## Goals & In-Scope

- **Goals**: Create five new workspace-specific skills, update the harness catalog, and record progress in `progress.md`.
- **In Scope**:
  - `.claude/skills/requirements-to-design/skill.md`
  - `.claude/skills/execution-plan/skill.md`
  - `.claude/skills/task-breakdown/skill.md`
  - `.claude/skills/ops-runbook/skill.md`
  - `.claude/skills/knowledge-map/skill.md`
  - Update the Skills table and Task-to-Skill Routing in `docs/00.agent-governance/harness-catalog.md`
  - Add a new entry to `docs/00.agent-governance/memory/progress.md`

## Non-Goals & Out-of-Scope

- Compose Stack Agent: deferred because Docker Compose scope belongs to an external service workspace
- Policy Gate Agent: deferred because OPA/Conftest P3 deferrals are incomplete
- `.codex/agents/` TOML mirrors: skill files are not agent mirror targets; only `agents/*.md` is mirrored
- Bulk file edits without structural changes

## Requirements & Acceptance Criteria

| ID     | Requirement                         | Completion Criteria          |
| ------ | ----------------------------------- | ---------------------------- |
| REQ-01 | Create five skill files             | Files exist with frontmatter |
| REQ-02 | Update harness-catalog Skills table | Five new rows added          |
| REQ-03 | Update Task-to-Skill Routing table  | SDD lifecycle routing row added |
| REQ-04 | Add progress.md entry               | Mission result recorded      |
| REQ-05 | Pass validate-repo-quality-gates.sh | Exit code 0                  |

## Work Breakdown

| Phase | Work                                | Priority |
| ---- | ----------------------------------- | -------- |
| 1    | Create five skill files             | P1       |
| 2    | Update harness-catalog.md           | P1       |
| 3    | Update progress.md                  | P1       |
| 4    | Run validate-repo-quality-gates.sh  | P1       |

## Risks & Mitigations

| Risk                                             | Mitigation                                 |
| ------------------------------------------------ | ------------------------------------------ |
| Skills are undiscoverable because harness-catalog update is missed | Update the catalog immediately after skill creation |
| Skill scope expands too far                     | Each skill includes a clear When NOT to Use section |

## Verification Plan

```bash
bash scripts/validate-repo-quality-gates.sh .
ls .claude/skills/requirements-to-design/skill.md
ls .claude/skills/execution-plan/skill.md
ls .claude/skills/task-breakdown/skill.md
ls .claude/skills/ops-runbook/skill.md
ls .claude/skills/knowledge-map/skill.md
```

## Agent Rollout & Evaluation Gates (If Applicable)

N/A — this plan covers infrastructure and documentation work and does not
deploy AI Agent models or prompts.

## Completion Criteria

- Five skill files each exist as `skill.md` under `.claude/skills/`.
- Five new rows are added to the Skills table in `docs/00.agent-governance/harness-catalog.md`.
- The Task-to-Skill Routing table includes an SDD lifecycle routing row.
- This mission is recorded in `docs/00.agent-governance/memory/progress.md`.
- `bash scripts/validate-repo-quality-gates.sh .` exits with code 0.

## Rollback

- Delete the new skill files.
- Remove the added rows from `harness-catalog.md`.
- Remove the added entry from `progress.md`.

## Related Documents

- Parent Gap Analysis: `../../00.agent-governance/memory/progress.md`
- Task record: `../tasks/2026-05-28-workspace-skill-expansion.md`
- harness-catalog: `../../00.agent-governance/harness-catalog.md`
- Spec 006: `../../03.specs/006-workspace-harness-gap-analysis/spec.md`
