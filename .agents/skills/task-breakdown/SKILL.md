---
name: "task-breakdown"
description: "Use when decomposing an approved implementation Plan into bounded executable Task records."
metadata:
  title: "Task Breakdown"
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

# task-breakdown

## Trigger

### When to Use

Use this skill as its frontmatter description states.

#### Inputs

This skill takes no input beyond the user's request and the files its Steps name; if a step comes to need another input, list it here.

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
   owner in that Task. Progress follows [context and memory](../../governance/context-and-memory.md#objective).

### Failure Handling

This skill has no failure branch of its own; a failing step is reported and the work lifecycle's bounded-attempt stop rule applies. If a step needs its own recovery, add it here.

## Outputs

### Artifacts

Ordered, profile-conformant Task records with complete acceptance and evidence
requirements, ready for authorized execution.

### Handoff

This skill completes and hands off through the work lifecycle's Completion steps and adds no field beyond what its Steps state; if it needs one, list it here.

## Verification

### Checks

This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here.

### Limits

The Task records created are ready for authorized execution but do not themselves authorize it, since delegation still requires authorization. A role without write permission returns the draft and routes the write to `doc-writer`.
