---
title: 'Template Legacy Cleanup Rules'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-03
---

# Template Legacy Cleanup Rules

## Overview

This document defines active legacy template names, frontmatter values,
sections, and route references to remove during the migration. Historical
evidence can remain only when it is clearly dated and not an active contract.

## Purpose

Legacy cleanup keeps active documentation from presenting old paths, duplicate
roles, or obsolete sections as current rules.

## Legacy Items to Remove from Active Contracts

| Legacy Item | Replacement | Cleanup Phase |
| --- | --- | --- |
| Deprecated operations-template route | `policy.template.md` and `type: sdlc/policy` | Phase 3 |
| Deprecated operations policy frontmatter type | `type: sdlc/policy` | Phase 3 |
| Deprecated team-owner value | `platform` | Phase 3 |
| Deprecated README related-document heading | `Related Documents` | Phase 3 |
| Flat template links in active route contracts | `docs/99.templates/templates/**` links | Phase 2 |
| Copied `Target:` template comments in authored docs | Topic-specific content with correct `Related Documents` | Phase 4 |
| Copied `Use this template` instructions in authored docs | Remove from authored docs | Phase 4 |
| README contract bodies that duplicate support docs | Brief pointers to support docs | Phase 1 and Phase 4 |

## Active vs Historical References

Active contracts include:

- Template README inventory and support docs.
- Stage 00 governance rules.
- Hook hints.
- Validator mappings.
- Stage README authoring instructions.
- Authored documents that describe current policy or current routing.

Historical references include:

- Dated progress ledger entries.
- Old completed plan or task evidence that records a past drift.
- Archive Tombstones.

Historical references may remain only when they are explicitly dated and cannot
be mistaken for current instructions.

## Cleanup Order

1. Create support contract baseline.
2. Move template files and update route enforcement.
3. Normalize frontmatter and remove active legacy values.
4. Apply the contract to authored documents and indexes.
5. Run final legacy searches and record evidence.

## Validation Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
rg -n "Target: docs/|Use this template" docs
```

The repository quality gate owns the active legacy denylist and namespaced
frontmatter profile checks. The template-residue scan may return template
files under `docs/99.templates/templates/**`; authored docs must not retain
those markers.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Template Routing](./template-routing.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
