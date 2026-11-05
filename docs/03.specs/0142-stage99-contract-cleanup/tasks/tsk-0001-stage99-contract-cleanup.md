---
title: "Stage 99 Contract Cleanup"
version: "0.4.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0142-TSK-0001"
parent_ids: ["SPEC-0142-PLAN-0001"]
---

# Task: Stage 99 Contract Cleanup

## Overview

Remove the stale and unused items the 2026-11-05 Stage 99 audits found. It
executes [SPEC-0142](../spec.md) through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-05): check `docs/99.templates/` against its governance,
  forms and the current repository, correct conflicts, and remove
  contradictions and repetition inside each file.
- Operator choice (2026-11-05): commit the Stage 05 and Stage 90 work first
  (`c1bbde2e`, `90c15f94`) and take the low-risk cleanup scope.
- Start: branch `docs/requirements-conformance` at `90c15f94`.
- Approval (2026-11-05): the operator's choice of the low-risk cleanup scope
  approves SPEC-0142 and its Plan after review of the draft in `6442183c`. It
  authorizes the repository change only.
- Correction (2026-11-05): the ADR form uses visible placeholders instead
  of comment-only cells (EVD-007); the Spec's Contracts state it.
- Acceptance (2026-11-06): the operator accepted VAL-S99-001 to VAL-S99-004
  and asked for a push and a pull request.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | Stage 00 promotion target and wording | platform | completed | PASS | EVD-005, EVD-006 |
| WORK-002 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | ADR form trace cells | platform | completed | PASS | EVD-007, EVD-008 |
| WORK-003 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | Unused modes, branches, definition and language entry | platform | completed | PASS | EVD-009, EVD-010 |
| WORK-004 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | Stage 99 README and AGENTS prose | platform | completed | PASS | EVD-011 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Lifecycle regression test | Pending | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template and profile checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Schema regression test and code search | Pending | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Document contract suite and strict document checks | Pending | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | WORK-001 | `python3 -m unittest tests.test_task_execution_contract -k retired_stage_00` before the code change | Working tree on `38ed864f` with the new test | FAIL | 2026-11-05T14:53Z, `AssertionError: 'PLAN-PROMOTION' not found in set()`, as expected | no | none |
| EVD-006 | [VAL-S99-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Lifecycle regression test | Staged change on `38ed864f` | PASS | 2026-11-05T14:53Z, `tests.test_task_execution_contract` 30 tests OK; the Plan form and governance text name `.agents/` and Stages 01, 02 and 05 | yes | EVD-001 |
| EVD-007 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | WORK-002 | `validate-markdown-profiles.py --mode strict` with comment-only cells | Working tree on `38ed864f` | FAIL | 2026-11-05T14:53Z, `BODY-CONTRACT-CELL` for `Affected Spec` and `Replacement relation`; visible placeholders were used instead | no | none |
| EVD-008 | [VAL-S99-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template and profile checks | Staged change on `38ed864f` | PASS | 2026-11-05T14:55Z, strict Markdown-profile and link checks PASS with the placeholder cells | yes | EVD-002 |
| EVD-009 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | WORK-003 | `python3 -m unittest tests.test_document_terminal_contract -k five_current_modes` before the code change | Working tree on `38ed864f` with the new test | FAIL | 2026-11-05T14:56Z, schema accepted modes `evidence` and `generated`, as expected | no | none |
| EVD-010 | [VAL-S99-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Schema regression test and code search | Staged change on `38ed864f` | PASS | 2026-11-05T14:56Z, `tests.test_document_terminal_contract` 34 tests OK; registry strict PASS; no live `evidence`/`generated` mode, `requirementMemberId` or `Agent Harness Requirements`; the baselined finding stays at registry line 5847 | yes | EVD-003 |
| EVD-011 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Document contract suite and strict document checks | Staged change on `38ed864f` | PASS | 2026-11-05T15:07Z, document suite 281 tests OK; registry, Markdown-profile, link and lifecycle strict PASS; `python3 scripts/qa.py staged` 12 gates PASS after `ruff format` | yes | EVD-004 |
| EVD-012 | [VAL-S99-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Independent review of the implementing change | Commit `7ca21393` | PASS | code-reviewer: both new tests fail when their change is reverted; the lifecycle check passes over `HEAD~1..HEAD`; no reader of the removed values remains; the baselined finding stays at line 5847; a doubled blank line in the README and a stale Plan risk sentence are fixed in the closing change | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-S99-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Operator accepted on 2026-11-06 | platform |
| [VAL-S99-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Operator accepted on 2026-11-06 | platform |
| [VAL-S99-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-010 | Operator accepted on 2026-11-06 | platform |
| [VAL-S99-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-011, EVD-012 | Operator accepted on 2026-11-06 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/`, `scripts/validate-document-lifecycle.py`,
  `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`,
  `scripts/document_contracts.py`, `scripts/document_authority.py`, `tests/`,
  `.secrets.baseline`, `.agents/governance/document-lifecycle.md`,
  `docs/03.specs/`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: current document bodies outside the Allowed Paths
- **Approval Required**: the operator's 2026-11-05 request authorizes the
  repository change; push and merge are separate.
- **Static Validation**: document contract suite, strict document checks,
  `python3 scripts/qa.py staged`
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none; only a baseline line number moves
- **Rollback Plan**: revert the implementing commits
- **Evidence Location**: this Task

## Verification Summary

- Repository-static lanes: PASS (EVD-006, EVD-008, EVD-010, EVD-011); each
  regression failed before its change (EVD-005, EVD-009).
- Review: EVD-012 passed; its two cosmetic findings are fixed. The operator
  accepted all four criteria on 2026-11-06.
- Follow-up outside this scope: the `Literal` in `scripts/document_contracts.py`
  and two checks in `scripts/validate-markdown-profiles.py` still name the
  modes `frontmatter-free` and `classification-only`, which no profile or
  schema allows.
- Rollback: revert `7ca21393` and the closing change.
