---
title: "Common Authority Fixture Reinstantiation"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0009"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Common Authority Fixture Reinstantiation

## Overview

Execute [VAL-P02-009](../spec.md#success-criteria--verification-plan) through
[WORK-009](../plan.md#work-breakdown), using the registered form for this
new unique draft and retaining current authority fixture refusals.

## Inputs

- [Plan](../plan.md) and [registered form](../../../99.templates/templates/specs/task.template.md).
- Retained Task8 source metadata, local receipts and reviewed forward rollback.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-009 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | One bounded authority fixture repair | repo-tooling-engineer | frontmatter | PASS | accepted | [Fixture](#fixture-acceptance), [indices](#prior-index-acceptance) and [creation](#creation-proof) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-090 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Retained first-appearance source mismatch | Task8 creation metadata | FAIL | [Intake](#verification-summary) | rejected |
| EVD-P02-091 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Retained exact-input named controls and pinned hooks | Fixture `e4d0017c` with unchanged public dependencies/configs | PASS | [Fixture acceptance](#fixture-acceptance) | accepted |
| EVD-P02-092 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Prior actual draft, corrected ready and implementation indices/messages | Trees `127a63a6`, `5ce73430` and `350d3216` | PASS | [Prior indices](#prior-index-acceptance) | accepted |
| EVD-P02-093 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Observed prospective terminal completion and review | Isolated tree `7a6dbd45` at accepted implementation | PASS | [Terminal acceptance](#terminal-acceptance) | accepted |
| EVD-P02-094 | [VAL-P02-009](../spec.md#success-criteria--verification-plan) | WORK-009 | Actual committed registered-form creation | Parent `342a105e` to draft `8fe19c20` | PASS | [Creation proof](#creation-proof) | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan, Task and `tests/test_common_agents_document_routes.py`.
- **Forbidden Paths**: Production contracts, schemas, Registry, frozen Archive and completed historical evidence.
- **Approval Required**: Existing scoped normal delivery and reviewed rollback authority; conditional closing reflection requires fresh actual checks and separate review before commit.
- **Static Validation**: Actual first-appearance source; named routing/native refusals, pinned hooks, each actual staged/message; prospective completion/review then fresh actual closing checks. Full/affected execution stays NOT_RUN.
- **Live Validation**: DEFER — no runtime action requested.
- **Secret / Vault Handling**: Safe metadata only; no raw logs or private values.
- **Rollback Plan**: Reviewed forward correction or revert preserving all commits and receipts.
- **Evidence Location**: This Task and external ignored retention/validation receipts.

## Verification Summary

Task8's real first-appearance metadata is `C014` from completed Task0007,
not its registered form. CI refusal is a static owner prediction; hosted
jobs were cancelled without runner assignment or code execution, with cause
unconfirmed. Its original four commits, source bytes and local PASS receipts
remain historical evidence. This source closing candidate accepts the observed prior implementation
and prospective completion/review only. Its completed Work records prior
implementation acceptance. Fresh actual closing-index staged, completion,
message and independent final review remain NOT_RUN pending; all must PASS
before a normal closing commit under the explicit conditional permission.

### Creation proof

The existing Git copy flags observed `C016` from
`docs/99.templates/templates/specs/task.template.md` to this new Task in both
the cached draft and committed parent-to-draft diff. The source is the same
regular blob, the target was absent in the parent and its ID is unique.
The committed receipt `hy-p01-task9-c1-committed-creation.json` has SHA-256
`034ef72d05294f76bf8fa6e50ad05c33d8752ac0c780ed5c32e5998fa2e0f9c3`.
It records selected tool-stdout metadata; the full raw diff was not persisted.

### Prior index acceptance

Actual draft tree `127a63a62ae45181531d342fe0953407a45e2300` passed six fresh
canonical staged gates and the pinned configured draft message; separate
review accepted that exact input before the normal draft commit. The staged
receipt SHA-256 is
`767e42c0bafd939416df0a12d4bd71c736899a18faec966ed016374a2dc05d98`
and message receipt SHA-256 is
`9380f2ae170c1f95bdfcaa874e63f3e773a40c5002243193f315081ed566f9ba`.
These results belong to the prior draft input. The corrected ready tree
`5ce7343042c63b42e630060c00c86ab5428d5fdc` subsequently passed six fresh
staged gates and its configured message; independent final review preceded
the normal ready commit. Its staged receipt SHA-256 is
`cf1c0dca072c1120e0e00b7feea751c89c6879126e5c672cabc794f2180553b3`
and message receipt SHA-256 is
`452c71d0498a9f4cb34aa0b692592e0da431047f7e1887e8406ab44443fd5504`.
Implementation tree `350d32167b71420ac3f28b6f16ee1a5eaee7c9e8` subsequently
passed seven fresh actual staged gates, changed Task Markdown and its exact
configured message. Separate final receipt review accepted that input before
the normal implementation commit. Receipt SHA-256 values are respectively
`3a4a38ed9af9de694f8798f591bda5ae7f073a1072f318c02864f1d5e403b0f0`,
`29cabb1e0168b8ac6ac491df1a88a15b9d91073b49be0efe7fbc4d40b44a4147`
and `e0afa99e75ade5b0bd09df3fc2a8209b8d6cf82f0866c96b00cbbd0719b400c3`.
These observations accept the prior implementation, not this terminal input.

### Readiness

Finite four-path selection reports seven validators, no unmatched paths and
no validator execution. `hy-p01-task9-selection.json` has SHA-256
`93c0892a7cf2af05b452efcd95dc82f7ca3c424bc65044436b5b3f5596a86dc3`.
The first ready index passed five of six actual gates; Markdown rejected
the historical `FAIL` row's erroneous `accepted` disposition. The failed
receipt SHA-256 is
`74c8c044ce6132055d59bb375f1b80ec2e4a0b0a56184e89c3214846acc78a39`.
The owner requires `accepted` results to be `PASS`; this correction retains
the failed observation with `rejected`. The message was not checked, and
at correction time the ready checks and review remained pending. Their
later observed acceptance is recorded above.
The four-method manifest retains governance routing, unowned/retired route,
native invocation-control and dangling-root refusals; its SHA-256 is
`7e13588a823153383e59ca5c5e625d3d1fa72c7ced5d72fb1e7f2051186db2e5`.
Existing focused bounds are sixty seconds; canonical staged uses the owner's
1200-second bound. Pinned Ruff, scanner, Markdown and configured message
prerequisites remain unchanged. Prior pure fixture observations can support
the upcoming implementation only after exact source, configuration and
public-dependency identity proof with independent attribution. No fixture
check, full/affected execution or hosted acceptance is claimed here.

### Fixture acceptance

The restored fixture SHA-256 is
`e4d0017c2a456290034adb2960880fb55a150ca1245a0f5e909ba45b7fe0bae3`,
exactly the previously tested final input. All ten route mappings and
existing refusal assertions remain intact. It expects the published six-state
governance domain and gives the native positive its required metadata.
Independent review accepted finite proof
`hy-p01-task9-fixture-reuse-proof.json`, SHA-256
`c462667a840f70ffba0c69bbce6077da768a58ff91da85244d2b496321715d2a`.
It binds exact bytes/AST, four methods, imports/setup, public owner assets,
behavioral dependencies/configs and original raw streams. These four
controls do not consume Task/Spec/Plan corpus or Git history.

The earlier first two PASS results and corrected native/fourth PASS results
remain attributed to their original invocations; the native prerequisite
FAIL is retained separately. The exact-byte pinned Ruff/check-format/scanner
observations are also attributed to their original receipts. No test or
hook was rerun for this lane, and no historical binary digest is invented.
This accepts only the deterministic fixture input; it grants no new Task
index, lifecycle-history, hosted or integrated-main acceptance. Its later fresh Task Markdown, actual selected staged/message and final
review are recorded above. Full/affected stays NOT_RUN.

### Terminal acceptance

The ignored same-base/config prospective input
`7a6dbd451d7c073587c55dc01c90ab22c85ed352` passed independent semantic
review and SPEC0106-only completion. Its observed snapshot is
`f937cb6e0d126378654652150aa3f626d1ab3ea9031da355551fd95999f6e3f9`;
receipt SHA-256 is
`6b9ee1e29ef55b5da8813786dada729450247ce939b6e62f7303671e35887c72`.
Independent raw/structured evidence review accepted that prospective lane.
No proposal staged repeat was executed.

The user explicitly permitted normal completed-candidate reflection followed
by actual-index verification. These source bytes are a different input:
fresh canonical staged, SPEC0106 completion, configured closing message and
separate final actual-evidence review remain NOT_RUN pending. Every required
actual result must PASS before the normal closing commit; no prospective
result substitutes for that condition. Final actual index/commit receipts
remain external to avoid a self-OID loop. Hosted and integrated-main
acceptance remain pending separate observations.
