---
title: "Agent Governance and Quality Gate Consolidation Implementation Plan"
version: "2.2.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-08"
layer: "specs"
artifact_id: "SPEC-0072-PLAN-0001"
---

# Agent Governance and Quality Gate Consolidation Implementation Plan

## Overview

Execute the approved [Spec](spec.md) with Superpowers writing-plans and
executing-plans. The Task owns state and results; the ordered work below owns
implementation and verification. The later user instruction selects local
main integration and task-owned branch/worktree cleanup only after the
completion audit closes the required acceptance.

## Context

The authority migration is complete. Its source disposition, former baseline,
reviews and one-off merge approval remain historical evidence in the Task and
Git; they are not work to repeat. ADR-0036 is the current structural decision.
The approved follow-up extends SPEC-0072 to native lint/commit configuration,
formatting coverage, full-tree secrets, diagnostic privacy and duplicate gates.
Re-observe Git before writes and preserve the original checkout and its index.

## Goals & In-Scope

Correct the observed defects through existing owners: common governance,
provider adapters, validation registry/runner, pre-commit/native tool config,
independent tests, current docs and the hosted QA adapter. Preserve the shared
full/ci gate set, required checks and domain verification boundaries.

## Non-Goals & Out-of-Scope

No new registry, QA wrapper, fixture framework, policy engine, provider model
change or live manifest behavior. No push, PR, dispatch, release/tag,
credentials, paid calls, global settings or live infrastructure actions. The
earlier local merge of updated origin/main into the task branch is complete.
The later user instruction conditionally approves local main integration and
task-owned branch/worktree cleanup after completion. Protected external actions
still require their own approval.

## Global Constraints

`scripts/qa.py` remains the single supported QA entrypoint. Required-tool,
cancellation, timeout, output and cleanup failures remain FAIL. External
permissions/environment remain DEFER. No history rewrite, arbitrary stash,
blanket restore or hook bypass. Preserve frozen recovery identities and NUL
machine paths. Native configuration does not prove runtime delivery.

## Work Breakdown

### WP-005: Correct bounded process diagnostics

Files: `scripts/run-validation-lane.py`, `tests/test_run_validation_lane.py`.
Keep the escaped tuple's fourth field as a state observation; remove argv reads.

1. Add a failing test that refuses `/proc/*/cmdline` access and observes running,
   zombie, disappeared and malformed states using temporary/mock process data.
2. Use bounded status reads and an allowlisted state letter; retain `comm`, PID,
   group and cleanup limits. Preserve updated main's exclusion of confirmed
   terminated states; unknown states still fail closed. Read state once for
   both classification and diagnostics. Remove synthetic token-only tests.
3. Run `python3 -B -m unittest tests.test_run_validation_lane` and inspect the
   diagnostic diff. Preserve timeout, cancellation and descendant regressions.

### WP-006: Repair formatting and full-snapshot secret coverage

Files: `.pre-commit-config.yaml`, `.gitleaks.toml`, validation registry,
`tests/test_validation_profiles.py`, `tests/test_validation_tooling_ownership.py`,
`tests/test_qa_runner.py`, and formatting/quality guidance.

1. Reproduce Codex selector omission, shfmt's success-without-check behavior,
   frozen mutation selection and clean-index Gitleaks scan omission.
2. Include both provider shell paths and set shfmt args to `--write -i 2`.
   Preserve Python-only Ruff selection. Resolve frozen exclusion through the
   existing lifecycle owner, retaining current/draft archive coverage.
3. Give full/ci pre-commit explicit `--hook-stage manual`; keep staged native
   Gitleaks and a manual directory-scan hook on the same pin. Skip `.git`
   traversal narrowly; retain all other manual-stage hook coverage.
4. Run targeted selector, stage and snapshot tests, including unchanged tracked
   canary and non-ignored hidden input. Explicit fixes target reviewed paths.

### WP-007: Align commit validation and current guidance

Files: Git/quality policy, commit prompt/provider command, `.cz.toml`,
`.gitmessage`, `cliff.toml`, PR/commit documentation and independent tests.

1. Test valid/invalid candidate messages and stage selection in a temporary Git
   repository using the pinned Commitizen hook. Create no invalid real commit.
2. Remove full-QA/native-hook equivalence claims and workstation policy prose.
   Use infrastructure examples, distinguish enforced syntax from advice, retain
   BREAKING CHANGE footer and document unsupported bang syntax.
