---
name: "requirements-to-design"
description: "Use when tracing Requirement Package members to relevant Architecture Descriptions, ADRs, and Spec contracts."
---

# requirements-to-design

## Workflow Steps

1. Read the Requirement Package and extract complete member IDs such as
   `REQ-0001-FR-0001`, `REQ-0001-NFR-0001`, and `REQ-0001-IF-0001`.
2. Identify relevant current Architecture Descriptions and accepted ADRs.
   Requirement evidence does not require an invented architecture artifact
   when no structural decision or view is needed.
3. Trace each relevant requirement to architecture rationale and the owning
   Spec's behavior/acceptance contract. Executable OpenAPI, GraphQL, and Proto
   definitions belong to that Spec package, not Stage 01.
4. Report covered, partial, missing, or not-applicable relationships with
   evidence. Do not auto-create an ADR or implementation document.
5. When authorized, update reciprocal/current links through the selected
   profiles and verify complete stable IDs and path ownership.

## Boundaries

Requirements remain solution-independent. Architecture owns structure and
durable choices; Spec owns change-specific implementation behavior. Use
docs-stage-routing for authoring and execution-plan for implementation order.

## Outputs

A bounded traceability/gap map with full requirement IDs and current owners,
plus any authorized link repair and validation evidence.
