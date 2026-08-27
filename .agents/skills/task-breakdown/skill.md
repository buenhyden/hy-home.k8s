---
name: task-breakdown
description: Use when decomposing an execution plan into agent-executable task units with acceptance criteria and evidence requirements in hy-home.k8s.
---

# task-breakdown

## Purpose

Decompose a feature-local execution plan (`docs/03.specs/<id>-<slug>/plan.md`) into
individual sibling `tasks/tsk-####-<slug>.md` records that can be executed and verified by an agent or operator,
following the SDD lifecycle contract in this repository.

## Trigger Phrases

- "break this plan into tasks"
- "create task files for this plan"
- "decompose the plan"
- "generate task units"
- "what tasks does this plan produce"
- "write tasks for this milestone"

## When to Use

- A feature-local `plan.md` has been approved and needs task-level tracking.
- Translating a phase or work item into a single, agent-executable unit of work.
- Each task needs acceptance criteria, evidence requirements, and a rollback note.
- Producing `task.template.md`-compliant feature-local Task records.

## When NOT to Use

- Authoring the execution plan itself; use `execution-plan`.
- Authoring or reviewing the spec/architecture; use `docs-stage-routing` or
  `requirements-to-design`.
- Authoring runbooks for operations; use `ops-runbook`.

## Workflow Steps

1. Read `docs/03.specs/<id>-<slug>/plan.md` and extract each
   work item from the Work Breakdown table.
2. For each work item, determine if it is independently executable (single file owner,
   single verification check). If not, split further.
3. Assign a package-qualified stable Task ID and map it to the plan's requirement ID.
4. Write or update one `docs/03.specs/<id>-<slug>/tasks/tsk-####-<slug>.md`
   record using profile `sdlc/task` and
   `docs/99.templates/templates/specs/task.template.md` as the base.
5. Each Task record must include: goal, acceptance criteria (binary), evidence (command or
   artifact path), rollback, and a `## Related Documents` link to the parent plan.
6. Update the parent plan's `## Work Breakdown` table and package README to reference the Task IDs and paths.
7. Update `docs/00.agent-governance/memory/progress.md` with the feature-local evidence paths.

## Output Format

Required headings (from `task.template.md`):

- `## Goal`
- `## Acceptance Criteria`
- `## Evidence`
- `## Rollback`
- `## Related Documents`
