# Template Forms

> Copy-ready template forms for SDLC and common repository documentation.

## Overview

This folder contains template forms only. Rules, contracts, routing, schema,
and legacy cleanup guidance live in `../support/`.

### Collection Readers

Primary readers:

- Documentation Writers
- Platform Engineers
- Repository Maintainers
- AI Agents

## Scope

### In Scope

- SDLC template forms under `sdlc/**`.
- Common documentation template forms under `common/**`.
- Native machine-readable contract templates for OpenAPI, GraphQL, and
  protobuf.

### Out of Scope

- Template governance rules.
- Frontmatter schema contracts.
- Authored stage documents.
- Runtime or external system actions.

## Item Index

```text
templates/
├── common/
│   ├── archive-record.template.md
│   ├── governance-reference.template.md
│   ├── memory.template.md
│   ├── progress.template.md
│   ├── readme-collection-index.template.md
│   ├── readme-implementation.template.md
│   ├── readme-repository.template.md
│   ├── readme-snapshot-pack.template.md
│   ├── readme-stage-index.template.md
│   ├── readme-workspace-staging.template.md
│   ├── reference.template.md
│   └── template-support.template.md
└── sdlc/
    ├── architecture/
    ├── execution/
    ├── operations/
    ├── requirements/
    └── specs/
```

## Add and Find

1. Choose the template through `../README.md` and `../support/template-routing.md`.
2. Copy the matching template into the final authored document path.
3. Remove placeholder text, comments, and template instructions from authored
   documents.
4. Keep native machine-readable templates parseable in their own format.
5. Update support contracts and validators when adding, moving, or removing a
   template form.

### Relative Link Rules

This README is located at `docs/99.templates/templates/`.

- Link to support contracts with `../support/`.
- Link to common templates with `./common/`.
- Link to SDLC templates with `./sdlc/`.
- Link to Stage 00 governance with `../../00.agent-governance/`.

## Related Documents

- [Templates README](../README.md)
- [Template Support Contracts](../support/README.md)
- [Template Routing](../support/template-routing.md)
- [Frontmatter Schema](../support/frontmatter-schema.md)
- [Canonical Task Form](./sdlc/execution/task.template.md)
