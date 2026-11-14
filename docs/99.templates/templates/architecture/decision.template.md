---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
artifact_id: "{{ARTIFACT_ID}}"
---

# {{ARTIFACT_ID}}: [Short Title]

## Context

### Problem and Drivers

<!-- Author prompt: state the forces, constraints, and evidence that require one decision. -->

### Decision Scope

<!-- Author prompt: name concerns deliberately excluded from this decision. -->
<!-- Author prompt: state the scope of the decision and the consumers it affects. -->

## Decision

### Chosen Option

<!-- Author prompt: summarize the decision, decision state, and affected boundary. -->
<!-- Author prompt: record one decision precisely enough for downstream implementation. -->

### Authority and Effect

<!-- Author prompt: name the decision makers and the decision date when they differ from the owner and the updated date, and state how compliance will be confirmed. -->

## Alternatives

### Considered Options

<!-- Author prompt: list the alternatives actually considered, each named as the option it is. -->

### Trade-offs

<!-- Author prompt: compare credible alternatives and why they were not selected. -->

| Alternative | Trade-off |
| --- | --- |
| <!-- Author prompt: Name one considered alternative. --> | <!-- Author prompt: State its gains, risks, cost and why it was not selected. --> |

## Consequences

### Impacts

<!-- Author prompt: record positive, negative, and operational consequences. -->

### Follow-up

<!-- Author prompt: state the follow-up work, who owns it, how the decision is recovered if it fails, and how it is verified. -->

## Traceability

### Sources

<!-- Author prompt: name the requirement IDs and architecture views this decision serves or constrains. -->

### Supersession

<!-- Author prompt: when a predecessor or successor decision exists, name it and its current or historical reference; remove this section when none exists. -->

### Lifecycle Traceability

<!-- Author prompt: map decision lineage, replacement state, and affected specifications. -->

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| Architecture owner | Supersedes {{PREDECESSOR_ADR_ID}} or N/A — first decision | {{AFFECTED_SPEC_LINK}} or N/A — SPEC-xxxx left the tree; Git history recovers it |
