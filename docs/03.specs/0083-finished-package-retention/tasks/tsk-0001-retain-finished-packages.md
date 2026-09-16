---
title: "Retain the Finished Stage 03 Packages"
version: "0.3.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0083-TSK-0001"
---

# Task: Retain the Finished Stage 03 Packages

## Overview

This Task records the round: the surveys each move starts from, the conflict
that blocks two units, the repointing, the ten retentions, the disposition of
every package that stays, and the closure. It records observed results only and
never promotes a repository-static result to hosted, provider-runtime, or live
evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: on 2026-09-16 the request owner approved this round after review,
  with SPEC-0082 held back for its own authorization, then approved SPEC-0004,
  SPEC-0005 and SPEC-0082 as a second group and a disposition review of every
  package that would stay.
- The survey below reads the registry's own unit, mode, and class definitions
  through `scripts/archive_dispositions.py`, so a candidate here is a candidate
  the gates recognize.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-FPR-001 | Record the survey of the nine units | platform | Done | Recorded below | This Task |
| WORK-002 | VAL-FPR-002 | Record the conflict that blocks SPEC-0068 and SPEC-0070 and return it to the request owner | platform | Done | Recorded below | This Task |
| WORK-003 | VAL-FPR-003 | Repoint every current consumer of the ten retained units | platform | Done | 100 references across 14 documents, both stage indexes, and two test fixtures | `PASS CROSS-DOCUMENT` over the whole corpus |
| WORK-004 | VAL-FPR-004 | Retain the ten finished packages in `completed/` | platform | Done | 22 renames in the first group and 19 in the second, one catalog row each | Staged QA 7/7 PASS per commit |
| WORK-005 | VAL-FPR-005 | Re-verify every catalog row in the full lane | platform | Queued | Not executed | Archive cutover and full QA |
| WORK-006 | VAL-FPR-006 | Close this package with its results | platform | Queued | Not executed | Staged and full QA |
| WORK-007 | VAL-FPR-007 | Record why every Stage 03 package that stays is staying | platform | Done | Sixteen packages in seven groups, recorded below | This Task |
| WORK-008 | VAL-FPR-008 | Repair every consumer the retention proved wrong | platform | Done | Two Stage 05 documents, two validators, one test budget | 1,099 unit tests pass with four skips; link, lifecycle and cutover gates pass |

## Approval and Safety Boundaries

- **Allowed Paths**: the ten packages retained in this round, their consumers
  in documents, in `scripts/` and in `tests/`, the Stage 98 index, the Stage 03
  index, and this package. The request owner widened this on 2026-09-16 to the
  consumers the retention proved wrong, having declined to revert it.
- **Forbidden Paths**: frozen records, ledgers, and retained bodies under
  `docs/98.archive/`, SPEC-0068 and SPEC-0070, every package that stays,
  `gitops/`, `infrastructure/`, `policy/`, `secrets/`, `.github/`.
- **Approval Required**: the disposition of each unit in this round. Push, pull
  request, and merge are not approved.
- **Static Validation**: focused checks per work item, `python3 scripts/qa.py
  staged` per logical commit, and one `python3 scripts/qa.py full` on the final
  tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the commits before integration; after integration a
  retained unit is frozen and only a forward decision changes it.
- **Evidence Location**: This Task record.

### Survey

Read on 2026-09-16 at `033532e0`. Every member of every unit below is terminal.
Every unit is also named twice by the Stage 03 index, in its tree block and in
its index row; those entries leave with the move instead of being repointed, so
the table lists only the consumers that keep a link.

| Unit | Anchor state | Class | Files | Current consumers |
| --- | --- | --- | --- | --- |
| SPEC-0068 | superseded | blocked | 1 | none |
| SPEC-0070 | superseded | blocked | 1 | SPEC-0048 spec and plan, SPEC-0071 spec and plan, SPEC-0081 Task |
| SPEC-0073 | done | `completed/` | 3 | REQ-0003, SPEC-0081 Task |
| SPEC-0074 | done | `completed/` | 3 | REQ-0003 |
| SPEC-0075 | done | `completed/` | 3 | REQ-0003, ADR-0036, SPEC-0081 Task |
| SPEC-0076 | done | `completed/` | 3 | REQ-0003, Stage 90 research m0009 |
| SPEC-0079 | done | `completed/` | 4 | REQ-0003 |
| SPEC-0080 | done | `completed/` | 3 | REQ-0003, `tests/test_archive_disposition_lifecycle.py` |
| SPEC-0081 | done | `completed/` | 3 | REQ-0003 |

