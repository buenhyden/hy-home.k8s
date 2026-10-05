---
title: "Stage 99 Lifecycle Normalization Plan"
version: "1.3.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-PLAN-0001"
parent_ids: ["SPEC-0106"]
---

# Stage 99 Lifecycle Normalization Implementation Plan

## Global Constraints

The [Spec](spec.md) owns behavior and `VAL-P02-001`; this Plan owns order,
dependencies, risk and rollback. Stage 99 owns machine form and lifecycle;
common governance owns meaning and approval. Preserve frozen history and
separate repository-static, provider-runtime, hosted and live evidence. The
original WORK-001 request authorizes scoped local authoring, review, checks, and three
logical local commits. The earlier P02 finish instruction also authorized
local P01/P02 integration into main and removal of their development branches
after verified integration; the Task records that observed finish. The current
P01 follow-up keeps its own feature branch/worktree and excludes further
integration or cleanup. For that historical scope, remote/publication, live/secret and archive-mutation
actions remain excluded, without an authenticated-actor claim.

WORK-003 applies the later instruction authorizing work-unit push and normal
merge after required hosted checks. Its repair stays on the preserved P01
feature branch; four local commits record draft, ready, in-progress and
completed Task states. No intermediate push is planned. Keep local full and
affected execution NOT_RUN under the scoped exclusion; hosted full remains
required. Preserve both worktrees and history.

## Overview

Deliver the one acceptance set through [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md).
Intake docs established the reviewable contract; the atomic implementation
changed the form/schema/checker/current-consumer surface. A corrective local
commit repaired an observed post-merge history-cache failure without changing
the acceptance contract. The original closing candidate commit recorded the
document state but did not itself establish that its separate closing checks
ran. EVD-P02-014 records the later historical and current-index rechecks,
with the original EVD-P02-013 result preserved. The Task alone owns execution
observations.

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
execution boundary, not a change to repository policy. The Task owns actual
test and QA observations.

## Goals & In-Scope

Normalize the existing six-key profile extensions, Task row/body lifecycle,
completion trace, route and historical compatibility, current P01/P02 documents,
forms, schemas, checker consumers and focused fixtures in one coherent change.
Use the affected-path validation registry and record exact snapshots/results.

## Non-Goals & Out-of-Scope

For original WORK-001, no new unrelated document family, duplicate stable ID copy, extra Task, progress ledger, inventory
pin, permanent `change_id` capacity, frozen archive rewrite, provider trust
change, global/private change, remote Git action, or live/secret operation.
P01 completion and SPEC-0104 archive disposition stay intact.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-005 | [VAL-P02-005](spec.md#success-criteria--verification-plan) | Align three stale current Registry test consumers with published profile/domain declarations while retaining their negative contracts | Completed Task0004; observed hosted unit failures and bounded local diagnosis; separate review and actual-index checks before each normal commit | [SPEC-0106-TSK-0005](tasks/tsk-0005-current-registry-fixture-consumers.md) | Five observed named RED inputs; changed-input named GREEN and explicitly selected shared-fixture controls; scoped hooks; actual-index staged/message; prospective completion/review then fresh actual closing checks; required hosted and integrated-main observations separate |
| WORK-004 | [VAL-P02-004](spec.md#success-criteria--verification-plan) | Admit only registered unchanged regular Task-template copies for a new canonical unique first draft; preserve all other history guards | Explicit narrow validator delegation; real-Git RED before implementation; separate review and exact-index checks before each normal commit | [SPEC-0106-TSK-0004](tasks/tsk-0004-registered-task-template-instantiation.md) | Named bounded RED/GREEN and source/binding/identity/state/provenance negatives; actual-index staged/message; isolated terminal proposal then actual completion/review; hosted PR and integrated-main results remain separate |
| WORK-003 | [VAL-P02-003](spec.md#success-criteria--verification-plan) | Align current proof fixtures with complete published assets and cumulative headers/review transitions; independently prove frozen asset reads; repair scoped formatting/scanner acceptance | Hosted failure and security disposition; review before each index commit; local acceptance before final push | [SPEC-0106-TSK-0003](tasks/tsk-0003-ci-fixture-and-format-follow-up.md) | Focused RED/GREEN, proof and illegal-transition negatives and missing-object refusal; staged/message; completion and independent review; hosted PR checks before merge and main checks after merge |
| WORK-001 | [VAL-P02-001](spec.md#success-criteria--verification-plan) | WP-001 intake and source inventory; WP-002 atomic registry, form, checker, fixture and current-consumer normalization; WP-003 acceptance and local handoff | Approved P02 scope; intake review before implementation; reviewable implementation bytes before closing acceptance | [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md) | Original intake, focused, affected, staged, review and local main finish evidence; candidate closing commit and current recheck in the Task; original full QA excluded by its finish scope |

## Verification Plan

WORK-005 changes only three current test consumers and its Spec/Plan/Task.
The artifact cases follow the published archive route identity; authority
cases follow current requirement and architecture lifecycle domains; the
migration fixture adjusts an existing bounded route in the complete current
graph instead of appending duplicate declarations or retired domains.
Preserve every related rejection and proof check. Quality executes explicit
named cases, including the 25 shared migration setup consumers, without
discovery or a full/all-files substitute. Each logical source index receives
canonical staged, configured message and independent review. A terminal
proposal receives completion and semantic review; the reflected source then
receives fresh actual staged/completion/message and separate review before
commit. Local full and affected execution remain NOT_RUN.

WORK-004 uses real Git copy evidence and exact current/historical template
bindings. Only the private copy guard and its focused regression fixture may
change. A first draft retains normal initial-event comparison and every later
state, identity, deletion, merge and budget check. Quality owns bounded named
tests and canonical staged/message/completion checks; an independent reader
reviews each exact index. Local full and affected execution remain NOT_RUN.
The existing automatic hosted run is preserved; the final corrected head
must receive normal required hosted checks before merge.

WORK-003 requires focused historical fixture RED/GREEN and missing-object
refusal; exact-index staged/message checks for each local commit; final
completion and independent review. Required hosted PR checks precede merge;
integrated-main hosted checks follow merge before integration acceptance.

Focus RED/GREEN on status aggregation, duplicate/missing rows, criterion links,
required versus nonrequired cancellation, Git transition/deletion/reopening,
route values and frozen fixtures. Inspect affected paths before selecting
`python3 scripts/qa.py quick`; exact-index `staged` and actual message checks
preceded each original P02 local commit. Its finish instruction excluded further
full QA and all-files/unit substitutes from the required set. Preserve the
interrupted full observations and record an unexecuted full as NOT_RUN with
acceptance not-required. The current P01 follow-up selected affected gates
without executing that lane; it rechecked the historical P02 candidate and
the later changed index separately. The local main finish is already
recorded in the Task. Record Task results as `NOT_RUN`, `PASS`, `FAIL`, `DEFER` or
`NOT_APPLICABLE`, with separate criterion acceptance and quality-lane evidence;
never promote an unexecuted check. The independent reviewer reports findings read-only.

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
commands, limits, residual risk and next owner. The Spec and Plan carried
version 1.0.0 and completed candidate status at the original source acceptance
and local finish recorded in the Task. The later EVD-P02-014 accepts the
historical recheck and a current changed-index staged, completion and
independent review result; it does not invent an approving actor, timestamp,
authentication or revocation check. Remote/live lanes remain
unobserved unless separately authorized and executed.
