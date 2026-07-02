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
and migration rule inline.

## Audience

Primary readers:

- Documentation Writers
- Platform Engineers
- Repository Maintainers
- AI Agents

## Scope

### In Scope

- Template support contracts and route ownership.
- SDLC and common documentation governance.
- Frontmatter profile rules.
- Legacy template, key, value, and section cleanup rules.
- Validator and hook alignment requirements for template routing.

### Out of Scope

- Template form bodies that authors copy into new documents.
- Authored PRD, ARD, ADR, Spec, Plan, Task, operations, reference, or archive
  documents.
- Runtime, cluster, Vault, GitHub remote, paid job, or cloud mutation.

## Structure

```text
support/
├── common-documentation-governance.md
├── documentation-contract.md
├── frontmatter-schema.md
├── legacy-cleanup-rules.md
├── sdlc-governance.md
├── template-routing.md
└── README.md
```

## How to Work in This Area

1. Update support contracts before changing template form paths or
   frontmatter profiles.
2. Keep template form instructions in `docs/99.templates/templates/**` and
   keep contract rules in this `support/` folder.
3. Keep detailed contract text here, not in `docs/99.templates/README.md`.
4. When a support rule changes route behavior, update Stage 00 governance,
   hook hints, validators, and affected authored docs in the matching
   implementation phase.
5. Run `git diff --check` and `bash scripts/validate-repo-quality-gates.sh .`
   after support changes.

## Link Basis

This README is located at `docs/99.templates/support/`.

- Link to template forms with `../templates/**`.
- Link to Stage 00 governance with `../../00.agent-governance/`.
- Link to stage documents with `../../<stage>/`.
- Keep optional future paths as code literals until the files exist.

## Support Document Index

| Document | Responsibility |
| --- | --- |
| [Documentation Contract](./documentation-contract.md) | Separates template forms, support contracts, Stage 00 governance, and authored docs. |
| [SDLC Governance](./sdlc-governance.md) | Defines SDLC lifecycle template responsibilities. |
| [Common Documentation Governance](./common-documentation-governance.md) | Defines README, reference, archive, memory, and progress template responsibilities. |
| [Frontmatter Schema](./frontmatter-schema.md) | Defines current and target frontmatter profile rules. |
| [Template Routing](./template-routing.md) | Defines the current `templates/**` route map. |
| [Legacy Cleanup Rules](./legacy-cleanup-rules.md) | Defines active legacy keys, values, sections, and routes to remove. |

## Related Documents

- [Templates README](../README.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Migration Spec](../../03.specs/011-template-contract-governance-migration/spec.md)
- [Migration Plan](../../04.execution/plans/2026-07-03-template-contract-governance-migration.md)
- [Migration Task](../../04.execution/tasks/2026-07-03-template-contract-governance-migration.md)
