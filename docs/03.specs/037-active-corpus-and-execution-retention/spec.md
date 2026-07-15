---
title: 'Active Corpus and Execution Retention Technical Specification'
type: sdlc/spec
status: active
owner: platform
updated: 2026-07-15
---

# Active Corpus and Execution Retention Technical Specification (Spec)

## Overview

This Spec applies lifecycle-based accumulation limits to Stages 01-04, audits
the current Stage 05 authored corpus for semantic ownership conflicts, and moves
eligible completed Plans and Tasks from closed lineages into full-body archive
records. It preserves valid accepted architecture decisions and implemented
Specs until an explicit successor removes their current authority.

## Strategic Boundaries & Non-goals

- **In scope**: Stage 01-05 current-owner census; Plan/Task lineage census;
  current Guide, Policy, Runbook, Incident, Postmortem, and helper Tests role
  conformance; migration ledger; eligible execution movement; archive indexes;
  current closure links; duplicate/stale semantic cleanup; and rollback
  evidence.
- **Non-goals**: Archiving solely by age or folder count, moving accepted ADRs,
  moving done Specs solely because they are done, renumbering, or fabricating
  lineage, incidents, postmortems, or live operations evidence.

## Contracts

- A normalized scope has at most one current PRD, ARD, and Spec owner.
- An active Spec lineage has at most one current Plan and one current Task.
- A closed lineage cannot retain done Plan or Task files in the active
  execution stage after an eligible migration.
- Terminal status alone does not remove a still-current Spec or accepted
  architecture owner.
- Every movement is atomic with archive creation, current index updates,
  cross-link repair, and migration-ledger evidence.
- Ineligible documents remain in place with DEFER reason and follow-up owner.
- Current operations documents have one role-specific owner, contain no copied
  template prompts or policy/procedure duplication, and retain real operational
  facts rather than synthetic completeness.

## Core Design

The migration begins with all 51 Plans and 53 Tasks. Each record is joined to
its upstream Spec, program, current-owner status, reciprocal link set, and
closure evidence. The classifier produces eligible, retain, or DEFER; there is
no default eligible state.

Eligible records migrate by lineage rather than one repository-wide commit.
Current documents point to an archive index anchor or a program closure record,
not directly to an individual archive payload. The payload retains its
historical links in source context.

Active stages are bounded by semantic cardinality. Folder size is reported for
observability but never causes destruction.

The Stage 05 audit compares each current Guide, Policy, and Runbook with its
profile, canonical owner, related Spec, and current repository implementation.
Incident and Postmortem collections may legitimately contain no authored event
record; their templates and indexes are validated without creating a fake
incident. Helper Tests remain feature-local specification support and never
become the Stage 04 execution tracker.

## Data Modeling & Storage Strategy

The migration ledger records original path, archive path, original type,
status, upstream Spec, program, closure evidence, current consumers, source
commit/blob, digest, disposition, reason, replacement/index anchor, validation
result, and rollback commit.

The current-corpus audit ledger also records operations/helper profile, topic
owner, implementation evidence, semantic conflict, disposition, and exception
owner when no migration is required.

A dry-run ledger is temporary scratch. The reviewed final ledger becomes
durable execution evidence and is preserved with the program closure.

## Interfaces & Data Structures

- Census interface: tracked Stage 01-05 and helper Tests files plus registry
  profiles, semantic owners, implementation evidence, and links.
- Eligibility interface: explicit predicates for lineage closure, authority,
  link migration, source recovery, and rollback.
- Migration interface: one lineage batch produces archive files, index rows,
  updated current links, and a result row.
- Residue interface: closed-lineage done Plan/Task paths remaining in active
  execution fail unless a DEFER row exists.

## Edge Cases & Error Handling

- Multiple plausible upstream Specs produce DEFER.
- A done Plan or Task still consumed as current procedure is retained until
  that authority is routed correctly.
- A current Spec may remain done when it still describes implemented behavior.
- Accepted ADRs remain in the decision log; previously archived ADRs remain one
  historical archive record and are not duplicated.
- A broken reciprocal link blocks the affected lineage batch.
- An empty Incident or Postmortem collection is not a gap when no real event
  exists; fabricated event records are forbidden.

## Failure Modes & Fallback / Human Escalation

- If closure evidence is absent, retain the file and open a bounded follow-up
  rather than inferring completion.
- If a batch fails after file movement, revert the entire lineage commit.
- If current-owner rules conflict with historical evidence, preserve history
  and create a successor current owner.

## Verification Commands

- Run the Stage 01-05 ownership, lineage, operations-role, and helper Tests
  census.
- Run migration in dry-run and check modes.
- Validate each lineage batch before and after movement.
- Run archive integrity, current links, indexes, strict profiles, repository
  quality, and all-files pre-commit.

## Success Criteria & Verification Plan

- **VAL-ACER-001**: All 104 baseline Plan/Task records receive an explicit
  eligible, retain, or DEFER disposition.
- **VAL-ACER-002**: Every eligible closed-lineage record moves with verified
  payload provenance and rollback metadata.
- **VAL-ACER-003**: Duplicate current owners and excess active Plan/Task owners
  are zero.
- **VAL-ACER-004**: Closed-lineage done Plan/Task residue is zero except
  explicitly owned DEFER rows.
- **VAL-ACER-005**: Accepted ADRs and still-current done Specs are not moved by
  terminal status alone.
- **VAL-ACER-006**: Current and historical link validation both report zero
  unresolved links in their respective contexts.
- **VAL-ACER-007**: Current Stage 05 and helper Tests documents have zero
  unsupported role overlap, copied template residue, stale current claims, or
  unowned exceptions.

## Traceability

- **Predecessor**: [Spec 036](../036-archive-record-and-workspace-boundary/spec.md)
- **Final integrator**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-001 | The census ledger covers the complete baseline execution set. |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-002 | Per-lineage migration results verify archive and rollback data. |
| [REQ-WDLEC-007](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-003 | Current-owner and lineage cardinality fixtures pass. |
| [REQ-WDLEC-007](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-004 | Active-stage residue validation matches the reviewed ledger. |
| [REQ-WDLEC-005](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-005 | Negative migration fixtures protect valid terminal authority. |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-006 | Dual-context link validators pass after every batch. |
| [REQ-WDLEC-013](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-007 | Operations/helper census and negative fixtures verify role and evidence boundaries. |
