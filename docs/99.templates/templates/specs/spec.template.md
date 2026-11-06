---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
---

# [Feature Name] Technical Specification (Spec)

## Overview

<!-- Author prompt: identify the implemented capability, consumers, and verification outcome. -->

## Strategic Boundaries & Non-goals

<!-- Author prompt: define authorized scope, protected surfaces, and explicit non-goals. -->
<!-- Author prompt: list open questions and assumptions with an owner; an open question that changes a criterion keeps this Spec out of approved. -->

## Contracts

<!-- Author prompt: state externally observable behavior, invariants, and authority boundaries. -->

## Core Design

<!-- Author prompt: explain components, control flow, state transitions, and key tradeoffs. -->
<!-- Author prompt: link the Architecture Descriptions and ADRs that constrain this change and state how the design conforms, or say that none apply; a needed departure is decided in a new or amended ADR before approval. -->

## Data Modeling & Storage Strategy

<!-- Author prompt: define data shape, ownership, persistence, lifecycle, and migration. -->

## Interfaces & Data Structures

<!-- Author prompt: specify inputs, outputs, schemas, versioning, and compatibility. -->

## Edge Cases & Error Handling

<!-- Author prompt: map boundary conditions to deterministic errors and recovery behavior. -->
<!-- Author prompt: name the normal, error and boundary scenarios and the requirement each one serves. -->

## Failure Modes & Fallback / Human Escalation

<!-- Author prompt: define fail-safe behavior, rollback, degraded operation, and escalation. -->

## Verification Commands

<!-- Author prompt: list deterministic commands, expected results, and explicit evidence limits. -->

## Success Criteria & Verification Plan

<!-- Author prompt: assign stable criterion IDs and name evidence that proves each one. -->

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-FEATURE-001 | Named test, contract, integration, or review evidence |

## Traceability

<!-- Author prompt: map product requirements to specification criteria, constraining architecture and verification evidence. -->

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| REQ-0001-FR-0001 | VAL-FEATURE-001 | Constraining AD or ADR link, or why none applies | Named unit, contract, integration, or review evidence |
