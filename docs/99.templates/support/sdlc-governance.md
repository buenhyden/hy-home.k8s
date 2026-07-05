---
title: 'SDLC Template Governance'
type: governance/template-support
status: draft
owner: platform
updated: 2026-07-06
---

# SDLC Template Governance

## Overview

This document defines the template governance contract for SDLC documents. SDLC
templates are lifecycle forms used to move from requirements to architecture,
specification, execution, operations, incident learning, and verification
evidence.

## Purpose

The SDLC template family ensures that each active stage document has one role,
one target path pattern, one template form, one lifecycle state contract, and
one validation route.

## SDLC Template Family

| Lifecycle Role | Target Pattern | Template Path |
| --- | --- | --- |
| Product requirement | `docs/01.requirements/<###-Numbering>-<feature-or-system>.md` | `../templates/sdlc/requirements/prd.template.md` |
| Architecture requirement | `docs/02.architecture/requirements/####-<system-or-domain>.md` | `../templates/sdlc/architecture/ard.template.md` |
| Architecture decision | `docs/02.architecture/decisions/####-<short-title>.md` | `../templates/sdlc/architecture/adr.template.md` |
| Technical specification | `docs/03.specs/<###-Numbering>-<feature-id>/spec.md` | `../templates/sdlc/specs/spec.template.md` |
| API contract doc | `docs/03.specs/<###-Numbering>-<feature-id>/api-spec.md` | `../templates/sdlc/specs/api-spec.template.md` |
| Agent design | `docs/03.specs/<###-Numbering>-<feature-id>/agent-design.md` | `../templates/sdlc/specs/agent-design.template.md` |
| Data model | `docs/03.specs/<###-Numbering>-<feature-id>/data-model.md` | `../templates/sdlc/specs/data-model.template.md` |
| Test design | `docs/03.specs/<###-Numbering>-<feature-id>/tests.md` | `../templates/sdlc/specs/tests.template.md` |
| OpenAPI contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/openapi.yaml` | `../templates/sdlc/specs/openapi.template.yaml` |
| GraphQL contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/schema.graphql` | `../templates/sdlc/specs/schema.template.graphql` |
| Protobuf contract | `docs/03.specs/<###-Numbering>-<feature-id>/contracts/service.proto` | `../templates/sdlc/specs/service.template.proto` |
| Execution plan | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` | `../templates/sdlc/execution/plan.template.md` |
| Execution task | `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md` | `../templates/sdlc/execution/task.template.md` |
| Guide | `docs/05.operations/guides/####-<topic>.md` | `../templates/sdlc/operations/guide.template.md` |
| Operations policy | `docs/05.operations/policies/####-<policy-or-standard>.md` | `../templates/sdlc/operations/policy.template.md` |
| Runbook | `docs/05.operations/runbooks/####-<topic>.md` | `../templates/sdlc/operations/runbook.template.md` |
| Incident record | `docs/05.operations/incidents/YYYY/INC-###-<title>/INC-###-<title>.md` | `../templates/sdlc/operations/incident.template.md` |
| Postmortem | `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` | `../templates/sdlc/operations/postmortem.template.md` |

Incident folders are created only for real incidents. The incident fact record
uses a filename that matches the incident folder, and the postmortem is always
`postmortem.md` in the same folder. Placeholder incident directories are not
part of the steady-state structure.

## Lifecycle State Contract

This support contract owns the shared SDLC lifecycle state language. Template
forms may show the starting state, and agent-facing routing rules may summarize
the table, but they must not invent separate lifecycle transitions.

| Document Family | Lifecycle Transition |
| --- | --- |
| PRD | `draft -> active -> done | archived` |
| ARD/ADR | `draft -> active -> accepted | archived` |
| Spec | `draft -> active -> done | archived` |
| Plan/Task | `draft -> active -> done | archived` |
| Operations | `draft -> active -> accepted | archived` |
| Archive Tombstone | `archived` only |

PRDs are product commitments and finish as `done` when their scope is satisfied
or as `archived` when superseded. ARDs and ADRs become `accepted` when the
architecture requirement or decision is approved. Specs, plans, and tasks use
`done` for completed delivery evidence. Guides, policies, runbooks, incident
records, and postmortems become `accepted` when they are durable operations
contracts. Archive Tombstones are not reactivated; they remain `archived`
metadata records and preserve traceability through archive fields such as
`original_path`.

## Numbering, Handoff, and Active Surfaces

Stage 01 PRDs use `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
Stage 03 specs use `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`. When creating new work,
the PRD and Spec numeric identifiers should match for the same feature lineage.
Historical mismatches are kept in place and linked explicitly in Related
Documents instead of being renumbered only for cosmetic consistency. Stage 04
plans and tasks stay date-based execution records.

Lifecycle handoff links must make lineage explicit: PRDs link to architecture
and specs, architecture documents link upstream PRDs and downstream specs,
specs link upstream inputs and downstream plan/task evidence, plans link the
spec they execute and expected task evidence, tasks link the parent plan/spec
and validation evidence, operations documents link the promoted spec, task,
incident, or policy owner, and archive tombstones link the original and
replacement or current location.

Active-surface duplicate rule: stages 01 through 04 must not keep multiple
active documents that own the same role, purpose, and feature lineage. Retire
superseded, duplicate, obsolete, migrated, or currentness-conflicting surfaces
to archive or rewrite them as historical evidence.

## Supplemental Task Starter

`harness-task-contract.template.md` supplements
`templates/sdlc/execution/task.template.md` for high-risk harness tasks. It
does not create a second structural route for `docs/04.execution/tasks/*.md`;
the authored Task record still uses `type: sdlc/task` and the Stage 04 Task
location.

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
- The operations policy template owns policy routing. Active contracts must
  use `policy.template.md` and `type: sdlc/policy`.
- Incident records own factual chronology and response state. Postmortems own
  root-cause analysis, prevention, and documentation feedback loops.

## Validation Rules

- Required heading checks come from the matched template.
- Required heading extraction uses literal `##` headings from the template,
  excluding headings that contain placeholders and headings marked optional or
  if-applicable.
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
