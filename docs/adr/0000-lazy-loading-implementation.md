---
title: 'ADR 0000: Lazy Loading Implementation for Agent Instructions'
status: 'Accepted'
date: '2026-03-16'
tags: ['adr', 'architecture']
layer: 'architecture'
---

# ADR: Lazy Loading Implementation for Agent Instructions - 0000

- **Status**: Accepted
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-16

**Overview (KR):** 에이전트 지침의 토큰 사용량을 최적화하기 위해 필요한 지침부만 선택적으로 로드하는 게이트웨이 방식의 Lazy Loading 메커니즘을 정의합니다.

## Context

The current AI Agent instruction set in `docs/agentic/` is growing large, leading to high token usage (~39k tokens) in the initial context window. This impacts performance, increases costs, and reduces the effective context available for actual task processing.

## Decision

We will implement a strict **Lazy Loading Protocol** for AI Agent instructions.

1. **Gateway-Only Initialization**: Agents will initially only load a thin "Gateway" document (`docs/agentic/agent-instructions.md`).
2. **Intent Dispatching**: The Gateway will contain a mapping table that links specific user intents to "Governing Rules" and "Task Scopes".
3. **On-Demand Loading**: Agents SHALL only read the Rule and Scope files relevant to the active task.
4. **Token Budgeting**: A hard limit of 15k tokens is set for the total instruction set loaded into the primary context at any given time.

## Rationale

- **Performance**: Reducing the initial context load speeds up agent response times and reduces latency.
- **Context Efficiency**: Saving 20k+ tokens in instructions provides significantly more "thinking space" for complex reasoning.
- **Maintainability**: Granular rules and scopes are easier to update and version-control than monolithic instruction files.

## Consequences

### Positive

- Faster initialization.
- Lower token costs.
- Higher precision in task-specific behaviors.

### Negative

- Requires agents to perform an extra "Read" step when switching intents.
- Slightly higher cognitive load for maintainers to distribute instructions correctly.

## Alternatives Considered

- **Monolithic Flattening**: Combining all instructions into one file. Rejected because it worsens the token bloat.
- **Skill-Based Loading**: Loading instructions based on which tools are available. Rejected because intent (PRD vs. Spec) is a better predictor of required logic than tool availability.
