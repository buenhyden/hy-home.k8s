# ADR 0003: Documentation Taxonomy and Metadata Standard

- **Status**: Proposed
- **Date**: 2026-03-15
- **layer:** meta

**Overview (KR):** 리포지토리의 문서 체계를 flattened taxonomy로 전환하고, 모든 문서에 layer 메타데이터를 필수적으로 포함하도록 강제함.

## Related Documents

## Context

The project documentation structure grew organically. To ensure clarity for both humans and AI agents, a stricter, flattened taxonomy is required alongside mandatory metadata for classification.

## Decision

1. **Flattened Folders**: All documentation MUST live in root-level `docs/` subdirectories based on type: `ard`, `adr`, `prd`, `specs`, `plans`, `runbooks`, `operations`.
2. **Mandatory Metadata**: All files in these folders MUST contain YAML frontmatter with a `layer` key identifying the functional component (e.g., `infra`, `gitops`, `app`, `meta`).
3. **Lazy Loading Implementation**: Implement a mapping between `rules/` and `scopes/` in `docs/agentic/agent-instructions.md` to facilitate lazy loading of specialized instructions.

## Consequences

- **Positive**: More deterministic file discovery for agents; clearer division of concerns.
- **Negative**: Existing links might break and require updating.
