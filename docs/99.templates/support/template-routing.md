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
| `docs/04.execution/tasks/YYYY-MM-DD-<harness-task>.md` | `templates/sdlc/specs/harness-task-contract.template.md` |
| `docs/05.operations/guides/####-<topic>.md` | `templates/sdlc/operations/guide.template.md` |
| `docs/05.operations/policies/####-<policy-or-standard>.md` | `templates/sdlc/operations/policy.template.md` |
| `docs/05.operations/runbooks/####-<topic>.md` | `templates/sdlc/operations/runbook.template.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` | `templates/sdlc/operations/incident.template.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` | `templates/sdlc/operations/postmortem.template.md` |
| `docs/90.references/<category>/<topic>.md` | `templates/common/reference.template.md` |
| `docs/98.archive/**/*.md` | `templates/common/archive-tombstone.template.md` |
| `docs/00.agent-governance/memory/<topic>.md` | `templates/common/memory.template.md` |
| `docs/00.agent-governance/memory/progress.md` | `templates/common/progress.template.md` |

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

The flat-path search should not return active route references after Phase 2.
Historical progress entries may require an explicit allow-list.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [SDLC Governance](./sdlc-governance.md)
- [Common Documentation Governance](./common-documentation-governance.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Repository Quality Gate](../../../scripts/validate-repo-quality-gates.sh)
