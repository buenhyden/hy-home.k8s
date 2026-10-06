---
title: "Stage 99 Lifecycle Normalization Plan"
version: "1.8.0"
type: "sdlc/plan"
status: "completed"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-PLAN-0001"
parent_ids: ["SPEC-0106"]
---

# Stage 99 Lifecycle Normalization Implementation Plan

## Global Constraints

The [Spec](spec.md) owns behavior and `VAL-P02-001/002/003/004/005/006/007/009/010/011`; this Plan owns order,
dependencies, risk and rollback. Stage 99 owns machine form and lifecycle;
common governance owns meaning and approval. Preserve frozen history and
separate repository-static, provider-runtime, hosted and live evidence. The
original WORK-001 request authorized scoped local authoring, review, checks, and three
logical local commits. The earlier P02 finish instruction also authorized
local P01/P02 integration into main and removal of their development branches
after verified integration; the original Task records that observed finish.
The current `VAL-P02-002` follow-up authorizes four normal work-unit commits
in its own feature worktree and retains the P01 worktree. The request owner's
later instruction authorizes push and merge after required review and hosted
checks. Worktree removal, live/secret and archive mutation remain excluded;
no authenticated-actor claim or remote outcome is inferred.

WORK-003 applies the later instruction authorizing work-unit push and normal
merge after required hosted checks. Its repair stays on the preserved P01
feature branch; four local commits record draft, ready, in-progress and
completed Task states. No intermediate push is planned. Keep local full and
affected execution NOT_RUN under the scoped exclusion; hosted full remains
required. Preserve both worktrees and history.

## Overview

The original acceptance set was delivered through [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md).
Intake docs established the reviewable contract; the atomic implementation
changed the form/schema/checker/current-consumer surface. A corrective local
commit repaired an observed post-merge history-cache failure without changing
the acceptance contract. The original closing candidate commit recorded the
document state but did not itself establish that its separate closing checks
ran. EVD-P02-014 records the later historical and current-index rechecks,
with the original EVD-P02-013 result preserved. The Task alone owns execution
observations.

## Context

