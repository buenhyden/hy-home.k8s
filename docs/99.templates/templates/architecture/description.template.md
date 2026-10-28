---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-description"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "architecture"
artifact_id: "{{ARTIFACT_ID}}"
---

# [System or Domain Name] Architecture Description (AD)

## Overview

<!-- Author prompt: identify the architecture subject, stakeholders, and current boundary. -->

## Boundaries & Non-goals

<!-- Author prompt: define system boundaries, external dependencies, and explicit non-goals. -->

## Quality Attributes

<!-- Author prompt: make quality attributes measurable and link each to a requirement. -->

<!-- Author prompt: For each material quality concern, state a requirement-linked scenario. -->
<!-- Author prompt: Name the stimulus, operating environment, expected response, and measurable threshold; an adjective alone is not a scenario. -->

| Quality attribute | Stimulus | Environment | Response | Measure |
| --- | --- | --- | --- | --- |
| <!-- Author prompt: Name the requirement-backed attribute. --> | <!-- Author prompt: State the triggering event. --> | <!-- Author prompt: State the operating condition. --> | <!-- Author prompt: State the system response. --> | <!-- Author prompt: State a measurable threshold. --> |

## System Overview & Context

<!-- Author prompt: Describe components, actors, trust boundaries, and major interactions. -->
<!-- Author prompt: State core structural choices and link each significant decision to its owning ADR. -->
<!-- Author prompt: Use proportionate context and container views to show responsibilities, labels, and relationships, or explain an omitted view. -->
<!-- Author prompt: Give every diagram a title, scope, intended reader, legend, and editable source. Label each element with its name, type and responsibility, and give each relationship a direction and a label that states its purpose and protocol. -->

## Data Architecture

<!-- Author prompt: state data ownership, flow, retention, and integrity constraints. -->

## Infrastructure & Deployment

<!-- Author prompt: define deployment topology, configuration owners, and failure boundaries. -->

## Traceability

<!-- Author prompt: map requirements and boundaries to the decisions or specifications that own them. -->
<!-- Author prompt: optionally map the twelve arc42 sections to where this description, an ADR or a requirement covers them, with a reason for each omitted section; link instead of copying. -->

### Lifecycle Traceability

| Upstream requirement | Quality attribute or boundary | ADR / Spec |
| --- | --- | --- |
| REQ-0001-NFR-0001 | Name one measurable attribute or architecture boundary. | ADR or Specification owner |
