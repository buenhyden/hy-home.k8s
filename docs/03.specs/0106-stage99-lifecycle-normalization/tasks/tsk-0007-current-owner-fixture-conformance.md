---
title: "Current Owner Fixture Conformance"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0007"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Current Owner Fixture Conformance

## Overview

This necessary bounded delivery follow-up owns
[VAL-P02-007](../spec.md#success-criteria--verification-plan) and
[WORK-007](../plan.md#work-breakdown). Three observed failures are stale
current-owner fixture expectations. A separate archive process-budget failure
requires causal accounting before a correction is proposed. Completed Tasks
and their accepted evidence remain historical inputs.

## Inputs

- The user's explicit normal unit-commit, push and merge instruction covers
  necessary reversible current-contract fixture repairs. Independent scope
  review confirms two test consumers plus this Spec, Plan and Task.
- [Plan](../plan.md), [registered Task form](../../../99.templates/templates/specs/task.template.md)
  and [quality policy](../../../../.agents/governance/quality.md).
- Clean P01 input `9264b3a9042a291e6cfe17dd0a28a7bc2b61a5e3`;
  automatic CI run `37339062037`, QA job `111861178282`. No retry or cancel.
- Published governance lifecycle and navigation section declarations; the
  existing corpus-based archive subprocess budget and its historical owner.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-007 | [VAL-P02-007](../spec.md#success-criteria--verification-plan) | Align current-owner fixture expectations and resolve measured archive process accounting | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Observed intake](#observed-intake) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-070 | [VAL-P02-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Hosted failure and exact named reproductions | Clean final Task0006 P01 input | FAIL | [Observed intake](#observed-intake) | pending |
| EVD-P02-071 | [VAL-P02-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Causal accounting, changed-input controls and scoped hooks | Reviewed exact two-file fixture input | PASS | [Implementation observations](#implementation-observations) | accepted |
| EVD-P02-072 | [VAL-P02-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Actual-index staged/message and independent review | Observed draft and ready indexes; current implementation index pending | PASS | [Validation boundaries](#validation-boundaries) | accepted |
| EVD-P02-073 | [VAL-P02-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Prospective terminal completion and independent review | Not prepared | NOT_RUN | [Validation boundaries](#validation-boundaries) | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: This Spec, Plan, Task, `tests/test_archive_validation.py` and `tests/test_common_agents_archive_routes.py`; one P01 writer.
- **Forbidden Paths**: Production contracts, Registry/schema/templates, frozen Archive, completed Tasks/evidence, hosted configuration, private values and unrelated files.
- **Approval Required**: Existing necessary scoped fixture-repair and normal delivery authority applies. A process-budget correction requires proven fixed corpus cost and independent review; no limit weakening or production regression repair is authorized. Conditional terminal reflection requires fresh actual checks and separate review before commit.
- **Static Validation**: Preserve observed RED. Run explicit changed-input named controls, scoped pinned hooks and each actual-index staged/message with independent review. Prospective completion/review precedes fresh actual closing checks. Local full and affected execution remain NOT_RUN.
- **Live Validation**: DEFER — no cluster or runtime action requested.
- **Secret / Vault Handling**: Safe path, rule and aggregate count metadata only; no raw CI payload, argument values or private contents.
- **Rollback Plan**: Reviewed forward correction or revert; no history rewrite, force, branch deletion, cleanup or local main mutation.
- **Evidence Location**: This Task and external safe receipts; absolute operational roots/argv and own commit identity stay outside tracked source.

## Verification Summary

### Observed intake

The observed failing hosted complement gate is `unit-tests`; the capped
failure preview is not an exhaustive failure inventory. Four exact named
methods were reproduced once, independently reviewed and preserved in a
safe receipt with SHA-256
`ec6871c91ecf88302d7b2df121ec83bae424951406ab799628a16722e3e801fc`.
No source, index or reference changed during diagnosis.

`ArchiveTransitionLinkTest.test_terminal_governance_owners_are_derived_from_stage_owners`
expects only active owners, while the published governance current states are
active and deprecated. Both `SpecIndexNavigationTest` payloads in
`test_member_listing_with_copied_status_is_rejected` and
`test_package_folder_rows_pass` use Document Index, while the registered
section is Structure. The minimum fixture correction retains owner membership
and all malformed-navigation rejection assertions.

`ArchiveValidationTest.test_repository_archive_git_snapshot_is_bounded_and_under_sixty_seconds`
fails at 287 Git calls versus a branch budget of 260. Report validity and
fallback batching assertions pass; the final time assertion is not reached.
A separate accounting invocation reports a valid archive, zero retired-form
fallback batches and 11.869 seconds, with safe receipt SHA-256
`70bbe512cd6c021415439e8d7d60ab0e23a9c66a3e812def8d2b9d09218993ce`.
This is diagnostic evidence, not authority to raise the process cap.
Causal comparison and independent review subsequently established the precise
cost. The immutable budget-owner input used 260 calls, while pre-P01 main used
287, matching the final P01 input. One memoized historical Registry sequence
costs three calls; eight authenticated historical successor sequences cost
24. All remaining owner/verb counts exactly match the earlier 260. Both
inputs remain valid with zero fallback batches and complete in under 60
seconds. Baseline composite receipt SHA-256 is
`a806345dd311e410979451fcd4d98b4cea2831f831b36c5c1dd3ac6cdbb1f5a7`;
the final owner-chain receipt SHA-256 is
`9a51ef4baf7edea505caa82b8ea0dfa4e6f9fc65653acb315e5c487cba931ab2`.
Independent review accepts a fixture-only finite budget correction to 287,
preserving report validity, fallback batching, detached adjustment and the
sixty-second limit. This neither makes the bound dynamic nor asserts constant
cost as the historical corpus grows. Production behavior is unchanged.

### Implementation observations

The archive test input SHA-256 is
`fbac7bcd78848358b1030d3e5e67a9df5063deb92badf69cdd33e44de9a75e37`;
the navigation test input SHA-256 is
`7b681b7c6d2e12139b3d92943cd858be16f045203b82bff80b705b5e19e8dd16`.
The four explicit changed-input methods passed separately under 60-second
bounds. Their actual qualified argv, complete outputs and stable source,
index and reference identities are bound by focused receipt SHA-256
`066db789657283f79f7f918e8c642661ef8f16e3faaf752ffc3c9e3ffd9057c3`.
Pinned Ruff check/format and detect-secrets passed on an exact-byte disposable
copy with unchanged configurations and no formatting delta; hook receipt
SHA-256 is
`41946c74d17f5e28aac514e4e3f046444e509d167e26e8faa55edc8e70031b1f`.
Separate independent read-only review verified the raw results and source
hashes. EVD-P02-071 accepts this focused input only.

Governance expectations now load real published declarations and retain
nonempty owner, exact current-state, profile, authored mode, owner identity
and state membership assertions. Both navigation payloads use Structure;
the copied-status/tree/depth refusals and valid-folder control are unchanged.
The finite budget is 287 with the measured accounting documented beside it;
validity, fallback batching, detached adjustment and time assertions remain
unchanged. No production owner or completed evidence is modified.

### Validation boundaries

The actual draft index passed six fresh canonical staged gates, configured
message validation and separate final independent review. All output and
cleanup completed with stable source/index/reference identities. Staged
receipt SHA-256 is
`331e369ad567bd730d72782a5973b0f7554d01388f5743ff4cb05ec9518d0f01`;
raw stdout SHA-256 is
`1b83e3645fb29bd825307ecf4efd3bd555c9b3422fec5e4cfbcec15da7b3530b`;
the exact configured message receipt SHA-256 is
`7c6e575e2422b67d9c94f54d7b2e248ba3384e45113a179cefdd4250c2b96212`.
The actual ready index subsequently passed six fresh canonical staged gates,
its exact configured message and separate final independent review. Its
staged receipt SHA-256 is
`b1b4538b094d1e30440a7889ad348184a5dac5b2ad0ba6fb48f3c713105369a4`;
raw stdout SHA-256 is
`11ecbceebf55a34a1a172fdd53dd907ddd91d1f6caeebf524fe4e0a49d1a8244`;
the configured message receipt SHA-256 is
`3acf2df8eebdf8a05505c7f4651530935a6a3ccabd967c9abf708755b6a60736`.
All output and cleanup completed with stable inputs. EVD-P02-072 accepts
only these observed draft and ready indexes; current implementation-index
staged/message and separate final review remain pending.

Readiness selects the finite five-path prospective scope through the canonical
selector: seven validators and no unmatched paths, without affected execution.
Its safe receipt SHA-256 is
`6b9d01844b52f3fc3fec4b770208a27b27734242b0cf13c70d26a8cc9afeebbf`.
The four explicitly named intake methods form the observed GREEN set;
the navigation rejection and valid-folder case are retained controls. Existing
pinned hooks and the canonical runner prerequisites come from prior actual
checks with unchanged configurations. Focused commands retain a 60-second
bound and canonical staged retains its existing runner limits.

The focused acceptance does not accept the current implementation index or
whole WORK-007. Each legal source index is separately reviewed and checked
before its normal commit. Prospective terminal completion/review is distinct
from the reflected source's fresh staged/completion/message and final review.
Hosted exact-head checks and integrated-main observations remain separate
required delivery evidence; prior local acceptance is preserved.
