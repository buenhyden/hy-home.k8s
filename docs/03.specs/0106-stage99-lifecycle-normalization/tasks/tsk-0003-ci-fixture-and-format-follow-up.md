---
title: "Hosted Fixture and Formatting Compatibility"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0003"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Hosted Fixture and Formatting Compatibility

## Overview

This follow-up owns [VAL-P02-003](../spec.md#success-criteria--verification-plan)
and [WORK-003](../plan.md#work-breakdown). PR 133 exposed historical fixture,
formatting and scanner failures after local P01 acceptance. Completed parent
and original Task evidence retain their historical meaning. Completion here
records local acceptance; remote and integrated-main outcomes need separate
observed evidence.

## Inputs

- The current user's work-unit commit, push and merge instruction authorizes
  necessary bounded forward repairs and normal delivery. The owning workflow
  assigns these paths to one repo-tooling-engineer; preserve other workers.
- Clean starting `codex/p01-authority-evidence` at
  `df3281d06a931bff6784bcc462800fab23bbb1c9`, based on main
  `9067729bf6679a0cd536362113be261056c32dd6`. P02 preserves its own inputs.
- [Stage 99 Task form](../../../99.templates/templates/specs/task.template.md),
  [Registry](../../../99.templates/registry.json) and
  [quality policy](../../../../.agents/governance/quality.md).
- Successful main CI run `36966489221` checked
  `997aa67d4a7ddb5dcdecf7048a68900155178231`. Its comparison to this intake
  selected 221 existing changed tracked paths for bounded diagnosis.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-003 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | Restore historical fixture and scoped formatting/scanner compatibility | repo-tooling-engineer | frontmatter | NOT_RUN | pending | [Verification Summary](#verification-summary) |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-020 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Hosted required failure | Head `df3281d0…`; checked merge `e972e787…`; run `37278597507` | FAIL | [Observed failure](#observed-failure) | pending |
| EVD-P02-021 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Historical fixture RED and schema diagnosis | Intake head; one named test and synthetic schema comparison | FAIL | [Focused diagnosis](#focused-diagnosis) | pending |
| EVD-P02-022 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Corrected fixture, missing-object refusal and focused hooks | Implementation pending | NOT_RUN | Pending | pending |
| EVD-P02-023 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Exact-index staged/message and semantic checks | Logical indexes pending | NOT_RUN | Pending | pending |
| EVD-P02-024 | [VAL-P02-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Final local completion and remote disposition | Terminal candidate and corrected hosted input pending | NOT_RUN | Pending | pending |

## Approval and Safety Boundaries

- **Allowed Paths**: `tests/archive_generation_fixture.py`, `tests/test_archive_generation_fixture.py`, `tests/test_generic_migration_recovery.py`, `tests/test_archive_cutover.py`, `tests/test_provider_guard_registry_generation.py`, `tests/README.md`, `docs/02.architecture/decisions/0033-common-document-contract-v9.md`, this Spec/Plan/Task and original `tsk-0001-lifecycle-normalization.md` only for its diagnosed Markdown formatting correction.
- **Forbidden Paths**: Production Registry/schema and validator/gate behavior, scanner baseline/configuration, frozen Archive, old Task facts, native/provider state, secrets, live resources and unrelated changes.
- **Approval Required**: The current user instruction authorizes scoped commits, feature push, PR update and normal merge after required hosted checks. The owning workflow verifies the trusted interaction before protected delivery; this Task claims no actor authentication or revocation result. Force push, rebase, cleanup, branch deletion and worktree removal remain outside scope.
- **Static Validation**: Focused RED/GREEN and historical helper missing-object refusal; focused pinned hooks; exact-index staged and actual message checks for four normal commits; final completion and independent review. Local affected and full execution NOT_RUN under the scoped exclusion. Required hosted PR checks precede merge; integrated-main checks follow merge before integration acceptance.
- **Live Validation**: DEFER — not requested; static and hosted QA establish no runtime activation.
- **Secret / Vault Handling**: No private value reads or output. Only two verified Git fixture identities receive inline annotations; no baseline/configuration update.
- **Rollback Plan**: Reviewed forward corrective commit or forward revert; preserve both worktrees and history.
- **Evidence Location**: This Task; safe structured receipts may remain in temporary scratch without becoming another progress authority.

## Verification Summary

### Observed failure

[PR 133](https://github.com/buenhyden/hy-home.k8s/pull/133) remains open.
[CI run 37278597507](https://github.com/buenhyden/hy-home.k8s/actions/runs/37278597507)
attempt 1 checked merge `e972e7872f8bdd4abf0d6219566381f9c93f1fb3`
for head `df3281d06a931bff6784bcc462800fab23bbb1c9`.
QA job `111661118879` and required summary `111666449249` failed;
required provenance was not observed. Unit tests and pre-commit failed;
the other complement validators, branch policy and isolated QA passed.
No merge, remote rerun, local ref update or gate bypass was performed.
Safe hosted receipt `/tmp/hy-p01-ci-run37278597507-safe-receipt.json`
has SHA-256 `f22b7b9c14aecae73566ef3957cdf1c42a5b8e1e82068720280839b2fc573c60`.
Only bounded redacted diagnostics survived; no artifact was uploaded.

### Focused diagnosis

On the disposable exact-head clone the canonical bounded runner executed
only `python3 -B -m unittest
tests.test_affected_surface_migration.RetiredSurfaceSelectionTest.test_composed_successor_is_classified_once_at_its_terminal -v`.
It returned 1 with `REGISTRY_SCHEMA`, `ARCHIVE-MIGRATION-PROFILE` and
`SURFACE-MIGRATION-PROOF`. The synthetic frozen Registry has one
current-schema `const` error at `schema_version`; its matching historical
schema at `c652331ce1c6bfddf1e670c748ce1a04b3835c33` has zero errors.
Only the generic migration fixture mixes generations. Other inspected legacy
consumers use a typed frozen Registry or matching current Registry/schema.

Focused Markdown found four diagnostics across three paths: ADR-0033 line 180
has two MD050 errors; original P02 Task line 646 has MD037; `tests/README.md`
line 31 has MD001. Python formatting changed only
`tests/test_provider_guard_registry_generation.py` in the disposable clone.
The security reviewer classified scanner findings at
`tests/test_archive_cutover.py` lines 66 and 225 as actual Git commit objects;
only their inline annotations may change.

Safe receipts remain under `/tmp/hy-p01-diagnostic-joka0i9i/`:
`focused-test-safe-receipt.json`, `fixture-schema-safe-receipt.json`,
`post-green-markdownlint-cli2-safe-receipt.json` and
`post-green-ruff-format-safe-receipt.json`. Raw logs and matched scanner values
were neither printed nor retained. Implementation, staged/message, completion
and independent review remain NOT_RUN/pending at draft intake. Local full and
affected execution remain NOT_RUN. Hosted delivery is blocked; next owners
are writer, quality-engineer and independent reviewer, then delivery executor.
