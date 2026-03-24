---
title: 'ADR 0004: Documentation Refactor and Lazy Loading'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'documentation']
layer: "meta"
---

## 1. Metadata

- **ADR Number**: 0004
- **Status**: Accepted
- **Date**: 2026-03-15
- **Deciders**: buenhyden
- **layer**: meta

## 2. Context & Problem Statement

Documentation fragmented and deeply nested. AI Agents prone to context bloat. We need a standardized way to trigger specialized rules.

## 3. Decision Drivers (Senior)

- **Token Economy**: Minimize expensive repeated instruction loading.
- **Decision Authority**: Clear boundaries between global shims and local scopes.
- **DevOps Alignment**: Treat documentation structures as rigorously as infrastructure paths.

## 4. Decision Outcome

**Chosen option: "Hub Consolidation & Lazy Loading"**

### Rationale
Using a lightweight shim (`AGENTS.md`) to route to deep documentation ensures the "Initial Thought" turn remains under 2k tokens while maintaining access to infinite complexity.

### Consequences
- **Positive**: Reduced token usage, higher fidelity in complex reasoning phases.
- **Negative**: Minimal latency increase during the "Read Scope" turn.

## 5. Technical Debt & Risk Assessment (Senior)

- **Debt Incurred**: The shim logic relies on agent compliance with the `Lazy Loading Protocol`. Enforcement is currently social/instruction-based, not hard-coded.
- **Risk Score**: Medium
- **Mitigation Plan**: Implement a "Scope Validator" tool in the future to check if an agent has loaded the required documents for a task.

## 6. Deferred Decisions (ADL - Architecture Decision Log)

- **Manual vs Guide Naming Strategy**: **DECIDED (2026-03-24)** - Shifted all operational docs to `*-manual-template.md`.
- **Instruction Pruning Automation**: Deferred.

## 7. Related Artifacts
- **PRD Reference**: `[../prd/2026-03-15-documentation-refactor-prd.md]`
- **Spec Reference**: `[../specs/2026-03-16-doc-and-agent-refactor-spec.md]`
