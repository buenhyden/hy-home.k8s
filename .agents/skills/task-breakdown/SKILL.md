---
name: "task-breakdown"
description: "Use when decomposing an approved implementation Plan into bounded executable Task records."
metadata:
  title: "Task Breakdown"
  version: "1.0.2"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# task-breakdown

## Purpose and Trigger

### When to Use

Use this skill as its frontmatter description states.

### When Not to Use

- Producing the ordered Plan the Task records come from; use `execution-plan`.
- Choosing the template and owner for the Task record; use `docs-stage-routing`.

#### Boundaries

A Task may touch several related files or require several checks; do not split
it merely to satisfy an artificial one-file/one-check rule. Ownership and
reviewability determine the unit. Delegation still requires authorization.

## Procedure

### Steps

1. Read the Spec and Plan work breakdown; preserve approved work-package IDs.
2. Define each independently reviewable logical unit with exact ownership,
   dependencies, acceptance, approval boundaries, and verification.
3. Allocate an unused package-qualified Task ID using the Stage 99 registry.
   Never reuse a retired ID.
4. Read the registry-selected `sdlc/task` template and create its Task record
   under the Spec package. Use its initial status and legal lifecycle rather
   than a generic draft/completed convention. A role without write permission returns the draft and routes the write to `doc-writer`.
5. Link the Task, Plan, and Spec as required by their profiles.
6. Keep status, validation evidence, review, rollback, residual risk, and next
   owner in that Task. Do not create a parallel monolithic task/progress record.

### Failure Handling

None is stated in this document.

## Inputs and Outputs

### Inputs

None is stated in this document.

### Outputs

Ordered, profile-conformant Task records with complete acceptance and evidence
requirements, ready for authorized execution.

## Verification

### Checks

None is stated in this document.

### Completion and Handoff

None is stated in this document.
