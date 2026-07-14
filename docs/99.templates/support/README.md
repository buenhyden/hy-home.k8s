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
- Authored PRD, ARD, ADR, Spec, Plan, Task, operations, reference, or archive
  documents.
- Runtime, cluster, Vault, GitHub remote, paid job, or cloud mutation.

## Item Index

```text
support/
├── common-documentation-governance.md
├── documentation-contract.md
├── document-profiles.json
├── document-profiles.schema.json
├── frontmatter-schema.md
├── legacy-cleanup-rules.md
├── sdlc-governance.md
├── template-routing.md
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
| [Documentation Contract](./documentation-contract.md) | Assigns ownership across forms, support, Stage 00 governance, authored documents, and enforcement surfaces. |
| [Document Profile Registry](./document-profiles.json) | Canonical machine contract for document classification, paths, frontmatter, lifecycle domains, headings, templates, and ownership declarations. |
| [Document Profile Registry Schema](./document-profiles.schema.json) | JSON Schema for the canonical document-profile registry shape and allowed values. |
| [SDLC Governance](./sdlc-governance.md) | Owns SDLC lifecycle rationale, handoff semantics, numbering, and active-surface rules. |
| [Common Documentation Governance](./common-documentation-governance.md) | Owns README, reference, archive, memory, and progress role rationale. |
| [Frontmatter Schema](./frontmatter-schema.md) | Explains metadata rationale while the registry owns exact profile values. |
| [Template Routing](./template-routing.md) | Owns the exact-one-profile selection procedure and examples without copying the registry inventory. |
| [Legacy Cleanup Rules](./legacy-cleanup-rules.md) | Owns migration and removal policy for legacy keys, values, sections, and route references. |

## Related Documents

- [Templates README](../README.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Migration Spec](../../03.specs/011-template-contract-governance-migration/spec.md)
- [Migration Plan](../../04.execution/plans/2026-07-03-template-contract-governance-migration.md)
- [Migration Task](../../04.execution/tasks/2026-07-03-template-contract-governance-migration.md)
