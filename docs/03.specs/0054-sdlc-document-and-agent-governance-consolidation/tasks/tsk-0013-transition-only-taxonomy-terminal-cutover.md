---
title: 'Task: Current corpus and transition-control cutover'
version: "1.0.0"
type: sdlc/task
layer: "specs"
status: in-progress
owner: platform
updated: 2026-09-03
artifact_id: "SPEC-0054-TSK-0013"
---

# Task: Current corpus and transition-control cutover

## Overview

This is the queued Task record for the remaining Stage 01, 02, 03, and 99
current-corpus convergence and transition-control retirement in WP-013. Named
dispositions are execution candidates, not permanent corpus-count policy.

Re-observation on 2026-09-03 refreshed those candidates. Two entry steps now
precede the cutover: Spec 0052 closes, which releases the suspension recorded
against REQ-0007 and REQ-0008, and Spec Packages `0047` through `0051` each
receive a resume-or-remove disposition. The Stage 03 removal set is the fifty-two
packages that will be `done`. The fifty-one measured today partition into
twenty-five already consumer-zero, thirteen released by rewriting REQ-0003,
AD-0006, AD-0008, and AD-0009, and thirteen held by owners disposed of
individually, including four accepted ADRs whose citations convert rather than
disappear. Fourteen packages are retained on unfinished scope rather than on a
fixed list, two of them conditionally: `0062` holds three `blocked` Tasks, and
`0006` is an `active` Spec with no Plan and no Tasks.

## Inputs

- [Common execution contract](../plan.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-013 execution boundary](../plan.md#wp-013--current-corpus-and-transition-control-cutover)

## Task Table

**Plan label:** WP-013

**Depends on:** WP-006; WP-008; WP-012; accepted ADR-0031; accepted and completed Spec 0066
result with SPEC-0066-TSK-0001, Plan 0066, and Spec 0066 all `done`; completed
SPEC-0054-TSK-0011 parent handoff; and the existing Spec 0054 compatibility pointer,
which named this Task while it was still `queued`

**Current state:** `in-progress`; the entry blocker in the link validator is
released and no corpus removal has been made

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-013 | VAL-SDLC-001..VAL-SDLC-004, VAL-SDLC-006, VAL-SDLC-009..VAL-SDLC-012 | After the completed child and parent handoffs, reconcile retained Stage 01 Requirements and Stage 02 Architecture bidirectionally with the current implementation, converge the reviewed Stage 01/02/03/99 current-owner set, remove active Archive citations and cross-links, transfer unfinished work and unique authority, then retire residual transition assets against the accepted and completed Spec 0066 routing result without a fixed corpus census. | platform | In progress | Entry blocker released; no corpus removal made. | Terminal Spec 0066 states, completed SPEC-0054-TSK-0011, compatibility pointer to this queued Task, manifest/configuration/code/validator/operational-interface evidence mapped to retained Requirement Packages and Architecture Descriptions, zero inbound Archive links, consumer/trace/lifecycle parity, Git-first recovery, registry/template parity, delegated routing evidence, and ordered logical commits |

## Approval and Safety Boundaries

The [common execution contract](../plan.md#common-execution-contract) applies
without exception. WP-013 may remove a current document or template only after
its unique authority and unfinished work are transferred or proven absent,
current consumers are zero, and Git-first recovery succeeds. The linked Plan
owns the exact candidate dispositions, reviews, rollback, and four ordered
logical commits: Stage 01/02, Stage 03, Stage 99, then transition controls. The
accepted and completed Spec 0066 result plus the completed SPEC-0054-TSK-0011
parent handoff are fixed dependencies; their execution does not overlap the
final WP-013 validation-side transition-control unit. The existing Spec 0054 compatibility pointer named this
Task while it was still `queued`, which satisfied the activation condition.
Each unit is independently validated and can stop before the next unit without
rolling back an already accepted predecessor unit.

The Stage 01/02 unit is not a prose-only consolidation. It compares retained
Requirement Packages `0001` through `0004` and Architecture Descriptions
`0004` through `0007` with current manifests, configuration, executable code,
validators, and supported operational interfaces. Unique current facts move
from removal candidates before deletion. Durable implemented behavior without
an appropriate current Requirement/Architecture owner and retained current
claims without implementation evidence are both blocking findings; raw
inventories remain direct repository evidence rather than duplicated document
authority.

## Verification Summary

No Stage 01, 02, 03, or 99 document has been removed. One entry blocker is
released.

Removing a package that a sealed migration row names as its endpoint raised
`configuration error: WORK-054 WP-004B migration target differs` and exited 2,
naming no holder. Three owners in `scripts/validate-links-and-owners.py`
required a sealed endpoint to be tracked today, and they chained: releasing
`_work054_wp004b_targets` surfaced `_work109_migration_projection`, and
releasing that surfaced `_document_taxonomy_transition_manifest`. With all
three released, the same removal reports eleven findings that each name their
holder -- seven `LINK-BROKEN` from Specs `0011` through `0023`, and
`INDEX-STALE`, `INDEX-TREE`, and `LINK-BROKEN` on `docs/03.specs/README.md`.
The intact tree still returns `PASS CROSS-DOCUMENT`.

The release is a proof rather than a waiver. Ledger coverage is now counted
from the sealed rows, so MIG-0002 still asserts its 141 rows and the transition
manifest still asserts its 82 move-current entries; a manifest target the
ledger never sealed is still rejected. Four regression cases in
`tests/test_archive_validation.py` hold each half.

Two measurements in the Plan were corrected by executing them: consumer-zero
must count terminal documents, and the first removal tier splits into twenty
MIG-0004 row targets, three named only by other ledgers, and two in no ledger.

This work creates no Archive record, redirect, or Migration row, so the WP-013
and WP-009 clauses forbidding them are unaffected.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-013](../plan.md#wp-013--current-corpus-and-transition-control-cutover) | In progress. | Sealed-endpoint pin released across three owners with four regression cases; intact tree `PASS CROSS-DOCUMENT`; no corpus removal made. |
