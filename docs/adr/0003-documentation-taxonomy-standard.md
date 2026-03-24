---
title: 'ADR 0003: Documentation Taxonomy and Metadata Standard'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'meta']
layer: "meta"
---

## 1. Metadata

- **ADR Number**: 0003
- **Status**: Accepted
- **Date**: 2026-03-15
- **Deciders**: buenhyden
- **layer**: meta

## 2. Context & Problem Statement

The project documentation structure grew organically. To ensure clarity for both humans and AI agents, a stricter, flattened taxonomy is required alongside mandatory metadata for classification.

## 3. Decision Drivers (Senior)

- **Determinism**: Agents must be able to predict file locations based on type.
- **Context Management**: Metadata enables programmatic filtering by AI shims.
- **Maintainability**: Root-level categorization prevents "deep nesting" sprawl.

## 4. Decision Outcome

**Chosen option: "Flattened Taxonomy + Mandatory Metadata"**

### Rationale
Flattening the structure directly reduces path-traversal complexity for agents. Metadata (`layer:`) allows for precise context injection during LLM turns.

### Consequences
- **Positive**: More deterministic file discovery; clearer division of concerns.
- **Negative**: Existing links require manual/automated fixing.

## 5. Technical Debt & Risk Assessment (Senior)

- **Debt Incurred**: The rapid transition from nested to flat hierarchy may result in "orphaned" files in git history if not properly pruned.
- **Risk Score**: Low
- **Mitigation Plan**: Run a weekly "Orphan Scan" to identify files not tracked by the primary [docs/README.md] index.

## 6. Deferred Decisions (ADL - Architecture Decision Log)

- **Automated Taxonomy Linting**: Deferred until the `pre-commit` hook pipeline is modernized.
- **Cross-Layer Dependency Mapping**: Deferred until the service mesh complexity warrants automated doc-graph generation.

## 7. Related Artifacts
- **PRD Reference**: `[../prd/2026-03-15-doc-and-agent-refactor-prd.md]`
