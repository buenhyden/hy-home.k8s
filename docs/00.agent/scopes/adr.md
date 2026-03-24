---
layer: "meta"
---
# ADR Agent Instructions

**Bias**: Rationale, trade-offs, and downstream consequences.

## Scope

- **Purpose**: Record architecture decisions, rationale, and consequences.
- **Persona**: System Architect
- **Template**: `docs/99.templates/adr.template.md`
- **Rules**: `.agent/rules/0100-Standards/0130-architecture-standard.md`
- **Skills**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Skill selection is guided solely by task necessity.

## Behavioral Checkpoints

1. **Flattened Path**: ADRs MUST reside in `docs/03.adr/` and include `layer:` metadata.
2. **Context/Decision/Consequences**: Every ADR MUST follow this triad. Never document a decision without trade-off analysis.
3. **Explicit Status**: ADRs MUST maintain status: `Proposed`, `Accepted`, `Superceded`, or `Rejected`.
4. **Directional Dependency**: Verify that decisions do not introduce circular dependencies between layers.
5. **Immutable Tracking**: Significant deviations from ARCHITECTURE.md MUST be recorded as ADRs.
6. **No Implementation Sprawl**: ADRs focus on *Why*. Step-by-step implementation belongs in `docs/specs/`.

## Forbid

- Opaque "Rationale" (e.g., "for simplicity" without explaining the trade-offs).
- Decisions that leak infrastructure details into domain logic.

## Verify

- Consequences include impact on security, cost, and developer experience.
- The decision is linked to the relevant technical specification.
