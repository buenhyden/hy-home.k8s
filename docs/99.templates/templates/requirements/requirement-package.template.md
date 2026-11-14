---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/requirement"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Feature or System Name] Requirement Package

## Overview

### Problem and Outcome

<!-- Author prompt: state the problem with evidence, the cost of leaving it unresolved and the measurable outcome this work enables, separating fact from assumption and linking real references. -->

### Stakeholders

<!-- Author prompt: identify the affected roles, their goals and constraints, and who writes, reviews and accepts the requirement. -->

## Scope

### In Scope

<!-- Author prompt: describe observable user journeys and the authorized scope without prescribing architecture. -->

### Constraints and Exclusions

<!-- Author prompt: separate explicit non-goals and future options from constraints, and record product risks, dependencies, assumptions and validation owners. -->

## Requirements

### Functional Requirements

<!-- Author prompt: assign package-dependent stable IDs to functional and implementation-independent interface requirements; give each a statement, a one-sentence rationale that names its source (or explains why none is recorded), its acceptance evidence and an optional priority. -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0001-FR-0001 | State one testable functional requirement. | State the reason and name its source, or explain why none is recorded. | Name the observable acceptance evidence. | Must |
| REQ-0001-IF-0001 | State one implementation-independent external interface requirement. | State the reason and name its source, or explain why none is recorded. | Name the observable contract evidence. | Must |

### Quality Requirements

<!-- Author prompt: keep this section only when a quality requirement applies; assign stable IDs and state each quality characteristic, its measurement environment and its target or decision-needed value. -->

| Requirement ID | Statement | Rationale | Acceptance | Priority |
| --- | --- | --- | --- | --- |
| REQ-0001-NFR-0001 | State one measurable non-functional constraint. | State the reason and name its source, or explain why none is recorded. | Name the observable quality evidence. | Must |

## Acceptance Criteria

### Acceptance Conditions

<!-- Author prompt: define measurable conditions that establish product success. -->

### Verification Method

<!-- Author prompt: state how each acceptance condition is verified, or point to the Acceptance column and the acceptance-criterion column of Lifecycle Traceability when they state it. -->

## Traceability

### Source and Constraints

<!-- Author prompt: name the upstream requirements, decisions and constraints this requirement derives from or depends on. -->

### Downstream Links

<!-- Author prompt: link the architecture descriptions, decisions and Specs that own the downstream contracts. -->

### Lifecycle Traceability

<!-- Author prompt: map each requirement to its acceptance criterion; the architecture description or Spec that owns it cites it in its own requirement column. -->

| Requirement ID | Acceptance criterion |
| --- | --- |
| REQ-0001-FR-0001 | State one measurable functional acceptance condition. |
| REQ-0001-NFR-0001 | State one measurable quality acceptance condition. |
| REQ-0001-IF-0001 | State one measurable interface acceptance condition. |
