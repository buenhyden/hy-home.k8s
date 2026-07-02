---
title: 'Template Routing Contract'
type: template-support
status: draft
owner: platform
updated: 2026-07-03
---

# Template Routing Contract

## Overview

This document defines the canonical route contract between authored document
target patterns and template forms. Phase 1 records both the current flat route
and the approved Phase 2 target route. Phase 2 updates files, validators, hooks,
and references.

## Purpose

Each authored document path must map to exactly one template. Route ambiguity
creates broken validation, duplicated contracts, and inconsistent authored
documents.

## Current Route Map

The current route map uses flat template files directly under
`docs/99.templates/`. This remains active until Phase 2.

| Target Pattern | Current Template |
| --- | --- |
| `README.md`, `**/README.md`, `.claude/README.md`, `.codex/README.md` | `readme.template.md` |
| `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `prd.template.md` |
| `docs/02.architecture/requirements/####-<system-or-domain>.md` | `ard.template.md` |
| `docs/02.architecture/decisions/####-<short-title>.md` | `adr.template.md` |
| `docs/03.specs/<feature-id>/spec.md` | `spec.template.md` |
| `docs/03.specs/<feature-id>/api-spec.md` | `api-spec.template.md` |
| `docs/03.specs/<feature-id>/agent-design.md` | `agent-design.template.md` |
| `docs/03.specs/<feature-id>/data-model.md` | `data-model.template.md` |
| `docs/03.specs/<feature-id>/tests.md` | `tests.template.md` |
| `docs/03.specs/<feature-id>/contracts/openapi.yaml` | `openapi.template.yaml` |
| `docs/03.specs/<feature-id>/contracts/schema.graphql` | `schema.template.graphql` |
| `docs/03.specs/<feature-id>/contracts/service.proto` | `service.template.proto` |
| `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `plan.template.md` |
| `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `task.template.md` |
| `docs/04.execution/tasks/YYYY-MM-DD-<harness-task>.md` | `harness-task-contract.template.md` |
| `docs/05.operations/guides/####-<topic>.md` | `guide.template.md` |
| `docs/05.operations/policies/####-<policy-or-standard>.md` | `policy.template.md` |
| `docs/05.operations/runbooks/####-<topic>.md` | `runbook.template.md` |
| `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md` | `incident.template.md` |
| `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md` | `postmortem.template.md` |
| `docs/90.references/<category>/<topic>.md` | `reference.template.md` |
| `docs/98.archive/**/*.md` | `archive-tombstone.template.md` |
| `docs/00.agent-governance/memory/<topic>.md` | `memory.template.md` |
| `docs/00.agent-governance/memory/progress.md` | `progress.template.md` |

## Target Route Families

Phase 2 moves template forms to these families:

| Family | Target Folder | Ownership |
| --- | --- | --- |
| Requirements | `templates/sdlc/requirements/` | Product requirements. |
| Architecture | `templates/sdlc/architecture/` | Architecture requirements and decisions. |
| Specs | `templates/sdlc/specs/` | Technical specs and helper contracts. |
| Execution | `templates/sdlc/execution/` | Plans and task evidence. |
| Operations | `templates/sdlc/operations/` | Guides, policies, runbooks, incidents, postmortems. |
| Common | `templates/common/` | README, reference, archive, memory, progress. |

## Enforcement Surfaces

Route-breaking changes must update these surfaces in the same logical phase:

- `docs/99.templates/README.md`
- This support document.
- `docs/00.agent-governance/rules/document-stage-routing.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/hooks/k8s-pre-edit.sh`
- `scripts/validate-repo-quality-gates.sh`
- Stage README links and authored document template references.

## Validation Commands

```bash
git diff --check
bash scripts/validate-repo-quality-gates.sh .
rg -n "docs/99\\.templates/[a-z0-9-]+\\.template\\.(md|yaml|graphql|proto)" docs scripts .codex AGENTS.md RTK.md
find docs/99.templates -maxdepth 5 -type f -print | sort
```

The flat-path search is expected to return active matches before Phase 2. After
Phase 2, active route references should point to `docs/99.templates/templates/**`.
Historical progress entries may require an explicit allow-list.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
