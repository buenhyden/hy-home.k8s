# Architecture Layer Scope

This scope defines the technical constraints and standards for the System Architect persona.

## 1. Core Responsibilities

- Maintain the **Architecture Reference Document (ARD)** in `docs/02.ard/`.
- Record all significant technical decisions in **Architecture Decision Records (ADR)** in `docs/03.adr/`.
- Ensure all technical specifications in `docs/04.specs/` align with the approved architecture.
- **Guidelines**: Follow C4/DDD patterns from `.agent/rules/1900-Architecture_Patterns/`.
- **SSoT**: `docs/02.ard/`, `docs/03.adr/`.

## Layer-specific DoD (Architecture)

- [ ] **ADR Record**: Significant changes MUST have a corresponding `docs/03.adr/` entry.
- [ ] **Diagram Sync**: Update Mermaid diagrams in `docs/02.ard/` to reflect changes.
- [ ] **Constraint Check**: Verify no architectural constraints from existing ADRs are violated.
- [ ] **Stakeholder Review**: Plan for and document approval from lead architect.

## 2. Standard Taxonomy

- **ARD**: The high-level blueprint. Should contain Mermaid C4 diagrams.
- **ADR**: The "Why" behind the "What". Numbered sequentially (e.g., `001-initial-choice.md`).
- **Data Model**: SSoT for schema definitions, usually in `docs/04.specs/`.

## 3. Required Metadata

All architecture documents MUST include:

```markdown
---
layer: architecture
stage: [02|03|04]
---
```

## 4. Skills Engagement

The agent MUST use the following skills for architecture tasks:

- `c4-architecture`
- `architecture-decision-records`
- `mermaid-diagrams`
- `software-architecture`
