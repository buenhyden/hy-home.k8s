---
title: 'Template Legacy Cleanup Rules'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-05
---

# Template Legacy Cleanup Rules

## Overview

This document defines active legacy template names, frontmatter values,
sections, and route references rejected by current contracts. Historical
evidence can remain only when it is clearly dated and not an active contract.

## Purpose

Legacy cleanup keeps active documentation from presenting old paths, duplicate
roles, or obsolete sections as current rules.

The [Document Profile Registry](./document-profiles.json) owns current machine
values. This document owns only the migration and removal policy for identifying
and disposing of legacy representations. The [Document Type Format and Evidence
Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
records the research basis for the replacement families without becoming an
enforcement source.

## Legacy Items to Remove from Active Contracts

| Legacy Item | Replacement | Current Enforcement |
| --- | --- | --- |
| Deprecated operations policy template route | `policy.template.md` and `type: sdlc/policy` | Reject in active contracts |
| Deprecated operations policy frontmatter type | `type: sdlc/policy` | Reject in active frontmatter |
| Deprecated team-owner value | `platform` | Reject in active owner fields |
| Deprecated README related-link heading alternatives | Required active heading: `## Related Documents` | Reject only deprecated alternatives; do not reject or remove the required active heading |
| Flat template links in active route contracts | `docs/99.templates/templates/**` links | Reject in active route contracts |
| Copied target-path template comments in authored docs | Topic-specific content with correct `Related Documents` | Reject in authored documents |
| Copied template-use instructions in authored docs | Remove from authored docs | Reject in authored documents |
| README contract bodies that duplicate support docs | Brief pointers to support docs | Keep README entries concise |
| GitHub-native Markdown frontmatter | Frontmatter-free `.github` control body with canonical links | Reject on `.github/ABOUT.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/SECURITY.md` |
| Provider-latest claims in cloud example indexes and example-local SDLC snapshot docs | Dated Cloud Example Snapshot wording, or a current approved provider refresh | Treat provider-latest claims as legacy unless backed by approved refresh evidence |
| Missing frontmatter on non-README cloud example docs | Role-appropriate `sdlc/*` frontmatter under the example-local SDLC snapshot route | Reject after the example-local route is enabled for the target provider tree |
| Active tracked scratch residue named or classified as backup files, auth files, token caches, shell history, local diagnostics, or secret-bearing logs | Delete, ignore as temporary non-secret scratch, or promote non-secret durable findings to the canonical docs taxonomy | Reject as active tracked scratch residue |

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
be mistaken for current instructions. When a dated audit finding has been
resolved, keep the original finding as historical evidence and add resolved
context in the next audit or normalization task instead of rewriting it into a
false current-state claim.

## Current Review Order

1. Confirm support contracts describe the current steady-state model.
2. Confirm template files and route enforcement use categorized paths.
3. Confirm active frontmatter uses current profile values.
4. Confirm authored documents and indexes follow the current contracts.
5. Run legacy searches and record evidence for any accepted historical matches.

## Validation Commands

```bash
bash scripts/validate-repo-quality-gates.sh .
template_instruction='Use this'
template_instruction="${template_instruction} template"
target_comment='Target:'
target_comment="${target_comment} docs/"
rg -n "${target_comment}|${template_instruction}" docs/99.templates/templates
```

The repository quality gate owns the active legacy denylist and namespaced
frontmatter profile checks. Template files may keep starter comments and
template-use instructions; authored docs must not retain those markers.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Template Routing](./template-routing.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
