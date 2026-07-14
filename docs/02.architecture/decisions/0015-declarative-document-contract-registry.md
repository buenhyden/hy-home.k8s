---
title: 'ADR-0015: Declarative Document Contract Registry'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-07-12
---

# ADR-0015: Declarative Document Contract Registry

## Overview

This decision selects a declarative, machine-readable registry as the single
owner of document routes, metadata profiles, lifecycle states, section
profiles, README profiles, and explicit exceptions.

## Context

The repository currently repeats route and profile facts across Stage 99
support tables, the templates README, template files, a large shell validator,
Stage 00 routing rules, and CI path filters. The copies agree syntactically
enough for the present gate to pass but allow semantically invalid states,
generic README structure, duplicated template guidance, and uncovered CI paths.
The approved program requires destructive consolidation while preserving
historical evidence and provider-native schemas.

## Decision

- Create a versioned JSON registry validated by JSON Schema 2020-12.
- Declare exact paths or patterns, profile family, type, required and allowed
  keys, repository key-order convention, type-specific states, required and
  allowed sections, template route, and exception class.
- Set `additionalProperties: false` or the appropriate composed-schema
  equivalent for exact metadata profiles.
- Keep the current five-key authored baseline and the existing Tombstone
  extension; add no universal metadata without a named consumer.
- Infer README profile by path and keep README frontmatter-free.
- Keep affected-surface-to-validator selection in a separate machine contract
  because execution routing is not document schema.
- Make Markdown support, README indexes, Stage 00 summaries, hooks, and CI
  consumers of these machine contracts rather than parallel owners.
- Use compatibility mode during corpus migration and enable strict enforcement
  only after all routed documents pass.

## Explicit Non-goals

- Treating key order as YAML data semantics.
- Treating YAML frontmatter as part of CommonMark or GFM.
- Replacing provider-native agent metadata, GitHub-native control files, or
  native OpenAPI, GraphQL, protobuf, Kubernetes, HCL, Rego, or TOML formats.
- Adding `id`, `created`, `review_due`, `supersedes`, or Release metadata without
  an approved automation consumer.
- Generating every explanatory document from the registry.

## Consequences

- **Positive**: One fact has one owner; validators can use fixtures; paths and
  state domains become reviewable data; README profiles and exception classes
  become explicit; copied route tables can be deleted.
- **Trade-offs**: The registry and its schema become protected surfaces;
  migration requires compatibility logic and a complete inventory; reviewers
  must distinguish machine facts from human rationale; JSON is less concise
  than duplicated prose for casual edits.

## Alternatives

### Keep hardcoded mirrors synchronized

- Good: Small initial change and no new contract format.
- Bad: Preserves the exact failure mode identified by the audit and requires
  manual multi-owner updates.

### Parse one Markdown support table as the machine contract

- Good: Human-readable and avoids an additional file.
- Bad: Couples prose formatting to execution, makes nested profile constraints
  awkward, and encourages support documents to become executable DSLs.

### Generate all governance and templates from one schema

- Good: Maximum mechanical consistency.
- Bad: Erases topic-specific rationale, creates noisy generated Markdown, and
  exceeds demonstrated consumer value.

## Traceability

- **PRD**: [Workspace Document Assurance Modernization](../../01.requirements/005-workspace-document-assurance-modernization.md)
- **ARD**: [Workspace Document Assurance Operating Model](../requirements/0008-workspace-document-assurance-operating-model.md)
- **Related ADR**: [Program-to-Tranche Lineage](./0016-program-to-tranche-document-lineage.md)
- **First Spec**: [Document Contract Registry](../../03.specs/026-document-contract-registry/spec.md)
- **JSON Schema Object Validation**: [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation)
- **YAML Mapping Order**: [YAML 1.2.2](https://yaml.org/spec/1.2.2/)
