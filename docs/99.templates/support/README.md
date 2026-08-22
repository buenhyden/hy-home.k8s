# Template Support Contracts

> Template-specific contracts, governance, routing, frontmatter schema, and
> legacy cleanup rules for `docs/99.templates/`.

## Overview

This folder separates template support rules from template forms. Template
forms remain the files authors copy from, while these support documents define
how those forms are classified, routed, validated, and applied to authored
documents.

The support layer exists so `docs/99.templates/README.md` can remain an
inventory and entrypoint instead of carrying every contract, governance rule,
and legacy cleanup rule inline.

### Collection Readers

Primary readers:

- Documentation Writers
- Platform Engineers
- Repository Maintainers
- AI Agents

## Scope

### In Scope

- Template support responsibility boundaries and route-selection procedure.
- SDLC lifecycle/handoff and common-role rationale.
- Frontmatter metadata rationale; exact profile values remain registry-owned.
- Legacy template, key, value, and section cleanup rules.
- Validator and hook alignment requirements for template routing.

### Out of Scope

- Template form bodies that authors copy into new documents.
- Authored PRD, AD, ADR, Spec, Plan, Task, operations, reference, or archive
  documents.
- Runtime, cluster, Vault, GitHub remote, paid job, or cloud mutation.

## Item Index

```text
support/
├── document-contract.md
├── document-lifecycle.md
├── document-profiles.json
└── README.md
```

## Add and Find

1. Update the registry before changing a template form path or frontmatter
   profile; update support only when its rationale or procedure changes.
2. Keep template form instructions in `docs/99.templates/templates/**` and
   keep contract rules in this `support/` folder.
3. Keep detailed contract text here, not in `docs/99.templates/README.md`.
4. When a support rule changes route behavior, update Stage 00 governance,
   hook hints, validators, and affected authored docs in the matching
   implementation unit.
5. Run `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .`
   after support changes.

### Relative Link Rules

This README is located at `docs/99.templates/support/`.

- Link to template forms with `../templates/**`.
- Link to Stage 00 governance with `../../00.agent-governance/`.
- Link to stage documents with `../../<stage>/`.
- Keep optional future paths as code literals until the files exist.

### Support Document Index

| Document | Responsibility |
| --- | --- |
| [Document Contract](./document-contract.md) | Owns exact-one-profile selection, form/body/frontmatter rationale, and the protected contract boundary. |
| [Document Lifecycle](./document-lifecycle.md) | Owns lifecycle, supersession, retention, archive, date-exception, and legacy-disposition rationale. |
| [Document Profile Registry](./document-profiles.json) | Canonical machine contract for document classification, paths, frontmatter, lifecycle domains, headings, templates, and ownership declarations. |

## Related Documents

- [Templates README](../README.md)
- [Document Registry Form Schema](../contracts/registry-form.schema.json)
- [Document Profile Registry](./document-profiles.json)
- [Spec-Driven SDLC and Document Contracts](../../90.references/research/2026-08-08-wer/spec-driven-sdlc-and-document-contracts.md)
- [Document Authoring Policy](../../00.agent-governance/rules/document-authoring.md)
- [Migration Spec](../../03.specs/0011-template-contract-governance-migration/spec.md)
- [Migration Plan](../../03.specs/0011-template-contract-governance-migration/plan.md)
- [Migration Task](../../03.specs/0011-template-contract-governance-migration/README.md)
