---
title: "Stage 99 Lifecycle Normalization Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "platform"
updated: "2026-10-04"
layer: "specs"
artifact_id: "SPEC-0106-PLAN-0001"
---

# Stage 99 Lifecycle Normalization Implementation Plan

## Global Constraints

The [Spec](spec.md) owns behavior and `VAL-P02-001`; this Plan owns order,
dependencies, risk and rollback. Stage 99 owns machine form and lifecycle;
common governance owns meaning and approval. Preserve frozen history and
separate repository-static, provider-runtime, hosted and live evidence. The
direct P02 request authorizes scoped local authoring, review, checks, and three
logical local commits; it does not authorize remote or live actions.

## Overview

Deliver the one acceptance set through [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md).
Intake docs establish a reviewable contract; one atomic implementation commit
changes the form/schema/checker/current-consumer surface; a closing acceptance
commit records final evidence and state. The Task alone owns observed progress.

## Context

Preflight observed clean `codex/p02-stage99-lifecycle` at
`50890376ddef88de69f7df4204fc72dfc265c051`, diverged from local `main`
`f6501e46a0d35858c598c207e726a0e89c92d7d7`. The completed P01 package
is still current; SPEC-0104 is in Stage 98 and is not reopened. SPEC-0106 was
vacant in current and archive path inventory. Planning source inspection found
81 registry profiles, 37 physical forms, two schemas and the existing
Stage 99 registry, Markdown, link, lifecycle, template, Archive, quality and
QA-route consumers; counts are observed snapshots, not acceptance constants.

Installed preflight identities supplied for this work are Python 3.12.3,
pre-commit 4.6.1, Kustomize 5.8.1 with digest
`f7b1605aa5143e0dcbd754a4d43c47ad7a560c540b1356b064d69fe236164494`,
and the fixed Conftest digest
`a38ba21668929a00dce2fe6ee43d1312228340bce5fd243f47dd0ce90516e558`, consumed by
`scripts/validate-policy-gates.sh:57`. Bounded shell calls have needed native
escalation because `bwrap` fails at loopback setup; that approval is a tool
execution boundary, not a change to repository policy. No P02 test or QA lane
has been run yet.

## Goals & In-Scope

Normalize the existing six-key profile extensions, Task row/body lifecycle,
completion trace, route and historical compatibility, current P01/P02 documents,
forms, schemas, checker consumers and focused fixtures in one coherent change.
Use the affected-path validation registry and record exact snapshots/results.

## Non-Goals & Out-of-Scope

No new document family, stable ID copy, extra Task, progress ledger, inventory
pin, permanent `change_id` capacity, frozen archive rewrite, provider trust
change, global/private change, remote Git action, or live/secret operation.
P01 completion and SPEC-0104 archive disposition stay intact.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Intake and source inventory | Approved P02 scope | Clean baseline, selected profiles and forms | Draft Spec/Plan/queued Task and affected check plan |
| WP-002 | Atomic registry, form, checker, fixture and current-consumer normalization | WP-001 | Intake reviewed; focused RED cases and exact consumer inventory | GREEN cases, affected gates, staged QA and implementation commit |
| WP-003 | Acceptance and local handoff | WP-002 | Reviewable implementation bytes | Independent review, one local full run, completion mode, closing documentation, staged/message evidence and closing commit |

## Verification Plan

Focus RED/GREEN on status aggregation, duplicate/missing rows, criterion links,
required versus nonrequired cancellation, Git transition/deletion/reopening,
route values and frozen fixtures. Inspect affected paths before selecting
`python3 scripts/qa.py quick`; exact-index `staged` and actual message checks
precede each local commit. Run full once on the final implementation tree, then
affected and completion mode after Task-only closure. Record `PASS`, `FAIL`,
`SKIP`, or `DEFER` by the quality lane vocabulary without promoting an
unexecuted check. The independent reviewer reports findings read-only.

## Risks & Mitigations

The Task parser could infer a false completion from one row: test mixed rows,
blocked priority, all-completed and cancelled cases. Historical fixtures could
be misclassified as current: compare archived generations without rewriting
them. Broad schema edits could break unrelated forms: inventory exact consumers
and preserve the six-key envelope. A tool/budget deny leaves the check pending,
not silently skipped. Rollback uses reviewed forward reverts of P02 commits
while preserving the Task evidence, Git ledger and unrelated changes.

## Completion Criteria

`VAL-P02-001` passes as one atomic set, all required local gates and read-only
review have observed evidence, and the Task records exact checked snapshots,
commands, limits, residual risk and next owner. Stable approval of Spec and
Plan may raise their versions to 1.0.0 and status to active using the existing
explicit P02 approval input; the record must not invent an approving actor,
timestamp, authentication or revocation check. Completion status waits for
actual implementation and acceptance evidence. Remote/live lanes remain
unobserved unless separately authorized and executed.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-P02-001](spec.md#success-criteria--verification-plan) | WP-001, WP-002, WP-003 | [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md) |
