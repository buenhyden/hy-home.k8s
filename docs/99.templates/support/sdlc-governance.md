---
title: 'SDLC Template Governance'
type: governance/template-support
status: active
owner: platform
updated: 2026-07-15
---

# SDLC Template Governance

## Overview

This document defines the template governance contract for SDLC documents. SDLC
templates are lifecycle forms used to move from requirements to architecture,
specification, execution, operations, incident learning, and verification
evidence.

## Purpose

The SDLC template family ensures that each active stage document has one role,
one registry-selected form, one lifecycle evidence contract, and one validation
route.

## Owned Contract

### SDLC Profile Handoff

The closed v7 [Document Profile Registry](./document-profiles.json) is the sole
machine owner of SDLC routes, templates, headings, frontmatter, lifecycle
domains, and body traceability contracts. Authors select the exact profile
from the target path instead of consulting a copied profile list. This document
owns why the roles remain separate and how they hand work and evidence to one
another.

The research basis and local adoption decisions for those families are recorded
in the [Document Type Format and Evidence
Contract](../../90.references/research/2026-07-07-wer/document-type-format-and-evidence-contract.md).

Incident folders are created only for real incidents. The incident fact record
uses a filename that matches the incident folder, and the postmortem is always
`postmortem.md` in the same folder. Placeholder incident directories are not
part of the steady-state structure.

### Lifecycle Rationale and Evidence

The registry owns every exact lifecycle value and allowed transition surface.
Template forms may show a valid starting value, but support prose and
agent-facing rules must not define a second transition set. Promotion requires
the evidence declared by the matched profile and its owning Plan or Task;
retirement preserves lineage instead of rewriting historical evidence.

Accepted architecture decisions are append-only decision evidence. A changed
decision is represented by a successor ADR and an explicit replacement
relation. Completed execution evidence is likewise preserved; new work creates
a new Plan or Task. Archive Tombstones preserve traceability but never become
current operating guidance.

Production body enforcement applies to authored SDLC consumers only while they
are `draft` or `active`. Their registry-routed template profiles retain the same
body contract for source parity and form validation. `done` execution evidence
and `accepted` decisions are excluded from retroactive body enforcement so a
new contract cannot manufacture historical evidence; successors carry new
work and link back instead.

### Numbering, Handoff, and Active Surfaces

New feature PRDs and Specs share a three-digit feature identifier when they
represent the same lineage. Architecture collections retain four-digit
identifiers, execution records remain date-based, and incident records retain
their year plus incident identity. Historical mismatches stay in place and are
linked explicitly rather than being renumbered for cosmetic consistency.

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

The numbered stages express responsibility and navigation rather than a
one-way waterfall. Operations, incident response, and postmortem learning feed
new requirements, architecture decisions, Specs, or Tasks when evidence shows
that an upstream contract must change. Incident records retain real-time facts;
postmortems own retrospective analysis and prevention actions.

## Authoring Rules

### Governance Rules

- Every non-README SDLC Markdown document must match exactly one registry
  profile and use that profile's canonical form.
- The matched template headings define required section coverage unless the
  heading is explicitly optional in the template.
- Stage 03 specs, Stage 04 plans, and Stage 04 tasks are English-first.
- Operations docs can use Korean for human-facing guidance while AI-agent
  execution notes and tool or prompt contracts remain English-first.
- Machine-readable OpenAPI, GraphQL, and protobuf templates stay native to
  their format and do not use Markdown frontmatter.
- Incident records own factual chronology and response state. Postmortems own
  root-cause analysis, prevention, and documentation feedback loops.

## Validation Contract

### Validation Rules

- Required headings and body traceability checks come from the matched registry
  profile. Its canonical form and current consumers must agree with that
  contract.
- Enforced lifecycle tables must use the profile-owned identifier and linked
  profile families. Required links carry reciprocal evidence when the registry
  requests it; a reasoned `N/A —` exclusion is allowed only for profiles that
  opt into explicit exclusions.
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
