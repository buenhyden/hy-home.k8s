---
title: 'ADR 0004: Documentation Refactor and Lazy Loading'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'documentation']
layer: 'meta'
---

# ADR: Documentation Refactor and Hub Consolidation - 0004

- **Status**: Decided
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-15

**Overview (KR):** 프로젝트 문서 구조의 복잡성을 해결하고 유지보수 효율성을 높이기 위해 대규모 리팩토링 및 표준화를 결정한 배경과 세부 전략을 기록합니다.
지연 로딩(Lazy Loading) 방식으로 변경하고, 문서 구조를 평탄화합니다.

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

- `[../specs/2026-03-16-doc-and-agent-refactor-spec.md]`
- `[../prd/2026-03-15-documentation-refactor-prd.md]`
