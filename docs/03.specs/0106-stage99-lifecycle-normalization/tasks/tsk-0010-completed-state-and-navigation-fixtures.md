---
title: "Completed-State and Navigation Fixtures"
version: "1.0.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0010"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Completed-State and Navigation Fixtures

## Overview

Repair two test consumers exposed by the executed hosted complement, preserving
their current and historical refusal contracts. Readiness accepts observed draft
checks and registered creation; implementation and its acceptance remain pending.

## Inputs

- [Spec](../spec.md#success-criteria--verification-plan), VAL-P02-010, and
  [Plan](../plan.md#work-breakdown), WORK-010.
- P01 branch `codex/p01-authority-evidence` at the accepted Task9 closing
  snapshot. Its source/index was clean before this three-document draft.
- PR133 run 37374280472 attempt2, job 111990529985: the complement executed
  and unit-tests failed. This is distinct from attempt1's runner acquisition
  cancellation. The displayed sanitized failure excerpt is capped and is not
  an exhaustive failure inventory.
- Three explicit named local checks reproduced the current Spec/Plan active
  predecessor rejection, own-generation replay refusal, and research-pack
  profile mismatch. Existing frozen-generation fixture bytes are available;
  a faithful replay construction is proposed but has not passed a check.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-010 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | Correct completed-state and navigation fixture prerequisites while preserving refusal controls | platform | frontmatter | NOT_RUN | pending | EVD-P02-101/102/103 pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-100 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | WORK-010 | Three explicit named RED checks; independent cause/scope review | Unchanged accepted Task9 checkout; sixty-second bounds | FAIL | External safe named receipt `hy-p01-751623-attempt2-named.receipt.json`; cause receipt `hy-p01-751623-attempt2-named-causes.json` | rejected |
| EVD-P02-101 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | WORK-010 | Named changed-input GREEN, related refusal controls and scoped hooks | Pending corrected fixture bytes | NOT_RUN | Pending focused receipts | pending |
| EVD-P02-102 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | WORK-010 | Draft actual-index staged/message and independent review | Frozen three-document draft; unchanged configs and exact message | PASS | External `hy-p01-task10-c1-staged.receipt.json`, separate `staged-qualification.json` and `message.receipt.json`; independent reviewer `/root/p02_independent_review` | accepted |
| EVD-P02-103 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | WORK-010 | Prospective completion/review and fresh actual closing checks | Pending terminal candidates | NOT_RUN | Pending separate prospective and actual receipts | pending |
| EVD-P02-104 | [VAL-P02-010](../spec.md#success-criteria--verification-plan) | WORK-010 | Registered-form first-appearance metadata | Actual cached and committed C007 from unchanged declared regular Task form; target absent before creation | PASS | Ignored `p01-task10-c1-creation-preflight.json` and `p01-task10-c1-postcommit.json`; selected metadata observations, full raw diff not persisted | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/plan.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0010-completed-state-and-navigation-fixtures.md`,
  `tests/test_completed_state_migration.py`,
  `tests/test_document_lifecycle_archive_cutover.py`.
- **Forbidden Paths**: Production validators/helpers, published Registry and
  schemas, native controls, frozen Archive, completed Task evidence and unrelated
  source. No gate, resource-bound or provenance relaxation.
- **Approval Required**: The user's explicit normal unit-commit/push/merge goal
  and the supervisor's scoped necessary fixture-repair delegation authorize this
  work. Existing conditional permission allows terminal candidate reflection only
  after prospective completion/review, with fresh actual checks and separate
  review required before commit. Protected merges still require exact-head hosted
  checks; no admin, force, history rewrite or live operation is authorized.
- **Static Validation**: Three observed named REDs; faithful current/historical
  fixture construction; seven explicit named GREEN/refusal controls in
  `p01-task10-focused-manifest.json` within sixty-second focused bounds; pinned
  scoped hooks; fresh canonical staged/message per actual
  index and independent review. The runner's existing envelope remains unchanged.
  Prospective completion/review precedes fresh actual closing staged/completion,
  message and review. Full/affected execution remains NOT_RUN.
- **Live Validation**: DEFER; no live infrastructure operation is in scope.
  Required hosted PR and integrated-main checks remain separate pending lanes.
- **Secret / Vault Handling**: No credential/private-state reads or raw payload
  publication. Preserve private raw diagnostics externally and expose only safe
  metadata, exact input identities and bounded failure classifications.
- **Rollback Plan**: A reviewed normal forward correction or revert of this
  bounded unit preserves original commits, branches, worktrees and raw evidence;
  no reset, force or destructive cleanup.
- **Evidence Location**: This Task owns execution meaning; external safe receipts
  and ignored `.worktrees/proposal` candidates retain raw input/check identities
  without a source self-OID loop.

## Verification Summary

Intake is observed: all three named checks failed on unchanged inputs, and the
independent reviewer confirmed the five-path fixture scope. Spec/Plan must use
the current in-progress predecessor; lifecycle-free creation must target the
domainless collection index, not a stateful research pack. Historical replay
must prove each commit's real declared graph. The independently reviewed design
uses two isolated Git fixtures: real frozen generation9 draft/active/done history
must be admitted using the current Registry argument; its unsupported terminal
cutover must be refused. A separate current-generation legal review/approval
prefix must reach completed, while a later same-path done must be refused. This
avoids unrelated copied-path provenance and does not claim which cutover
condition rejects first. The construction is not implemented or tested yet.

The observed draft index ran six fresh canonical gates and the exact configured
message hook, with complete streams/cleanup and no input drift. An initial QA
receipt parser incorrectly aggregated quoted semicolon fields; its original
false wrapper is preserved, with a separately audited parsing qualification and
no execution retry. Configured message validation observed equal disposable
stage entries and copied configs; raw disposable index bytes changed without a
known cause and were not an acceptance prerequisite. Independent final review
accepted the actual leaves before the normal draft commit.

Readiness selection over the five paths lists seven validators, unmatched zero,
without executing affected validation. The explicit seven-method manifest keeps
all six completed-state tests plus the domainless-navigation case. No production
or fixture input has changed. This ready index's staged/message, implementation,
whole WORK and terminal checks remain NOT_RUN until observed. Next owners are
the writer, separate quality actor and independent reviewer; hosted admission
remains required for the final checkout, beyond the capped failure excerpt.
