---
title: "Cut Over Archive Reappraisal and Verifiable Sources"
version: "0.3.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0085-TSK-0002"
---

# Task: Cut Over Archive Reappraisal and Verifiable Sources

## Overview

This Task owns WP-003 and WP-004 of the [Implementation Plan](../plan.md): the
acceptance of ADR-0040 with its registry, index, validator, and test cutover,
and the envelope verification against the default branch. It closes with
focused, staged, and full evidence.

## Inputs

- [SPEC-0085](../spec.md) and its [Implementation Plan](../plan.md).
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md),
  which the request owner approved as written on 2026-09-17, together with
  current Task, Spec, and decision documents as the allowed Decision kinds.
- The survey in
  [SPEC-0085-TSK-0001](tsk-0001-propose-archive-reappraisal-and-document-standards.md).

## Task Table

| ID       | Upstream criterion | Work item                                                                          | Owner    | Status | Result       | Evidence                |
| -------- | ------------------ | ---------------------------------------------------------------------------------- | -------- | ------ | ------------ | ----------------------- |
| WORK-001 | VAL-ARS-009 | Accept ADR-0040, supersede ADR-0039, amend REQ-0003-FR-0020, activate this package | platform | Done | ADR-0040 `accepted` with `supersedes`; ADR-0039 `superseded` with `superseded_by` and a dated note; REQ-0003-FR-0020 amended; Spec and Plan `active` | Lifecycle gate PASS in quick QA |
| WORK-002 | VAL-ARS-004 | Registry assessment contract and removal transition, RED then GREEN | platform | Done | `archive_assessment` contract, schema, loader, and diagnostics; removal transition in the lifecycle gate | RED 23 new-module errors and 9 lifecycle failures, then GREEN |
| WORK-003 | VAL-ARS-005 | Treat a `git-history-only` unit as available in Git, not as a missing payload | platform | Done | Parity and cutover re-verification skip a removed unit's payload but keep its envelope check; the index keeps its catalog link | Archive contract tests |
| WORK-004 | VAL-ARS-006 | Availability and assessment rule in the citation table | platform | Done | Two ordered rules before the Incident exemption; the link, archive, and cutover gates pass the parsed table | Citation decision and reappraisal tests |
| WORK-005 | VAL-ARS-007 | Reject every `purged` row | platform | Done | A `purged` row fails as reserved | Reappraisal tests |
| WORK-006 | VAL-ARS-008 | Default branch, object-format length, and Git object fixtures | platform | Done | Reachability resolves the registry's default branch (remote-tracking ref preferred, local branch otherwise; never `HEAD`) and fails closed on an unresolvable branch or a shallow clone; the catalog grammar accepts sha1 (40) and sha256 (64) object-id lengths; regression fixtures cover a missing object, an unreachable commit, wrong type in both directions, a mode change, a symlink change, a missing native member, and an empty source tree | RED 4 failures/1 error, then GREEN in `tests.test_archive_catalog_reverification` and `tests.test_archive_dispositions`; commit `11664e49` |
| WORK-007 | VAL-ARS-012 | Staged and full evidence | platform | Done | Staged profile PASS on the WORK-006 commit; full profile run on the final tree | QA results below |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/contracts/`, `docs/98.archive/README.md` outside existing
  catalog rows, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `docs/02.architecture/decisions/`, this package, `scripts/archive_*.py`,
  `scripts/document_*.py`, `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`, `scripts/run-archive-contract-tests.py`,
  and `tests/`.
- **Forbidden Paths**: every retained body, sealed record, ledger, and existing
  catalog row; `gitops/`; secrets and private configuration.
- **Approval Required**: WORK-001 needs the request owner's approval of the
  written ADR-0040. Removing or reappraising a real unit is not approved. Push,
  pull request, and merge are not approved.
- **Static Validation**: focused tests per work item, the quick profile on the
  working tree, the staged profile per logical commit, and one full profile on
  the final tree.
- **Live Validation**: not run. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: no secret, credential, or private configuration
  is read or printed. Fixtures use synthetic content only.
- **Rollback Plan**: revert the cutover commits together; no frozen byte or
  catalog row changes, so a revert restores ADR-0039 enforcement.
- **Evidence Location**: this Task record.

## Verification Summary

WORK-001 through WORK-005 are committed at `5d382767`.

- **targeted**: `python3 -m unittest tests.test_archive_reappraisal` failed with
  23 errors before the implementation and passed after it;
  `tests.test_archive_disposition_lifecycle` failed 9 of 11 new removal cases
  before the lifecycle change and passed all 39 after it.
- **affected suites**: 263 tests across the archive validation, cutover, link
  boundary, lifecycle cutover, route, and historical-proof modules. With the
  registry change unstaged, 25 new failures came from
  `ARCHIVE-MIGRATION-STAGED-DRIFT`, the index/worktree registry guard. After
  staging, one failure remained,
  `test_repository_archive_git_snapshot_is_bounded_and_under_sixty_seconds`, which
  also fails on the pre-change commit `cce56df9` in an isolated worktree and is
  a local timing limit, not a regression of this change.
- **quick** (`python3 scripts/qa.py quick`, working tree): first
  `archive-contract-tests` and `document-lifecycle` failed, because the
  assessment span parser assumed the table directly follows its heading and a
  frozen-parser test called the parsers without the registry. Both were fixed
  with new regression tests; the rerun returned 13 PASS.
- A shell wait on an interactive `rm` alias stalled one run; the edits it
  skipped were re-applied and re-tested.

WORK-006 is committed at `11664e49`.

- **targeted**: `python3 -m unittest tests.test_archive_catalog_reverification
  tests.test_archive_dispositions` failed 4 (3 failures, 1 error) before the
  implementation — an off-default-branch commit, an unresolvable default
  branch, and a shallow clone each passed when they must not, and a 64-hex-digit
  commit was rejected — and passed all 40 after it. The mode-change,
  symlink-change, missing-native-member, wrong-type (both directions), and
  empty-source-tree fixtures already passed before the change; they are added
  as regression locks, not RED-then-GREEN fixes.
- **affected suites**: `tests.test_archive_validation`, `tests.test_archive_cutover`,
  `tests.test_document_lifecycle_migration`, `tests.test_archive_registry_contract`,
  and `tests.test_archive_recovery` (214 tests) return the identical set of 25
  pre-existing failures (12 failures, 13 errors, all rooted in
  `RECOVERY-MIGRATION-TARGET` against
  `docs/98.archive/migrations/0004-document-authority-convergence.md`) with the
  WORK-006 commit staged and with it stashed out, confirmed by a byte-for-byte
  diff of both failing-test-name lists. This defect predates this branch (it
  reproduces from a clean `24659ba3` checkout), sits outside this Task's
  Allowed Paths (a sealed migration ledger), and is out of scope for VAL-ARS-008;
  it is reported to the next owner rather than fixed here.
- **staged** (`python3 scripts/qa.py staged` on the WORK-006 index): 8 of 8
  gates PASS (`agent-governance`, `archive-contract-tests`, `gitops-structure`,
  `infrastructure-contracts`, `k8s-manifests`, `policy-gates`,
  `repository-quality`, `secret-handling`).
- **full** (`python3 scripts/qa.py full`, final tree, commit `11664e49`): 20 of
  23 gates PASS. `archive-contract-tests` (the narrow archive/lifecycle/link
  regression gate this Task's Allowed Paths own) PASSES. Three gates FAIL:
  - `unit-tests` (`python3 -m unittest discover -s tests -t .`): the same
    previously-known local-only failures (2 secret-scan tests with no
    `gitleaks` locally, `test_file_reader_rejects_changes_during_read`,
    `test_escaped_descendant_is_failed_without_post_reap_group_signal`,
    `test_equal_size_same_inode_content_restore_fails_closed`, and the
    `..._under_sixty_seconds` timing test) plus the pre-existing
    `RECOVERY-MIGRATION-TARGET` cascade reported above. None of these change
    between the WORK-006 commit and its parent.
  - `archive-cutover` (`python3 scripts/archive_cutover.py --root .`): PASSES
    with only `ARCHIVE-SECRET-CLASSIFIER-UNAVAILABLE` (no `gitleaks` locally,
    same local-only cause as the two `unit-tests` secret-scan cases) when run
    from an isolated `git worktree add` checkout of either `24659ba3` (before
    WORK-006) or `11664e49` (after it) — proving no regression. Run in place
    inside this agent's provisioned worktree, it additionally reports
    `ARCHIVE-EVIDENCE-COUNT`, `RECOVERY-MIGRATION-TARGET`, and eight
    `ARCHIVE-SOURCE-OWNERSHIP` diagnostics that do not reproduce in the
    isolated checkout of the same commit, that involve a pure, environment-
    independent lookup (`_source_commit`) and byte-identical `docs/98.archive`
    content (confirmed with `diff -rq`) between the two locations, and that
    also do not depend on this Task's new `resolve_default_branch` /
    `is_shallow_repository` functions (confirmed identical outputs in both
    locations). This is recorded as an unresolved, worktree-runtime-specific
    artifact rather than a repository or VAL-ARS-008 defect, and is reported to
    the next owner rather than fixed here.
  - `pre-commit` (`pre-commit run --all-files --hook-stage manual`): reports
    "required tool unavailable" in this environment, a tool-availability gap
    rather than a finding.

Hosted CI and live results are not run in this round.

Because the `unit-tests` and (in place) `archive-cutover` gates do not cleanly
pass on this worktree for reasons demonstrated above to be pre-existing and
environment-specific rather than caused by WORK-006, this Task does not itself
flip [SPEC-0085](../spec.md) or its [Plan](../plan.md) to `done`; their
completion criterion of "the final full profile passes on the final tree" is
not honestly met from this worktree, and closing them is left to the request
owner with this evidence.

### Handoff

- **Snapshot**: branch `feat/spec-0085-default-branch-envelope`, diverged from
  `main` at `24659ba3`; WORK-006 committed at `11664e49`.
- **Approval boundary in force**: this Task's own boundaries above; no push,
  pull request, merge, live cluster, or credential action was taken or is
  authorized.
- **Reviewer identity and disposition**: self-checked only (RED/GREEN evidence
  and staged/full QA above); no independent code review has run.
- **Rollback**: `git revert 11664e49` on this branch restores the pre-WORK-006
  `HEAD` ancestry check and 40-hex-only commit grammar; no frozen byte, sealed
  record, or catalog row changed.
- **Residual risk**: the pre-existing `RECOVERY-MIGRATION-TARGET` cascade and
  the worktree-runtime `archive-cutover` anomaly documented above; neither is
  in this Task's Allowed Paths.
- **Next owner**: `quality-engineer` for both residual-risk items (live
  re-verification of the `archive-cutover` anomaly and disposition of the
  `RECOVERY-MIGRATION-TARGET` cascade), and the request owner for the
  Spec/Plan `done` decision this Task leaves open.

## Traceability

### Lifecycle Traceability

| Criterion / work item                 | Result       | Evidence                |
| ------------------------------------- | ------------ | ----------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done | Lifecycle gate PASS in quick QA |
| [WORK-002](../plan.md#work-breakdown) | Done | RED 23 new-module errors and 9 lifecycle failures, then GREEN |
| [WORK-003](../plan.md#work-breakdown) | Done | Archive contract tests |
| [WORK-004](../plan.md#work-breakdown) | Done | Citation decision and reappraisal tests |
| [WORK-005](../plan.md#work-breakdown) | Done | Reappraisal tests |
| [WORK-006](../plan.md#work-breakdown) | Done | RED 4 (3 failures, 1 error), then GREEN in Git fixture tests |
| [WORK-007](../plan.md#work-breakdown) | Done | Staged 8/8 PASS; full profile below |
