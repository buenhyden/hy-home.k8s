---
title: "Finished Package Retention Technical Specification"
version: "0.3.0"
type: "sdlc/spec"
status: "done"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0083"
---

# Finished Package Retention Technical Specification (Spec)

## Overview

Stage 03 accumulated packages that are no longer current. ADR-0039 says a
finished unit waits in its stage until its disposition is approved, and the
request owner approved this round in two groups: seven packages already `done`,
then SPEC-0004, SPEC-0005 and SPEC-0082 once their own authorization arrived.

This Spec owns that round: it retains ten finished packages as exact units in
`completed/`, repoints the documents that cite them, records the disposition of
every package that stays, and closes. It also records why the two superseded
proposals cannot be retained yet. It changes no contract. The machinery it uses
was built and proved by
[SPEC-0082](../../98.archive/completed/03.specs/0082-unit-archive-retention-contract/spec.md).

## Strategic Boundaries & Non-goals

In scope: the ten finished Stage 03 packages named in Core Design; the
citations they receive from current documents and from `tests/`; one Retention
Catalog row per retained unit; the stage index and requirement pointers that
name them; the recorded finding that blocks the two superseded proposals; and a
recorded disposition for every Stage 03 package that stays.

Out of scope: any change to the retention contract, the citation table, or the
registry; the retention of SPEC-0068 and SPEC-0070, which the contracts block; the frozen ADR-0032 generation and the sixteen ADR-0038
retained bodies; the disposition of any package that stays, which is recorded
and returned rather than decided here; any package that still has a
non-terminal member; and every live cluster, provider runtime, and network
action.

## Contracts

A retained unit equals its source Git object entry for entry, links included.
The anchor state decides the class: `done` admits `completed/`. Every other
member is terminal in its own family. Each unit gets one catalog row naming
`<commit>:<original path>`, where the commit is the comparison base.

Citation follows the registry's ordered table. A `completed/` body stays citable
at its retained path, so a current consumer keeps its link and moves it.

The `superseded` class names a successor, so its retention requires
`superseded_by` on the unit anchor. For a spec package that anchor is
`spec.md`, and the `sdlc/spec` profile allows exactly eight frontmatter keys,
none of them `superseded_by`. Both contracts cannot hold at once, so no spec
package can be retained in `superseded/` today.

## Core Design

`completed/` receives SPEC-0073, SPEC-0074, SPEC-0075, SPEC-0076, SPEC-0079,
SPEC-0080, and SPEC-0081 in the first group, then SPEC-0004, SPEC-0005, and
SPEC-0082 in the second. Each has `done` for its `spec.md`, `plan.md`, and
every Task. SPEC-0004 and SPEC-0005 reached `done` by their own declared
`active` to `done` edge, in a commit of their own, before any move.

The sixteen packages that stay are surveyed but not disposed of. Each is
recorded with its anchor state and the reason it stays, and the reasons divide
into a current contract, open work, a withdrawal the registry cannot express, a
retention the profile cannot express, and a decision nobody has taken.

SPEC-0068 and SPEC-0070 stay in Stage 03. Both carry `status: "superseded"` and
both state in their own Overview that SPEC-0072 owns the current implementation
and acceptance criteria, which
[SPEC-0071](../0071-document-taxonomy-and-form-identity-normalization/spec.md)
records as well. Their successor is therefore settled and neither is a
withdrawal. Their retention is blocked instead by the contract conflict stated
above, which only a decision owning that contract can resolve.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference, and the
retained path is the only copy. No digest, blob pin, redirect, or path ledger is
added.

## Interfaces & Data Structures

No contract, registry, or citation-table changes. Retaining a unit did prove
three consumers of the move that no contract had taught about ADR-0039, and the
request owner authorized repairing them in place rather than reverting the
retention. Each repair states a fact the retention created; none lowers a gate.

- An operations document may not name Stage 98 at all, and the Promoted owner
  table may not hold a bare label. Both hold at once through the `N/A — reason`
  form this corpus already uses, so the two Stage 05 consumers name the package
  by identifier and reach it through the Archive index.
- A sealed WORK-054 or WORK-109 row names the successor that was current when
  it was sealed. Retention moves that successor without a ledger row, so
  `scripts/validate-links-and-owners.py` composes the Retention Catalog as
  successor edges and resolves each chain to its end. Retention is a move, not
  a removal, so the row still names a current owner.
- `scripts/archive_cutover.py` asks a different question: whether a terminal
  target is a current tracked file. A retained endpoint is not, so that sealed
  row composes no current owner and resolves through the Archive index, which
  is what the same branch already does for a deleted endpoint. The two modules
  stay different because their questions differ.
- The Git subprocess budget in `tests/test_archive_validation.py` moves 248 to
  252. Vacating a path costs a fixed four for Git-first recovery, which the
  constant's own history already records twice.

## Edge Cases & Error Handling

A package whose members are not all terminal stays where it is, and so does one
whose class the contracts cannot express; its consumers keep the links they
have. A consumer that cannot move to the retained path names the package by
identifier and reaches it through the Archive index. A Stage 98 index link to a
moved path is repaired in the same change, because the index is an archive
source that may link anywhere.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the round; the disposition is not weakened to pass. A
retention already merged is frozen, so a later correction needs its own
decision. An unresolved successor question returns to the request owner rather
than being decided here.

## Verification Commands

```bash
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/qa.py staged
python3 scripts/qa.py full
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-FPR-001 | Every unit in this round is recorded with its anchor state, its members, and the consumers it must move, before any move | Retention Task |
| VAL-FPR-002 | The blocked retention of SPEC-0068 and SPEC-0070 is recorded with both observed diagnostics and the successor their bodies already name | Retention Task |
| VAL-FPR-003 | No current document and no test pins a retained unit's active-stage path after the repointing | Link gate over the whole corpus, and the archive contract tests for the code consumer |
| VAL-FPR-004 | The ten finished packages are retained in `completed/`, each as one exact unit with one catalog row | Lifecycle and archive gates |
| VAL-FPR-005 | Full validation re-verifies every catalog row, including the rows this round adds | Archive cutover and full QA |
| VAL-FPR-006 | The stage index and the requirement pointers name the retained packages, and this package closes with observed results | Staged and full QA |
| VAL-FPR-007 | Every Stage 03 package that stays is recorded with its anchor state and the observed reason it stays | Retention Task |
| VAL-FPR-008 | Every consumer the retention proved wrong is repaired in place, and no gate, contract, or test pin is lowered to pass | Full QA and the unit-test suite |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[retention Task](tasks/tsk-0001-retain-finished-packages.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-001 | Survey recorded in the Task |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-002 | Contract conflict observed and recorded |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-003 | Citation decision over the corpus |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-004 | Lifecycle gate regressions |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-005 | Full-lane catalog re-verification |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-006 | Policy and index review |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-007 | Disposition survey recorded in the Task |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FPR-008 | Gate and unit-test regressions |
