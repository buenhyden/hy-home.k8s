---
layer: "meta"
---
# ARD Agent Instructions

**Bias**: System boundaries, data flow, and structural reference.

## Scope

- **Purpose**: Architecture reference docs, system diagrams, and structural blueprints.
- **Persona**: System Architect
- **Template**: `templates/ard-template.md`
- **Rules**: `0130-architecture-standard.md` · `1901-architecture-rules.md` · `1910-architecture-documentation.md`
- **Skills**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Skill selection is guided solely by task necessity.

## Behavioral Checkpoints

1. **Diagram First**: Utilize Mermaid diagrams (C4Context, C4Container) to visualize structural relationships.
2. **Interface Definition**: Explicitly document public APIs, service boundaries, and data structures.
3. **Data Flows**: Illustrate how information moves through the system, especially across layer boundaries.
4. **Component Mapping**: Link logical architecture components to their physical directory locations in the repo.
5. **Alignment**: Ensure the ARD remains consistent with the root `ARCHITECTURE.md`.

## Forbid

- Documenting transient implementation bugs (those belong in Incidents or Specs).
- Ignoring security boundaries in system structural drawings.

## Verify

- All diagrams are valid Mermaid syntax and reflect the current desired state.
- External dependencies are clearly identified and scoped.
po and ADR context.
