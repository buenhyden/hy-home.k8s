---
name: "execution-plan"
description: "Use when turning an approved Spec and architecture constraints into ordered, testable implementation work."
metadata:
  title: "Execution Plan"
  version: "1.1.0"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-17"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation grants no authority
([EXEC-R005](../../governance/agent-execution.md#requirements)).

# execution-plan

## Trigger

### When to Use

Use this skill as its frontmatter description states.

#### Inputs

This skill takes no input beyond the user's request and the files its Steps name; if a step comes to need another input, list it here.

### When Not to Use

- Decomposing an approved Plan into Task records; use `task-breakdown`.
- Tracing a Requirement to the designs that constrain it; use `requirements-to-design`.
- Scoring and recording the risks the plan carries; use `risk-report`.

#### Boundaries

Do not restate the template's heading inventory here or create standalone
design/test authority. The Spec owns behavior; the Plan owns implementation
order, verification, risk, and rollback. Use `task-breakdown` for executable units.

## Procedure

### Steps

1. Read the approved Spec, related requirements and decisions, current task
   state, and repository evidence.
2. Group deliverables into logical work units with dependencies and exact
   ownership. Preserve existing approved work-package IDs.
3. For each unit identify acceptance, focused checks, risk, rollback,
   approvals, and external limitations. Do not hide unresolved work as done.
4. Resolve profile `sdlc/plan` and its current template through the Stage 99
   registry, then author the package's plan.md beside its Spec. A role without write permission returns the draft and routes the write to `doc-writer`.
5. Link the ordered work to Task records and the package Spec/Plan. Execution
   state and evidence belong to those Tasks ([context and memory](../../governance/context-and-memory.md#objective)).
6. Review the direction and ownership boundary with the user when the request
   requires design approval; then follow the authorized execution workflow.

### Failure Handling

This skill has no failure branch of its own; a failing step is reported and the work lifecycle's bounded-attempt stop rule applies. If a step needs its own recovery, add it here.

## Outputs

### Artifacts

A profile-conformant Plan with explicit dependencies, verification, rollback,
and links to the current Spec and Tasks.

### Handoff

This skill completes and hands off through the work lifecycle's Completion steps and adds no field beyond what its Steps state; if it needs one, list it here.

## Verification

### Checks

This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here.

### Limits

The resulting Plan does not create standalone design or test authority, because the Spec owns behavior and the Plan owns order, verification, risk and rollback. Unresolved work is not recorded as done, and execution state and evidence belong to the Tasks rather than the Plan.
