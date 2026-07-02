---
title: 'Template Frontmatter Schema'
type: template-support
status: draft
owner: platform
updated: 2026-07-03
---

# Template Frontmatter Schema

## Overview

This document defines the current and target frontmatter schema for Markdown
template families. It is a migration baseline: Phase 1 records the contract,
Phase 3 applies the final schema to template files and authored documents.

## Purpose

Frontmatter is repository metadata used for lifecycle status, ownership,
document classification, freshness, and validation. It should contain only
metadata that belongs to the document type. It should not duplicate headings,
content summaries, route tables, or governance prose.

## Current Baseline

Most Markdown templates currently use these keys:

```yaml
title: '<Document Title>'
type: <simple-type>
status: draft
owner: platform
updated: YYYY-MM-DD
```

README, progress-entry, and native machine-readable templates are exceptions:

- README files are frontmatter-free.
- `progress.template.md` is an appendable ledger entry template.
- OpenAPI, GraphQL, and protobuf templates must remain native to their format.

## Target Profile Families

| Profile Family | Example Profile | Target `type` Value | Required Keys | Notes |
| --- | --- | --- | --- | --- |
| `sdlc` | `sdlc.spec` | `sdlc/spec` | `title`, `type`, `status`, `owner`, `updated` | Stage 03 parent implementation spec. |
| `sdlc` | `sdlc.task` | `sdlc/task` | `title`, `type`, `status`, `owner`, `updated` | Stage 04 execution evidence. |
| `sdlc` | `sdlc.policy` | `sdlc/policy` | `title`, `type`, `status`, `owner`, `updated` | Replaces legacy operation wording. |
| `content` | `content.reference` | `content/reference` | `title`, `type`, `status`, `owner`, `updated` | Durable reference material. |
| `content` | `content.archive-tombstone` | `content/archive-tombstone` | `title`, `type`, `status`, `owner`, `updated` | Archive Tombstones use `status: archived`. |
| `content` | `content.readme` | none | none | README files remain frontmatter-free. |
| `governance` | `governance.memory` | `governance/memory` | `title`, `type`, `status`, `owner`, `updated` | Standalone governance memory. |
| `governance` | `governance.progress-entry` | none | none | Progress entries are not whole-document frontmatter. |
| `machine-contract` | `machine.openapi` | n/a | n/a | OpenAPI root stays native YAML. |
| `machine-contract` | `machine.graphql` | n/a | n/a | GraphQL root stays schema text. |
| `machine-contract` | `machine.protobuf` | n/a | n/a | Protobuf root stays `.proto` text. |
| `template-support` | `template-support.rule` | `template-support` | `title`, `type`, `status`, `owner`, `updated` | Support docs under this folder. |

## Key Rules

- `title` is the human-readable document title.
- `type` classifies the document role. Phase 3 owns migration from simple
  values to namespaced values.
- `status` is the lifecycle state. New authored documents start as `draft`
  unless a template has a fixed state such as archive Tombstones.
- `owner` is `platform` for repository-authored documents.
- `updated` uses an ISO calendar date.

## Legacy Cleanup Rules

- Remove `platform-team` from active authored frontmatter and task owner cells.
- Replace legacy `type: operation` with the current policy type during the
  current baseline. Phase 3 then migrates policy documents to the final
  namespaced type value.
- Remove keys that duplicate the same role as another key unless the target
  profile explicitly allows both.
- Do not add frontmatter to README files or native machine-readable templates
  during this migration.

## Validation Contract

Phase 3 should update `scripts/validate-repo-quality-gates.sh` so each routed
Markdown path has exactly one frontmatter profile. The gate should reject:

- Missing required keys.
- Unsupported keys for the profile.
- Unsupported `type`, `status`, or `owner` values.
- Frontmatter on README files when not required.
- Markdown frontmatter in OpenAPI, GraphQL, or protobuf templates.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Migration Spec](../../03.specs/011-template-contract-governance-migration/spec.md)
