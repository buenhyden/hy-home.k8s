---
name: execution-plan
description: Use when transforming design or architecture artifacts into a structured execution plan with work breakdown, risks, verification plan, and completion criteria in hy-home.k8s.
---

# execution-plan

## Purpose

Transform architecture or spec artifacts (`docs/02.architecture/`, `docs/03.specs/`) into
a concrete execution plan (`docs/04.execution/plans/`) following the SDD lifecycle contract
in this repository.

## Trigger Phrases

- "create execution plan"
- "write a plan for this spec"
- "turn this design into a plan"
- "plan the implementation"
- "break this into a work breakdown"
- "what are the phases for this work"

## When to Use

- A spec or ARD/ADR has been approved and needs a delivery plan.
- Translating a design decision into ordered implementation phases.
- Defining risks, mitigations, verification steps, and completion criteria before starting work.
- Producing a `plan.template.md`-compliant document for `docs/04.execution/plans/`.

## When NOT to Use

- Authoring the spec or architecture artifact; use `docs-stage-routing` to select the template.
- Decomposing a plan into individual agent task units; use `task-breakdown`.
- Tracing requirements to architecture; use `requirements-to-design`.
- Authoring runbooks for operations; use `ops-runbook`.

## Workflow Steps

1. Read the driving spec (`docs/03.specs/`) or ARD/ADR (`docs/02.architecture/`) to extract
   the goal, scope, and constraints.
2. Identify all in-scope deliverables and group them into phases (P1 = immediate low-risk,
   P2 = bounded medium-risk, P3 = deferred high-risk/external-dependency).
3. For each phase, list the work items and their verification method.
4. Identify risks and mitigations per phase.
5. Write a Verification Plan section with concrete commands or checks.
6. Write a Completion Criteria section with measurable, binary acceptance tests.
7. Create the plan file under `docs/04.execution/plans/YYYY-MM-DD-<slug>.md` using
   `docs/99.templates/templates/sdlc/execution/plan.template.md` as the base.
8. Link the plan from `docs/00.agent-governance/memory/progress.md`.

## Output Format

Required headings (from `plan.template.md`):

- `## Overview`
- `## Goals & In-Scope`
- `## Non-Goals & Out-of-Scope`
- `## Requirements & Acceptance Criteria`
- `## Work Breakdown`
- `## Risks & Mitigations`
- `## Verification Plan`
- `## Completion Criteria`
- `## Rollback`
- `## Related Documents`
