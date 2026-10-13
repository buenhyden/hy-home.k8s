---
title: "SDLC Document Sync and Remaining v9 Gaps"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0113-TSK-0001"
parent_ids: ["SPEC-0113-PLAN-0001"]
---

# Task: SDLC Document Sync and Remaining v9 Gaps

## Overview

Execute the seven work units of the [Plan](../plan.md) for
[SPEC-0113](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0113](../spec.md) and its [Plan](../plan.md).
- Operator request on 2026-10-13: check that requirements, architecture
  and Spec documents follow the revisions, and review and proceed with F22,
  F02, F18, F05 and F39; the operator chose the section reorder for F02.
- Main `86daf8158f0b03875b1ffa47f2cd86c4914ed391`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | Correct stale requirements, architecture and Spec text | platform | completed | PASS | EVD-012, EVD-015 |
| WORK-002 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | Frozen-exclusion cross-check test and fix recipe | platform | completed | PASS | EVD-011 |
| WORK-003 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | Four F05 claim statuses in the Stage 99 README | platform | completed | PASS | EVD-010 |
| WORK-004 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | F18 evidence correction | platform | completed | PASS | EVD-008 |
| WORK-005 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | Remove the stale `.hadolint.yaml` route | platform | completed | PASS | EVD-007 |
| WORK-006 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | `AGENTS.md` common and Codex-only blocks | platform | completed | PASS | EVD-009 |
| WORK-007 | [VAL-SYNC-007](../spec.md#success-criteria--verification-plan) | Bound the memory store Git call with a timeout | platform | completed | PASS | EVD-014 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | WORK-004 commit index | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | WORK-005 commit index | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | WORK-006 commit index | NOT_RUN | Pending | yes | none |
| EVD-007 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Focused checks and staged QA | Before: `select-affected-surfaces.py` routed a reintroduced `.hadolint.yaml` silently to `agent-governance`, `ci-python-contract` and `repository-quality` although the file was deleted in `1014bba7` and no other consumer names it. After removing the exact route the same path reports `SURFACE-PATH-UNMATCHED`, so a reintroduction fails closed; 88 registry, scope and consumer tests passed. `qa.py staged` on the WORK-005 index passed | PASS | This Task; WORK-005 commit | yes | EVD-005 |
| EVD-008 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Focused checks and staged QA | Appended EVD-013 to the SPEC-0110 Task stating that `greeting` and `label` success in its EVD-011 is notification automation, not QA evidence, and naming `style-pr`, `ci-summary` and local `qa.py staged` as the QA results; EVD-011 stays as history. `qa.py staged` on the WORK-004 index passed | PASS | This Task; WORK-004 commit | yes | EVD-004 |
| EVD-009 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | WORK-006 | Focused checks and staged QA | `AGENTS.md` now reads the common lifecycle and `RTK.md` first, then the common owner list, then a block labelled 'Codex-only provider reads' with `.codex/provider.md` and `.codex/CODEX.md`; line texts and the validated reference set are unchanged (24 lines). Moving the Codex reads into a separate native entry was not done: Codex documents load at most one instruction file per directory and no verified loader exists for `.codex/CODEX.md`, and the operator chose this reorder. `validate-agent-governance.py` and the profile validator passed, and 129 governance, consumer and language tests passed. `qa.py staged` on the WORK-006 index passed | PASS | This Task; WORK-006 commit | yes | EVD-006 |
| EVD-010 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Focused checks and staged QA | The Stage 99 README (v0.12.0) now states each `WGOV-CORE / 3.0.0` claim separately: common approval confirmed (Registry `approval_ref`, SPEC-0105 Task EVD-033); original-source verification confirmed only on the Project-Template input and not re-verified here, with its raw comparison data in the Git-ignored `_workspace/residual-controls/`; local acceptance complete for C07 only, with C04 and C08 applicability and full-core adoption pending; four-repository adoption unobserved and not claimed. `stage: candidate` is unchanged. Profile validator passed; `qa.py staged` on the WORK-003 index passed | PASS | This Task; WORK-003 commit | yes | EVD-003 |
| EVD-011 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused checks and staged QA | New `test_frozen_exclusions_follow_the_registry` compares the sealed migration names in the pre-commit `&frozen_archive` exclusion with the Registry `archive/migration` `path_pattern`, and the markdownlint Archive ignores with the Registry retention classes and archive profile roots. It passed on the repository and failed on two tampered copies (one migration line removed from the exclusion; the `resolved/` ignore removed). `scripts/README.md` (v0.10.0) now separates fixing from checking with a copyable `pre-commit run <hook-id> --hook-stage manual --files <reviewed-path>...` recipe. The exclusion itself is unchanged. `qa.py staged` on the WORK-002 index passed | PASS | This Task; WORK-002 commit | yes | EVD-002 |
| EVD-012 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Focused checks and staged QA | Corrected the audited stale text. SPEC-0109 (v0.3.0) no longer calls itself a pre-implementation draft: its Overview, limits, interface and FR-0022 row reflect the delivered store, and it links AD-0006 back. AD-0006 (v2.2.0) describes the memory store in its checkpoint section, names SPEC-0109 in the FR-0022 row and lists SPEC-0108 to SPEC-0113. REQ-0003 (v2.1.0, updated 2026-10-13) gains a Traceability paragraph for SPEC-0108 to SPEC-0113 and the SPEC-0107 links missing from FR-0001, FR-0005, FR-0024, FR-0026, FR-0027 and IF-0001. SPEC-0106 gains a dated successor note on the retired writer, SPEC-0108 VAL-TSKSUM-002 a point-in-time note, and ADR-0036 a sentence separating the SPEC-0109 store from the retired memory structure. The SPEC-0108 to SPEC-0112 Tasks each gain a delivery row for pull requests #140 to #142. The first staged run failed `BODY-LINK-RECIPROCAL` until SPEC-0109 linked AD-0006; the rerun passed | PASS | This Task; WORK-001 commit | yes | EVD-001 |
| EVD-013 | [VAL-SYNC-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Focused checks and staged QA | WORK-007 commit index | NOT_RUN | Pending | yes | none |
| EVD-014 | [VAL-SYNC-007](../spec.md#success-criteria--verification-plan) | WORK-007 | Focused checks and staged QA | The full suite on main `86daf815` (1405 tests) failed `test_subprocess_run_calls_declare_a_timeout` on `scripts/workspace_memory.py:88`, a SPEC-0109 regression that its staged QA did not select; the same module at base `57f44c44` has no such file. The Git call now has `timeout=GIT_TIMEOUT_SECONDS` (10), and `TimeoutExpired` reports `MEMORY_UNAVAILABLE: Git did not answer in time`. The new `test_git_timeout_reports_the_store_unavailable` errored with an uncaught `TimeoutExpired` against the previous module and passes now; 12 store tests and the tooling timeout test passed. The other 13 suite failures also fail at base `57f44c44` and are outside this package. `qa.py staged` on the WORK-007 index passed | PASS | This Task; WORK-007 commit | yes | EVD-013 |
| EVD-015 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent review and full suite | An independent read-only review of `86daf815..9397d6f6` found no HIGH issue and confirmed the merge SHAs, F05 claim sources, memory wording, the AGENTS.md validator effect and the timeout mapping. Its findings were fixed in `95bb89eb`: REQ-0003 no longer calls the completed SPEC-0107 a draft; the SPEC-0113 Plan and Task count seven units; the F22 test also compares the two harness globs between pre-commit and markdownlint (it passed on the repository and failed on two tampered copies); SPEC-0109 names its body rewrite a revision rather than a note and drops 'once approved'; the `workspace_memory.py` limits comment says accepted; the SPEC-0108 to SPEC-0112 Task summaries and the SPEC-0108 Plan gain dated notes closing the merge handoff and the pending README risk, with patch version bumps. The SPEC-0109 Overview, limits and interface text was rewritten in place, beyond the notes-only allowance named below; Git keeps the earlier text. The full suite on `9397d6f6` ran 1407 tests with 12 failures and 1 error: 12 match failures on main `86daf815`, and `test_pre_effect_group_interrupt_reuses_deadline_and_finishes_tree` passed three times alone (load-sensitive timing). `qa.py staged` on the review-fix index passed | PASS | This Task; review-fix commit | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-012, EVD-015 | Accept the document sync and the review fixes; the SPEC-0109 in-place rewrite is recorded | platform |
| [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-011 | Accept the Registry cross-check and the explicit fix recipe | platform |
| [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-010 | Accept the four separate claim statuses | platform |
| [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Accept the correction record | platform |
| [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Accept the route removal; reintroduction now fails closed | platform |
| [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | accepted | EVD-009 | Accept the common and Codex-only blocks; a native split stays unverified and out of scope | platform |
| [VAL-SYNC-007](../spec.md#success-criteria--verification-plan) | accepted | EVD-014 | Accept the bounded Git call; 13 earlier suite failures stay out of scope | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package; `docs/03.specs/README.md`;
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`;
  `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`;
  `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`;
  the SPEC-0106, SPEC-0108, SPEC-0109, SPEC-0110, SPEC-0111 and SPEC-0112
  package documents (notes and appended evidence only);
  `docs/99.templates/README.md`; `scripts/README.md`;
  `scripts/validation/registry.json`; `AGENTS.md`;
  `tests/test_validation_tooling_ownership.py`.
- **Forbidden Paths**: `.pre-commit-config.yaml` exclusion removal,
  `docs/99.templates/registry.json` and schemas, validators, workflows,
  frozen Archive payloads, live cluster, Vault and secret material.
- **Approval Required**: the operator approved SPEC-0113 and its Plan for
  implementation on 2026-10-13 after reviewing the draft at `535d8c11`.
  After the full test run the operator added WORK-007 the same day, which
  extends the allowed paths to `scripts/workspace_memory.py` and
  `tests/test_workspace_memory.py`. Push, pull request and merge await the
  operator; this Task does not infer them.
- **Static Validation**: focused tests, document validators and staged QA
  from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

All seven work units are complete and all seven criteria are accepted.
Every commit passed `qa.py staged` from the documented validation
environment, and one independent review covered the whole branch; its
findings were fixed in `95bb89eb` (EVD-015).

Limitations: the F02 split is a reorder inside one `AGENTS.md`, because no
verified Codex loader reads a second instruction file in the same directory;
WGOV-CORE four-repository adoption is unobserved and local acceptance covers
C07 only; hosted CI, push and pull request are not executed here. Residual
risk: 12 suite failures that already fail on main `86daf815` stay outside
this package, and one timing test fails only under full-suite load. Rollback:
forward revert of the package commits. Next owner: the operator for push,
pull request and merge.
