---
title: "Task Status Derivation and Provider Boundaries"
version: "1.0.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0108-TSK-0001"
parent_ids: ["SPEC-0108-PLAN-0001"]
---

# Task: Task Status Derivation and Provider Boundaries

## Overview

Execute the three work units of the [Plan](../plan.md) for
[SPEC-0108](../spec.md) as separate logical commits and record their
focused, staged and review evidence here.

## Inputs

- [SPEC-0108](../spec.md) and its [Plan](../plan.md).
- Operator selections on 2026-10-13: implement K-P1 and K-P2 first; move
  push and pull-request commands to `ask`; write only a design Spec for the
  shared memory store.
- Base main `57f44c4446e9ad0e9c8ae87e81c1d208aa7f3c8b`, equal to
  `origin/main` at intake.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | README language exception and Korean roles router | platform | completed | PASS | EVD-004 in commit `5285a3c87ce4692a008387422aeb1e6cdc973056` |
| WORK-002 | [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | Claude ask list and exact permission validation | platform | completed | PASS | EVD-005 in commit `2741068d3c50e3170231b57300dc0efb0dac1a94` |
| WORK-003 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | Shared Task status reader and writer retirement | platform | completed | PASS | EVD-006, EVD-007 in commit `9cadabddc0922fd8bf371371cf57427933876093` |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Language tests and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Governance tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Task contract tests and staged QA | WORK-003 commit index | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Language tests and staged QA | `python3 -m unittest tests.test_document_language`: 30 tests with 2 failures and 1 error before the shared predicate, 30 OK after. `python3 scripts/qa.py staged` on the WORK-001 index: 10 selected gates PASS; `selected-style` and `selected-nonstyle` FAIL because the closed QA PATH has no pre-commit, so `~/.local/bin/pre-commit run` in pre-commit and manual stages ran on the same files and passed after refreshing the moved secret-scan baseline line | PASS | This Task; commit `5285a3c87ce4692a008387422aeb1e6cdc973056` | yes | EVD-001 |
| EVD-005 | [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | WORK-002 | Governance tests and staged QA | `python3 -m unittest tests.test_agent_governance`: 58 tests with 1 error before the ask list, 58 OK after; `scripts/validate-agent-governance.py` PASS. Staged QA first failed `repository-quality` on a literal push example in the Spec, which was reworded; the rerun had 8 gates PASS and only the two PATH-limited style gates FAIL; pre-commit and manual stages passed | PASS | This Task; commit `2741068d3c50e3170231b57300dc0efb0dac1a94` | yes | EVD-002 |
| EVD-006 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Task contract tests and staged QA | `OptionalMultiRowStatusTests` failed (import error, then FM-KEYSET) before repair and passed after, with `tests.test_task_summary_derivation` and `tests.test_document_scope_selection` OK. Staged QA on the WORK-003 index: 14 selected gates PASS including lifecycle, links, profiles, archive and Kubernetes gates; only the two PATH-limited style gates FAIL; pre-commit and manual stages passed with no file change | PASS | This Task; commit `9cadabddc0922fd8bf371371cf57427933876093` | yes | EVD-003 |
| EVD-007 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Independent read-only review | A code-reviewer subagent found that an unreadable table let an omitted summary skip the summary check (MEDIUM) and that a non-string status fell back to derivation (LOW); both were fixed with failing-then-passing regressions before commit. A fenced decoy table now fails loudly; SPEC-0106 mentions of the retired writer remain as history | PASS | This Task; commit `9cadabddc0922fd8bf371371cf57427933876093` | yes | none |
| EVD-008 | [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | WORK-003 | Related regression on the clean base | The 3 `GenerationAdmissionTests` and 2 `ApprovedPackageRetentionTests` failures also occur on an unmodified `57f44c4446e9ad0e9c8ae87e81c1d208aa7f3c8b` worktree, so they are pre-existing; the other 219 related tests passed | PASS | This Task | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-TSKSUM-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006, EVD-007 | Accept local derivation, fail-closed reading and writer retirement; hosted CI is not observed | platform |
| [VAL-TSKSUM-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accept the README exception and Korean roles router; eight READMEs stay pending for a later Task | platform |
| [VAL-TSKSUM-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-005 | Accept the validated ask list; native Claude prompting is not observed | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/0109-shared-workspace-memory/`,
  `docs/03.specs/README.md`, `docs/99.templates/`, `scripts/document_*.py`,
  `scripts/validate-{markdown-profiles,links-and-owners,agent-governance}.py`,
  `scripts/validation/registry.json`, `scripts/sync-task-status.py`
  (removal), `.agents/governance/document-authoring.md`,
  `.agents/roles/README.md`, `.claude/settings.json` and the named tests.
- **Forbidden Paths**: frozen Archive payloads, other Spec packages, live
  cluster, Vault and secret material.
- **Approval Required**: the operator selected the scope and the `ask`
  conversion in this session and approved SPEC-0108 and its Plan on
  2026-10-13 after reviewing the result at `d142c250`; push, pull request
  and merge await the operator.
- **Static Validation**: focused unit tests, the four validators named in
  the Spec and `python3 scripts/qa.py staged` per commit.
- **Live Validation**: DEFER — no live surface is touched; native Claude
  prompting for `ask` entries and hosted CI are not observed.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

All three work units passed focused before/after tests, exact-index staged
QA and local pre-commit, with one independent review on the riskiest unit.
Limitations: the closed QA PATH cannot run the two style gates, so
pre-commit ran them directly; five related test failures are pre-existing on
the clean base; native `ask` prompting, hosted CI, push and pull request are
not executed. Residual risk: the eight pending READMEs remain English until a
later Task translates them. Next owner: the operator for push, pull request
and merge; platform for the pending READMEs and SPEC-0109 review.
