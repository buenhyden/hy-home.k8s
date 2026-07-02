---
title: 'Template Forms'
type: template-support
status: draft
owner: platform
updated: 2026-07-03
---

# Template Forms

> Copy-ready template forms for SDLC and common repository documentation.

## Overview

This folder contains template forms only. Rules, contracts, routing, schema,
and legacy cleanup guidance live in `../support/`.

## Audience

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

## Structure

```text
templates/
├── common/
│   ├── archive-tombstone.template.md
│   ├── memory.template.md
│   ├── progress.template.md
│   ├── readme.template.md
│   └── reference.template.md
└── sdlc/
    ├── architecture/
    ├── execution/
    ├── operations/
    ├── requirements/
    └── specs/
```

## How to Work in This Area

1. Choose the template through `../README.md` and `../support/template-routing.md`.
2. Copy the matching template into the final authored document path.
3. Remove placeholder text, comments, and template instructions from authored
   documents.
4. Keep native machine-readable templates parseable in their own format.
5. Update support contracts and validators when adding, moving, or removing a
   template form.

## Link Basis

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