The `VAL-P02-002` follow-up reuses this completed package. WORK-002 adds an
explicit multi-row Task status writer while retaining the Registry generation,
Schema and existing validation behavior. Its scoped local handoff has four
normal commits (draft, ready, implementation in-progress, completion) on a
feature worktree based on `df3281d06a931bff6784bcc462800fab23bbb1c9`,
then proceeds through the authorized push, PR, hosted checks and merge route.
Only [SPEC-0106-TSK-0002](tasks/tsk-0002-task-summary-writer.md) records this
follow-up's actual execution results.

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
change, global/private change, or live/secret operation.
P01 completion and SPEC-0104 archive disposition stay intact.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-011 | [VAL-P02-011](spec.md#success-criteria--verification-plan) | Align three authority lifecycle fixture prerequisites with current role vocabularies and reciprocal evidence | Observed three named REDs; complete implicated-class and independent cause review; genuine registered-form first draft | [SPEC-0106-TSK-0011](tasks/tsk-0011-authority-lifecycle-state-fixtures.md) | Three named changed-input methods and their state/evidence boundaries; scoped hooks, each actual-index staged/message and independent review; prospective completion/review then fresh actual closing checks; hosted acceptance separate |
| WORK-010 | [VAL-P02-010](spec.md#success-criteria--verification-plan) | Align completed-state and navigation test fixtures with their current and historical owners | Observed named RED; faithful historical replay construction; registered-form first draft and independent review | [SPEC-0106-TSK-0010](tasks/tsk-0010-completed-state-and-navigation-fixtures.md) | Named changed-input cases and related refusal controls; scoped hooks, each actual-index staged/message and separate review; prospective completion/review then fresh actual closing checks; hosted acceptance separate |
| WORK-009 | [VAL-P02-009](spec.md#success-criteria--verification-plan) | Instantiate a new unique Task from its registered form and repair the common authority fixture | Separate reviewed Task8 rollback; observed registered-form creation metadata; retained named fixture failures and observations | [SPEC-0106-TSK-0009](tasks/tsk-0009-common-authority-fixture-reinstantiation.md) | Named routing/native controls; exact-input reuse only when independently justified; scoped hooks, each actual-index staged/message and separate review; prospective completion/review then fresh actual closing checks; hosted acceptance separate |
| WORK-007 | [VAL-P02-007](spec.md#success-criteria--verification-plan) | Align governance and Spec navigation fixtures with current declarations; resolve the archive process-budget failure through measured causal accounting | Observed final-head failures; independent cause/scope review; immutable accounting before any budget correction; completed Tasks preserved | [SPEC-0106-TSK-0007](tasks/tsk-0007-current-owner-fixture-conformance.md) | Changed named cases and relevant controls; unchanged batching/time bounds; scoped hooks, each actual-index staged/message and independent review; prospective completion/review then fresh actual closing checks; hosted acceptance separate |
| WORK-006 | [VAL-P02-006](spec.md#success-criteria--verification-plan) | Bind the additive recovery fixture's frozen Registry, source and immediate successor to one actual Git revision | Observed final-head hosted failure and exact named RED; independent cause/scope review; preserve completed Tasks and all production refusals | [SPEC-0106-TSK-0006](tasks/tsk-0006-sealed-source-revision-fixture.md) | 21 explicit shared recovery-fixture methods, scoped hooks, each actual-index staged/message and separate review; prospective terminal completion/review then fresh actual closing checks; hosted exact-head/main results separate |
| WORK-005 | [VAL-P02-005](spec.md#success-criteria--verification-plan) | Restore Task-only new history metadata eligibility and align three current Registry test consumers while retaining their negative contracts | Completed Task0004; observed hosted unit failures and same-pattern causal comparison; independent code/security review and actual-index checks before each normal commit | [SPEC-0106-TSK-0005](tasks/tsk-0005-current-registry-fixture-consumers.md) | Observed RED; changed-input Task-template, ordinary-copy and bounded malicious-pattern controls; identity/authority and all25 shared migration-fixture methods; scoped hooks; actual-index staged/message; prospective completion/review then fresh actual closing checks; required hosted and integrated-main observations separate |
| WORK-004 | [VAL-P02-004](spec.md#success-criteria--verification-plan) | Admit only registered unchanged regular Task-template copies for a new canonical unique first draft; preserve all other history guards | Explicit narrow validator delegation; real-Git RED before implementation; separate review and exact-index checks before each normal commit | [SPEC-0106-TSK-0004](tasks/tsk-0004-registered-task-template-instantiation.md) | Named bounded RED/GREEN and source/binding/identity/state/provenance negatives; actual-index staged/message; isolated terminal proposal then actual completion/review; hosted PR and integrated-main results remain separate |
| WORK-003 | [VAL-P02-003](spec.md#success-criteria--verification-plan) | Align current proof fixtures with complete published assets and cumulative headers/review transitions; independently prove frozen asset reads; repair scoped formatting/scanner acceptance | Hosted failure and security disposition; review before each index commit; local acceptance before final push | [SPEC-0106-TSK-0003](tasks/tsk-0003-ci-fixture-and-format-follow-up.md) | Focused RED/GREEN, proof and illegal-transition negatives and missing-object refusal; staged/message; completion and independent review; hosted PR checks before merge and main checks after merge |
| WORK-001 | [VAL-P02-001](spec.md#success-criteria--verification-plan) | WP-001 intake and source inventory; WP-002 atomic registry, form, checker, fixture and current-consumer normalization; WP-003 acceptance and local handoff | Approved P02 scope; intake review before implementation; reviewable implementation bytes before closing acceptance | [SPEC-0106-TSK-0001](tasks/tsk-0001-lifecycle-normalization.md) | Original intake, focused, affected, staged, review and local main finish evidence; candidate closing commit and current recheck in the Task; original full QA excluded by its finish scope |
| WORK-002 | [VAL-P02-002](spec.md#success-criteria--verification-plan) | WP-004 inspect current Task mutation path and create scoped Task; WP-005 extract summary helper, build opt-in CLI, focused RED/GREEN and author guidance; WP-006 exact-index verification, independent review and local source handoff; authorized push/merge follows separately | P01 tip `df3281d06a931bff6784bcc462800fab23bbb1c9`; WORK-001 completed contract; no Registry/Schema migration | [SPEC-0106-TSK-0002](tasks/tsk-0002-task-summary-writer.md) | Existing Task aggregate regression; writer preview/write/refusal regression; staged, actual message, completion and review on the exact follow-up inputs; required PR hosted result before merge and integrated main result afterward |

## Verification Plan

WORK-011 owns only `tests/test_document_lifecycle_archive_cutover.py`, this Spec,
Plan and its new registered-form Task. Use in-progress for current Spec body
maintenance and approved for the reciprocal supersession source/current successor.
Keep audit draft creation accepted, active/completed states refused and published
creation refused as noninitial. Preserve missing reciprocal evidence rejection
and exact reciprocal acceptance. Four forward commits record draft, readiness,
implementation and completion. The three explicit methods and scoped hooks
precede each actual-index staged/message and separate review. Prospective
completion/review precedes fresh actual closing checks. No local full/affected
execution or production change is in scope; hosted full-checkout admission remains
required beyond the capped failure preview.

WORK-010 owns only `tests/test_completed_state_migration.py`,
`tests/test_document_lifecycle_archive_cutover.py`, this Spec, Plan and its new
registered-form Task. Use the current in-progress predecessor and the actual
domainless collection README. Resolve own-generation replay with real frozen
Registry evidence rather than relabeling a modified current graph as history.
Preserve done rejection, terminal/no-reopen/direct-create and navigation controls.
The historical construction remains unverified until its named changed-input
check passes. Four forward commits record draft, readiness, implementation and
completion. Named checks and scoped hooks precede fresh actual-index staged,
message and independent review. The terminal proposal needs completion/review;
reflected source needs fresh actual staged/completion/message and final review
before commit. Local full/affected execution remains NOT_RUN; required hosted
checks admit the complete final checkout after the capped failure preview.

WORK-009 owns only `tests/test_common_agents_document_routes.py`, this Spec,
Plan and its new unique Task. After the separate reviewed Task8 rollback,
instantiate the genuine registered form with prompts removed; inspect its
actual copy-source metadata before the first normal commit. Preserve all ten
semantic routes, require the published governance domain and six states,
and give the synthetic native control its required metadata while retaining
every refusal. Four forward commits record draft, readiness, implementation
and completion. Pure fixture evidence may be reused only with exact input,
configuration and dependency proof and independent attribution. Every actual
index still needs fresh staged/message and separate review. The terminal
proposal needs completion/review; reflected source needs fresh actual
staged/completion/message and final review before commit. Full/affected
execution remains NOT_RUN; hosted gates stay required.

WORK-007 owns only `tests/test_archive_validation.py`,
`tests/test_common_agents_archive_routes.py`, this Spec, Plan and its new
Task. Derive governance expectations from current authored owner declarations
and retain profile, mode and state-membership checks. Both navigation payloads
use the registered section without changing their rejection assertions.
Immutable archive accounting must distinguish fixed corpus growth from an
implementation regression before any budget proposal. Preserve fallback
batching, the sixty-second bound and all production behavior. Four forward
commits record draft, readiness, implementation and completion. Explicit
named changed-input checks and scoped hooks precede each reviewed actual
index's canonical staged/message checks. The terminal proposal needs only
completion/review; reflected source needs fresh actual staged/completion,
message and separate final review before commit. Local full/affected remain
NOT_RUN; no remote run is retried or protected gate bypassed.

WORK-006 owns only `tests/test_archive_disposition_routes.py`, this Spec,
Plan and its new Task. Existing `GitFixture.commit_many` records exact
`legacy_registry_bytes()` and the unchanged source/successor bytes together;
the source blob is taken from that actual commit map. No new production API,
schema, template or asset helper is needed. Preserve all existing assertions
and proof-reuse checks. Four forward commits record draft, readiness,
implementation and completion. Quality selects the 21 named methods sharing
the changed recovery setup without discovery. Each actual source index needs
canonical staged, configured message and independent review. The terminal
proposal needs completion/review; its reflected actual index needs fresh
staged/completion/message and separate review before normal commit. Local
full and affected execution remain NOT_RUN, and no failed remote run is retried.

WORK-005 owns three current test consumers, its Spec/Plan/Task and the private
first-appearance metadata condition in `scripts/validate-document-lifecycle.py`.
The new all-mode eligibility is limited to trusted `sdlc/task` classification;
the existing ordinary-copy condition and every other refusal remain intact.
No new mirrored test or completed Task0004 edit is required. Five forward
logical commits separate draft, readiness, guard restoration, fixture repairs
and completion. The guard slice leaves fixture edits unstaged during its
actual-index checks; focused working-tree evidence names that separate input.
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
