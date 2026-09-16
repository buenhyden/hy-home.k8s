---
title: "Stage 03 Backlog Closeout Technical Specification"
version: "0.1.1"
type: "sdlc/spec"
status: "active"
owner: "platform"
updated: "2026-09-16"
layer: "specs"
artifact_id: "SPEC-0084"
---

# Stage 03 Backlog Closeout Technical Specification (Spec)

## Overview

[SPEC-0083](../../98.archive/completed/03.specs/0083-finished-package-retention/spec.md) retained the ten
finished Stage 03 packages and surveyed the sixteen that stayed, but it recorded
their dispositions rather than deciding them. Two of those dispositions were
blocked by the contracts themselves and were returned to the request owner.

This Spec owns the round that decides them. It closes the two contract gaps that
blocked the return, moves every remaining package to the terminal state its
evidence supports, resolves the duplicated frontmatter readers that SPEC-0077
still holds open, retains the units that reach a terminal state, and repairs the
consumers those retentions prove wrong.

## Strategic Boundaries & Non-goals

In scope: the sixteen Stage 03 packages that SPEC-0083 surveyed; the two
registry gaps that block their dispositions; the duplicated frontmatter readers
under `scripts/`; the retention of every unit that reaches a terminal state; the
consumers those retentions move; and this package.

Out of scope: opening a new archive stage directory; any change to a frozen
record, a sealed ledger, or a retained body; the native-runtime evidence that
SPEC-0072 defers to an operator; any live cluster, provider runtime, or network
action; and push, pull request, and merge.

## Contracts

A lifecycle edge is taken only where the registry declares it. A package reaches
a terminal state through its own family domain, and a Task reaches one through
the task domain, which declares no edge from `queued` to a terminal state.

Two gaps block dispositions the evidence already supports. The `sdlc/spec`
profile declares an empty `optional` key list, so a superseded spec cannot carry
the `superseded_by` key that `superseded/` retention requires, although
twenty-four sibling profiles already declare it optional and no profile forbids
it. The `spec-plan` domain declares no edge from `draft` to `withdrawn`,
although the `requirement-architecture` domain declares exactly that edge.
Closing both is a gap-fill: neither relaxes an assertion, and neither removes a
state or an edge that exists today.

Retention follows ADR-0039 unchanged. A retained unit equals its source Git
object entry for entry, the anchor state decides the class, and each unit gets
one catalog row.

## Core Design

Seven packages reach `done` on evidence already recorded: SPEC-0006,
SPEC-0054, SPEC-0062, SPEC-0071, SPEC-0077, SPEC-0078, and SPEC-0083, which
closed its own round. SPEC-0078 takes two edges because it is still `draft`.
SPEC-0054 and SPEC-0062 take their Task edges first, cancelling the items their
own records show to be unexecutable and closing the items their own records show
to be complete.

SPEC-0048 and SPEC-0051 reach `withdrawn` on the dated notes they already carry,
which name withdrawal as the recommended disposition and the missing edge as the
only blocker. Their Tasks are cancelled through the declared two-step path,
because the task domain gains no edge in this round.

SPEC-0068 and SPEC-0070 gain `superseded_by` naming SPEC-0072, which both
already name in prose, and are retained in `superseded/`. They are the first
spec packages to enter that class.

Five packages stay and gain a dated disposition note instead: SPEC-0008 owns the
current platform contract and six accepted ADRs name it as their Spec;
SPEC-0047 holds an unowned stash obligation; SPEC-0049 and SPEC-0050 hold
genuinely unowned work whose contract location must be re-planned before
activation; SPEC-0072 holds native-runtime criteria an operator must observe.

## Data Modeling & Storage Strategy

Git holds the bytes. The catalog row is the only recovery reference, and the
retained path is the only copy. No digest, blob pin, redirect, or path ledger is
added, and no archive stage directory is created.

## Interfaces & Data Structures

Two registry edits and one code consolidation change an interface.

- `docs/99.templates/registry.json` gains `superseded_by` in the `sdlc/spec`
  profile's `optional` list. The allowed key set is computed as required plus
  optional, so this admits one key and forbids nothing. The JSON schema already
  carries the grammar.
- The same file gains the `draft` to `withdrawn` pair in the `spec-plan`
  domain's transitions. The states already exist; only the edge is new.
- The duplicated frontmatter readers under `scripts/` resolve to the single
  owner in `scripts/validation/repository/bounded_io.py`. Behaviour does not
  change: every gate produces the output it produces today.

## Edge Cases & Error Handling

A package whose members are not all terminal stays where it is. A withdrawn
package stays at its Stage 03 path, because the `retired` retention class has no
directory in this repository and creating one is a separate decision. A consumer
that cannot move onto a retained path names the package by identifier and
reaches it through the Archive index. This package cites SPEC-0083, so that
citation moves when SPEC-0083 is retained in this same round.

## Failure Modes & Fallback / Human Escalation

A failing gate stops the round; no disposition is weakened to pass. A retention
already merged is frozen, so a later correction needs its own decision. A
criterion that an operator alone can observe is recorded as a deferral with a
named owner rather than claimed.

## Verification Commands

```bash
python3 scripts/validate-document-lifecycle.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/qa.py staged
python3 scripts/qa.py full
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-SBC-001 | Every remaining Stage 03 package is recorded with its anchor state, its non-terminal members, and its consumers before any edge is taken | Closeout Task |
| VAL-SBC-002 | The two registry gaps are closed as gap-fills, and no other profile, domain, state, or edge changes | Registry diff and the lifecycle gate |
| VAL-SBC-003 | SPEC-0071, SPEC-0078, SPEC-0062, and SPEC-0054 reach `done` with every member terminal and every edge declared | Lifecycle gate |
| VAL-SBC-004 | SPEC-0048 and SPEC-0051 reach `withdrawn` with every Task cancelled through the declared two-step path | Lifecycle gate |
| VAL-SBC-005 | SPEC-0006 reaches `done` after the stale sibling path in its body is repaired, because retention freezes bytes | Link gate |
| VAL-SBC-006 | SPEC-0068 and SPEC-0070 carry `superseded_by` and are retained in `superseded/` as exact units with one catalog row each | Archive gates |
| VAL-SBC-007 | Every package that stays carries a dated disposition note naming the reason and the next owner | Closeout Task and the stage index |
| VAL-SBC-008 | The duplicated frontmatter readers under `scripts/` resolve to one owner with no gate output change | Unit tests and full QA |
| VAL-SBC-009 | Every package that reaches `done` in this round is retained as an exact unit with one catalog row, and every consumer moves first | Link, lifecycle, and archive gates |
| VAL-SBC-010 | Every consumer the retention proves wrong is repaired in place, and no gate, contract, or test pin is lowered to pass | Full QA and the unit-test suite |
| VAL-SBC-011 | SPEC-0077 closes with its authority-blocked criteria recorded as deferrals with named owners | Closeout Task |
| VAL-SBC-012 | This package closes with observed results | Staged and full QA |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[closeout Task](tasks/tsk-0001-close-the-stage-03-backlog.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-001 | Survey recorded in the Task |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-002 | Registry review and lifecycle gate |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-003 | Lifecycle gate regressions |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-004 | Lifecycle gate regressions |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-005 | Citation decision over the corpus |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-006 | Archive cutover re-verification |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-007 | Disposition notes recorded in the Task |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-008 | Unit-test and gate regressions |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-009 | Lifecycle and archive gates |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-010 | Gate and unit-test regressions |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-011 | Deferral records with named owners |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SBC-012 | Policy and index review |
