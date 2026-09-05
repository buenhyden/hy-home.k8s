---
name: "execution-plan"
description: "Use when turning an approved Spec and architecture constraints into ordered, testable implementation work."
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# execution-plan

## Workflow Steps

1. Read the approved Spec, related requirements and decisions, current task
   state, and repository evidence.
2. Group deliverables into logical work units with dependencies and exact
   ownership. Preserve existing approved work-package IDs.
3. For each unit identify acceptance, focused checks, risk, rollback,
   approvals, and external limitations. Do not hide unresolved work as done.
4. Resolve profile `sdlc/plan` and its current template through the Stage 99
   registry, then author the package's plan.md beside its Spec.
5. Link the ordered work to Task records and the package Spec/Plan. Execution
   state and evidence belong to those Tasks, not a separate progress ledger.
6. Review the direction and ownership boundary with the user when the request
   requires design approval; then follow the authorized execution workflow.

## Boundaries

Do not restate the template's heading inventory here or create standalone
design/test authority. The Spec owns behavior; the Plan owns implementation
order, verification, risk, and rollback. Use task-breakdown for executable units.

## Outputs

A profile-conformant Plan with explicit dependencies, verification, rollback,
and links to the current Spec and Tasks.
