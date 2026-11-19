---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-description"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [System or Domain Name] Architecture Description (AD)

## Context and Boundaries

### System Boundary

<!-- Author prompt: define system boundaries, what the system owns and does not own, and explicit non-goals. -->

#### Purpose and Readers

<!-- Author prompt: identify the architecture subject, its stakeholders and the readers this description serves, and state who owns the structure description. -->

#### Context

<!-- Author prompt: name the external dependencies, actors and trust boundaries the system consumes or serves. -->

### Constraints

<!-- Author prompt: state the constraints that limit the architecture; a description without a constraints table explains where its constraints are recorded. -->

| Architecture ID | Constraint | Affected Components |
| --- | --- | --- |
| <!-- Author prompt: Name a free-text constraint identifier. --> | <!-- Author prompt: State the constraint as a checkable fact. --> | <!-- Author prompt: Name the components or views it limits. --> |

## Structure

### Building Blocks

<!-- Author prompt: Describe components, actors, trust boundaries, and major interactions declared by the current sources. Identify approved target structure that those sources do not yet declare. -->
<!-- Author prompt: Use proportionate context and container views to show responsibilities, labels, and relationships, or explain an omitted view. -->
<!-- Author prompt: Give every diagram a title, scope, intended reader, legend, and editable source. Label each element with its name, type and responsibility, and give each relationship a direction and a label that states its purpose and protocol. -->

### Interfaces

<!-- Author prompt: state data ownership, flow, retention, integrity constraints and the contracts between components. -->
<!-- Author prompt: keep the External Interfaces table below only when this description states an external interface; give each boundary one row with its producer, consumer, contract reference and failure handling as this description states them, and keep only the header while a stated fact is missing. Delete the table when the description states no external interface. -->

| Interface | Producer | Consumer | Contract | Failure |
| --- | --- | --- | --- | --- |
| <!-- Author prompt: Name one boundary. --> | <!-- Author prompt: Name the producer. --> | <!-- Author prompt: Name the consumer. --> | <!-- Author prompt: Link the contract. --> | <!-- Author prompt: State how a failure is handled. --> |

## Runtime Behavior

### Normal Flow

<!-- Author prompt: Identify the declared deployment topology and its configuration owners. Cite actual runtime observations with their input, environment, and result. Identify any unobserved scope and its verification owner. -->

### Failure and Recovery

<!-- Author prompt: define failure boundaries and what each failure leaves intact. -->

## Quality Scenarios

### Scenarios

<!-- Author prompt: make quality attributes measurable and link each to a requirement. -->

<!-- Author prompt: For each material quality concern, state a requirement-linked scenario. -->
<!-- Author prompt: Name the stimulus, operating environment, expected response, and measurable threshold; an adjective alone is not a scenario. -->

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| <!-- Author prompt: Name the requirement-backed attribute. --> | <!-- Author prompt: State the triggering event. --> | <!-- Author prompt: State the operating condition. --> | <!-- Author prompt: State the system response. --> | <!-- Author prompt: State a measurable threshold. --> |

### Trade-offs

<!-- Author prompt: state what the structure gives up for each quality it favors, using only facts from this description and its ADRs. -->

## Decisions and Adoption

### Decisions

<!-- Author prompt: State core structural choices and link each significant decision to its owning ADR. -->

#### Requirement Mapping

<!-- Author prompt: name the requirement this description serves and cite each of its members in the Lifecycle Traceability table. -->

### Adoption Boundaries

<!-- Author prompt: Explain differences between approved targets, current declarations, and observed operation. Link the evidence and responsible owners, including lineage for Specs or evidence that left the tree. Optionally map arc42 sections to their current owners and explain omissions. -->

### Lifecycle Traceability

<!-- Author prompt: map requirements and boundaries to the decisions or specifications that own them. -->

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| REQ-0001-NFR-0001 | Name one measurable attribute or architecture boundary. | ADR or Specification owner |
