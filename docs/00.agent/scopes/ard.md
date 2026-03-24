---
layer: "meta"
---
# ARD Agent Instructions

**Bias**: System boundaries, data flow, and structural reference.

## Scope

- **Purpose**: Architecture reference docs, system diagrams, and structural blueprints.
- **Persona**: System Architect
- **Template**: `docs/99.templates/ard.template.md`
- **Rules**: `.agent/rules/0100-Standards/0130-architecture-standard.md`
- **Skills**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Skill selection is guided solely by task necessity.

## Behavioral Checkpoints

1. **Flattened Path**: ARDs MUST reside in `docs/02.ard/` and include `layer:` metadata.
2. **Diagram First**: Utilize Mermaid diagrams (C4Context, C4Container) to visualize structural relationships.
3. **Interface Definition**: Explicitly document public APIs, service boundaries, and data structures.
4. **Data Flows**: Illustrate how information moves through the system, especially across layer boundaries.
5. **Component Mapping**: Link logical architecture components to their physical directory locations in the repo.
6. **Alignment**: Ensure the ARD remains consistent with the root `ARCHITECTURE.md`.

## Forbid

- Documenting transient implementation bugs (those belong in Incidents or Specs).
- Ignoring security boundaries in system structural drawings.

## Verify

- All diagrams are valid Mermaid syntax and reflect the current desired state.
- External dependencies are clearly identified and scoped.
po and ADR context.
