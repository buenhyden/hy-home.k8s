---
title: "Retain the Finished Stage 03 Packages"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0083-TSK-0001"
---

# Task: Retain the Finished Stage 03 Packages

## Overview

This Task records the round: the survey each move starts from, the conflict
that blocks two of the nine units, the repointing, the seven retentions, and
the closure. It records observed results only and never promotes a
repository-static result to hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: on 2026-09-16 the request owner approved this round after review,
  with SPEC-0082 held back for its own authorization.
- The survey below reads the registry's own unit, mode, and class definitions
  through `scripts/archive_dispositions.py`, so a candidate here is a candidate
  the gates recognize.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-FPR-001 | Record the survey of the nine units | platform | Done | Recorded below | This Task |
| WORK-002 | VAL-FPR-002 | Record the conflict that blocks SPEC-0068 and SPEC-0070 and return it to the request owner | platform | Done | Recorded below | This Task |
| WORK-003 | VAL-FPR-003 | Repoint every current consumer of the seven retained units | platform | Queued | Not executed | Link gate |
| WORK-004 | VAL-FPR-004 | Retain the seven finished packages in `completed/` | platform | Queued | Not executed | Lifecycle and archive gates |
| WORK-005 | VAL-FPR-005 | Re-verify every catalog row in the full lane | platform | Queued | Not executed | Archive cutover and full QA |
| WORK-006 | VAL-FPR-006 | Close this package with its results | platform | Queued | Not executed | Staged and full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: the seven packages retained in this round, their consumers
  in documents and in `tests/`, the Stage 98 index, the Stage 03 index, and this
  package.
- **Forbidden Paths**: frozen records, ledgers, and retained bodies under
  `docs/98.archive/`, SPEC-0082, SPEC-0068 and SPEC-0070, `scripts/`,
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

SPEC-0082 is finished but stays. It is the evidence trail of the contract this
round applies, and ADR-0039 requires its own authorization for its disposition.

## Verification Summary

WORK-001 and WORK-002 are done and recorded above. WORK-003 to WORK-006 have
not run.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Done. | This Task. |
| [WORK-002](../plan.md#work-breakdown) | Done. | This Task. |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Link gate. |
| [WORK-004](../plan.md#work-breakdown) | Not executed. | Lifecycle and archive gates. |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Archive cutover and full QA. |
| [WORK-006](../plan.md#work-breakdown) | Not executed. | Staged and full QA. |
