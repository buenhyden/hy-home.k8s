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

## Overview

### Purpose and Readers

<!-- Author prompt: identify the architecture subject, its stakeholders and the readers this description serves, and state who owns the structure description. -->

### System Boundary

<!-- Author prompt: define system boundaries, what the system owns and does not own, and explicit non-goals. -->

## Context and Constraints

### Context

<!-- Author prompt: name the external dependencies, actors and trust boundaries the system consumes or serves. -->

### Constraints

<!-- Author prompt: state the constraints that limit the architecture; a description without a constraints table explains where its constraints are recorded. -->

| Architecture ID | Constraint | Affected Components |
| --- | --- | --- |
| <!-- Author prompt: Name a free-text constraint identifier. --> | <!-- Author prompt: State the constraint as a checkable fact. --> | <!-- Author prompt: Name the components or views it limits. --> |

## Current Structure

### Building Blocks

<!-- Author prompt: Describe components, actors, trust boundaries, and major interactions. -->
<!-- Author prompt: Use proportionate context and container views to show responsibilities, labels, and relationships, or explain an omitted view. -->
<!-- Author prompt: Give every diagram a title, scope, intended reader, legend, and editable source. Label each element with its name, type and responsibility, and give each relationship a direction and a label that states its purpose and protocol. -->

### Runtime and Deployment

<!-- Author prompt: define deployment topology, configuration owners, runtime platform and operational evidence. -->

## Interfaces

### Contracts

<!-- Author prompt: state data ownership, flow, retention, integrity constraints and the contracts between components. -->

### Failure Boundaries

<!-- Author prompt: define failure boundaries and what each failure leaves intact. -->

## Decisions

### Decision Links

<!-- Author prompt: State core structural choices and link each significant decision to its owning ADR. -->

### Quality and Risks

<!-- Author prompt: make quality attributes measurable and link each to a requirement. -->

<!-- Author prompt: For each material quality concern, state a requirement-linked scenario. -->
<!-- Author prompt: Name the stimulus, operating environment, expected response, and measurable threshold; an adjective alone is not a scenario. -->

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| <!-- Author prompt: Name the requirement-backed attribute. --> | <!-- Author prompt: State the triggering event. --> | <!-- Author prompt: State the operating condition. --> | <!-- Author prompt: State the system response. --> | <!-- Author prompt: State a measurable threshold. --> |

## Traceability

### Requirement Mapping

<!-- Author prompt: name the requirement this description serves and cite each of its members in the Lifecycle Traceability table. -->

### Currentness and Lineage

<!-- Author prompt: state what is current, which Specs or evidence left the tree, and optionally map the twelve arc42 sections to where this description, an ADR or a requirement covers them, with a reason for each omitted section; link instead of copying. -->

### Lifecycle Traceability

<!-- Author prompt: map requirements and boundaries to the decisions or specifications that own them. -->

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| REQ-0001-NFR-0001 | Name one measurable attribute or architecture boundary. | ADR or Specification owner |
