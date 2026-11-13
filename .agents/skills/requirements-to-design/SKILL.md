---
name: "requirements-to-design"
description: "Use when tracing Requirement Package members to relevant Architecture Descriptions, ADRs, and Spec contracts."
metadata:
  title: "Requirements To Design"
  version: "1.0.4"
  type: "governance/skill"
  status: "active"
  owner: "platform"
  updated: "2026-11-13"
disable-model-invocation: true
---

Read `.agents/governance/approval-and-safety.md` and the selected role before
using this procedure. Skill invocation does not authorize additional actions.

# requirements-to-design

## Purpose and Trigger

### When to Use

Use this skill as its frontmatter description states.

### When Not to Use

- Turning an approved Spec into ordered implementation work; use `execution-plan`.
- Choosing where the resulting design document belongs; use `docs-stage-routing`.

#### Boundaries

Requirements remain solution-independent. Architecture owns structure and
durable choices; Spec owns change-specific implementation behavior. Use
`docs-stage-routing` for authoring and `execution-plan` for implementation order.

## Procedure

### Steps

1. Read the Requirement Package and extract complete member IDs such as
   `REQ-0001-FR-0001`, `REQ-0001-NFR-0001`, and `REQ-0001-IF-0001`.
2. Identify relevant current Architecture Descriptions and accepted ADRs.
   Requirement evidence does not require an invented architecture artifact
   when no structural decision or view is needed.
3. Trace each relevant requirement to architecture rationale and the owning
   Spec's behavior/acceptance contract. Executable OpenAPI, GraphQL, and Proto
   definitions belong to that Spec package, not Stage 01. When the Spec
   package was deleted, cite the Archived Lineage row of the current owning
   document instead.
4. Report covered, partial, missing, or not-applicable relationships with
   evidence. Do not auto-create an ADR or implementation document.
5. When authorized, update forward links to the current owners through the selected
   profiles and verify complete stable IDs and path ownership.

### Failure Handling

This skill has no failure branch of its own; a failing step is reported and the work lifecycle's bounded-attempt stop rule applies. If a step needs its own recovery, add it here.

## Inputs and Outputs

### Inputs

This skill takes no input beyond the user's request and the files its Steps name; if a step comes to need another input, list it here.

### Outputs

A bounded traceability/gap map with full requirement IDs and current owners,
plus any authorized link repair and validation evidence.

## Verification

### Checks

This skill defines no verification step separate from its Steps; the checks the invoking task selects under the quality policy apply. If it needs a separate one, list it here.

### Completion and Handoff

This skill completes and hands off through the work lifecycle's Completion steps and adds no field beyond what its Steps state; if it needs one, list it here.