3. Put release-chore skip before generic chore; account for supported build,
   deps and release groups. Preserve historical parser compatibility.
4. Test synthetic changelog behavior with the pinned tool when available;
   record missing tool/environment as a visible limitation.

### WP-008: Remove demonstrated duplication

Files: `scripts/validate-harness.sh`, its current README/PR/fixture consumers,
`scripts/validation/repository/quality.py`, independent test modules,
`.pre-commit-config.yaml`, `.hadolint.yaml`, formatting guidance.

1. Inventory current wrapper consumers and its seven domain gate contracts.
   Point consumers at full QA; remove repeated infrastructure validation.
2. Move embedded heading/table and generic-residue synthetic probes into tests.
   Keep actual production rule functions and independent negative diagnostics.
3. Confirm no Dockerfile target, remove unused hadolint hook/config and repair
   current references. Preserve historical references and Git recovery.
4. Run ownership/profile and transferred-probe tests. Record removed call
   counts; do not claim measured wall-time savings without measurements.

### WP-009: Validate environment, workflows and final handoff

Files: `.github/workflows/ci.yml`, workflow tests, scripts/QA documentation and
this package's Task. Other workflows change only for observed defects.

1. Check local OS/Python/tools, interpreter fallback and trusted caches. Reuse
   hash-locked CI dependencies in an isolated environment when feasible;
   preserve closed HOME/PATH and avoid cold-cache pressure on this workstation.
2. Correct resolver documentation and cache identity where evidence requires.
   Preserve named checkout/history, single QA job and fail-closed ci-summary.
3. Run focused workflow tests for PR, push, dispatch and failure/cancel/skip;
   contract-test full/ci equality instead of rerunning equivalent profiles.
4. Complete independent read-only review and the sequence below. Record actual
   results, limits, rollback and next owner in the Task. Keep WORK-004 open for
   external acceptance that local evidence cannot establish.
5. Re-observe public hosted results and available native client capabilities.
   Obtain the existing protected-action approvals before publishing the task
   branch, dispatching CI or invoking an authenticated Provider session. Keep
   upstream runs separate from evidence for this implementation.
6. Once required acceptance is complete, verify main and the task branch are
   clean and current, merge locally, validate any changed integration input,
   then remove only this task-owned worktree and its merged branch. Preserve
   both while a required result is missing; do not auto-pull or rewrite history.

## Verification Plan

For each changed behavior, targeted RED then GREEN. During work run quick;
before each logical commit inspect status/diffs, stage explicit paths, inspect
cached diff, run both diff checks and exact staged QA, then validate the actual
message and use normal active hooks. Related contract/implementation/tests
travel together; no arbitrary commit count target.

Run full QA over the final working tree before handoff. Its discovery and
pre-commit gate are not repeated on identical bytes. If fixes alter bytes,
review/restage and refresh affected evidence. Record subsequent Task-only
changes with scoped document checks; do not create a self-SHA/full-run loop.
Measure targeted invocation/setup/snapshot/gate timing and cache identity.
Cold installation, hosted/native/live results require their own environment;
no absent measurement is a performance claim or PASS.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| User work is mixed into commits | Separate worktree from observed HEAD; preserve original index |
| Security scan or formatter input shrinks | Synthetic stage/lifecycle/path tests and explicit owner review |
| Removal loses a diagnostic | Move tests before removal; map consumers and unique domain gates |
| Tool installation or active hooks fail | Keep changes; report exact blocker without bypass/global changes |
| Rollback reopens a defect | Forward revert reviewed logical commits with paired config/tests/consumers |

## Completion Criteria

All applicable local acceptance passes with independent review disposition and
logical local commits. Required failures remain incomplete. Hosted, native and
live evidence stay separate with next owners. Required hosted/native acceptance
must close before the newly selected local main integration and cleanup.
Remote writes still require separate authorization. The Task preserves the completed
migration and current limits.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGQ-001](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-002](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-003](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-004](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-005](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-006](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-007](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-008](spec.md#success-criteria--verification-plan) | WP-009 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-009](spec.md#success-criteria--verification-plan) | WP-007 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-010](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-011](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-012](spec.md#success-criteria--verification-plan) | WP-006 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-013](spec.md#success-criteria--verification-plan) | WP-005 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-014](spec.md#success-criteria--verification-plan) | WP-008 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
