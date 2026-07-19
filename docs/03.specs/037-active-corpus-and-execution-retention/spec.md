---
title: 'Active Corpus and Execution Retention Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-07-19
---

# Active Corpus and Execution Retention Technical Specification (Spec)

## Overview

This Spec applies lifecycle-based accumulation limits to Stages 01-04, audits
the current Stage 05 authored corpus for semantic ownership conflicts, and moves
eligible completed Plans and Tasks from closed lineages into full-body archive
records. It preserves valid accepted architecture decisions and implemented
Specs until an explicit successor removes their current authority.

The reciprocal implementation Plan and Task record the completed ACER-001
through ACER-005 packages and this ACER-006
terminal staged-closure proposal. The proposal converts the reciprocal pair
from active execution control to terminal Stage 04 evidence while preserving
an owned `DEFER` until exact successor migration evidence exists. The closure
commit and clean-tree post-commit verification are pending and unclaimed.

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

The parent `a12aedf` activation input contains 54 Plans and 56 Tasks, or 110
records. The frozen design baseline contains 51 Plans and 53 Tasks (104
records); the six-record delta is the three later reciprocal pairs for Specs
034, 035, and 036. At activation, the staged Spec 037 pair raised the proposed
authored corpus to 55 Plans and 57 Tasks (112 records); those two documents were
separate active controls outside the pre-activation migration candidate set.
ACER-001 reconciled the 104+6 candidate set before eligibility. In the current
terminal state, the Spec, Plan, and Task are done; the reciprocal pair remains
as terminal owned `DEFER` evidence with no active execution authority until an
exact successor migration evidence change. Each candidate is joined
to its upstream Spec, program, current-owner status, reciprocal link set, and
closure evidence. The classifier produces eligible, retain, or DEFER; there is
no default eligible state.

Eligible records migrate by lineage rather than one repository-wide commit.
Current documents point to an archive index anchor or a program closure record,
not directly to an individual archive payload. The payload retains its
historical links in source context.

Active stages are bounded by semantic cardinality. Folder size is reported for
observability but never causes destruction.

The Stage 05 activation input contains 24 authored records: eight Guides,
seven Policies, and nine Runbooks. The audit compares each record with its
profile, canonical owner, related Spec, and current repository implementation.
There are zero real authored Incident records and zero real authored
Postmortem records; their templates and indexes are validated without creating
a fake event. The prior helper Tests inventory is only an input and must be
recomputed before it supports any PASS. Helper Tests remain feature-local
specification support and never become the Stage 04 execution tracker.

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
- Delta interface: the frozen 104-record Stage 04 baseline and six later
  records joined exactly to the parent 110-record activation input; at
  activation, the new Spec 037 pair was a separately retained execution
  control. It is now terminal owned `DEFER` evidence with reason
  `terminal-spec-037-lineage-awaiting-successor-migration-evidence` and refresh
  trigger `exact-successor-migration-evidence-change`, not active authority.
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
- Run staged lifecycle admission for the exact reciprocal Spec 037 Plan/Task
  activation before beginning ACER-001.

## Success Criteria & Verification Plan

- **VAL-ACER-001**: All 104 baseline Plan/Task records and the six later
  Plan/Task records reconciled to the parent 110-record activation input and
  received an explicit eligible, retain, or DEFER disposition; the Spec 037
  pair was the separate active control at that observation boundary. The
  terminal pair remains current only as owned `DEFER` evidence, has no active
  execution authority, and refreshes on exact successor migration evidence.
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

### Activation Evidence

The activation proposal starts from exact parent `a12aedf`. The required
Plan-only staged RED exits 1 with `LIFECYCLE-CREATE`, observing `Plan count 1,
Task count 0`. The complete proposal adds one active reciprocal Plan/Task pair,
updates the three indexes, and updates the three 14-column migration-ledger
records without changing the already-active registry relation. It records the
parent 54-Plan/56-Task activation inventory, the proposed 55-Plan/57-Task
corpus, and the 104+6 candidate census obligation; no row is claimed eligible
before ACER-001. Specs 038 and 040 remain unplanned, and Spec 039 retains
CI/FIFO ownership.

ACER-001 through ACER-005 completed their reviewed repository-static packages.
ACER-006 staged the terminal lifecycle and residue-control proposal with exact
`100` current Stage 04 rows, `49` Plans, `51` Tasks, `52` lineages in exact
`48/1/3` cardinality, `100` current `DEFER`, zero current `retain`, four partial
owned `DEFER`, `13` accepted-ADR guards, `29` done-Spec guards including this
Spec, and eight empty finding arrays. The immutable control-source facts remain
`retain` / `active-spec-037-control` / `platform` / `Spec037 closure`; only the
current terminal evidence role changes. Observed staged QA passed the 65-test
focused module, 19-case residue self-test, exact production counts, staged
lifecycle, strict 436-path registry, zero-violation Markdown, strict links,
`43/362/43` archive cutover, direct repository aggregate, changed-file
pre-commit, and cached diff check. Initial independent requirements and quality
reviews each required changes; their remediations were re-reviewed by
`/root/acer006_requirements_rereview` as `REQUIREMENTS COMPLIANT` and
`/root/acer006_quality_rereview` as `QUALITY APPROVED`, with no blocking
findings. Raw all-files pre-commit failed only at the Spec 039-owned strict
GitOps FIFO self-test (`os.mkfifo` `Errno 95`); the run with the already-proven
duplicate strict hook skipped passed. No FIFO or CI remediation is claimed.
The closure commit and clean-tree post-commit/postflight do not yet exist and
remain pending and unclaimed. Specs 038, 039, and 040 remain active, Spec 039
retains CI/FIFO ownership, and Spec 040 remains the final integrator.
Remote/live and CI/FIFO PASS results are unclaimed.

## Traceability

- **Predecessor**: [Spec 036](../036-archive-record-and-workspace-boundary/spec.md)
- **Final integrator**: [Spec 040](../040-contract-cutover-and-program-closure/spec.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Plan**: [Active Corpus and Execution Retention Implementation Plan](../../04.execution/plans/2026-07-18-active-corpus-and-execution-retention.md)
- **Task**: [Active Corpus and Execution Retention Task](../../04.execution/tasks/2026-07-18-active-corpus-and-execution-retention.md)

### Lifecycle Traceability

| PRD requirement | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-WDLEC-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md#functional-requirements) | VAL-ACER-001 | The census ledger covers the complete baseline execution set. |
| N/A — REQ-WDLEC-006 / VAL-ACER-002 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-002 | Per-lineage migration results verify archive and rollback data. |
| N/A — REQ-WDLEC-007 / VAL-ACER-003 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-003 | Current-owner and lineage cardinality fixtures pass. |
| N/A — REQ-WDLEC-007 / VAL-ACER-004 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-004 | Active-stage residue validation matches the reviewed ledger. |
| N/A — REQ-WDLEC-005 / VAL-ACER-005 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-005 | Negative migration fixtures protect valid terminal authority. |
| N/A — REQ-WDLEC-006 / VAL-ACER-006 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-006 | Dual-context link validators pass after every batch. |
| N/A — REQ-WDLEC-013 / VAL-ACER-007 shares the PRD-006 source linked in VAL-ACER-001 | VAL-ACER-007 | Operations/helper census and negative fixtures verify role and evidence boundaries. |