One consumer is code rather than a document.
`tests/test_archive_disposition_lifecycle.py` reads SPEC-0080's three members
from their Stage 03 path to seed its fixture, so that constant moves with the
retention or the archive contract gate fails. Consumer search therefore covered
the whole repository, not `docs/` alone.

SPEC-0068 and SPEC-0070 were superseded as proposals before implementation.
Both Overviews name
[SPEC-0072](../../0072-agent-governance-and-quality-gate-consolidation/spec.md)
as the owner of the current implementation and acceptance criteria, and
SPEC-0071 records the same succession. The successor question the request owner
asked is therefore answered: a successor exists, so neither package is a
withdrawal and neither belongs in `retired/`.

Their retention in `superseded/` is blocked. That class names a successor, so
the parity check requires `superseded_by` on the unit anchor, which for a spec
package is `spec.md`; the `sdlc/spec` profile allows exactly eight frontmatter
keys and `superseded_by` is not one of them. Both halves were observed on
2026-09-16 rather than inferred:

- Retaining a spec package in `superseded/` without the key reports
  `ARCHIVE-DISPOSITION-NAMING`. The same package in `completed/` reports
  nothing, and the same package in `superseded/` carrying the key reports
  nothing, so the class is the cause and the key is the only way through.
- Adding `superseded_by` to a `sdlc/spec` body reports `FM-KEYSET` with
  `extra: ["superseded_by"]` against an eight-key allowed set.

No spec package has ever been retained in `superseded/`; all fifty-three
archived spec packages sit in `completed/`, whose class names a promotion and
demands no successor key. Resolving this needs a decision that owns the
retention contract or the `sdlc/spec` profile, which this round is not
authorized to make. This Task returns the question to the request owner and
changes no contract.

SPEC-0082 was held back at first, because it is the evidence trail of the
contract this round applies and ADR-0039 requires its own authorization. The
request owner gave that authorization, so it was retained with the second group.

### Second survey

Read on 2026-09-16 at `90caf0bd`. SPEC-0004 and SPEC-0005 carried `active`
anchors over work finished long ago. They took the single declared `active` to
`done` edge in their own commit before any move, so the anchor state decided the
class rather than the move deciding it.

| Unit | Anchor state | Class | Files | Current consumers |
| --- | --- | --- | --- | --- |
| SPEC-0004 | done | `completed/` | 7 | REQ-0001, ADR-0011, AD-0004, policy 0004, runbook 0004 |
| SPEC-0005 | done | `completed/` | 7 | REQ-0002, ADR-0012, AD-0005, AD index, policy 0004, runbook 0004 |
| SPEC-0082 | done | `completed/` | 5 | REQ-0003, ADR-0039, research 0002, SPEC-0072 Task, SPEC-0083 |

Two consumer shapes escaped the first search pattern and are recorded so the
next round does not repeat them. A sibling package cites its neighbour without
the stage prefix, as `../0082-.../spec.md`, so a search keyed on `03.specs/`
cannot see it; this package's own citation of SPEC-0082 was caught by the link
gate rather than by the survey. A slug is not unique across stages either:
SPEC-0004 and AD-0004 share `0004-argo-rollouts-progressive-delivery`, so a
bare-slug search also returns the architecture description, which does not move.
The reliable key is the trailing slash, because a package is a directory and a
single document is not.

`tests/test_archive_citation_decision.py` names a retained package in two
fixtures. Both pass the path as a string and neither reads it, so the move did
not break them; the eighty-seven archive contract tests passed before the change
and after it. The names had gone stale rather than broken, and the request owner
chose to repoint them at a package that is still in Stage 03.

### Disposition of the packages that stay

Read on 2026-09-16 at `1698be68`. Sixteen packages remain in Stage 03, this one
included. Every one was read. None is retained by this round, and the reasons
differ in what they ask of the next owner.

| Group | Packages | Observation |
| --- | --- | --- |
| Active technical contract | SPEC-0008 | Self-declares the current contract for `gitops/`, `infrastructure/` and `scripts/`; ADR-0014 names it as its Spec |
| Work still open | SPEC-0047, SPEC-0054, SPEC-0062, SPEC-0071, SPEC-0072, SPEC-0077 | At least one member is `queued`, `in-progress` or `blocked`, so the unit has no terminal anchor |
| Withdrawal recommended, edge undeclared | SPEC-0048, SPEC-0051 | Each carries a dated disposition note from 2026-09-14 naming the blocker and the owner |
| Draft, no disposition recorded | SPEC-0049, SPEC-0050, SPEC-0078 | Never activated and never judged |
| Retention blocked by the profile | SPEC-0068, SPEC-0070 | Recorded above |
| Active, no disposition recorded | SPEC-0006 | Nothing blocks it; no decision has been taken |
| This package | SPEC-0083 | Closes with this round |

