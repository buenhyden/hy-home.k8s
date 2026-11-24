---
title: "Forecast Consumer Link Task"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-11-24"
artifact_id: "SPEC-0234-TSK-0001"
parent_ids: ["SPEC-0234-PLAN-0001"]
---

# Task: Forecast Consumer Link

## 문서 개요

### 목적과 독자

This Task records the P11 execution and evidence for the [Plan](../plan.md)
and [Spec](../spec.md). The operator and reviewers use it to separate module
behavior, the live forecast round trip and criterion acceptance.

### 책임과 적용 범위

WORK-001 serves AC-0001 and AC-0002. This Task owns P11 work state, results
and criterion decisions.

## 내용 계약

### 입력과 전제

The operator entered `prompts/P11-FORECAST.md` from package
`workspace_governance_remediation_1_2_0_20261123` (`package_version: 1.2.0`)
on 2026-11-24, authorizing bounded implementation, verification and
commit, push, pull request and merge. Intake found branch `main` at
`bdb2d39b3e187fa11968fc609cda05e6baa75775` with a clean worktree. Earlier
packages are not re-executed.

### 본문과 규칙

#### Scope

##### Objective and Parent

WORK-001 executes the [Plan work unit](../plan.md#work-units) for the two
[Spec criteria](../spec.md#criteria).

##### Inputs and Authority

The current user P11 message is the scoped request reference; EVD-001
records the execution receipt. The Spec and Plan stay `draft`; the receipt
grants no formal approval or criterion acceptance.

- **Allowed Paths**: the [Plan WORK-001](../plan.md#work-units) write scope and this workspace's forecast store.
- **Forbidden Paths**: other repositories, the user's provider configuration, and P12–P17.
- **Approval Required**: none beyond the current P11 request for ordinary Git delivery.
- **Static Validation**: forecast regressions and staged QA.
- **Live Validation**: one forecast round trip in the live store and its score.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: revert the commit; the store never rewrites rows.
- **Evidence Location**: this Task's Results.

#### Execution Log

##### Work Performed

`scripts/work_forecast.py` and its 14 regressions are kept unchanged: they
already refuse unordered, negative and non-finite quantiles, count only
earlier completed runs of the same group as the sample, keep cancelled,
failed and incomplete runs censored, report coverage and pinball loss with
N, and label every forecast uncalibrated. No hook, QA lane or CI job reads
the store, so no forecast gate exists. SDLC-R038 now states that P80 is a
completion probability and not progress, that the task reference names the
work unit and the request whose brief it serves, and that a final cutover
sets the store aside so the new baseline starts at N=0. This change itself
was forecast as record 20 after its brief was recorded and before its first
repository change.

##### Blockers and Decisions

No calculator change is made: the derived requirement to show a small
sample is met by the stored sample size, the required assumptions text and
the `uncalibrated` label, and a fixed small-sample threshold would claim
what N cannot. Residue W10-H01 stays open: the Codex account quota is used
up until 2026-11-27, so no Codex round trip was attempted.

##### Lifecycle Traceability

| Item | Upstream criterion | Result | Evidence |
| --- | --- | --- | --- |
| WORK-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | PASS | Regressions pass (EVD-002); record 20 fixed and started (EVD-003); hosted checks pass (EVD-004); record 20 finished and scored (EVD-005) |

#### Verification Evidence

##### Results

| Evidence ID | Criteria | Work Unit | Method | Input | Tool and Config | Command | Exit | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | observation | {"actor":"user","approval_ref":"Current human P11-FORECAST.md request of 2026-11-24 in this conversation for package workspace_governance_remediation_1_2_0_20261123, bounded implementation, verification and commit/push/PR/merge","scope":["SPEC-0234","SPEC-0234-PLAN-0001","SPEC-0234-TSK-0001"],"reviewed_spec_sha256":"ba15dd58a123f1379b22bb309bcb55388777def1c85bf3d322ce772f78ea6fe4","reviewed_plan_sha256":"1b8c4fbae2d9995ce4f77b84a68c2291b95137ed4474258e4f5c740fc2660235","request_revision":"fc2424a4e3f10220c6488ed450a8994bcfd2fa4e1e75aff789f2fceaffaff677","validity":"confirmed","revocation":"none"} | Current trusted human request; request revision is the validator-defined digest of this Task's scope and work items; exact draft parent hashes | Scoped execution approval | none | PASS | Records the current P11 execution scope only; no formal Spec or Plan approval or criterion acceptance follows | true | none |
| EVD-002 | [AC-0001](../spec.md#criteria) | WORK-001 | automated | Unchanged `scripts/work_forecast.py` at `bdb2d39b` | Pinned validation venv, `unittest` | `python -m unittest tests.test_work_forecast` | 0 | PASS | 14 tests OK: quantile order and NaN refusal, censoring, earlier-only sample, coverage and pinball, immutability, clock order | true | none |
| EVD-003 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | Live `.workspace-memory/forecast.sqlite3`, 19 records before; the brief of request `006d2ca4bea0dc52` recorded first | `scripts/work_forecast.py` | `forecast` with task reference `SPEC-0234 WORK-001 request 006d2ca4bea0dc52`, `governance-prompt`, `elapsed`, `minutes`, P30 40, P50 60, P80 100; then `start 20` | 0 | PASS | Record 20, digest `e8c05b1685c4ad963cf3bf456ecf5915b2325b04b8fdd3cac1b706219e8f3600`, sample size 3, `uncalibrated`; started 2026-11-24T03:34:35.991889Z before the first repository change; end definition is the merge of the P11 pull request | true | none |
| EVD-004 | [AC-0001](../spec.md#criteria), [AC-0002](../spec.md#criteria) | WORK-001 | observation | Pull request #358, head `9bdf126b` | GitHub Actions CI run 45321783910; GitGuardian | Hosted pull request checks | 0 | PASS | ci-summary, style-pr (5 min 15 s), label, greeting and GitGuardian passed | true | none |
| EVD-005 | [AC-0002](../spec.md#criteria) | WORK-001 | observation | Record 20 after pull request #358 merged as `0e491835` | `scripts/work_forecast.py` | `finish 20 completed`; `score` | 0 | PASS | Finished 2026-11-24T04:02:05.165471Z, completed, elapsed actual 27.486226 minutes from the tool clock, below its P30 of 40. The `governance-prompt`/elapsed/minutes group now has N=4, nothing censored, open or unstarted, coverage P30 0.75, P50 0.75, P80 1.0 and pinball loss P30 11.26, P50 17.16, P80 15.85; the score stays descriptive only and uncalibrated | true | none |

##### Resolution Links

None yet.

#### Acceptance Decision

##### Criterion Decisions

| Criterion | Intent | Acceptance | Evidence | Decision | Accepted By | Current Owner | Reassigned To |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-0001](../spec.md#criteria) | accept | pending | EVD-002, EVD-004 | Awaiting the operator's decision | none | platform | none |
| [AC-0002](../spec.md#criteria) | accept | pending | EVD-003, EVD-004, EVD-005 | Awaiting the operator's decision | none | platform | none |

##### Remaining Conditions

Record 20 was finished and scored after pull request #358 merged (EVD-005);
one run in a group of four is no calibration. Hosted checks passed (EVD-004).
W10-H01 waits for a Codex session after 2026-11-27.

#### Handoff

##### Promotion Receipt

P11-FORECAST-RULE: [SDLC-R038](../../../00.workspace/03.process/sdlc.md)
states the changed forecast rule.

##### Next Owner

The platform owner records the finish, score and hosted results; the
operator decides the criteria. The next package input is
`prompts/P12-PARALLEL.md`; this Task does not run it.

## 적용과 확인

### 적용 방법

Use this Task for P11 evidence and leave criteria pending until the operator
records decisions.

### 확인 기준

Module behavior is repository-static evidence; EVD-003 shows the live store.

## 관계와 출처

### 관련 문서

| Relation | Target |
| --- | --- |
| requires | [SPEC-0234 Plan](../plan.md) |
| verifies | [SPEC-0234](../spec.md) |

### 외부 근거

Design D11 is a dated input; no external standard is adopted.
