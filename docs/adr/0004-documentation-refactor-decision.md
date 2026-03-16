---
title: 'ADR 0004: Documentation Refactor and Lazy Loading'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'documentation']
layer: 'meta'
---

# ADR 0004: Documentation Refactor and Lazy Loading

- **Status**: Accepted
- **Date**: 2026-03-15
- **layer:** meta

**Overview (KR):** 대규모 상황 정보(Context)로 인한 성능 저하를 방지하기 위해 AI Agent의 지침을 지연 로딩(Lazy Loading) 방식으로 변경하고, 문서 구조를 평탄화합니다.

## Context

The repository documentation has become fragmented and sometimes deeply nested. AI Agents are prone to context bloat when they ingest too many instructions at once. We need a standardized way to trigger specific rules and load only the necessary scopes for a given task.

## Decision

- **Flattened Hierarchy**: Organize all documents in `docs/<type>/` (e.g., `docs/adr/`, `docs/prd/`).
- **Lazy Loading**: AI Agents MUST only load detailed instructions from `docs/agentic/` when triggered by a specific rule.
- **Explicit Triggers**: Use `AGENTS.md` as the root contract for these triggers.
- **Layer Metadata**: Mandate `layer:` in frontmatter to enable programmatic filtering.

## Consequences

- **Positive**: Reduced token usage, less hallucination, clearer authority boundaries.
- **Negative**: Requires agents to perform an extra look-up step to load instructions.

## Related Documents

- `[../specs/2026-03-15-documentation-refactor-spec.md]`
- `[../prd/documentation-refactor-prd.md]`
