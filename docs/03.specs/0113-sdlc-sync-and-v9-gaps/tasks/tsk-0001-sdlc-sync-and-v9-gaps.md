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

Execute the six work units of the [Plan](../plan.md) for
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
| WORK-001 | [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | Correct stale requirements, architecture and Spec text | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | Frozen-exclusion cross-check test and fix recipe | platform | completed | PASS | EVD-011 |
| WORK-003 | [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | Four F05 claim statuses in the Stage 99 README | platform | completed | PASS | EVD-010 |
| WORK-004 | [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | F18 evidence correction | platform | completed | PASS | EVD-008 |
| WORK-005 | [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | Remove the stale `.hadolint.yaml` route | platform | completed | PASS | EVD-007 |
| WORK-006 | [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | `AGENTS.md` common and Codex-only blocks | platform | completed | PASS | EVD-009 |

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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SYNC-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-SYNC-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-011 | Accept the Registry cross-check and the explicit fix recipe | platform |
| [VAL-SYNC-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-010 | Accept the four separate claim statuses | platform |
| [VAL-SYNC-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Accept the correction record | platform |
| [VAL-SYNC-005](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Accept the route removal; reintroduction now fails closed | platform |
| [VAL-SYNC-006](../spec.md#success-criteria--verification-plan) | accepted | EVD-009 | Accept the common and Codex-only blocks; a native split stays unverified and out of scope | platform |

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
  implementation on 2026-10-13 after reviewing the draft at `535d8c11`;
  push, pull request and merge await the operator.
- **Static Validation**: focused tests, document validators and staged QA
  from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
