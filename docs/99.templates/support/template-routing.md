---
title: 'Template Routing Contract'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-06
---

# Template Routing Contract

## Overview

This document defines the canonical route contract between authored document
target patterns and template forms. Template forms now live under
`docs/99.templates/templates/**`; support contracts live under
`docs/99.templates/support/**`.

## Purpose

Each authored document path must map to exactly one template. Route ambiguity
creates broken validation, duplicated contracts, and inconsistent authored
documents.

The machine-readable [Document Profile Registry](./document-profiles.json)
owns every exact or anchored-regex route and its profile, heading, and template
facts. This support document owns the route-selection procedure, rationale,
boundaries, and examples. Its one temporary route-map mirror is explicitly
non-authoritative and exists only for the current compatibility consumer.

## Route-selection Procedure

1. Normalize the repository-relative POSIX target path without traversing
   ignored paths or symlinked provider views.
2. Load the [Document Profile Registry](./document-profiles.json) and evaluate
   every exact or anchored-regex route.
3. Require exactly one matching profile; declaration order is never precedence.
4. Use that profile's template and document contract, and use this support
   document only for routing rationale and migration boundaries.

## Lifecycle Route Summary

The registry owns the exact path patterns. The lifecycle rationale remains:
requirements and specifications carry numbered lineage, plans and tasks remain
dated execution evidence, example-local cloud snapshots reuse SDLC roles
without becoming active-stage owners, and README files remain navigation
surfaces rather than governance bodies.

Exact lifecycle domains remain registry facts. Numeric lineage rationale,
handoff links, and the active-surface duplicate rule are owned by [SDLC
Governance](./sdlc-governance.md). This document owns the selection procedure
and the temporary compatibility mirror below, not the route facts themselves.

## Current Route Map

The [Document Profile Registry](./document-profiles.json) is the sole machine
owner. The following non-authoritative compatibility mirror remains only while
the existing Stage 99 README and embedded quality-gate comparison stay active
through Spec 030. The quality gate verifies this mirror against the migration
contract; maintainers must not expand or hand-edit it beyond that consumer's
requirements:

| Target Pattern | Template Path |
| --- | --- |
| `README.md`, `**/README.md`, `.claude/README.md`, `.codex/README.md` | `templates/common/readme.template.md` |
| `docs/01.requirements/<###-Numbering>-<feature-or-system>.md` | `templates/sdlc/requirements/prd.template.md` |
| `docs/02.architecture/requirements/####-<system-or-domain>.md` | `templates/sdlc/architecture/ard.template.md` |
| `docs/02.architecture/decisions/####-<short-title>.md` | `templates/sdlc/architecture/adr.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/spec.md` | `templates/sdlc/specs/spec.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md` | `templates/sdlc/specs/api-spec.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md` | `templates/sdlc/specs/agent-design.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/data-model.md` | `templates/sdlc/specs/data-model.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/tests.md` | `templates/sdlc/specs/tests.template.md` |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml` | `templates/sdlc/specs/openapi.template.yaml` |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql` | `templates/sdlc/specs/schema.template.graphql` |
| `docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto` | `templates/sdlc/specs/service.template.proto` |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `templates/sdlc/execution/plan.template.md` |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `templates/sdlc/execution/task.template.md` |
| `docs/05.operations/guides/####-<topic>.md` | `templates/sdlc/operations/guide.template.md` |
| `docs/05.operations/policies/####-<policy-or-standard>.md` | `templates/sdlc/operations/policy.template.md` |
| `docs/05.operations/runbooks/####-<topic>.md` | `templates/sdlc/operations/runbook.template.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` | `templates/sdlc/operations/incident.template.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` | `templates/sdlc/operations/postmortem.template.md` |
| `docs/90.references/<category>/<topic>.md` | `templates/common/reference.template.md` |
| `docs/98.archive/**/*.md` | `templates/common/archive-tombstone.template.md` |
| `docs/00.agent-governance/memory/<topic>.md` | `templates/common/memory.template.md` |
| `docs/00.agent-governance/memory/progress.md` | `templates/common/progress.template.md` |

Feature-local indexes such as `docs/03.specs/<###-Numbering>-<feature-id>/README.md` use the
generic README route. Do not add a second structural README route for a nested
README target.

The memory `<topic>` placeholder excludes `progress`; `progress.md` is an
exact reserved route owned by `templates/common/progress.template.md`.

## Explicit Non-routed Markdown Exceptions

The registry identifies the exact GitHub-native control paths as exception
profiles. They remain active repository control surfaces rather than authored
stage documents: the configuration hub routes policy detail to canonical
owners, the pull-request template mirrors intake and CI/QA owners, and the
security policy remains GitHub-renderable.

Validators may check these files for frontmatter bans and stale currentness
claims, but they must not require stage frontmatter or required template
headings.

## Example-Local SDLC Snapshot Boundary

AWS and Azure cloud example docs under `examples/aws/docs/**` and
`examples/azure/docs/**` are dated Cloud Example Snapshot material and
example-local SDLC snapshot documents. They are not provider-latest guidance
and they do not move into the main active `docs/01` through `docs/05` stage
tree. Non-README Markdown in those trees uses the matching SDLC frontmatter
role and should align section names with the closest SDLC template without
retaining template instructions or placeholders.

The registry owns the exact example-local path mappings and provider coverage.
Conceptually, non-README example documents resolve by their SDLC role, while
example README files remain frontmatter-free navigation. That distinction lets
examples reuse structure without claiming current provider authority.

## Enforcement Surfaces

Route-breaking changes must update these surfaces in the same logical unit:

- `docs/99.templates/README.md`
- This support document.
- `docs/00.agent-governance/rules/document-stage-routing.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
- `scripts/validate-repo-quality-gates.sh`
- Stage README links and authored document template references.
- Example-local cloud snapshot README indexes and cross-links when
  `examples/aws/docs/**` or `examples/azure/docs/**` files are normalized,
  renamed, consolidated, or archived.
- GitHub-native Markdown control-surface exceptions when `.github` control
  documents are added, removed, or repurposed.

## Validation Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
find docs/99.templates -maxdepth 5 -type f -print | sort
```

The flat-path search must not return active route references in current
contracts.
Historical progress entries may require an explicit allow-list.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
