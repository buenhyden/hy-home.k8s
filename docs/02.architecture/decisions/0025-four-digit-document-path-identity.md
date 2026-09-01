---
title: 'Four-Digit Document Path Identity'
version: "1.0"
type: sdlc/adr
layer: "02.architecture"
status: superseded
owner: platform
updated: 2026-08-13
artifact_id: "ADR-0025"
superseded_by: ADR-0030
---

# ADR-0025: Four-Digit Document Path Identity

## Overview

This accepted decision standardizes every numeric identity token in current
`docs/` authored routes on four zero-padded digits. It also fixes the Incident
directory grammar at
`docs/05.operations/incidents/<year>/inc-<dddd>-<slug>/`. It partially
supersedes only the three-digit PRD/Spec/work-unit and Incident clauses of
[ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md); every
archive, provenance, recovery, authority, and script-disposition decision in
ADR-0024 remains accepted.

## Context

The terminal contract already uses four digits for AD, ADR, Guide, Policy,
Runbook, Stage 98 change, and stable migration identities, but retained three
digits for PRD and Stage 03 work units and for the Incident number. Mixed widths
make path parsing, artifact-ID comparison, sorting, and future capacity depend
on the document family rather than one repository rule. The human-approved
direction is that numeric document identities under `docs/` use four digits by
default and Incident directories use one exact lowercase route.

WORK-109 is the first tranche allowed to activate terminal document routes.
The cutover must therefore migrate current path and frontmatter identities
atomically, repair current consumers, preserve immutable Stage 90/98 bytes,
and limit Stage 05 edits to exact old-to-new current-link normalization. A validator may resolve a protected
historical link through an exact reviewed alias, but may not retain a second
live three-digit route.

## Decision

The terminal numeric token is `<dddd>`, exactly four zero-padded ASCII decimal
digits. Current authored routes and their path-derived IDs use these forms:

| Family | Canonical route | `artifact_id` |
| --- | --- | --- |
| PRD | `docs/01.requirements/<dddd>-<slug>.md` | `PRD-<DDDD>` |
| SRS | `docs/01.requirements/srs-<dddd>-<slug>.md` | `SRS-<DDDD>` |
| Interface Requirement | `docs/01.requirements/ifc-<dddd>-<slug>.md` | `IFC-<DDDD>` |
| AD | `docs/02.architecture/descriptions/ad-<dddd>-<slug>.md` | `AD-<DDDD>` |
| ADR | `docs/02.architecture/decisions/<dddd>-<slug>.md` | `ADR-<DDDD>` |
| Stage 03 work unit | `docs/03.specs/<dddd>-<slug>/` | shared `<DDDD>` |
| Spec | `docs/03.specs/<dddd>-<slug>/spec.md` | `SPEC-<DDDD>` |
| Plan | `docs/03.specs/<dddd>-<slug>/plan.md` | `PLAN-<DDDD>` |
| Task | `docs/03.specs/<dddd>-<slug>/tasks.md` | `TASK-<DDDD>` |
| Incident directory | `docs/05.operations/incidents/<year>/inc-<dddd>-<slug>/` | shared year and `<DDDD>` |
| Incident | `docs/05.operations/incidents/<year>/inc-<dddd>-<slug>/incident.md` | `INC-<YYYY>-<DDDD>` |
| Postmortem | `docs/05.operations/incidents/<year>/inc-<dddd>-<slug>/postmortem.md` | `POSTMORTEM-<YYYY>-<DDDD>` |

Agent Design, Data Model, Tests, and any other path-derived child of a Stage 03
work unit inherit the same four-digit directory token. Guide, Policy, and
Runbook routes retain their already-four-digit grammar.

README files, templates, the three consolidated authority documents,
feature-local `spec.md`/`plan.md`/`tasks.md` basenames, native schema files,
approved Stage 90 dated observations, and stable Stage 98 records are closed
non-numbered or separately governed exceptions. They do not authorize a
three-digit current route. Historical path strings inside immutable Stage 90
or Stage 98 bytes remain evidence and are resolved only by exact reviewed
aliases.

WORK-109 migrates the existing eight PRD paths and every current Stage 03 work
unit from three to four digits, updates their path-derived artifact IDs, and
repairs all mutable consumers in the same logical cutover. The transition
registry remains globally `transition` until WORK-114 removes the reviewed
migration assets, but no live three-digit PRD, Stage 03, or Incident route may
remain after WORK-109.

## Explicit Non-goals

- Do not change Stage 90 or Stage 98 bytes or stable archive identities.
- Do not renumber AD, ADR, Guide, Policy, or Runbook records; they already use
  four digits.
- Do not create an Incident record merely to exercise the route.
- Do not remove the transition manifest, migration tool, or their external test
  before WORK-114.
- Do not alter Stage 05 operational meaning or topology. Exact current-link
  normalization required by the four-digit cutover is allowed; historical
  links remain unchanged and require reviewed alias resolution.

## Consequences

- All current numeric path identities share one width and sort consistently.
- Path-derived artifact IDs remain deterministic and globally unique.
- Existing PRD and Stage 03 paths require a reviewed atomic rename and consumer
  rewrite; partial application must fail closed.
- Protected historical surfaces need exact old-to-new resolution without byte
  mutation.
- Incident authoring gains one lowercase directory and two fixed sibling
  basenames, eliminating case and repeated-slug ambiguity.

## Alternatives

- Keep mixed three- and four-digit families: rejected because family-specific
  width remains embedded in every router and validator.
- Apply four digits only to new documents: rejected because two live path
  grammars would remain indefinitely and path-ID equality would depend on age.
- Rename protected archive/history records too: rejected because it would
  violate accepted payload, provenance, and recovery invariants.

## Traceability

This decision is implemented by the active document-taxonomy program and is
machine-enforced by the document registry, lifecycle, Markdown, link, and
artifact-identity validators.

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0024](./0024-terminal-artifact-identity-and-archive-layout.md) | Partially supersedes only three-digit PRD/Stage 03/Incident path and ID grammar | [Spec 0052](../../03.specs/0052-document-taxonomy-consolidation/spec.md) is the predecessor program; [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) is the active successor. |
