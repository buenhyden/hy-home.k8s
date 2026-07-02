---
title: 'Template Frontmatter Schema'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-03
---

# Template Frontmatter Schema

## Overview

This document defines the canonical frontmatter schema for Markdown template
families and authored documents. Phase 3 applies this schema to template files,
authored documents, and repository validation.

## Purpose

Frontmatter is repository metadata used for lifecycle status, ownership,
document classification, freshness, and validation. It should contain only
metadata that belongs to the document type. It should not duplicate headings,
content summaries, route tables, or governance prose.

## Current Baseline

Most Markdown documents with frontmatter use these keys:

```yaml
title: '<Document Title>'
type: <profile-family>/<document-role>
status: draft
owner: platform
updated: YYYY-MM-DD
```

Exceptions:

- README files are frontmatter-free.
- `progress.template.md` is an appendable ledger entry template.
- OpenAPI, GraphQL, and protobuf templates must remain native to their format.

## Profile Families

| Profile Family | Document Role | `type` Value | Required Keys | Notes |
| --- | --- | --- | --- | --- |
| `sdlc` | PRD | `sdlc/prd` | `title`, `type`, `status`, `owner`, `updated` | Stage 01 product requirements. |
| `sdlc` | ARD | `sdlc/ard` | `title`, `type`, `status`, `owner`, `updated` | Stage 02 architecture requirements. |
| `sdlc` | ADR | `sdlc/adr` | `title`, `type`, `status`, `owner`, `updated` | Stage 02 architecture decisions. |
| `sdlc` | Spec | `sdlc/spec` | `title`, `type`, `status`, `owner`, `updated` | Stage 03 parent implementation spec. |
| `sdlc` | API spec | `sdlc/api-spec` | `title`, `type`, `status`, `owner`, `updated` | Feature-local API contract. |
| `sdlc` | Agent design | `sdlc/agent-design` | `title`, `type`, `status`, `owner`, `updated` | Feature-local agent behavior and safety design. |
| `sdlc` | Data model | `sdlc/data-model` | `title`, `type`, `status`, `owner`, `updated` | Feature-local data model. |
| `sdlc` | Tests | `sdlc/tests` | `title`, `type`, `status`, `owner`, `updated` | Feature-local test and evaluation strategy. |
| `sdlc` | Plan | `sdlc/plan` | `title`, `type`, `status`, `owner`, `updated` | Stage 04 execution plan. |
| `sdlc` | Task | `sdlc/task` | `title`, `type`, `status`, `owner`, `updated` | Stage 04 execution evidence. |
| `sdlc` | Guide | `sdlc/guide` | `title`, `type`, `status`, `owner`, `updated` | Stage 05 stable-state guide. |
| `sdlc` | Policy | `sdlc/policy` | `title`, `type`, `status`, `owner`, `updated` | Stage 05 operational policy. |
| `sdlc` | Runbook | `sdlc/runbook` | `title`, `type`, `status`, `owner`, `updated` | Stage 05 executable operational procedure. |
| `sdlc` | Incident | `sdlc/incident` | `title`, `type`, `status`, `owner`, `updated` | Incident fact record. |
| `sdlc` | Postmortem | `sdlc/postmortem` | `title`, `type`, `status`, `owner`, `updated` | Incident analysis and prevention follow-up. |
| `content` | Reference | `content/reference` | `title`, `type`, `status`, `owner`, `updated` | Durable reference material under Stage 90. |
| `content` | Archive Tombstone | `content/archive-tombstone` | `title`, `type`, `status`, `owner`, `updated` | Archive Tombstones use `status: archived`. |
| `content` | README | none | none | README files remain frontmatter-free. |
| `governance` | Governance reference | `governance/reference` | `title`, `type`, `status`, `owner`, `updated` | Stage 00 governance reference documents with frontmatter. |
| `governance` | Governance memory | `governance/memory` | `title`, `type`, `status`, `owner`, `updated` | Standalone governance memory. |
| `governance` | Progress entry | none | none | Progress entries are appended sections, not whole documents. |
| `governance` | Template support | `governance/template-support` | `title`, `type`, `status`, `owner`, `updated` | Support docs under `docs/99.templates/support/**`. |
| `machine-contract` | `machine.openapi` | n/a | n/a | OpenAPI root stays native YAML. |
| `machine-contract` | `machine.graphql` | n/a | n/a | GraphQL root stays schema text. |
| `machine-contract` | `machine.protobuf` | n/a | n/a | Protobuf root stays `.proto` text. |

## Key Rules

- `title` is the human-readable document title.
- `type` classifies the document role and must use a namespaced value from
  the profile family table.
- `status` is the lifecycle state. New authored documents start as `draft`
  unless a template has a fixed state such as archive Tombstones.
- `owner` is `platform` for repository-authored documents.
- `updated` uses an ISO calendar date.
- Do not quote scalar `owner` values when the value is the canonical owner.

## Legacy Cleanup Rules

- Use `owner: platform` in active authored frontmatter and task owner cells.
- Use `type: sdlc/policy` for operations policy documents.
- Replace old simple `type` values with the namespaced values in this schema.
- Remove keys that duplicate the same role as another key unless the target
  profile explicitly allows both.
- Do not add frontmatter to README files or native machine-readable templates.

## Validation Contract

`scripts/validate-repo-quality-gates.sh` must ensure each routed Markdown path
has exactly one frontmatter profile. The gate rejects:

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
