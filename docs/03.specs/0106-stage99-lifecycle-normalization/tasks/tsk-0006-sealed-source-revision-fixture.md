---
title: "Sealed Source Revision Fixture"
version: "1.0.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0006"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Sealed Source Revision Fixture

## Overview

This bounded follow-up owns [VAL-P02-006](../spec.md#success-criteria--verification-plan)
and [WORK-006](../plan.md#work-breakdown). A final-head hosted unit failure
exposed missing Git-revision prerequisites in the additive archive recovery
fixture. Completed Tasks0003/0004/0005 and their evidence remain historical.

## Inputs

- The user's explicit normal unit-commit, push and merge instruction covers
  this necessary reversible fixture repair. Independent cause/scope review
  confirmed the four-path boundary and existing production contract.
- [Plan](../plan.md), [registered Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Final P01 implementation `c4c0a5f2d316f4e740c13b1c76be0568727dab06`;
  automatic run `37326092921`, QA job `111817095660`. No retry or cancel.
- Source fixture `tests/test_archive_disposition_routes.py` and existing
  `tests/git_fixture.py` commit API; immutable generation-9 Registry reader
  in `tests/archive_generation_fixture.py`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-006 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | Record the real frozen Registry, source and successor at the authenticated source revision | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Observed intake](#observed-intake) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-060 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Hosted failure and exact named reproduction | Unchanged additive recovery fixture at P01 `c4c0a5f2…` | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-061 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Changed-input recovery checks and scoped hooks | Pending reviewed implementation | NOT_RUN | [Validation boundaries](#validation-boundaries) | pending |
| EVD-P02-062 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Actual-index staged/message and separate review | Pending actual logical source indexes | NOT_RUN | [Validation boundaries](#validation-boundaries) | pending |
| EVD-P02-063 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Prospective terminal completion and independent review | Pending isolated terminal candidate | NOT_RUN | [Validation boundaries](#validation-boundaries) | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan, Task and `tests/test_archive_disposition_routes.py`; one repo-tooling-engineer writer.
- **Forbidden Paths**: Production validators, Registry/schema/template assets, frozen Archive, completed Tasks/evidence, existing fixture helpers, hosted configuration, private values and unrelated files.
- **Approval Required**: Existing explicit normal delivery and necessary scoped fixture-repair authority applies. The user's conditional terminal reflection permission requires fresh actual checks and separate review before commit; no external authority is widened.
- **Static Validation**: Preserve observed RED; run the 21 explicit shared recovery-setup methods on changed bytes, scoped pinned hooks and each actual-index staged/message with independent review. Prospective completion/review precedes reflected source's fresh actual staged/completion/message/review. Local full and affected execution remain NOT_RUN.
- **Live Validation**: DEFER — no cluster or runtime operation requested.
- **Secret / Vault Handling**: Safe rule, path and exception metadata only; no raw CI payload or private values.
- **Rollback Plan**: Reviewed forward correction or revert; no force, rebase, branch deletion, cleanup or local main mutation.
- **Evidence Location**: This Task and external safe receipts. Operational absolute argv/cwd and actual closing OID stay outside tracked source.

## Verification Summary

### Observed intake

The automatic final-head run's observed failing gate was `unit-tests`; its
canonical document-lifecycle, pre-commit and other reported gates passed.
The failure preview is capped at 1024 characters and is not an exhaustive
failure count. It names
`ArchiveDispositionRecoveryTest.test_additive_record_uses_its_own_sealed_disposition_not_work107_census`.
The exact named method ran once under a 60-second bound and failed because
`ARCHIVE-MIGRATION-PARITY` was unexpectedly present. Actual outer rc was1,
elapsed0.902s; output and cleanup completed, source/index/refs stayed clean.
Safe RED receipt SHA-256 is
`b3e0260a8dda2d36358d401f14c3afd7d21dd370bcff38254dea6e85ab28b7cd`;
raw stderr SHA-256 is
`b744bf30b35081271b3ca97acf201236a61b3d6545b610429747a43b6bdf1871`.

The authenticated source commit currently contains only source bytes;
Registry is absent and successor is committed afterward. The existing
`historical_generation_registry` refuses the missing regular Registry blob
with `ARCHIVE-MIGRATION-PROFILE`, before disposition lifecycle checks.
The generation-9 path also requires the immediate replacement blob in that
same revision. Independent review confirmed both prerequisites. The minimum
repair uses existing `GitFixture.commit_many` with exact frozen Registry,
unchanged source and successor bytes, and binds recovery metadata to its
actual source blob. Historical projection needs no schema/template assets
here; no production fallback or refusal is changed.

### Validation boundaries

Draft records scope and actual intake only. Implementation, scoped hooks,
current draft/ready indexes and terminal observations are NOT_RUN until
performed. Quality and independent review are separate from the sole writer.
The 21 recovery methods share this setup; their parity, source-edge, identity,
cutover and no-rediscovery assertions remain unchanged. Each source state
transition is a normal forward commit after required actual checks/review.
Remote required checks run on a new exact pushed head only after local
completion; integrated-main observation precedes integration acceptance.
