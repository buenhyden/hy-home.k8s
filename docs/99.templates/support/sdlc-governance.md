---
title: 'SDLC Template Governance'
type: template-support
status: draft
owner: platform
updated: 2026-07-03
---

# SDLC Template Governance

## Overview

This document defines the template governance contract for SDLC documents. SDLC
templates are lifecycle forms used to move from requirements to architecture,
specification, execution, operations, incident learning, and verification
evidence.

## Purpose

The SDLC template family ensures that each active stage document has one role,
one target path pattern, one template form, and one validation route.

## SDLC Template Family

| Lifecycle Role | Target Pattern | Template Path |
| --- | --- | --- |
| Product requirement | `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` | `../templates/sdlc/requirements/prd.template.md` |
| Architecture requirement | `docs/02.architecture/requirements/####-<system-or-domain>.md` | `../templates/sdlc/architecture/ard.template.md` |
| Architecture decision | `docs/02.architecture/decisions/####-<short-title>.md` | `../templates/sdlc/architecture/adr.template.md` |
| Technical specification | `docs/03.specs/<feature-id>/spec.md` | `../templates/sdlc/specs/spec.template.md` |
| API contract doc | `docs/03.specs/<feature-id>/api-spec.md` | `../templates/sdlc/specs/api-spec.template.md` |
| Agent design | `docs/03.specs/<feature-id>/agent-design.md` | `../templates/sdlc/specs/agent-design.template.md` |
| Data model | `docs/03.specs/<feature-id>/data-model.md` | `../templates/sdlc/specs/data-model.template.md` |
| Test design | `docs/03.specs/<feature-id>/tests.md` | `../templates/sdlc/specs/tests.template.md` |
| OpenAPI contract | `docs/03.specs/<feature-id>/contracts/openapi.yaml` | `../templates/sdlc/specs/openapi.template.yaml` |
| GraphQL contract | `docs/03.specs/<feature-id>/contracts/schema.graphql` | `../templates/sdlc/specs/schema.template.graphql` |
| Protobuf contract | `docs/03.specs/<feature-id>/contracts/service.proto` | `../templates/sdlc/specs/service.template.proto` |
| Execution plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `../templates/sdlc/execution/plan.template.md` |
| Execution task | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `../templates/sdlc/execution/task.template.md` |
| Harness task contract | `docs/04.execution/tasks/YYYY-MM-DD-<harness-task>.md` | `../templates/sdlc/specs/harness-task-contract.template.md` |
| Guide | `docs/05.operations/guides/####-<topic>.md` | `../templates/sdlc/operations/guide.template.md` |
| Operations policy | `docs/05.operations/policies/####-<policy-or-standard>.md` | `../templates/sdlc/operations/policy.template.md` |
| Runbook | `docs/05.operations/runbooks/####-<topic>.md` | `../templates/sdlc/operations/runbook.template.md` |
| Incident record | `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident>.md` | `../templates/sdlc/operations/incident.template.md` |
| Postmortem | `docs/05.operations/incidents/postmortems/YYYY/YYYY-MM-DD-<incident>.md` | `../templates/sdlc/operations/postmortem.template.md` |

## Governance Rules

- Every non-README SDLC Markdown document must match exactly one structural
  template mapping.
- The matched template headings define required section coverage unless the
  heading is explicitly optional in the template.
- Stage 03 specs, Stage 04 plans, and Stage 04 tasks are English-first.
- Operations docs can use Korean for human-facing guidance while AI-agent
  execution notes and tool or prompt contracts remain English-first.
- Machine-readable OpenAPI, GraphQL, and protobuf templates stay native to
  their format and do not use Markdown frontmatter.
- The operations policy template replaces legacy `operation.template.md`
  routing. Active contracts must use `policy.template.md` and `type: policy`
  until Phase 3 introduces namespaced type values.

## Validation Rules

- Required heading checks come from the matched template.
- Route checks must reject uncovered SDLC Markdown paths.
- Route checks must reject paths that match more than one template.
- Route-breaking changes must update Stage 00 routing docs, hook hints, and
  validator mappings in the same logical unit.

## Related Documents

- [Documentation Contract](./documentation-contract.md)
- [Template Routing](./template-routing.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
