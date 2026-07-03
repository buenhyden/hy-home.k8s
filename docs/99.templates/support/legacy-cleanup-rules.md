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
sections, and route references rejected by current contracts. Historical
evidence can remain only when it is clearly dated and not an active contract.

## Purpose

Legacy cleanup keeps active documentation from presenting old paths, duplicate
roles, or obsolete sections as current rules.

## Legacy Items to Remove from Active Contracts

| Legacy Item | Replacement | Current Enforcement |
| --- | --- | --- |
| Deprecated operations-template route | `policy.template.md` and `type: sdlc/policy` | Reject in active contracts |
| Deprecated operations policy frontmatter type | `type: sdlc/policy` | Reject in active frontmatter |
| Deprecated team-owner value | `platform` | Reject in active owner fields |
| Deprecated README related-document heading | `Related Documents` | Reject in active README headings |
| Flat template links in active route contracts | `docs/99.templates/templates/**` links | Reject in active route contracts |
| Copied `Target:` template comments in authored docs | Topic-specific content with correct `Related Documents` | Reject in authored documents |
| Copied `Use this template` instructions in authored docs | Remove from authored docs | Reject in authored documents |
| README contract bodies that duplicate support docs | Brief pointers to support docs | Keep README entries concise |

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

## Current Review Order

1. Confirm support contracts describe the current steady-state model.
2. Confirm template files and route enforcement use categorized paths.
3. Confirm active frontmatter uses current profile values.
4. Confirm authored documents and indexes follow the current contracts.
5. Run legacy searches and record evidence for any accepted historical matches.

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
