---
layer: "meta"
---
# ADR 003: Documentation Taxonomy and Metadata Standard

## Status

Proposed

## Context

The project documentation structure grew organically. To ensure clarity for both humans and AI agents, a stricter, flattened taxonomy is required alongside mandatory metadata for classification.

## Decision

1. **Flattened Folders**: All documentation MUST live in root-level `docs/` subdirectories based on type: `ard`, `adr`, `prd`, `specs`, `plans`, `runbooks`, `operations`.
2. **Mandatory Metadata**: All files in these folders MUST contain YAML frontmatter with a `layer` key identifying the functional component (e.g., `infra`, `gitops`, `app`, `meta`).
3. **Lazy Loading Implementation**: Implement a mapping between `rules/` and `scopes/` in `docs/agentic/agent-instructions.md` to facilitate lazy loading of specialized instructions.

## Consequences

- **Positive**: More deterministic file discovery for agents; clearer division of concerns.
- **Negative**: Existing links might break and require updating.
