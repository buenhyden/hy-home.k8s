---
title: 'Template Frontmatter Schema'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-06
---

# Template Frontmatter Schema

## Overview

This document defines the canonical frontmatter schema for Markdown template
families and authored documents. This schema applies to Markdown template
files, authored documents, and repository validation.

## Purpose

Frontmatter is repository metadata used for lifecycle status, ownership,
document classification, freshness, and validation. It should contain only
metadata that belongs to the document type. It should not duplicate headings,
content summaries, route tables, or governance prose.

## Current Baseline

The machine-readable [Document Profile Registry](./document-profiles.json)
owns the exact required, allowed, and ordered key sets, lifecycle state domains,
heading sets, and template path for every profile. The following block remains
an illustrative authored-document example, not a second schema:

```yaml
title: '<Document Title>'
type: <profile-family>/<document-role>
status: draft
owner: platform
updated: YYYY-MM-DD
```

Exceptions:

- README files are frontmatter-free.
- `_workspace/README.md` is a frontmatter-free README. Ignored scratch files
  under `_workspace/**` are not authored documents.
- GitHub-native Markdown control files under `.github/` are
  frontmatter-free because GitHub renders or consumes their body directly.
- Cloud example docs under `examples/aws/docs/**` and
  `examples/azure/docs/**` are routed as example-local SDLC snapshot
  documents. Non-README Markdown in those trees uses the matching `sdlc/*`
  frontmatter type for its role, while README files remain frontmatter-free.
- `progress.template.md` is an appendable ledger entry template.
- OpenAPI, GraphQL, and protobuf templates must remain native to their format.

## Profile Families

The registry defines the complete profile set. The families remain useful as a
human model: SDLC profiles cover delivery records, common and governance
profiles cover durable repository support, README profiles stay
frontmatter-free, and explicit exception profiles preserve GitHub-native,
provider-native, generated, and native-contract behavior. Exact `type` values,
keys, states, headings, and templates must be read from the registry rather
than copied into a Markdown table.

## Key Rules

- `title` is the human-readable document title.
- `type` classifies the document role and must use a namespaced value from
  the matching registry profile.
- `status` is the lifecycle state. New authored documents start as `draft`
  unless a template has a fixed state such as archive Tombstones.
- `owner` is `platform` for repository-authored documents.
- `updated` uses an ISO calendar date.
- Do not quote scalar `owner` values when the value is the canonical owner.
- Archive Tombstones add `original_path`, `archived_on`, `archive_reason`, and
  `replacement` because archive routing and replacement traceability are part
  of the tombstone identity, not body prose.
- `archive_reason` uses one of `superseded`, `duplicate`, `obsolete`,
  `migrated`, or `historical-baseline`.
- `replacement` is a repository path when a current owner exists, or `none`
  when there is no direct replacement.

## Legacy Cleanup Rules

- Use `owner: platform` in active authored frontmatter and task owner cells.
- Use `type: sdlc/policy` for operations policy documents.
- Replace old simple `type` values with the namespaced values in this schema.
- Remove keys that duplicate the same role as another key unless the target
  profile explicitly allows both.
- Do not add frontmatter to README files, ignored `_workspace/**` scratch,
  GitHub-native Markdown control files, or native machine-readable templates.
- Add role-appropriate `sdlc/*` frontmatter to example-local cloud snapshot
  documents under `examples/aws/docs/**` and `examples/azure/docs/**` when
  they are non-README Markdown files.

## Validation Contract

`scripts/validate-repo-quality-gates.sh` must ensure each routed Markdown path
has exactly one frontmatter profile. The gate rejects:

- Missing required keys.
- Unsupported keys for the profile.
- Unsupported `type`, `status`, or `owner` values.
- Unsupported `archive_reason` values on Archive Tombstones.
- Frontmatter on README files when not required.
- Frontmatter or authored-document treatment for ignored `_workspace/**`
  scratch files.
- Frontmatter on GitHub-native Markdown control files.
- Missing, extra, or unsupported frontmatter on routed example-local cloud
  snapshot documents.
- Markdown frontmatter in OpenAPI, GraphQL, or protobuf templates.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Document Profile Registry](./document-profiles.json)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Legacy Cleanup Rules](./legacy-cleanup-rules.md)
- [Migration Spec](../../03.specs/011-template-contract-governance-migration/spec.md)
