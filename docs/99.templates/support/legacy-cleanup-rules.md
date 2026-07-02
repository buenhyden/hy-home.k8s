---
title: 'Template Legacy Cleanup Rules'
type: template-support
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
| `operation.template.md` | `policy.template.md`, then target Phase 3 policy profile | Phase 3 |
| `type: operation` | `type: policy`, then target Phase 3 namespaced value | Phase 3 |
| `platform-team` | `platform` | Phase 3 |
| `Related References` | `Related Documents` | Phase 3 |
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
rg -n "operation\\.template\\.md|platform-team|Related References" docs scripts .codex AGENTS.md RTK.md
rg -n "^type:\\s*operation\\s*$" docs
rg -n "Target: docs/|Use this template" docs
```

Before the cleanup phases, these commands may return existing active and
historical matches. After the migration closes, active matches should be zero
or explicitly allow-listed as historical evidence.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Template Routing](./template-routing.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
