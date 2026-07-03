---
title: 'Template Routing Contract'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-03
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

## Route Families

| Family | Target Folder | Ownership |
| --- | --- | --- |
| Requirements | `templates/sdlc/requirements/` | Product requirements. |
| Architecture | `templates/sdlc/architecture/` | Architecture requirements and decisions. |
| Specs | `templates/sdlc/specs/` | Technical specs and helper contracts. |
| Execution | `templates/sdlc/execution/` | Plans and task evidence. |
| Operations | `templates/sdlc/operations/` | Guides, policies, runbooks, incidents, postmortems. |
| Common | `templates/common/` | README, reference, archive, memory, progress. |

## Current Route Map

| Target Pattern | Template Path |
| --- | --- |
| `README.md`, `**/README.md`, `.claude/README.md`, `.codex/README.md` | `templates/common/readme.template.md` |
| `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `templates/sdlc/requirements/prd.template.md` |
| `docs/02.architecture/requirements/####-<system-or-domain>.md` | `templates/sdlc/architecture/ard.template.md` |
| `docs/02.architecture/decisions/####-<short-title>.md` | `templates/sdlc/architecture/adr.template.md` |
| `docs/03.specs/<feature-id>/spec.md` | `templates/sdlc/specs/spec.template.md` |
| `docs/03.specs/<feature-id>/api-spec.md` | `templates/sdlc/specs/api-spec.template.md` |
| `docs/03.specs/<feature-id>/agent-design.md` | `templates/sdlc/specs/agent-design.template.md` |
| `docs/03.specs/<feature-id>/data-model.md` | `templates/sdlc/specs/data-model.template.md` |
| `docs/03.specs/<feature-id>/tests.md` | `templates/sdlc/specs/tests.template.md` |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml` | `templates/sdlc/specs/openapi.template.yaml` |
| `docs/03.specs/<feature-id>/contracts/schema.graphql` | `templates/sdlc/specs/schema.template.graphql` |
| `docs/03.specs/<feature-id>/contracts/service.proto` | `templates/sdlc/specs/service.template.proto` |
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

Feature-local indexes such as `docs/03.specs/<feature-id>/README.md` use the
generic README route. Do not add a second structural README route for a nested
README target.

The memory `<topic>` placeholder excludes `progress`; `progress.md` is an
exact reserved route owned by `templates/common/progress.template.md`.

## Explicit Non-routed Markdown Exceptions

The following Markdown files are active repository control surfaces but are not
authored stage documents and are not copied from a structural template:

| Target | Contract |
| --- | --- |
| `.github/ABOUT.md` | GitHub configuration hub; frontmatter-free; routes policy detail to Stage 00, Stage 05, scripts, and workflow owners. |
| `.github/PULL_REQUEST_TEMPLATE.md` | GitHub PR body template; frontmatter-free; checklist mirrors canonical governance and CI/QA owners. |
| `.github/SECURITY.md` | GitHub security policy surface; frontmatter-free; vulnerability reporting body must remain GitHub-renderable. |

Validators may check these files for frontmatter bans and stale currentness
claims, but they must not require stage frontmatter or required template
headings.

## Supplemental Task Starter

`harness-task-contract.template.md` supplements
`templates/sdlc/execution/task.template.md` for high-risk harness tasks. It
does not create a second structural route for `docs/04.execution/tasks/*.md`;
the authored Task record still uses `type: sdlc/task` and the Stage 04 Task
location.

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
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
