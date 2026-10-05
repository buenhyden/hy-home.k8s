---
title: "Sealed Source Revision Fixture"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
| WORK-006 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | Record the real frozen Registry, source and successor at the authenticated source revision | repo-tooling-engineer | frontmatter | PASS | accepted | [Implementation observations](#implementation-observations) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-060 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Hosted failure and exact named reproduction | Unchanged additive recovery fixture at P01 `c4c0a5f2…` | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-061 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Changed-input recovery checks and scoped hooks | Reviewed corrected standalone recovery fixture | PASS | [Implementation observations](#implementation-observations) | accepted |
| EVD-P02-062 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Actual-index staged/message and separate review | Observed draft, ready and implementation indexes; current closing index pending | PASS | [Validation boundaries](#validation-boundaries) | accepted |
| EVD-P02-063 | [VAL-P02-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Prospective terminal completion and independent review | Observed isolated terminal candidate, distinct from actual closing index | PASS | [Validation boundaries](#validation-boundaries) | accepted |

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
`ARCHIVE-MIGRATION-PARITY` was unexpectedly present. Actual outer rc was 1,
elapsed 0.902s; output and cleanup completed, source/index/refs stayed clean.
Safe RED receipt SHA-256 is
`b3e0260a8dda2d36358d401f14c3afd7d21dd370bcff38254dea6e85ab28b7cd`;
raw stderr SHA-256 is
`b744bf30b35081271b3ca97acf201236a61b3d6545b610429747a43b6bdf1871`.

The observed failing source commit contained only source bytes;
Registry was absent and successor was committed afterward. The existing
`historical_generation_registry` refuses the missing regular Registry blob
with `ARCHIVE-MIGRATION-PROFILE`, before disposition lifecycle checks.
The generation-9 path also requires the immediate replacement blob in that
same revision. Independent review confirmed both prerequisites. The minimum
repair uses existing `GitFixture.commit_many` with exact frozen Registry,
unchanged source and successor bytes, and binds recovery metadata to its
actual source blob. Historical projection needs no schema/template assets
here; no production fallback or refusal is changed. After sealing those
objects, only the temporary current Registry file is removed to preserve
the original standalone fixture's documented no-current-Registry context.

### Implementation observations

The first shared-setup candidate passed seven of ten executed methods;
three additive methods raised `REGISTRY_SCHEMA`, and the remaining eleven
methods and hooks were held. Materializing historical generation 9 in the
current fixture tree made the existing published loader correctly reject
that context. Its receipt SHA-256 is
`fdbdc209dceb1c337ef73461a231543fdc12bc441b75b774a2782cfd1c9a6177`;
the failing group stderr SHA-256 is
`dd5ddd301fa534b08c181da56138f5ce23c22cfd4c3711deaeb4a919428f8fd5`.
Independent review confirmed the current fixture's absent-Registry branch
and the historical reader's committed-Registry prerequisite are distinct.

The corrected fixture SHA-256 is
`4585a688f865f1b26cc671ccb2c39c97aa5e5b4c941612c455effb92b43f2f5c`.
All twenty-one explicitly named recovery methods passed in five groups,
each under a 60-second bound, with complete streams and cleanup. The exact
manifest SHA-256 is
`b9e46a7940be7a47cae8132794e5712a6613124942d91633a8fc441e247d5ead`;
the completed focused receipt SHA-256 is
`3bb7d4088f8b00cd2748c719734a29253b022aedf77d3da4d2952c85430d6f29`.
Pinned Ruff check/format and detect-secrets passed on an exact-byte
disposable copy; its bytes/configs stayed unchanged and cleanup completed.
The hook receipt SHA-256 is
`242457efbb982c09ecffa5726701ae1e35fea6e7345ecf017f419e96b04c5d22`.
All source/index/ref identities stayed stable during these checks. Existing
test assertions, source/successor literals, helpers and production owners
remain unchanged. This focused acceptance does not accept the still-pending
actual implementation index or whole WORK-006.

### Validation boundaries

The actual draft index passed all six selected canonical staged gates,
the exact configured message check and separate independent review. Its
staged raw stdout SHA-256 is
`633757622d6c715f375839db60d4684bfaf1712090fcd45053d37519417f5b0f`;
the structured receipt SHA-256 is
`8d8a0ccfcbe8a7205b0600241a3c7c8a79b107858b93735cf6d97871725aca79`.
The actual message SHA-256 is
`59e1ab29bca9791458a4f3662fba1f42865fb0eb49f7c50b267adff75f47ddf6`;
its receipt SHA-256 is
`734855504b4c6a8ab0e4eb4c47a07786f52b3872d3339cb3b1cdc49fc87238cb`.
All streams and cleanup completed, with unchanged input identities.

Readiness inspected the finite four-path selector without running affected
validation: seven validators selected, no unmatched path. The exact 21 named
recovery methods are recorded in an external manifest. Existing pinned hooks
and canonical runner prerequisites are available from the prior actual checks.
An unsupported selection-only attempt through `qa.py affected` returned usage
without executing a validator; the subsequent direct selector receipt is the
observed readiness result. The ready index subsequently passed six fresh
canonical staged gates, its configured message and separate independent review.
Ready staged receipt SHA-256 is
`bbedcf2b46dd863484268d7b11e655d4dbfef6c05bd5df26e2fe7533c3c0d7f6`;
raw stdout SHA-256 is
`afd7284433c8c73eaa64acfbb0fd138ecc8813f313e74d5a6bee3d9e3c2625ac`.
Its exact message SHA-256 is
`75c73116b3b6108181d1456ac01161b727e3ba46d2d8b5740a70f4aa35312380`;
message receipt SHA-256 is
`a2fcf4c987d38bd2e2be67f8bee4bc8f3c1572799fa2749d07732c78c47b40ad`.
The actual implementation index subsequently passed all seven fresh canonical
staged gates, pinned Task Markdown, its exact configured message and separate
final independent review. Staged receipt SHA-256 is
`cfa75d6fcc5f0482b5beea9578b6c9151ccf4133ddd2bf10055a0b260fdac652`;
raw stdout SHA-256 is
`80328d0efdd7d92217def89cb41829ba546fa7973d753a266f09fe734036fb02`.
The exact implementation message SHA-256 is
`07512eb6a04d99731a59ef1f3a9f709822e51c470c5fb5dded1c6e3026faeef9`;
its receipt SHA-256 is
`acbd3c9b664d5ca9053c0f25a543a0ee827f7c15b14a5cc7ac0fb6e67b3a6dec`.
The Task Markdown receipt SHA-256 is
`4d56e66379df021f43a73ecaa0334cef646f14b3cfd66cae2f60dcb220df5da4`.
All streams and cleanup completed with stable source/index/ref identities.
EVD-P02-062 acceptance covers only these observed source indexes.

The nonauthoritative isolated terminal proposal under ignored
`.worktrees/proposal/p01-task6-c4-terminal` passed SPEC-0106-only completion
and separate independent review. Actual completion snapshot SHA-256 is
`eb063ea60cb4f0647e3d3e1ea8cbc7824f03510481fc0b9e8e9e8fefd7ca015b`;
raw stdout SHA-256 is
`b8a0952ef424b0a2f9111eba67c3866c1f020ecdbfda2b88965432024dc24c02`;
structured receipt SHA-256 is
`5365448842b6a2be0597a4bb1ce50ffc4517ac077dc01d5c6ccf109c12d48f64`.
The clone and original input identities remained stable, streams and cleanup
completed, and no proposal staged run was required or performed.

The user's explicit conditional reflection permission allows this normal
source closing candidate after prospective acceptance. Its fresh actual
staged, SPEC-0106 completion, configured message and separate final review
remain NOT_RUN until observed; every one must pass before the closing commit.
EVD-P02-063 accepts the prospective lane only. Actual closing receipts and
the closing commit identity stay external, avoiding a source self-OID loop.
Quality and independent review are separate from the sole writer.
The 21 recovery methods share this setup; their parity, source-edge, identity,
cutover and no-rediscovery assertions remain unchanged. Each source state
transition is a normal forward commit after required actual checks/review.
Remote required checks run on a new exact pushed head only after local
completion; integrated-main observation precedes integration acceptance.
