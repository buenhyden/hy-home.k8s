---
title: "Linked Run Observation Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0236-TSK-0001"
parent_ids: ["SPEC-0236-PLAN-0001"]
---

# Task: Linked Run Observation

## 문서 개요

### 목적과 독자

This Task records the P13 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate module
behavior, live observation and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 through AC-0004. This Task owns P13 work state,
results and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P13-OBSERVABILITY.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`e45125dc28720279dc2e54fd38289512991caa82` with a clean worktree. Earlier
packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the four
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P13 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope; the live stores are read only.
- **Forbidden Paths**: other repositories, the user's provider configuration, and P14–P17.
- **Approval Required**: none beyond the current P13 request for ordinary Git delivery.
- **Static Validation**: join, analysis and dispatcher regressions, Ruff and staged QA.
- **Live Validation**: one read-only join per key and the candidate 1 recheck read.
- **Secret / Vault Handling**: no secret is read or printed; the join reads no transcript or provider output.
- **Rollback Plan**: revert the commit; no store schema changes.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

`scripts/work_observe.py report --key` reads, without writing, the forecast
records (through their own digest check), the parallel run reports and the
promoted analysis candidates whose task reference names the key, and lists
each missing source as null with its reason. `session_analysis.py
candidates` now reports `effect` (`recurred`, `met`, `unobserved` with a
reason or `not-tracked` with a reason) instead of `acceptance`, a label that
read like the user's acceptance. `work_parallel.py` reports
`cost_estimate_usd`, the CLI's own figure, with `charge_usd` null and a
note, and deletes a provider worker's raw output after collection, on
success, failure, timeout and cancel. The join is registered as
`work-observe-regressions` with its two surfaces. CTX-R023, the delegated
development workflow and the scripts index describe the change. W10-H04 is
closed in the SPEC-0223 Task (its EVD-045) and the ledger.

##### Blockers and Decisions

No new store, dashboard or copy of hosted CI logs is made: CI leaf timing
stays in the GitHub run log and is cited by run ID. The P12 run reports were
deleted during the P12 cleanup, so the join finds no parallel record for
SPEC-0235; its facts remain in that Task's EVD-005 and EVD-008, and from now
on the report is kept as the run's local fact source. Holds that remain open,
with owners: the first scheduled firing of the per-workspace timer on
2026-11-25 03:00 KST (SPEC-0233 owner), the Codex request brief observation
(SPEC-0231, EVD-008) and the Codex worker run (SPEC-0235 AC-0004, W10-H02),
both blocked by the account usage limit until 2026-11-27 12:53, and P95 and
billed cost, which stay null. Candidate 1 recurred on 2026-11-23; that is an
analysis fact for later review, not a failure hidden as unobserved.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | PASS | Regressions pass (EVD-003); live join (EVD-004); W10-H04 closed (EVD-005); hosted checks pass (EVD-006) |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P13-OBSERVABILITY.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0236","SPEC-0236-PLAN-0001","SPEC-0236-TSK-0001"],"reviewed_spec_sha256":"b24c09ee1257075b2c934750de8809fc584b573b5e46aa66b7418d4086824806","reviewed_plan_sha256":"015a58d84f2b65a5e5af6d77e4b6c8e0ad96d05573a83af5cab811229da8f0de","request_revision":"681b6faf8d3e6abd6f6ac2162cce2617758514e1ee6e3fda197154bbe9dc73d7","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P13 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | automated | Rewritten effect, cost and raw-output assertions and the new join module test, before the code change | Pinned validation venv, `unittest` | `python -m unittest tests.test_session_analysis`; `python -m unittest tests.test_work_parallel.ProviderPlanTest tests.test_work_parallel.ContainmentTest`; `python tests/test_work_observe.py` | 1 | FAIL | Failing-first: analysis 4 errors, dispatcher 3 errors, join module missing | false | none |
| EVD-003 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria) | WORK-001 | automated | Working tree after the change | Pinned validation venv, `unittest`; Ruff; affected-surface contract | `python -m unittest tests.test_session_analysis tests.test_work_parallel tests.test_work_observe`; `ruff check`; `scripts/validate-affected-surfaces.py --root .` | 0 | PASS | analysis 31, dispatcher 49 and join 4 tests OK, including null reasons, no store creation, key boundary `SPEC-0235` against `SPEC-02350`, effect states and reasons, and no `.out` after success or timeout; Ruff clean; surface contract PASS with the new gate in both local profiles | true | none |
| EVD-004 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | observation | Live `.workspace-memory` stores and `.workspace-test/parallel`, 2026-11-24 | Changed working-tree code | `scripts/work_observe.py report --key SPEC-0234`, `--key SPEC-0235`, `--key SPEC-0161` | 0 | PASS | SPEC-0234: forecast 20 completed in 27.486226 elapsed minutes against P30 40, P50 60, P80 100, other sources null with reasons. SPEC-0235: all three sources null with reasons (its run reports were deleted in P12). SPEC-0161: 17 completed forecasts and candidate 1 with effect `recurred`; no parallel record. No store was created | true | none |
| EVD-005 | [AC-0004](../spec.md#criteria) | WORK-001 | observation | Live `.workspace-memory/analysis.sqlite3`; runs 16 to 20 | `scripts/session_analysis.py` | `session_analysis.py candidates` for candidate 1 | 0 | PASS | Rechecks 2026-11-20 `met` (0 failures, 2 sessions) and 2026-11-23 `recurred` (106 failures, 3 sessions); W10-H04 closed as SPEC-0223 EVD-045 and the ledger entry made terminal | true | none |
| EVD-006 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria), [AC-0003](../spec.md#criteria), [AC-0004](../spec.md#criteria) | WORK-001 | observation | Pull request #361, head `92593519` | GitHub Actions CI run 45336381341; GitGuardian | Hosted pull request checks | 0 | PASS | ci-summary, style-pr (9 min 11 s, including the affected regressions), label, greeting and GitGuardian passed | true | none |

##### Resolution Links

EVD-002 was a planned failing-first result, not a required failure; EVD-003
shows the passing state.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | pending | EVD-003, EVD-004, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0002](../spec.md#criteria) | accept | pending | EVD-003, EVD-004, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0003](../spec.md#criteria) | accept | pending | EVD-003, EVD-006 | Awaiting the operator's decision | none | platform | none |
| [AC-0004](../spec.md#criteria) | accept | pending | EVD-005, EVD-006 | Awaiting the operator's decision | none | platform | none |

##### Remaining Conditions

Hosted checks passed (EVD-006). The open holds named under Blockers and
Decisions stay with their owners.

#### Handoff

##### Promotion Receipt

P13-RUN-OBSERVATION: CTX-R023 of the
[context and memory policy](../../../../.agents/governance/context-and-memory.md)
states the candidate effect and the read-only join.

##### Next Owner

The platform owner records hosted results; the operator decides the
criteria. The next package input is `prompts/P14-K8S.md`; this Task does not
run it.

## 적용과 확인

### 적용 방법

Use this Task for P13 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Module behavior is repository-static evidence; EVD-004 and EVD-005 show the
local stores.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0236 Plan](../plan.md) |
| verifies | [SPEC-0236](../spec.md) |

### 외부 근거

Design D13 is a dated input; no external standard is adopted.
