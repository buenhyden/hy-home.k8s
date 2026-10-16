---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: ["{{PARENT_ID}}"]
---

# [Feature Name] Implementation Plan

## Global Constraints

<!-- Author prompt: Link the approved Spec constraints and state only additional execution constraints here. -->
<!-- Author prompt: Every work package inherits the approved Spec constraints. -->

## Overview

<!-- Author prompt: identify the specification being executed and the intended completion state. -->

## Context

<!-- Author prompt: summarize current evidence, constraints, and prerequisite decisions. -->

## Goals & In-Scope

<!-- Author prompt: list bounded outcomes this plan is authorized to deliver. -->

## Non-Goals & Out-of-Scope

<!-- Author prompt: state excluded work, protected surfaces, and deferred decisions. -->

## Work Breakdown

<!-- Author prompt: order work packages by dependency and make each entry and exit gate observable. -->

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#success-criteria--verification-plan) | One bounded implementation outcome | None | [Task]({{TASK_RELATIVE_PATH}}) | Named deterministic check and expected evidence |

## Verification Plan

<!-- Author prompt: map every work package to deterministic checks and evidence lanes. -->

## Risks & Mitigations

<!-- Author prompt: record delivery, compatibility, and rollback risks with owners. -->

## Completion Criteria

<!-- Author prompt: define the conditions that close work without claiming live evidence. -->

## Promotion

<!-- Author prompt: Use this section as the sole durable-contract promotion receipt for this Plan. -->
<!-- Author prompt: Name each lasting contract and one current Stage 00, 01, 02, or 05 authority. -->
<!-- Author prompt: Link that authority with one relative Markdown link and give its concrete section or member. -->
<!-- Author prompt: For a Registry-realized contract, link the current rule that delegates mechanics to Stage 99. -->
<!-- Author prompt: If nothing durable is promoted, use only the row `none | none | No durable contract was introduced`. -->
<!-- Author prompt: Record actual receiving owner updates before claiming promotion. -->

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| {{DURABLE_CONTRACT}} | [{{CURRENT_AUTHORITY_TITLE}}]({{CURRENT_AUTHORITY_PATH}}) | {{LOCATION_IN_OWNER}} |
