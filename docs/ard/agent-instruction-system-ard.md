- **Status**: Approved
- **Owner**: buenhyden
- **Scope**: master
- **layer:** architecture
- **Parent Master ARD**: `[../ard/documentation-architecture-ard.md]`
- **PRD Reference**: `[../prd/2026-03-16-documentation-system-prd.md]`

**Overview (KR):** AI 에이전트의 효율적인 협업을 위해 지침 문서를 체계적으로 관리하고 로딩 성능을 최적화하는 에이전트 지침 시스템의 아키텍처를 정의합니다.

# Agent Instruction System Architecture

## Summary

The Agent Instruction System is the primary governance layer for Human-AI collaboration in the `hy-home.k8s` repository. It is designed to be high-performance (low token overhead) and strictly spec-compliant.

## Boundaries

- **Owns**: Instruction dispatching logic, rule set organization, and intent-to-scope mapping.
- **Consumes**: Markdown files in `docs/agentic/`, user intent signals.
- **Does Not Own**: Actual code implementation logic beyond document structure rules.

## Ownership

- **Primary owner**: buenhyden
- **Primary artifacts**: `docs/agentic/`, `AGENTS.md`
- **Operational evidence**: `[../runbooks/documentation-management.md]`

## 1. Overview

The Agent Instruction System is the primary governance layer for Human-AI collaboration in the `hy-home.k8s` repository. It is designed to be high-performance (low token overhead) and strictly spec-compliant.

## 2. Component Diagram (Mermaid)

```mermaid
graph TD
    A[CLAUDE.md / GEMINI.md] --> B[AGENTS.md]
    B --> C[Gateway: agent-instructions.md]
    C --> D{Intent Dispatcher}
    D --> E[Governing Rules: rules/*.md]
    D --> F[Task Scopes: scopes/*.md]
    E --> G[Context Load]
    F --> G[Context Load]
```

## 3. Communication Patterns

### Lazy Loading Protocol

1. **Discovery**: Entry points (`AGENTS.md`) provide a minimal context.
2. **Intent Recognition**: The agent identifies the task type (e.g., "Create a spec").
3. **Scoped Injection**: The agent reads only the files listed in the **Intent-to-Scope Mapping** within `agent-instructions.md`.

### Metadata standards

- Every agent-generated file MUST contain a `layer` attribute in YAML frontmatter.
- Valid Layers: `meta`, `infra`, `gitops`, `app`, `ops`.

## 4. Constraint Matrix

| Constraint | Enforcement |
| --- | --- |
| **Max Token Load** | 15k Tokens (estimated) |
| **Instruction Location** | `docs/agentic/` |
| **Template Location** | `templates/` |
| **Persistence** | Plural directory paths only (`plans/`, `specs/`) |

## 5. Directory Organization

- `docs/agentic/rules/`: Persona-level behavioral rules.
- `docs/agentic/scopes/`: Task-level technical instructions and target paths.