Two registry edges, not three, account for the blocked withdrawals. The
`spec-plan` domain covers `spec.md` and `plan.md` together and declares
`draft → active`, `active → done`, `active → superseded` and
`active → withdrawn`, but no `draft → withdrawn`. The `task` domain declares no
`queued → cancelled`. Withdrawing a never-activated draft therefore needs either
a false activation or a new edge, and this round adds neither. SPEC-0078 already
prescribes the handling those two packages carry: a package whose recommended
disposition needs an undeclared edge keeps its state and gains a dated
disposition note naming the blocker and the owner.

SPEC-0006 is unjudged rather than blocked, and the difference decides who acts
next. Both `active → done` and `active → withdrawn` are declared, so no contract
stands in the way. Its own Overview says it remains active only for the
historical harness-gap baseline and hands its live ownership to SPEC-0025, which
is itself already retained in `completed/`. Outside the archive and the stage
index, no current document names it as an owner. What it needs is a decision,
not a contract change.

Three observations about the open packages are recorded without judgement,
because this round is not authorized to dispose of an open package. SPEC-0047
holds five `queued` Tasks last touched on 2026-09-10 and no `in-progress`
member. SPEC-0054 holds `tsk-0009` from 2026-09-03 and `tsk-0014` from
2026-08-31 in the same shape. SPEC-0062 holds three Tasks `blocked` since
2026-08-29, and `blocked → in-progress` is declared, so the registry is not what
holds them.

### Consumers the retention proved wrong

Full QA over the working tree named two failing gates that staged QA could not
see, because both belong to the full lane only. Both trace to the same act:
moving a finished package out of Stage 03. The request owner declined to revert
the retention and authorized repairing each consumer instead. Every repair below
states a fact the retention created; none lowers a gate, a contract or a pin.

| Consumer | What the retention broke | Repair |
| --- | --- | --- |
| `docs/05.operations/policies/0004-...md`, `docs/05.operations/runbooks/0004-...md` | An operations document may not name Stage 98, and the Promoted owner table may not hold a bare label | Name the package by identifier and declare the exclusion in the `N/A — reason` form the corpus already uses |
| `scripts/validate-links-and-owners.py` | A sealed WORK-054 or WORK-109 row named a successor the retention moved, so the edge read as vacated | Compose the Retention Catalog as successor edges and resolve each chain to its end |
| `scripts/archive_cutover.py` | A sealed row's terminal target was no longer a current tracked file | Treat a retained endpoint the way the same branch already treats a deleted one: it composes no current owner and resolves through the Archive index |
| `tests/test_archive_validation.py` | Vacating `docs/03.specs/0004-.../` sent the archived-bytes proof through Git-first recovery | Move the Git subprocess budget 248 to 252 and record why, as the constant's own history does |

Two observations are recorded because they were nearly missed. The two Stage 05
rules are not one rule: removing the archive link satisfied the first and broke
the second, and only the `N/A — reason` form satisfies both. And the two
validators are left deliberately different. One asks where an alias resolves, so
a retained endpoint is a move and composes; the other asks whether a terminal
target is a current tracked file, so a retained endpoint is not and drops.
Making them identical for symmetry would change an answer neither question
asked.

## Verification Summary

WORK-001 to WORK-004, WORK-007 and WORK-008 are done and recorded above.
WORK-005 and WORK-006 have not run.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | This Task. |
| [WORK-002](../plan.md#work-breakdown) | Done. | This Task. |
| [WORK-003](../plan.md#work-breakdown) | Done. | Link gate over the whole corpus. |
| [WORK-004](../plan.md#work-breakdown) | Done. | Lifecycle and archive gates, staged QA per commit. |
| [WORK-007](../plan.md#work-breakdown) | Done. | This Task. |
| [WORK-008](../plan.md#work-breakdown) | Done. | 1,099 unit tests pass; link, lifecycle and cutover gates pass. |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Archive cutover and full QA. |
| [WORK-006](../plan.md#work-breakdown) | Not executed. | Staged and full QA. |
