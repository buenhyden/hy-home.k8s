---
title: 'SDLC Template Governance'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-13
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

## Owned Contract

### SDLC Profile Handoff

The [Document Profile Registry](./document-profiles.json) is the sole machine
owner of SDLC routes, templates, headings, frontmatter, and lifecycle domains.
Use its `sdlc/prd`, `sdlc/ard`, `sdlc/adr`, `sdlc/spec`, helper-spec,
`sdlc/plan`, `sdlc/task`, and operations profiles for exact values. This
document owns why those roles remain separate and how they hand work and
evidence to one another.

The research basis and local adoption decisions for those families are recorded
in the [Document Type Format and Evidence
Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md).

Incident folders are created only for real incidents. The incident fact record
uses a filename that matches the incident folder, and the postmortem is always
`postmortem.md` in the same folder. Placeholder incident directories are not
part of the steady-state structure.

### Lifecycle Rationale and Deferred Normalization

The registry owns the exact status domains. Template forms may show a valid
starting state, but support prose and agent-facing routing rules must not define
or normalize a second transition set. TCC-003 verified the registry values
against the pre-consolidation canonical domains before removing the copied
table; this tranche does not rename, narrow, or expand a state.

PRDs are product commitments and finish as `done` when their scope is satisfied
or as `archived` when superseded. ARDs and ADRs become `accepted` when the
architecture requirement or decision is approved. Specs, plans, and tasks use
`done` for completed delivery evidence. Guides, policies, runbooks, incident
records, and postmortems become `accepted` when they are durable operations
contracts. Archive Tombstones are not reactivated; they remain `archived`
metadata records and preserve traceability through archive fields such as
`original_path`.

The [Current research decision
ledger](../../90.references/research/2026-07-07-wer/README.md#canonical-requirement-to-research-to-audit-ownership-map)
retains document-state transitions as a gap with the RMD-007 follow-up. Any
future lifecycle normalization remains **Deferred**. The `platform` owner must
first publish a dedicated migration decision and corpus transition evidence,
then refresh that ledger disposition. Spec 027 does not enact the proposal.

### Numbering, Handoff, and Active Surfaces

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

## Authoring Rules

### Governance Rules

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

## Validation Contract

### Validation Rules

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
- [Document Profile Registry](./document-profiles.json)
- [Document Type Format and Evidence Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md)
- [Template Routing](./template-routing.md)
- [Frontmatter Schema](./frontmatter-schema.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
