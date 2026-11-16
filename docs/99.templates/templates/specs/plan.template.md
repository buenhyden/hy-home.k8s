---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids: ["{{PARENT_ID}}"]
---

# [Feature Name] Implementation Plan

## Overview

### Outcome

<!-- Author prompt: identify the specification being executed and the intended completion state. -->
<!-- Author prompt: list bounded outcomes this plan is authorized to deliver. -->
<!-- Author prompt: state excluded work, protected surfaces, and deferred decisions. -->

### Constraints

<!-- Author prompt: summarize current evidence, constraints, and prerequisite decisions. -->
<!-- Author prompt: name the architecture views or ADRs, interfaces, migration and rollback this plan touches, or say that none apply. -->

#### Global Constraints

<!-- Author prompt: Link the approved Spec constraints and state only additional execution constraints here. -->
<!-- Author prompt: Every work package inherits the approved Spec constraints. -->

#### Risks and Mitigations

<!-- Author prompt: record delivery, compatibility, and rollback risks with owners. -->

#### Escalation

<!-- Author prompt: name the blocking conditions, the questions for the user and the condition to resume. -->

## Dependencies

### Prerequisites

<!-- Author prompt: name the existing contracts, consumers, authorities and environments this plan needs before work starts, or say that none apply. -->

### Shared Resources

<!-- Author prompt: name the files, environments, registries and locks that more than one work unit uses, and how their use is ordered, or say that none are shared. -->

## Work Breakdown

### Work Units

<!-- Author prompt: order work packages by dependency and make each entry and exit gate observable. -->

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FEATURE-001]({{SPEC_RELATIVE_PATH}}#criteria) | One bounded implementation outcome | None | [Task]({{TASK_RELATIVE_PATH}}) | Named deterministic check and expected evidence |

#### Change and Rollback

<!-- Author prompt: state what each work unit changes, how, and the order in which a change is undone. -->

### Dependency Edges

<!-- Author prompt: state the inputs, outputs and entry conditions that order one work unit after another. -->

## Verification Plan

### Selected Checks

<!-- Author prompt: map every work package to deterministic checks and evidence lanes. -->
<!-- Author prompt: include an architecture compliance check that each work package stays within the views and ADRs named in Assumptions; a departure returns the Spec to in-review. -->
<!-- Author prompt: define the conditions that close work without claiming live evidence. -->

### Evidence Plan

<!-- Author prompt: state at which commit, push, pull request or merge each check runs and how repeats are avoided. -->

## Promotion Map

### Durable Owners

<!-- Author prompt: Use this section as the sole durable-contract promotion receipt for this Plan. -->
<!-- Author prompt: Name each lasting contract and one current `.agents/` governance, or Stage 01, 02, or 05 authority. -->
<!-- Author prompt: Link that authority with one relative Markdown link and give its concrete section or member. -->
<!-- Author prompt: For a Registry-realized contract, link the current rule that delegates mechanics to Stage 99. -->
<!-- Author prompt: State in the Acceptance cell the condition under which the promotion counts as done. -->
<!-- Author prompt: If nothing durable is promoted, use only the row `none | none | none | No durable contract was introduced`. -->
<!-- Author prompt: Record actual receiving owner updates before claiming promotion. -->

| Promotion ID | Target Owner | Acceptance | Evidence |
| --- | --- | --- | --- |
| {{DURABLE_CONTRACT}} | [{{CURRENT_AUTHORITY_TITLE}}]({{CURRENT_AUTHORITY_PATH}}) | {{ACCEPTANCE_CONDITION}} | {{LOCATION_IN_OWNER}} |

### Consumer Updates

<!-- Author prompt: name the contracts and operating meaning that remain after the work is complete, or say that none remain. -->
