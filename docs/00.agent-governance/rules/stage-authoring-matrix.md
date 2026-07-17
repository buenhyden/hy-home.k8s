---
title: 'Stage Authoring Matrix'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Stage Authoring Matrix

## Overview

Canonical authoring matrix for the current docs taxonomy.

All authored stage documents must use the matching template from
`docs/99.templates/support/template-routing.md` before writing. New authored
documents start with `status: draft`, keep the required template headings, and
include the relationship section selected by the document profile registry.
README entrypoints use the selected profile's form and heading contract.
This matrix summarizes stage responsibility and timing; exact target patterns
and template paths remain owned by the template routing support contract and
the Templates README.

Human-facing README and overview prose should prefer Korean. Agent governance,
provider adapters, hook contracts, prompt/tool contracts, technical specs,
execution plans, task evidence, and explicit AI-agent-facing sections such as
`AI Agent Requirements` should prefer English. `docs/03.specs/**/spec.md`,
`docs/04.execution/plans/*.md`, and `docs/04.execution/tasks/*.md` are
English-first execution artifacts. When a stage document mixes human and agent
audiences, keep the reader-facing context in Korean and keep the AI-agent
execution requirements in English.

## Authority Boundary

This matrix owns stage purpose, timing, primary persona, and completion intent.
It does not own exact path patterns, frontmatter keys, required headings, or
status enums; those are selected by the Stage 99 registry, routing, schema, and
lifecycle contracts. Route ownership changes through those contracts first,
then update this summary.

## Governance Context

Bootstrap and persona routing use this matrix to choose the authoritative
stage before authoring. Stage READMEs index current documents, while Stage 99
support files own reusable document form. This file links those systems without
copying their complete schemas or templates.

## Current Contract

### Lifecycle Pre-Edit Contract

Agents must check these lifecycle rules before editing authored documents:

Resolve the exact lifecycle domain from the [Document Profile
Registry](../../99.templates/support/document-profiles.json), validate metadata
against the [Frontmatter Schema](../../99.templates/support/frontmatter-schema.md),
apply promotion and preservation semantics from [SDLC
Governance](../../99.templates/support/sdlc-governance.md), and select the
canonical form through [Template
Routing](../../99.templates/support/template-routing.md). This Stage 00 matrix
does not publish a second transition set.

- Stage 01 PRDs use `docs/01.requirements/<###-Numbering>-<feature-or-system>.md`.
- Stage 03 specs use `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
- Stage 04 plans and tasks stay date-based execution records.
- README files route readers to lifecycle contract owners instead of carrying
  full governance bodies.
- Handoff links must connect PRD, architecture, spec, plan, task, operations,
  and archive records through the relationship section selected by each
  route-owned profile.
- Active-surface duplicate rule: stages 01 through 04 must not keep multiple
  active documents that own the same role, purpose, and feature lineage.

| Taxonomy Path | Purpose | Authoring Timing | Persona (Primary) | Input Documents | Output Documents | Template | Completion Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `00.agent-governance` | Agent governance and execution control | Before work starts and when governance changes | Governance Steward | Repository structure, policy context | Rules/scopes/providers/memory entries | `memory.template.md`, `progress.template.md` | JIT loading, language boundary, progress ledger, and checklist consistency are enforced |
| `01.requirements` | Product intent and requirements | Before feature implementation | Product Manager | Problem statement, business goals | PRD | `prd.template.md` | Acceptance criteria, scope, and success metrics are testable |
| `02.architecture/requirements` | Architecture requirements and reference design | After PRD baseline | System Architect | PRD | ARD | `ard.template.md` | Boundaries, quality attributes, and data flow are explicit |
| `02.architecture/decisions` | Architecture decision records | When major decisions are made | System Architect | ARD, alternatives | ADR | `adr.template.md` | Decision rationale, alternatives, and consequences are traceable |
| `03.specs` | Detailed technical specification | Before implementation | Backend/Frontend/Security Engineer | PRD, ARD, ADR | Spec/API/Agent/Data/Test design docs | `spec.template.md`, `api-spec.template.md`, `agent-design.template.md`, `data-model.template.md`, `tests.template.md` | Contracts and verification-ready design are complete |
| `04.execution/plans` | Execution planning | Immediately after spec baseline | Product/QA/Tech Lead | PRD, Spec, ADR | Plan | `plan.template.md` | Phases, risks, gates, and rollback are defined |
| `04.execution/tasks` | Task execution tracking | During implementation and validation | Engineer/QA Engineer | Plan, Spec | Task records with evidence | [Canonical Task form](../../99.templates/templates/sdlc/execution/task.template.md#approval-and-safety-boundaries) | Status, protected-surface boundaries, validation, and evidence are continuously updated |
| `05.operations/guides` | User and operator guides | After feature stabilization | Technical Writer | Spec, operations context | Guides | `guide.template.md` | Target audience can follow and reproduce procedures |
| `05.operations/policies` | Operational policy | Before release and when policy changes | Operations Engineer | Spec, security/compliance requirements | Operation policy docs | `policy.template.md` | Control, retention, and promotion criteria are explicit |
| `05.operations/runbooks` | Executable run procedures | When operations tasks are standardized | Operations Engineer | Operation policy | Runbooks | `runbook.template.md` | Steps are executable with validation and recovery paths |
| `05.operations/incidents` | Incident fact records and post-incident learning | During incident handling and after incident closure | Operations/Security Engineer | Runtime evidence, runbooks | Incident folders with `YYYY/INC-###-<title>/INC-###-<title>.md` and optional `postmortem.md` | `incident.template.md`, `postmortem.template.md` | Timeline, impact, mitigations, RCA, and prevention actions are linked back to the system |
| `90.references` | Durable reference material | When knowledge should be reused across features or operations | Technical Writer/Governance Steward | Stable facts, inventories, learning material | Reference documents | `reference.template.md` | Reference material is factual, slow-moving, linked from relevant stages, and keeps authority/source/freshness fields English-first |
| `98.archive` | Metadata-only old document Tombstones | When an old active-stage document conflicts with current implementation or is deprecated-only/superseded-only | Governance Steward | Current replacement docs, implementation evidence | Tombstone documents and archive index rows | `archive-tombstone.template.md` | Archive traceability metadata and mirrored path are preserved, old body is removed, active docs link only to the archive index |
| `99.templates` | Reusable document templates | Before authoring or restructuring docs | Technical Writer/Governance Steward | Taxonomy requirements | Templates | n/a | Templates match canonical paths and stay referenced by README files |

## Validation and Refresh

Run the strict document registry, Markdown profile, and link/owner validators,
then `bash scripts/validate-repo-quality-gates.sh .`. Review this matrix when a
stage, persona, lifecycle family, template route, or completion criterion
changes. The Stage 99 contracts must be updated before this summary when the
change affects document shape.

## Related Documents

- [Document Stage Routing Rules](document-stage-routing.md)
- [Stage Checklists](stage-checklists.md)
- [Template Routing Contract](../../99.templates/support/template-routing.md)
- [SDLC Governance](../../99.templates/support/sdlc-governance.md)
